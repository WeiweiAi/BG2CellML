from libcellml import Analyser, Component, Generator, GeneratorProfile, Model, Units, Validator, Variable, Parser, ImportSource, Printer, Importer
import pandas as pd
import os
from utilities import print_model, ask_for_file_or_folder, ask_for_input, load_matrix
import sys
import libsbml
import cellml
MATH_HEADER = '<math xmlns="http://www.w3.org/1998/Math/MathML" xmlns:cellml="http://www.cellml.org/cellml/2.0#">'
MATH_FOOTER = '</math>'
MATH_DUMMY = """<apply>
                <eq/>
                <ci>a</ci>
                <ci>b</ci>
            </apply>"""
#----------------------------------------------------------------Build a cellML model for BG model----------------------------------------------------------#
"""Define BG component class"""
class BG():
   # Define physical domain and corresponding effort and flow variables, and their units
   dom = {'Ch':{'e':['mu','J_per_mol'],'f':['v','fmol_per_sec'],'q':['q','fmol']}, 
         'E':{'e':['V','volt'],'f':['I','fA'],'q':['q','fC']}} 
   # Define component and corresponding parameters, and their units
   comp = {'Ce':{'dom':'Ch', 'description':'Chemical species', 'para':['K','per_fmol']},
           'Se':{'dom':'Ch','description':'Chemostat', 'para':['K','per_fmol']},
           'C':{'dom':'E', 'description':'Capacitor','para':['C','fF']},
           'Ve':{'dom':'E','description':'Voltage source', 'para':['C','fF']},
           'Re':{'dom':'Ch','description':'Chemical Reaction', 'para':['kappa','fmol_per_sec']},
           'Re_GHK':{'dom':'Ch','description':'GHK Reaction', 'para':['kappa','fmol_per_sec']},
           'R':{'dom':'E','description':'Resistor', 'para':['g','fS']} }
   # Define constant value and their units
   const = {'F':[96485,'C_per_mol'], 'R':[8.31,'J_per_mol_per_K'], 'T':[293, 'kelvin']}

"""Add variables and equations based on the component type"""
def add_BGcomp(model, name, type):   
    if type not in list(BG.comp):
       sys.exit(f'BG {type} is not defined!')
    component = model.component(model.name())
    component_param = model.component(model.name()+ '_param')
    dom = BG.comp[type]['dom']
    para_name = BG.comp[type]['para'][0] + '_' + name
    para_unit = BG.comp[type]['para'][1]
    para=Variable(para_name)
    para.setUnits(para_unit)
    component.addVariable(para)
    component_param.addVariable(para)
    f_name = BG.dom[dom]['f'][0]+ '_' + name
    f_unit = BG.dom[dom]['f'][1]
    f=Variable(f_name)
    f.setUnits(f_unit)
    component.addVariable(f)
    if type in ['Ce','Se','C','Ve']:          
        q_init_name = BG.dom[dom]['q'][0]+ '_' + name + '_init'
        q_unit = BG.dom[dom]['q'][1]
        q_init=Variable(q_init_name)
        q_init.setUnits(q_unit)
        component_param.addVariable(q_init)
        component.addVariable(q_init)
        q_name = BG.dom[dom]['q'][0]+ '_' + name
        q=Variable(q_name)
        q.setUnits(q_unit)
        q.setInitialValue(q_init)
        component.addVariable(q)
        e_name = BG.dom[dom]['e'][0]+ '_' + name
        e_unit = BG.dom[dom]['e'][1]
        e=Variable(e_name)
        e.setUnits(e_unit)
        component.addVariable(e)
        if type in ['Ce','Se']:   
           eq = [f'{e.name()} = R*T*ln({para.name()}*{q.name()})']
        else: # 'C','Ve'
           eq = [f'{e.name()} = {f.name()}/{para.name()}'] 
        new_mathml = libsbml.parseL3Formula(eq)
        new_string = libsbml.writeMathMLToString(new_mathml)
        component.appendMath(new_string)
        if type in ['Ce','C']:
           eq = [f'ode({q.name()},t) = {f.name()};\n']
           new_mathml = libsbml.parseL3Formula(eq)
           new_string = libsbml.writeMathMLToString(new_mathml)
           component.appendMath(new_string)                    
    elif type == 'Re':
        ein_name = BG.dom[dom]['e'][0]+ '_' + name+ '_in'
        eout_name = BG.dom[dom]['e'][0]+ '_' + name+ '_out'
        e_unit = BG.dom[dom]['e'][1]
        ein=Variable(ein_name)
        eout=Variable(eout_name)
        ein.setUnits(e_unit)
        eout.setUnits(e_unit)
        component.addVariable(ein)
        component.addVariable(eout)
        eq = [f'{f.name()} = {para.name()}*(exp({ein.name()}/(R*T))-exp({eout.name()}/(R*T)))']
        new_mathml = libsbml.parseL3Formula(eq)
        new_string = libsbml.writeMathMLToString(new_mathml)
        component.appendMath(new_string)
    else:
        sys.exit(f'BG {type} is not defined!')

""""Add equations based on the connection matrices"""
def add_BGbond(model, comps, compd, Nf, Nr):
    # Add the zero nodes, i.e., mass balance equations
    component = model.component(model.name())
    for i,ecomp in enumerate(comps):
        name = ecomp[0]
        type = ecomp[1]
        dom = BG.comp[type]['dom']
        f_name = BG.dom[dom]['f'][0]+ '_' + name
        eq = [f'{f_name} = ']
        for j in range(len(Nf[0,:])):
            if Nf[i,j] != 0:
                name = compd[j][0]
                type = compd[j][1]
                dom = BG.comp[type]['dom']
                f_name = BG.dom[dom]['f'][0]+ '_' + name
                if Nf[i,j] == 1:
                    eq.append(f'-{f_name}')
                else:
                    eq.append(f'-{Nf[i,j]}*{f_name}')
        for j in range(len(Nr[0,:])):
            if Nr[i,j] != 0:
                name = compd[j][0]
                type = compd[j][1]
                dom = BG.comp[type]['dom']
                f_name = BG.dom[dom]['f'][0]+ '_' + name
                if Nr[i,j] == 1:
                    eq.append(f'+{f_name}')
                else:
                    eq.append(f'+{Nr[i,j]}*{f_name}')
        new_mathml = libsbml.parseL3Formula(eq)
        new_string = libsbml.writeMathMLToString(new_mathml)
        component.appendMath(new_string)
    # Add the one nodes, i.e., energy balance equations
    for j,dcomp in enumerate(compd):
        name = dcomp[0]
        type = dcomp[1]
        dom = BG.comp[type]['dom']
        ein_name = BG.dom[dom]['e'][0]+ '_' + name+ '_in'
        eout_name = BG.dom[dom]['e'][0]+ '_' + name+ '_out'
        eqout = [f'{eout_name} = ']
        eqin = [f'{ein_name} = ']
        for i in range(len(Nf[:,0])):
            if Nf[i,j] != 0:
                name = comps[i][0]
                type = comps[i][1]
                dom = BG.comp[type]['dom']
                e_name = BG.dom[dom]['e'][0]+ '_' + name
                if Nf[i,j] == 1:
                    eqin.append(f'+{e_name}')
                else:
                    eqin.append(f'+{Nf[i,j]}*{e_name}')
        for i in range(len(Nr[:,0])):
            if Nr[i,j] != 0:
                name = comps[i][0]
                type = comps[i][1]
                dom = BG.comp[type]['dom']
                e_name = BG.dom[dom]['e'][0]+ '_' + name
                if Nr[i,j] == 1:
                    eqout.append(f'+{e_name}')
                else:
                    eqout.append(f'+{Nr[i,j]}*{e_name}')
        new_mathml = libsbml.parseL3Formula(eqin)
        new_string = libsbml.writeMathMLToString(new_mathml)
        component.appendMath(new_string)
        new_mathml = libsbml.parseL3Formula(eqout)
        new_string = libsbml.writeMathMLToString(new_mathml)
        component.appendMath(new_string) 

"""Read bond graph model from a csv file and create a CellML model from it."""
def read_csvBG():
    # Get the csv file from the user by opening a file dialog
    message='Select the forward matrix csv file:'
    file_name_f = ask_for_file_or_folder(message)
    message='Select the reverse matrix csv file:'
    file_name_r = ask_for_file_or_folder(message) 
    # Read the csv file, which has two rows of headers, the first row is the reaction type and the second row is the reaction name
    CompName,CompType,ReName,ReType,N_f,N_r=load_matrix(file_name_f,file_name_r)
    message = 'Do you want to change the model name?'
    answer = ask_for_input(message, 'Confirm')
    if answer == True:
        message = 'Enter the model name:'
        model_name = ask_for_input(message, 'Text')
    else:
        # Get the default model name: BG_filename
        model_name = 'BG_'+ os.path.splitext(os.path.basename(file_name_f))[0]
    # Build the model
    model = Model(model_name)
    component=Component(model_name)
    component_param=Component(model_name+'_param')
    model.addComponent(component)
    model.addComponent(component_param)
    for i, comp in enumerate(CompName):
        add_BGcomp(model, comp, CompType[i])
    for i, re in enumerate(ReName):
        add_BGcomp(model, re, ReType[i])
    comps = list(zip(CompName,CompType))
    compd = list(zip(ReName,ReType))
    add_BGbond(model, comps, compd, N_f, N_r)
    # Set the default parameters as 1
    for var_numb in range(model.component(component_param.name()).variableCount()):
        model.component(component_param.name()).variable(var_numb).setInitialValue(1)
    # Add the constant variables
    message = 'Select the constant variables to add:'
    choices = [const for const in BG.const]
    const_selected = ask_for_input(message, 'Checkbox', choices)
    for const in const_selected:
        var_const=Variable(const)
        var_const.setUnits(BG.const[const][1])
        param_const = var_const.clone()
        param_const.setInitialValue(BG.const[const][0])
        var_const.setInitialValue(param_const)
        model.component(component.name()).addVariable(var_const)
        model.component(component_param.name()).addVariable(param_const)
    editModel(model)    
#----------------------------------------------------------------------Build a CellML model from a csv file--------------------------------------------------------------
""" Read a csv file and create components and variables from it. """
def read_csv():
    # Get the csv file from the user by opening a file dialog
    message='Select the csv file to load the model from:'
    file_path = ask_for_file_or_folder(message)
    df = pd.read_csv(file_path, sep=',', header=0, index_col=False,na_values='nan')
    df['component']=df['component'].fillna(method="ffill")
    gdf=df.groupby('component')
    components = []
    params_comp = Component('parameters')
    # Create CellMLVariable for each variable in the component and add it to the component
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
            name, units = row['variable'], row['units']
            variable = Variable(name)
            variable.setUnits(units)
            if pd.isna(row['initial_value']):
                pass
            elif row["param"]=='param':
                param = variable.clone()
                param.setInitialValue(row['initial_value'])
                params_comp.addVariable(param)                                             
            elif row['param'] == 'init':
                param = Variable(name+'_init')
                variable.setInitialValue(param)
                param.setUnits(units)
                param.setInitialValue(row['initial_value'])
                params_comp.addVariable(param)
            else:
                variable.setInitialValue(row['initial_value'])
            component.addVariable(variable)           
        components += [component]
    if params_comp.variableCount()>0:        
        components += [params_comp]    
    return components

""" Specify imports and units. """
def importCellML(model,start):    
    while True:
        message = 'Do you want to import components or units from a CellML file?'
        answer = ask_for_input(message, 'Confirm')
        if answer:
            message='Select the CellML file to import from:'
            filename = ask_for_file_or_folder(message)
            relative_path = os.path.relpath(filename, start) 
            # Parse the CellML file
            existing_model=cellml.parse_model(filename, False)
            importSource = ImportSource()
            importSource.setUrl(relative_path)
            message="Select the component or unit to import:"
            choices=['units', 'components','equations']
            import_type = ask_for_input(message, 'Checkbox', choices)[0]
            if import_type == 'units':
                units_undefined=checkUndefinedUnits(model)
                if len(units_undefined)>0:
                    # Get the intersection of the units_undefined and the units defined in the existing model
                    existing_units=set([existing_model.units(unit_numb).name() for unit_numb in range(existing_model.unitsCount())])
                    units_to_import = units_undefined.intersection(existing_units)
                else:
                    units_to_import = set()
                for unit in units_to_import:
                    u = Units(unit)
                    u.setImportSource(importSource)
                    u.setImportReference(unit)
                    model.addUnits(u)
            elif import_type == 'components':
                message="Select the components to import:"
                choices=[existing_model.component(comp_numb).name() for comp_numb in range(existing_model.componentCount())]
                answers = ask_for_input( message, 'Checkbox', choices)
                for component in answers:
                    message="Do you want to rename the component?"
                    answer = ask_for_input(message, 'Confirm')
                    if answer:
                        message="Enter the new name for the component:"
                        answer = ask_for_input(message, 'Text')
                        c = Component(answer)
                    else:
                        c = Component(component)
                    c.setImportSource(importSource)
                    c.setImportReference(component)
                    dummy_c = c.importSource().model().component(c.importReference()).clone()
                    while(dummy_c.variableCount()):
                         c.addVariable(dummy_c.variable(0))
                    model.addComponent(c)
            else: # if the user does not select any component or unit, then import equations; assume the component name is the same as the new model
                for i in range(existing_model.componentCount()):
                    model.component(existing_model.component(i).name()).setMath(MATH_HEADER)
                    model.component(existing_model.component(i).name()).appendMath(existing_model.component(i).math())
                    model.component(existing_model.component(i).name()).appendMath(MATH_FOOTER)           
        else:
            break

""" Carry out the encapsulation. """
def encapsulate(model):
    while True:
        message = 'Do you want to encapsulate components?'
        answer = ask_for_input(message, 'Confirm')
        if answer:
            message="Select the parent component for encapsulation:"
            choices=[model.component(comp_numb).name() for comp_numb in range(model.componentCount())]
            component_parent_selected = ask_for_input(message, 'Checkbox', choices)[0] 
            message="Select the children components for encapsulation:"
            choices=[model.component(comp_numb).name() for comp_numb in range(model.componentCount()) if model.component(comp_numb).name() != component_parent_selected]
            answers = ask_for_input(message, 'Checkbox', choices)
            for component_child in answers:
                model.component(component_parent_selected).addComponent(model.component(component_child))
        else:
            break

"""" Provide variable connection suggestion based on variable name and carry on the variable mapping based on user inputs. """
def suggestConnection(comp1,comp2):
    # Get the variables in the two components
    variables1 = [comp1.variable(var_numb).name() for var_numb in range(comp1.variableCount())]
    variables2 = [comp2.variable(var_numb).name() for var_numb in range(comp2.variableCount())]
    print('The variables in the first component are:', variables1)
    print('The variables in the second component are:', variables2)
    # Get the intersection of the two variables
    variables = set(variables1).intersection(variables2)
    message="Select the variables to map:"
    choices=[var for var in variables]
    answers = ask_for_input(question, message, 'Checkbox', choices)
    for var in answers:
        Variable.addEquivalence(comp1.variable(var), comp2.variable(var))
    # Get the variables in the two components that are not mapped
    variables1 = [comp1.variable(var_numb).name() for var_numb in range(comp1.variableCount()) if comp1.variable(var_numb).name() not in answers]
    variables2 = [comp2.variable(var_numb).name() for var_numb in range(comp2.variableCount()) if comp2.variable(var_numb).name() not in answers]
    message="Select the unmapped variables in the first component to clone and map:"
    choices=[var for var in variables1]
    answers = ask_for_input(question, message, 'Checkbox', choices)
    for var in answers:
        comp2.addVariable(comp1.variable(var).clone())
        Variable.addEquivalence(comp1.variable(var), comp2.variable(var))     
    message="Select the unmapped variables in the second component to clone and map:"
    choices=[var for var in variables2]
    answers = ask_for_input(question, message, 'Checkbox', choices)
    for var in answers:
        comp1.addVariable(comp2.variable(var).clone())
        Variable.addEquivalence(comp1.variable(var), comp2.variable(var))
    # Get the difference of the two variables
    variables1 = [comp1.variable(var_numb).name() for var_numb in range(comp1.variableCount())]
    variables2 = [comp2.variable(var_numb).name() for var_numb in range(comp2.variableCount())]
    variables1_diff = set(variables1).difference(variables2)
    variables2_diff = set(variables2).difference(variables1)
    # Ask the user to map the variables in the two components that are not mapped
    while True:
        question = 'map'
        message="Select the unmapped variable pair or Enter to skip:"
        choices=[var for var in variables1_diff] + [var for var in variables2_diff]
        answers = ask_for_input(question, message, 'Checkbox', choices)
        if len(answers)>0:
            var1 = answers[0]
            var2 = answers[1]
            Variable.addEquivalence(comp1.variable(var1), comp2.variable(var2))
        else:
            break   

""" Carry out the connection. """
def connect(model):
    # List the components in the model
    components = [model.component(comp_numb).name() for comp_numb in range(model.componentCount())]
    # Find the components that have encapsulated components, and connect the parent and child components
    def suggestConnection_parent_child(parent_component):
        if parent_component.componentCount()>0:
            for child_numb in range(parent_component.componentCount):                
                child_component = parent_component.component(child_numb)
                suggestConnection(parent_component, child_component)
                suggestConnection_parent_child(child_component)

    for comp_numb in range(model.componentCount()):
        parent_component = model.component(comp_numb)
        suggestConnection_parent_child(parent_component)
        
    while True:
        message = 'Select two components to connect or Enter to skip:'
        answer = ask_for_input(message, 'Checkbox', components)       
        if len(answer)>0:
            comp1= answer[0]
            comp2= answer[1]
            suggestConnection(model.component(comp1), model.component(comp2))
        else:
            break
"""Check the undefined non base units"""
def _checkUndefinedUnits(model):
    units_claimed = set()
    for comp_numb in range(model.componentCount()):
        for var_numb in range(model.component(comp_numb).variableCount()):
            if model.component(comp_numb).variable(var_numb).units().name() != '':
                print(model.component(comp_numb).variable(var_numb).name() + ': ' + model.component(comp_numb).variable(var_numb).units().name())
                #if not model.component(comp_numb).variable(var_numb).units() in Units.StandardUnit:
                units_claimed.add(model.component(comp_numb).variable(var_numb).units().name())
    print('The units claimed in the variables are:', units_claimed)
    units_defined = set()
    for unit_numb in range(model.unitsCount()):
        print(model.units(unit_numb).name())
        units_defined.add(model.units(unit_numb).name()) 
    print('The units defined in the model are:', units_defined)   
    units_undefined = units_claimed - units_defined
    print('The units claimed in the variables but not defined in the model are:',units_undefined)
    return units_undefined

# Define the units
def _defineUnits(model,iunits):
    while True:
        message = 'Type the name of the standardUnit or Enter to skip:'
        unitName = ask_for_input(message, 'Text')
        if unitName != '':
            iunits.addUnit(unitName)
            message = 'Type the prefix or Enter to skip:'
            prefix = ask_for_input(message, 'Text')
            message = 'Type the exponent or Enter to skip:'
            exponent = ask_for_input(message, 'Text')
            message = 'Type the multiplier or Enter to skip:'
            multiplier = ask_for_input(message, 'Text')
            if exponent != '':
                exponent = float(exponent)
            else:
                exponent = 1.0
            if multiplier != '':
                multiplier = float(multiplier)
            else:
                multiplier = 1.0   
            if prefix == '':
                prefix = 1   
            iunits.addUnit(unitName, prefix, exponent, multiplier)
        else:
            break              
        model.addUnits(iunits)

# Add units to the model
def addUnitsUI(model):
    units_undefined=_checkUndefinedUnits(model)
    # Ask the user to add the units which are claimed in the variables but not defined in the model
    for units in units_undefined:
        while True:
            message = 'Do you want to add units:' + units + '?'
            answer = ask_for_input(message, 'Confirm', True)           
            if answer:
                iunits = Units(units)
                _defineUnits(model,iunits)                              
            else:
                break
    # Ask the user to add custom units
    while True:
        message = 'Do you want to add custom units? Type the name of the units or Enter to skip:'
        answers = ask_for_input(message, 'Text')
        if answers!= '':
            iunits = Units(answers)
            _defineUnits(model,iunits)    
        else:
            break              

# Write a model to hold the equations of the components, input: component names, output: equations model file
def writeEquations(components):
    model = Model('equations')
    for component in components:
        message = 'Select the folder to save the equation model:'
        file_path = ask_for_file_or_folder(message,True)
        for component in components:
            # Create a component
            icomp = Component(component.name())
            icomp.setMath(MATH_HEADER)
            icomp.appendMath(MATH_DUMMY)
            icomp.appendMath(MATH_FOOTER)
            model.addComponent(icomp)
    writeCellML(file_path, model)

# Write a model to cellml file, input: directory, model, output: cellml file
def writeCellML(directory, model):
    message = 'Type the filename or Enter to skip, the default name is model name:'
    file_name = ask_for_input(message, 'Text')
    if file_name == '':
        file_name=model.name()+'.cellml'
    else:
        file_name=file_name+'.cellml'        
    printer = Printer()
    serialised_model = printer.printModel(model)
    write_file = open(directory +file_name, "w")
    write_file.write(serialised_model)
    write_file.close()
    print('Model saved to:', directory + file_name)

""""Write python code for the complete model"""
def writePythonCode(base_dir, model,strict_mode=True):
    message = 'Do you want to generate the python code?'
    answer = ask_for_input(message, 'Confirm', False)           
    if answer:
        importer = cellml.resolve_imports(model, base_dir, strict_mode)
        flatModel = importer.flattenModel(model)
        analyser = cellml.analyse_model(flatModel)                   
        generator = Generator()
        generator.setModel(analyser.model())
        profile = GeneratorProfile(GeneratorProfile.Profile.PYTHON)
        generator.setProfile(profile)
        implementation_code_python = generator.implementationCode() 
        message = 'Type the filename or Enter to skip, the default name is model name:'
        file_name = ask_for_input(message, 'Text')
        if file_name == '':
            file_name=model.name()+'.py'
        else:
            file_name=file_name+'.py'                   
        # Save the python file in the same directory as the CellML file
        with open(base_dir+file_name, "w") as f:
            f.write(implementation_code_python)
        print('Python code saved to:', base_dir + file_name)
""""Edit the model based on the user input"""
def editModel(model):
    message = 'Select the folder to save the model:'
    directory = ask_for_file_or_folder(message,True)
    importCellML(model,directory)
    addUnitsUI(model)
    encapsulate(model)
    connect(model)
    model.fixVariableInterfaces()
    #    Create a validator and use it to check the model so far.
    cellml.get_model_component_hierarchy(model)
    print_model(model)
    cellml.validate_model(model)
    cellml.analyse_model(model)
    message="Do you want to save the model?"
    answer = ask_for_input(message, 'Confirm', True)
    if answer:
        writeCellML(directory, model)
        writePythonCode(directory, model)

""" Create a model from a list of components. """
def createModel():
    # Get the components from the user csv file first
    components = read_csv()
    message="Do you want to write equations model file with only component names and a dummy equation?"
    answers = ask_for_input(message, 'Confirm')
    if answers:
        components_name = [component.name() for component in components]
        writeEquations(components_name)
    while True:
        message="Type the model name or Enter to skip:"
        model_name = ask_for_input(message, 'Text')
        if model_name!= '':           
            model = Model(model_name)
            message="Select the components to add to the model:"
            choices=[str(components.index(component))+ ":"+ component.name() for component in components]
            components_selected = ask_for_input(message, 'Checkbox', choices)
            indexes = [int(i.split(':')[0]) for i in components_selected]
            for index in indexes:
                model.addComponent(components[index].clone())
            editModel(model)                               
        else:
            break
            
# main function
if __name__ == "__main__":
    createModel()


