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
from src.CellML_annotator import visualize_model
from src import cellml
from pyvis.network import Network

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
    model_select = SelectField('Please select the model',choices=[],validators=[DataRequired(message=None)])
    model_name = StringField('Please type the model name', validators=[DataRequired()]) # will not autocapitalize on mobile
    submit = SubmitField('compose new model')
    def __init__(self, model_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_select.choices = model_list

filenames = ['SLCT3V_ss_test_inOne.cellml','SLCT3V_ss.cellml']
foldername = './test/cellml/SLC_SS'
model_fullpath_list = []
model_list = []
pyvis_graph_list = []


for filename in filenames:
    model_fullpath = PurePath(foldername).joinpath(filename)
    model=cellml.parse_model(model_fullpath, True)
    G_model=visualize_model(model,'complete',None)
    pyvis_graph = Network(height="750px", width="100%",directed=True,layout=True)
    pyvis_graph.from_nx(G_model)
    model_list.append(model)
    model_fullpath_list.append(model_fullpath)
    pyvis_graph_list.append(pyvis_graph)
    
math_jason = getEquations_present(model)

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
    form = model_form(pairs)
    message = ""
    if form.validate_on_submit():
        model_name = form.model_name.data
        message = "Model name is " + model_name
    else:
        model_name = ""
    return render_template('index.html', graph="model.png", pairs=pairs, form=form, message=message,math_jason=math_jason)

@csrf.exempt
@app.route("/process",methods=['POST'])
def process():
    data = request.get_json() # retrieve the data sent from JavaScript
    print(data['model_name'])
    print(data['selected_nodes'])
    # process the data using Python code
    nodes =pyvis_graph.nodes
    edges= pyvis_graph.edges
    print(nodes)
    nodes=json.dumps(nodes)
    edges=json.dumps(edges)


    return jsonify(nodes=nodes,edges=edges) # return the result to JavaScript

@app.route("/model/<num>", methods=['GET', 'POST'])
def detail(num):
    if request.method == 'GET':
        nodes =pyvis_graph.nodes
        edges= pyvis_graph.edges
        nodes=json.dumps(nodes)
        edges=json.dumps(edges)
    else:
        nodes = request.form.get('nodes')
        edges = request.form.get('edges')
        nodes=json.loads(nodes)
        edges=json.loads(edges)
        print(nodes)
        print(edges)

    return render_template('model.html', model_name=model_fullpath,nodes=nodes,edges=edges,math_list=math_jason)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=7000, debug=True)