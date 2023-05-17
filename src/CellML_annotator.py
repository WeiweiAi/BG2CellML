from build_CellMLV2 import getEntityID
from BG2CellML import BG
from libcellml import Units
from utilities import ask_for_input
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
class RDF_Graph(Graph):
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
        super().__init__()
        # Defined Namespace bindings.
        self.bind('orcid', self.ORCID)
        self.bind('rdf', RDF)
        self.bind('foaf', FOAF)
        self.bind('dc', DCTERMS)
        self.bind('bqmodel', self.BQMODEL)
        self.bind('bqbiol', self.BQBIOL)
        self.bind('pubmed', self.PUBMED)
        self.bind('NCBI_Taxon', self.NCBI_TAXONOMY)
        self.bind('biomod', self.BIOMOD)
        self.bind('chebi', self.CHEBI)
        self.bind('uniprot', self.UNIPROT)
        self.bind('opb', self.OPB)
        self.bind('fma', self.FMA)
        self.bind('go', self.GO)
        self.bind('semsim', self.SEMSIM)        

""" This class is used to annotate a CellML model with RDF metadata. It is based on the CellML 2.0 specification."""
class RDF_Editor():
    def __init__(self,rdf_g,filename):
         # input: rdf_g, a RDF graph object
         #       filename, the fullpath of the CellML file which is to be annotated
         # output: a RDF_Editor object
         # By default, the model base namespace is the CellML filename (e.g.,file.cellml)
         # By default, the local namespace is the RDF filename (e.g.,file.ttl), in the same folder as the CellML file, and sharing the same name except for the suffix.
        file_withoutSuffix = PurePath(filename).stem
        LOCAL = Namespace('./'+file_withoutSuffix + '.ttl#') # 
        MODEL_BASE = Namespace('./'+file_withoutSuffix + '.cellml#') # 
        self.rdf_file = str(PurePath(filename).parent .joinpath(file_withoutSuffix)) + '.ttl'        
        self.base_dir = str(PurePath(filename).parent)
        self.model=cellml.parse_model(filename, True)
        importer = cellml.resolve_imports(self.model, self.base_dir, True)
        self.flatModel = importer.flattenModel(self.model) # this may not be necessary after the units compatibility check function is fixed
        rdf_g.bind('local', LOCAL)   
        rdf_g.bind('model_base', MODEL_BASE)
        self.prefix_NAMESPACE_local = RDF_Graph.prefix_NAMESPACE|{'local':LOCAL,'model_base':MODEL_BASE}
        self.rdf_g = rdf_g        
    # -----------------------  RDF node editing functions -----------------------
    def getNode_local(self,subnode):
        # output: node, the RDF URI node of the local entity
        base = 'local'
        node = self.prefix_NAMESPACE_local[base][subnode]   
        return node
    
    def getNode_model(self, comp_name=None, var_name=None):
        # input: comp_name, the CellML component name
        #        var_name, the CellML variable name
        # output: the RDF node of the model entity.
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
    
    def getNode_ontology(self, database, term_id):
        # output: node, the RDF URI node of the ontology term
        node = self.prefix_NAMESPACE_local[database][term_id]   
        return node
    
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
    # ----------------------- User interfaces for RDF node creation -----------------------
    # Provide a variable list for the user to select the variable to be annotated
    # The variables are grouped by the compatible units, which can be used to infer the biological meaning of the variable,
    # e.g., the variable with the unit of fmol can be annotated as the molar amount of a chemical species.
    def getVars_byUnits(self,comp_name, units):
        # input: comp_name, the CellML component name
        #        units, the units of the expected returned variables      
        # output: vars, the list of the  variables, which are the variables with the units compatible with input units       
        variables = [self.model.component(comp_name).variable(var_numb).name() for var_numb in range(self.model.component(comp_name).variableCount())]
        vars =[var for var in variables if Units. compatible (self.flatModel.component(comp_name).variable(var).units(),units)]
        return vars
    
    def getLocalEntityName_UI(self):
        message = 'Please type the local entity name'
        return ask_for_input(message, 'Text')
    
    def selectVar_UI(self,message, var_list):
        return ask_for_input(message, 'List', var_list)
   
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
    
    # -----------------------  RDF triple editing functions with hard-coded items for biological process annotation-----------------------
    def add_triple(self, subject, predicate, object):
        # input: subject, the RDF URI node of the subject
        #        predicate, the RDF URI node of the predicate
        #        object, the RDF URI node of the object
        # output: None
        # add the triple to the RDF graph
        self.rdf_g.add((subject, predicate, object))
        
        # The following triples have hard-coded predicates
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
        #        object, the RDF URI node of the object   
        # output: None
        # add the anatomy triple to the RDF graph
        database = 'bqbiol'
        term_id = 'isPartOf'
        pred = self.getNode_ontology( database, term_id)
        self.rdf_g.add((subject, pred, object))
    
    def add_property_triple(self, subject, object):
        # input: subject, the RDF URI node of the subject
        #        object, the RDF URI node of the object
        # output: None
        # add the property triple to the RDF graph
        database = 'bqbiol'
        term_id = 'isPropertyOf'
        pred = self.getNode_ontology( database, term_id)
        self.rdf_g.add((subject, pred, object))
        
        # The following triples have hard-coded objects 
    def annotate_flux(self,comp_name,flux_var,process_entity):
        subj = self.getNode_model(comp_name, flux_var)
        database = 'opb'
        term_id = 'OPB_00592'
        obj= self.getNode_ontology(database, term_id)       
        self.add_identity_triple(subj, obj)               
        self.add_property_triple(subj, process_entity)
    
    def annotate_quantity(self,comp_name,quantity_var):
        subj = self.getNode_model(comp_name, quantity_var)
        database = 'opb'
        term_id = 'OPB_00425'
        obj= self.getNode_ontology(database, term_id)       
        self.add_identity_triple(subj, obj)
       
    def annotate_source(self,comp_name,quantity_var,multiplier_input,chemical_term,anatomy_term,process_entity,source_entity):
        self.annotate_quantity(comp_name,quantity_var)
        subj=self.getNode_model(comp_name, quantity_var)
        self.add_property_triple(subj,source_entity)
        pred = self.prefix_NAMESPACE_local['semsim']['hasSourceParticipant']
        self.rdf_g.add((process_entity, pred, source_entity))
        pred = self.prefix_NAMESPACE_local['semsim']['hasMultiplier']
        mulitplier = Literal(multiplier_input, datatype=XSD.float)
        self.rdf_g.add((source_entity, pred, mulitplier))
        self.add_identity_triple(source_entity,chemical_term)
        self.add_anatomy_triple(source_entity,anatomy_term)
    
    def annotate_sink(self,comp_name,quantity_var,multiplier_input,chemical_term,anatomy_term,process_entity,sink_entity):
        self.annotate_quantity(comp_name,quantity_var)
        subj=self.getNode_model(comp_name, quantity_var)
        self.add_property_triple(subj,sink_entity)
        pred = self.prefix_NAMESPACE_local['semsim']['hasSinkParticipant']
        self.rdf_g.add((process_entity, pred, sink_entity))
        pred = self.prefix_NAMESPACE_local['semsim']['hasMultiplier']
        mulitplier = Literal(multiplier_input, datatype=XSD.float)
        self.rdf_g.add((sink_entity, pred, mulitplier))
        self.add_identity_triple(sink_entity,chemical_term)
        self.add_anatomy_triple(sink_entity,anatomy_term)

    def annotate_mediator(self,comp_name,processID,mediatorDict):
        # mediatorDict: {'flux_var': flux_var, 'quantity_var': quantity_var, 'protein_term': protein_term, 'anatomy_term': anatomy_term}
        process_entity = self.getProcessEntity(processID)
        mediator_entity = self.getMediatorEntity(processID)
        self.annotate_flux(comp_name,mediatorDict['flux_var'],process_entity) 
        self.annotate_quantity(comp_name,mediatorDict['quantity_var'])
        subj=self.getNode_model(comp_name, mediatorDict['quantity_var'])
        self.add_property_triple(subj,mediator_entity)
        pred = self.prefix_NAMESPACE_local['semsim']['hasMediatorParticipant']
        self.rdf_g.add((process_entity, pred, mediator_entity))
        self.add_identity_triple(mediator_entity,mediatorDict['protein_term'])
        self.add_anatomy_triple(mediator_entity,mediatorDict['anatomy_term'])
    
    def annotate_sources(self,comp_name,processID,sourceDict):
        # sourceDict: [{'quantity_var': quantity_var, 'stoichiometric_coefficient': stoichiometric_coefficient, 'chemical_term': chemical_term, 'anatomy_term': anatomy_term}, {},...]
        process_entity = self.getProcessEntity(processID)
        sourceID_subfix = 0       
        for arg in sourceDict:
            quantity_var = arg['quantity_var']
            multiplier_input = arg['stoichiometric_coefficient']
            chemical_term = arg['chemical_term']
            anatomy_term = arg['anatomy_term']
            sourceID= f'{processID}_{sourceID_subfix}'
            source_entity=self.getSourceEntity(sourceID)
            self.annotate_source(comp_name,quantity_var,multiplier_input,chemical_term,anatomy_term,process_entity,source_entity)
            sourceID_subfix += 1 

    def annotate_sinks(self,comp_name,processID,sinkDict):
        # sinkDict: 
        process_entity = self.getProcessEntity(processID)
        sinkID_subfix = 0       
        for arg in sinkDict:
            quantity_var = arg['quantity_var']
            multiplier_input = arg['stoichiometric_coefficient']
            chemical_term = arg['chemical_term']
            anatomy_term = arg['anatomy_term']
            sinkID= f'{processID}_{sinkID_subfix}'
            sink_entity=self.getSinkEntity(sinkID)
            self.annotate_sink(comp_name,quantity_var,multiplier_input,chemical_term,anatomy_term,process_entity,sink_entity)
            sinkID_subfix += 1
    
    def annotate_bioProcess(self,comp_name,processID, mediatorDict,sourceDict,sinkDict):
        self.annotate_mediator(comp_name,processID,mediatorDict)
        self.annotate_sources(comp_name,processID,sourceDict)
        self.annotate_sinks(comp_name,processID,sinkDict)
    
    def build_mediatorDict(self,mediator):
        # input: mediator=[flux_var, quantity_var,protein_term,anatomy_term]
        # By default, using uniprot and go as the ontology for protein and anatomy terms,respectively
        protein_term_node =self.getNode_ontology('uniprot', mediator[2])
        anatomy_term_node =self.getNode_ontology('go', mediator[3])
        mediatorDict = {'flux_var': mediator[0], 'quantity_var': mediator[1], 'protein_term': protein_term_node, 'anatomy_term': anatomy_term_node}
        return mediatorDict
    
    def build_participantsDict(self,participants):
        # input: participants=[[quantity_var, stoichiometric_coefficient,chemical_term,anatomy_term],[],...]
        # By default, using chebi and go as the ontology for chemical and anatomy terms,respectively
        participantsDict = []
        for i in range(len(participants)):
            quantity_var = participants[i][0]
            stoichiometric_coefficient = participants[i][1]
            chemical_term_node =self.getNode_ontology('chebi', participants[i][2])
            anatomy_term_node =self.getNode_ontology('go', participants[i][3])
            participantDict = {'quantity_var': quantity_var, 'stoichiometric_coefficient': stoichiometric_coefficient, 'chemical_term': chemical_term_node, 'anatomy_term': anatomy_term_node}
            participantsDict.append(participantDict)
        return participantsDict

    def build_mediatorDict_UI(self,flux_vars, quantity_vars):
        message = f'Please select the flux variable of the process'
        flux_var = self.selectVar_UI(message, flux_vars)
        message = f'Please select the molar amount variable of the transporter'
        quantity_var = self.selectVar_UI(message, quantity_vars)
        message = f'Please select the name of the transporter'
        protein_term= self.getTermID_UI('uniprot',message)
        protein_term_node =self.getNode_ontology('uniprot', protein_term)
        message = f'Please select subcellular location of the transporter'
        anatomy_term= self.getTermID_UI('go',message)
        anatomy_term_node =self.getNode_ontology('go', anatomy_term)
        mediatorDict = {'flux_var': flux_var, 'quantity_var': quantity_var, 'protein_term': protein_term_node, 'anatomy_term': anatomy_term_node}
        return mediatorDict
    
    def build_participantsDict_UI(self,quantity_vars):
        for quantity_var in quantity_vars:
            message = f'Please select the transported species name of the quantity variable {quantity_var}'
            chemical_term= self.getTermID_UI('chebi',message)
            chemical_term_node =self.getNode_ontology('chebi', chemical_term)
            stoichiometric_coefficient = ask_for_input('Please enter the stoichiometric coefficient of the source participant', 'Text')               
            message = f'Please select the subcellular location of the source participant'
            anatomy_term= self.getTermID_UI('go',message) 
            anatomy_term_node =self.getNode_ontology('go', anatomy_term)
            participantDict = {'quantity_var': quantity_var, 'stoichiometric_coefficient': stoichiometric_coefficient, 'chemical_term': chemical_term_node, 'anatomy_term': anatomy_term_node}
            return participantDict  
              
    def save_graph(self):
        # Save the RDF triples to a file
        with open(self.rdf_file, 'w') as f:
            f.write(self.rdf_g.serialize(format='ttl'))
            f.close()
        print(f'The RDF triples are saved to {self.rdf_file}')
        
    def get_graph(self):
        return self.rdf_g

def get_bioProcess(rdf_g):
    # search for all biological processes in the RDF graph
    # return: a list of biological processes in the RDF graph [{'cellml_path': cellml_path,'mediator': mediator, 'sources': sources, 'sinks': sinks}] 
    # mediator: (flux_varID, mediator_term, mediator_location)
    # sources: [(source_varID, stoichiometric_coefficient, chemical_term, anatomy_term),...]
    # sinks: [(sink_varID, stoichiometric_coefficient, chemical_term, anatomy_term),...]    
    bioProcesses = []
    for local_proc in rdf_g.subjects(RDF_Graph.prefix_NAMESPACE['semsim']['hasMediatorParticipant'],None):
        for flux_var in rdf_g.subjects(None, local_proc):
            flux_varID = flux_var.fragment
            cellml_path = flux_var.n3().split('#')[0].strip('<>')
        local_mediator = rdf_g.value(local_proc, RDF_Graph.prefix_NAMESPACE['semsim']['hasMediatorParticipant'], None)
        mediator_term = rdf_g.value(local_mediator, RDF_Graph.prefix_NAMESPACE['bqbiol']['isVersionOf'],None).n3()
        anatomy_term = rdf_g.value(local_mediator, RDF_Graph.prefix_NAMESPACE['bqbiol']['isPartOf'],None).n3()
        mediator = (flux_varID, mediator_term, anatomy_term)
        sources=[]
        for local_source in rdf_g.objects(local_proc,RDF_Graph.prefix_NAMESPACE['semsim']['hasSourceParticipant']):
            source_varID = rdf_g.value(None,RDF_Graph.prefix_NAMESPACE['bqbiol']['isPropertyOf'], local_source).fragment
            coef = rdf_g.value(local_source, RDF_Graph.prefix_NAMESPACE['semsim']['hasMultiplier']).toPython()
            anatomy_term = rdf_g.value(local_source, RDF_Graph.prefix_NAMESPACE['bqbiol']['isPartOf']).n3()
            chemical_term = rdf_g.value(local_source, RDF_Graph.prefix_NAMESPACE['bqbiol']['isVersionOf']).n3()
            sources.append((source_varID,coef,chemical_term, anatomy_term))
        sinks=[]
        for local_sink in rdf_g.objects(local_proc,RDF_Graph.prefix_NAMESPACE['semsim']['hasSinkParticipant']):
            sink_varID = rdf_g.value(None,RDF_Graph.prefix_NAMESPACE['bqbiol']['isPropertyOf'], local_sink).fragment
            coef = rdf_g.value(local_sink, RDF_Graph.prefix_NAMESPACE['semsim']['hasMultiplier']).toPython()
            anatomy_term = rdf_g.value(local_sink, RDF_Graph.prefix_NAMESPACE['bqbiol']['isPartOf']).n3()
            chemical_term = rdf_g.value(local_sink, RDF_Graph.prefix_NAMESPACE['bqbiol']['isVersionOf']).n3()
            sinks.append((sink_varID,coef,chemical_term, anatomy_term))
        bioProcesses.append({'cellml_path': cellml_path,'mediator': mediator, 'sources': sources, 'sinks':sinks})
    return bioProcesses

# main function for testing
if __name__ == "__main__":

    rdf_g = RDF_Graph()
    filename = 'SLCT3V_ss_test_inOne.cellml'
    foldername = 'C:/Users/wai484/Documents/BG2CellML/test/cellml/SLC_SS'
    filename = PurePath(foldername).joinpath(filename)
    rdf_editor = RDF_Editor(rdf_g,filename)
    comp_name = 'SLCT3V_ss'
    mediator=['v_ss', 'E','P11166','0005886']
    sources=[['q_Ao','1','4167','0005615']]
    sinks=[['q_Ai','1','4167','0005829']]
    mediatorDict = rdf_editor.build_mediatorDict(mediator)
    sourceDict = rdf_editor.build_participantsDict(sources)
    sinkDict = rdf_editor.build_participantsDict(sinks)
    rdf_editor.annotate_bioProcess(comp_name,0, mediatorDict,sourceDict,sinkDict)
    rdf_editor.save_graph()
    get_bioProcess(rdf_g)
    
    
    


