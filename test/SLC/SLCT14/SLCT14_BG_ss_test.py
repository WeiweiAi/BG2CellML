# The content of this file was generated using the Python profile of libCellML 0.4.0.

from enum import Enum
from math import *


__version__ = "0.4.0"
LIBCELLML_VERSION = "0.4.0"

VARIABLE_COUNT = 67


class VariableType(Enum):
    CONSTANT = 0
    COMPUTED_CONSTANT = 1
    ALGEBRAIC = 2


VARIABLE_INFO = [
    {"name": "v_ss", "units": "fmol_per_sec", "component": "SLCT14_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "q_InAAi", "units": "fmol", "component": "SLCT14_BG_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_Nai", "units": "fmol", "component": "SLCT14_BG_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_cAAo", "units": "fmol", "component": "SLCT14_BG_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_InAAo", "units": "fmol", "component": "SLCT14_BG_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_Nao", "units": "fmol", "component": "SLCT14_BG_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_cAAi", "units": "fmol", "component": "SLCT14_BG_ss_io", "type": VariableType.CONSTANT},
    {"name": "V_m", "units": "volt", "component": "SLCT14_BG_ss_io", "type": VariableType.CONSTANT},
    {"name": "F", "units": "C_per_mol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "R", "units": "J_per_K_per_mol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "T", "units": "kelvin", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "E", "units": "fmol", "component": "SLCT14_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_0", "units": "per_fmol3_sec8", "component": "SLCT14_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_1", "units": "per_fmol3_sec8", "component": "SLCT14_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_10", "units": "per_fmol2_sec7", "component": "SLCT14_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_9", "units": "per_fmol2_sec7", "component": "SLCT14_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_8", "units": "per_fmol2_sec7", "component": "SLCT14_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_7", "units": "per_fmol2_sec7", "component": "SLCT14_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_6", "units": "per_fmol2_sec7", "component": "SLCT14_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_5", "units": "per_fmol2_sec7", "component": "SLCT14_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_4", "units": "per_fmol2_sec7", "component": "SLCT14_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_3", "units": "per_fmol_sec7", "component": "SLCT14_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_23", "units": "per_fmol4_sec7", "component": "SLCT14_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_22", "units": "per_fmol4_sec7", "component": "SLCT14_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_21", "units": "per_fmol4_sec7", "component": "SLCT14_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_20", "units": "per_fmol3_sec7", "component": "SLCT14_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_2", "units": "per_fmol_sec7", "component": "SLCT14_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_19", "units": "per_fmol3_sec7", "component": "SLCT14_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_18", "units": "per_fmol3_sec7", "component": "SLCT14_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_17", "units": "per_fmol3_sec7", "component": "SLCT14_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_16", "units": "per_fmol3_sec7", "component": "SLCT14_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_15", "units": "per_fmol3_sec7", "component": "SLCT14_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_14", "units": "per_fmol3_sec7", "component": "SLCT14_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_13", "units": "per_fmol3_sec7", "component": "SLCT14_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_12", "units": "per_fmol2_sec7", "component": "SLCT14_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_11", "units": "per_fmol2_sec7", "component": "SLCT14_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "K_cAAo", "units": "per_fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_cAAi", "units": "per_fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_InAAo", "units": "per_fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_InAAi", "units": "per_fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_Nai", "units": "per_fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_Nao", "units": "per_fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_7", "units": "per_fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_7_init", "units": "fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_8", "units": "per_fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_8_init", "units": "fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_9", "units": "per_fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_9_init", "units": "fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_10", "units": "per_fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_10_init", "units": "fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_11", "units": "per_fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_11_init", "units": "fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_12", "units": "per_fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_12_init", "units": "fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_13", "units": "per_fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_13_init", "units": "fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_14", "units": "per_fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_14_init", "units": "fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "C_m", "units": "fF", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "kappa_re1", "units": "fmol_per_sec", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "kappa_re2", "units": "fmol_per_sec", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "kappa_re3", "units": "fmol_per_sec", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "kappa_re4", "units": "fmol_per_sec", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "kappa_re5", "units": "fmol_per_sec", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "kappa_re6", "units": "fmol_per_sec", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "kappa_re7", "units": "fmol_per_sec", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "kappa_re8", "units": "fmol_per_sec", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT}
]


def create_variables_array():
    return [nan]*VARIABLE_COUNT


def initialise_variables(variables):
    variables[1] = 1.0
    variables[2] = 1.0
    variables[3] = 1.0
    variables[4] = 1.0
    variables[5] = 1.0
    variables[6] = 1.0
    variables[7] = 1.0
    variables[8] = 96485.0
    variables[9] = 8.31
    variables[10] = 293.0
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
    variables[46] = 1.0
    variables[47] = 1.0
    variables[48] = 1.0
    variables[49] = 1.0
    variables[50] = 1.0
    variables[51] = 1.0
    variables[52] = 1.0
    variables[53] = 1.0
    variables[54] = 1.0
    variables[55] = 1.0
    variables[56] = 1.0
    variables[57] = 1.0
    variables[58] = 1.0
    variables[59] = 1.0
    variables[60] = 1.0
    variables[61] = 1.0
    variables[62] = 1.0
    variables[63] = 1.0
    variables[64] = 1.0
    variables[65] = 1.0
    variables[66] = 1.0


def compute_computed_constants(variables):
    variables[0] = variables[11]*(variables[12]*variables[4]*variables[5]*variables[6]*exp(variables[8]*variables[7]/(variables[9]*variables[10]))-variables[13]*variables[1]*variables[2]*variables[3])/(variables[14]*variables[4]*variables[5]*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[35]*variables[2]*variables[3]+variables[34]*variables[5]*variables[3]*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[33]*variables[1]*variables[2]*variables[3]+variables[32]*variables[4]*variables[5]*variables[6]*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[31]*variables[2]*variables[6]*variables[3]+variables[30]*variables[5]*variables[6]*variables[3]*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[29]*variables[1]*variables[4]*variables[5]*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[28]*variables[1]*variables[5]*variables[3]*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[27]*variables[1]*variables[4]*variables[2]+variables[26]*variables[6]+variables[25]*variables[4]*variables[2]*variables[6]+variables[24]*variables[1]*variables[4]*variables[2]*variables[5]*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[23]*variables[1]*variables[2]*variables[5]*variables[3]*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[22]*variables[4]*variables[2]*variables[5]*variables[6]*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[21]*variables[3]+variables[20]*variables[1]*variables[2]+variables[19]*variables[2]*variables[6]+variables[18]*variables[5]*variables[6]*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[17]*variables[6]*variables[3]+variables[16]*variables[1]*variables[3]+variables[15]*variables[4]*variables[6])
    variables[12] = variables[48]*variables[50]*variables[52]*variables[54]*variables[56]*variables[42]*variables[44]*variables[46]*variables[38]*variables[41]*variables[37]*variables[59]*variables[60]*variables[61]*variables[62]*variables[63]*variables[64]*variables[65]*variables[66]
    variables[13] = variables[48]*variables[50]*variables[52]*variables[54]*variables[56]*variables[42]*variables[44]*variables[46]*variables[39]*variables[40]*variables[36]*variables[59]*variables[60]*variables[61]*variables[62]*variables[63]*variables[64]*variables[65]*variables[66]
    variables[26] = variables[48]*variables[50]*variables[52]*variables[54]*variables[56]*variables[42]*variables[44]*variables[37]*variables[59]*variables[60]*variables[61]*variables[62]*variables[63]*variables[64]*variables[65]+variables[48]*variables[50]*variables[52]*variables[54]*variables[56]*variables[42]*variables[44]*variables[37]*variables[59]*variables[60]*variables[61]*variables[62]*variables[63]*variables[65]*variables[66]+variables[48]*variables[50]*variables[52]*variables[54]*variables[56]*variables[42]*variables[44]*variables[37]*variables[59]*variables[60]*variables[61]*variables[62]*variables[64]*variables[65]*variables[66]
    variables[21] = variables[50]*variables[52]*variables[54]*variables[56]*variables[42]*variables[44]*variables[46]*variables[36]*variables[59]*variables[60]*variables[61]*variables[62]*variables[63]*variables[64]*variables[65]+variables[50]*variables[52]*variables[54]*variables[56]*variables[42]*variables[44]*variables[46]*variables[36]*variables[59]*variables[60]*variables[61]*variables[62]*variables[63]*variables[65]*variables[66]+variables[50]*variables[52]*variables[54]*variables[56]*variables[42]*variables[44]*variables[46]*variables[36]*variables[59]*variables[60]*variables[61]*variables[62]*variables[64]*variables[65]*variables[66]
    variables[20] = variables[48]*variables[50]*variables[52]*variables[54]*variables[56]*variables[42]*variables[44]*variables[39]*variables[40]*variables[59]*variables[60]*variables[61]*variables[62]*variables[63]*variables[64]*variables[66]+variables[48]*variables[50]*variables[52]*variables[54]*variables[56]*variables[42]*variables[44]*variables[39]*variables[40]*variables[59]*variables[61]*variables[62]*variables[63]*variables[64]*variables[65]*variables[66]+variables[48]*variables[50]*variables[52]*variables[54]*variables[56]*variables[42]*variables[44]*variables[39]*variables[40]*variables[60]*variables[61]*variables[62]*variables[63]*variables[64]*variables[65]*variables[66]
    variables[19] = variables[48]*variables[50]*variables[52]*variables[54]*variables[56]*variables[42]*variables[44]*variables[40]*variables[37]*variables[59]*variables[60]*variables[61]*variables[63]*variables[64]*variables[65]*variables[66]
    variables[18] = variables[48]*variables[50]*variables[52]*variables[54]*variables[56]*variables[42]*variables[44]*variables[41]*variables[37]*variables[59]*variables[60]*variables[62]*variables[63]*variables[64]*variables[65]*variables[66]
    variables[17] = variables[48]*variables[50]*variables[52]*variables[54]*variables[56]*variables[42]*variables[46]*variables[37]*variables[36]*variables[59]*variables[60]*variables[61]*variables[62]*variables[63]*variables[64]*variables[65]+variables[48]*variables[50]*variables[52]*variables[54]*variables[56]*variables[42]*variables[46]*variables[37]*variables[36]*variables[59]*variables[60]*variables[61]*variables[62]*variables[63]*variables[65]*variables[66]+variables[48]*variables[50]*variables[52]*variables[54]*variables[56]*variables[42]*variables[46]*variables[37]*variables[36]*variables[59]*variables[60]*variables[61]*variables[62]*variables[64]*variables[65]*variables[66]+variables[48]*variables[50]*variables[52]*variables[54]*variables[56]*variables[44]*variables[46]*variables[37]*variables[36]*variables[59]*variables[60]*variables[61]*variables[62]*variables[63]*variables[64]*variables[65]+variables[48]*variables[50]*variables[52]*variables[54]*variables[56]*variables[44]*variables[46]*variables[37]*variables[36]*variables[59]*variables[60]*variables[61]*variables[62]*variables[63]*variables[65]*variables[66]+variables[48]*variables[50]*variables[52]*variables[54]*variables[56]*variables[44]*variables[46]*variables[37]*variables[36]*variables[59]*variables[60]*variables[61]*variables[62]*variables[64]*variables[65]*variables[66]
    variables[16] = variables[48]*variables[50]*variables[54]*variables[56]*variables[42]*variables[44]*variables[46]*variables[39]*variables[36]*variables[59]*variables[60]*variables[61]*variables[62]*variables[63]*variables[64]*variables[65]+variables[48]*variables[50]*variables[54]*variables[56]*variables[42]*variables[44]*variables[46]*variables[39]*variables[36]*variables[59]*variables[60]*variables[61]*variables[62]*variables[63]*variables[65]*variables[66]+variables[48]*variables[50]*variables[54]*variables[56]*variables[42]*variables[44]*variables[46]*variables[39]*variables[36]*variables[59]*variables[60]*variables[61]*variables[62]*variables[64]*variables[65]*variables[66]
    variables[15] = variables[48]*variables[52]*variables[54]*variables[56]*variables[42]*variables[44]*variables[46]*variables[38]*variables[37]*variables[59]*variables[60]*variables[61]*variables[62]*variables[63]*variables[64]*variables[65]+variables[48]*variables[52]*variables[54]*variables[56]*variables[42]*variables[44]*variables[46]*variables[38]*variables[37]*variables[59]*variables[60]*variables[61]*variables[62]*variables[63]*variables[65]*variables[66]+variables[48]*variables[52]*variables[54]*variables[56]*variables[42]*variables[44]*variables[46]*variables[38]*variables[37]*variables[59]*variables[60]*variables[61]*variables[62]*variables[64]*variables[65]*variables[66]
    variables[14] = variables[50]*variables[52]*variables[54]*variables[56]*variables[42]*variables[44]*variables[46]*variables[38]*variables[41]*variables[59]*variables[60]*variables[61]*variables[62]*variables[63]*variables[64]*variables[66]+variables[50]*variables[52]*variables[54]*variables[56]*variables[42]*variables[44]*variables[46]*variables[38]*variables[41]*variables[59]*variables[61]*variables[62]*variables[63]*variables[64]*variables[65]*variables[66]+variables[50]*variables[52]*variables[54]*variables[56]*variables[42]*variables[44]*variables[46]*variables[38]*variables[41]*variables[60]*variables[61]*variables[62]*variables[63]*variables[64]*variables[65]*variables[66]
    variables[35] = variables[50]*variables[52]*variables[54]*variables[56]*variables[42]*variables[44]*variables[46]*variables[40]*variables[36]*variables[59]*variables[60]*variables[61]*variables[63]*variables[64]*variables[65]*variables[66]
    variables[34] = variables[50]*variables[52]*variables[54]*variables[56]*variables[42]*variables[44]*variables[46]*variables[41]*variables[36]*variables[59]*variables[60]*variables[62]*variables[63]*variables[64]*variables[65]*variables[66]
    variables[33] = variables[48]*variables[50]*variables[52]*variables[54]*variables[56]*variables[42]*variables[46]*variables[39]*variables[40]*variables[36]*variables[59]*variables[61]*variables[62]*variables[63]*variables[64]*variables[65]*variables[66]+variables[48]*variables[50]*variables[52]*variables[54]*variables[56]*variables[44]*variables[46]*variables[39]*variables[40]*variables[36]*variables[59]*variables[60]*variables[61]*variables[62]*variables[63]*variables[64]*variables[66]+variables[48]*variables[50]*variables[52]*variables[54]*variables[56]*variables[44]*variables[46]*variables[39]*variables[40]*variables[36]*variables[59]*variables[61]*variables[62]*variables[63]*variables[64]*variables[65]*variables[66]+variables[48]*variables[50]*variables[52]*variables[54]*variables[42]*variables[44]*variables[46]*variables[39]*variables[40]*variables[36]*variables[59]*variables[60]*variables[61]*variables[62]*variables[63]*variables[64]*variables[65]+variables[48]*variables[50]*variables[52]*variables[54]*variables[42]*variables[44]*variables[46]*variables[39]*variables[40]*variables[36]*variables[59]*variables[60]*variables[61]*variables[62]*variables[64]*variables[65]*variables[66]+variables[48]*variables[50]*variables[52]*variables[56]*variables[42]*variables[44]*variables[46]*variables[39]*variables[40]*variables[36]*variables[59]*variables[60]*variables[61]*variables[62]*variables[64]*variables[65]*variables[66]+variables[48]*variables[52]*variables[54]*variables[56]*variables[42]*variables[44]*variables[46]*variables[39]*variables[40]*variables[36]*variables[59]*variables[60]*variables[62]*variables[63]*variables[64]*variables[65]*variables[66]
    variables[32] = variables[48]*variables[50]*variables[52]*variables[54]*variables[56]*variables[42]*variables[46]*variables[38]*variables[41]*variables[37]*variables[59]*variables[60]*variables[61]*variables[62]*variables[63]*variables[64]*variables[66]+variables[48]*variables[50]*variables[52]*variables[54]*variables[56]*variables[42]*variables[46]*variables[38]*variables[41]*variables[37]*variables[60]*variables[61]*variables[62]*variables[63]*variables[64]*variables[65]*variables[66]+variables[48]*variables[50]*variables[52]*variables[54]*variables[56]*variables[44]*variables[46]*variables[38]*variables[41]*variables[37]*variables[60]*variables[61]*variables[62]*variables[63]*variables[64]*variables[65]*variables[66]+variables[48]*variables[50]*variables[52]*variables[54]*variables[42]*variables[44]*variables[46]*variables[38]*variables[41]*variables[37]*variables[59]*variables[60]*variables[61]*variables[62]*variables[63]*variables[65]*variables[66]+variables[48]*variables[50]*variables[52]*variables[56]*variables[42]*variables[44]*variables[46]*variables[38]*variables[41]*variables[37]*variables[59]*variables[60]*variables[61]*variables[62]*variables[63]*variables[64]*variables[65]+variables[48]*variables[50]*variables[52]*variables[56]*variables[42]*variables[44]*variables[46]*variables[38]*variables[41]*variables[37]*variables[59]*variables[60]*variables[61]*variables[62]*variables[63]*variables[65]*variables[66]+variables[48]*variables[50]*variables[54]*variables[56]*variables[42]*variables[44]*variables[46]*variables[38]*variables[41]*variables[37]*variables[59]*variables[60]*variables[61]*variables[63]*variables[64]*variables[65]*variables[66]
    variables[31] = variables[48]*variables[50]*variables[52]*variables[54]*variables[56]*variables[42]*variables[46]*variables[40]*variables[37]*variables[36]*variables[59]*variables[60]*variables[61]*variables[63]*variables[64]*variables[65]*variables[66]+variables[48]*variables[50]*variables[52]*variables[54]*variables[56]*variables[44]*variables[46]*variables[40]*variables[37]*variables[36]*variables[59]*variables[60]*variables[61]*variables[63]*variables[64]*variables[65]*variables[66]
    variables[30] = variables[48]*variables[50]*variables[52]*variables[54]*variables[56]*variables[42]*variables[46]*variables[41]*variables[37]*variables[36]*variables[59]*variables[60]*variables[62]*variables[63]*variables[64]*variables[65]*variables[66]+variables[48]*variables[50]*variables[52]*variables[54]*variables[56]*variables[44]*variables[46]*variables[41]*variables[37]*variables[36]*variables[59]*variables[60]*variables[62]*variables[63]*variables[64]*variables[65]*variables[66]
    variables[29] = variables[48]*variables[50]*variables[54]*variables[56]*variables[42]*variables[44]*variables[46]*variables[39]*variables[38]*variables[41]*variables[59]*variables[60]*variables[61]*variables[62]*variables[63]*variables[64]*variables[66]+variables[48]*variables[50]*variables[54]*variables[56]*variables[42]*variables[44]*variables[46]*variables[39]*variables[38]*variables[41]*variables[59]*variables[61]*variables[62]*variables[63]*variables[64]*variables[65]*variables[66]+variables[48]*variables[50]*variables[54]*variables[56]*variables[42]*variables[44]*variables[46]*variables[39]*variables[38]*variables[41]*variables[60]*variables[61]*variables[62]*variables[63]*variables[64]*variables[65]*variables[66]
    variables[28] = variables[48]*variables[50]*variables[54]*variables[56]*variables[42]*variables[44]*variables[46]*variables[39]*variables[41]*variables[36]*variables[59]*variables[60]*variables[62]*variables[63]*variables[64]*variables[65]*variables[66]
    variables[27] = variables[48]*variables[52]*variables[54]*variables[56]*variables[42]*variables[44]*variables[46]*variables[39]*variables[38]*variables[40]*variables[59]*variables[60]*variables[61]*variables[62]*variables[63]*variables[64]*variables[66]+variables[48]*variables[52]*variables[54]*variables[56]*variables[42]*variables[44]*variables[46]*variables[39]*variables[38]*variables[40]*variables[59]*variables[61]*variables[62]*variables[63]*variables[64]*variables[65]*variables[66]+variables[48]*variables[52]*variables[54]*variables[56]*variables[42]*variables[44]*variables[46]*variables[39]*variables[38]*variables[40]*variables[60]*variables[61]*variables[62]*variables[63]*variables[64]*variables[65]*variables[66]
    variables[25] = variables[48]*variables[52]*variables[54]*variables[56]*variables[42]*variables[44]*variables[46]*variables[38]*variables[40]*variables[37]*variables[59]*variables[60]*variables[61]*variables[63]*variables[64]*variables[65]*variables[66]
    variables[24] = variables[48]*variables[50]*variables[52]*variables[54]*variables[42]*variables[44]*variables[46]*variables[39]*variables[38]*variables[40]*variables[41]*variables[59]*variables[60]*variables[61]*variables[62]*variables[63]*variables[64]*variables[66]+variables[48]*variables[50]*variables[52]*variables[54]*variables[42]*variables[44]*variables[46]*variables[39]*variables[38]*variables[40]*variables[41]*variables[59]*variables[61]*variables[62]*variables[63]*variables[64]*variables[65]*variables[66]+variables[48]*variables[50]*variables[52]*variables[54]*variables[42]*variables[44]*variables[46]*variables[39]*variables[38]*variables[40]*variables[41]*variables[60]*variables[61]*variables[62]*variables[63]*variables[64]*variables[65]*variables[66]+variables[48]*variables[50]*variables[52]*variables[56]*variables[42]*variables[44]*variables[46]*variables[39]*variables[38]*variables[40]*variables[41]*variables[59]*variables[60]*variables[61]*variables[62]*variables[63]*variables[64]*variables[66]+variables[48]*variables[50]*variables[52]*variables[56]*variables[42]*variables[44]*variables[46]*variables[39]*variables[38]*variables[40]*variables[41]*variables[59]*variables[61]*variables[62]*variables[63]*variables[64]*variables[65]*variables[66]+variables[48]*variables[50]*variables[52]*variables[56]*variables[42]*variables[44]*variables[46]*variables[39]*variables[38]*variables[40]*variables[41]*variables[60]*variables[61]*variables[62]*variables[63]*variables[64]*variables[65]*variables[66]
    variables[23] = variables[48]*variables[50]*variables[52]*variables[54]*variables[42]*variables[44]*variables[46]*variables[39]*variables[40]*variables[41]*variables[36]*variables[59]*variables[60]*variables[62]*variables[63]*variables[64]*variables[65]*variables[66]+variables[48]*variables[50]*variables[52]*variables[56]*variables[42]*variables[44]*variables[46]*variables[39]*variables[40]*variables[41]*variables[36]*variables[59]*variables[60]*variables[62]*variables[63]*variables[64]*variables[65]*variables[66]
    variables[22] = variables[48]*variables[50]*variables[52]*variables[54]*variables[42]*variables[44]*variables[46]*variables[38]*variables[40]*variables[41]*variables[37]*variables[59]*variables[60]*variables[61]*variables[63]*variables[64]*variables[65]*variables[66]+variables[48]*variables[50]*variables[52]*variables[56]*variables[42]*variables[44]*variables[46]*variables[38]*variables[40]*variables[41]*variables[37]*variables[59]*variables[60]*variables[61]*variables[63]*variables[64]*variables[65]*variables[66]
    variables[11] = variables[49]+variables[51]+variables[53]+variables[55]+variables[57]+variables[43]+variables[45]+variables[47]


def compute_variables(variables):
    pass
