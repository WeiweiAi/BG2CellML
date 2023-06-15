# The content of this file was generated using the Python profile of libCellML 0.4.0.

from enum import Enum
from math import *


__version__ = "0.4.0"
LIBCELLML_VERSION = "0.4.0"

VARIABLE_COUNT = 27


class VariableType(Enum):
    CONSTANT = 0
    COMPUTED_CONSTANT = 1
    ALGEBRAIC = 2


VARIABLE_INFO = [
    {"name": "v_ss", "units": "fmol_per_sec", "component": "SLCT3_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "q_Ao", "units": "fmol", "component": "SLCT3_BG_ss_io", "type": VariableType.CONSTANT},
    {"name": "q_Ai", "units": "fmol", "component": "SLCT3_BG_ss_io", "type": VariableType.CONSTANT},
    {"name": "E", "units": "fmol", "component": "SLCT3_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_0", "units": "per_fmol_sec4", "component": "SLCT3_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_1", "units": "per_fmol_sec4", "component": "SLCT3_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_2", "units": "per_fmol_sec3", "component": "SLCT3_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_5", "units": "per_sec3", "component": "SLCT3_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_4", "units": "per_fmol2_sec3", "component": "SLCT3_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "P_3", "units": "per_fmol_sec3", "component": "SLCT3_BG_ss", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "K_Ai", "units": "per_fmol", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_Ao", "units": "per_fmol", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_3", "units": "per_fmol", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_3_init", "units": "fmol", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_4", "units": "per_fmol", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_4_init", "units": "fmol", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_5", "units": "per_fmol", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_5_init", "units": "fmol", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_6", "units": "per_fmol", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_6_init", "units": "fmol", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "kappa_re1", "units": "fmol_per_sec", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "kappa_re2", "units": "fmol_per_sec", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "kappa_re3", "units": "fmol_per_sec", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "kappa_re4", "units": "fmol_per_sec", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "F", "units": "C_per_mol", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "R", "units": "J_per_K_per_mol", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "T", "units": "kelvin", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT}
]


def create_variables_array():
    return [nan]*VARIABLE_COUNT


def initialise_variables(variables):
    variables[1] = 1.0
    variables[2] = 1.0
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
    variables[24] = 96485.0
    variables[25] = 8.31
    variables[26] = 293.0


def compute_computed_constants(variables):
    variables[0] = variables[3]*(variables[4]*variables[1]-variables[5]*variables[2])/(variables[6]*variables[2]+variables[9]*variables[1]+variables[8]*variables[2]*variables[1]+variables[7])
    variables[4] = variables[12]*variables[14]*variables[16]*variables[18]*variables[11]*variables[20]*variables[21]*variables[22]*variables[23]
    variables[5] = variables[12]*variables[14]*variables[16]*variables[18]*variables[10]*variables[20]*variables[21]*variables[22]*variables[23]
    variables[6] = variables[12]*variables[14]*variables[16]*variables[10]*variables[20]*variables[22]*variables[23]+variables[12]*variables[14]*variables[18]*variables[10]*variables[20]*variables[21]*variables[22]+variables[12]*variables[14]*variables[18]*variables[10]*variables[20]*variables[22]*variables[23]+variables[12]*variables[16]*variables[18]*variables[10]*variables[20]*variables[21]*variables[23]
    variables[9] = variables[12]*variables[14]*variables[16]*variables[11]*variables[20]*variables[21]*variables[22]+variables[12]*variables[14]*variables[16]*variables[11]*variables[21]*variables[22]*variables[23]+variables[12]*variables[14]*variables[18]*variables[11]*variables[21]*variables[22]*variables[23]+variables[14]*variables[16]*variables[18]*variables[11]*variables[20]*variables[21]*variables[23]
    variables[8] = variables[12]*variables[14]*variables[16]*variables[10]*variables[11]*variables[20]*variables[21]*variables[23]+variables[12]*variables[14]*variables[18]*variables[10]*variables[11]*variables[20]*variables[21]*variables[23]
    variables[7] = variables[12]*variables[16]*variables[18]*variables[20]*variables[21]*variables[22]+variables[12]*variables[16]*variables[18]*variables[20]*variables[22]*variables[23]+variables[12]*variables[16]*variables[18]*variables[21]*variables[22]*variables[23]+variables[14]*variables[16]*variables[18]*variables[20]*variables[21]*variables[22]+variables[14]*variables[16]*variables[18]*variables[20]*variables[22]*variables[23]+variables[14]*variables[16]*variables[18]*variables[21]*variables[22]*variables[23]
    variables[3] = variables[13]+variables[15]+variables[17]+variables[19]


def compute_variables(variables):
    pass
