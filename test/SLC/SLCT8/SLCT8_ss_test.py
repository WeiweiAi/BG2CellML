# The content of this file was generated using the Python profile of libCellML 0.4.0.

from enum import Enum
from math import *


__version__ = "0.4.0"
LIBCELLML_VERSION = "0.4.0"

VARIABLE_COUNT = 21


class VariableType(Enum):
    CONSTANT = 0
    COMPUTED_CONSTANT = 1
    ALGEBRAIC = 2


VARIABLE_INFO = [
    {"name": "v_ss", "units": "fmol_per_sec", "component": "SLCT8_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "q_Gluo", "units": "fmol", "component": "SLCT8_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_Nao", "units": "fmol", "component": "SLCT8_ss_io", "type": VariableType.CONSTANT},
    {"name": "V_m", "units": "volt", "component": "SLCT8_ss_io", "type": VariableType.CONSTANT},
    {"name": "F", "units": "C_per_mol", "component": "SLCT8_ss_io", "type": VariableType.CONSTANT},
    {"name": "R", "units": "J_per_K_per_mol", "component": "SLCT8_ss_io", "type": VariableType.CONSTANT},
    {"name": "T", "units": "kelvin", "component": "SLCT8_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_Glui", "units": "fmol", "component": "SLCT8_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_Nai", "units": "fmol", "component": "SLCT8_ss_io", "type": VariableType.CONSTANT},
    {"name": "E", "units": "fmol", "component": "SLCT8_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_0", "units": "per_fmol3_sec7", "component": "SLCT8_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_1", "units": "per_fmol3_sec7", "component": "SLCT8_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_10", "units": "per_fmol5_sec6", "component": "SLCT8_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_9", "units": "per_fmol3_sec6", "component": "SLCT8_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_8", "units": "per_fmol2_sec6", "component": "SLCT8_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_7", "units": "per_fmol3_sec6", "component": "SLCT8_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_6", "units": "per_fmol3_sec6", "component": "SLCT8_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_5", "units": "per_fmol3_sec6", "component": "SLCT8_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_4", "units": "per_fmol3_sec6", "component": "SLCT8_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_3", "units": "per_fmol_sec6", "component": "SLCT8_ss_param", "type": VariableType.CONSTANT},
    {"name": "P_2", "units": "per_fmol_sec6", "component": "SLCT8_ss_param", "type": VariableType.CONSTANT}
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


def compute_computed_constants(variables):
    variables[0] = variables[9]*(variables[10]*variables[1]*pow(variables[2], 2.0)-variables[11]*variables[7]*pow(variables[8], 2.0))*exp(2.0*variables[4]*variables[3]/(variables[5]*variables[6]))/(variables[12]*variables[7]*pow(variables[8], 2.0)*pow(variables[2], 2.0)*exp(variables[4]*variables[3]/(variables[5]*variables[6]))+variables[20]*variables[7]*exp(variables[4]*variables[3]/(variables[5]*variables[6]))+variables[19]*variables[7]*exp(2.0*variables[4]*variables[3]/(variables[5]*variables[6]))+variables[18]*variables[7]*pow(variables[8], 2.0)*exp(2.0*variables[4]*variables[3]/(variables[5]*variables[6]))+variables[17]*variables[1]*pow(variables[8], 2.0)*exp(2.0*variables[4]*variables[3]/(variables[5]*variables[6]))+variables[16]*variables[7]*pow(variables[2], 2.0)*exp(variables[4]*variables[3]/(variables[5]*variables[6]))+variables[15]*variables[7]*pow(variables[8], 2.0)*exp(variables[4]*variables[3]/(variables[5]*variables[6]))+variables[14]*pow(variables[8], 2.0)*exp(2.0*variables[4]*variables[3]/(variables[5]*variables[6]))+variables[13]*variables[7]*pow(variables[2], 2.0)*exp(2.0*variables[4]*variables[3]/(variables[5]*variables[6])))


def compute_variables(variables):
    pass
