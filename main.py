import sys
    # caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, './src')
from flask import Flask, render_template, redirect, url_for,request,jsonify
from flask_bootstrap import Bootstrap5
import os
from pathlib import Path, PurePath
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField,SelectField,SelectMultipleField
from wtforms.validators import DataRequired, Length
import json
from lxml import etree
from CellML_annotator import visualize_model
from src import cellml
from pyvis.network import Network


xslt = etree.parse("ctopff.xsl")
tran_c2p = etree.XSLT(xslt)

def m_c2p(math_c):
    preff = '{http://www.w3.org/1998/Math/MathML}'
    if '<math ' not in math_c:
        math_c = '<math xmlns="http://www.w3.org/1998/Math/MathML">' + math_c + '</math>'
    mml_dom = etree.fromstring(math_c)
    mmldom = tran_c2p(mml_dom)
        
    return str(mmldom).replace('·', '&#xB7;').replace('−', '-').replace('<?xml version="1.0"?>', '<?xml version="1.0" encoding="UTF-8"?>')


filename = 'SLCT3V_ss_test_inOne.cellml'
foldername = 'C:/Users/wai484/Documents/BG2CellML/test/cellml/SLC_SS'
filename = PurePath(foldername).joinpath(filename)
model=cellml.parse_model(filename, True)
G_model=visualize_model(model,'complete',None)
pyvis_graph = Network(height="750px", width="100%",directed=True,layout=True)
pyvis_graph.from_nx(G_model)

for c in range(model.componentCount()):
    if model.component(c).math()!='':
        xml_mathstring= model.component(c).math()

    else:
        xml_mathstring= ''

math_jason=m_c2p(xml_mathstring)

app = Flask(__name__)
app.secret_key = 'tO$&!|0wkamvVia0?n$NqIRVWOG'
app.config['UPLOAD_FOLDER'] = Path('./templates')
# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)

class model_form(FlaskForm):
    model_select = SelectField('Please select the model',choices=[],validators=[DataRequired(message=None)])
    component_select = SelectMultipleField('Please select the components',choices=[],validators=[DataRequired(message=None)])
    model_name = StringField('Please type the model name', validators=[DataRequired(), Length(10, 40)]) # will not autocapitalize on mobile
    submit = SubmitField('Submit')
    def __init__(self, model_list, component_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_select.choices = model_list
        self.component_select.choices = component_list

model_list = [('model1','model1'),('model2','model2')]
component_list = [('component1','component1'),('component2','component2')]

@app.route("/", methods=['GET', 'POST'])
def index():
    
    form = model_form(model_list,component_list)
    pairs = [(1,'modelname1'),(2,'modelname1')]
    message = ""
    if form.validate_on_submit():
        model_name = form.model_name.data
        message = "Model name is " + model_name
    else:
        model_name = ""
    return render_template('index.html', graph="model.png", pairs=pairs,names=model_name, form=form, message=message,math_jason=math_jason)

@csrf.exempt
@app.route("/process",methods=['POST'])
def process():
    data = request.get_json() # retrieve the data sent from JavaScript
    print(type(data))
    print(data['new_graph'])
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
    form = model_form(model_list,component_list)
    try:
        model = model_list[int(num) - 1]
    except:
        return f"<h1>Invalid value for model: {num}</h1>"
    return render_template('model.html',  graph="model.png",form=form)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=7000, debug=True)