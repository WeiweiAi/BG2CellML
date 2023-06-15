# The content of this file was generated using the Python profile of libCellML 0.4.0.

from enum import Enum
from math import *


__version__ = "0.4.0"
LIBCELLML_VERSION = "0.4.0"

VARIABLE_COUNT = 56


class VariableType(Enum):
    CONSTANT = 0
    COMPUTED_CONSTANT = 1
    ALGEBRAIC = 2


VARIABLE_INFO = [
    {"name": "v_ss", "units": "fmol_per_sec", "component": "SLCT11_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "q_Clo", "units": "fmol", "component": "SLCT11_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_Ki", "units": "fmol", "component": "SLCT11_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_Nao", "units": "fmol", "component": "SLCT11_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_So", "units": "fmol", "component": "SLCT11_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_Cli", "units": "fmol", "component": "SLCT11_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_Ko", "units": "fmol", "component": "SLCT11_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_Nai", "units": "fmol", "component": "SLCT11_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_Si", "units": "fmol", "component": "SLCT11_ss_io", "type": VariableType.CONSTANT},
    {"name": "E", "units": "fmol", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_0", "units": "per_fmol4_sec10", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_1", "units": "per_fmol4_sec10", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_10", "units": "per_fmol2_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_9", "units": "per_fmol2_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_8", "units": "per_fmol2_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_7", "units": "per_fmol2_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_6", "units": "per_fmol2_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_5", "units": "per_fmol2_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_45", "units": "per_fmol6_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_44", "units": "per_fmol6_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_43", "units": "per_fmol6_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_42", "units": "per_fmol5_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_41", "units": "per_fmol5_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_40", "units": "per_fmol5_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_4", "units": "per_fmol2_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_39", "units": "per_fmol5_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_38", "units": "per_fmol5_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_37", "units": "per_fmol5_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_36", "units": "per_fmol5_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_35", "units": "per_fmol5_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_34", "units": "per_fmol4_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_33", "units": "per_fmol4_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_32", "units": "per_fmol4_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_31", "units": "per_fmol4_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_30", "units": "per_fmol4_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_3", "units": "per_fmol_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_29", "units": "per_fmol4_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_28", "units": "per_fmol4_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_27", "units": "per_fmol4_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_26", "units": "per_fmol4_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_25", "units": "per_fmol4_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_24", "units": "per_fmol3_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_23", "units": "per_fmol3_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_22", "units": "per_fmol3_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_21", "units": "per_fmol3_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_20", "units": "per_fmol3_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_2", "units": "per_fmol_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_19", "units": "per_fmol3_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_18", "units": "per_fmol3_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_17", "units": "per_fmol3_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_16", "units": "per_fmol3_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_15", "units": "per_fmol3_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_14", "units": "per_fmol3_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_13", "units": "per_fmol3_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_12", "units": "per_fmol3_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_11", "units": "per_fmol3_sec9", "component": "SLCT11_ss_param", "type": VariableType.CONSTANT}
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
    variables[8] = 1.0
    variables[9] = 1.0
    variables[10] = 1.0
    variables[11] = 1.0
    variables[12] = 1.0
    variables[13] = 1.0
    variables[14] = 1.0
    variables[15] = 1.0
    variables[16] = 1.0
    variables[17] = 1.0
    variables[18] = 1.0
    variables[19] = 1.0
    variables[20] = 1.0
    variables[21] = 1.0
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


def compute_computed_constants(variables):
    variables[0] = variables[9]*(variables[10]*variables[1]*variables[2]*variables[3]*variables[4]-variables[11]*variables[5]*variables[6]*variables[7]*variables[8])/(variables[12]*variables[6]*variables[7]+variables[55]*variables[5]*variables[2]*variables[3]+variables[54]*variables[1]*variables[2]*variables[3]+variables[53]*variables[5]*variables[2]*variables[6]+variables[52]*variables[1]*variables[2]*variables[6]+variables[51]*variables[5]*variables[6]*variables[8]+variables[50]*variables[1]*variables[6]*variables[4]+variables[49]*variables[1]*variables[3]*variables[4]+variables[48]*variables[5]*variables[2]*variables[8]+variables[47]*variables[5]*variables[7]*variables[8]+variables[46]*variables[6]+variables[45]*variables[1]*variables[2]*variables[4]+variables[44]*variables[6]*variables[7]*variables[8]+variables[43]*variables[2]*variables[3]*variables[4]+variables[42]*variables[5]*variables[6]*variables[7]+variables[41]*variables[1]*variables[6]*variables[7]+variables[40]*variables[5]*variables[2]*variables[3]*variables[8]+variables[39]*variables[5]*variables[6]*variables[7]*variables[8]+variables[38]*variables[5]*variables[7]*variables[3]*variables[8]+variables[37]*variables[5]*variables[2]*variables[6]*variables[8]+variables[36]*variables[1]*variables[2]*variables[6]*variables[4]+variables[35]*variables[2]+variables[34]*variables[1]*variables[2]*variables[3]*variables[4]+variables[33]*variables[1]*variables[6]*variables[7]*variables[8]+variables[32]*variables[5]*variables[2]*variables[3]*variables[4]+variables[31]*variables[1]*variables[6]*variables[7]*variables[4]+variables[30]*variables[1]*variables[7]*variables[3]*variables[4]+variables[29]*variables[5]*variables[1]*variables[2]*variables[3]*variables[4]+variables[28]*variables[5]*variables[1]*variables[6]*variables[7]*variables[8]+variables[27]*variables[1]*variables[2]*variables[3]*variables[8]*variables[4]+variables[26]*variables[1]*variables[6]*variables[7]*variables[8]*variables[4]+variables[25]*variables[1]*variables[7]*variables[3]*variables[8]*variables[4]+variables[24]*variables[2]*variables[3]+variables[23]*variables[5]*variables[2]*variables[3]*variables[8]*variables[4]+variables[22]*variables[5]*variables[6]*variables[7]*variables[8]*variables[4]+variables[21]*variables[5]*variables[7]*variables[3]*variables[8]*variables[4]+variables[20]*variables[5]*variables[1]*variables[2]*variables[3]*variables[8]*variables[4]+variables[19]*variables[5]*variables[1]*variables[6]*variables[7]*variables[8]*variables[4]+variables[18]*variables[5]*variables[1]*variables[7]*variables[3]*variables[8]*variables[4]+variables[17]*variables[2]*variables[6]+variables[16]*variables[5]*variables[6]+variables[15]*variables[1]*variables[6]+variables[14]*variables[5]*variables[2]+variables[13]*variables[1]*variables[2])


def compute_variables(variables):
    pass
