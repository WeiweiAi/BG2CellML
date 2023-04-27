from libcellml import Component, Model, Units,  Variable
from utilities import  ask_for_file_or_folder, ask_for_input, load_matrix, infix_to_mathml
import sys
from pathlib import PurePath
from build_CellMLV2 import editModel, MATH_FOOTER, MATH_HEADER 
from sympy import *
import numpy as np
from itertools import combinations
import networkx as nx

R,T,V_m, F, E=symbols('R,T,V_m, F, E')
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

""" From the stoichiometric matrix to derive the steady state equations"""
def flux_ss(CompName,CompType,ReName,ReType,N_f,N_r):
    # Note: cannot handle large matrix due to performance issue
    # define lambda functions to apply to the entries of matrix
    f_exp = lambda x: exp(x)
    f_log = lambda x: log(x)
    # convert the string stoichiometric matrix to float matrix. TODO: need to handle the case of stoichiometric matrix with symbolic entries   
    Nf = nsimplify(Matrix(np.array(N_f,dtype=float)))
    Nr = nsimplify(Matrix(np.array(N_r,dtype=float)))
    # Get the quantities q, thermal parameters K, of the species
    q = Matrix([Symbol(f'q_{comp}') for comp in CompName])
    K_cd=diag(*[Symbol(f'K_{comp}') for i,comp in enumerate(CompName) if CompType[i]=='Ce'])
    K_cs=diag(*[Symbol(f'K_{comp}') for i,comp in enumerate(CompName) if CompType[i]=='Se'])
    # Get the reaction rate constants kappa
    kappa = diag(*[Symbol(f'kappa_{re}') for re in ReName])
    # Split the matrices into 3 parts: the first part is the chemostatic, the second part is the chemodynamic, the third part is the electrical charge if any  
    chemostatic_index = [i for i, x in enumerate(CompType) if x == 'Se']
    chemodynamic_index = [i for i, x in enumerate(CompType) if x == 'Ce']
    electrogenic_index = [i for i, x in enumerate(CompType) if x == 'Ve']
    N_cs_f = Matrix(Nf[chemostatic_index,:])
    N_cs_r = Matrix(Nr[chemostatic_index,:])
    N_cd_f = Matrix(Nf[chemodynamic_index,:])
    N_cd_r = Matrix(Nr[chemodynamic_index,:])
    q_cs = q[chemostatic_index,:]
    N_cd = N_cd_r-N_cd_f 
    # Get the chemical potentials and electrical potential (converted to chemical potential)   
    mu_cs = R*T*((K_cs*q_cs).applyfunc(f_log))
    if len(electrogenic_index)>0:
        N_e_f = Matrix(Nf[electrogenic_index,:])
        N_e_r = Matrix(Nr[electrogenic_index,:])
        mu_e = Matrix([F*V_m for i in range(len(electrogenic_index))])
        mu_source = mu_cs.col_join(mu_e)
        N_source_f = N_cs_f.col_join(N_e_f)
        N_source_r = N_cs_r.col_join(N_e_r)
    else:
        mu_source = mu_cs
        N_source_f = N_cs_f
        N_source_r = N_cs_r
    # Construct the matrices B_f and B_r which encode the potentials impact on the reaction rates
    B_f=diag(*((N_source_f.T *(mu_source/(R*T))).applyfunc(f_exp)))
    B_r=diag(*((N_source_r.T *(mu_source/(R*T))).applyfunc(f_exp)))
    # Construct the matrix M and vector b for the linear equations
    # b is a vector containing N number of 0s and the last entry is E; N is the number of reactions minus 1
    b = Matrix([0 for i in range(Nf.shape[1]-1)]+[E])
    M_ss=N_cd*(kappa*(B_f*N_cd_f.T-B_r*N_cd_r.T)*K_cd)
    M_G = Matrix([[1 for i in range(len(chemodynamic_index))]])
    M_ss_red = M_ss[0:len(chemodynamic_index)-1,:]
    M = nsimplify(M_ss_red.col_join(M_G))
    # Solve the linear equations
    q_cd_ss =  nsimplify(M.LUsolve(b))
    M_v = nsimplify(kappa*(B_f*N_cd_f.T-B_r*N_cd_r.T)*K_cd)
    v = nsimplify(M_v*q_cd_ss)
    v_ss = factor(v[0]) # This is where the performance issue comes from
    # Get the numerator and denominator of the steady state equation
    vss_num, vss_den = fraction(v_ss)
    return vss_num, vss_den
    # Simplify the steady state equation
def simplify_flux_ss(vss_num,vss_den):
    # Get the subexpression of vss_num containing q, E and exp(F*V_m/(R*T))
    vss_num_terms = Add.make_args(expand(vss_num))
    vss_num_subterms =[]
    for i in range(len(vss_num_terms)):
        subliterals=[j for j in vss_num_terms[i].atoms() if (str(j).startswith('q') or j==E)]
        if vss_num_terms[i].has(exp(F*V_m/(R*T))): subliterals.append(exp(F*V_m/(R*T)))
        if len(subliterals)>1:
            vss_num_subterms.append(Mul(*subliterals))
        elif len(subliterals)==1:
            vss_num_subterms.append(subliterals[0])
    # Get the subexpression of vss_den containing q and exp(F*V_m/(R*T))
    vss_den_terms = Add.make_args(expand(vss_den))
    vss_den_subterms =[]
    for i in range(len(vss_den_terms)):
        subliterals=[j for j in vss_den_terms[i].atoms() if str(j).startswith('q')]
        if vss_den_terms[i].has(exp(F*V_m/(R*T))): subliterals.append(exp(F*V_m/(R*T)))
        if len(subliterals)>1:
            vss_den_subterms.append(Mul(*subliterals))
        elif len(subliterals)==1:
            vss_den_subterms.append(subliterals[0])

    # Collect the terms of the numerator and denominator to simplify the expression
    P={}
    dict_vss_num= collect(expand(vss_num),vss_num_subterms, evaluate=False)
    dict_vss_num_keys = list(dict_vss_num.keys())
    sub_dict = {}
    for i,key in enumerate(dict_vss_num_keys):
        if dict_vss_num[key].could_extract_minus_sign():
            sub_dict.update({-dict_vss_num[key]:Symbol(f'P_{i}')})
            P.update({Symbol(f'P_{i}'):-dict_vss_num[key]})
        else:
            sub_dict.update({dict_vss_num[key]:Symbol(f'P_{i}')})
            P.update({Symbol(f'P_{i}'):dict_vss_num[key]})

    c_vss_num = collect(expand(vss_num),vss_num_subterms)
    c_vss_num_simp= factor( (c_vss_num).subs(sub_dict))
    print('c_vss_num_sim=\n',c_vss_num_simp)

    dict_vss_den= collect(expand(vss_den),vss_den_subterms, evaluate=False)
    dict_vss_den_keys = list(dict_vss_den.keys())
    sub_dict = {}
    for j,key in enumerate(dict_vss_den_keys):
        if dict_vss_den[key].could_extract_minus_sign():
            sub_dict.update({-dict_vss_den[key]:Symbol(f'P_{i+j+1}')})
            P.update({Symbol(f'P_{i+j+1}'):-dict_vss_den[key]})
        else:
            sub_dict.update({dict_vss_den[key]:Symbol(f'P_{i+j+1}')})
            P.update({Symbol(f'P_{i+j+1}'):dict_vss_den[key]})

    c_vss_den= collect(expand(vss_den),vss_den_subterms)
    c_vss_den_simp= (c_vss_den).subs(sub_dict)
    print('c_vss_den_sim=\n',c_vss_den_simp)
    v_ss_simplified = c_vss_num_simp/c_vss_den_simp
    print('v_ss_simplified=\n',v_ss_simplified)
    for key in P.keys():
        print(key,'=',P[key])
    return v_ss_simplified, P
    

def flux_ss_diagram(CompName,CompType,ReName,ReType,N_f,N_r):
    # Based on the approach proposed in 
    # Hill, Terrell. Free energy transduction in biology: the steady-state kinetic and thermodynamic formalism. Elsevier, 2012.
    
    # convert the string stoichiometric matrix to float matrix   
    Nf = nsimplify(Matrix(np.array(N_f,dtype=float)))
    Nr = nsimplify(Matrix(np.array(N_r,dtype=float)))
    # Get the quantities q of the chemodynamic species (in the enzyme reaction network)
    q_cd = [f'q_{comp}' for i,comp in enumerate(CompName) if CompType[i]=='Ce']
    # Get the reaction rate constants kappa
    kappa = [Symbol(f'kappa_{re}') for re in ReName]
    # Construct a directed graph of the reaction network
    # Compute the apparent reaction rate constants of the enzyme reaction network
    G = nx.DiGraph()
    for i,comp in enumerate(CompName):
        if CompType[i]=='Ce':
            G.add_node(comp)  
    for j,re in enumerate(ReName):
        k_f_terms =[]
        k_r_terms =[]
        for i,comp in enumerate(CompName):
            if Nf[i,j]!=0 and CompType[i]=='Ce':
                mu_f = R*T*log(Symbol(f'K_{comp}')*Symbol(f'q_{comp}'))
                q_f = Symbol(f'q_{comp}')
            elif Nf[i,j]!=0 and CompType[i]=='Se':
                mu_f = R*T*log(Symbol(f'K_{comp}')*Symbol(f'q_{comp}'))
            elif Nf[i,j]!=0 and CompType[i]=='Ve':
                mu_f = F*V_m
            else:
                mu_f = 0
            if mu_f != 0:
               k_f_terms.append(Nf[i,j]*mu_f)
            if Nr[i,j]!=0 and CompType[i]=='Ce':
                mu_r = R*T*log(Symbol(f'K_{comp}')*Symbol(f'q_{comp}'))
                q_r = Symbol(f'q_{comp}')
            elif Nr[i,j]!=0 and CompType[i]=='Se':
                mu_r = R*T*log(Symbol(f'K_{comp}')*Symbol(f'q_{comp}'))
            elif Nr[i,j]!=0 and CompType[i]=='Ve':
                mu_r = F*V_m
            else:
                mu_r = 0
            if mu_r != 0:
               k_r_terms.append(Nr[i,j]*mu_r)
        k_f_mat = Matrix(k_f_terms)
        k_r_mat = Matrix(k_r_terms)
        kf_exp = nsimplify(kappa[j]*exp(sum((k_f_mat)/(R*T))))
        dict_kf= collect(kf_exp,q_f, evaluate=False)
        kr_exp = nsimplify(kappa[j]*exp(sum((k_r_mat)/(R*T))))
        dict_kr= collect(kr_exp,q_r, evaluate=False)
        G.add_edge(q_f.name,q_r.name,reaction=re, k_f=dict_kf[list(dict_kf.keys())[0]], k_r=dict_kr[list(dict_kr.keys())[0]])
    
    edge_list = list(G.edges(data=True))
    
    # Construct a 2D sympy matrix to store the product of the rate constants on the edges
    # the first dimension is the number of q_cd, the second dimension is the number of edges (reactions)
    k_mat = Matrix([[0 for i in range(len(edge_list))] for j in range(len(q_cd))])
    for  j, edgej in enumerate (edge_list):
        G_copy = G.copy()
        G_copy.remove_edge(edgej[0],edgej[1]) # Partial diagram
        for i, q in enumerate (q_cd):
            item = []
            # Get the edge list that connects the node q in the reverse direction
            edge_list_q = list(nx.edge_dfs(G_copy,q,orientation='ignore'))
            edge_list_q_rev=[edge for edge in edge_list_q if edge[2]=='reverse']
            for edge in edge_list_q_rev:
                item.append(G_copy.get_edge_data(edge[0],edge[1])['k_f'])                          
            # Get the edge list that connects the node q in the forward direction
            edge_list_q_fwd = [edge for edge in edge_list_q if edge[2]=='forward']
            for edge in edge_list_q_fwd:
                item.append(G_copy.get_edge_data(edge[0],edge[1])['k_r'])
            # Get the product of all the k_f/k_r on the path reaching q
            k_mat[i,j] = prod(item)
    # Add the columns of the k_mat to get the steady state expression of q
    q_ss_E = Matrix([0 for i in range(len(q_cd))])
    for i in range(len(q_cd)):
        q_ss_E[i] = sum(k_mat[i,:])
    
    kf_all,kr_all = [],[]
    for  j, edgej in enumerate (edge_list):
        kf_all.append(G.get_edge_data(edgej[0],edgej[1])['k_f'])
        kr_all.append(G.get_edge_data(edgej[0],edgej[1])['k_r'])

    vss_num = factor(E*(prod(kf_all)-prod(kr_all)))
    vss_den= sum(q_ss_E[:])
    return vss_num,vss_den
                    
# main function
if __name__ == "__main__":
    # Get the csv file from the user by opening a file dialog
    message='Please select the forward matrix csv file:'
    file_name_f = ask_for_file_or_folder(message)
    message='Please select the reverse matrix csv file:'
    file_name_r = ask_for_file_or_folder(message) 
    # Read the csv file, which has two rows of headers, the first row is the reaction type and the second row is the reaction name
    CompName,CompType,ReName,ReType,N_f,N_r=load_matrix(file_name_f,file_name_r)
    vss_num,vss_den = flux_ss(CompName,CompType,ReName,ReType,N_f,N_r)
    vss_num2,vss_den2 = flux_ss_diagram(CompName,CompType,ReName,ReType,N_f,N_r)
    # check the equivalence of the two expressions
    print(vss_num==vss_num2)
    print('vss_num:\n',vss_num)
    print('vss_num2:\n',vss_num2)
    print(vss_den==vss_den2)




