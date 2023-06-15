# The content of this file was generated using the Python profile of libCellML 0.4.0.

from enum import Enum
from math import *


__version__ = "0.4.0"
LIBCELLML_VERSION = "0.4.0"

VARIABLE_COUNT = 32


class VariableType(Enum):
    CONSTANT = 0
    COMPUTED_CONSTANT = 1
    ALGEBRAIC = 2


VARIABLE_INFO = [
    {"name": "v_ss", "units": "fmol_per_sec", "component": "SLCT7_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "q_Cli", "units": "fmol", "component": "SLCT7_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_Nao", "units": "fmol", "component": "SLCT7_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_HCO3o", "units": "fmol", "component": "SLCT7_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_Clo", "units": "fmol", "component": "SLCT7_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_Nai", "units": "fmol", "component": "SLCT7_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_HCO3i", "units": "fmol", "component": "SLCT7_ss_io", "type": VariableType.CONSTANT},
    {"name": "E", "units": "fmol", "component": "SLCT7_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_0", "units": "per_fmol4_sec8", "component": "SLCT7_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_1", "units": "per_fmol4_sec8", "component": "SLCT7_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_10", "units": "per_fmol3_sec7", "component": "SLCT7_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_9", "units": "per_fmol2_sec7", "component": "SLCT7_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_8", "units": "per_fmol2_sec7", "component": "SLCT7_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_7", "units": "per_fmol2_sec7", "component": "SLCT7_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_6", "units": "per_fmol3_sec7", "component": "SLCT7_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_5", "units": "per_fmol3_sec7", "component": "SLCT7_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_4", "units": "per_fmol3_sec7", "component": "SLCT7_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_3", "units": "per_fmol_sec7", "component": "SLCT7_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_23", "units": "per_fmol6_sec7", "component": "SLCT7_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_22", "units": "per_fmol6_sec7", "component": "SLCT7_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_21", "units": "per_fmol6_sec7", "component": "SLCT7_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_20", "units": "per_fmol4_sec7", "component": "SLCT7_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_2", "units": "per_fmol_sec7", "component": "SLCT7_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_19", "units": "per_fmol4_sec7", "component": "SLCT7_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_18", "units": "per_fmol4_sec7", "component": "SLCT7_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_17", "units": "per_fmol4_sec7", "component": "SLCT7_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_16", "units": "per_fmol4_sec7", "component": "SLCT7_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_15", "units": "per_fmol4_sec7", "component": "SLCT7_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_14", "units": "per_fmol4_sec7", "component": "SLCT7_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_13", "units": "per_fmol4_sec7", "component": "SLCT7_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_12", "units": "per_fmol3_sec7", "component": "SLCT7_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_11", "units": "per_fmol3_sec7", "component": "SLCT7_ss_param", "type": VariableType.CONSTANT}
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


def compute_computed_constants(variables):
    variables[0] = variables[7]*(variables[8]*variables[1]*pow(variables[3], 2.0)*variables[2]-variables[9]*variables[4]*pow(variables[6], 2.0)*variables[5])/(variables[10]*variables[4]*pow(variables[6], 2.0)+variables[31]*variables[4]*pow(variables[3], 2.0)+variables[30]*pow(variables[3], 2.0)*variables[2]+variables[29]*variables[1]*variables[4]*pow(variables[6], 2.0)+variables[28]*variables[1]*variables[4]*pow(variables[3], 2.0)+variables[27]*variables[1]*pow(variables[3], 2.0)*variables[2]+variables[26]*variables[4]*pow(variables[6], 2.0)*variables[5]+variables[25]*variables[4]*pow(variables[3], 2.0)*variables[5]+variables[24]*pow(variables[3], 2.0)*variables[5]*variables[2]+variables[23]*variables[1]*pow(variables[6], 2.0)*variables[2]+variables[22]*variables[1]+variables[21]*pow(variables[6], 2.0)*variables[5]*variables[2]+variables[20]*variables[1]*pow(variables[6], 2.0)*pow(variables[3], 2.0)*variables[2]+variables[19]*variables[4]*pow(variables[6], 2.0)*pow(variables[3], 2.0)*variables[5]+variables[18]*pow(variables[6], 2.0)*pow(variables[3], 2.0)*variables[5]*variables[2]+variables[17]*variables[4]+variables[16]*variables[1]*pow(variables[6], 2.0)+variables[15]*variables[1]*pow(variables[3], 2.0)+variables[14]*pow(variables[6], 2.0)*variables[5]+variables[13]*variables[1]*variables[4]+variables[12]*variables[4]*variables[5]+variables[11]*variables[1]*variables[2])


def compute_variables(variables):
    pass
