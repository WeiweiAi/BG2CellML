# The content of this file was generated using the Python profile of libCellML 0.4.0.

from enum import Enum
from math import *


__version__ = "0.4.0"
LIBCELLML_VERSION = "0.4.0"

VARIABLE_COUNT = 89


class VariableType(Enum):
    CONSTANT = 0
    COMPUTED_CONSTANT = 1
    ALGEBRAIC = 2


VARIABLE_INFO = [
    {"name": "v_ss", "units": "fmol_per_sec", "component": "SLCT13_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "q_Ai", "units": "fmol", "component": "SLCT13_BG_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_Cli", "units": "fmol", "component": "SLCT13_BG_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_Nai", "units": "fmol", "component": "SLCT13_BG_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_Ao", "units": "fmol", "component": "SLCT13_BG_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_Clo", "units": "fmol", "component": "SLCT13_BG_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_Nao", "units": "fmol", "component": "SLCT13_BG_ss_io", "type": VariableType.CONSTANT},
    {"name": "V_m", "units": "volt", "component": "SLCT13_BG_ss_io", "type": VariableType.CONSTANT},
    {"name": "F", "units": "C_per_mol", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "R", "units": "J_per_K_per_mol", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "T", "units": "kelvin", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "E", "units": "fmol", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_0", "units": "per_fmol4_sec8", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_1", "units": "per_fmol4_sec8", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_10", "units": "per_fmol3_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_9", "units": "per_fmol3_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_8", "units": "per_fmol_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_7", "units": "per_fmol_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_6", "units": "per_fmol2_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_5", "units": "per_fmol2_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_45", "units": "per_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_44", "units": "per_fmol8_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_43", "units": "per_fmol8_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_42", "units": "per_fmol7_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_41", "units": "per_fmol6_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_40", "units": "per_fmol6_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_4", "units": "per_fmol2_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_39", "units": "per_fmol6_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_38", "units": "per_fmol6_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_37", "units": "per_fmol7_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_36", "units": "per_fmol5_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_35", "units": "per_fmol5_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_34", "units": "per_fmol5_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_33", "units": "per_fmol5_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_32", "units": "per_fmol5_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_31", "units": "per_fmol5_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_30", "units": "per_fmol6_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_3", "units": "per_fmol2_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_29", "units": "per_fmol6_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_28", "units": "per_fmol5_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_27", "units": "per_fmol5_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_26", "units": "per_fmol4_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_25", "units": "per_fmol4_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_24", "units": "per_fmol4_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_23", "units": "per_fmol4_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_22", "units": "per_fmol4_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_21", "units": "per_fmol4_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_20", "units": "per_fmol4_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_2", "units": "per_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_19", "units": "per_fmol4_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_18", "units": "per_fmol3_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_17", "units": "per_fmol3_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_16", "units": "per_fmol2_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_15", "units": "per_fmol2_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_14", "units": "per_fmol3_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_13", "units": "per_fmol3_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_12", "units": "per_fmol3_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_11", "units": "per_fmol3_sec7", "component": "SLCT13_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "K_Nao", "units": "per_fmol", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_Nai", "units": "per_fmol", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_Ao", "units": "per_fmol", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_Ai", "units": "per_fmol", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_Cli", "units": "per_fmol", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_Clo", "units": "per_fmol", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_7", "units": "per_fmol", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_7_init", "units": "fmol", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_8", "units": "per_fmol", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_8_init", "units": "fmol", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_9", "units": "per_fmol", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_9_init", "units": "fmol", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_10", "units": "per_fmol", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_10_init", "units": "fmol", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_11", "units": "per_fmol", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_11_init", "units": "fmol", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_12", "units": "per_fmol", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_12_init", "units": "fmol", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_13", "units": "per_fmol", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_13_init", "units": "fmol", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_14", "units": "per_fmol", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_14_init", "units": "fmol", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "C_m", "units": "fF", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "kappa_re1", "units": "fmol_per_sec", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "kappa_re2", "units": "fmol_per_sec", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "kappa_re3", "units": "fmol_per_sec", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "kappa_re4", "units": "fmol_per_sec", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "kappa_re5", "units": "fmol_per_sec", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "kappa_re6", "units": "fmol_per_sec", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "kappa_re7", "units": "fmol_per_sec", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT},
    {"name": "kappa_re8", "units": "fmol_per_sec", "component": "SLCT13_BG_param", "type": VariableType.CONSTANT}
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
    variables[58] = 1.0
    variables[59] = 1.0
    variables[60] = 1.0
    variables[61] = 1.0
    variables[62] = 1.0
    variables[63] = 1.0
    variables[64] = 1.0
    variables[65] = 1.0
    variables[66] = 1.0
    variables[67] = 1.0
    variables[68] = 1.0
    variables[69] = 1.0
    variables[70] = 1.0
    variables[71] = 1.0
    variables[72] = 1.0
    variables[73] = 1.0
    variables[74] = 1.0
    variables[75] = 1.0
    variables[76] = 1.0
    variables[77] = 1.0
    variables[78] = 1.0
    variables[79] = 1.0
    variables[80] = 1.0
    variables[81] = 1.0
    variables[82] = 1.0
    variables[83] = 1.0
    variables[84] = 1.0
    variables[85] = 1.0
    variables[86] = 1.0
    variables[87] = 1.0
    variables[88] = 1.0


def compute_computed_constants(variables):
    variables[0] = variables[11]*(variables[12]*variables[4]*variables[5]*pow(variables[6], 2.0)*exp(variables[8]*variables[7]/(variables[9]*variables[10]))-variables[13]*variables[1]*variables[2]*pow(variables[3], 2.0))/(variables[14]*variables[5]*pow(variables[6], 2.0)*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[57]*variables[1]*pow(variables[3], 2.0)+variables[56]*variables[4]*pow(variables[3], 2.0)*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[55]*variables[1]*pow(variables[6], 2.0)+variables[54]*variables[4]*pow(variables[6], 2.0)*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[53]*variables[1]*variables[2]+variables[52]*variables[4]*variables[5]*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[51]*variables[2]*pow(variables[3], 2.0)+variables[50]*variables[2]*pow(variables[3], 2.0)*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[49]*variables[1]*variables[2]*pow(variables[3], 2.0)+variables[48]*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[47]*variables[1]*variables[5]*pow(variables[6], 2.0)+variables[46]*variables[4]*variables[5]*pow(variables[6], 2.0)*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[45]*variables[4]*variables[5]*pow(variables[3], 2.0)*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[44]*variables[1]*variables[2]*pow(variables[6], 2.0)+variables[43]*variables[1]*variables[2]*pow(variables[3], 2.0)*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[42]*variables[4]*variables[5]*pow(variables[6], 2.0)+variables[41]*variables[4]*variables[2]*pow(variables[3], 2.0)*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[40]*variables[1]*variables[2]*variables[5]*pow(variables[6], 2.0)+variables[39]*variables[1]*variables[2]*variables[5]*pow(variables[3], 2.0)+variables[38]*variables[4]*variables[5]*pow(variables[3], 2.0)*pow(variables[6], 2.0)*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[37]*pow(variables[3], 2.0)+variables[36]*variables[1]*variables[2]*pow(variables[3], 2.0)*pow(variables[6], 2.0)+variables[35]*variables[1]*variables[4]*variables[2]*pow(variables[3], 2.0)*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[34]*variables[1]*variables[4]*variables[5]*pow(variables[6], 2.0)*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[33]*variables[1]*variables[4]*variables[2]*pow(variables[3], 2.0)+variables[32]*variables[1]*variables[4]*variables[5]*pow(variables[6], 2.0)+variables[31]*variables[4]*variables[2]*variables[5]*pow(variables[6], 2.0)*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[30]*variables[4]*variables[2]*variables[5]*pow(variables[3], 2.0)*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[29]*variables[1]*variables[2]*variables[5]*pow(variables[3], 2.0)*pow(variables[6], 2.0)+variables[28]*variables[1]*variables[4]*variables[2]*variables[5]*pow(variables[6], 2.0)*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[27]*variables[1]*variables[4]*variables[2]*variables[5]*pow(variables[3], 2.0)*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[26]*pow(variables[3], 2.0)*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[25]*variables[1]*variables[4]*variables[2]*variables[5]*pow(variables[6], 2.0)+variables[24]*variables[1]*variables[4]*variables[2]*variables[5]*pow(variables[3], 2.0)+variables[23]*variables[4]*variables[2]*variables[5]*pow(variables[3], 2.0)*pow(variables[6], 2.0)*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[22]*variables[1]*variables[4]*variables[2]*variables[5]*pow(variables[3], 2.0)*pow(variables[6], 2.0)*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[21]*variables[1]*variables[4]*variables[2]*variables[5]*pow(variables[3], 2.0)*pow(variables[6], 2.0)+variables[20]+variables[19]*pow(variables[6], 2.0)+variables[18]*pow(variables[6], 2.0)*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[17]*variables[1]+variables[16]*variables[4]*exp(variables[8]*variables[7]/(variables[9]*variables[10]))+variables[15]*variables[5]*pow(variables[6], 2.0))
    variables[12] = variables[70]*variables[72]*variables[74]*variables[76]*variables[78]*variables[64]*variables[66]*variables[68]*variables[60]*variables[63]*pow(variables[58], 2.0)*variables[81]*variables[82]*variables[83]*variables[84]*variables[85]*variables[86]*variables[87]*variables[88]
    variables[13] = variables[70]*variables[72]*variables[74]*variables[76]*variables[78]*variables[64]*variables[66]*variables[68]*variables[61]*variables[62]*pow(variables[59], 2.0)*variables[81]*variables[82]*variables[83]*variables[84]*variables[85]*variables[86]*variables[87]*variables[88]
    variables[48] = variables[70]*variables[72]*variables[74]*variables[76]*variables[64]*variables[66]*variables[68]*variables[81]*variables[82]*variables[83]*variables[84]*variables[86]*variables[87]*variables[88]+variables[70]*variables[72]*variables[74]*variables[78]*variables[64]*variables[66]*variables[68]*variables[81]*variables[82]*variables[83]*variables[84]*variables[86]*variables[87]*variables[88]
    variables[37] = variables[70]*variables[72]*variables[74]*variables[76]*variables[78]*variables[64]*variables[68]*pow(variables[59], 2.0)*variables[81]*variables[82]*variables[83]*variables[84]*variables[85]*variables[86]*variables[88]+variables[70]*variables[72]*variables[74]*variables[76]*variables[78]*variables[64]*variables[68]*pow(variables[59], 2.0)*variables[81]*variables[82]*variables[83]*variables[84]*variables[85]*variables[87]*variables[88]
    variables[26] = variables[70]*variables[72]*variables[74]*variables[76]*variables[78]*variables[64]*variables[68]*pow(variables[59], 2.0)*variables[81]*variables[82]*variables[83]*variables[84]*variables[86]*variables[87]*variables[88]
    variables[19] = variables[70]*variables[72]*variables[74]*variables[76]*variables[78]*variables[66]*variables[68]*pow(variables[58], 2.0)*variables[81]*variables[82]*variables[83]*variables[84]*variables[85]*variables[86]*variables[88]+variables[70]*variables[72]*variables[74]*variables[76]*variables[78]*variables[66]*variables[68]*pow(variables[58], 2.0)*variables[81]*variables[82]*variables[83]*variables[84]*variables[85]*variables[87]*variables[88]
    variables[18] = variables[70]*variables[72]*variables[74]*variables[76]*variables[78]*variables[66]*variables[68]*pow(variables[58], 2.0)*variables[81]*variables[82]*variables[83]*variables[84]*variables[86]*variables[87]*variables[88]
    variables[17] = variables[70]*variables[72]*variables[74]*variables[76]*variables[64]*variables[66]*variables[68]*variables[61]*variables[81]*variables[82]*variables[83]*variables[85]*variables[86]*variables[87]*variables[88]+variables[70]*variables[72]*variables[74]*variables[78]*variables[64]*variables[66]*variables[68]*variables[61]*variables[81]*variables[82]*variables[83]*variables[85]*variables[86]*variables[87]*variables[88]
    variables[16] = variables[70]*variables[72]*variables[74]*variables[76]*variables[64]*variables[66]*variables[68]*variables[60]*variables[81]*variables[82]*variables[84]*variables[85]*variables[86]*variables[87]*variables[88]+variables[70]*variables[72]*variables[74]*variables[78]*variables[64]*variables[66]*variables[68]*variables[60]*variables[81]*variables[82]*variables[84]*variables[85]*variables[86]*variables[87]*variables[88]
    variables[15] = variables[70]*variables[72]*variables[74]*variables[76]*variables[78]*variables[64]*variables[66]*variables[63]*pow(variables[58], 2.0)*variables[81]*variables[82]*variables[83]*variables[84]*variables[85]*variables[86]*variables[88]+variables[70]*variables[72]*variables[74]*variables[76]*variables[78]*variables[64]*variables[66]*variables[63]*pow(variables[58], 2.0)*variables[81]*variables[82]*variables[83]*variables[84]*variables[85]*variables[87]*variables[88]
    variables[14] = variables[70]*variables[72]*variables[74]*variables[76]*variables[78]*variables[64]*variables[66]*variables[63]*pow(variables[58], 2.0)*variables[81]*variables[82]*variables[83]*variables[84]*variables[86]*variables[87]*variables[88]
    variables[57] = variables[70]*variables[72]*variables[74]*variables[76]*variables[78]*variables[64]*variables[68]*variables[61]*pow(variables[59], 2.0)*variables[81]*variables[82]*variables[83]*variables[85]*variables[86]*variables[87]*variables[88]
    variables[56] = variables[70]*variables[72]*variables[74]*variables[76]*variables[78]*variables[64]*variables[68]*variables[60]*pow(variables[59], 2.0)*variables[81]*variables[82]*variables[84]*variables[85]*variables[86]*variables[87]*variables[88]
    variables[55] = variables[70]*variables[72]*variables[74]*variables[76]*variables[78]*variables[66]*variables[68]*variables[61]*pow(variables[58], 2.0)*variables[81]*variables[82]*variables[83]*variables[85]*variables[86]*variables[87]*variables[88]
    variables[54] = variables[70]*variables[72]*variables[74]*variables[76]*variables[78]*variables[66]*variables[68]*variables[60]*pow(variables[58], 2.0)*variables[81]*variables[82]*variables[84]*variables[85]*variables[86]*variables[87]*variables[88]
    variables[53] = variables[70]*variables[72]*variables[74]*variables[76]*variables[64]*variables[66]*variables[68]*variables[61]*variables[62]*variables[81]*variables[83]*variables[84]*variables[85]*variables[86]*variables[87]*variables[88]+variables[70]*variables[72]*variables[74]*variables[78]*variables[64]*variables[66]*variables[68]*variables[61]*variables[62]*variables[81]*variables[83]*variables[84]*variables[85]*variables[86]*variables[87]*variables[88]
    variables[52] = variables[70]*variables[72]*variables[74]*variables[76]*variables[64]*variables[66]*variables[68]*variables[60]*variables[63]*variables[82]*variables[83]*variables[84]*variables[85]*variables[86]*variables[87]*variables[88]+variables[70]*variables[72]*variables[74]*variables[78]*variables[64]*variables[66]*variables[68]*variables[60]*variables[63]*variables[82]*variables[83]*variables[84]*variables[85]*variables[86]*variables[87]*variables[88]
    variables[51] = variables[72]*variables[74]*variables[76]*variables[78]*variables[64]*variables[66]*variables[68]*variables[62]*pow(variables[59], 2.0)*variables[81]*variables[82]*variables[83]*variables[84]*variables[85]*variables[86]*variables[88]+variables[72]*variables[74]*variables[76]*variables[78]*variables[64]*variables[66]*variables[68]*variables[62]*pow(variables[59], 2.0)*variables[81]*variables[82]*variables[83]*variables[84]*variables[85]*variables[87]*variables[88]
    variables[50] = variables[72]*variables[74]*variables[76]*variables[78]*variables[64]*variables[66]*variables[68]*variables[62]*pow(variables[59], 2.0)*variables[81]*variables[82]*variables[83]*variables[84]*variables[86]*variables[87]*variables[88]
    variables[49] = variables[70]*variables[72]*variables[74]*variables[76]*variables[78]*variables[64]*variables[66]*variables[61]*variables[62]*pow(variables[59], 2.0)*variables[81]*variables[82]*variables[84]*variables[85]*variables[86]*variables[87]*variables[88]+variables[70]*variables[72]*variables[74]*variables[76]*variables[78]*variables[66]*variables[68]*variables[61]*variables[62]*pow(variables[59], 2.0)*variables[82]*variables[83]*variables[84]*variables[85]*variables[86]*variables[87]*variables[88]+variables[70]*variables[72]*variables[74]*variables[78]*variables[64]*variables[66]*variables[68]*variables[61]*variables[62]*pow(variables[59], 2.0)*variables[81]*variables[82]*variables[83]*variables[84]*variables[85]*variables[86]*variables[87]+variables[70]*variables[72]*variables[76]*variables[78]*variables[64]*variables[66]*variables[68]*variables[61]*variables[62]*pow(variables[59], 2.0)*variables[81]*variables[82]*variables[83]*variables[84]*variables[85]*variables[86]*variables[88]+variables[70]*variables[74]*variables[76]*variables[78]*variables[64]*variables[66]*variables[68]*variables[61]*variables[62]*pow(variables[59], 2.0)*variables[81]*variables[82]*variables[83]*variables[84]*variables[86]*variables[87]*variables[88]
    variables[47] = variables[70]*variables[72]*variables[74]*variables[76]*variables[78]*variables[64]*variables[66]*variables[61]*variables[63]*pow(variables[58], 2.0)*variables[81]*variables[82]*variables[83]*variables[85]*variables[86]*variables[87]*variables[88]
    variables[46] = variables[70]*variables[72]*variables[74]*variables[76]*variables[78]*variables[64]*variables[68]*variables[60]*variables[63]*pow(variables[58], 2.0)*variables[81]*variables[83]*variables[84]*variables[85]*variables[86]*variables[87]*variables[88]+variables[70]*variables[72]*variables[74]*variables[76]*variables[64]*variables[66]*variables[68]*variables[60]*variables[63]*pow(variables[58], 2.0)*variables[81]*variables[82]*variables[83]*variables[84]*variables[85]*variables[86]*variables[87]+variables[70]*variables[72]*variables[76]*variables[78]*variables[64]*variables[66]*variables[68]*variables[60]*variables[63]*pow(variables[58], 2.0)*variables[81]*variables[82]*variables[83]*variables[84]*variables[85]*variables[87]*variables[88]+variables[72]*variables[74]*variables[76]*variables[78]*variables[64]*variables[66]*variables[68]*variables[60]*variables[63]*pow(variables[58], 2.0)*variables[81]*variables[82]*variables[83]*variables[85]*variables[86]*variables[87]*variables[88]
    variables[45] = variables[70]*variables[72]*variables[74]*variables[76]*variables[78]*variables[64]*variables[68]*variables[60]*variables[63]*pow(variables[59], 2.0)*variables[82]*variables[83]*variables[84]*variables[85]*variables[86]*variables[87]*variables[88]
    variables[44] = variables[70]*variables[72]*variables[74]*variables[76]*variables[78]*variables[66]*variables[68]*variables[61]*variables[62]*pow(variables[58], 2.0)*variables[81]*variables[83]*variables[84]*variables[85]*variables[86]*variables[87]*variables[88]
    variables[43] = variables[70]*variables[72]*variables[76]*variables[78]*variables[64]*variables[66]*variables[68]*variables[61]*variables[62]*pow(variables[59], 2.0)*variables[81]*variables[82]*variables[83]*variables[84]*variables[86]*variables[87]*variables[88]
    variables[42] = variables[70]*variables[74]*variables[76]*variables[78]*variables[64]*variables[66]*variables[68]*variables[60]*variables[63]*pow(variables[58], 2.0)*variables[81]*variables[82]*variables[83]*variables[84]*variables[85]*variables[86]*variables[88]+variables[70]*variables[74]*variables[76]*variables[78]*variables[64]*variables[66]*variables[68]*variables[60]*variables[63]*pow(variables[58], 2.0)*variables[81]*variables[82]*variables[83]*variables[84]*variables[85]*variables[87]*variables[88]
    variables[41] = variables[72]*variables[74]*variables[76]*variables[78]*variables[64]*variables[66]*variables[68]*variables[60]*variables[62]*pow(variables[59], 2.0)*variables[81]*variables[82]*variables[84]*variables[85]*variables[86]*variables[87]*variables[88]
    variables[40] = variables[70]*variables[72]*variables[74]*variables[76]*variables[78]*variables[64]*variables[66]*variables[61]*variables[62]*variables[63]*pow(variables[58], 2.0)*variables[81]*variables[83]*variables[84]*variables[85]*variables[86]*variables[87]*variables[88]
    variables[39] = variables[70]*variables[72]*variables[74]*variables[76]*variables[78]*variables[64]*variables[66]*variables[61]*variables[62]*variables[63]*pow(variables[59], 2.0)*variables[82]*variables[83]*variables[84]*variables[85]*variables[86]*variables[87]*variables[88]
    variables[38] = variables[70]*variables[72]*variables[74]*variables[76]*variables[78]*variables[64]*variables[68]*variables[60]*variables[63]*pow(variables[59], 2.0)*pow(variables[58], 2.0)*variables[81]*variables[82]*variables[83]*variables[84]*variables[85]*variables[86]*variables[87]
    variables[36] = variables[70]*variables[72]*variables[74]*variables[76]*variables[78]*variables[66]*variables[68]*variables[61]*variables[62]*pow(variables[59], 2.0)*pow(variables[58], 2.0)*variables[81]*variables[82]*variables[83]*variables[84]*variables[85]*variables[86]*variables[87]
    variables[35] = variables[70]*variables[72]*variables[76]*variables[78]*variables[64]*variables[66]*variables[68]*variables[61]*variables[60]*variables[62]*pow(variables[59], 2.0)*variables[81]*variables[82]*variables[84]*variables[85]*variables[86]*variables[87]*variables[88]
    variables[34] = variables[70]*variables[72]*variables[76]*variables[78]*variables[64]*variables[66]*variables[68]*variables[61]*variables[60]*variables[63]*pow(variables[58], 2.0)*variables[81]*variables[82]*variables[83]*variables[85]*variables[86]*variables[87]*variables[88]
    variables[33] = variables[70]*variables[74]*variables[76]*variables[78]*variables[64]*variables[66]*variables[68]*variables[61]*variables[60]*variables[62]*pow(variables[59], 2.0)*variables[81]*variables[82]*variables[84]*variables[85]*variables[86]*variables[87]*variables[88]
    variables[32] = variables[70]*variables[74]*variables[76]*variables[78]*variables[64]*variables[66]*variables[68]*variables[61]*variables[60]*variables[63]*pow(variables[58], 2.0)*variables[81]*variables[82]*variables[83]*variables[85]*variables[86]*variables[87]*variables[88]
    variables[31] = variables[72]*variables[74]*variables[76]*variables[78]*variables[64]*variables[66]*variables[68]*variables[60]*variables[62]*variables[63]*pow(variables[58], 2.0)*variables[81]*variables[83]*variables[84]*variables[85]*variables[86]*variables[87]*variables[88]
    variables[30] = variables[72]*variables[74]*variables[76]*variables[78]*variables[64]*variables[66]*variables[68]*variables[60]*variables[62]*variables[63]*pow(variables[59], 2.0)*variables[82]*variables[83]*variables[84]*variables[85]*variables[86]*variables[87]*variables[88]
    variables[29] = variables[70]*variables[72]*variables[74]*variables[76]*variables[78]*variables[64]*variables[66]*variables[61]*variables[62]*variables[63]*pow(variables[59], 2.0)*pow(variables[58], 2.0)*variables[81]*variables[82]*variables[83]*variables[84]*variables[85]*variables[86]*variables[87]
    variables[28] = variables[70]*variables[72]*variables[76]*variables[78]*variables[64]*variables[66]*variables[68]*variables[61]*variables[60]*variables[62]*variables[63]*pow(variables[58], 2.0)*variables[81]*variables[83]*variables[84]*variables[85]*variables[86]*variables[87]*variables[88]
    variables[27] = variables[70]*variables[72]*variables[76]*variables[78]*variables[64]*variables[66]*variables[68]*variables[61]*variables[60]*variables[62]*variables[63]*pow(variables[59], 2.0)*variables[82]*variables[83]*variables[84]*variables[85]*variables[86]*variables[87]*variables[88]
    variables[25] = variables[70]*variables[74]*variables[76]*variables[78]*variables[64]*variables[66]*variables[68]*variables[61]*variables[60]*variables[62]*variables[63]*pow(variables[58], 2.0)*variables[81]*variables[83]*variables[84]*variables[85]*variables[86]*variables[87]*variables[88]
    variables[24] = variables[70]*variables[74]*variables[76]*variables[78]*variables[64]*variables[66]*variables[68]*variables[61]*variables[60]*variables[62]*variables[63]*pow(variables[59], 2.0)*variables[82]*variables[83]*variables[84]*variables[85]*variables[86]*variables[87]*variables[88]
    variables[23] = variables[72]*variables[74]*variables[76]*variables[78]*variables[64]*variables[66]*variables[68]*variables[60]*variables[62]*variables[63]*pow(variables[59], 2.0)*pow(variables[58], 2.0)*variables[81]*variables[82]*variables[83]*variables[84]*variables[85]*variables[86]*variables[87]
    variables[22] = variables[70]*variables[72]*variables[76]*variables[78]*variables[64]*variables[66]*variables[68]*variables[61]*variables[60]*variables[62]*variables[63]*pow(variables[59], 2.0)*pow(variables[58], 2.0)*variables[81]*variables[82]*variables[83]*variables[84]*variables[85]*variables[86]*variables[87]
    variables[21] = variables[70]*variables[74]*variables[76]*variables[78]*variables[64]*variables[66]*variables[68]*variables[61]*variables[60]*variables[62]*variables[63]*pow(variables[59], 2.0)*pow(variables[58], 2.0)*variables[81]*variables[82]*variables[83]*variables[84]*variables[85]*variables[86]*variables[87]
    variables[20] = variables[70]*variables[72]*variables[74]*variables[76]*variables[64]*variables[66]*variables[68]*variables[81]*variables[82]*variables[83]*variables[84]*variables[85]*variables[86]*variables[88]+variables[70]*variables[72]*variables[74]*variables[76]*variables[64]*variables[66]*variables[68]*variables[81]*variables[82]*variables[83]*variables[84]*variables[85]*variables[87]*variables[88]+variables[70]*variables[72]*variables[74]*variables[78]*variables[64]*variables[66]*variables[68]*variables[81]*variables[82]*variables[83]*variables[84]*variables[85]*variables[86]*variables[88]+variables[70]*variables[72]*variables[74]*variables[78]*variables[64]*variables[66]*variables[68]*variables[81]*variables[82]*variables[83]*variables[84]*variables[85]*variables[87]*variables[88]
    variables[11] = variables[71]+variables[73]+variables[75]+variables[77]+variables[79]+variables[65]+variables[67]+variables[69]


def compute_variables(variables):
    pass
