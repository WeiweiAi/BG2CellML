import sys
from pathlib import PurePath,Path
# import simCellML from simCellMLV2.py which is in ../../src folder
sys.path.append('../../src')
from simCellMLV2 import simCellML

SCIPY_SOLVERS = ['dopri5', 'dop853', 'vode', 'lsoda']

step_size = 0.000001
interval = [0, 100]
result_step_size = 0.1
method = 'lsoda'

def test_SLC1():
    SLCn='1'
    py_fullpath_bg = f'./SLCT{SLCn}/SLCT{SLCn}_BG_test.py'
    py_fullpath_ss = f'./SLCT{SLCn}/SLCT{SLCn}_BG_ss_test.py'
    csv_bg_base = PurePath(py_fullpath_bg).stem
    csv_ss_base = PurePath(py_fullpath_ss).stem
    dir_path = Path(py_fullpath_bg).parent.absolute()
    parametersQ = ['q_Ai','q_Hi','q_Nai','q_Ki','q_Ao','q_Ho','q_Nao','q_Ko']
    parametersRates = ['kappa_re1','kappa_re3']
    parametersK = ['K_Ai','K_Hi','K_Nai','K_Ki','K_Ao','K_Ho','K_Nao','K_Ko']
    parametersQ_modifies_bg = [f'SLCT{SLCn}_BG_io.'+p for p in parametersQ]
    parametersRates_modifies_bg = [f'SLCT{SLCn}_BG_param.'+p for p in parametersRates]
    parametersK_modifies_bg = [f'SLCT{SLCn}_BG_param.'+p for p in parametersK]
    parameter_modifies_bg = [*parametersQ_modifies_bg,*parametersRates_modifies_bg,*parametersK_modifies_bg]
    outputs_bg = [f'SLCT{SLCn}_BG.v_Ao',f'SLCT{SLCn}_BG.v_Nao',f'SLCT{SLCn}_BG.v_Ho',f'SLCT{SLCn}_BG.v_Ko',*parameter_modifies_bg]
    
    parametersQ_modifies_ss = [f'SLCT{SLCn}_BG_ss_io.'+p for p in parametersQ]
    parameter_modifies_ss = [*parametersQ_modifies_ss,*parametersRates_modifies_bg,*parametersK_modifies_bg]
    nparameters = len(parameter_modifies_bg)
    outputs_ss = [f'SLCT{SLCn}_ss.v_ss', f'SLCT{SLCn}_BG_ss.P_0', f'SLCT{SLCn}_BG_ss.P_1',*parameter_modifies_ss]
    
    
    parameter_values = [i+2 for i in range(nparameters)]
    nparametersK = int(len(parametersK)/2)
    for i in range(nparametersK):
        parameter_values[nparameters-nparametersK*2+2*i] = (i+2)*0.1
        parameter_values[nparameters-nparametersK*2+2*i+1] = (i+2)*0.1
     
    # simulate the models using the default parameters
    csv_fullpath_bg = PurePath(dir_path).joinpath(csv_bg_base + '.csv').as_posix()
    csv_fullpath_ss = PurePath(dir_path).joinpath(csv_ss_base + '.csv').as_posix()
    simCellML(py_fullpath_bg, csv_fullpath_bg, method, interval, step_size, result_step_size,[],[],outputs_bg)
    simCellML(py_fullpath_ss, csv_fullpath_ss, method, interval, step_size, result_step_size,[],[],outputs_ss)
    csv_fullpath_bg = PurePath(dir_path).joinpath(csv_bg_base + '_1'+'.csv').as_posix()
    csv_fullpath_ss = PurePath(dir_path).joinpath(csv_ss_base + '_1'+'.csv').as_posix()
    simCellML(py_fullpath_bg, csv_fullpath_bg, method, interval, step_size, result_step_size, parameter_modifies_bg, parameter_values, outputs_bg)
    simCellML(py_fullpath_ss, csv_fullpath_ss, method, interval, step_size, result_step_size, parameter_modifies_ss, parameter_values, outputs_ss)

def test_SLC3():
    SLCn='3'
    py_fullpath_bg = f'./SLCT{SLCn}/SLCT{SLCn}_BG_test.py'
    py_fullpath_ss = f'./SLCT{SLCn}/SLCT{SLCn}_BG_ss_test.py'
    csv_bg_base = PurePath(py_fullpath_bg).stem
    csv_ss_base = PurePath(py_fullpath_ss).stem
    dir_path = Path(py_fullpath_bg).parent.absolute()
    parametersQ = ['q_Ai','q_Ao']
    parametersRates = ['kappa_re1','kappa_re2']
    parametersK = ['K_Ai','K_Ao']
    parametersQ_modifies_bg = [f'SLCT{SLCn}_BG_io.'+p for p in parametersQ]
    parametersRates_modifies_bg = [f'SLCT{SLCn}_BG_param.'+p for p in parametersRates]
    parametersK_modifies_bg = [f'SLCT{SLCn}_BG_param.'+p for p in parametersK]
    parameter_modifies_bg = [*parametersQ_modifies_bg,*parametersRates_modifies_bg,*parametersK_modifies_bg]
    outputs_bg = [f'SLCT{SLCn}_BG.v_Ao',*parameter_modifies_bg]
    
    parametersQ_modifies_ss = [f'SLCT{SLCn}_BG_ss_io.'+p for p in parametersQ]
    parameter_modifies_ss = [*parametersQ_modifies_ss,*parametersRates_modifies_bg,*parametersK_modifies_bg]
    nparameters = len(parameter_modifies_bg)
    outputs_ss = [f'SLCT{SLCn}_ss.v_ss',f'SLCT{SLCn}_BG_ss.P_0', f'SLCT{SLCn}_BG_ss.P_1',*parameter_modifies_ss]

    parameter_values = [i+2 for i in range(nparameters)]
    nparametersK = int(len(parametersK)/2)
    for i in range(nparametersK):
        parameter_values[nparameters-nparametersK*2+2*i] = (i+2)*0.1
        parameter_values[nparameters-nparametersK*2+2*i+1] = (i+2)*0.1
      
    # simulate the models using the default parameters
    csv_fullpath_bg = PurePath(dir_path).joinpath(csv_bg_base + '.csv').as_posix()
    csv_fullpath_ss = PurePath(dir_path).joinpath(csv_ss_base + '.csv').as_posix()
    simCellML(py_fullpath_bg, csv_fullpath_bg, method, interval, step_size, result_step_size,[],[],outputs_bg)
    simCellML(py_fullpath_ss, csv_fullpath_ss, method, interval, step_size, result_step_size,[],[],outputs_ss)
    csv_fullpath_bg = PurePath(dir_path).joinpath(csv_bg_base + '_1'+'.csv').as_posix()
    csv_fullpath_ss = PurePath(dir_path).joinpath(csv_ss_base + '_1'+'.csv').as_posix()
    simCellML(py_fullpath_bg, csv_fullpath_bg, method, interval, step_size, result_step_size, parameter_modifies_bg, parameter_values, outputs_bg)
    simCellML(py_fullpath_ss, csv_fullpath_ss, method, interval, step_size, result_step_size, parameter_modifies_ss, parameter_values, outputs_ss)

def test_SLC4():
    SLCn='4'
    py_fullpath_bg = f'./SLCT{SLCn}/SLCT{SLCn}_BG_test.py'
    py_fullpath_ss = f'./SLCT{SLCn}/SLCT{SLCn}_BG_ss_test.py'
    csv_bg_base = PurePath(py_fullpath_bg).stem
    csv_ss_base = PurePath(py_fullpath_ss).stem
    dir_path = Path(py_fullpath_bg).parent.absolute()
    parametersQ = ['q_Ai','q_Ao','q_Bi','q_Bo']
    parametersRates = ['kappa_re1','kappa_re2']
    parametersK = ['K_Ai','K_Ao','K_Bi','K_Bo']
    parametersQ_modifies_bg = [f'SLCT{SLCn}_BG_io.'+p for p in parametersQ]
    parametersRates_modifies_bg = [f'SLCT{SLCn}_BG_param.'+p for p in parametersRates]
    parametersK_modifies_bg = [f'SLCT{SLCn}_BG_param.'+p for p in parametersK]
    parameter_modifies_bg = [*parametersQ_modifies_bg,*parametersRates_modifies_bg,*parametersK_modifies_bg]
    outputs_bg = [f'SLCT{SLCn}_BG.v_Ao',f'SLCT{SLCn}_BG.v_Bo',*parameter_modifies_bg]
    
    parametersQ_modifies_ss = [f'SLCT{SLCn}_BG_ss_io.'+p for p in parametersQ]
    parameter_modifies_ss = [*parametersQ_modifies_ss,*parametersRates_modifies_bg,*parametersK_modifies_bg]
    nparameters = len(parameter_modifies_bg)
    outputs_ss = [f'SLCT{SLCn}_ss.v_ss',f'SLCT{SLCn}_BG_ss.P_0', f'SLCT{SLCn}_BG_ss.P_1',*parameter_modifies_ss]

    parameter_values = [i+2 for i in range(nparameters)]
    nparametersK = int(len(parametersK)/2)
    for i in range(nparametersK):
        parameter_values[nparameters-nparametersK*2+2*i] = (i+2)*0.1
        parameter_values[nparameters-nparametersK*2+2*i+1] = (i+2)*0.1
      
    # simulate the models using the default parameters
    csv_fullpath_bg = PurePath(dir_path).joinpath(csv_bg_base + '.csv').as_posix()
    csv_fullpath_ss = PurePath(dir_path).joinpath(csv_ss_base + '.csv').as_posix()
    simCellML(py_fullpath_bg, csv_fullpath_bg, method, interval, step_size, result_step_size,[],[],outputs_bg)
    simCellML(py_fullpath_ss, csv_fullpath_ss, method, interval, step_size, result_step_size,[],[],outputs_ss)
    csv_fullpath_bg = PurePath(dir_path).joinpath(csv_bg_base + '_1'+'.csv').as_posix()
    csv_fullpath_ss = PurePath(dir_path).joinpath(csv_ss_base + '_1'+'.csv').as_posix()
    simCellML(py_fullpath_bg, csv_fullpath_bg, method, interval, step_size, result_step_size, parameter_modifies_bg, parameter_values, outputs_bg)
    simCellML(py_fullpath_ss, csv_fullpath_ss, method, interval, step_size, result_step_size, parameter_modifies_ss, parameter_values, outputs_ss)

def test_SLC5():
    SLCn='5'
    py_fullpath_bg = f'./SLCT{SLCn}/SLCT{SLCn}_BG_test.py'
    py_fullpath_ss = f'./SLCT{SLCn}/SLCT{SLCn}_BG_ss_test.py'
    csv_bg_base = PurePath(py_fullpath_bg).stem
    csv_ss_base = PurePath(py_fullpath_ss).stem
    dir_path = Path(py_fullpath_bg).parent.absolute()
    parametersQ = ['q_HCO3i','q_HCO3o','q_Nai','q_Nao']
    parametersRates = ['kappa_re1','kappa_re2']
    parametersK = ['K_HCO3i','K_HCO3o','K_Ai','K_Ao']
    parametersQ_modifies_bg = [f'SLCT{SLCn}_BG_io.'+p for p in parametersQ]
    parametersRates_modifies_bg = [f'SLCT{SLCn}_BG_param.'+p for p in parametersRates]
    parametersK_modifies_bg = [f'SLCT{SLCn}_BG_param.'+p for p in parametersK]
    parameter_modifies_bg = [*parametersQ_modifies_bg,*parametersRates_modifies_bg,*parametersK_modifies_bg,f'SLCT{SLCn}_BG_io. q_m']
    outputs_bg = [f'SLCT{SLCn}_BG.v_HCO3o',f'SLCT{SLCn}_BG.v_Nao',*parameter_modifies_bg]
    
    parametersQ_modifies_ss = [f'SLCT{SLCn}_BG_ss_io.'+p for p in parametersQ]
    parameter_modifies_ss = [*parametersQ_modifies_ss,*parametersRates_modifies_bg,*parametersK_modifies_bg,f'SLCT{SLCn}_BG_ss_io. V_m']
    nparameters = len(parameter_modifies_bg)-1
    outputs_ss = [f'SLCT{SLCn}_ss.v_ss',f'SLCT{SLCn}_BG_ss.P_0', f'SLCT{SLCn}_BG_ss.P_1',*parameter_modifies_ss]

    parameter_values = [i+2 for i in range(nparameters)]
    nparametersK = int(len(parametersK)/2)
    for i in range(nparametersK):
        parameter_values[nparameters-nparametersK*2+2*i] = (i+2)*0.1
        parameter_values[nparameters-nparametersK*2+2*i+1] = (i+2)*0.1

    parameter_values.append(-0.01)

    # simulate the models using the default parameters
    csv_fullpath_bg = PurePath(dir_path).joinpath(csv_bg_base + '.csv').as_posix()
    csv_fullpath_ss = PurePath(dir_path).joinpath(csv_ss_base + '.csv').as_posix()
    simCellML(py_fullpath_bg, csv_fullpath_bg, method, interval, step_size, result_step_size,[],[],outputs_bg)
    simCellML(py_fullpath_ss, csv_fullpath_ss, method, interval, step_size, result_step_size,[],[],outputs_ss)
    csv_fullpath_bg = PurePath(dir_path).joinpath(csv_bg_base + '_1'+'.csv').as_posix()
    csv_fullpath_ss = PurePath(dir_path).joinpath(csv_ss_base + '_1'+'.csv').as_posix()
    simCellML(py_fullpath_bg, csv_fullpath_bg, method, interval, step_size, result_step_size, parameter_modifies_bg, parameter_values, outputs_bg)
    simCellML(py_fullpath_ss, csv_fullpath_ss, method, interval, step_size, result_step_size, parameter_modifies_ss, parameter_values, outputs_ss)

def test_SLC6():
    SLCn='6'
    py_fullpath_bg = f'./SLCT{SLCn}/SLCT{SLCn}_BG_test.py'
    py_fullpath_ss = f'./SLCT{SLCn}/SLCT{SLCn}_BG_ss_test.py'
    csv_bg_base = PurePath(py_fullpath_bg).stem
    csv_ss_base = PurePath(py_fullpath_ss).stem
    dir_path = Path(py_fullpath_bg).parent.absolute()
    parametersQ = ['q_HCO3i','q_HCO3o','q_Nai','q_Nao']
    parametersRates = ['kappa_re1','kappa_re2']
    parametersK = ['K_HCO3i','K_HCO3o','K_Nai','K_Nao']
    parametersQ_modifies_bg = [f'SLCT{SLCn}_BG_io.'+p for p in parametersQ]
    parametersRates_modifies_bg = [f'SLCT{SLCn}_BG_param.'+p for p in parametersRates]
    parametersK_modifies_bg = [f'SLCT{SLCn}_BG_param.'+p for p in parametersK]
    parameter_modifies_bg = [*parametersQ_modifies_bg,*parametersRates_modifies_bg,*parametersK_modifies_bg,f'SLCT{SLCn}_BG_io. q_m']
    outputs_bg = [f'SLCT{SLCn}_BG.v_HCO3o',f'SLCT{SLCn}_BG.v_Nao',f'SLCT{SLCn}_BG.v_re2',f'SLCT{SLCn}_BG.v_re3',f'SLCT{SLCn}_BG.v_re4',f'SLCT{SLCn}_BG.v_re5',f'SLCT{SLCn}_BG.v_re6',*parameter_modifies_bg]
    
    parametersQ_modifies_ss = [f'SLCT{SLCn}_BG_ss_io.'+p for p in parametersQ]
    parameter_modifies_ss = [*parametersQ_modifies_ss,*parametersRates_modifies_bg,*parametersK_modifies_bg,f'SLCT{SLCn}_BG_ss_io. V_m']
    nparameters = len(parameter_modifies_bg)-1
    outputs_ss = [f'SLCT{SLCn}_ss.v_ss',f'SLCT{SLCn}_BG_ss.P_0', f'SLCT{SLCn}_BG_ss.P_1',*parameter_modifies_ss]

    parameter_values = [i+1 for i in range(nparameters)]
    nparametersK = int(len(parametersK)/2)
    for i in range(nparametersK):
        parameter_values[nparameters-nparametersK*2+2*i] = (i+2)*0.1
        parameter_values[nparameters-nparametersK*2+2*i+1] = (i+2)*0.1

    parameter_values.append(-0.01)
    # simulate the models using the default parameters
    csv_fullpath_bg = PurePath(dir_path).joinpath(csv_bg_base + '.csv').as_posix()
    csv_fullpath_ss = PurePath(dir_path).joinpath(csv_ss_base + '.csv').as_posix()
    simCellML(py_fullpath_bg, csv_fullpath_bg, method, interval, step_size, result_step_size,[],[],outputs_bg)
    simCellML(py_fullpath_ss, csv_fullpath_ss, method, interval, step_size, result_step_size,[],[],outputs_ss)
    csv_fullpath_bg = PurePath(dir_path).joinpath(csv_bg_base + '_1'+'.csv').as_posix()
    csv_fullpath_ss = PurePath(dir_path).joinpath(csv_ss_base + '_1'+'.csv').as_posix()
    simCellML(py_fullpath_bg, csv_fullpath_bg, method, interval, step_size, result_step_size, parameter_modifies_bg, parameter_values, outputs_bg)
    simCellML(py_fullpath_ss, csv_fullpath_ss, method, interval, step_size, result_step_size, parameter_modifies_ss, parameter_values, outputs_ss)

def test_SLC7():
    SLCn='7'
    py_fullpath_bg = f'./SLCT{SLCn}/SLCT{SLCn}_BG_test.py'
    py_fullpath_ss = f'./SLCT{SLCn}/SLCT{SLCn}_BG_ss_test.py'
    csv_bg_base = PurePath(py_fullpath_bg).stem
    csv_ss_base = PurePath(py_fullpath_ss).stem
    dir_path = Path(py_fullpath_bg).parent.absolute()
    parametersQ = ['q_HCO3i','q_HCO3o','q_Nai','q_Nao','q_Cli','q_Clo']
    parametersRates = ['kappa_re1','kappa_re2']
    parametersK = ['K_HCO3i','K_HCO3o','K_Nai','K_Nao','K_Cli','K_Clo']
    parametersQ_modifies_bg = [f'SLCT{SLCn}_BG_io.'+p for p in parametersQ]
    parametersRates_modifies_bg = [f'SLCT{SLCn}_BG_param.'+p for p in parametersRates]
    parametersK_modifies_bg = [f'SLCT{SLCn}_BG_param.'+p for p in parametersK]
    parameter_modifies_bg = [*parametersQ_modifies_bg,*parametersRates_modifies_bg,*parametersK_modifies_bg]
    outputs_bg = [f'SLCT{SLCn}_BG.v_HCO3o',f'SLCT{SLCn}_BG.v_Nao',f'SLCT{SLCn}_BG.v_Clo',*parameter_modifies_bg]
    
    parametersQ_modifies_ss = [f'SLCT{SLCn}_BG_ss_io.'+p for p in parametersQ]
    parameter_modifies_ss = [*parametersQ_modifies_ss,*parametersRates_modifies_bg,*parametersK_modifies_bg]
    nparameters = len(parameter_modifies_bg)
    outputs_ss = [f'SLCT{SLCn}_ss.v_ss',f'SLCT{SLCn}_BG_ss.P_0', f'SLCT{SLCn}_BG_ss.P_1',*parameter_modifies_ss]

    parameter_values = [i+2 for i in range(nparameters)]
    nparametersK = int(len(parametersK)/2)
    for i in range(nparametersK):
        parameter_values[nparameters-nparametersK*2+2*i] = (i+2)*0.1
        parameter_values[nparameters-nparametersK*2+2*i+1] = (i+2)*0.1
    
    # simulate the models using the default parameters
    csv_fullpath_bg = PurePath(dir_path).joinpath(csv_bg_base + '.csv').as_posix()
    csv_fullpath_ss = PurePath(dir_path).joinpath(csv_ss_base + '.csv').as_posix()
    simCellML(py_fullpath_bg, csv_fullpath_bg, method, interval, step_size, result_step_size,[],[],outputs_bg)
    simCellML(py_fullpath_ss, csv_fullpath_ss, method, interval, step_size, result_step_size,[],[],outputs_ss)
    csv_fullpath_bg = PurePath(dir_path).joinpath(csv_bg_base + '_1'+'.csv').as_posix()
    csv_fullpath_ss = PurePath(dir_path).joinpath(csv_ss_base + '_1'+'.csv').as_posix()
    simCellML(py_fullpath_bg, csv_fullpath_bg, method, interval, step_size, result_step_size, parameter_modifies_bg, parameter_values, outputs_bg)
    simCellML(py_fullpath_ss, csv_fullpath_ss, method, interval, step_size, result_step_size, parameter_modifies_ss, parameter_values, outputs_ss)

def test_SLC8():
    SLCn='8'
    py_fullpath_bg = f'./SLCT{SLCn}/SLCT{SLCn}_BG_test.py'
    py_fullpath_ss = f'./SLCT{SLCn}/SLCT{SLCn}_BG_ss_test.py'
    csv_bg_base = PurePath(py_fullpath_bg).stem
    csv_ss_base = PurePath(py_fullpath_ss).stem
    dir_path = Path(py_fullpath_bg).parent.absolute()
    parametersQ = ['q_Nai','q_Nao','q_Glui','q_Gluo']
    parametersRates = ['kappa_re1','kappa_re2']
    parametersK = ['K_Glui','K_Gluo','K_Nai','K_Nao']
    parametersQ_modifies_bg = [f'SLCT{SLCn}_BG_io.'+p for p in parametersQ]
    parametersRates_modifies_bg = [f'SLCT{SLCn}_BG_param.'+p for p in parametersRates]
    parametersK_modifies_bg = [f'SLCT{SLCn}_BG_param.'+p for p in parametersK]
    parameter_modifies_bg = [*parametersQ_modifies_bg,*parametersRates_modifies_bg,*parametersK_modifies_bg,f'SLCT{SLCn}_BG_io. q_m']
    outputs_bg = [f'SLCT{SLCn}_BG.v_Gluo',f'SLCT{SLCn}_BG.v_Nao',f'SLCT{SLCn}_BG.v_re6',f'SLCT{SLCn}_BG.v_re1',f'SLCT{SLCn}_BG.v_re3',*parameter_modifies_bg]
    
    parametersQ_modifies_ss = [f'SLCT{SLCn}_BG_ss_io.'+p for p in parametersQ]
    parameter_modifies_ss = [*parametersQ_modifies_ss,*parametersRates_modifies_bg,*parametersK_modifies_bg,f'SLCT{SLCn}_BG_ss_io. V_m']
    nparameters = len(parameter_modifies_bg)-1
    outputs_ss = [f'SLCT{SLCn}_ss.v_ss',*parameter_modifies_ss]

    parameter_values = [i+1 for i in range(nparameters)]
    nparametersK = int(len(parametersK)/2)
    for i in range(nparametersK):
        parameter_values[nparameters-nparametersK*2+2*i] = (i+2)*0.1
        parameter_values[nparameters-nparametersK*2+2*i+1] = (i+2)*0.1
    
    parameter_values.append(-0.01)  
      
    # simulate the models using the default parameters
    csv_fullpath_bg = PurePath(dir_path).joinpath(csv_bg_base + '.csv').as_posix()
    csv_fullpath_ss = PurePath(dir_path).joinpath(csv_ss_base + '.csv').as_posix()
    simCellML(py_fullpath_bg, csv_fullpath_bg, method, interval, step_size, result_step_size,[],[],outputs_bg)
    simCellML(py_fullpath_ss, csv_fullpath_ss, method, interval, step_size, result_step_size,[],[],outputs_ss)
    csv_fullpath_bg = PurePath(dir_path).joinpath(csv_bg_base + '_1'+'.csv').as_posix()
    csv_fullpath_ss = PurePath(dir_path).joinpath(csv_ss_base + '_1'+'.csv').as_posix()
    simCellML(py_fullpath_bg, csv_fullpath_bg, method, interval, step_size, result_step_size, parameter_modifies_bg, parameter_values, outputs_bg)
    simCellML(py_fullpath_ss, csv_fullpath_ss, method, interval, step_size, result_step_size, parameter_modifies_ss, parameter_values, outputs_ss)


def test_SLC9():
    SLCn='9'
    py_fullpath_bg = f'./SLCT{SLCn}/SLCT{SLCn}_BG_test.py'
    py_fullpath_ss = f'./SLCT{SLCn}/SLCT{SLCn}_BG_ss_test.py'
    csv_bg_base = PurePath(py_fullpath_bg).stem
    csv_ss_base = PurePath(py_fullpath_ss).stem
    dir_path = Path(py_fullpath_bg).parent.absolute()
    parametersQ = ['q_Ai','q_Ao','q_Nai','q_Nao','q_Cli','q_Clo']
    parametersRates = ['kappa_re1','kappa_re2']
    parametersK = ['K_Ai','K_Ao','K_Nai','K_Nao','K_Cli','K_Clo']
    parametersQ_modifies_bg = [f'SLCT{SLCn}_BG_io.'+p for p in parametersQ]
    parametersRates_modifies_bg = [f'SLCT{SLCn}_BG_param.'+p for p in parametersRates]
    parametersK_modifies_bg = [f'SLCT{SLCn}_BG_param.'+p for p in parametersK]
    parameter_modifies_bg = [*parametersQ_modifies_bg,*parametersRates_modifies_bg,*parametersK_modifies_bg,f'SLCT{SLCn}_BG_io. q_m']
    outputs_bg = [f'SLCT{SLCn}_BG.v_Ao',f'SLCT{SLCn}_BG.v_Nao',f'SLCT{SLCn}_BG.v_Clo',*parameter_modifies_bg]
    
    parametersQ_modifies_ss = [f'SLCT{SLCn}_BG_ss_io.'+p for p in parametersQ]
    parameter_modifies_ss = [*parametersQ_modifies_ss,*parametersRates_modifies_bg,*parametersK_modifies_bg,f'SLCT{SLCn}_BG_ss_io. V_m']
    nparameters = len(parameter_modifies_bg)-1
    outputs_ss = [f'SLCT{SLCn}_ss.v_ss',f'SLCT{SLCn}_BG_ss.P_0', f'SLCT{SLCn}_BG_ss.P_1',*parameter_modifies_ss]

    parameter_values = [i+2 for i in range(nparameters)]
    nparametersK = int(len(parametersK)/2)
    for i in range(nparametersK):
        parameter_values[nparameters-nparametersK*2+2*i] = (i+2)*0.1
        parameter_values[nparameters-nparametersK*2+2*i+1] = (i+2)*0.1
    parameter_values.append(-0.01)  
    # simulate the models using the default parameters
    csv_fullpath_bg = PurePath(dir_path).joinpath(csv_bg_base + '.csv').as_posix()
    csv_fullpath_ss = PurePath(dir_path).joinpath(csv_ss_base + '.csv').as_posix()
    simCellML(py_fullpath_bg, csv_fullpath_bg, method, interval, step_size, result_step_size,[],[],outputs_bg)
    simCellML(py_fullpath_ss, csv_fullpath_ss, method, interval, step_size, result_step_size,[],[],outputs_ss)
    csv_fullpath_bg = PurePath(dir_path).joinpath(csv_bg_base + '_1'+'.csv').as_posix()
    csv_fullpath_ss = PurePath(dir_path).joinpath(csv_ss_base + '_1'+'.csv').as_posix()
    simCellML(py_fullpath_bg, csv_fullpath_bg, method, interval, step_size, result_step_size, parameter_modifies_bg, parameter_values, outputs_bg)
    simCellML(py_fullpath_ss, csv_fullpath_ss, method, interval, step_size, result_step_size, parameter_modifies_ss, parameter_values, outputs_ss)

def test_SLC10():
    SLCn='10'
    py_fullpath_bg = f'./SLCT{SLCn}/SLCT{SLCn}_BG_test.py'
    py_fullpath_ss = f'./SLCT{SLCn}/SLCT{SLCn}_BG_ss_test.py'
    csv_bg_base = PurePath(py_fullpath_bg).stem
    csv_ss_base = PurePath(py_fullpath_ss).stem
    dir_path = Path(py_fullpath_bg).parent.absolute()
    parametersQ = ['q_Ai','q_Ao','q_Nai','q_Nao','q_Cli','q_Clo']
    parametersRates = ['kappa_re1','kappa_re2']
    parametersK = ['K_Ai','K_Ao','K_Nai','K_Nao','K_Cli','K_Clo']
    parametersQ_modifies_bg = [f'SLCT{SLCn}_BG_io.'+p for p in parametersQ]
    parametersRates_modifies_bg = [f'SLCT{SLCn}_BG_param.'+p for p in parametersRates]
    parametersK_modifies_bg = [f'SLCT{SLCn}_BG_param.'+p for p in parametersK]
    parameter_modifies_bg = [*parametersQ_modifies_bg,*parametersRates_modifies_bg,*parametersK_modifies_bg,f'SLCT{SLCn}_BG_io. q_m']
    outputs_bg = [f'SLCT{SLCn}_BG.v_Ao',f'SLCT{SLCn}_BG.v_Nao',f'SLCT{SLCn}_BG.v_Clo',*parameter_modifies_bg]
    
    parametersQ_modifies_ss = [f'SLCT{SLCn}_BG_ss_io.'+p for p in parametersQ]
    parameter_modifies_ss = [*parametersQ_modifies_ss,*parametersRates_modifies_bg,*parametersK_modifies_bg,f'SLCT{SLCn}_BG_ss_io. V_m']
    nparameters = len(parameter_modifies_bg)-1
    outputs_ss = [f'SLCT{SLCn}_ss.v_ss',f'SLCT{SLCn}_BG_ss.P_0', f'SLCT{SLCn}_BG_ss.P_1',*parameter_modifies_ss]

    parameter_values = [i+2 for i in range(nparameters)]
    nparametersK = int(len(parametersK)/2)
    for i in range(nparametersK):
        parameter_values[nparameters-nparametersK*2+2*i] = (i+2)*0.1
        parameter_values[nparameters-nparametersK*2+2*i+1] = (i+2)*0.1
    parameter_values.append(-0.01)  
    # simulate the models using the default parameters
    csv_fullpath_bg = PurePath(dir_path).joinpath(csv_bg_base + '.csv').as_posix()
    csv_fullpath_ss = PurePath(dir_path).joinpath(csv_ss_base + '.csv').as_posix()
    simCellML(py_fullpath_bg, csv_fullpath_bg, method, interval, step_size, result_step_size,[],[],outputs_bg)
    simCellML(py_fullpath_ss, csv_fullpath_ss, method, interval, step_size, result_step_size,[],[],outputs_ss)
    csv_fullpath_bg = PurePath(dir_path).joinpath(csv_bg_base + '_1'+'.csv').as_posix()
    csv_fullpath_ss = PurePath(dir_path).joinpath(csv_ss_base + '_1'+'.csv').as_posix()
    simCellML(py_fullpath_bg, csv_fullpath_bg, method, interval, step_size, result_step_size, parameter_modifies_bg, parameter_values, outputs_bg)
    simCellML(py_fullpath_ss, csv_fullpath_ss, method, interval, step_size, result_step_size, parameter_modifies_ss, parameter_values, outputs_ss)

def test_SLC11():
    SLCn='11'
    py_fullpath_bg = f'./SLCT{SLCn}/SLCT{SLCn}_BG_test.py'
    py_fullpath_ss = f'./SLCT{SLCn}/SLCT{SLCn}_BG_ss_test.py'
    csv_bg_base = PurePath(py_fullpath_bg).stem
    csv_ss_base = PurePath(py_fullpath_ss).stem
    dir_path = Path(py_fullpath_bg).parent.absolute()
    parametersQ = ['q_Si','q_So','q_Nai','q_Nao','q_Cli','q_Clo','q_Ki','q_Ko']
    parametersRates = ['kappa_re1','kappa_re2']
    parametersK = ['K_Si','K_So','K_Nai','K_Nao','K_Cli','K_Clo','K_Ki','K_Ko']
    parametersQ_modifies_bg = [f'SLCT{SLCn}_BG_io.'+p for p in parametersQ]
    parametersRates_modifies_bg = [f'SLCT{SLCn}_BG_param.'+p for p in parametersRates]
    parametersK_modifies_bg = [f'SLCT{SLCn}_BG_param.'+p for p in parametersK]
    parameter_modifies_bg = [*parametersQ_modifies_bg,*parametersRates_modifies_bg,*parametersK_modifies_bg]
    outputs_bg = [f'SLCT{SLCn}_BG.v_So',f'SLCT{SLCn}_BG.v_Nao',f'SLCT{SLCn}_BG.v_Clo',f'SLCT{SLCn}_BG.v_Ko',*parameter_modifies_bg]
    
    parametersQ_modifies_ss = [f'SLCT{SLCn}_BG_ss_io.'+p for p in parametersQ]
    parameter_modifies_ss = [*parametersQ_modifies_ss,*parametersRates_modifies_bg,*parametersK_modifies_bg]
    nparameters = len(parameter_modifies_bg)
    outputs_ss = [f'SLCT{SLCn}_ss.v_ss',f'SLCT{SLCn}_BG_ss.P_0', f'SLCT{SLCn}_BG_ss.P_1',*parameter_modifies_ss]

    parameter_values = [i+2 for i in range(nparameters)]
    nparametersK = int(len(parametersK)/2)
    for i in range(nparametersK):
        parameter_values[nparameters-nparametersK*2+2*i] = (i+2)*0.1
        parameter_values[nparameters-nparametersK*2+2*i+1] = (i+2)*0.1
      
    # simulate the models using the default parameters
    csv_fullpath_bg = PurePath(dir_path).joinpath(csv_bg_base + '.csv').as_posix()
    csv_fullpath_ss = PurePath(dir_path).joinpath(csv_ss_base + '.csv').as_posix()
    simCellML(py_fullpath_bg, csv_fullpath_bg, method, interval, step_size, result_step_size,[],[],outputs_bg)
    simCellML(py_fullpath_ss, csv_fullpath_ss, method, interval, step_size, result_step_size,[],[],outputs_ss)
    csv_fullpath_bg = PurePath(dir_path).joinpath(csv_bg_base + '_1'+'.csv').as_posix()
    csv_fullpath_ss = PurePath(dir_path).joinpath(csv_ss_base + '_1'+'.csv').as_posix()
    simCellML(py_fullpath_bg, csv_fullpath_bg, method, interval, step_size, result_step_size, parameter_modifies_bg, parameter_values, outputs_bg)
    simCellML(py_fullpath_ss, csv_fullpath_ss, method, interval, step_size, result_step_size, parameter_modifies_ss, parameter_values, outputs_ss)

def test_SLC12():
    SLCn='12'
    py_fullpath_bg = f'./SLCT{SLCn}/SLCT{SLCn}_BG_test.py'
    py_fullpath_ss = f'./SLCT{SLCn}/SLCT{SLCn}_BG_ss_test.py'
    csv_bg_base = PurePath(py_fullpath_bg).stem
    csv_ss_base = PurePath(py_fullpath_ss).stem
    dir_path = Path(py_fullpath_bg).parent.absolute()
    parametersQ = ['q_Ai','q_Ao','q_Nai','q_Nao']
    parametersRates = ['kappa_re1','kappa_re2']
    parametersK = ['K_Ai','K_Ao','K_Nai','K_Nao']
    parametersQ_modifies_bg = [f'SLCT{SLCn}_BG_io.'+p for p in parametersQ]
    parametersRates_modifies_bg = [f'SLCT{SLCn}_BG_param.'+p for p in parametersRates]
    parametersK_modifies_bg = [f'SLCT{SLCn}_BG_param.'+p for p in parametersK]
    parameter_modifies_bg = [*parametersQ_modifies_bg,*parametersRates_modifies_bg,*parametersK_modifies_bg,f'SLCT{SLCn}_BG_io. q_m']
    outputs_bg = [f'SLCT{SLCn}_BG.v_Ao',f'SLCT{SLCn}_BG.v_Nao',*parameter_modifies_bg]
    
    parametersQ_modifies_ss = [f'SLCT{SLCn}_BG_ss_io.'+p for p in parametersQ]
    parameter_modifies_ss = [*parametersQ_modifies_ss,*parametersRates_modifies_bg,*parametersK_modifies_bg,f'SLCT{SLCn}_BG_ss_io. V_m']
    nparameters = len(parameter_modifies_bg)-1
    outputs_ss = [f'SLCT{SLCn}_ss.v_ss',f'SLCT{SLCn}_BG_ss.P_0', f'SLCT{SLCn}_BG_ss.P_1',*parameter_modifies_ss]

    parameter_values = [i+2 for i in range(nparameters)]
    nparametersK = int(len(parametersK)/2)
    for i in range(nparametersK):
        parameter_values[nparameters-nparametersK*2+2*i] = (i+2)*0.1
        parameter_values[nparameters-nparametersK*2+2*i+1] = (i+2)*0.1
    parameter_values.append(-0.01)  
    # simulate the models using the default parameters
    csv_fullpath_bg = PurePath(dir_path).joinpath(csv_bg_base + '.csv').as_posix()
    csv_fullpath_ss = PurePath(dir_path).joinpath(csv_ss_base + '.csv').as_posix()
    simCellML(py_fullpath_bg, csv_fullpath_bg, method, interval, step_size, result_step_size,[],[],outputs_bg)
    simCellML(py_fullpath_ss, csv_fullpath_ss, method, interval, step_size, result_step_size,[],[],outputs_ss)
    csv_fullpath_bg = PurePath(dir_path).joinpath(csv_bg_base + '_1'+'.csv').as_posix()
    csv_fullpath_ss = PurePath(dir_path).joinpath(csv_ss_base + '_1'+'.csv').as_posix()
    simCellML(py_fullpath_bg, csv_fullpath_bg, method, interval, step_size, result_step_size, parameter_modifies_bg, parameter_values, outputs_bg)
    simCellML(py_fullpath_ss, csv_fullpath_ss, method, interval, step_size, result_step_size, parameter_modifies_ss, parameter_values, outputs_ss)

def test_SLC13():
    SLCn='13'
    py_fullpath_bg = f'./SLCT{SLCn}/SLCT{SLCn}_BG_test.py'
    py_fullpath_ss = f'./SLCT{SLCn}/SLCT{SLCn}_BG_ss_test.py'
    csv_bg_base = PurePath(py_fullpath_bg).stem
    csv_ss_base = PurePath(py_fullpath_ss).stem
    dir_path = Path(py_fullpath_bg).parent.absolute()
    parametersQ = ['q_Ai','q_Ao','q_Nai','q_Nao','q_Cli','q_Clo']
    parametersRates = ['kappa_re1','kappa_re2']
    parametersK = ['K_Ai','K_Ao','K_Nai','K_Nao','K_Cli','K_Clo']
    parametersQ_modifies_bg = [f'SLCT{SLCn}_BG_io.'+p for p in parametersQ]
    parametersRates_modifies_bg = [f'SLCT{SLCn}_BG_param.'+p for p in parametersRates]
    parametersK_modifies_bg = [f'SLCT{SLCn}_BG_param.'+p for p in parametersK]
    parameter_modifies_bg = [*parametersQ_modifies_bg,*parametersRates_modifies_bg,*parametersK_modifies_bg,f'SLCT{SLCn}_BG_io. q_m']
    outputs_bg = [f'SLCT{SLCn}_BG.v_Ao',f'SLCT{SLCn}_BG.v_Nao',f'SLCT{SLCn}_BG.v_Clo',*parameter_modifies_bg]
    
    parametersQ_modifies_ss = [f'SLCT{SLCn}_BG_ss_io.'+p for p in parametersQ]
    parameter_modifies_ss = [*parametersQ_modifies_ss,*parametersRates_modifies_bg,*parametersK_modifies_bg,f'SLCT{SLCn}_BG_ss_io. V_m']
    nparameters = len(parameter_modifies_bg)-1
    outputs_ss = [f'SLCT{SLCn}_ss.v_ss',f'SLCT{SLCn}_BG_ss.P_0', f'SLCT{SLCn}_BG_ss.P_1',*parameter_modifies_ss]

    parameter_values = [i+2 for i in range(nparameters)]
    nparametersK = int(len(parametersK)/2)
    for i in range(nparametersK):
        parameter_values[nparameters-nparametersK*2+2*i] = (i+2)*0.1
        parameter_values[nparameters-nparametersK*2+2*i+1] = (i+2)*0.1
    parameter_values.append(-0.01)  
    # simulate the models using the default parameters
    csv_fullpath_bg = PurePath(dir_path).joinpath(csv_bg_base + '.csv').as_posix()
    csv_fullpath_ss = PurePath(dir_path).joinpath(csv_ss_base + '.csv').as_posix()
    simCellML(py_fullpath_bg, csv_fullpath_bg, method, interval, step_size, result_step_size,[],[],outputs_bg)
    simCellML(py_fullpath_ss, csv_fullpath_ss, method, interval, step_size, result_step_size,[],[],outputs_ss)
    csv_fullpath_bg = PurePath(dir_path).joinpath(csv_bg_base + '_1'+'.csv').as_posix()
    csv_fullpath_ss = PurePath(dir_path).joinpath(csv_ss_base + '_1'+'.csv').as_posix()
    simCellML(py_fullpath_bg, csv_fullpath_bg, method, interval, step_size, result_step_size, parameter_modifies_bg, parameter_values, outputs_bg)
    simCellML(py_fullpath_ss, csv_fullpath_ss, method, interval, step_size, result_step_size, parameter_modifies_ss, parameter_values, outputs_ss)

def test_SLC14():
    SLCn='14'
    py_fullpath_bg = f'./SLCT{SLCn}/SLCT{SLCn}_BG_test.py'
    py_fullpath_ss = f'./SLCT{SLCn}/SLCT{SLCn}_BG_ss_test.py'
    csv_bg_base = PurePath(py_fullpath_bg).stem
    csv_ss_base = PurePath(py_fullpath_ss).stem
    dir_path = Path(py_fullpath_bg).parent.absolute()
    parametersQ = ['q_cAAi','q_cAAo','q_Nai','q_Nao','q_InAAi','q_InAAo']
    parametersRates = ['kappa_re1','kappa_re2']
    parametersK = ['K_cAAi','K_cAAo','K_Nai','K_Nao','K_InAAi','K_InAAo']
    parametersQ_modifies_bg = [f'SLCT{SLCn}_BG_io.'+p for p in parametersQ]
    parametersRates_modifies_bg = [f'SLCT{SLCn}_BG_param.'+p for p in parametersRates]
    parametersK_modifies_bg = [f'SLCT{SLCn}_BG_param.'+p for p in parametersK]
    parameter_modifies_bg = [*parametersQ_modifies_bg,*parametersRates_modifies_bg,*parametersK_modifies_bg,f'SLCT{SLCn}_BG_io. q_m']
    outputs_bg = [f'SLCT{SLCn}_BG.v_cAAo',f'SLCT{SLCn}_BG.v_Nao',f'SLCT{SLCn}_BG.v_InAAo',*parameter_modifies_bg]
    
    parametersQ_modifies_ss = [f'SLCT{SLCn}_BG_ss_io.'+p for p in parametersQ]
    parameter_modifies_ss = [*parametersQ_modifies_ss,*parametersRates_modifies_bg,*parametersK_modifies_bg,f'SLCT{SLCn}_BG_ss_io. V_m']
    nparameters = len(parameter_modifies_bg)-1
    outputs_ss = [f'SLCT{SLCn}_ss.v_ss',f'SLCT{SLCn}_BG_ss.P_0', f'SLCT{SLCn}_BG_ss.P_1',*parameter_modifies_ss]

    parameter_values = [i+2 for i in range(nparameters)]
    nparametersK = int(len(parametersK)/2)
    for i in range(nparametersK):
        parameter_values[nparameters-nparametersK*2+2*i] = (i+2)*0.1
        parameter_values[nparameters-nparametersK*2+2*i+1] = (i+2)*0.1
    parameter_values.append(-0.01)
      
    # simulate the models using the default parameters
    csv_fullpath_bg = PurePath(dir_path).joinpath(csv_bg_base + '.csv').as_posix()
    csv_fullpath_ss = PurePath(dir_path).joinpath(csv_ss_base + '.csv').as_posix()
    simCellML(py_fullpath_bg, csv_fullpath_bg, method, interval, step_size, result_step_size,[],[],outputs_bg)
    simCellML(py_fullpath_ss, csv_fullpath_ss, method, interval, step_size, result_step_size,[],[],outputs_ss)
    csv_fullpath_bg = PurePath(dir_path).joinpath(csv_bg_base + '_1'+'.csv').as_posix()
    csv_fullpath_ss = PurePath(dir_path).joinpath(csv_ss_base + '_1'+'.csv').as_posix()
    simCellML(py_fullpath_bg, csv_fullpath_bg, method, interval, step_size, result_step_size, parameter_modifies_bg, parameter_values, outputs_bg)
    simCellML(py_fullpath_ss, csv_fullpath_ss, method, interval, step_size, result_step_size, parameter_modifies_ss, parameter_values, outputs_ss)

def main():

    test_SLC6()

    

if __name__ == "__main__":
    main()