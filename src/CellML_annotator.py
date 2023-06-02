# Description: This script is used to annotate a CellML model with RDF metadata. It is based on the CellML 2.0 specification.
import cellml
from pathlib import PurePath 
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, FOAF,  DCTERMS, XSD
from rdflib.extras.external_graph_libs import rdflib_to_networkx_graph
import networkx as nx
from utilities import infix_to_mathml
from libcellml import Component, Generator, GeneratorProfile, Model, Units,  Variable, Annotator
from build_CellMLV2 import importComponents_clone,getEntityList,copyUnits_temp, MATH_FOOTER, MATH_HEADER
import numpy as np
def getEntityID(model, comp_name=None, var_name=None):
    # input: model, the CellML model object
    #        comp_name, the CellML component name
    #        var_name, the CellML variable name
    # output: the ID of the entity.
    # if the component name is not provided, the ID of the model is returned; 
    # if the variable name is not provided, the ID of the component is returned; 
    # if both the component name and the variable name are provided, the ID of the variable is returned
    if comp_name is None:
        return model.id()
    elif var_name is None:
        return model.component(comp_name).id()
    else:
        return model.component(comp_name).variable(var_name).id()
    
def getNamebyID(model, ID):
    # input: model, the CellML model object
    #        ID, the ID of the entity.
    # output: the name of the entity.
    # if the ID is the ID of the component, the name of the component is returned; 
    # if the ID is the ID of the variable, the name of the component and the variable is returned
    for comp in range(model.componentCount()):
        if ID == model.component(comp).id():
            return model.component(comp).name(), None
        else:
            for var in range(model.component(comp).variableCount()):
                if ID == model.component(comp).variable(var).id():
                    return model.component(comp).name(), model.component(comp).variable(var).name()
    return None, None
class Qualifiers():
    # Hard-coded qualifiers
    # todo: could retrieve these from relevant specifications
    bqmodel_qualifiers = ['is']
    bqbiol_qualifiers=['isPartOf','hasPart','isPropertyOf','hasProperty','isVersionOf','hasVersion','occursIn']
    semsim_qualifiers = ['hasMediatorParticipant','hasSinkParticipant','hasSourceParticipant','hasMultiplier','hasPhysicalEntityReference','isProductOf','isReactantOf']
    dc_predicates = ['description','creator','created','contributor']
    prefix_qualifier = {'bqmodel':bqmodel_qualifiers,'bqbiol':bqbiol_qualifiers,'semsim':semsim_qualifiers,'dcterms':dc_predicates}

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
    CHEBI = Namespace('http://identifiers.org/CHEBI:')
    UNIPROT = Namespace('http://identifiers.org/uniprot:')
    OPB = Namespace('http://identifiers.org/opb:')
    FMA = Namespace('http://identifiers.org/FMA:')
    GO = Namespace('http://identifiers.org/GO:')
    SEMSIM = Namespace('http://bime.uw.edu/semsim/')
    prefix_NAMESPACE = {'rdf':RDF,'foaf':FOAF,'dcterms':DCTERMS, 'orcid':ORCID, 'bqmodel':BQMODEL,'bqbiol':BQBIOL, 'pubmed':PUBMED,'NCBI_Taxon':NCBI_TAXONOMY,
                        'biomod':BIOMOD, 'chebi':CHEBI,'uniprot':UNIPROT,'opb':OPB,'fma':FMA,'go':GO, 'semsim':SEMSIM}

    def __init__(self):
        # output: a RDF graph object 
        super().__init__()
        # Defined Namespace bindings.
        self.bind('orcid', self.ORCID)
        self.bind('rdf', RDF)
        self.bind('foaf', FOAF)
        self.bind('dcterms', DCTERMS)
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
        model_entity = self.getNode_model()
        dc_pred = RDF_Graph.prefix_NAMESPACE['dcterms']['description']
        description = Literal('Built for automatic model composition project', datatype=XSD.string)
        self.rdf_g.add((model_entity, dc_pred, description))       
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
    
    def annotate_mediator(self,comp_name,processID,mediatorDict):
        # mediatorDict: {'v_ss':{'physics':[('opb','OPB_00592')],'chemical terms':[('uniprot','P11166')],'anatomy terms': [('go','0005886')]}}
        process_entity = self.getProcessEntity(processID)
        mediator_entity = self.getMediatorEntity(processID)
        flux_var = list(mediatorDict.keys())[0]
        if  flux_var:
            subj = self.getNode_model(comp_name, flux_var)
            self.add_property_triple(subj, process_entity)
            for flux_physics in mediatorDict[flux_var]['physics']:           
               obj= self.getNode_ontology(flux_physics[0], flux_physics[1])       
               self.add_identity_triple(subj, obj)                             
        else:
            print('A flux variable is needed for the bioprocess.')
            return
        pred = self.prefix_NAMESPACE_local['semsim']['hasMediatorParticipant']
        self.rdf_g.add((process_entity, pred, mediator_entity))
        for chemical_term in mediatorDict[flux_var]['chemical terms']:
            chemical_term_node =self.getNode_ontology(chemical_term[0], chemical_term[1])
            self.add_identity_triple(mediator_entity,chemical_term_node)
        for anatomy_term in mediatorDict[flux_var]['anatomy terms']:
            anatomy_term_node =self.getNode_ontology(anatomy_term[0],anatomy_term[1])
            self.add_anatomy_triple(mediator_entity,anatomy_term_node)
    
    def annotate_sources(self,comp_name,processID,sourceDict):
        # sourceDict: sourceDict={'q_Ao':{'proportionality':1,'physics':[('opb','OPB_00425')] ,'chemical terms':[('chebi','4167')],'anatomy terms': [('go','0005615')]}}
        process_entity = self.getProcessEntity(processID)
        sourceID_subfix = 0
        quantity_var_list = list(sourceDict.keys())
        if len(quantity_var_list) == 0:
            print('A quantity variable is needed for the bioprocess.')
            return       
        for quantity_var in quantity_var_list:
            subj = self.getNode_model(comp_name, quantity_var)
            sourceID= f'{processID}_{sourceID_subfix}'
            source_entity=self.getSourceEntity(sourceID)           
            self.add_property_triple(subj,source_entity)

            for quantity_physics in sourceDict[quantity_var]['physics']:           
               obj= self.getNode_ontology(quantity_physics[0], quantity_physics[1])       
               self.add_identity_triple(subj, obj)

            pred = self.prefix_NAMESPACE_local['semsim']['hasSourceParticipant']
            self.rdf_g.add((process_entity, pred, source_entity))
            pred = self.prefix_NAMESPACE_local['semsim']['hasMultiplier']
            mulitplier = Literal(sourceDict[quantity_var]['proportionality'], datatype=XSD.float)
            self.rdf_g.add((source_entity, pred, mulitplier)) 

            for chemical_term in sourceDict[quantity_var]['chemical terms']:
               chemical_term_node =self.getNode_ontology(chemical_term[0], chemical_term[1])
               self.add_identity_triple(source_entity,chemical_term_node)
            for anatomy_term in sourceDict[quantity_var]['anatomy terms']:
               anatomy_term_node =self.getNode_ontology(anatomy_term[0],anatomy_term[1])
               self.add_anatomy_triple(source_entity,anatomy_term_node)
            sourceID_subfix += 1


    def annotate_sinks(self,comp_name,processID,sinkDict):
        # sinkDict: sinkDict={'q_Ai':{'proportionality':1,'physics':[('opb','OPB_00425')] ,'chemical terms':[('chebi','4167')],'anatomy terms': [('go','0005829')]}}
        process_entity = self.getProcessEntity(processID)
        sinkID_subfix = 0       
        quantity_var_list = list(sinkDict.keys())
        if len(quantity_var_list) == 0:
            print('A quantity variable is needed for the bioprocess.')
            return
        for quantity_var in quantity_var_list:
            subj = self.getNode_model(comp_name, quantity_var)
            sinkID= f'{processID}_{sinkID_subfix}'
            sink_entity=self.getSinkEntity(sinkID)           
            self.add_property_triple(subj,sink_entity)

            for quantity_physics in sinkDict[quantity_var]['physics']:           
               obj= self.getNode_ontology(quantity_physics[0], quantity_physics[1])       
               self.add_identity_triple(subj, obj)

            pred = self.prefix_NAMESPACE_local['semsim']['hasSinkParticipant']
            self.rdf_g.add((process_entity, pred, sink_entity))
            pred = self.prefix_NAMESPACE_local['semsim']['hasMultiplier']
            mulitplier = Literal(sinkDict[quantity_var]['proportionality'], datatype=XSD.float)
            self.rdf_g.add((sink_entity, pred, mulitplier)) 

            for chemical_term in sinkDict[quantity_var]['chemical terms']:
               chemical_term_node =self.getNode_ontology(chemical_term[0], chemical_term[1])
               self.add_identity_triple(sink_entity,chemical_term_node)
            for anatomy_term in sinkDict[quantity_var]['anatomy terms']:
               anatomy_term_node =self.getNode_ontology(anatomy_term[0],anatomy_term[1])
               self.add_anatomy_triple(sink_entity,anatomy_term_node)
            sinkID_subfix += 1
    
    def annotate_bioProcess(self,comp_name,processID, mediatorDict,sourceDict,sinkDict):
        self.annotate_mediator(comp_name,processID,mediatorDict)
        self.annotate_sources(comp_name,processID,sourceDict)
        self.annotate_sinks(comp_name,processID,sinkDict)
              
    def save_graph(self):
        # Save the RDF triples to a file
        with open(self.rdf_file, 'w') as f:
            f.write(self.rdf_g.serialize(format='ttl'))
            f.close()
        print(f'The RDF triples are saved to {self.rdf_file}')
        G = rdflib_to_networkx_graph(rdf_g)
        print("Visualizing the graph:")
        A = nx.nx_agraph.to_agraph(G)
        A.graph_attr.update(arrowtype='open',arrowsize=0.5,rankdir='LR')
        A.layout('dot')
        A.draw('test.png', format='png', prog='dot')
        
        
    def get_graph(self):
        return self.rdf_g

def compose_model(new_model_name,selection_dict):
    # input: new_model_name, the name of the new model
    #       selection_dict, the dictionary of the selected models and components {model1:{'components':{comp:compref,..},"annotation":annotation_dict,...}
    #       annotation_dict = {'cellml_path': cellml_path,'mediator': mediator_dict, 'sources': sourceDict , 'sinks':sinkDict}
    #  # output: the new model object
    # species_list = {1:{'varinfo':[],chemical terms:[],anatomy terms:[]},2:{'':[],chemical terms:[],anatomy terms:[]}}
    # Add a new component to the new model
    new_model = Model(new_model_name)
    new_component = Component(new_model_name)
    new_model.addComponent(new_component)
    voi = 't'
    units = Units('second')
    voi = Variable(voi)
    voi.setUnits(units)
    new_component.addVariable(voi)   
    #new_component.setMath(MATH_HEADER)
    # Clone the selected components from the selected models to the new model
    for import_model,model_info in selection_dict.items():
       import_components_dict=model_info['components']
       importComponents_clone(new_model,import_model,import_components_dict)
       
    copyUnits_temp(new_model,import_model)
    print('new_model components',getEntityList(new_model))
    # Add new variables for each unique species to the new component
    # To do: check if the species is selected by the user; now assume all species are selected
    annotator = Annotator()
    annotator.setModel(new_model)
    annotator.clearAllIds()
    annotator.assignAllIds()

    species_list = {}
    flux_list = {}
    def update_unique_process(flux_list,mediator,model):
        unique_flag=True
        if len(flux_list) == 0:
            unique_flag=True
        else:
            for id,flux_dict in flux_list.items():
                v_ss_ID = list(mediator.keys())[0]
                if set(mediator[v_ss_ID]["chemical terms"])& set(flux_dict["chemical terms"]) and set(mediator[v_ss_ID]["anatomy terms"])& set(flux_dict["anatomy terms"]):
                    unique_flag=False                    
                    flux_list[id]["varinfo"].append((model,v_ss_ID))
                    break
        if unique_flag:
            id = len(flux_list)+1
            v_ss_ID = list(mediator.keys())[0]
            flux_list.update({id:{'varinfo':[(model,v_ss_ID)],"chemical terms":mediator[v_ss_ID]["chemical terms"],"anatomy terms":mediator[v_ss_ID]["anatomy terms"]}})

    def update_unique_species(species_list,q_varID,species,participant_location,v_ss_ID,model):
        unique_flag=True
        if len(species_list) == 0:
            unique_flag=True
        else:          
            for id,species_dict in species_list.items():                
                if set(species["anatomy terms"])& set(species_dict["anatomy terms"]) and set(species["chemical terms"])& set(species_dict["chemical terms"]):
                    unique_flag=False
                    species_list[id]["varinfo"].append((model,v_ss_ID,participant_location,species['proportionality'],q_varID))
                    break
        
        if unique_flag:
            id = len(species_list)+1
            species_list.update({id:{'varinfo':[(model,v_ss_ID,participant_location,species['proportionality'],q_varID)],"chemical terms":species["chemical terms"],"anatomy terms":species["anatomy terms"]}})
    # Todo: check if the flux is unique, now assume all fluxes are unique
    for model,model_info in selection_dict.items():
        for bioProc in list(model_info['annotation'].values()):
            v_ss_ID = list(bioProc['mediator'].keys())[0]
            update_unique_process(flux_list,bioProc['mediator'],model)
            for participant_location, participants in bioProc.items():
                # participants = {'q_varID':{'proportionality':1,'physics':[('opb','OPB_00425')] ,'chemical terms':[('chebi','4167')],'anatomy terms': [('go','0005615')]}}
                if participant_location == 'sources':
                    for q_varID, participant in participants.items():
                        update_unique_species(species_list,q_varID,participant,participant_location,v_ss_ID,model)

                if participant_location == 'sinks':
                    for q_varID, participant in participants.items():
                        update_unique_species(species_list,q_varID, participant,participant_location,v_ss_ID,model)
    
    for speciesID, species_info in species_list.items():
        print("species", speciesID, species_info)
        qvar_infos = species_info['varinfo']
        q_var = Variable(f"q_{speciesID}")
        q_var.setInitialValue(1.0)
        new_component.addVariable(q_var)
        ode_var = f'{q_var.name()}'
        new_v_ss_q = f'v_ss_{speciesID}_new'
        new_v_ss = Variable(new_v_ss_q)
        model = qvar_infos[0][0]
        v_ss_ID = qvar_infos[0][1]
        comp_name, fvar_name=getNamebyID(model, v_ss_ID)
        vss_units=model.component(comp_name).variable(fvar_name).units().clone()
        new_v_ss.setUnits(vss_units)
        new_component.addVariable(new_v_ss)
        new_component.appendMath(MATH_HEADER)
        new_component.appendMath(infix_to_mathml(''.join(new_v_ss_q), ode_var,voi="t"))
        new_component.appendMath(MATH_FOOTER)
        eq = []
        # get the units of the quantity variable        
        print('qvar_infos',qvar_infos)
        for qvar_info in qvar_infos:
            model = qvar_info[0]
            v_ss_ID = qvar_info[1]
            participant_location = qvar_info[2]
            coef=qvar_info[3]
            q_varID = qvar_info[4]
            model_info=selection_dict[model]
            qimport_components_dict=model_info['components']
            print('qimport_components_dict',qimport_components_dict)
            qcomp_name, qvar_name=getNamebyID(model, q_varID)
            qvar_units=model.component(qcomp_name).variable(qvar_name).units().clone()
            q_var.setUnits(qvar_units)
            for component in list(qimport_components_dict.keys()):
                if qcomp_name == qimport_components_dict[component]:
                    Variable.addEquivalence(new_component.variable(q_var.name()), new_model.component(component).variable(qvar_name))
                    break

            for fluxID, mediator_info in flux_list.items():
                print('flux',fluxID, mediator_info)
                flux_infos = mediator_info['varinfo']
                for flux_info in flux_infos:
                    model_f = flux_info[0]
                    v_ss_ID_f = flux_info[1]
                    if model == model_f and v_ss_ID == v_ss_ID_f:
                        comp_name, fvar_name=getNamebyID(model_f, v_ss_ID)
                        model_info=selection_dict[model_f]
                        import_components_dict=model_info['components']
                        for component in list(import_components_dict.keys()):
                           if comp_name == import_components_dict[component]:                              
                               var_list=getEntityList(new_model,new_model.name())
                               # get the end of the component name to avoid duplication
                               compid=component.split('_')[-1]
                               new_v_ss_name = f'{fvar_name}_{compid}'
                               if new_v_ss_name not in var_list:
                                      new_v_ss = Variable(new_v_ss_name)
                                      vss_units=model_f.component(comp_name).variable(fvar_name).units().clone()
                                      new_v_ss.setUnits(vss_units)
                                      new_component.addVariable(new_v_ss)                                      
                                      Variable.addEquivalence(new_component.variable(new_v_ss_name), new_model.component(component).variable(fvar_name))
                               else:
                                      Variable.addEquivalence(new_component.variable(new_v_ss_name), new_model.component(component).variable(fvar_name))                                                                    
                        if participant_location == 'sources':
                            if coef == 1:
                                eq.append(f'-{fvar_name}_{compid}')
                            else:
                                eq.append(f'-{coef}*{fvar_name}_{compid}')
                        elif participant_location == 'sinks':
                            if coef == 1:
                                if len(eq) == 0:
                                    eq.append(f'{fvar_name}_{compid}')
                                else:
                                    eq.append(f'+{fvar_name}_{compid}')
                            else:
                                if len(eq) == 0:
                                    eq.append(f'{coef}*{fvar_name}_{compid}')
                                else:
                                    eq.append(f'+{coef}*{fvar_name}_{compid}')
        new_component.appendMath(MATH_HEADER)
        new_component.appendMath(infix_to_mathml(''.join(eq), new_v_ss_q))
        new_component.appendMath(MATH_FOOTER)
    new_model.fixVariableInterfaces()            
    return new_model
        

def visualize_model(model,mode='root', annotations=None):
    # input: model, the CellML model object
    # output: None
    # visualize the model
    annotation_dict ={}
    if annotations is not None:
        proc_list = list(annotations.keys())
        for bioProc in proc_list:
            bioDict = annotations[bioProc]
            for key in bioDict: # 'cellml_path','mediator','sources','sinks'
                if isinstance (bioDict[key],dict):
                    for item_key, item_value in bioDict[key].items(): # item_key=varID, item_value={'physics':[('opb','OPB_00592')],'chemical terms':[('uniprot','P11166')],'anatomy terms': [('go','0005886')]}
                        annotation_dict.update({item_key:item_value})
    
    annotated_varIDs = list(annotation_dict.keys())

    G_model=nx.DiGraph()
    root=model.name()+'_model'
    G_model.add_node(root,shape='box',color='magenta',style='filled',level=0)
    
    def visualize_variable(comp,level):
        for v in range(comp.variableCount()):
            if (v % 2) == 0:
                sublevel = 1
            else:
                sublevel = 0
            node_level = level + sublevel
            var=comp.variable(v)
            if var.initialValue() != "":
                   G_model.add_node(comp.name()+var.name(),color='turquoise',shape="ellipse",level=node_level,label='{}: {}\n{init}'.format(var.name(),var.units().name(),init="init: "+var.initialValue()))
            else:
                G_model.add_node(comp.name()+var.name(),color='lightblue', shape="ellipse",level=node_level,label='{}: {}'.format(var.name(),var.units().name()))
            if comp.variable(v).equivalentVariableCount() > 0:                 
                for e in range(0,comp.variable(v).equivalentVariableCount()):
                    ev = comp.variable(v).equivalentVariable(e)
                    ev_parent = ev.parent()
                    if not comp.containsComponent(ev_parent):
                        G_model.add_edge(ev_parent.name()+ev.name(),comp.name()+var.name(),color='black')
                    elif mode=='complete':
                        G_model.add_edge(ev_parent.name()+ev.name(),comp.name()+var.name(),color='black')       
            G_model.add_edge(comp.name()+var.name(),comp.name(),color='blue',weight=1)
            varID = var.id()
            if varID in annotated_varIDs:
                for physics_term in annotation_dict[varID]['physics']:
                    G_model.add_node('{}: {}'.format(physics_term[0],physics_term[1]),label='{}: {}'.format(physics_term[0],physics_term[1]),color='red',level=node_level+1,shape="ellipse")
                    G_model.add_edge('{}: {}'.format(physics_term[0],physics_term[1]),comp.name()+var.name(),color='red')
                for chemical_term in annotation_dict[varID]['chemical terms']:
                    G_model.add_node('{}: {}'.format(chemical_term[0],chemical_term[1]),label='{}: {}'.format(chemical_term[0],chemical_term[1]),color='red',level=node_level+2,shape="ellipse")
                    G_model.add_edge('{}: {}'.format(chemical_term[0],chemical_term[1]),comp.name()+var.name(),color='red')
                for anatomy_term in annotation_dict[varID]['anatomy terms']:
                    G_model.add_node('{}: {}'.format(anatomy_term[0],anatomy_term[1]),label='{}: {}'.format(anatomy_term[0],anatomy_term[1]),color='red',level=node_level+1,shape="ellipse")
                    G_model.add_edge('{}: {}'.format(anatomy_term[0],anatomy_term[1]),comp.name()+var.name(),color='red')

    def visualize_comp(parentcomp,level):
        visualize_variable(parentcomp,level+1)
        if parentcomp.componentCount()>0:
            G_model.add_node(parentcomp.name(),shape='box',color='orange',style='filled',level=level)
        else:
            G_model.add_node(parentcomp.name(),shape='box',color='green',style='filled',level=level)
        
        if parentcomp.isImport():
            G_model.add_node(parentcomp.importReference(),shape='box',color='cyan',style='filled',level=level)
            G_model.add_edge(parentcomp.importReference(),parentcomp.name(),color='cyan')
            G_model.add_edge(parentcomp.importSource().url(),parentcomp.importReference(),color='cyan')

        if mode=='complete':            
            for c in range(parentcomp.componentCount()):
                childcomp=parentcomp.component(c)
                G_model.add_edge(childcomp.name(),parentcomp.name(),color='orange')
                visualize_comp(childcomp,level+3)       

    for c in range(model.componentCount()):
        G_model.add_edge(model.component(c).name(),root,color='red')
        visualize_comp(model.component(c),1)
        
   # A=nx.nx_agraph.to_agraph(G_model)
   # A.draw('model.png', format='png', prog='dot', args='-Grankdir=LR')
    return G_model


def get_bioProcess(rdf_g):
    # search for all biological processes in the RDF graph
    # return: a list of biological processes in the RDF graph [{'cellml_path': cellml_path,'mediator': mediator, 'sources': sources, 'sinks': sinks}]  
    bioProcesses = {}
    for local_proc in rdf_g.subjects(RDF_Graph.prefix_NAMESPACE['semsim']['hasMediatorParticipant'],None):
        local_procID = local_proc.n3(rdf_g.namespace_manager).split(':')[1]
        for flux_var in rdf_g.subjects(RDF_Graph.prefix_NAMESPACE['bqbiol']['isPropertyOf'], local_proc):
            flux_varID = flux_var.n3(rdf_g.namespace_manager).split(':')[1]
            cellml_path = flux_var.n3().split('#')[0].strip('<>')
            for flux_thing in rdf_g.objects(flux_var,RDF_Graph.prefix_NAMESPACE['bqbiol']['isVersionOf']):
                flux_onotology,_,flux_termID = rdf_g.compute_qname(flux_thing)
        local_mediator = rdf_g.value(local_proc, RDF_Graph.prefix_NAMESPACE['semsim']['hasMediatorParticipant'], None)
        if local_mediator is None:
            print('There is no mediator for the process.')
            return
        chemical_terms = []
        anatomy_terms = [] 
        for mediator in rdf_g.objects(local_mediator,RDF_Graph.prefix_NAMESPACE['bqbiol']['isVersionOf']):
            mediator_ontolgoy,_,mediator_termID = rdf_g.compute_qname(mediator)
            chemical_terms.append((mediator_ontolgoy,mediator_termID))     
        for mediator in rdf_g.objects(local_mediator,RDF_Graph.prefix_NAMESPACE['bqbiol']['isPartOf']):
            mediator_anatomy_ontology,_,mediator_anatomy_termID = rdf_g.compute_qname(mediator)
            anatomy_terms.append((mediator_anatomy_ontology,mediator_anatomy_termID))          
        mediator_dict = {flux_varID:{'physics':[(flux_onotology,flux_termID)], 'chemical terms': chemical_terms, 'anatomy terms': anatomy_terms}}
        sourceDict={}
        for local_source in rdf_g.objects(local_proc,RDF_Graph.prefix_NAMESPACE['semsim']['hasSourceParticipant']):
            source_var= rdf_g.value(None,RDF_Graph.prefix_NAMESPACE['bqbiol']['isPropertyOf'], local_source)
            source_varID = source_var.n3(rdf_g.namespace_manager).split(':')[1]
            coef = rdf_g.value(local_source, RDF_Graph.prefix_NAMESPACE['semsim']['hasMultiplier']).toPython()
            physics_terms=[]
            for source_thing in rdf_g.objects(source_var,RDF_Graph.prefix_NAMESPACE['bqbiol']['isVersionOf']):
                source_ontology,_,source_termID = rdf_g.compute_qname(source_thing)
                physics_terms.append((source_ontology,source_termID))
            anatomy_terms=[]
            chemical_terms=[]
            for SourceParticipant in rdf_g.objects(local_source,RDF_Graph.prefix_NAMESPACE['bqbiol']['isVersionOf']):
                SourceChemical_onotology,_, SourceChemical_termID= rdf_g.compute_qname(SourceParticipant)
                chemical_terms.append((SourceChemical_onotology,SourceChemical_termID))
            for SourceParticipant in rdf_g.objects(local_source,RDF_Graph.prefix_NAMESPACE['bqbiol']['isPartOf']):
                SourceAnatomy_onotology,_, SourceAnatomy_termID= rdf_g.compute_qname(SourceParticipant)
                anatomy_terms.append((SourceAnatomy_onotology,SourceAnatomy_termID)) 

            sourceDict.update({source_varID:{'proportionality':coef,'physics':physics_terms,'chemical terms':chemical_terms,'anatomy terms':anatomy_terms}})
        sinkDict={}
        for local_sink in rdf_g.objects(local_proc,RDF_Graph.prefix_NAMESPACE['semsim']['hasSinkParticipant']):
            sink_var= rdf_g.value(None,RDF_Graph.prefix_NAMESPACE['bqbiol']['isPropertyOf'], local_sink)
            sink_varID = sink_var.n3(rdf_g.namespace_manager).split(':')[1]
            coef = rdf_g.value(local_sink, RDF_Graph.prefix_NAMESPACE['semsim']['hasMultiplier']).toPython()
            physics_terms=[]
            for sink_thing in rdf_g.objects(sink_var,RDF_Graph.prefix_NAMESPACE['bqbiol']['isVersionOf']):
                sink_ontology,_,sink_termID = rdf_g.compute_qname(sink_thing)
                physics_terms.append((sink_ontology,sink_termID))
            anatomy_terms = []
            chemical_terms = []
            for SinkParticipant in rdf_g.objects(local_sink,RDF_Graph.prefix_NAMESPACE['bqbiol']['isVersionOf']):
                SinkChemical_ontology, _, SinkChemical_termID= rdf_g.compute_qname(SinkParticipant)
                chemical_terms.append((SinkChemical_ontology,SinkChemical_termID))
            for SinkParticipant in rdf_g.objects(local_sink,RDF_Graph.prefix_NAMESPACE['bqbiol']['isPartOf']):
                SinkAnatomy_ontology, _, SinkAnatomy_termID= rdf_g.compute_qname(SinkParticipant)
                anatomy_terms.append((SinkAnatomy_ontology,SinkAnatomy_termID))
            sinkDict.update({sink_varID:{'proportionality':coef,'physics':physics_terms,'chemical terms':chemical_terms,'anatomy terms':anatomy_terms}})
        
        bioProcesses.update({local_procID:{'cellml_path': cellml_path,'mediator': mediator_dict, 'sources': sourceDict , 'sinks':sinkDict}})
    
    return bioProcesses

# main function for testing
if __name__ == "__main__":

    rdf_g = RDF_Graph()
    filename = 'SLCT3_ss_test_inOne.cellml'
    foldername = 'C:/Users/wai484/Documents/BG2CellML/test/cellml/SLC_SS'
    filename = PurePath(foldername).joinpath(filename)
    rdf_editor = RDF_Editor(rdf_g,filename)
    comp_name = 'SLCT3_ss_test_inOne'
    mediatorDict={'v_ss':{'physics':[('opb','OPB_00592')],'chemical terms':[('uniprot','P11166')],'anatomy terms': [('go','0005886')]}}
    sourceDict={'q_Ao':{'proportionality':1,'physics':[('opb','OPB_00425')] ,'chemical terms':[('chebi','4167')],'anatomy terms': [('go','0005615')]}}
    sinkDict={'q_Ai':{'proportionality':1,'physics':[('opb','OPB_00425')] ,'chemical terms':[('chebi','4167')],'anatomy terms': [('go','0005829')]}}
    rdf_editor.annotate_bioProcess(comp_name,0, mediatorDict,sourceDict,sinkDict)
    rdf_editor.save_graph()

    bioPro=get_bioProcess(rdf_g)
    proc_list = list(bioPro.keys())
    for bioProc in proc_list:
        print('biological process:',bioProc)
        bioDict = bioPro[bioProc]
        for key in bioDict: # 'cellml_path','mediator','sources','sinks'
            print(key,':')
            if isinstance (bioDict[key],dict):
                for item_key, item_value in bioDict[key].items():
                    print(item_key,':',item_value)
            else:
                print(bioDict[key])  
    model=cellml.parse_model(filename, True)
    visualize_model(model,'root',bioPro)


