# The content of this file was generated using the Python profile of libCellML 0.4.0.

from enum import Enum
from math import *


__version__ = "0.4.0"
LIBCELLML_VERSION = "0.4.0"

STATE_COUNT = 8
VARIABLE_COUNT = 95


class VariableType(Enum):
    VARIABLE_OF_INTEGRATION = 0
    STATE = 1
    CONSTANT = 2
    COMPUTED_CONSTANT = 3
    ALGEBRAIC = 4


VOI_INFO = {"name": "t", "units": "second", "component": "SLCT14_BG", "type": VariableType.VARIABLE_OF_INTEGRATION}

STATE_INFO = [
    {"name": "q_7", "units": "fmol", "component": "SLCT14_BG", "type": VariableType.STATE},
    {"name": "q_8", "units": "fmol", "component": "SLCT14_BG", "type": VariableType.STATE},
    {"name": "q_9", "units": "fmol", "component": "SLCT14_BG", "type": VariableType.STATE},
    {"name": "q_10", "units": "fmol", "component": "SLCT14_BG", "type": VariableType.STATE},
    {"name": "q_11", "units": "fmol", "component": "SLCT14_BG", "type": VariableType.STATE},
    {"name": "q_12", "units": "fmol", "component": "SLCT14_BG", "type": VariableType.STATE},
    {"name": "q_13", "units": "fmol", "component": "SLCT14_BG", "type": VariableType.STATE},
    {"name": "q_14", "units": "fmol", "component": "SLCT14_BG", "type": VariableType.STATE}
]

VARIABLE_INFO = [
    {"name": "v_cAAo", "units": "fmol_per_sec", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_cAAo", "units": "fmol", "component": "SLCT14_BG_io", "type": VariableType.CONSTANT},
    {"name": "v_cAAi", "units": "fmol_per_sec", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_cAAi", "units": "fmol", "component": "SLCT14_BG_io", "type": VariableType.CONSTANT},
    {"name": "v_InAAo", "units": "fmol_per_sec", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_InAAo", "units": "fmol", "component": "SLCT14_BG_io", "type": VariableType.CONSTANT},
    {"name": "v_InAAi", "units": "fmol_per_sec", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_InAAi", "units": "fmol", "component": "SLCT14_BG_io", "type": VariableType.CONSTANT},
    {"name": "v_Nai", "units": "fmol_per_sec", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_Nai", "units": "fmol", "component": "SLCT14_BG_io", "type": VariableType.CONSTANT},
    {"name": "v_Nao", "units": "fmol_per_sec", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_Nao", "units": "fmol", "component": "SLCT14_BG_io", "type": VariableType.CONSTANT},
    {"name": "I_m", "units": "fA", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_m", "units": "fC", "component": "SLCT14_BG_io", "type": VariableType.CONSTANT},
    {"name": "mu_cAAo", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "R", "units": "J_per_K_per_mol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_cAAo", "units": "per_fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "T", "units": "kelvin", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_cAAi", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "K_cAAi", "units": "per_fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_InAAo", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "K_InAAo", "units": "per_fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_InAAi", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "K_InAAi", "units": "per_fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_Nai", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "K_Nai", "units": "per_fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_Nao", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "K_Nao", "units": "per_fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_7", "units": "fmol_per_sec", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_7", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_7", "units": "per_fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_8", "units": "fmol_per_sec", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_8", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_8", "units": "per_fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_9", "units": "fmol_per_sec", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_9", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_9", "units": "per_fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_10", "units": "fmol_per_sec", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_10", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_10", "units": "per_fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_11", "units": "fmol_per_sec", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_11", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_11", "units": "per_fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_12", "units": "fmol_per_sec", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_12", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_12", "units": "per_fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_13", "units": "fmol_per_sec", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_13", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_13", "units": "per_fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_14", "units": "fmol_per_sec", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_14", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_14", "units": "per_fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "V_m", "units": "volt", "component": "SLCT14_BG", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "C_m", "units": "fF", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_re1", "units": "fmol_per_sec", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re1", "units": "fmol_per_sec", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re1_in", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re1_out", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re2", "units": "fmol_per_sec", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re2", "units": "fmol_per_sec", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re2_in", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re2_out", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re3", "units": "fmol_per_sec", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re3", "units": "fmol_per_sec", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re3_in", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re3_out", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re4", "units": "fmol_per_sec", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re4", "units": "fmol_per_sec", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re4_in", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re4_out", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re5", "units": "fmol_per_sec", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re5", "units": "fmol_per_sec", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re5_in", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re5_out", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re6", "units": "fmol_per_sec", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re6", "units": "fmol_per_sec", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re6_in", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re6_out", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re7", "units": "fmol_per_sec", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re7", "units": "fmol_per_sec", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re7_in", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re7_out", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re8", "units": "fmol_per_sec", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re8", "units": "fmol_per_sec", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re8_in", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re8_out", "units": "J_per_mol", "component": "SLCT14_BG", "type": VariableType.ALGEBRAIC},
    {"name": "F", "units": "C_per_mol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_7_init", "units": "fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_8_init", "units": "fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_9_init", "units": "fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_10_init", "units": "fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_11_init", "units": "fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_12_init", "units": "fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_13_init", "units": "fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_14_init", "units": "fmol", "component": "SLCT14_BG_param", "type": VariableType.CONSTANT}
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
    variables[9] = 1.0
    variables[11] = 1.0
    variables[13] = 1.0
    variables[15] = 8.31
    variables[16] = 1.0
    variables[17] = 293.0
    variables[19] = 1.0
    variables[21] = 1.0
    variables[23] = 1.0
    variables[25] = 1.0
    variables[27] = 1.0
    variables[30] = 1.0
    variables[33] = 1.0
    variables[36] = 1.0
    variables[39] = 1.0
    variables[42] = 1.0
    variables[45] = 1.0
    variables[48] = 1.0
    variables[51] = 1.0
    variables[53] = 1.0
    variables[55] = 1.0
    variables[59] = 1.0
    variables[63] = 1.0
    variables[67] = 1.0
    variables[71] = 1.0
    variables[75] = 1.0
    variables[79] = 1.0
    variables[83] = 1.0
    variables[86] = 96485.0
    variables[87] = 1.0
    variables[88] = 1.0
    variables[89] = 1.0
    variables[90] = 1.0
    variables[91] = 1.0
    variables[92] = 1.0
    variables[93] = 1.0
    variables[94] = 1.0
    states[0] = variables[87]
    states[1] = variables[88]
    states[2] = variables[89]
    states[3] = variables[90]
    states[4] = variables[91]
    states[5] = variables[92]
    states[6] = variables[93]
    states[7] = variables[94]


def compute_computed_constants(variables):
    variables[14] = variables[15]*variables[17]*log(variables[16]*variables[1])
    variables[18] = variables[15]*variables[17]*log(variables[19]*variables[3])
    variables[20] = variables[15]*variables[17]*log(variables[21]*variables[5])
    variables[22] = variables[15]*variables[17]*log(variables[23]*variables[7])
    variables[24] = variables[15]*variables[17]*log(variables[25]*variables[9])
    variables[26] = variables[15]*variables[17]*log(variables[27]*variables[11])
    variables[52] = variables[13]/variables[53]


def compute_rates(voi, states, rates, variables):
    variables[29] = variables[15]*variables[17]*log(variables[30]*states[0])
    variables[56] = variables[29]
    variables[35] = variables[15]*variables[17]*log(variables[36]*states[2])
    variables[57] = variables[14]+variables[35]
    variables[54] = variables[55]*(exp(variables[56]/(variables[15]*variables[17]))-exp(variables[57]/(variables[15]*variables[17])))
    variables[32] = variables[15]*variables[17]*log(variables[33]*states[1])
    variables[80] = variables[32]
    variables[81] = variables[29]
    variables[78] = variables[79]*(exp(variables[80]/(variables[15]*variables[17]))-exp(variables[81]/(variables[15]*variables[17])))
    variables[28] = -variables[54]+variables[78]
    rates[0] = variables[28]
    variables[38] = variables[15]*variables[17]*log(variables[39]*states[3])
    variables[60] = variables[18]+variables[38]
    variables[61] = variables[32]
    variables[58] = variables[59]*(exp(variables[60]/(variables[15]*variables[17]))-exp(variables[61]/(variables[15]*variables[17])))
    variables[31] = -variables[78]+variables[58]
    rates[1] = variables[31]
    variables[64] = variables[20]+variables[35]
    variables[41] = variables[15]*variables[17]*log(variables[42]*states[4])
    variables[65] = variables[41]
    variables[62] = variables[63]*(exp(variables[64]/(variables[15]*variables[17]))-exp(variables[65]/(variables[15]*variables[17])))
    variables[34] = -variables[62]+variables[54]
    rates[2] = variables[34]
    variables[44] = variables[15]*variables[17]*log(variables[45]*states[5])
    variables[68] = variables[44]
    variables[69] = variables[22]+variables[38]
    variables[66] = variables[67]*(exp(variables[68]/(variables[15]*variables[17]))-exp(variables[69]/(variables[15]*variables[17])))
    variables[37] = -variables[58]+variables[66]
    rates[3] = variables[37]
    variables[72] = variables[26]+variables[41]+variables[86]*variables[52]
    variables[47] = variables[15]*variables[17]*log(variables[48]*states[6])
    variables[73] = variables[47]
    variables[70] = variables[71]*(exp(variables[72]/(variables[15]*variables[17]))-exp(variables[73]/(variables[15]*variables[17])))
    variables[40] = -variables[70]+variables[62]
    rates[4] = variables[40]
    variables[50] = variables[15]*variables[17]*log(variables[51]*states[7])
    variables[76] = variables[50]
    variables[77] = variables[24]+variables[44]
    variables[74] = variables[75]*(exp(variables[76]/(variables[15]*variables[17]))-exp(variables[77]/(variables[15]*variables[17])))
    variables[43] = -variables[66]+variables[74]
    rates[5] = variables[43]
    variables[84] = variables[47]
    variables[85] = variables[50]
    variables[82] = variables[83]*(exp(variables[84]/(variables[15]*variables[17]))-exp(variables[85]/(variables[15]*variables[17])))
    variables[46] = -variables[82]+variables[70]
    rates[6] = variables[46]
    variables[49] = -variables[74]+variables[82]
    rates[7] = variables[49]


def compute_variables(voi, states, rates, variables):
    variables[29] = variables[15]*variables[17]*log(variables[30]*states[0])
    variables[32] = variables[15]*variables[17]*log(variables[33]*states[1])
    variables[35] = variables[15]*variables[17]*log(variables[36]*states[2])
    variables[38] = variables[15]*variables[17]*log(variables[39]*states[3])
    variables[41] = variables[15]*variables[17]*log(variables[42]*states[4])
    variables[44] = variables[15]*variables[17]*log(variables[45]*states[5])
    variables[47] = variables[15]*variables[17]*log(variables[48]*states[6])
    variables[50] = variables[15]*variables[17]*log(variables[51]*states[7])
    variables[56] = variables[29]
    variables[57] = variables[14]+variables[35]
    variables[54] = variables[55]*(exp(variables[56]/(variables[15]*variables[17]))-exp(variables[57]/(variables[15]*variables[17])))
    variables[60] = variables[18]+variables[38]
    variables[61] = variables[32]
    variables[58] = variables[59]*(exp(variables[60]/(variables[15]*variables[17]))-exp(variables[61]/(variables[15]*variables[17])))
    variables[64] = variables[20]+variables[35]
    variables[65] = variables[41]
    variables[62] = variables[63]*(exp(variables[64]/(variables[15]*variables[17]))-exp(variables[65]/(variables[15]*variables[17])))
    variables[68] = variables[44]
    variables[69] = variables[22]+variables[38]
    variables[66] = variables[67]*(exp(variables[68]/(variables[15]*variables[17]))-exp(variables[69]/(variables[15]*variables[17])))
    variables[72] = variables[26]+variables[41]+variables[86]*variables[52]
    variables[73] = variables[47]
    variables[70] = variables[71]*(exp(variables[72]/(variables[15]*variables[17]))-exp(variables[73]/(variables[15]*variables[17])))
    variables[76] = variables[50]
    variables[77] = variables[24]+variables[44]
    variables[74] = variables[75]*(exp(variables[76]/(variables[15]*variables[17]))-exp(variables[77]/(variables[15]*variables[17])))
    variables[80] = variables[32]
    variables[81] = variables[29]
    variables[78] = variables[79]*(exp(variables[80]/(variables[15]*variables[17]))-exp(variables[81]/(variables[15]*variables[17])))
    variables[84] = variables[47]
    variables[85] = variables[50]
    variables[82] = variables[83]*(exp(variables[84]/(variables[15]*variables[17]))-exp(variables[85]/(variables[15]*variables[17])))
    variables[0] = variables[54]
    variables[2] = -variables[58]
    variables[4] = -variables[62]
    variables[6] = variables[66]
    variables[8] = variables[74]
    variables[10] = -variables[70]
    variables[28] = -variables[54]+variables[78]
    variables[31] = -variables[78]+variables[58]
    variables[34] = -variables[62]+variables[54]
    variables[37] = -variables[58]+variables[66]
    variables[40] = -variables[70]+variables[62]
    variables[43] = -variables[66]+variables[74]
    variables[46] = -variables[82]+variables[70]
    variables[49] = -variables[74]+variables[82]
    variables[12] = -variables[86]*variables[70]
