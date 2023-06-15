import sys
    # caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, './src')
from apiflask import APIFlask
from flask import request,render_template
from flask_bootstrap import Bootstrap5
from src.build_CellMLV2 import writeCellML_default,checkInits,addInits, update_varmap
from pathlib import Path, PurePath
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import json
from src.CellML_annotator import visualize_model,get_bioProcess,RDF_Graph,compose_model
from src import cellml
from pyvis.network import Network
from src.utilities import getEquations_present,validate_model_full,parse_model
import os
from src.CellML_builder import writePythonCode

selection_dict = {} # {model1:{'components':{comp:compref,..},"annotation":annotation_dict,...}}


class model_form(FlaskForm):
    var_init = StringField('Please type the initial value', validators=[DataRequired()]) # will not autocapitalize on mobile
    submit = SubmitField(label='Submit')
    def __init__(self, var_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.submit.label.text = var_name

filenames = ['SLCT3V_ss_test_inOne.cellml','SLCT3_ss_test_inOne.cellml']
foldername = './test/cellml/SLC_SS'
model_candidates_N = len(filenames)
# model_candidates_N+1 is the index of the new model; create model_candidates_N+1 empty lists
model_fullpath_list = [None]*(model_candidates_N+1)
model_list = [None]*(model_candidates_N+1)
pyvis_graph_list = [None]*(model_candidates_N+1)
bioPro_list = [None]*(model_candidates_N+1)
new_model_name=''

for index, filename in enumerate (filenames):
    model_fullpath = PurePath(foldername).joinpath(filename)
    model=cellml.parse_model(model_fullpath, True)
    rdf = RDF_Graph()
    rdf_file = model_fullpath.with_suffix('.ttl')
    rdf_g = rdf.parse(rdf_file)
    #rdf_nxg = rdflib_to_networkx_digraph(rdf_g)
    #pyvis_rdf_nxg = Network(height="750px", width="100%",directed=True,layout=True)
    #pyvis_rdf_nxg.from_nx(rdf_nxg) # pyvis_rdf_nxg is the RDF graph presentation, but the labels are the full uri.
    bioPro=get_bioProcess(rdf_g)
    G_model=visualize_model(model,'complete',bioPro)
    pyvis_graph = Network(height="750px", width="100%",directed=True,layout=True)
    pyvis_graph.from_nx(G_model)
    model_list[index]=model
    model_fullpath_list[index]=model_fullpath
    pyvis_graph_list[index]=pyvis_graph
    bioPro_list[index]=bioPro  

app = APIFlask(__name__)
app.secret_key = 'tO$&!|0wkamvVia0?n$NqIRVWOG'
app.config['UPLOAD_FOLDER'] = Path('./templates/files')
Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)

# The index page
@app.get("/")
def index():
    pairs = []
    for model_index, model_fullpath in enumerate (model_fullpath_list):
        if model_index < model_candidates_N:
           pairs.append((model_index,model_fullpath))
    selected_components = set() # 
    for model,selected in selection_dict.items():
        for comp,comp_ref in selected['components'].items():
            selected_components.add((model.name(),comp_ref))  
    selected_components_list = list(selected_components)
    
    return render_template('index.html', graph="model.png", pairs=pairs, selected_components=selected_components_list)

@csrf.exempt
@app.post("/compose")
# When the user clicks the compose button in the index page, the new model will be composed
def compose():
    data = request.get_json() # retrieve the data sent from JavaScript
    new_model_name = data['model_name']
    print(selection_dict)
    new_model = compose_model(new_model_name,selection_dict)    
    new_G_model=visualize_model(new_model,'complete',None)
    pyvis_graph = Network(height="750px", width="100%",directed=True,layout=True)
    pyvis_graph.from_nx(new_G_model)
    pyvis_graph_list[model_candidates_N]=pyvis_graph
    model_list[model_candidates_N]=new_model
    bioPro_list[model_candidates_N]=None
    full_path=f'./test/cellml/SLC_SS/{new_model_name}.cellml'
    model_fullpath_list[model_candidates_N]=full_path
    writeCellML_default(full_path, new_model)

    return {'model_name':new_model_name} # return the result to JavaScript
  
@app.get("/model/<num>")
# When the user clicks the model name in the index page, the model page will be shown
def detail(num):
    model_fullpath = model_fullpath_list[int(num)]
    pyvis_graph = pyvis_graph_list[int(num)]
    model=model_list[int(num)]
    nodes =pyvis_graph.nodes
    edges= pyvis_graph.edges
    nodes=json.dumps(nodes)
    edges=json.dumps(edges)
    math_list = getEquations_present(model)
    selection_dict.update({model:{"components":{},"annotation":{}}})
    return render_template('model.html', model_name=model_fullpath,model_index=num, nodes=nodes,edges=edges,math_list=math_list)
    
@csrf.exempt
@app.post("/process")
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
     
    return 'success' # return the result to JavaScript

# The new model page
@app.get("/new_model")
def new_model():
    if pyvis_graph_list[model_candidates_N] is not None:
       pyvis_graph = pyvis_graph_list[model_candidates_N]
       model=model_list[model_candidates_N]
       model_fullpath=model_fullpath_list[model_candidates_N]
    else: # if the new model is not composed yet, use the first model as the default
        pyvis_graph = pyvis_graph_list[0]
        model=model_list[0]
        model_fullpath=model_fullpath_list[0]
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

    return render_template('new_model.html', forms=var_noInit_forms, mmodel_name='aa',nodes=nodes,edges=edges,math_list=math_list)

@csrf.exempt
@app.post("/validation")
def validation():
    data = request.get_json() # retrieve the data sent from JavaScript
    if pyvis_graph_list[model_candidates_N] is not None:
           model=model_list[model_candidates_N]
           model_fullpath=model_fullpath_list[model_candidates_N]
    else: # if the new model is not composed yet, use the first model as the default
        model=model_list[0]
        model_fullpath=model_fullpath_list[0]
    base_dir = PurePath(model_fullpath).parent.as_posix()
    isValid, issues,issue_details = validate_model_full(model, base_dir)
    # get back to index.html

    return {"json_issues":issues} # return the result to JavaScript

@csrf.exempt
@app.post("/update_init")
def update_init():
    data = request.get_json() # retrieve the data sent from JavaScript
    comp_name = data['comp_name']
    var_name = data['var_name'].split(':')[0]
    init_value = float(data['init_text'])

    if pyvis_graph_list[model_candidates_N] is not None:
           model=model_list[model_candidates_N]
           model_fullpath=model_fullpath_list[model_candidates_N]
           addInits(model,comp_name,var_name,init_value)
           writeCellML_default(model_fullpath, model)
           new_G_model=visualize_model(model,'complete',None)
           pyvis_graph = Network(height="750px", width="100%",directed=True,layout=True)
           pyvis_graph.from_nx(new_G_model)
           pyvis_graph_list[model_candidates_N]=pyvis_graph
           model_list[model_candidates_N]=model
           bioPro_list[model_candidates_N]=None
    else: # if the new model is not composed yet, use the first model as the default
        model=model_list[0]
        model_fullpath=model_fullpath_list[0]
        pyvis_graph = pyvis_graph_list[0]
   
    nodes =pyvis_graph.nodes
    edges= pyvis_graph.edges

    return {'nodes':nodes,'edges':edges} # return the result to JavaScript

@csrf.exempt
@app.post("/connect")
def connect():
    data = request.get_json() # retrieve the data sent from JavaScript
    comp_name_1 = data['comp_name_1']
    var_name_1 = data['var_name_1'].split(':')[0]
    comp_name_2 = data['comp_name_2']
    var_name_2 = data['var_name_2'].split(':')[0]
    varmaps=[(comp_name_1,var_name_1,comp_name_2,var_name_2)]

    if pyvis_graph_list[model_candidates_N] is not None:
           model=model_list[model_candidates_N]
           model_fullpath=model_fullpath_list[model_candidates_N]
           update_varmap(model, varmaps, True)
           writeCellML_default(model_fullpath, model)
           new_G_model=visualize_model(model,'complete',None)
           pyvis_graph = Network(height="750px", width="100%",directed=True,layout=True)
           pyvis_graph.from_nx(new_G_model)
           pyvis_graph_list[model_candidates_N]=pyvis_graph
           model_list[model_candidates_N]=model
           bioPro_list[model_candidates_N]=None
    else: # if the new model is not composed yet, use the first model as the default
        model=model_list[0]
        model_fullpath=model_fullpath_list[0]
        pyvis_graph = pyvis_graph_list[0]

    nodes =pyvis_graph.nodes
    edges= pyvis_graph.edges

    return {'nodes':nodes,'edges':edges} # return the result to JavaScript

@csrf.exempt
@app.post("/disconnect")
def disconnect():
    data = request.get_json() # retrieve the data sent from JavaScript
    comp_name_1 = data['comp_name_1']
    var_name_1 = data['var_name_1'].split(':')[0]
    comp_name_2 = data['comp_name_2']
    var_name_2 = data['var_name_2'].split(':')[0]
    varmaps=[(comp_name_1,var_name_1,comp_name_2,var_name_2)]

    if pyvis_graph_list[model_candidates_N] is not None:
           model=model_list[model_candidates_N]
           model_fullpath=model_fullpath_list[model_candidates_N]
           update_varmap(model, varmaps, False)
           writeCellML_default(model_fullpath, model)
           new_G_model=visualize_model(model,'complete',None)
           pyvis_graph = Network(height="750px", width="100%",directed=True,layout=True)
           pyvis_graph.from_nx(new_G_model)
           pyvis_graph_list[model_candidates_N]=pyvis_graph
           model_list[model_candidates_N]=model
           bioPro_list[model_candidates_N]=None
    else: # if the new model is not composed yet, use the first model as the default
        model=model_list[0]
        model_fullpath=model_fullpath_list[0]
        pyvis_graph = pyvis_graph_list[0]

    nodes =pyvis_graph.nodes
    edges= pyvis_graph.edges

    return {'nodes':nodes,'edges':edges} # return the result to JavaScript

@app.get("/modelSim")
def modelSim_get():
    if pyvis_graph_list[model_candidates_N] is not None:
       pyvis_graph = pyvis_graph_list[model_candidates_N]
       model=model_list[model_candidates_N]
       model_fullpath=model_fullpath_list[model_candidates_N]
    else: # if the new model is not composed yet, use the first model as the default
        pyvis_graph = pyvis_graph_list[0]
        model=model_list[0]
        model_fullpath=model_fullpath_list[0]
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

    return render_template('modelSim.html', model_fullpath=model_fullpath)

@csrf.exempt
@app.post("/modelSim_getModel")
def modelSim_getModel():
    model_file = request.files['model_file']
    model_file.save(os.path.join(app.config['UPLOAD_FOLDER'], model_file.filename))
    model_fullpath=PurePath(os.path.join(app.config['UPLOAD_FOLDER'], model_file.filename)).as_posix()
    print(model_fullpath)
    return render_template('modelSim.html', model_fullpath=model_fullpath)

@csrf.exempt
@app.post("/modelSim_validate")
def modelSim_validate():
    data = request.get_json() # retrieve the data sent from JavaScript
    model_fullpath = data['model_fullpath']
    print(model_fullpath)
    model, issues,issue_details= parse_model(model_fullpath, strict_mode=True)
    py_fullpath=model_fullpath.replace('.cellml','.py')
    if model:
        isValid, issues,issue_details = writePythonCode(py_fullpath, model,strict_mode=True)
        print(isValid) 
    return render_template('modelSim.html', issues=issues)



    

    
    

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)