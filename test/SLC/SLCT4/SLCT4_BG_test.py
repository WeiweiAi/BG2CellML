# The content of this file was generated using the Python profile of libCellML 0.4.0.

from enum import Enum
from math import *


__version__ = "0.4.0"
LIBCELLML_VERSION = "0.4.0"

STATE_COUNT = 6
VARIABLE_COUNT = 67


class VariableType(Enum):
    VARIABLE_OF_INTEGRATION = 0
    STATE = 1
    CONSTANT = 2
    COMPUTED_CONSTANT = 3
    ALGEBRAIC = 4


VOI_INFO = {"name": "t", "units": "second", "component": "SLCT4_BG", "type": VariableType.VARIABLE_OF_INTEGRATION}

STATE_INFO = [
    {"name": "q_5", "units": "fmol", "component": "SLCT4_BG", "type": VariableType.STATE},
    {"name": "q_6", "units": "fmol", "component": "SLCT4_BG", "type": VariableType.STATE},
    {"name": "q_7", "units": "fmol", "component": "SLCT4_BG", "type": VariableType.STATE},
    {"name": "q_8", "units": "fmol", "component": "SLCT4_BG", "type": VariableType.STATE},
    {"name": "q_9", "units": "fmol", "component": "SLCT4_BG", "type": VariableType.STATE},
    {"name": "q_10", "units": "fmol", "component": "SLCT4_BG", "type": VariableType.STATE}
]

VARIABLE_INFO = [
    {"name": "v_Ao", "units": "fmol_per_sec", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_Ao", "units": "fmol", "component": "SLCT4_BG_io", "type": VariableType.CONSTANT},
    {"name": "v_Ai", "units": "fmol_per_sec", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_Ai", "units": "fmol", "component": "SLCT4_BG_io", "type": VariableType.CONSTANT},
    {"name": "v_Bo", "units": "fmol_per_sec", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_Bo", "units": "fmol", "component": "SLCT4_BG_io", "type": VariableType.CONSTANT},
    {"name": "v_Bi", "units": "fmol_per_sec", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_Bi", "units": "fmol", "component": "SLCT4_BG_io", "type": VariableType.CONSTANT},
    {"name": "mu_Ao", "units": "J_per_mol", "component": "SLCT4_BG", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "R", "units": "J_per_K_per_mol", "component": "SLCT4_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_Ao", "units": "per_fmol", "component": "SLCT4_BG_param", "type": VariableType.CONSTANT},
    {"name": "T", "units": "kelvin", "component": "SLCT4_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_Ai", "units": "J_per_mol", "component": "SLCT4_BG", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "K_Ai", "units": "per_fmol", "component": "SLCT4_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_Bo", "units": "J_per_mol", "component": "SLCT4_BG", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "K_Bo", "units": "per_fmol", "component": "SLCT4_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_Bi", "units": "J_per_mol", "component": "SLCT4_BG", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "K_Bi", "units": "per_fmol", "component": "SLCT4_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_5", "units": "fmol_per_sec", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_5", "units": "J_per_mol", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_5", "units": "per_fmol", "component": "SLCT4_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_6", "units": "fmol_per_sec", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_6", "units": "J_per_mol", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_6", "units": "per_fmol", "component": "SLCT4_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_7", "units": "fmol_per_sec", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_7", "units": "J_per_mol", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_7", "units": "per_fmol", "component": "SLCT4_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_8", "units": "fmol_per_sec", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_8", "units": "J_per_mol", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_8", "units": "per_fmol", "component": "SLCT4_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_9", "units": "fmol_per_sec", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_9", "units": "J_per_mol", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_9", "units": "per_fmol", "component": "SLCT4_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_10", "units": "fmol_per_sec", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_10", "units": "J_per_mol", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_10", "units": "per_fmol", "component": "SLCT4_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_re1", "units": "fmol_per_sec", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re1", "units": "fmol_per_sec", "component": "SLCT4_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re1_in", "units": "J_per_mol", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re1_out", "units": "J_per_mol", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re2", "units": "fmol_per_sec", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re2", "units": "fmol_per_sec", "component": "SLCT4_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re2_in", "units": "J_per_mol", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re2_out", "units": "J_per_mol", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re3", "units": "fmol_per_sec", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re3", "units": "fmol_per_sec", "component": "SLCT4_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re3_in", "units": "J_per_mol", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re3_out", "units": "J_per_mol", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re4", "units": "fmol_per_sec", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re4", "units": "fmol_per_sec", "component": "SLCT4_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re4_in", "units": "J_per_mol", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re4_out", "units": "J_per_mol", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re5", "units": "fmol_per_sec", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re5", "units": "fmol_per_sec", "component": "SLCT4_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re5_in", "units": "J_per_mol", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re5_out", "units": "J_per_mol", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re6", "units": "fmol_per_sec", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re6", "units": "fmol_per_sec", "component": "SLCT4_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re6_in", "units": "J_per_mol", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re6_out", "units": "J_per_mol", "component": "SLCT4_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_5_init", "units": "fmol", "component": "SLCT4_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_6_init", "units": "fmol", "component": "SLCT4_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_7_init", "units": "fmol", "component": "SLCT4_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_8_init", "units": "fmol", "component": "SLCT4_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_9_init", "units": "fmol", "component": "SLCT4_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_10_init", "units": "fmol", "component": "SLCT4_BG_param", "type": VariableType.CONSTANT},
    {"name": "F", "units": "C_per_mol", "component": "SLCT4_BG_param", "type": VariableType.CONSTANT}
]


def create_states_array():
    return [nan]*STATE_COUNT


def create_variables_array():
    return [nan]*VARIABLE_COUNT


def initialise_variables(states, rates, variables):
    variables[1] = 1.0
    variables[3] = 1.0
    variables[5] = 1.0
    variables[7] = 1.0
    variables[9] = 8.31
    variables[10] = 1.0
    variables[11] = 293.0
    variables[13] = 1.0
    variables[15] = 1.0
    variables[17] = 1.0
    variables[20] = 1.0
    variables[23] = 1.0
    variables[26] = 1.0
    variables[29] = 1.0
    variables[32] = 1.0
    variables[35] = 1.0
    variables[37] = 1.0
    variables[41] = 1.0
    variables[45] = 1.0
    variables[49] = 1.0
    variables[53] = 1.0
    variables[57] = 1.0
    variables[60] = 1.0
    variables[61] = 1.0
    variables[62] = 1.0
    variables[63] = 1.0
    variables[64] = 1.0
    variables[65] = 1.0
    variables[66] = 96485.0
    states[0] = variables[60]
    states[1] = variables[61]
    states[2] = variables[62]
    states[3] = variables[63]
    states[4] = variables[64]
    states[5] = variables[65]


def compute_computed_constants(variables):
    variables[8] = variables[9]*variables[11]*log(variables[10]*variables[1])
    variables[12] = variables[9]*variables[11]*log(variables[13]*variables[3])
    variables[14] = variables[9]*variables[11]*log(variables[15]*variables[5])
    variables[16] = variables[9]*variables[11]*log(variables[17]*variables[7])


def compute_rates(voi, states, rates, variables):
    variables[19] = variables[9]*variables[11]*log(variables[20]*states[0])
    variables[38] = variables[8]+variables[19]
    variables[25] = variables[9]*variables[11]*log(variables[26]*states[2])
    variables[39] = variables[25]
    variables[36] = variables[37]*(exp(variables[38]/(variables[9]*variables[11]))-exp(variables[39]/(variables[9]*variables[11])))
    variables[31] = variables[9]*variables[11]*log(variables[32]*states[4])
    variables[46] = variables[31]
    variables[47] = variables[14]+variables[19]
    variables[44] = variables[45]*(exp(variables[46]/(variables[9]*variables[11]))-exp(variables[47]/(variables[9]*variables[11])))
    variables[18] = -variables[36]+variables[44]
    rates[0] = variables[18]
    variables[22] = variables[9]*variables[11]*log(variables[23]*states[1])
    variables[50] = variables[16]+variables[22]
    variables[34] = variables[9]*variables[11]*log(variables[35]*states[5])
    variables[51] = variables[34]
    variables[48] = variables[49]*(exp(variables[50]/(variables[9]*variables[11]))-exp(variables[51]/(variables[9]*variables[11])))
    variables[28] = variables[9]*variables[11]*log(variables[29]*states[3])
    variables[42] = variables[28]
    variables[43] = variables[12]+variables[22]
    variables[40] = variables[41]*(exp(variables[42]/(variables[9]*variables[11]))-exp(variables[43]/(variables[9]*variables[11])))
    variables[21] = -variables[48]+variables[40]
    rates[1] = variables[21]
    variables[58] = variables[25]
    variables[59] = variables[28]
    variables[56] = variables[57]*(exp(variables[58]/(variables[9]*variables[11]))-exp(variables[59]/(variables[9]*variables[11])))
    variables[24] = -variables[56]+variables[36]
    rates[2] = variables[24]
    variables[27] = -variables[40]+variables[56]
    rates[3] = variables[27]
    variables[54] = variables[34]
    variables[55] = variables[31]
    variables[52] = variables[53]*(exp(variables[54]/(variables[9]*variables[11]))-exp(variables[55]/(variables[9]*variables[11])))
    variables[30] = -variables[44]+variables[52]
    rates[4] = variables[30]
    variables[33] = -variables[52]+variables[48]
    rates[5] = variables[33]


def compute_variables(voi, states, rates, variables):
    variables[19] = variables[9]*variables[11]*log(variables[20]*states[0])
    variables[22] = variables[9]*variables[11]*log(variables[23]*states[1])
    variables[25] = variables[9]*variables[11]*log(variables[26]*states[2])
    variables[28] = variables[9]*variables[11]*log(variables[29]*states[3])
    variables[31] = variables[9]*variables[11]*log(variables[32]*states[4])
    variables[34] = variables[9]*variables[11]*log(variables[35]*states[5])
    variables[38] = variables[8]+variables[19]
    variables[39] = variables[25]
    variables[36] = variables[37]*(exp(variables[38]/(variables[9]*variables[11]))-exp(variables[39]/(variables[9]*variables[11])))
    variables[42] = variables[28]
    variables[43] = variables[12]+variables[22]
    variables[40] = variables[41]*(exp(variables[42]/(variables[9]*variables[11]))-exp(variables[43]/(variables[9]*variables[11])))
    variables[46] = variables[31]
    variables[47] = variables[14]+variables[19]
    variables[44] = variables[45]*(exp(variables[46]/(variables[9]*variables[11]))-exp(variables[47]/(variables[9]*variables[11])))
    variables[50] = variables[16]+variables[22]
    variables[51] = variables[34]
    variables[48] = variables[49]*(exp(variables[50]/(variables[9]*variables[11]))-exp(variables[51]/(variables[9]*variables[11])))
    variables[54] = variables[34]
    variables[55] = variables[31]
    variables[52] = variables[53]*(exp(variables[54]/(variables[9]*variables[11]))-exp(variables[55]/(variables[9]*variables[11])))
    variables[58] = variables[25]
    variables[59] = variables[28]
    variables[56] = variables[57]*(exp(variables[58]/(variables[9]*variables[11]))-exp(variables[59]/(variables[9]*variables[11])))
    variables[0] = -variables[36]
    variables[2] = variables[40]
    variables[4] = variables[44]
    variables[6] = -variables[48]
    variables[18] = -variables[36]+variables[44]
    variables[21] = -variables[48]+variables[40]
    variables[24] = -variables[56]+variables[36]
    variables[27] = -variables[40]+variables[56]
    variables[30] = -variables[44]+variables[52]
    variables[33] = -variables[52]+variables[48]
