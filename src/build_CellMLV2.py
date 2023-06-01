from libcellml import Component, Generator, GeneratorProfile, Model, Units,  Variable, ImportSource, Printer, Annotator
import pandas as pd
from utilities import print_model, ask_for_file_or_folder, ask_for_input, infix_to_mathml
import cellml
from pathlib import PurePath
import os
import re 

MATH_HEADER = '<math xmlns="http://www.w3.org/1998/Math/MathML" xmlns:cellml="http://www.cellml.org/cellml/2.0#">\n'
MATH_FOOTER = '</math>\n'
BUILTIN_UNITS = {'ampere':Units.StandardUnit.AMPERE, 'becquerel':Units.StandardUnit.BECQUEREL, 'candela':Units.StandardUnit.CANDELA, 'coulomb':Units.StandardUnit.COULOMB, 'dimensionless':Units.StandardUnit.DIMENSIONLESS, 
                 'farad':Units.StandardUnit.FARAD, 'gram':Units.StandardUnit.GRAM, 'gray':Units.StandardUnit.GRAY, 'henry':Units.StandardUnit.HENRY, 'hertz':Units.StandardUnit.HERTZ, 'joule':Units.StandardUnit.JOULE,
                   'katal':Units.StandardUnit.KATAL, 'kelvin':Units.StandardUnit.KELVIN, 'kilogram':Units.StandardUnit.KILOGRAM, 'liter':Units.StandardUnit.LITRE, 'litre':Units.StandardUnit.LITRE, 
                   'lumen':Units.StandardUnit.LUMEN, 'lux':Units.StandardUnit.LUX, 'metre':Units.StandardUnit.METRE, 'meter':Units.StandardUnit.METRE, 'mole':Units.StandardUnit.MOLE, 'newton':Units.StandardUnit.NEWTON, 
                   'ohm':Units.StandardUnit.OHM, 'pascal':Units.StandardUnit.PASCAL, 'radian':Units.StandardUnit.RADIAN, 'second':Units.StandardUnit.SECOND, 'siemens':Units.StandardUnit.SIEMENS, 'sievert':Units.StandardUnit.SIEVERT, 
                   'steradian':Units.StandardUnit.STERADIAN, 'tesla':Units.StandardUnit.TESLA, 'volt':Units.StandardUnit.VOLT, 'watt':Units.StandardUnit.WATT, 'weber':Units.StandardUnit.WEBER}

def getEntityList(model, comp_name=None):
    # input: model, the CellML model object
    #        comp_name, the CellML component name
    # output: a list of the entity names.
    # if the component name is not provided, the list of the component names is returned;
    # if the component name is provided, the list of the variable names is returned
    if comp_name is None:
        return [model.component(comp_numb).name() for comp_numb in range(model.componentCount())]
    else:
        return [model.component(comp_name).variable(var_numb).name() for var_numb in range(model.component(comp_name).variableCount())]
    
def getEntityName_UI(model, comp_name=None):
    # input: model, the CellML model object
    #        comp_name, the CellML component name
    # output: the name of the entity.
    # if the component name is not provided, ask user to select the name from the component list and return the name of the component; 
    # if the component name is provided, ask user to select the name from the variable list and return the name of the variable
    if comp_name is None:
        message = 'Please select the component'
        choices = getEntityList(model)
        return ask_for_input(message, 'List', choices)
    else:
        message = 'Please select the variable'
        choices = getEntityList(model, comp_name)
        return ask_for_input(message, 'List', choices)

#----------------------------------------------------------------------Build a CellML model from a csv file--------------------------------------------------------------
""" Read a csv file and create components and variables from it. """
def read_csv_UI():
    # Get the csv file from the user by opening a file dialog
    message='Please select the csv file to collect components:'
    file_path = ask_for_file_or_folder(message)
    return file_path

def read_csv(file_path):    
    # input: file_path: the path of the csv file (including the file name and extension)
    # output: None, write the components and variables to a CellML model, saved as a .cellml file

    # Read the csv file and create components and variables from it
    df = pd.read_csv(file_path, sep=',', header=0, index_col=False,na_values='nan')
    df['component']=df['component'].fillna(method="ffill")
    gdf=df.groupby('component')
    params_comp = Component('param')
    components = []
    # Create CellML Variable for each variable in the component and add it to the component
        # Rules: 1. if the initial_value is nan, then the initial_value is None;
        #        2. if the param column is 'param', then the variable is a parameter and it will be added to the params list; 
        #           The initial_value of the variable will be None; 
        #           The initial_value of the parameter will be the value in the initial_value column;
        #        3. if the param column is init, then the variable is a state variable, and the variable name + '_init' will be added to the params list;
        #           The initial_value of the variable will be variable name + '_init'; 
        #           The initial_value of the parameter (variable name + '_init') will be the value in the initial_value column; 
    for component_name, groupi in gdf:
        component=Component(component_name)          
        for index, row in groupi.iterrows():
            units_name = row['units']
            var_name = row['variable']
            variable = Variable(var_name)
            units = Units(units_name)
            variable.setUnits(units)
            variable.setInterfaceType(Variable.InterfaceType.PUBLIC)
            if pd.isna(row['initial_value']):
                pass
            elif row["param"]=='param':
                param = variable.clone()
                param.setInitialValue(row['initial_value'])
                params_comp.addVariable(param)                                             
            elif row['param'] == 'init':
                param = Variable(var_name+'_init')
                variable.setInitialValue(param)
                param.setUnits(units)
                param.setInitialValue(row['initial_value'])
                params_comp.addVariable(param)
            else:
                variable.setInitialValue(row['initial_value'])
            component.addVariable(variable)
                 
        components.append(component)
    
    if params_comp.variableCount()>0:        
        components.append(params_comp)
    
    # Write the components to a CellML file
    model_name = PurePath(file_path).stem
    full_path = PurePath(file_path).parent.joinpath(model_name+'.cellml')
    modeli = Model(model_name+'_comps')
    for component in components:
        modeli.addComponent(component)
    writeCellML(full_path,modeli)

    return components   

"""" Parse a cellml file."""
def parseCellML_UI(strict_mode=True):
    message='Please select the CellML file:'
    full_path = ask_for_file_or_folder(message)   
    # Parse the CellML file
    existing_model=cellml.parse_model(full_path, strict_mode)
    return full_path, existing_model

""""To set up for importing a CellML model."""
def import_setup(model_path,full_path, strict_mode=True):
    # input: model_path: the directory of the CellML model that imports other CellML models
    #        full_path: the path of the CellML model that is imported (including the file name and extension)
    #        strict_mode: whether to use strict mode when parsing the CellML model
    # output: import_model: the existing model that is imported
    #         importSource: the ImportSource object which contains the url of the imported model
    import_model=cellml.parse_model(full_path, strict_mode)
    relative_path_os = os.path.relpath(full_path, model_path)
    relative_path=PurePath(relative_path_os).as_posix()
    importSource = ImportSource()
    importSource.setUrl(relative_path)
    importSource.setModel(import_model)
    return importSource, import_model

"""" The user interface for importing specific components from a CellML model."""
def importComponent_UI(import_model):
    # input: import_model: the existing model that is imported
    # output: import_component_dict: a dictionary of the import components,
    #                                 key: the name of the import component
    #                                 value: component_ref of the import component
    import_component_dict ={}
    message="Please select the components to import:"
    imported_components = ask_for_input( message, 'Checkbox', getEntityList(import_model))
    for component in imported_components:
        message=f"If you want to rename the component {component}, please type the new name. Otherwise, just press 'Enter':"
        answer = ask_for_input(message, 'Text')
        if answer!='':
            import_component_dict.update({answer: component})
        else:
            import_component_dict.update({component:component})
    return import_component_dict

def importComponents_default(model_path, importFile):
    # input: model_path: the path of the CellML model that imports other CellML models
    #        importFile: the path of the CellML model that is imported (including the file name and extension)
    # output: importSources: the ImportSource objects, only one ImportSource object in this case
    #         import_components_dicts: a dictionary of the imported components, 
    #                                   key: the name of the import component
    #                                   value: component_ref of the import component                               
    importSource, import_model = import_setup(model_path,importFile, True)
    imported_components = getEntityList(importSource.model())
    import_components_dict = {}
    for component in imported_components:
        import_components_dict.update({component:component})
    return  importSource, import_model, import_components_dict

"""" Collect import components from multiple cellml files with user inputs."""
def importComponents_UI(model_path,strict_mode=True):
    # input: model_path: the path of the CellML model that imports other CellML models
    #        strict_mode: whether to use strict mode when parsing the CellML model
    # output: importSources: a list of the ImportSource objects
    #         import_components_dicts: a list of dictionary of the imported components, 
    #                                   key: the name of the import component
    #                                  value: component_ref of the import component 
    import_action = ask_for_input('Do you want to import components?', 'Confirm', True)
    importSources,import_models, import_components_dicts = [], [], []
    while import_action:
        message='Please select the CellML file to import components:'
        full_path = ask_for_file_or_folder(message)
        importSource, import_model = import_setup(model_path,full_path, strict_mode)
        import_components_dict = importComponent_UI(importSource.model())
        importSources.append(importSource)
        import_models.append(import_model)
        import_components_dicts.append(import_components_dict)
        import_action = ask_for_input('Do you want to continue to import components?', 'Confirm', False)

    return  importSources, import_models, import_components_dicts

""" Carry out the import of components . """
def importComponents(model,importSource,import_model,import_components_dict):
    # input: model: the model that imports other CellML models
    #        importSource: the ImportSource object
    #        imported_components_dict: a dictionary of the imported components 
    # output: None
    #        The import components will be added to the model          
    
    for component in list(import_components_dict.keys()):
        c = Component(component)
        c.setImportSource(importSource)
        c.setImportReference(import_components_dict[component])
        dummy_c = import_model.component(c.importReference()).clone()
        while(dummy_c.variableCount()):
             c.addVariable(dummy_c.variable(0))
        model.addComponent(c) 
""" Carry out the clone of components (temporary solution to get around of units issues of libcellml) . """
def importComponents_clone(model,import_model,import_components_dict):        
    
    for component in list(import_components_dict.keys()):
        importReference=import_components_dict[component]
        dummy_c = import_model.component(importReference).clone()
        dummy_c.setName(component)
        model.addComponent(dummy_c)
        real_c = import_model.component(importReference)
        # list of the children components of the dummy component
        children_components = [dummy_c.component(child_numb).name() for child_numb in range(dummy_c.componentCount())]
        # check if the component has children components and if the children components have equivalent variables
        for child_numb in range(dummy_c.componentCount()):
            dummy_c_child = dummy_c.component(child_numb)
            real_c_child = real_c.component(child_numb)
            for var_numb in range(dummy_c_child.variableCount()):
                if real_c_child.variable(var_numb).equivalentVariableCount()>0:
                    for e in range(real_c_child.variable(var_numb).equivalentVariableCount()):
                        ev = real_c_child.variable(var_numb).equivalentVariable(e)          
                        ev_parent = ev.parent()
                        if ev_parent.name() in children_components:
                            Variable.addEquivalence(dummy_c_child.variable(var_numb), model.component(ev_parent.name()).variable(ev.name())) 
                        if ev_parent.name() == real_c.name():
                            Variable.addEquivalence(dummy_c_child.variable(var_numb), model.component(dummy_c.name()).variable(ev.name()))             
    copyUnits_temp(model,import_model)



def importUnits_UI(model_path,strict_mode=True):
    if ask_for_input('Do you want to import Units?', 'Confirm', True):
        message='Please select the CellML file to import Units:'
        full_path = ask_for_file_or_folder(message)
        importSource, import_model = import_setup(model_path,full_path, strict_mode)
        return importSource, import_model
    else:
        return None, None

""" Import units or components from an existing CellML model. """
def importUnits(model,importSource,units_model):
    # input: model: the model that imports units from other CellML models
    #        importSource: the ImportSource object
    # output: None
    #        The import units will be added to the model; 
    #        The units to import are determined by the intersection of units_undefined in the model and the units defined in the import source
    units_undefined=_checkUndefinedUnits(model)
    if len(units_undefined)>0:
        # Get the intersection of the units_undefined and the units defined in the import source
        if importSource.model() is None:
            print('The import source is not valid.')
        existing_units=set([units_model.units(unit_numb).name() for unit_numb in range(units_model.unitsCount())]) # Get the units names defined in the import source
        units_to_import = units_undefined.intersection(existing_units)
    else:
        units_to_import = set()
    for unit in units_to_import:
        u = Units(unit) # Get the units object from the import source based on the name
        u.setImportSource(importSource)
        u.setImportReference(unit)
        model.addUnits(u)
    print(f'The units {units_to_import} have been imported.')

def copyUnits(model,importSource,units_model):
    # input: model: the model that imports units from other CellML models
    #        importSource: the ImportSource object
    # output: None
    #        The import units will be added to the model; 
    #        The units to import are determined by the intersection of units_undefined in the model and the units defined in the import source
    units_undefined=_checkUndefinedUnits(model)
    if len(units_undefined)>0:
        # Get the intersection of the units_undefined and the units defined in the import source
        if importSource.model() is None:
            print('The import source is not valid.')
        existing_units=set([units_model.units(unit_numb).name() for unit_numb in range(units_model.unitsCount())]) # Get the units names defined in the import source
        units_to_copy = units_undefined.intersection(existing_units)
    else:
        units_to_copy = set()
    units_to_copy.add('per_sec')
    units_to_copy.add('per_fmol')
    for unit in units_to_copy:
        u = units_model.units(unit).clone() # Get the units object from the import source based on the name       
        model.addUnits(u)
    print(f'The units {units_to_copy} have been copied.')

def copyUnits_temp(model,units_model):
    # input: model: the model that imports units from other CellML models
    #        importSource: the ImportSource object
    # output: None
    #        The import units will be added to the model; 
    #        The units to import are determined by the intersection of units_undefined in the model and the units defined in the import source
    units_undefined=_checkUndefinedUnits_temp(model)
    if len(units_undefined)>0:
        # Get the intersection of the units_undefined and the units defined in the import source
        existing_units=set([units_model.units(unit_numb).name() for unit_numb in range(units_model.unitsCount())]) # Get the units names defined in the import source
        units_to_copy = units_undefined.intersection(existing_units)
    else:
        units_to_copy = set()
    for unit in units_to_copy:
        u = units_model.units(unit).clone() # Get the units object from the import source based on the name       
        model.addUnits(u)
    print(f'The units {units_to_copy} have been copied.')

"""Check the undefined non base units"""
def _checkUndefinedUnits_temp(model):
    # inputs:  a model object
    # outputs: a set of undefined units names
    units_claimed = set()
    def _getUnitsClaimed(component):
        for var_numb in range(component.variableCount()):
            if component.variable(var_numb).units().name() != '':
                if  not (component.variable(var_numb).units().name() in BUILTIN_UNITS.keys()):
                    units_claimed.add(component.variable(var_numb).units().name())
        for child_numb in range(component.componentCount()):
            _getUnitsClaimed(component.component(child_numb))

    for comp_numb in range(model.componentCount()): # Does it count the import components?
        if not model.component(comp_numb).requiresImports(): # Check if the component is imported
            _getUnitsClaimed(model.component(comp_numb))
    
    for units_numb in range(model.unitsCount()):
        # print(model.units(unit_numb).name())
        for unit_numb in range(model.units(units_numb).unitCount()):
            if  not (model.units(units_numb).unitAttributeReference(unit_numb) in BUILTIN_UNITS.keys()):
                units_claimed.add(model.units(units_numb).unitAttributeReference(unit_numb))

    units_defined = set()
    for units_numb in range(model.unitsCount()):
        # print(model.units(unit_numb).name())
        units_defined.add(model.units(units_numb).name()) 
    units_undefined = units_claimed - units_defined
    return units_undefined

"""Check the undefined non base units"""
def _checkUndefinedUnits(model):
    # inputs:  a model object
    # outputs: a set of undefined units names
    units_claimed = set()
    for comp_numb in range(model.componentCount()): # Does it count the import components?
        if not model.component(comp_numb).requiresImports(): # Check if the component is imported
            for var_numb in range(model.component(comp_numb).variableCount()):
                if model.component(comp_numb).variable(var_numb).units().name() != '':
                    if  not (model.component(comp_numb).variable(var_numb).units().name() in BUILTIN_UNITS.keys()):
                        units_claimed.add(model.component(comp_numb).variable(var_numb).units().name())
    units_defined = set()
    for unit_numb in range(model.unitsCount()):
        # print(model.units(unit_numb).name())
        units_defined.add(model.units(unit_numb).name()) 
    units_undefined = units_claimed - units_defined
    return units_undefined

def encapsulate_UI(model):
    # input: model: the model object that includes the components to be encapsulated
    # output: component_parent_selected: the name of the parent component
    #         component_children_selected: a list of the names of the children components
    confirm =ask_for_input('Do you want to encapsulate components', 'Confirm', False)
    if confirm: 
        message="Please select the parent component:"
        component_list = getEntityList(model)
        component_parent_selected = ask_for_input(message, 'List', component_list)
        message="Please select the children components:"
        choices=[comp_name for comp_name in component_list if comp_name != component_parent_selected]
        component_children_selected = ask_for_input(message, 'Checkbox', choices)
    else:
        component_parent_selected = ''
        component_children_selected = []
    return component_parent_selected, component_children_selected

""" Carry out the encapsulation. """
def encapsulate(model, component_parent_selected, component_children_selected):
    # input: model: the model object that includes the components to be encapsulated
    #        component_parent_selected: the name of the parent component
    #        component_children_selected: a list of the names of the children components
    # output: None
    #        The encapsulation will be added to the model
    for component_child in component_children_selected:
        model.component(component_parent_selected).addComponent(model.component(component_child))


""" Find the variables that are mapped in two components. """
def _findMappedVariables(comp1,comp2):
    # input: comp1: the first component
    #        comp2: the second component
    # output: mapped_variables_comp1: a list of the names of the variables in comp1 that are mapped to variables in comp2
    #         mapped_variables_comp2: a list of the names of the variables in comp2 that are mapped to variables in comp1
    mapped_variables_comp1 = []
    mapped_variables_comp2 = []
    for v in range(comp1.variableCount()):
        if comp1.variable(v).equivalentVariableCount()>0:
            for e in range(comp1.variable(v).equivalentVariableCount()):
                ev = comp1.variable(v).equivalentVariable(e)
                if ev is None:
                    print("WHOOPS! Null equivalent variable!")
                    continue               
                ev_parent = ev.parent()
                if ev_parent is None:
                    print("WHOOPS! Null parent component for equivalent variable!")
                    continue  
                if ev_parent.name() == comp2.name():
                    mapped_variables_comp1.append(comp1.variable(v).name())
                    mapped_variables_comp2.append(ev.name())
    return mapped_variables_comp1, mapped_variables_comp2

""" Find the variables that share the same name in two components. """
def sharedVars(comp1, comp2):
    # input: comp1: the first component
    #        comp2: the second component
    # output: shared_variables: a set of the names of the variables that share the same name in comp1 and comp2
    variables1 = [comp1.variable(var_numb).name() for var_numb in range(comp1.variableCount())]
    variables2 = [comp2.variable(var_numb).name() for var_numb in range(comp2.variableCount())]
    shared_variables = set(variables1).intersection(variables2)
    return shared_variables

"""" Clone variables from comp1 to comp2 if you want to expose some variables in comp1 via comp2 but comp2 does not have the variables. Visa versa. """
def cloneVariables_UI(comp1,comp2):
    # input: comp1: the first component
    #        comp2: the second component
    # output: None
    #        The variables will be cloned from comp1 to comp2
    shared_variables = sharedVars(comp1, comp2)
    # Get the variables in the two components that are not sharing the same name
    variables1 = [comp1.variable(var_numb).name() for var_numb in range(comp1.variableCount()) if comp1.variable(var_numb).name() not in shared_variables]
    variables2 = [comp2.variable(var_numb).name() for var_numb in range(comp2.variableCount()) if comp2.variable(var_numb).name() not in shared_variables]
    if len(variables1)>0:
        message=f"Please select the unmapped variables in {comp1.name()} to clone and map or Enter to skip:"
        choices=[var for var in variables1]
        answers = ask_for_input( message, 'Checkbox', choices)
        for var in answers:
            comp2.addVariable(comp1.variable(var).clone())
            Variable.addEquivalence(comp1.variable(var), comp2.variable(var))     
    if len(variables2)>0:    
        message=f"Please select the unmapped variables in {comp2.name()} to clone and map or Enter to skip:"
        choices=[var for var in variables2]
        answers = ask_for_input( message, 'Checkbox', choices)
        for var in answers:
            comp1.addVariable(comp2.variable(var).clone())
            Variable.addEquivalence(comp1.variable(var), comp2.variable(var))

def compPair4CloneVars_UI(model):
    # input: model: the model object that includes the components 
    # output: None
    #        The variables will be cloned from one component to another
    #         
    component_list = getEntityList(model)
    comp1_list = []
    comp2_list = []
    if len(component_list) > 2:
        while True:
            confirm =ask_for_input('Do you want to clone variables from one component to another', 'Confirm', False)
            if confirm:
                message="Please select the first component:"
                comp1 = ask_for_input(message, 'List', component_list)
                comp1_list.append(comp1)
                message="Please select the second component:"
                comp2 = ask_for_input(message, 'List', [comp for comp in component_list if comp!= comp1])
                comp2_list.append(comp2) 
                cloneVariables_UI(comp1,comp2)      
            else:
                break

"""" Provide variable connection suggestion based on shared variable name and carry on the variable mapping according to user inputs. """
def mapVariablesbyName_UI (model, comp1, comp2):
    shared_variables = sharedVars(comp1, comp2)
    mapped_variables_comp1, mapped_variables_comp2= _findMappedVariables(comp1,comp2)
    shared_variables_unmapped = shared_variables.difference(set(mapped_variables_comp1))
    if len(shared_variables_unmapped)>0:
        print('The variable names that are shared by the two components but unmapped are:', shared_variables_unmapped)
        message="Please select the variables to map. If you want to map all the variables, just press 'Enter'"
        choices=[var for var in shared_variables_unmapped]
        answers = ask_for_input( message, 'Checkbox', choices)
        if len(answers)>0:
            for var in answers:
                if Units.compatible(model.component(comp1.name()).variable(var).units(), model.component(comp2.name()).variable(var).units()):
                    Variable.addEquivalence(comp1.variable(var), comp2.variable(var))
                else:
                    Variable.addEquivalence(comp1.variable(var), comp2.variable(var))
                    print(f'{var} has units {comp1.variable(var).units().name()} in {comp1.name()} but {comp2.variable(var).units().name()} in {comp2.name()}, which are not compatible.')
                
        else:
            for var in shared_variables_unmapped:
                if Units.compatible(model.component(comp1.name()).variable(var).units(), model.component(comp2.name()).variable(var).units()):
                    Variable.addEquivalence(comp1.variable(var), comp2.variable(var))
                else:
                    Variable.addEquivalence(comp1.variable(var), comp2.variable(var))
                    print(f'{var} has units {comp1.variable(var).units().name()} in {comp1.name()} but {comp2.variable(var).units().name()} in {comp2.name()}, which are not compatible.') 

"""" Provide variable connection suggestion for unmapped variables (may have different name) and carry on the variable mapping according to user inputs."""
def mapVariables_UI (model, comp1, comp2):

    mapped_variables_comp1, mapped_variables_comp2= _findMappedVariables(comp1,comp2)
    unmapped_variables_comp1 = [comp1.variable(v).name() for v in range(comp1.variableCount()) if comp1.variable(v).name() not in mapped_variables_comp1]
    unmapped_variables_comp2 = [comp2.variable(v).name() for v in range(comp2.variableCount()) if comp2.variable(v).name() not in mapped_variables_comp2]
    print(f'The unmapped variables in {comp1.name()} are:', unmapped_variables_comp1)
    print(f'The unmapped variables in {comp2.name()} are:', unmapped_variables_comp2)

    while True:
        if len(unmapped_variables_comp1)>0 and len(unmapped_variables_comp2)>0 and ask_for_input('Do you want to map the unmapped variables?', 'Confirm', False):
            message=f"Please select one variable in {comp1.name()} and another in {comp2.name()} to map"
            choices=[f'{comp1.name()}:{var}' for var in unmapped_variables_comp1] + [f'{comp2.name()}:{var}' for var in unmapped_variables_comp2]
            answers = ask_for_input( message, 'Checkbox', choices)
            if len(answers)>0:
                var1 = answers[0].split(':')[1]
                var2 = answers[1].split(':')[1]
                if Units.compatible(model.component(comp1.name()).variable(var1).units(), model.component(comp2.name()).variable(var2).units()):
                    Variable.addEquivalence(comp1.variable(var1), comp2.variable(var2))
                else:
                    Variable.addEquivalence(comp1.variable(var1), comp2.variable(var2))
                    print(f'{var1} has units {comp1.variable(var1).units().name()} in {comp1.name()} but {comp2.variable(var2).units().name()} in {comp2.name()}, which are not compatible.')
            else:
                break
        else:
            break
""""Get the variables in the two components that are mapped but both have initial values; ask the user to select the initial value to keep"""
def fixInits_UI (comp1, comp2):
    mapped_variables_comp1, mapped_variables_comp2= _findMappedVariables(comp1,comp2)
    doubleInit = [(var1,var2) for var1,var2 in zip(mapped_variables_comp1, mapped_variables_comp2) if (comp1.variable(var1).initialValue()!='') and (comp2.variable(var2).initialValue()!= '')]
    for var1,var2 in doubleInit:
        message=f"Please select the initial value to keep for {var1} in {comp1.name()} and {var2} in {comp2.name()}"
        choices=[f'{comp1.name()}:{var1}:{comp1.variable(var1).initialValue()}', f'{comp2.name()}:{var2}:{comp2.variable(var2).initialValue()}']
        answer = ask_for_input( message, 'List', choices)
        if answer ==f'{comp1.name()}:{var1}:{comp1.variable(var1).initialValue()}':
            comp2.variable(var2).removeInitialValue()
        else:
            comp1.variable(var1).removeInitialValue()

def checkInits(model):
    # input: model: the model object
    # output: 1. a set of variables that have no initial values set((comp1,var1),(comp1,var1)); 
    #         2. a set of variables that have more than two initial values set(set((comp1,var1),(comp1,var1)),set((comp1,var1),(comp1,var1)))
    # get the list of variables on the left hand side of the equations
    equations=getEquations(model)
    regex = r'<apply>\s*<eq/>\s*<ci>(.*?)</ci>\s*<apply>'
    output_dict = {}
    for comp_name, equation in equations.items():
        math_c_reg = equation.replace('\n','')
        output_vars = re.findall(regex, math_c_reg)
        output_dict.update({comp_name:output_vars})
    
    regex = r'<apply>\s*<eq/>\s*<apply>\s*<diff/>\s*<bvar>\s*<ci>(.*?)</ci>\s*</bvar>\s*<ci>(.*?)</ci>\s*</apply>' # odes
    for comp_name, equation in equations.items():
        math_c_reg = equation.replace('\n','')
        output_vars = re.findall(regex, math_c_reg)
        for var in output_vars:
            output_dict[comp_name].append(var[1]) # 

    comp_withMath_list = list(output_dict.keys())

    noInit = set()
    multipleInit = {}
    def _checkInits(parentcomp):
        multipleInit.update({parentcomp.name():[]})
        for var_numb in range(parentcomp.variableCount()):
            if parentcomp.variable(var_numb).equivalentVariableCount()==0:
                if parentcomp.variable(var_numb).initialValue() == '':
                    if parentcomp.name() in comp_withMath_list:
                        if parentcomp.variable(var_numb).name() not in output_dict[parentcomp.name()]:
                           noInit.add((parentcomp.name(), parentcomp.variable(var_numb).name()))                   
            else:
                tempset=set()
                initcount = 0

                if parentcomp.variable(var_numb).initialValue() != '':
                    initcount += 1
                    tempset.add((parentcomp.name(), parentcomp.variable(var_numb).name())) 
                for e in range(parentcomp.variable(var_numb).equivalentVariableCount()):
                    ev = parentcomp.variable(var_numb).equivalentVariable(e)               
                    ev_parent = ev.parent()
                    if ev.initialValue() != '':
                        initcount += 1
                        tempset.add((ev_parent.name(), ev.name()))
                
                if initcount > 1:
                    multipleInit[parentcomp.name()].append(tempset)
                elif initcount == 0:
                    if parentcomp.name() in comp_withMath_list:
                        if parentcomp.variable(var_numb).name() not in output_dict[parentcomp.name()]:
                           noInit.add((parentcomp.name(), parentcomp.variable(var_numb).name()))
                    else:
                        flag_output = False
                        for comp_withMath, output_vars in output_dict.items():
                            for output_var in output_vars:
                                if not parentcomp.variable(var_numb).hasEquivalentVariable(model.component(comp_withMath).variable(output_var),True): # to do: seems not working
                                    print(comp_withMath, output_var,parentcomp.variable(var_numb).name()) #
                                    #noInit.add((parentcomp.name(), parentcomp.variable(var_numb).name()))                           
                                for e in range(parentcomp.variable(var_numb).equivalentVariableCount()):
                                    ev = parentcomp.variable(var_numb).equivalentVariable(e)               
                                    ev_parent = ev.parent()
                                    if ev_parent.name()==comp_withMath and ev.name()==output_var:
                                        flag_output = True
                                        break
                        if not flag_output:
                            noInit.add((parentcomp.name(), parentcomp.variable(var_numb).name()))

        for child_numb in range(parentcomp.componentCount()):
            _checkInits(parentcomp.component(child_numb))

    for comp_numb in range(model.componentCount()):
        _checkInits(model.component(comp_numb))
    
    multipleInit_summary = set()
    for comp in multipleInit.keys():
        for item in multipleInit[comp]:
            multipleInit_summary.add(item)

    return noInit, multipleInit_summary

def addInits(model,comp_name,var_name,init):
    # input: model: the model object
    #        comp_name: the name of the component
    #        var_name: the name of the variable
    #        init: the initial value to be set
    # output: None
    #        The initial value will be set to the variable
    model.component(comp_name).variable(var_name).setInitialValue(init)

def update_varmap(model, varmaps):
    # input: model, the CellML model object
    #        varmaps, a list of variable mappings [(comp1,var1,comp2,var2),(comp3,var3,comp4,var4)]
    for varmap in varmaps:
        comp1 = varmap[0]
        var1 = varmap[1]
        comp2 = varmap[2]
        var2 = varmap[3]
        Variable.addEquivalence(model.component(comp1).variable(var1), model.component(comp2).variable(var2))


def suggestConnection (model,comp1, comp2):
    mapVariablesbyName_UI (model, comp1, comp2)
    mapVariables_UI (model, comp1, comp2)

# Find the components that have encapsulated components, and connect the parent and children components
def suggestConnection_parent_child(base_dir,model,parent_component):
    importer = cellml.resolve_imports(model, base_dir, True)
    flatModel = importer.flattenModel(model) # this may not be necessary after the units compatibility check function is fixed
    if parent_component.componentCount()>0:
        for child_numb in range(parent_component.componentCount()):                
            child_component = parent_component.component(child_numb)
            suggestConnection(flatModel,parent_component, child_component)
            fixInits_UI (parent_component, child_component)
            suggestConnection_parent_child(base_dir,model,child_component)

""" Carry out the connection. """
def connect_UI(base_dir,model):
    importer = cellml.resolve_imports(model, base_dir, True)
    flatModel = importer.flattenModel(model) # this may not be necessary after the units compatibility check function is fixed
    # List the components in the model
    components = getEntityList(model)
    if len(components)>1:
        for comp_numb in range(model.componentCount()):
            parent_component = model.component(comp_numb)
            suggestConnection_parent_child(base_dir,model,parent_component)    
        while True:
            message = 'Please select two components to connect or Enter to skip:'
            answer = ask_for_input(message, 'Checkbox', components)       
            if len(answer)>0:
                comp1= answer[0]
                comp2= answer[1]
                suggestConnection(flatModel, model.component(comp1), model.component(comp2))
                fixInits_UI (model.component(comp1), model.component(comp2))
            else:
                break
    
def defineUnits_UI(iunitsName):
    print(f'Please define the units {iunitsName}:')
    message = 'Please type the name of the standardUnit or press Enter to skip:'
    unitName = ask_for_input(message, 'Text')
    message = 'Please type the prefix or press Enter to skip:'
    prefix = ask_for_input(message, 'Text')
    message = 'Please type the exponent or press Enter to skip:'
    exponent = ask_for_input(message, 'Text')
    message = 'Please type the multiplier or press Enter to skip:'
    multiplier = ask_for_input(message, 'Text')
    return unitName, prefix, exponent, multiplier

# Define the units
def _defineUnits(iunitsName):
    iunits = Units(iunitsName)
    while True:
        unitName, prefix, exponent, multiplier = defineUnits_UI(iunitsName)
        if unitName == '':
            break
        else:    
            if exponent != '':
                exponent = float(exponent)
            else:
                exponent = 1.0
            if multiplier != '':
                multiplier = float(multiplier)
            else:
                multiplier = 1.0   
            if prefix == '':
                prefix = 0   
            if unitName in BUILTIN_UNITS:
                iunits.addUnit(BUILTIN_UNITS[unitName], prefix, exponent, multiplier)
            else:
                iunits.addUnit(unitName,prefix, exponent, multiplier)                
    return iunits

# Add units to the model
def addUnits_UI(model):
    units_undefined=_checkUndefinedUnits(model)
    print('The units claimed in the variables but undefined are:',units_undefined)
    # Ask the user to add the units which are claimed in the variables but not defined in the model
    for units in units_undefined:
        while True:
            message = 'Do you want to add units:' + units + '?'
            answer = ask_for_input(message, 'Confirm', True)           
            if answer:
                iunits=_defineUnits(units)
                model.addUnits(iunits)
            else:
                break
# Write the equations to a component
def writeEquations_UI(component):
    while True:
        message = 'Please type the lefthand of the equation or press Enter to skip:'
        ode_var = ask_for_input(message, 'Text')
        if ode_var != '':            
            message = 'Please type the righthand of the equation:'
            infix = ask_for_input(message, 'Text')
            message = 'Please type the the variable of integration or press Enter to skip:'
            voi = ask_for_input(message, 'Text')
            component. appendMath(infix_to_mathml(infix, ode_var, voi))
        else:
            break

# Add equations to the model
def addEquations(component, equations):

    component.setMath(MATH_HEADER)            
    for equation in equations:
        infix = equation[0]
        ode_var = equation[1]
        voi = equation[2]
        component. appendMath(infix_to_mathml(infix, ode_var, voi))
    component. appendMath(MATH_FOOTER)

def getEquations(model):
    # input: model: the model object
    # output: equations: a dictionary of the equations in the model: {component_name:equation}
    equations = {}
    def _getEquations(component):
        if component.math()!='':
            equations.update({component.name():component.math()})
        if component.componentCount()>0:
            for c in range(component.componentCount()):                   
                   _getEquations(component.component(c))
    
    for c in range(model.componentCount()):
            _getEquations(model.component(c))
    return equations

def writeCellML_UI(model_path, model):
    message = f'If you want to change the default filename {model.name()}.cellml, please type the new name. Otherwise, just press Enter.'
    file_name = ask_for_input(message, 'Text')
    if file_name == '':
        file_name=model.name()+'.cellml'
    else:
        file_name=file_name+'.cellml'
    full_path = str(PurePath(model_path).joinpath(file_name))
    return full_path

# Write a model to cellml file, input: directory, model, output: cellml file
def writeCellML(full_path, model): 
    assignAllIds(model)    
    printer = Printer()
    serialised_model = printer.printModel(model)    
    write_file = open(full_path, "w")
    write_file.write(serialised_model)
    write_file.close()
    print('CellML model saved to:',full_path)

def writeCellML_default(full_path, model): 
    assignAllIds_default(model)    
    printer = Printer()
    serialised_model = printer.printModel(model)
    write_file = open(full_path, "w")
    write_file.write(serialised_model)
    write_file.close()
    print('CellML model saved to:',full_path)

def writePythonCode_UI(model_path, model):
    message = f'If you want to change the default filename {model.name()}.py, please type the new name. Otherwise, just press Enter.'
    file_name = ask_for_input(message, 'Text')
    if file_name == '':
        file_name=model.name()+'.py'
    else:
        file_name=file_name+'.py'
    full_path = str(PurePath(model_path).joinpath(file_name))  
    return full_path
      
""""Write python code for the complete model"""
def writePythonCode(full_path, model,strict_mode=True):
    base_dir = PurePath(full_path).parent.as_posix()
    importer = cellml.resolve_imports(model, base_dir, strict_mode)
    flatModel = importer.flattenModel(model)
    a = cellml.analyse_model(flatModel)         
    generator = Generator()
    generator.setModel(a)
    profile = GeneratorProfile(GeneratorProfile.Profile.PYTHON)
    generator.setProfile(profile)
    implementation_code_python = generator.implementationCode()                   
    # Save the python file in the same directory as the CellML file
    with open(full_path, "w") as f:
        f.write(implementation_code_python)
    print('Python code saved to:', full_path)

""""Edit the model based on the user input"""
def editModel(model_path,model,importSource_units,import_units_model,importSources_comp=[], import_models=[],import_components_dicts=[]):
    # Assume that the new components have been added to the model
    # import the existing components from other CellML files
    for i, importSource in enumerate(importSources_comp):
        importComponents(model,importSource,import_models[i],import_components_dicts[i])
    
    # Clone variables from import components to the new components when needed
    compPair4CloneVars_UI(model)
    # Import units from other CellML files
    if importSource_units:
        if importSource_units.model() is None:
            print('Warning: the units file is not a valid CellML file.')
        importUnits(model,importSource_units,import_units_model)
    cellml.resolve_imports(model, model_path, True)
    # Encapsulate the components when needed
    component_parent_selected, component_children_selected = encapsulate_UI(model)
    encapsulate(model, component_parent_selected, component_children_selected)
    # Carry out the connection between the components
    connect_UI(model_path,model)
    # Add units to the model when needed
    addUnits_UI(model)
    # Fix the variable interfaces
    if not model.fixVariableInterfaces():
        print('Warning: some variable interfaces in the model are incorrect.')
    if model.hasUnlinkedUnits():
        print('Warning: some units in the model are unlinked, and start linking...')
        if not model.linkUnits():
            print('Warning: some units in the model are still unlinked.')
    #    Create a validator and use it to check the model so far.
    print_model(model,True)
    cellml.validate_model(model)

def editModel_default(model_path,model,importSource_units,import_units_model,importSources_comp=[], import_models=[],import_components_dicts=[],comp_pairs=[]):
    # Assume that the new components have been added to the model
    # import the existing components from other CellML files
    for i, importSource in enumerate(importSources_comp):
        importComponents(model,importSource,import_models[i],import_components_dicts[i])
    
    # Clone variables from import components to the new components when needed
    compPair4CloneVars_UI(model)
    # Import units from other CellML files
    if importSource_units:
        if importSource_units.model() is None:
            print('Warning: the units file is not a valid CellML file.')
        copyUnits(model,importSource_units,import_units_model)
    cellml.resolve_imports(model, model_path, True)
    # Encapsulate the components when needed
    component_list = getEntityList(model)
    component_children_selected=[]
    component_parent_selected=''
    for comp in component_list:
        comp_namelist = comp.split('_')
        if 'test' in comp_namelist:
            component_parent_selected = comp
        elif 'io' not in comp_namelist:
            component_children_selected.append(comp)
    if component_parent_selected != '':
        encapsulate(model, component_parent_selected, component_children_selected)
    # Carry out the connection between the components
    importer = cellml.resolve_imports(model, model_path, True)
    flatModel = importer.flattenModel(model) # this may not be necessary after the units compatibility check function is fixed
    for comp_pair in comp_pairs:
        suggestConnection(flatModel, model.component(comp_pair[0]), model.component(comp_pair[1]))
        fixInits_UI (model.component(comp_pair[0]), model.component(comp_pair[1]))
    # Add units to the model when needed
    addUnits_UI(model)
    # Fix the variable interfaces
    if not model.fixVariableInterfaces():
        print('Warning: some variable interfaces in the model are incorrect.')
    if model.hasUnlinkedUnits():
        print('Warning: some units in the model are unlinked, and start linking...')
        if not model.linkUnits():
            print('Warning: some units in the model are still unlinked.')
    #    Create a validator and use it to check the model so far.
    # print_model(model,True)
    cellml.validate_model(model)
    

"""" Assign IDs to all entities in the model; """
def assignAllIds(model):
    meassage = f'Do you want to assign all the ids to the {model.name()}?'
    answer = ask_for_input(meassage, 'Confirm', True)
    if answer:
        annotator = Annotator()
        annotator.setModel(model)
        annotator.clearAllIds()
        annotator.assignAllIds()
        duplicates = annotator.duplicateIds()
        if len(duplicates) > 0: 
            print('Warning: there are duplicate IDs.')
        """"
        if len(duplicates) > 0: # aways true
            print('There are duplicate IDs. Assigning new IDs to all entities.')
            annotator.clearAllIds()
            annotator.assignAllIds()
            # Save the updated model to a new file - the filename is the original one + '_newIDs'
            filename = str(PurePath(fullpath).stem)+'_newIDs.cellml'
            fullpath = str(PurePath(directory).joinpath(filename))
            writeCellML(fullpath, model)
        """
def assignAllIds_default(model):
    annotator = Annotator()
    annotator.setModel(model)
    annotator.clearAllIds()
    annotator.assignAllIds()
    duplicates = annotator.duplicateIds()
    if len(duplicates) > 0: 
        print('Warning: there are duplicate IDs.')   

""" Create a model from a list of components. """
def buildModel():
    message = 'Start building a model from csv file or an existing model?'
    choices = ['csv file', 'existing model']
    choice = ask_for_input(message, 'List', choices)

    if choice == 'csv file':
        file_path=read_csv_UI()
        components=read_csv(file_path)    
    else:
        full_path, existing_model=parseCellML_UI()
        components= getEntityList(existing_model)
    
    message="Please type the model name:"
    model_name = ask_for_input(message, 'Text')
    message = 'Please select the folder to save the model:'
    model_path = ask_for_file_or_folder(message,True)

    while True:
        if model_name!= '':           
            model = Model(model_name)
            message="Select the components to add to the model:"
            choices=[str(components.index(component))+ ":"+ component.name() for component in components]
            components_selected = ask_for_input(message, 'Checkbox', choices)
            indexes = [int(i.split(':')[0]) for i in components_selected]
            for index in indexes:
                model.addComponent(components[index].clone())
            importSources_comp,import_models, import_components_dicts=importComponents_UI(model_path,strict_mode=True)
            importSource_units,import_units_model = importUnits_UI(model_path,strict_mode=True)
            editModel(model_path,model, importSource_units, import_units_model, importSources_comp, import_models, import_components_dicts)

            message="Do you want to save the model?"
            answer = ask_for_input(message, 'Confirm', True)
            if answer:
                full_path=writeCellML_UI(model_path, model)
                writeCellML(full_path, model)
                full_path=writePythonCode_UI(model_path, model)
                writePythonCode(full_path, model)
            
            message="Please type the model name or press Enter to quit building models:"
            model_name = ask_for_input(message, 'Text')                               
        else:
            break
            
# main function
if __name__ == "__main__":
    buildModel()


