from build_CellMLModelV2 import getEntityID, getEntityName_UI
from libcellml import Units
from utilities import ask_for_input, ask_for_file_or_folder
import cellml
from pathlib import PurePath 
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, FOAF,  DCTERMS, XSD

class Qualifiers():
    # Hard-coded qualifiers
    # todo: could retrieve these from relevant specifications
    bqmodel_qualifiers = ['is']
    bqbiol_qualifiers=['isPartOf','hasPart','isPropertyOf','hasProperty','isVersionOf','hasVersion','occursIn']
    semsim_qualifiers = ['hasMediatorParticipant','hasSinkParticipant','hasSourceParticipant','hasMultiplier','hasPhysicalEntityReference','isProductOf','isReactantOf']
    prefix_qualifier = {'bqmodel':bqmodel_qualifiers,'bqbiol':bqbiol_qualifiers,'semsim':semsim_qualifiers}

class LocalOntology():
    # Hard-coded local ontology
    # todo: could dynamically retrieve these from relevant ontologies
    uniprot_terms={'P11166':'Solute carrier family 1, facilitated glucose transporter member 1'}
    chebi_terms={'4167':'D-glucose','29101':'sodium(1+)','29103':'potassium(+1)'}
    go_terms={'0005886':'plasma membrane','0005829':'cytosol','0005615':'extracellular space',
              '0060205':'cytoplasmic vesicle lumen','0030659':'cytoplasmic vesicle membrane',}
    opb_terms={'OPB_00592':'Chemical amount flow rate','OPB_00425': 'Molar amount of chemical'}

    db_terms = {'uniprot':uniprot_terms,'chebi':chebi_terms,'opb':opb_terms,'go':go_terms}
    db_list = list(db_terms.keys())

"""" This class is used to create a RDF graph and bind namespaces based on the OMEX metadata specification (version 1.2)"""
class RDF_Graph():
    # Namespaces according to OMEX metadata specification (version 1.2)
    ORCID = Namespace('http://orcid.org/')   
    BQMODEL = Namespace('http://biomodels.net/model-qualifiers/')
    BQBIOL = Namespace('http://biomodels.net/biology-qualifiers/')
    PUBMED = Namespace('http://identifiers.org/pubmed:')
    NCBI_TAXONOMY = Namespace('http://identifiers.org/taxonomy:')
    BIOMOD = Namespace('http://identifiers.org/biomodels.db:')
    CHEBI = Namespace('http://identifiers.org/chebi/CHEBI:')
    UNIPROT = Namespace('http://identifiers.org/uniprot:')
    OPB = Namespace('http://identifiers.org/opb:')
    FMA = Namespace('http://identifiers.org/FMA:')
    GO = Namespace('http://identifiers.org/GO:')
    SEMSIM = Namespace('http://bime.uw.edu/semsim/')
    prefix_NAMESPACE = {'rdf':RDF,'foaf':FOAF,'dc':DCTERMS, 'orcid':ORCID, 'bqmodel':BQMODEL,'bqbiol':BQBIOL, 'pubmed':PUBMED,'NCBI_Taxon':NCBI_TAXONOMY,
                        'biomod':BIOMOD, 'chebi':CHEBI,'uniprot':UNIPROT,'opb':OPB,'fma':FMA,'go':GO, 'semsim':SEMSIM}

    def __init__(self):
        # output: a RDF graph object 
        self.graph = Graph()
        # Defined Namespace bindings.
        self.graph.bind('orcid', self.ORCID)
        self.graph.bind('rdf', RDF)
        self.graph.bind('foaf', FOAF)
        self.graph.bind('dc', DCTERMS)
        self.graph.bind('bqmodel', self.BQMODEL)
        self.graph.bind('bqbiol', self.BQBIOL)
        self.graph.bind('pubmed', self.PUBMED)
        self.graph.bind('NCBI_Taxon', self.NCBI_TAXONOMY)
        self.graph.bind('biomod', self.BIOMOD)
        self.graph.bind('chebi', self.CHEBI)
        self.graph.bind('uniprot', self.UNIPROT)
        self.graph.bind('opb', self.OPB)
        self.graph.bind('fma', self.FMA)
        self.graph.bind('go', self.GO)
        self.graph.bind('semsim', self.SEMSIM)        

""" This class is used to annotate a CellML model with RDF metadata. It is based on the CellML 2.0 specification."""
class RDF_Editor():
    def __init__(self,rdf_g,filename):
         # input: filename, the fullpath of the CellML file which is to be annotated
        file_withoutSuffix = PurePath(filename).stem
        LOCAL = Namespace('./'+file_withoutSuffix + '.ttl#') # By default, the local namespace is the same as the RDF file name
        MODEL_BASE = Namespace('./'+file_withoutSuffix + '.cellml#') # By default, the model base namespace is the same as the CellML file name
        self.rdf_file = str(PurePath(filename).parent .joinpath(file_withoutSuffix)) + '.ttl' # the fullpath of the RDF file, which is in the same folder as the CellML file and has the same name        
        self.base_dir = str(PurePath(filename).parent)
        self.model=cellml.parse_model(filename, True)
        rdf_g.bind('local', LOCAL)   
        rdf_g.bind('model_base', MODEL_BASE)
        self.prefix_NAMESPACE_local = RDF_Graph.prefix_NAMESPACE|{'local':LOCAL,'model_base':MODEL_BASE}
        self.rdf_g = rdf_g        
    
    def getNode_model(self, comp_name=None, var_name=None):
        # input: comp_name, the CellML component name
        #        var_name, the CellML variable name
        # output: the RDF node of the entity.
        # if the component name is not provided, the RDF node of the model is returned; 
        # if the variable name is not provided, the RDF node of the component is returned; 
        # if both the component name and the variable name are provided, the RDF node of the variable is returned
        base = 'model_base'
        if comp_name is None:
            subnode=getEntityID(self.model)      
        elif var_name is None:
            subnode=getEntityID(self.model, comp_name)
        else:
            subnode=getEntityID(self.model, comp_name, var_name)
        node = self.prefix_NAMESPACE_local[base][subnode]
        return node
    
    def getLocalEntityName_UI(self):
        message = 'Please type the local entity name'
        return ask_for_input(message, 'Text')

    def getNode_local(self,subnode):
        # output: node, the RDF URI node of the local entity
        base = 'local'
        node = self.prefix_NAMESPACE_local[base][subnode]   
        return node
    
    def getDatabase_UI(self):
        message = 'Please select the database'
        return ask_for_input(message, 'List', LocalOntology.db_list)
    
    def getTermID_UI(self,database, message):
        choices = [key +':'+ val for key,val in LocalOntology.db_terms[database].items()]
        term_selected = ask_for_input(message, 'List', choices)
        return term_selected.split(':')[0]
    
    def getQualifier_UI(self):
        message = 'Please select the prefix of the predicate'
        choices = list(Qualifiers.prefix_qualifier.keys())
        base = ask_for_input(message, 'List', choices)
        message = 'Please select the qualifier'
        choices = Qualifiers.prefix_qualifier[base]
        subnode = ask_for_input(message, 'List', choices)
        return base, subnode
    
    def getNode_ontology(self, database, term_id):
        # output: node, the RDF URI node of the ontology term
        node = self.prefix_NAMESPACE_local[database][term_id]   
        return node
    
    def add_identity_triple(self, subject, object):
        # input: subject, the RDF URI node of the subject
        #        object, the RDF URI node of the object
        # output: None
        # add the identity triple to the RDF graph
        database = 'bqbiol'
        term_id = 'isVersionOf'
        pred = self.getNode_ontology( database, term_id)
        self.rdf_g.add((subject, pred, object))

    def add_anatomy_triple(self, subject, object):
        # input: subject, the RDF URI node of the subject
        # output: None
        # add the anatomy triple to the RDF graph
        database = 'bqbiol'
        term_id = 'isPartOf'
        pred = self.getNode_ontology( database, term_id)
        self.rdf_g.add((subject, pred, object))
    
    def add_property_triple(self, subject, object):
        # input: subject, the RDF URI node of the subject
        # output: None
        # add the property triple to the RDF graph
        database = 'bqbiol'
        term_id = 'isPropertyOf'
        pred = self.getNode_ontology( database, term_id)
        self.rdf_g.add((subject, pred, object))

    def getVars(self,comp_name):
        # input: comp_name, the CellML component name
        # output: flux_vars, the list of the flux variables, which are the variables with the units compatible with 'mole_per_second'
        #         quantity_vars, the list of the quantity variables, which are the variables with the units compatible with 'mole'
        flux_units = Units('mole_per_second')
        flux_units.addUnit(Units.StandardUnit.MOLE)
        flux_units.addUnit(Units.StandardUnit.SECOND, 1, -1)
        importer = cellml.resolve_imports(self.model, self.base_dir, True)
        flatModel = importer.flattenModel(self.model)
        variables = [self.model.component(comp_name).variable(var_numb).name() for var_numb in range(self.model.component(comp_name).variableCount())]
        flux_vars =[var for var in variables if Units. compatible (flatModel.component(comp_name).variable(var).units(),flux_units)]
        quantity_vars = [var for var in variables if Units. compatible (flatModel.component(comp_name).variable(var).units(),Units('mole'))]
        return flux_vars, quantity_vars
    
    def selectVar_UI(self,message, var_list):
        return ask_for_input(message, 'List', var_list)
    
    def annotate_flux(self,comp_name,flux_var):
        subj = self.getNode_model(comp_name, flux_var)
        database = 'opb'
        term_id = 'OPB_00592'
        obj= self.getNode_ontology(database, term_id)       
        self.add_identity_triple(subj, obj)
    
    def annotate_quantity(self,comp_name,quantity_var):
        subj = self.getNode_model(comp_name, quantity_var)
        database = 'opb'
        term_id = 'OPB_00425'
        obj= self.getNode_ontology(database, term_id)       
        self.add_identity_triple(subj, obj)
  
    def getProcessEntity(self,entity_id):
        # input:  entity_id, the integer number of the entity
        # output: process_entity, the RDF URI node of the process entity
        process_entity = self.prefix_NAMESPACE_local['local'][f'Process_{entity_id}']
        return process_entity
    
    def getMediatorEntity(self,entity_id):
        # input:  entity_id, the integer number of the entity
        # output: mediator_entity, the RDF URI node of the mediator entity
        mediator_entity = self.prefix_NAMESPACE_local['local'][f'Mediator_{entity_id}']
        return mediator_entity
    
    def getSourceEntity(self,entity_id):
        # input:  entity_id, the integer number of the entity
        # output: source_entity, the RDF URI node of the source entity
        source_entity = self.prefix_NAMESPACE_local['local'][f'Source_{entity_id}']
        return source_entity
    
    def getSinkEntity(self,entity_id):
        # input:  entity_id, the integer number of the entity
        # output: sink_entity, the RDF URI node of the sink entity
        sink_entity = self.prefix_NAMESPACE_local['local'][f'Sink_{entity_id}']
        return sink_entity

    def annotate_source(self,comp_name,quantity_var,multiplier_input,chemical_term,anatomy_term,process_entity,source_entity):
        subj=self.getNode_model(comp_name, quantity_var)
        self.add_property_triple((subj,source_entity))
        pred = self.prefix_NAMESPACE_local['semsim']['hasSourceParticipant']
        self.rdf_g.add(process_entity, pred, source_entity)
        pred = self.prefix_NAMESPACE_local['semsim']['hasMultiplier']
        mulitplier = Literal(multiplier_input, datatype=XSD.float)
        self.rdf_g.add((source_entity, pred, mulitplier))
        self.add_identity_triple(source_entity,chemical_term)
        self.add_anatomy_triple(source_entity,anatomy_term)
    
    def annotate_sink(self,comp_name,quantity_var,multiplier_input,chemical_term,anatomy_term,process_entity,sink_entity):
        subj=self.getNode_model(comp_name, quantity_var)
        self.add_property_triple((subj,sink_entity))
        pred = self.prefix_NAMESPACE_local['semsim']['hasSinkParticipant']
        self.rdf_g.add(process_entity, pred, sink_entity)
        pred = self.prefix_NAMESPACE_local['semsim']['hasMultiplier']
        mulitplier = Literal(multiplier_input, datatype=XSD.float)
        self.rdf_g.add((sink_entity, pred, mulitplier))
        self.add_identity_triple(sink_entity,chemical_term)
        self.add_anatomy_triple(sink_entity,anatomy_term)

    def annotate_mediator(self,comp_name,quantity_var, protein_term, anatomy_term,process_entity,mediator_entity):
        subj=self.getNode_model(comp_name, quantity_var)
        self.add_property_triple((subj,mediator_entity))
        pred = self.prefix_NAMESPACE_local['semsim']['hasMediatorParticipant']
        self.rdf_g.add(process_entity, pred, mediator_entity)
        self.add_identity_triple(mediator_entity,protein_term)
        self.add_anatomy_triple(mediator_entity,anatomy_term)

    def annotate_bioProcess(self,comp_name):
        process_id =0
        flux_vars, quantity_vars = self.getVars(comp_name)
        while True:          
            message = f'Please select the flux variable of the process'
            flux_var = self.selectVar_UI(message, flux_vars)
            self.annotate_flux(comp_name,flux_var)
            process_entity = self.getProcessEntity(process_id)                 
            self.add_property_triple(flux_var, process_entity)
            message = f'Please select the molar amount variable of the transporter'
            quantity_mediator = self.selectVar_UI(message, quantity_vars)
            mediator_entity = self.getMediatorEntity(process_id)
            message = f'Please select the name of the transporter'
            protein_term= self.getTermID_UI(self,'uniprot',message)
            message = f'Please select subcellular location of the transporter'
            anatomy_term= self.getTermID_UI(self,'go',message)
            self.annotate_mediator(comp_name,quantity_mediator, protein_term, anatomy_term,process_entity,mediator_entity)
            participant_id = 0
            while True:
                entity_id = f'{process_id}_{participant_id}'
                message = f'Please select the transported species name'
                chemical_term= self.getTermID_UI(self,'chebi',message)
                message = f'Please select the molar amount variable of the source participant'
                quantity_source = self.selectVar_UI(message, quantity_vars)
                source_entity = self.getSourceEntity(entity_id)
                multiplier_input = ask_for_input('Please enter the stoichiometric coefficient of the source participant', 'Text')               
                message = f'Please select the subcellular location of the source participant'
                anatomy_term= self.getTermID_UI(self,'go',message)                
                self.annotate_source(comp_name,quantity_source,multiplier_input,chemical_term,anatomy_term,process_entity,source_entity)
                message = f'Please select the molar amount variable of the sink participant'
                quantity_sink = self.selectVar_UI(message, quantity_vars)
                sink_entity = self.getSinkEntity(entity_id)
                multiplier_input = ask_for_input('Please enter the stoichiometric coefficient of the sink participant', 'Text')
                message = f'Please select the subcellular location of the sink participant'
                anatomy_term= self.getTermID_UI(self,'go',message)
                self.annotate_sink(comp_name,quantity_sink,multiplier_input,chemical_term,anatomy_term,process_entity,sink_entity)

                message = 'Do you want to add another species?'
                if ask_for_input(message, 'Confirm'):
                    participant_id += 1
                else:
                    break
            message = 'Do you want to add another process?'
            if ask_for_input(message, 'Confirm'):
                process_id += 1
            else:
                break  
              
    def save_graph(self):
        # Save the RDF triples to a file
        with open(self.rdf_file, 'w') as f:
            f.write(self.rdf_g.serialize(format='ttl'))
            f.close()
        print(f'The RDF triples are saved to {self.rdf_file}')
        
    def get_graph(self):
        return self.rdf_g
           
# main function
if __name__ == "__main__":

    rdf_g = RDF_Graph()
    filename = ask_for_file_or_folder('Please select the CellML file')
    rdf_editor = RDF_Editor(rdf_g,filename)
    comp_name= getEntityName_UI(rdf_editor.model)
    rdf_editor.annotate_bioProcess(comp_name)
    if ask_for_input('Do you want to save the RDF triples?', 'Confirm'):
        rdf_editor.save_graph()
    


