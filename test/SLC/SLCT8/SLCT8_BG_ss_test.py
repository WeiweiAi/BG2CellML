# The content of this file was generated using the Python profile of libCellML 0.4.0.

from enum import Enum
from math import *


__version__ = "0.4.0"
LIBCELLML_VERSION = "0.4.0"

VARIABLE_COUNT = 46


class VariableType(Enum):
    CONSTANT = 0
    COMPUTED_CONSTANT = 1
    ALGEBRAIC = 2


VARIABLE_INFO = [
    {"name": "v_ss", "units": "fmol_per_sec", "component": "SLCT8_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "q_Gluo", "units": "fmol", "component": "SLCT8_BG_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_Nao", "units": "fmol", "component": "SLCT8_BG_ss_io", "type": VariableType.CONSTANT},
    {"name": "V_m", "units": "volt", "component": "SLCT8_BG_ss_io", "type": VariableType.CONSTANT},
    {"name": "F", "units": "C_per_mol", "component": "SLCT8_BG_param", "type": VariableType.CONSTANT},
    {"name": "R", "units": "J_per_K_per_mol", "component": "SLCT8_BG_param", "type": VariableType.CONSTANT},
    {"name": "T", "units": "kelvin", "component": "SLCT8_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_Glui", "units": "fmol", "component": "SLCT8_BG_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_Nai", "units": "fmol", "component": "SLCT8_BG_ss_io", "type": VariableType.CONSTANT},
    {"name": "E", "units": "fmol", "component": "SLCT8_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_0", "units": "per_fmol3_sec7", "component": "SLCT8_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_1", "units": "per_fmol3_sec7", "component": "SLCT8_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_10", "units": "per_fmol3_sec6", "component": "SLCT8_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_9", "units": "per_fmol2_sec6", "component": "SLCT8_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_8", "units": "per_fmol3_sec6", "component": "SLCT8_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_7", "units": "per_fmol3_sec6", "component": "SLCT8_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_6", "units": "per_fmol3_sec6", "component": "SLCT8_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_5", "units": "per_fmol3_sec6", "component": "SLCT8_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_4", "units": "per_fmol2_sec6", "component": "SLCT8_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_3", "units": "per_fmol_sec6", "component": "SLCT8_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_2", "units": "per_fmol_sec6", "component": "SLCT8_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_11", "units": "per_fmol5_sec6", "component": "SLCT8_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "K_Nao", "units": "per_fmol", "component": "SLCT8_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_Nai", "units": "per_fmol", "component": "SLCT8_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_Gluo", "units": "per_fmol", "component": "SLCT8_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_Glui", "units": "per_fmol", "component": "SLCT8_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_5", "units": "per_fmol", "component": "SLCT8_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_5_init", "units": "fmol", "component": "SLCT8_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_6", "units": "per_fmol", "component": "SLCT8_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_6_init", "units": "fmol", "component": "SLCT8_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_7", "units": "per_fmol", "component": "SLCT8_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_7_init", "units": "fmol", "component": "SLCT8_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_8", "units": "per_fmol", "component": "SLCT8_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_8_init", "units": "fmol", "component": "SLCT8_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_9", "units": "per_fmol", "component": "SLCT8_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_9_init", "units": "fmol", "component": "SLCT8_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_10", "units": "per_fmol", "component": "SLCT8_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_10_init", "units": "fmol", "component": "SLCT8_BG_param", "type": VariableType.CONSTANT},
    {"name": "C_m", "units": "fF", "component": "SLCT8_BG_param", "type": VariableType.CONSTANT},
    {"name": "kappa_re1", "units": "fmol_per_sec", "component": "SLCT8_BG_param", "type": VariableType.CONSTANT},
    {"name": "kappa_re2", "units": "fmol_per_sec", "component": "SLCT8_BG_param", "type": VariableType.CONSTANT},
    {"name": "kappa_re3", "units": "fmol_per_sec", "component": "SLCT8_BG_param", "type": VariableType.CONSTANT},
    {"name": "kappa_re4", "units": "fmol_per_sec", "component": "SLCT8_BG_param", "type": VariableType.CONSTANT},
    {"name": "kappa_re5", "units": "fmol_per_sec", "component": "SLCT8_BG_param", "type": VariableType.CONSTANT},
    {"name": "kappa_re6", "units": "fmol_per_sec", "component": "SLCT8_BG_param", "type": VariableType.CONSTANT},
    {"name": "kappa_re7", "units": "fmol_per_sec", "component": "SLCT8_BG_param", "type": VariableType.CONSTANT}
]


def create_variables_array():
    return [nan]*VARIABLE_COUNT


def initialise_variables(variables):
    variables[1] = 1.0
    variables[2] = 1.0
    variables[3] = 1.0
    variables[4] = 96485.0
    variables[5] = 8.31
    variables[6] = 293.0
    variables[7] = 1.0
    variables[8] = 1.0
    variables[22] = 1.0
    variables[23] = 1.0
    variables[24] = 1.0
    variables[25] = 1.0
    variables[26] = 1.0
    variables[27] = 1.0
    variables[28] = 1.0
    variables[29] = 1.0
    variables[30] = 1.0
    variables[31] = 1.0
    variables[32] = 1.0
    variables[33] = 1.0
    variables[34] = 1.0
    variables[35] = 1.0
    variables[36] = 1.0
    variables[37] = 1.0
    variables[38] = 1.0
    variables[39] = 1.0
    variables[40] = 1.0
    variables[41] = 1.0
    variables[42] = 1.0
    variables[43] = 1.0
    variables[44] = 1.0
    variables[45] = 1.0


def compute_computed_constants(variables):
    variables[0] = variables[9]*(variables[10]*variables[1]*pow(variables[2], 2.0)-variables[11]*variables[7]*pow(variables[8], 2.0))*exp(2.0*variables[4]*variables[3]/(variables[5]*variables[6]))/(variables[12]*variables[7]*pow(variables[2], 2.0)*exp(2.0*variables[4]*variables[3]/(variables[5]*variables[6]))+variables[21]*variables[7]*pow(variables[8], 2.0)*pow(variables[2], 2.0)*exp(variables[4]*variables[3]/(variables[5]*variables[6]))+variables[20]*variables[7]*exp(variables[4]*variables[3]/(variables[5]*variables[6]))+variables[19]*variables[7]*exp(2.0*variables[4]*variables[3]/(variables[5]*variables[6]))+variables[18]*pow(variables[2], 2.0)*exp(2.0*variables[4]*variables[3]/(variables[5]*variables[6]))+variables[17]*variables[7]*pow(variables[8], 2.0)*exp(2.0*variables[4]*variables[3]/(variables[5]*variables[6]))+variables[16]*variables[1]*pow(variables[2], 2.0)*exp(2.0*variables[4]*variables[3]/(variables[5]*variables[6]))+variables[15]*variables[7]*pow(variables[2], 2.0)*exp(variables[4]*variables[3]/(variables[5]*variables[6]))+variables[14]*variables[7]*pow(variables[8], 2.0)*exp(variables[4]*variables[3]/(variables[5]*variables[6]))+variables[13]*pow(variables[8], 2.0)*exp(2.0*variables[4]*variables[3]/(variables[5]*variables[6])))
    variables[10] = variables[36]*variables[26]*variables[28]*variables[30]*pow(variables[32], 2.0)*variables[34]*variables[24]*pow(variables[22], 2.0)*variables[39]*variables[40]*variables[41]*variables[42]*variables[43]*variables[44]*variables[45]
    variables[11] = variables[36]*variables[26]*variables[28]*pow(variables[30], 2.0)*variables[32]*variables[34]*variables[25]*pow(variables[23], 2.0)*variables[39]*variables[40]*variables[41]*variables[42]*variables[43]*variables[44]*variables[45]
    variables[20] = variables[36]*variables[26]*variables[30]*pow(variables[32], 2.0)*variables[34]*variables[25]*variables[40]*variables[41]*variables[42]*variables[43]*variables[44]*variables[45]+variables[36]*variables[28]*variables[30]*pow(variables[32], 2.0)*variables[34]*variables[25]*variables[40]*variables[41]*variables[42]*variables[43]*variables[44]*variables[45]
    variables[19] = variables[36]*variables[26]*pow(variables[30], 2.0)*variables[32]*variables[34]*variables[25]*variables[39]*variables[41]*variables[42]*variables[43]*variables[44]*variables[45]+variables[36]*variables[28]*pow(variables[30], 2.0)*variables[32]*variables[34]*variables[25]*variables[39]*variables[41]*variables[42]*variables[43]*variables[44]*variables[45]
    variables[18] = variables[36]*variables[26]*variables[28]*variables[30]*variables[32]*variables[34]*pow(variables[22], 2.0)*variables[39]*variables[40]*variables[41]*variables[42]*variables[43]*variables[44]+variables[36]*variables[26]*variables[28]*variables[30]*variables[32]*variables[34]*pow(variables[22], 2.0)*variables[39]*variables[40]*variables[41]*variables[43]*variables[44]*variables[45]+variables[36]*variables[26]*variables[28]*variables[30]*variables[32]*variables[34]*pow(variables[22], 2.0)*variables[39]*variables[40]*variables[42]*variables[43]*variables[44]*variables[45]
    variables[17] = variables[36]*variables[26]*variables[28]*variables[30]*pow(variables[32], 2.0)*variables[25]*pow(variables[23], 2.0)*variables[39]*variables[40]*variables[42]*variables[43]*variables[44]*variables[45]+6.0*variables[36]*variables[26]*variables[28]*variables[30]*variables[32]*variables[34]*variables[25]*pow(variables[23], 2.0)*variables[39]*variables[40]*variables[41]*variables[42]*variables[43]*variables[45]+variables[26]*variables[28]*variables[30]*pow(variables[32], 2.0)*variables[34]*variables[25]*pow(variables[23], 2.0)*variables[39]*variables[40]*variables[41]*variables[42]*variables[43]*variables[44]+variables[26]*variables[28]*variables[30]*pow(variables[32], 2.0)*variables[34]*variables[25]*pow(variables[23], 2.0)*variables[39]*variables[40]*variables[42]*variables[43]*variables[44]*variables[45]
    variables[16] = variables[36]*variables[26]*variables[28]*pow(variables[30], 2.0)*variables[32]*variables[24]*pow(variables[22], 2.0)*variables[39]*variables[40]*variables[41]*variables[42]*variables[43]*variables[44]+variables[36]*variables[26]*variables[28]*pow(variables[30], 2.0)*variables[32]*variables[24]*pow(variables[22], 2.0)*variables[39]*variables[40]*variables[41]*variables[43]*variables[44]*variables[45]+variables[26]*variables[28]*pow(variables[30], 2.0)*variables[32]*variables[34]*variables[24]*pow(variables[22], 2.0)*variables[39]*variables[40]*variables[41]*variables[43]*variables[44]*variables[45]
    variables[15] = variables[36]*variables[26]*variables[30]*pow(variables[32], 2.0)*variables[34]*variables[25]*pow(variables[22], 2.0)*variables[39]*variables[40]*variables[41]*variables[42]*variables[44]*variables[45]
    variables[14] = 4.0*variables[36]*variables[26]*variables[28]*variables[30]*variables[32]*variables[34]*variables[25]*pow(variables[23], 2.0)*variables[40]*variables[41]*variables[42]*variables[43]*variables[44]*variables[45]+variables[36]*variables[28]*pow(variables[30], 2.0)*variables[32]*variables[34]*variables[25]*pow(variables[23], 2.0)*variables[39]*variables[40]*variables[41]*variables[42]*variables[44]*variables[45]
    variables[13] = 3.0*variables[36]*variables[26]*variables[28]*variables[30]*variables[32]*variables[34]*pow(variables[23], 2.0)*variables[39]*variables[40]*variables[41]*variables[42]*variables[43]*variables[44]+3.0*variables[36]*variables[26]*variables[28]*variables[30]*variables[32]*variables[34]*pow(variables[23], 2.0)*variables[39]*variables[40]*variables[41]*variables[43]*variables[44]*variables[45]+3.0*variables[36]*variables[26]*variables[28]*variables[30]*variables[32]*variables[34]*pow(variables[23], 2.0)*variables[39]*variables[40]*variables[42]*variables[43]*variables[44]*variables[45]
    variables[12] = 4.0*variables[36]*variables[26]*variables[28]*variables[30]*variables[32]*variables[34]*variables[25]*pow(variables[22], 2.0)*variables[39]*variables[41]*variables[42]*variables[43]*variables[44]*variables[45]
    variables[21] = 4.0*variables[36]*variables[26]*variables[28]*variables[30]*variables[32]*variables[34]*variables[25]*pow(variables[23], 2.0)*pow(variables[22], 2.0)*variables[39]*variables[40]*variables[41]*variables[42]*variables[44]*variables[45]
    variables[9] = variables[37]+variables[27]+variables[29]+variables[31]+variables[33]+variables[35]


def compute_variables(variables):
    pass
