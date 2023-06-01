import sys
    # caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, './src')
from flask import Flask, render_template, redirect, url_for,request,jsonify
from flask_bootstrap import Bootstrap5
from src.build_CellMLV2 import getEquations,writeCellML_default,checkInits
import os
from pathlib import Path, PurePath
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField,SelectField,SelectMultipleField
from wtforms.validators import DataRequired, Length
import json
from lxml import etree
from src.CellML_annotator import visualize_model,get_bioProcess,RDF_Graph,compose_model
from src import cellml
from pyvis.network import Network
from src.utilities import getCompinfo
import re
from libcellml import Validator

def _dump_issues(source_method_name, logger):
    issues_list = ''
    if logger.issueCount() > 0:
        issue_sum = 'The method "{}" found {} issues:'.format(source_method_name, logger.issueCount())
        issues_list=issues_list+issue_sum+'<br>'
        for i in range(0, logger.issueCount()):
            issuei=logger.issue(i).description()
            issues_list=issues_list+issuei+'<br>'
    return issues_list

def validate_model(model):
    validator = Validator()
    validator.validateModel(model)
    issues_list=_dump_issues("validate_model", validator)
    if issues_list=='':
        issues_list="No issues found!"
    json_issues = json.dumps(issues_list)
    return json_issues

selection_dict = {} # {model1:{'components':{comp:compref,..},"annotation":annotation_dict,...}}


def getEquations_present(model):
    equations = getEquations(model)
    math_jason = []
    xslt = etree.parse("ctopff.xsl")
    tran_c2p = etree.XSLT(xslt)
    def m_c2p(math_c):
        #preff = '{http://www.w3.org/1998/Math/MathML}'
        if '<math ' not in math_c:
            math_c = '<math xmlns="http://www.w3.org/1998/Math/MathML">' + math_c + '</math>'
        # separate the math_c according to <math> and </math>
        math_c_reg=math_c.replace('\n','')
        regex = r'(<math[^>]*>)(.*?)(</math>)'
        math_match = re.findall(regex, math_c_reg)
        math_present = []
        for tuple in math_match:
            submath_c = ''.join(tuple)
            if '<math ' not in submath_c:
                submath_c = '<math xmlns="http://www.w3.org/1998/Math/MathML">' + submath_c + '</math>'

            mml_dom = etree.fromstring(submath_c)
            mmldom = tran_c2p(mml_dom)
            math_present.append(str(mmldom).replace('·', '&#xB7;').replace('−', '-').replace('<?xml version="1.0"?>', '<?xml version="1.0" encoding="UTF-8"?>'))  
                    
        return math_present
    
    for key,value in equations.items():
        math_jason.append((key,m_c2p(value)))
    return math_jason

class model_form(FlaskForm):
    var_init = StringField('Please type the initial value', validators=[DataRequired()]) # will not autocapitalize on mobile
    submit = SubmitField(label='Submit')
    def __init__(self, var_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.submit.label.text = var_name

filenames = ['SLCT3V_ss_test_inOne.cellml','SLCT3_ss_test_inOne.cellml']
foldername = './test/cellml/SLC_SS'
model_fullpath_list = []
model_list = []
pyvis_graph_list = []
bioPro_list = []

for filename in filenames:
    model_fullpath = PurePath(foldername).joinpath(filename)
    model=cellml.parse_model(model_fullpath, True)
    rdf = RDF_Graph()
    rdf_file = model_fullpath.with_suffix('.ttl')
    rdf_g = rdf.parse(rdf_file)
    bioPro=get_bioProcess(rdf_g)
    G_model=visualize_model(model,'complete',bioPro)
    pyvis_graph = Network(height="750px", width="100%",directed=True,layout=True)
    pyvis_graph.from_nx(G_model)
    model_list.append(model)
    model_fullpath_list.append(model_fullpath)
    pyvis_graph_list.append(pyvis_graph)
    bioPro_list.append(bioPro)
    math_list = getEquations_present(model)
   

app = Flask(__name__)
app.secret_key = 'tO$&!|0wkamvVia0?n$NqIRVWOG'
app.config['UPLOAD_FOLDER'] = Path('./templates')
# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)

# The index page
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        pairs = []
        for model_index, model_fullpath in enumerate (model_fullpath_list):
            pairs.append((model_index,model_fullpath))
        selected_components = set() # 
        for model,selected in selection_dict.items():
            for comp,comp_ref in selected['components'].items():
                selected_components.add((model.name(),comp_ref))  
        selected_components_list = list(selected_components)
    
    return render_template('index.html', graph="model.png", pairs=pairs, selected_components=selected_components_list)

@csrf.exempt
@app.route("/compose",methods=['POST'])
# When the user clicks the compose button in the index page, the new model will be composed
def compose():
    data = request.get_json() # retrieve the data sent from JavaScript
    model_name = data['model_name']
    print(model_name)
    print(selection_dict)
    new_model = compose_model(model_name,selection_dict)    
    new_G_model=visualize_model(new_model,'complete',None)
    pyvis_graph = Network(height="750px", width="100%",directed=True,layout=True)
    pyvis_graph.from_nx(new_G_model)
    pyvis_graph_list.append(pyvis_graph)
    model_list.append(new_model)
    full_path=f'./test/cellml/SLC_SS/{model_name}.cellml'
    writeCellML_default(full_path, new_model)
    model_fullpath_list.append(full_path)
    return jsonify(model_name=model_name) # return the result to JavaScript
  
@app.route("/model/<num>", methods=['GET', 'POST'])
# When the user clicks the model name in the index page, the model page will be shown
def detail(num):
    model_fullpath = model_fullpath_list[int(num)]
    pyvis_graph = pyvis_graph_list[int(num)]
    model=model_list[int(num)]
    if request.method == 'GET':
        nodes =pyvis_graph.nodes
        edges= pyvis_graph.edges
        nodes=json.dumps(nodes)
        edges=json.dumps(edges)
        math_list = getEquations_present(model)
        selection_dict.update({model:{"components":{},"annotation":{}}})
        return render_template('model.html', model_name=model_fullpath,model_index=num, nodes=nodes,edges=edges,math_list=math_list)
    else:
        return redirect('/')
    
@csrf.exempt
@app.route("/process",methods=['POST'])
# When the user clicks the submit button in the model page, the selected components will be processed
def process():
    data = request.get_json() # retrieve the data sent from JavaScript
    model_index = data['model_index']
    selected_nodes = data['selected_nodes']
    model=model_list[int(model_index)]
    import_components_dict={}
    bioPro=bioPro_list[int(model_index)]   
    for comp_ref in selected_nodes:
        comp= f"{comp_ref}_{model_index}"
        import_components_dict.update({comp:comp_ref})
    selection_dict.update({model:{"components":import_components_dict,"annotation":bioPro}})
    print(selection_dict)
     
    return jsonify('success') # return the result to JavaScript

# The new model page
@app.route("/new_model", methods=['GET', 'POST'])
def new_model():
    if request.method == 'GET':
        pyvis_graph = pyvis_graph_list[-1]
        model=model_list[-1]
        nodes =pyvis_graph.nodes
        edges= pyvis_graph.edges
        nodes=json.dumps(nodes)
        edges=json.dumps(edges)
        math_list = getEquations_present(model)
        noInit, multipleInit_summary = checkInits(model)
        var_noInit_forms=[]
        for var in noInit:
            form = model_form(var)
            var_noInit_forms.append(form)

    for iform in var_noInit_forms:
       if iform.validate_on_submit():
          var_init = iform.var_init.data
          print(var_init)    

    return render_template('new_model.html', forms=var_noInit_forms, mmodel_name='aa',nodes=nodes,edges=edges,math_list=math_list)

@csrf.exempt
@app.route("/validation",methods=['POST'])
def validation():
    data = request.get_json() # retrieve the data sent from JavaScript
    model=model_list[-1]
    json_issues= validate_model(model)

    # get back to index.html

    return jsonify(json_issues=json_issues) # return the result to JavaScript

@csrf.exempt
@app.route("/update_init",methods=['POST'])
def update_init():
    data = request.get_json() # retrieve the data sent from JavaScript
    model=model_list[-1]
    json_issues= validate_model(model)

    # get back to index.html

    return jsonify(json_issues=json_issues) # return the result to JavaScript

@csrf.exempt
@app.route("/add_edge",methods=['POST'])
def add_edge():
    data = request.get_json() # retrieve the data sent from JavaScript
    node_pair = data['new_edge']
    print(node_pair)
    nodes =pyvis_graph.nodes
    edges= pyvis_graph.edges
    # get back to index.html

    return jsonify(nodes=nodes,edges=edges) # return the result to JavaScript

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)