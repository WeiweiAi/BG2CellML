from libcellml import Component, Generator, GeneratorProfile, Model, Units,  Variable, ImportSource, Printer, Annotator
import pandas as pd
from utilities import print_model, ask_for_file_or_folder, ask_for_input, infix_to_mathml,parse_model,resolve_imports,analyse_model
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
    # if the component name is not provided, the list of the component names is returned (excluding the encapsulated children components);
    # if the component name is provided, the list of the variable names is returned
    if comp_name is None:
        return [model.component(comp_numb).name() for comp_numb in range(model.componentCount())]
    else:
        return [model.component(comp_name).variable(var_numb).name() for var_numb in range(model.component(comp_name).variableCount())]  
#----------------------------------------------------------------------Build a CellML model from a csv file--------------------------------------------------------------
""" Read a csv file and create components and variables from it. """
def read_csv(file_path):    
    # input: the path of the csv file (including the file name and extension)
    # output: None, write the components and variables to a CellML model, saved as a .cellml file; 
    #         the name of the model is the same as the csv file name
    #         the model is saved in the same folder as the csv file

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

""""To set up for importing a CellML model."""
def import_setup(model_path,full_path_imported_model, strict_mode=True):
    # input: model_path: the directory of the CellML model that imports other CellML models
    #        full_path_imported_model: the path of the CellML model that is imported (including the file name and extension)
    #        strict_mode: whether to use strict mode when parsing the CellML model
    # output: import_model: the existing model that is imported
    #         importSource: the ImportSource object which contains the url of the imported model
    import_model,issues,issue_details=parse_model(full_path_imported_model, strict_mode)
    if not import_model:
        return False, issues
    else:
        relative_path_os = os.path.relpath(full_path_imported_model, model_path)
        relative_path=PurePath(relative_path_os).as_posix()
        importSource = ImportSource()
        importSource.setUrl(relative_path)
        importSource.setModel(import_model)
        return importSource, import_model


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

""" Import units or components from an existing CellML model. """
def importUnits(model,importSource):
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
            return
        else:
            units_model=importSource.model()
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

""" Carry out the encapsulation. """
def encapsulate(model, component_parent, component_children):
    # input: model: the model object that includes the components to be encapsulated
    #        component_parent_selected: the name of the parent component
    #        component_children_selected: a list of the names of the children components
    # output: None
    #        The encapsulation will be added to the model
    for component_child in component_children:
        model.component(component_parent).addComponent(model.component(component_child))

""" Get the equivalent variables of a variable. """
def equivalent_variables(variable, variable_set):
    if variable is None:
        return
    for i in range(0, variable.equivalentVariableCount()):
        equivalent_variable = variable.equivalentVariable(i)
        if equivalent_variable not in variable_set:
            variable_set.add(equivalent_variable)
            equivalent_variables(equivalent_variable, variable_set)
     
def addInit(model,comp_name,var_name,init):
    # input: model: the model object
    #        comp_name: the name of the component
    #        var_name: the name of the variable
    #        init: the initial value to be set
    # output: None
    #        The initial value will be set to the variable
    model.component(comp_name).variable(var_name).setInitialValue(init)

def update_varmap(model, varmaps,connection=True):
    # input: model, the CellML model object
    #        varmaps, a list of variable mappings [(comp1,var1,comp2,var2),(comp3,var3,comp4,var4)]
    for varmap in varmaps:
        comp1 = varmap[0]
        var1 = varmap[1]
        comp2 = varmap[2]
        var2 = varmap[3]
        if connection:
           Variable.addEquivalence(model.component(comp1).variable(var1), model.component(comp2).variable(var2))
           print(f'{var1} in {comp1} is mapped to {var2} in {comp2}.')
        else:
           Variable.removeEquivalence(model.component(comp1).variable(var1), model.component(comp2).variable(var2))
           print(f'{var1} in {comp1} is unmapped to {var2} in {comp2}.')

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

# Add equations to the model
def addEquations(component, equations):

    component.setMath(MATH_HEADER)            
    for equation in equations:
        infix = equation[0]
        ode_var = equation[1]
        voi = equation[2]
        component. appendMath(infix_to_mathml(infix, ode_var, voi))
    component. appendMath(MATH_FOOTER)

# Write a model to cellml file, input: directory, model, output: cellml file
def writeCellML(full_path, model):    
    printer = Printer()
    serialised_model = printer.printModel(model)    
    write_file = open(full_path, "w")
    write_file.write(serialised_model)
    write_file.close()
    print('CellML model saved to:',full_path)
    
""""Write python code for the complete model"""
def writePythonCode(full_path, model,strict_mode=True):
    base_dir = PurePath(full_path).parent.as_posix()
    importer, issues,issue_details = resolve_imports(model, base_dir, strict_mode)
    print("'resolve_imports' finished.", issues,issue_details)
    if importer:
        flatModel = importer.flattenModel(model)
        analyser, issues,issue_details = analyse_model(flatModel)
        print("'analyse_model' finished.", issues,issue_details)
        if analyser:
            generator = Generator()
            generator.setModel(analyser.model())
            profile = GeneratorProfile(GeneratorProfile.Profile.PYTHON)
            generator.setProfile(profile)
            implementation_code_python = generator.implementationCode()                   
            # Save the python file in the same directory as the CellML file
            with open(full_path, "w") as f:
                f.write(implementation_code_python)
            return True, issues,issue_details 
        else:
            return False, issues,issue_details
    else:
        return False, issues,issue_details
 


