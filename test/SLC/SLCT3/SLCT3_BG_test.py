# The content of this file was generated using the Python profile of libCellML 0.4.0.

from enum import Enum
from math import *


__version__ = "0.4.0"
LIBCELLML_VERSION = "0.4.0"

STATE_COUNT = 4
VARIABLE_COUNT = 43


class VariableType(Enum):
    VARIABLE_OF_INTEGRATION = 0
    STATE = 1
    CONSTANT = 2
    COMPUTED_CONSTANT = 3
    ALGEBRAIC = 4


VOI_INFO = {"name": "t", "units": "second", "component": "SLCT3_BG", "type": VariableType.VARIABLE_OF_INTEGRATION}

STATE_INFO = [
    {"name": "q_3", "units": "fmol", "component": "SLCT3_BG", "type": VariableType.STATE},
    {"name": "q_4", "units": "fmol", "component": "SLCT3_BG", "type": VariableType.STATE},
    {"name": "q_5", "units": "fmol", "component": "SLCT3_BG", "type": VariableType.STATE},
    {"name": "q_6", "units": "fmol", "component": "SLCT3_BG", "type": VariableType.STATE}
]

VARIABLE_INFO = [
    {"name": "v_Ai", "units": "fmol_per_sec", "component": "SLCT3_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_Ai", "units": "fmol", "component": "SLCT3_BG_io", "type": VariableType.CONSTANT},
    {"name": "v_Ao", "units": "fmol_per_sec", "component": "SLCT3_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_Ao", "units": "fmol", "component": "SLCT3_BG_io", "type": VariableType.CONSTANT},
    {"name": "mu_Ai", "units": "J_per_mol", "component": "SLCT3_BG", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "R", "units": "J_per_K_per_mol", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_Ai", "units": "per_fmol", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "T", "units": "kelvin", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_Ao", "units": "J_per_mol", "component": "SLCT3_BG", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "K_Ao", "units": "per_fmol", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_3", "units": "fmol_per_sec", "component": "SLCT3_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_3", "units": "J_per_mol", "component": "SLCT3_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_3", "units": "per_fmol", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_4", "units": "fmol_per_sec", "component": "SLCT3_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_4", "units": "J_per_mol", "component": "SLCT3_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_4", "units": "per_fmol", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_5", "units": "fmol_per_sec", "component": "SLCT3_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_5", "units": "J_per_mol", "component": "SLCT3_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_5", "units": "per_fmol", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_6", "units": "fmol_per_sec", "component": "SLCT3_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_6", "units": "J_per_mol", "component": "SLCT3_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_6", "units": "per_fmol", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_re1", "units": "fmol_per_sec", "component": "SLCT3_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re1", "units": "fmol_per_sec", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re1_in", "units": "J_per_mol", "component": "SLCT3_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re1_out", "units": "J_per_mol", "component": "SLCT3_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re2", "units": "fmol_per_sec", "component": "SLCT3_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re2", "units": "fmol_per_sec", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re2_in", "units": "J_per_mol", "component": "SLCT3_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re2_out", "units": "J_per_mol", "component": "SLCT3_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re3", "units": "fmol_per_sec", "component": "SLCT3_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re3", "units": "fmol_per_sec", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re3_in", "units": "J_per_mol", "component": "SLCT3_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re3_out", "units": "J_per_mol", "component": "SLCT3_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re4", "units": "fmol_per_sec", "component": "SLCT3_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re4", "units": "fmol_per_sec", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re4_in", "units": "J_per_mol", "component": "SLCT3_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re4_out", "units": "J_per_mol", "component": "SLCT3_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_3_init", "units": "fmol", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_4_init", "units": "fmol", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_5_init", "units": "fmol", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_6_init", "units": "fmol", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT},
    {"name": "F", "units": "C_per_mol", "component": "SLCT3_BG_param", "type": VariableType.CONSTANT}
]


def create_states_array():
    return [nan]*STATE_COUNT


def create_variables_array():
    return [nan]*VARIABLE_COUNT


def initialise_variables(states, rates, variables):
    variables[1] = 1.0
    variables[3] = 1.0
    variables[5] = 8.31
    variables[6] = 1.0
    variables[7] = 293.0
    variables[9] = 1.0
    variables[12] = 1.0
    variables[15] = 1.0
    variables[18] = 1.0
    variables[21] = 1.0
    variables[23] = 1.0
    variables[27] = 1.0
    variables[31] = 1.0
    variables[35] = 1.0
    variables[38] = 1.0
    variables[39] = 1.0
    variables[40] = 1.0
    variables[41] = 1.0
    variables[42] = 96485.0
    states[0] = variables[38]
    states[1] = variables[39]
    states[2] = variables[40]
    states[3] = variables[41]


def compute_computed_constants(variables):
    variables[4] = variables[5]*variables[7]*log(variables[6]*variables[1])
    variables[8] = variables[5]*variables[7]*log(variables[9]*variables[3])


def compute_rates(voi, states, rates, variables):
    variables[11] = variables[5]*variables[7]*log(variables[12]*states[0])
    variables[32] = variables[11]
    variables[14] = variables[5]*variables[7]*log(variables[15]*states[1])
    variables[33] = variables[14]
    variables[30] = variables[31]*(exp(variables[32]/(variables[5]*variables[7]))-exp(variables[33]/(variables[5]*variables[7])))
    variables[17] = variables[5]*variables[7]*log(variables[18]*states[2])
    variables[24] = variables[17]
    variables[25] = variables[4]+variables[11]
    variables[22] = variables[23]*(exp(variables[24]/(variables[5]*variables[7]))-exp(variables[25]/(variables[5]*variables[7])))
    variables[10] = -variables[30]+variables[22]
    rates[0] = variables[10]
    variables[28] = variables[8]+variables[14]
    variables[20] = variables[5]*variables[7]*log(variables[21]*states[3])
    variables[29] = variables[20]
    variables[26] = variables[27]*(exp(variables[28]/(variables[5]*variables[7]))-exp(variables[29]/(variables[5]*variables[7])))
    variables[13] = -variables[26]+variables[30]
    rates[1] = variables[13]
    variables[36] = variables[20]
    variables[37] = variables[17]
    variables[34] = variables[35]*(exp(variables[36]/(variables[5]*variables[7]))-exp(variables[37]/(variables[5]*variables[7])))
    variables[16] = -variables[22]+variables[34]
    rates[2] = variables[16]
    variables[19] = -variables[34]+variables[26]
    rates[3] = variables[19]


def compute_variables(voi, states, rates, variables):
    variables[11] = variables[5]*variables[7]*log(variables[12]*states[0])
    variables[14] = variables[5]*variables[7]*log(variables[15]*states[1])
    variables[17] = variables[5]*variables[7]*log(variables[18]*states[2])
    variables[20] = variables[5]*variables[7]*log(variables[21]*states[3])
    variables[24] = variables[17]
    variables[25] = variables[4]+variables[11]
    variables[22] = variables[23]*(exp(variables[24]/(variables[5]*variables[7]))-exp(variables[25]/(variables[5]*variables[7])))
    variables[28] = variables[8]+variables[14]
    variables[29] = variables[20]
    variables[26] = variables[27]*(exp(variables[28]/(variables[5]*variables[7]))-exp(variables[29]/(variables[5]*variables[7])))
    variables[32] = variables[11]
    variables[33] = variables[14]
    variables[30] = variables[31]*(exp(variables[32]/(variables[5]*variables[7]))-exp(variables[33]/(variables[5]*variables[7])))
    variables[36] = variables[20]
    variables[37] = variables[17]
    variables[34] = variables[35]*(exp(variables[36]/(variables[5]*variables[7]))-exp(variables[37]/(variables[5]*variables[7])))
    variables[0] = variables[22]
    variables[2] = -variables[26]
    variables[10] = -variables[30]+variables[22]
    variables[13] = -variables[26]+variables[30]
    variables[16] = -variables[22]+variables[34]
    variables[19] = -variables[34]+variables[26]
