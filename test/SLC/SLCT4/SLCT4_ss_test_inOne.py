# The content of this file was generated using the Python profile of libCellML 0.4.0.

from enum import Enum
from math import *


__version__ = "0.4.0"
LIBCELLML_VERSION = "0.4.0"

VARIABLE_COUNT = 16


class VariableType(Enum):
    CONSTANT = 0
    COMPUTED_CONSTANT = 1
    ALGEBRAIC = 2


VARIABLE_INFO = [
    {"name": "v_ss", "units": "fmol_per_sec", "component": "SLCT4_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "q_Ao", "units": "fmol", "component": "SLCT4_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_Bi", "units": "fmol", "component": "SLCT4_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_Ai", "units": "fmol", "component": "SLCT4_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_Bo", "units": "fmol", "component": "SLCT4_ss_io", "type": VariableType.CONSTANT},
    {"name": "E", "units": "fmol", "component": "SLCT4_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_0", "units": "per_fmol2_sec6", "component": "SLCT4_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_1", "units": "per_fmol2_sec6", "component": "SLCT4_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_2", "units": "per_fmol_sec5", "component": "SLCT4_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_9", "units": "per_fmol2_sec5", "component": "SLCT4_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_8", "units": "per_fmol2_sec5", "component": "SLCT4_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_7", "units": "per_fmol2_sec5", "component": "SLCT4_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_6", "units": "per_fmol2_sec5", "component": "SLCT4_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_5", "units": "per_fmol_sec5", "component": "SLCT4_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_4", "units": "per_fmol_sec5", "component": "SLCT4_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_3", "units": "per_fmol_sec5", "component": "SLCT4_ss_param", "type": VariableType.CONSTANT}
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


def compute_computed_constants(variables):
    variables[0] = variables[5]*(variables[6]*variables[1]*variables[2]-variables[7]*variables[3]*variables[4])/(variables[8]*variables[1]+variables[15]*variables[4]+variables[14]*variables[3]+variables[13]*variables[2]+variables[12]*variables[3]*variables[4]+variables[11]*variables[1]*variables[2]+variables[10]*variables[2]*variables[4]+variables[9]*variables[3]*variables[1])


def compute_variables(variables):
    pass
