import pandas as pd
from ordered_set import OrderedSet
from anytree import Node, RenderTree, Resolver
import os
import xml.etree.ElementTree as ET
from CellMLModel import Model, Variable, Units, Component, Math, Connection, Map_variables, Encapsulation,Import_component, Import, Component_ref, Unit,addImport_Units
import sys
import inquirer
from pprint import pprint
from  copy import deepcopy
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askdirectory
# Parse the CellML file v1.1 and return the CellML model as a dictionary
def parseCellMLFile(cellmlFile):
    # Read the CellML file
    tree = ET.parse(cellmlFile)
    root = tree.getroot()
    # Check if the CellML file is v1.1
    if root.tag != '{http://www.cellml.org/cellml/1.1#}model':
        sys.exit('The CellML file is not v1.1')
    # Get the model name
    modelName = root.attrib['name']
    # Get the model units
    modelUnits = []
    modelComponents = []
    modelEquations = []
    for child in root:
        if child.tag == '{http://www.cellml.org/cellml/1.1#}units':
            # Create Units object
            units = Units(child.attrib['name'])
            # Get the units attributes
            unit_list = []
            for grandchild in child:
                if grandchild.tag == '{http://www.cellml.org/cellml/1.1#}unit':
                    unit = Unit(grandchild.attrib['units'])
                    if 'prefix' in grandchild.attrib:
                        unit.prefix = grandchild.attrib['prefix']
                    if 'exponent' in grandchild.attrib:
                        unit.exponent = grandchild.attrib['exponent']
                    if 'multiplier' in grandchild.attrib:
                        unit.multiplier = grandchild.attrib['multiplier']
                    if 'offset' in grandchild.attrib:
                        unit.offset = grandchild.attrib['offset']
                    unit_list.append(unit)
            units.children = unit_list        
            modelUnits.append(units)
    # Get the model components and corresponding variables  
        if child.tag == '{http://www.cellml.org/cellml/1.1#}component':
            component = Component(child.attrib['name'])
            variable_list=[]
            for grandchild in child:
                if grandchild.tag == '{http://www.cellml.org/cellml/1.1#}variable':
                    # Create Variable object
                    variable = Variable(grandchild.attrib['name'], grandchild.attrib['units'], parent=component,children=None)
                    # Get the variable attributes
                    if 'initial_value' in grandchild.attrib:
                        variable.initial_value = grandchild.attrib['initial_value']
                    if 'public_interface' in grandchild.attrib:
                        variable.public_interface = grandchild.attrib['public_interface']
                    if 'private_interface' in grandchild.attrib:
                        variable.private_interface = grandchild.attrib['private_interface']
                    # Add the variable to the component
                    variable_list.append(variable)
                if grandchild.tag == '{http://www.w3.org/1998/Math/MathML}math':
                    # Get the equations by parsing the MathML <apply> tags
                    for grandgrandchild in grandchild:
                        if grandgrandchild.tag == '{http://www.w3.org/1998/Math/MathML}apply':
                            #get the id of the equation
                            if 'id' in grandgrandchild.attrib:
                                id = grandgrandchild.attrib['id']
                            else:
                                id = 'eq'
                            #get the equation and add it to the equation dictionary with the id as key
                            #equation = ET.tostring(grandgrandchild, encoding='unicode', method='xml')
                            modelEquations.append(Math(id, grandgrandchild, parent=component))
            component.children=variable_list
            modelComponents.append(component) 
    
    # Return the CellML model as a dictionary
    return {'name': modelName, 'units': modelUnits, 'components': modelComponents, 'equations': modelEquations}

def createCellMLComponent():
    # Get the csv file from the user by opening a file dialog
    print('Select the csv file to load the model from:')
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    # close the file dialog
    root.update()
    root.destroy()   # destroy main window
    # Read the csv file
    df = pd.read_csv(file_path, sep=',', header=0, index_col=False,na_values='nan')
    df['component']=df['component'].fillna(method="ffill")
    gdf=df.groupby('component')
    # Get the component name and create a list of components
    components = OrderedSet()
    params = OrderedSet()
    for component_name, groupi in gdf:
        # Create CellMLVariable for each variable in the component and add it to the component
        variables = OrderedSet()
        equations = OrderedSet()
        for index, row in groupi.iterrows():
            name, units = row['variable'], row['units']
            param_name = None
            if row['param'] == 'eq':
                equations.add(Math(name,''))
            else:
                if row[ 'public_interface'] == 'var':
                    public_interface = None
                else:
                    public_interface = row['public_interface']
    
                if pd.isna(row['initial_value']):
                    initial_value = None
                elif row["param"]==name:
                    initial_value = None
                    param_name = name                
                elif row['param'] == 'init':
                    initial_value = name+'_init'
                    param_name= name+'_init'
                else:
                    initial_value = row['initial_value']
                    variables.add(Variable(name,units,initial_value=initial_value,public_interface=public_interface,children=None))
                    if param_name is not None:
                        params.add(Variable(param_name,units,initial_value=row['initial_value'],public_interface='out',children=None))

        component = Component(component_name,children=variables.union(equations))
        components.add(component)
    if len(params)>0:        
        component = Component('parameters',children=params)
        components.add(component)
    
    return components

def importCellMLComponent():
    # Ask the user if importing components from a CellML file
    # Get the current working directory
    start = os.getcwd()
    Imports=[]
    while True:
        questions = [
            inquirer.Confirm(
                'import',
                message="Do you want to import components from a CellML file?",
                default=False,
            ),
        ]
        answers = inquirer.prompt(questions)
        # Check if the user wants to import components from a CellML file
        if answers['import']:
            Import_components=[]
            # Get the CellML file from the user
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename()
            relative_path = os.path.relpath(file_path, start)
            # close the file dialog
            root.update()
            root.destroy()   # destroy main window
            # Parse the CellML file
            existModel=parseCellMLFile(file_path)
            # Get the components from the CellML file
            existComponents = existModel['components']
            modelName = existModel['name']            
            print(f'The model {modelName} contains components:')
            for i,component in enumerate(existComponents):
                print(str(i)+':'+ str(component))
            # Ask the user to select components to import
            questions = [
                inquirer.Checkbox(
                    'components',
                    message="Select the components to import",
                    choices=[str(existComponents.index(component))+':'+component.name for component in existComponents],
                ),
            ]
            answers = inquirer.prompt(questions)
            # get the indexes of the selected components
            indexes = [int(i.split(':')[0]) for i in answers['components']]
            # Get the components based on the user selection
            components = [existComponents[index] for index in indexes]
            component_names = [component.name for component in components]
            # Ask the user if they want to rename the component for the imported components, if yes, ask the user to type the new name
            for i,component in enumerate(components):
                questions = [
                    inquirer.Confirm(
                        'rename',
                        message=f"Do you want to rename the component {component.name}?",
                        default=False,
                    ),
                ]
                answers = inquirer.prompt(questions)
                if answers['rename']:
                    questions = [
                        inquirer.Text(
                            'name',
                            message="Type the new name for the component",
                        ),
                    ]
                    answers = inquirer.prompt(questions)
                    component_names[i] = answers['name']
            
            # Create imports for the components
            for i,component in enumerate(components):
                Import_components+=[Import_component(component_names[i],component.name,component)]
            
            Imports.append(Import(relative_path,children=Import_components))    
        else:
            break
    if len(Imports)==0:
        return None
    return Imports

def importCellMLunits(model):
    # Get the current working directory
    start = os.getcwd()
    # Ask the user if importing units from a CellML file; assume that the units are in the same file
    units=model.units_namespace
    # Ask the user if they want to import the units from a CellML file, if yes, ask the user to select the unit file to import
    while True:
        questions = [
            inquirer.Confirm(
                'import',
                message="Do you want to import units from a CellML file?",
                default=False,
            ),
        ]
        answers = inquirer.prompt(questions)
        # Check if the user wants to import the units and components from a CellML file
        if answers['import']:
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename()
            units_href = os.path.relpath(file_path, start)
            # close the file dialog
            root.update()
            root.destroy()   # destroy main window
            model.children.append(addImport_Units(model,units_href,units))
        else:
            break
        

def encapCellMLcomponent(model):
    # Ask the user if they want to encapsulate the components (# TODO: need to be improved)
    while True:
        questions = [
            inquirer.Confirm(
                'encapsulate',
                message="Do you want to encapsulate the components?",
                default=False,
            ),
        ]
        answers = inquirer.prompt(questions)
        # Check if the user wants to encapsulate the components
        top_level_component_refs = []
        if answers['encapsulate']:
            # Ask the user to name the top level components for the encapsulation
            questions = [
                    inquirer.Checkbox(
                        'top_level',
                        message=f"Select top level components for the encapsulation",
                        choices=model.component_namespace,
                    ),
                ]
            answers = inquirer.prompt(questions)
            # Get the top level components
            top_level_components = answers['top_level']
            # Ask if the user wants to encapsulate the components for each top level component
            for top_level_component in top_level_components:
                # Ask the user to select the components to encapsulate
                questions = [
                    inquirer.Checkbox(
                        'components',
                        message=f"Select the components to encapsulate for {top_level_component}",
                        choices=model.component_namespace,
                    ),
                ]
                answers = inquirer.prompt(questions)
                if answers['components']:
                    # Get the components to encapsulate
                    children_comp = answers['components']
                    # Create the top level component ref
                    children_refs = [Component_ref(child,children=None) for child in children_comp]
                    top_level_component_ref = Component_ref(top_level_component,children=children_refs)
                    top_level_component_refs+=[top_level_component_ref]         
                else:
                    top_level_component_ref = Component_ref(top_level_component,children=None)
                    top_level_component_refs+=[top_level_component_ref]
        else:
            break
    if len(top_level_component_refs)>0:
       encap = Encapsulation(parent=model,children=top_level_component_refs)
    else:
        encap = None
    return encap

def connectCellMLcomponent(model):
     # Print all the components in the model 
    # Get the imported components
    imported_components = [item.component_def for item in model.Import_components]
    imported_components_name = [item.name for item in model.Import_components]
    
    print(f'The model {model.name} contains components:')
    for i,component in enumerate(model.component_namespace):
        print(str(i)+':'+ str(component))
    # Ask the user to type the component pairs to connect
    while True:
        questions = [
            inquirer.Text(
                'connection pairs',
                message="Type the component pairs to connect: comp1_index,comp1_index",
            ),
        ]
        answers = inquirer.prompt(questions)
        # Check if the user wants to connect the components
        if answers['connection pairs']:
            # Get the component pairs
            pairs = answers['connection pairs'].split(',')
            component1_name = model.component_namespace[int(pairs[0])]
            component2_name = model.component_namespace[int(pairs[1])] 
            # Check if the components are imported
            if component1_name in imported_components_name:
                component1 = imported_components[imported_components_name.index(component1_name)]
            else:
                component1 = model.components[int(pairs[0])]
            if component2_name in imported_components_name:
                component2 = imported_components[imported_components_name.index(component2_name)]
            else:
                component2 = model.components[int(pairs[1])]
            # Create the connection pair
            Connection_pair=Connection(component1,component2)           
            variable_map = Map_variables_suggestion(component1,component2)
            vars_map=[]
            for vars in variable_map:
                vars_map += [Map_variables(vars[0],vars[1],parent=Connection_pair)]   
            Connection_pair.children=vars_map    
            model.children.append(Connection_pair)
        else:
            break

def Map_variables_suggestion(comp1,comp2):
    # comp1 is not equal to comp2
    if comp1 == comp2:
        print('The two components are the same')
        return None
    # Map the variables in the two components
    variable_list1 = comp1.variables
    variable_list2 = comp2.variables
    # Print the variables in the two components side by side
    print(f'Variables in {comp1.name}:')
    for i,variable in enumerate(variable_list1):
        print(str(i)+':'+variable.cellMLText())
    print(f'Variables in {comp2.name}:')
    for i,variable in enumerate(variable_list2):
        print(str(i)+':'+variable.cellMLText())
    # Create a list of variables to map
    variable_map = []
    # Ask if the type is "encapsulation"
    questions = [
        inquirer.List(
            'type',
            message="Select the type of mapping",
            choices=['encapsulation','connection'],
        ),
    ]
    answers = inquirer.prompt(questions)
    type = answers['type']

    if type =='encapsulation':
        # Get all the variables in the second component that could be parameters but not the ones that are already in the first component
        possible_parameters = [variable for variable in variable_list2 if variable.public_interface == 'in' and variable.initial_value is None and variable.name not in [variable.name for variable in variable_list1]]
        # Ask the user to select the parameters
        if possible_parameters == []:
            print('No parameters found')
            parameters = []
        else:
            questions = [
                inquirer.Checkbox(
                    'parameters',
                    message="Select the parameters",
                    choices=[variable.name for variable in possible_parameters],
                ),
            ]
            answers = inquirer.prompt(questions)            
            print(answers['parameters'])
            parameters=[variable for variable in possible_parameters if variable.name in answers['parameters']]
        # Add the parameters to the first component with private interface "out" and to the variable map
        for parameter in parameters:
            # Get the variable from the list of possible parameters and make a copy of it
            variable = deepcopy(parameter)
            variable.public_interface = 'in'
            variable.private_interface = 'out'
            comp1.children.append(variable)
            variable_map.append([variable, parameter])

        # Get all the variables intersection between the two components based on the name and the public interface should not be None
        for variable1 in variable_list1:
            for variable2 in variable_list2:
                if variable1.name == variable2.name and variable1.public_interface is not None and variable2.public_interface is not None:
                    variable_map.append([variable1, variable2])
    else:
        for variable1 in variable_list1:
            for variable2 in variable_list2:
                if variable1.name == variable2.name and ((variable1.public_interface =='in' and variable2.public_interface =='out') or (variable1.public_interface =='out' and variable2.public_interface =='in')):
                    variable_map.append([variable1, variable2])
 
    questions = [
    inquirer.Checkbox(
        "variable_map",
        message="Select the variables to map:",
        choices=[str(variable_map.index([variable1, variable2]))+":"+variable1.cellMLText()+' <-> '+variable2.cellMLText() for variable1, variable2 in variable_map],
    ),
    ]

    answers = inquirer.prompt(questions)
    variable_map_index = []
    # get the variable map based on the user selection
    for i in answers['variable_map']:
        ianswer = i.split(':')[0]
        variable_map_index.append(int(ianswer))

    variable_map = [variable_map[i] for i in variable_map_index]    
    # Update the private interface of the variables in the first component based on the user selection
    if type =='encapsulation':
        for variable1, variable2 in variable_map:
            if variable2.public_interface == 'in':
                variable1.private_interface = 'out'
            elif variable2.public_interface == 'out':
                variable1.private_interface = 'in'
    # Display the variables in the first component after the update excluding the unmapped variables
    variable_in_comp1= [variable1 for variable1, variable2 in variable_map]
    variable_in_comp2= [variable2 for variable1, variable2 in variable_map]
    print(f'Unmapped variables in the component {comp1.name}:')
    for i,variable in enumerate(comp1.variables):
        if variable not in variable_in_comp1:
            print(str(i)+':'+variable.cellMLText())
    # Display the variables in the second component excluding the unmapped variables
    print(f'Unmapped variables in the component {comp2.name}:')
    for i,variable in enumerate(comp2.variables):
        if variable not in variable_in_comp2:
            print(str(i)+':'+variable.cellMLText())
    # Ask the user to type the variables to map manually: component1_variable,component2_variable
    while True:
        questions = [
            inquirer.Text(
                'variable_map',
                message="Type the variables to map: component1_variable index,component2_variable index",
            ),
        ]
        answers = inquirer.prompt(questions)
        # Add the variables to the variable map
        if answers['variable_map'] != '':
                variables = answers['variable_map'].split(',')
                variable1 = comp1.variables[int(variables[0])]
                variable2 = comp2.variables[int(variables[1])]
                variable_map.append([variable1, variable2])
        else:
            break
    # Print the variable map
    variable_map_name = []
    print('Variable map:')
    for variable1, variable2 in variable_map:
        print(variable1.cellMLText()+' <-> '+variable2.cellMLText())
        variable_map_name.append([variable1.name, variable2.name])
    # Return the variable map
    return variable_map_name
# Update the equations for new components
def getEquations(new_components):
    # Check if the new components have math
    if all (len(component.equations) == 0 for component in new_components):
        print('New components have no math')
        return
    else:
        print('Open the file with the equations')
    
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    root.update()
    root.destroy()
    # Read the file and get the equations
    existing_model=parseCellMLFile(file_path)
    existing_equations = existing_model['equations']
    equation_ids = [equation.id for equation in existing_equations]
    # Get the equations for the new components based on the id
    for component in new_components:
        for child in component.children:
            if isinstance(child, Math):
                # get the index of the equation in the list of equations
                index = equation_ids.index(child.id)
                # if the index is not found, raise an error
                if index == -1:
                    raise Exception('Equation not found')
                else:
                    # get the equation
                    equation = existing_equations[index]
                    # update the equation
                    child.math = equation.math
                    child.parent = component
                 
# Create a CellML model from a csv file
def createCellMLModel():
    new_components = createCellMLComponent()
    # Print the component list
    print('Component list:')
    for i,component in enumerate(new_components):
        print(str(i)+':'+ str(component))
    # Keep building the model until the user is done
    while True:
        # Ask the user to type the model name
        questions = [
            inquirer.Text(
                'name',
                message="Type the name for the model",
            ),
        ]
        answers = inquirer.prompt(questions)
        # Create the model
        if answers['name'] != '':
            model = Model(answers['name'])
            # Ask the user to select the new components for the model
            questions = [
                inquirer.Checkbox(
                    'components',
                    message="Select the components",
                    choices=[component.name for component in new_components],
                ),
            ]
            answers = inquirer.prompt(questions)
            # Get the selected components
            new_components = [component for component in new_components if component.name in answers['components']]
            getEquations(new_components)
            imports=importCellMLComponent()
            if imports is not None:     
               model.children =new_components+imports
            else:
                model.children =new_components
            encap = encapCellMLcomponent(model)
            if encap is not None:
               model.children.append(encap)
            importCellMLunits(model) 
            connectCellMLcomponent(model)
            # Print the model
            for pre, fill, node in RenderTree(model):
                print("%s%s" % (pre, node))
            # Save the model by writing the CellML text to a file using the save file dialog
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.asksaveasfilename()
            model.cellML(file_path)
        else:
            break
    
# _main_ function to test the code createCellMLModel
if __name__ == '__main__':
    createCellMLModel()
    
