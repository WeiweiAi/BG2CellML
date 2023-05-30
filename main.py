import sys
    # caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, './src')
from flask import Flask, render_template, redirect, url_for,request,jsonify
from flask_bootstrap import Bootstrap5
from src.build_CellMLV2 import getEquations
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
        mml_dom = etree.fromstring(math_c)
        mmldom = tran_c2p(mml_dom)            
        return str(mmldom).replace('·', '&#xB7;').replace('−', '-').replace('<?xml version="1.0"?>', '<?xml version="1.0" encoding="UTF-8"?>')
    
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
selected_components = set() # 

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

@app.route("/", methods=['GET', 'POST'])
def index():
    pairs = []
    for model_index, model_fullpath in enumerate (model_fullpath_list):
        pairs.append((model_index,model_fullpath))
    form = model_form('test')
    selected_components_list = list(selected_components)
    forms=[form]
    for iform in forms:
       if iform.validate_on_submit():
          var_init = iform.var_init.data
          print(var_init)

    return render_template('index.html', graph="model.png", pairs=pairs, selected_components=selected_components_list,forms=forms)

@app.route("/new_model_display", methods=['GET', 'POST'])
def new_model_display():

    pyvis_graph = pyvis_graph_list[-1]
    model=model_list[-1]
    if request.method == 'GET':
        nodes =pyvis_graph.nodes
        edges= pyvis_graph.edges
        nodes=json.dumps(nodes)
        edges=json.dumps(edges)
        math_list = getEquations_present(model)

    return render_template('new_model.html', mmodel_name='aa',nodes=nodes,edges=edges,math_list=math_list)

@csrf.exempt
@app.route("/compose",methods=['POST'])
def compose():
    data = request.get_json() # retrieve the data sent from JavaScript
    model_name = data['model_name']
    print(model_name)
    print(selection_dict)
    new_model = compose_model(model_name,selection_dict)    
    new_G_model=visualize_model(new_model,'complete',None)
    pyvis_graph = Network(height="750px", width="100%",directed=True,layout=True)
    pyvis_graph.from_nx(new_G_model)
    nodes =pyvis_graph.nodes
    edges= pyvis_graph.edges
    pyvis_graph_list.append(pyvis_graph)
    model_list.append(new_model)
        
    return jsonify(nodes=nodes,edges=edges) # return the result to JavaScript

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

@csrf.exempt
@app.route("/process",methods=['POST'])
def process():
    data = request.get_json() # retrieve the data sent from JavaScript
    model_index = data['model_index']
    selected_nodes = data['selected_nodes']
    model=model_list[int(model_index)]
    import_components_dict={}
    bioPro=bioPro_list[int(model_index)]   
    for comp_ref in selected_nodes:
        comp= f"{comp_ref}_{model_index}"
        selected_components.add((model.name(),comp_ref))
        import_components_dict.update({comp:comp_ref})
    selection_dict.update({model:{"components":import_components_dict,"annotation":bioPro}})
    print(selection_dict)
     
     # process the data using Python code
    nodes =pyvis_graph.nodes
    edges= pyvis_graph.edges
    nodes=json.dumps(nodes)
    edges=json.dumps(edges)
    # get back to index.html

    return jsonify(nodes=nodes,edges=edges) # return the result to JavaScript

    # process the data using Python code
   
    

@app.route("/model/<num>", methods=['GET', 'POST'])
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
        return render_template('model.html', model_name=model_fullpath,model_index=num, nodes=nodes,edges=edges,math_list=math_list)
    else:
        nodes = request.form.get('nodes')
        edges = request.form.get('edges')
        nodes=json.loads(nodes)
        edges=json.loads(edges)
        print(nodes)
        print(edges)
        return redirect('/')


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=7000, debug=True)