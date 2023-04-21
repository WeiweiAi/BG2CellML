from libcellml import Analyser, Component, Generator, GeneratorProfile, Model, Units, Validator, Variable, Parser, ImportSource, Printer, Importer, Annotator
import pandas as pd
from utilities import print_model, ask_for_file_or_folder, ask_for_input, load_matrix, infix_to_mathml
import sys
import cellml
from pathlib import PurePath 
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, FOAF,  DCTERMS, XSD
MATH_HEADER = '<math xmlns="http://www.w3.org/1998/Math/MathML" xmlns:cellml="http://www.cellml.org/cellml/2.0#">\n'
MATH_FOOTER = '</math>\n'
BUILTIN_UNITS = {'ampere':Units.StandardUnit.AMPERE, 'becquerel':Units.StandardUnit.BECQUEREL, 'candela':Units.StandardUnit.CANDELA, 'coulomb':Units.StandardUnit.COULOMB, 'dimensionless':Units.StandardUnit.DIMENSIONLESS, 
                 'farad':Units.StandardUnit.FARAD, 'gram':Units.StandardUnit.GRAM, 'gray':Units.StandardUnit.GRAY, 'henry':Units.StandardUnit.HENRY, 'hertz':Units.StandardUnit.HERTZ, 'joule':Units.StandardUnit.JOULE,
                   'katal':Units.StandardUnit.KATAL, 'kelvin':Units.StandardUnit.KELVIN, 'kilogram':Units.StandardUnit.KILOGRAM, 'liter':Units.StandardUnit.LITRE, 'litre':Units.StandardUnit.LITRE, 
                   'lumen':Units.StandardUnit.LUMEN, 'lux':Units.StandardUnit.LUX, 'metre':Units.StandardUnit.METRE, 'meter':Units.StandardUnit.METRE, 'mole':Units.StandardUnit.MOLE, 'newton':Units.StandardUnit.NEWTON, 
                   'ohm':Units.StandardUnit.OHM, 'pascal':Units.StandardUnit.PASCAL, 'radian':Units.StandardUnit.RADIAN, 'second':Units.StandardUnit.SECOND, 'siemens':Units.StandardUnit.SIEMENS, 'sievert':Units.StandardUnit.SIEVERT, 
                   'steradian':Units.StandardUnit.STERADIAN, 'tesla':Units.StandardUnit.TESLA, 'volt':Units.StandardUnit.VOLT, 'watt':Units.StandardUnit.WATT, 'weber':Units.StandardUnit.WEBER}

#---------------------------------------------------------------Build a cellML model for BG----------------------------------------------------------#
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
   const = {'F':[96485,'C_per_mol'], 'R':[8.31,'J_per_K_per_mol'], 'T':[293, 'kelvin']}

"""Add variables and equations based on the component type"""
def add_BGcomp(model, name, type, voi = 't'):   
    if type not in list(BG.comp):
       sys.exit(f'BG {type} is not defined!')
    component = model.component(model.name())
    component_param = model.component(model.name()+ '_param')
    dom = BG.comp[type]['dom']
    para_name = BG.comp[type]['para'][0] + '_' + name
    para_unit = Units(BG.comp[type]['para'][1])
    para=Variable(para_name)
    para.setUnits(para_unit)
    component.addVariable(para)
    component_param.addVariable(para.clone())
    f_name = BG.dom[dom]['f'][0]+ '_' + name
    f_unit = Units(BG.dom[dom]['f'][1])
    f=Variable(f_name)
    f.setUnits(f_unit)
    component.addVariable(f)
    if type in ['Ce','Se','C','Ve']:          
        q_init_name = BG.dom[dom]['q'][0]+ '_' + name + '_init'
        q_unit = Units(BG.dom[dom]['q'][1])
        q_init=Variable(q_init_name)
        q_init.setUnits(q_unit)
        component.addVariable(q_init)
        component_param.addVariable(q_init.clone())
        q_name = BG.dom[dom]['q'][0]+ '_' + name
        q=Variable(q_name)
        q.setUnits(q_unit)
        q.setInitialValue(q_init)
        component.addVariable(q)
        e_name = BG.dom[dom]['e'][0]+ '_' + name
        e_unit = Units(BG.dom[dom]['e'][1])
        e=Variable(e_name)
        e.setUnits(e_unit)
        component.addVariable(e)
        if type in ['Ce','Se']:   
           eq = f'R*T*ln({para.name()}*{q.name()})'
        else: # 'C','Ve'
           eq = f'{f.name()}/{para.name()}'
        ode_var = f'{e.name()}'          
        component.appendMath(infix_to_mathml(eq, ode_var))
        if type in ['Ce','C']:
           ode_var = f'{q.name()}'
           eq = f'{f.name()}'
           component.appendMath(infix_to_mathml(eq, ode_var, voi))                    
    elif type == 'Re':
        ein_name = BG.dom[dom]['e'][0]+ '_' + name+ '_in'
        eout_name = BG.dom[dom]['e'][0]+ '_' + name+ '_out'
        e_unit = Units(BG.dom[dom]['e'][1])
        ein=Variable(ein_name)
        eout=Variable(eout_name)
        ein.setUnits(e_unit)
        eout.setUnits(e_unit)
        component.addVariable(ein)
        component.addVariable(eout)
        eq = f'{para.name()}*(exp({ein.name()}/(R*T))-exp({eout.name()}/(R*T)))'
        ode_var = f'{f.name()}'
        component.appendMath(infix_to_mathml(eq, ode_var))
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
        ode_var = f'{f_name}'
        eq = []
        for j in range(len(Nf[0,:])):
            if Nf[i,j] != '0':
                name = compd[j][0]
                type = compd[j][1]
                dom = BG.comp[type]['dom']
                f_name = BG.dom[dom]['f'][0]+ '_' + name
                if Nf[i,j] == '1':
                    eq.append(f'-{f_name}')
                else:
                    eq.append(f'-{Nf[i,j]}*{f_name}')
        for j in range(len(Nr[0,:])):
            if Nr[i,j] != '0':
                name = compd[j][0]
                type = compd[j][1]
                dom = BG.comp[type]['dom']
                f_name = BG.dom[dom]['f'][0]+ '_' + name
                if Nr[i,j] == '1':
                    if len(eq) == 0:
                        eq.append(f'{f_name}')
                    else:
                        eq.append(f'+{f_name}')
                else:
                    if len(eq) == 0:
                        eq.append(f'{Nr[i,j]}*{f_name}')
                    else:
                        eq.append(f'+{Nr[i,j]}*{f_name}')
                        
        component.appendMath(infix_to_mathml(''.join(eq), ode_var))
    # Add the one nodes, i.e., energy balance equations
    for j,dcomp in enumerate(compd):
        name = dcomp[0]
        type = dcomp[1]
        dom = BG.comp[type]['dom']
        ein_name = BG.dom[dom]['e'][0]+ '_' + name+ '_in'
        eout_name = BG.dom[dom]['e'][0]+ '_' + name+ '_out'
        eqout = []
        eqin = []
        ode_var_out = f'{eout_name}'
        ode_var_in = f'{ein_name}'
        for i in range(len(Nf[:,0])):
            if Nf[i,j] != '0':
                name = comps[i][0]
                type = comps[i][1]
                dom = BG.comp[type]['dom']
                e_name = BG.dom[dom]['e'][0]+ '_' + name
                if Nf[i,j] == '1':
                    if len(eqin) == 0:
                        eqin.append(f'{e_name}')
                    else:
                        eqin.append(f'+{e_name}')
                else:
                    if len(eqin) == 0:
                        eqin.append(f'{Nf[i,j]}*{e_name}')
                    else:
                        eqin.append(f'+{Nf[i,j]}*{e_name}')
        for i in range(len(Nr[:,0])):
            if Nr[i,j] != '0':
                name = comps[i][0]
                type = comps[i][1]
                dom = BG.comp[type]['dom']
                e_name = BG.dom[dom]['e'][0]+ '_' + name
                if Nr[i,j] == '1':
                    if len(eqout) == 0:
                        eqout.append(f'{e_name}')
                    else:
                        eqout.append(f'+{e_name}')
                else:
                    if len(eqout) == 0:
                        eqout.append(f'{Nr[i,j]}*{e_name}')
                    else:
                        eqout.append(f'+{Nr[i,j]}*{e_name}')

        component.appendMath(infix_to_mathml(''.join(eqin), ode_var_in))
        component.appendMath(infix_to_mathml(''.join(eqout), ode_var_out))

"""Read bond graph model from a csv file and create a CellML model from it."""
def read_csvBG():
    # Get the csv file from the user by opening a file dialog
    message='Please select the forward matrix csv file:'
    file_name_f = ask_for_file_or_folder(message)
    message='Please select the reverse matrix csv file:'
    file_name_r = ask_for_file_or_folder(message) 
    # Read the csv file, which has two rows of headers, the first row is the reaction type and the second row is the reaction name
    CompName,CompType,ReName,ReType,N_f,N_r=load_matrix(file_name_f,file_name_r)
    # Get the default model name: BG_filename
    name_f=PurePath(file_name_f).stem
    model_name = 'BG_'+ name_f.split('_')[0]
    message = f'The default model name is {model_name}. If you want to change it, please type the new name. Otherwise, just press Enter.'
    answer = ask_for_input(message, 'Text')
    if answer != '':
        model_name = answer
    # Build the model
    model = Model(model_name)
    component=Component(model_name)
    component_param=Component(model_name+'_param')
    model.addComponent(component)
    model.addComponent(component_param)
    message = 'Please specify the variable of integration, units, initial value or press Enter to use the default i.e, t,second,0:'
    answer = ask_for_input(message, 'Text')
    if answer == '':
        voi = 't'
        units = Units('second')
        init = 0
    else:
        voi = answer.split(',')[0]
        units = Units(answer.split(',')[1])
        init = float(answer.split(',')[2])
    voi = Variable(voi)
    voi.setUnits(units)
    voi.setInitialValue(init)
    component.addVariable(voi)
    component.setMath(MATH_HEADER)              
    for i, comp in enumerate(CompName):
        add_BGcomp(model, comp, CompType[i],voi.name())
    for i, re in enumerate(ReName):
        add_BGcomp(model, re, ReType[i],voi.name())
    comps = list(zip(CompName,CompType))
    compd = list(zip(ReName,ReType))
    add_BGbond(model, comps, compd, N_f, N_r)
    component.appendMath(MATH_FOOTER)
    # Set the default parameters as 1
    for var_numb in range(model.component(component_param.name()).variableCount()):
        model.component(component_param.name()).variable(var_numb).setInitialValue(1)
    # Add the constant variables
    message = 'Please select the constant variables to add:'
    choices = [f'{const}: {BG.const[const]}' for const in BG.const]
    const_selected = ask_for_input(message, 'Checkbox', choices)
    for const in const_selected:
        const_name = const.split(':')[0]
        var_const=Variable(const_name)
        unit_name = BG.const[const_name][1]
        u=Units(unit_name)
        var_const.setUnits(u)
        param_const = var_const.clone()
        param_const.setInitialValue(BG.const[const_name][0])
        model.component(component.name()).addVariable(var_const)
        model.component(component_param.name()).addVariable(param_const)
    editModel(model)    
#----------------------------------------------------------------------Build a CellML model from a csv file--------------------------------------------------------------
""" Read a csv file and create components and variables from it. """
def read_csv():    
    # Get the csv file from the user by opening a file dialog
    message='Please select the csv file to collect components:'
    file_path = ask_for_file_or_folder(message)
    df = pd.read_csv(file_path, sep=',', header=0, index_col=False,na_values='nan')
    df['component']=df['component'].fillna(method="ffill")
    gdf=df.groupby('component')
    params_comp = Component('parameters')
    components = []
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
            units_name = row['units']
            var_name = row['variable']
            variable = Variable(var_name)
            units = Units(units_name)
            variable.setUnits(units)
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
        message = f'Do you want to add equations for {component.name()}:'
        answer = ask_for_input(message, 'Confirm')
        if answer:
            component.setMath(MATH_HEADER)   
            writeEquations(component)
            component.appendMath(MATH_FOOTER)                   
        components.append(component)
    
    if params_comp.variableCount()>0:        
        components.append(params_comp)           
    return components

"""" Parse a cellml file."""
def parseCellML(strict_mode=True):
    message='Please select the CellML file:'
    filename = ask_for_file_or_folder(message)   
    # Parse the CellML file
    existing_model=cellml.parse_model(filename, strict_mode)
    return filename, existing_model


""" Specify imports and units. """
def importCellML(model,start,strict_mode=True):    
    while True:
        message = 'Do you want to import components or units from a CellML file?'
        answer = ask_for_input(message, 'Confirm')
        if answer:
            filename, existing_model = parseCellML(strict_mode)
            relative_path=PurePath(filename).relative_to(start).as_posix()
            importSource = ImportSource()
            importSource.setUrl(relative_path)
            message="Please select the component, units or equations to import:"
            choices=['units', 'components','equations']
            import_type = ask_for_input(message, 'Checkbox', choices)[0]
            if import_type == 'units':
                units_undefined=_checkUndefinedUnits(model)
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
                print(f'The units {units_to_import} have been imported.')
            elif import_type == 'components':
                message="Please select the components to import:"
                choices=[existing_model.component(comp_numb).name() for comp_numb in range(existing_model.componentCount())]
                answers = ask_for_input( message, 'Checkbox', choices)
                for component in answers:
                    message=f"If you want to rename the component {component}, please type the new name. Otherwise, just press 'Enter':"
                    answer = ask_for_input(message, 'Text')
                    if answer!='':
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
                message="Please select the components which contain the equations:"
                choices=[existing_model.component(comp_numb).name() for comp_numb in range(existing_model.componentCount())]
                answers = ask_for_input( message, 'Checkbox', choices)
                for component in answers:
                    message = f'If not {component}, please select the component which contains the equations in the new model:'
                    choices=[model.component(comp_numb).name() for comp_numb in range(model.componentCount())]
                    component_new = ask_for_input(message, 'Checkbox', choices)[0]
                    model.component(existing_model.component(component_new)).appendMath(existing_model.component(component).math())      
        else:
            break

""" Carry out the encapsulation. """
def encapsulate(model):
    while True:
        message = 'Do you want to encapsulate components?'
        answer = ask_for_input(message, 'Confirm')
        if answer:
            message="Please select the parent component:"
            choices=[model.component(comp_numb).name() for comp_numb in range(model.componentCount())]
            component_parent_selected = ask_for_input(message, 'Checkbox', choices)[0] 
            message="Please select the children components:"
            choices=[model.component(comp_numb).name() for comp_numb in range(model.componentCount()) if model.component(comp_numb).name() != component_parent_selected]
            answers = ask_for_input(message, 'Checkbox', choices)
            for component_child in answers:
                model.component(component_parent_selected).addComponent(model.component(component_child))
        else:
            break

""" Find the variables that are not mapped in two components. """
def _findMappedVariables(comp1,comp2):
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
                    

"""" Provide variable connection suggestion based on variable name and carry on the variable mapping based on user inputs. """
def suggestConnection(comp1,comp2):
    # Get the variables in the two components
    variables1 = [comp1.variable(var_numb).name() for var_numb in range(comp1.variableCount())]
    variables2 = [comp2.variable(var_numb).name() for var_numb in range(comp2.variableCount())]
    print('The variables in the first component are:', variables1)
    print('The variables in the second component are:', variables2)
    # Get the intersection of the two variables
    variables = set(variables1).intersection(variables2)
    if len(variables)>0:
        print('The variables that are shared by the two components are:', variables)
        message="Please select the variables to map. If you want to map all the variables, just press 'Enter'"
        choices=[var for var in variables]
        answers = ask_for_input( message, 'Checkbox', choices)
        if len(answers)>0:
            for var in answers:
                if Units.compatible(comp1.variable(var).units(), comp2.variable(var).units()):
                    Variable.addEquivalence(comp1.variable(var), comp2.variable(var))
                else:
                    print(f'{var} has units {comp1.variable(var).units()} in comp1 but {comp2.variable(var).units()} in comp2, which are not compatible.')
                
        else:
            for var in variables:
                if Units.compatible(comp1.variable(var).units(), comp2.variable(var).units()):
                    Variable.addEquivalence(comp1.variable(var), comp2.variable(var))
                else:
                    print(f'{var} has units {comp1.variable(var).units()} in comp1 but {comp2.variable(var).units()} in comp2, which are not compatible.')
    # Get the variables in the two components that are not sharing the same name
    variables1 = [comp1.variable(var_numb).name() for var_numb in range(comp1.variableCount()) if comp1.variable(var_numb).name() not in variables]
    variables2 = [comp2.variable(var_numb).name() for var_numb in range(comp2.variableCount()) if comp2.variable(var_numb).name() not in variables]
    if len(variables1)>0:
        message="Please select the unmapped variables in the first component to clone and map:"
        choices=[var for var in variables1]
        answers = ask_for_input( message, 'Checkbox', choices)
        for var in answers:
            comp2.addVariable(comp1.variable(var).clone())
            Variable.addEquivalence(comp1.variable(var), comp2.variable(var))     
    if len(variables2)>0:    
        message="Please select the unmapped variables in the second component to clone and map:"
        choices=[var for var in variables2]
        answers = ask_for_input( message, 'Checkbox', choices)
        for var in answers:
            comp1.addVariable(comp2.variable(var).clone())
            Variable.addEquivalence(comp1.variable(var), comp2.variable(var))
    # Keep mapping the variables in the two components that are not mapped
    while True:
        mapped_variables_comp1, mapped_variables_comp2= _findMappedVariables(comp1,comp2)
        unmapped_variables_comp1 = [comp1.variable(v).name() for v in range(comp1.variableCount()) if comp1.variable(v).name() not in mapped_variables_comp1]
        unmapped_variables_comp2 = [comp2.variable(v).name() for v in range(comp2.variableCount()) if comp2.variable(v).name() not in mapped_variables_comp2]
        if len(unmapped_variables_comp1)>0 and len(unmapped_variables_comp2)>0:
            message="Please select one variable in comp1 and another in comp2 to map or Enter to skip"
            choices=[f'comp1:{var}' for var in unmapped_variables_comp1] + [f'comp2:{var}' for var in unmapped_variables_comp2]
            answers = ask_for_input( message, 'Checkbox', choices)
            if len(answers)>0:
                var1 = answers[0].split(':')[1]
                var2 = answers[1].split(':')[1]
                if Units.compatible(comp1.variable(var).units(), comp2.variable(var).units()):
                    Variable.addEquivalence(comp1.variable(var), comp2.variable(var))
                else:
                    print(f'{var} has units {comp1.variable(var).units()} in comp1 but {comp2.variable(var).units()} in comp2, which are not compatible.')
            else:
                break
        else:
            break
    # Get the variables in the two components that are mapped but both have initial values; ask the user to select the initial value to keep
    mapped_variables_comp1, mapped_variables_comp2= _findMappedVariables(comp1,comp2)
    for var1,var2 in zip(mapped_variables_comp1, mapped_variables_comp2):
        if (comp1.variable(var1).initialValue()!='') and (comp2.variable(var2).initialValue()!= '') :
            message = f'var {var1} in {comp1.name()} with init: {comp1.variable(var1).initialValue()}\n    var {var2} in {comp2.name()} init: {comp2.variable(var2).initialValue()} \n Please select the initial value to keep:'
            choices=[comp1.name(), comp2.name()]
            answer = ask_for_input(message, 'Checkbox', choices)
            if comp1.name() not in answer:
                comp1.variable(var1).removeInitialValue()
            if  comp2.name() not in answer:
                comp2.variable(var2).removeInitialValue()

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
        message = 'Please select two components to connect or Enter to skip:'
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
                if  not (model.component(comp_numb).variable(var_numb).units().name() in BUILTIN_UNITS.keys()):
                    units_claimed.add(model.component(comp_numb).variable(var_numb).units().name())

    units_defined = set()
    for unit_numb in range(model.unitsCount()):
        # print(model.units(unit_numb).name())
        units_defined.add(model.units(unit_numb).name()) 
    units_undefined = units_claimed - units_defined
    return units_undefined

# Define the units
def _defineUnits(model,iunits):
    while True:
        message = 'Please type the name of the standardUnit or press Enter to skip:'
        unitName = ask_for_input(message, 'Text')
        if unitName != '':
            message = 'Please type the prefix or press Enter to skip:'
            prefix = ask_for_input(message, 'Text')
            message = 'Please type the exponent or press Enter to skip:'
            exponent = ask_for_input(message, 'Text')
            message = 'Please type the multiplier or press Enter to skip:'
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
            if unitName in BUILTIN_UNITS:
                iunits.addUnit(BUILTIN_UNITS[unitName], prefix, exponent, multiplier)
            else:
                iunits.addUnit(unitName,prefix, exponent, multiplier)
        else:
            break              
        model.addUnits(iunits)

# Add units to the model
def addUnitsUI(model):
    units_undefined=_checkUndefinedUnits(model)
    print('The units claimed in the variables but undefined are:',units_undefined)
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
        message = 'Please type the name of a custom units or pressEnter to skip:'
        answers = ask_for_input(message, 'Text')
        if answers!= '':
            iunits = Units(answers)
            _defineUnits(model,iunits)    
        else:
            break              
    # Replace the units with the standard units
# Write the equations to a component
def writeEquations(component):
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

# Write a model to cellml file, input: directory, model, output: cellml file
def writeCellML(directory, model):
    message = f'If you want to change the default filename {model.name()}.cellml, please type the new name. Otherwise, just press Enter.'
    file_name = ask_for_input(message, 'Text')
    if file_name == '':
        file_name=model.name()+'.cellml'
    else:
        file_name=file_name+'.cellml'        
    printer = Printer()
    serialised_model = printer.printModel(model)
    full_path = str(PurePath(directory).joinpath(file_name))
    write_file = open(full_path, "w")
    write_file.write(serialised_model)
    write_file.close()
    print('Model saved to:',full_path)
    return full_path

""""Write python code for the complete model"""
def writePythonCode(base_dir, model,strict_mode=True):
    message = 'Do you want to generate the python code?'
    answer = ask_for_input(message, 'Confirm', False)           
    if answer:
        importer = cellml.resolve_imports(model, base_dir, strict_mode)
        flatModel = importer.flattenModel(model)
        a = cellml.analyse_model(flatModel)              
        generator = Generator()
        generator.setModel(a)
        profile = GeneratorProfile(GeneratorProfile.Profile.PYTHON)
        generator.setProfile(profile)
        implementation_code_python = generator.implementationCode() 
        message = f'If you want to change the default filename {model.name()}.py, please type the new name. Otherwise, just press Enter.'
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
    message = 'Please select the folder to save the model:'
    directory = ask_for_file_or_folder(message,True)
    importCellML(model,directory)
    addUnitsUI(model)
    encapsulate(model)
    connect(model)
    model.fixVariableInterfaces()
    if model.hasUnlinkedUnits():
        model.linkUnits()
    #    Create a validator and use it to check the model so far.
    print_model(model,True)
    cellml.validate_model(model)
    #cellml.analyse_model(model)
    message="Do you want to save the model?"
    answer = ask_for_input(message, 'Confirm', True)
    if answer:
        writeCellML(directory, model)
        writePythonCode(directory, model)

"""" Assign IDs to all entities in the model; """
def assignAllIds(filename,model):
    directory=str(PurePath(filename).parent)
    annotator = Annotator()
    annotator.setModel(model)
    change = False
    # Make sure all entities in the model have an ID and make sure that all IDs in the model are unique
    if annotator.assignAllIds():
        print('Some entities have been assigned an ID, you should save the model!')
        change=True
    else:
        print('Everything already had an ID.')
    duplicates = annotator.duplicateIds()
    if len(duplicates) > 0:
        print('There are duplicate IDs. Assigning new IDs to all entities.')
        annotator.clearAllIds()
        annotator.assignAllIds()
        change=True
    if change:
        # save the updated model to a new file - note, we need the model filename for making our annotations later
        message = 'Do you want to choose different folder to save the model?'
        answer = ask_for_input(message, 'Confirm', True)
        if answer:
            message = 'Please select the folder to save the model:'
            directory = ask_for_file_or_folder(message,True)
        filename=writeCellML(directory, model)
    return filename, model  

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

""" Create a model from a list of components. """
def buildModel():
    message = 'Please select the folder to save the model:'
    directory = ask_for_file_or_folder(message,True)
    message="Please type the model name:"
    model_name = ask_for_input(message, 'Text')
    model = Model(model_name)
    message = 'Start building a model from csv file or an existing model?'
    choices = ['csv file', 'existing model']
    choice = ask_for_input(message, 'List', choices)
    if choice == 'csv file':
        components=read_csv()
        modeli = Model(model_name+'_comps')
        for component in components:
            modeli.addComponent(component)
        writeCellML(directory,modeli)      
    else:
        filename, existing_model=parseCellML
        components=[existing_model.component(comp_numb) for comp_numb in range(existing_model.componentCount())]
    while True:
        if model_name!= '':           
            model = Model(model_name)
            message="Select the components to add to the model:"
            choices=[str(components.index(component))+ ":"+ component.name() for component in components]
            components_selected = ask_for_input(message, 'Checkbox', choices)
            indexes = [int(i.split(':')[0]) for i in components_selected]
            for index in indexes:
                model.addComponent(components[index].clone())
            editModel(model)
            message="Please type the model name or press Enter to quit building models:"
            model_name = ask_for_input(message, 'Text')                               
        else:
            break
            
# main function
if __name__ == "__main__":
    buildModel()


