from pyomexmeta import RDF, eUriType
# Read a cellml file to a string

cellml = """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<model xmlns=\"http://www.cellml.org/cellml/1.1#\" xmlns:cmeta=\"http://www.cellml.org/metadata/1.0#\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\" xmlns:bqs=\"http://www.cellml.org/bqs/1.0#\" xmlns:semsim=\"http://bime.uw.edu/semsim/#\" xmlns:dc=\"http://purl.org/dc/terms/\" xmlns:vCard=\"http://www.w3.org/2001/vcard-rdf/3.0#\" name=\"annotation_examples\" cmeta:id=\"annExamples\">
  <component name=\"main\">
    <variable cmeta:id=\"main.Volume\" initial_value=\"100\" name=\"Volume\" units=\"dimensionless\" />
    <variable cmeta:id=\"main.MembraneVoltage\" initial_value=\"-80\" name=\"MembraneVoltage\" units=\"dimensionless\" />
    <variable cmeta:id=\"main.ReactionRate\" initial_value=\"1\" name=\"ReactionRate\" units=\"dimensionless\" />
    <variable cmeta:id=\"main.entity1\" initial_value=\"1\" name=\"entity1\" units=\"dimensionless\" />
    <variable cmeta:id=\"main.entity2\" initial_value=\"1\" name=\"entity2\" units=\"dimensionless\" />
    <variable cmeta:id=\"main.entity3\" initial_value=\"1\" name=\"entity3\" units=\"dimensionless\" />
  </component>
</model>
"""

# create an empty RDF object
rdf = RDF()
# create an editor object from the RDF object and the cellml file
# the editor object is used to add annotations to the RDF object
# Get the cellml
#1 editor = rdf.to_editor("<../test/cellml/A.cellml>", True)
# rdf.set_repository_uri("https://Repositorious.org")
# rdf.set_model_uri("SignallingNetwork.sbml")
editor = rdf.to_editor(cellml, generate_new_metaids=True, sbml_semantic_extraction=False)

sbml_with_metaids = editor.get_xml()

with editor.new_physical_entity() as physical_entity:
    physical_entity \
        .about("R1", eUriType.LOCAL_URI) \
        .identity("CHEBI:16236") \
        .has_property("main.MembraneVoltage", eUriType.MODEL_URI, "fma:18228") 

with editor.new_physical_entity() as physical_entity:
    physical_entity \
        .about("C2", eUriType.LOCAL_URI) \
        .identity("CHEBI:16236") \
        .has_part("q") \
        .has_property("main.ReactionRate", eUriType.MODEL_URI, "fma:18228")     

with editor.new_physical_entity() as sub1:
    sub1 \
        .about("sub", eUriType.LOCAL_URI) \
        .has_part("R1") \
        .has_part("C2") \
        .has_property("main.entity1", eUriType.MODEL_URI, "fma:18228") 
    
with editor.new_physical_process() as physical_process:
    physical_process.about("Process", eUriType.LOCAL_URI) \
        .is_version_of("CHEBI:16236") \
        .add_source("sub", eUriType.LOCAL_URI, 1)\
        .add_sink("R1", eUriType.LOCAL_URI, 1)\
        .has_property("main.entity2", eUriType.MODEL_URI, "fma:18228")
        
         

with editor.new_physical_entity() as physical_entity:
    physical_entity \
        .about("R2", eUriType.LOCAL_URI) \
        .identity("CHEBI:16236") \
        .has_property("main.MembraneVoltage", eUriType.MODEL_URI, "fma:18228") 

       
print(rdf)

# rdf.to_file(filename: str, syntax: str)
