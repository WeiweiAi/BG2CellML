from libcellml import Component, Model, Units,  Variable
from utilities import  ask_for_file_or_folder, ask_for_input, load_matrix, infix_to_mathml
import sys
from pathlib import PurePath
from build_CellMLV2 import editModel, MATH_FOOTER, MATH_HEADER 

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
    # Define the default units for material quantity q, flow f, and effort e of each domain
    # Biochemical domain
    q_Ch_1 = Units('fmol')
    q_Ch_1.addUnit(Units.StandardUnit.MOLE, 'femto')
    v_Ch_1 = Units('fmol_per_sec')
    v_Ch_1.addUnit(Units.StandardUnit.MOLE, 'femto')
    v_Ch_1.addUnit(Units.StandardUnit.SECOND, 1, -1)
    mu_Ch_1 = Units('J_per_mol')
    mu_Ch_1.addUnit(Units.StandardUnit.JOULE)
    mu_Ch_1.addUnit(Units.StandardUnit.MOLE, 1, -1)
    q_Ch_2 = Units('mM')
    q_Ch_2.addUnit(Units.StandardUnit.MOLE, 'milli')
    q_Ch_2.addUnit(Units.StandardUnit.LITRE, 1, -1)
    v_Ch_2 = Units('mM_per_sec')
    v_Ch_2.addUnit(Units.StandardUnit.MOLE, 'milli')
    v_Ch_2.addUnit(Units.StandardUnit.LITRE, 1, -1)
    v_Ch_2.addUnit(Units.StandardUnit.SECOND, 1, -1)
    mu_Ch_2 = Units('J_per_mM')
    mu_Ch_2.addUnit(Units.StandardUnit.JOULE)
    mu_Ch_2.addUnit(Units.StandardUnit.MOLE,'milli', -1)
    mu_Ch_2.addUnit(Units.StandardUnit.LITRE)
    # Electrical domain
    q_E_1 = Units('fC')
    q_E_1.addUnit(Units.StandardUnit.COULOMB, 'femto')
    v_E_1 = Units('fA')
    v_E_1.addUnit(Units.StandardUnit.AMPERE, 'femto')
    v_E_1.addUnit(Units.StandardUnit.SECOND, 1, -1)
    # mu_E_1 = Units('volt') # volt is the default unit for effort, so no need to define it

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
            
# main function
if __name__ == "__main__":
    read_csvBG()


