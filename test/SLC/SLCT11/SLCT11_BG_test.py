# The content of this file was generated using the Python profile of libCellML 0.4.0.

from enum import Enum
from math import *


__version__ = "0.4.0"
LIBCELLML_VERSION = "0.4.0"

STATE_COUNT = 10
VARIABLE_COUNT = 115


class VariableType(Enum):
    VARIABLE_OF_INTEGRATION = 0
    STATE = 1
    CONSTANT = 2
    COMPUTED_CONSTANT = 3
    ALGEBRAIC = 4


VOI_INFO = {"name": "t", "units": "second", "component": "SLCT11_BG", "type": VariableType.VARIABLE_OF_INTEGRATION}

STATE_INFO = [
    {"name": "q_9", "units": "fmol", "component": "SLCT11_BG", "type": VariableType.STATE},
    {"name": "q_10", "units": "fmol", "component": "SLCT11_BG", "type": VariableType.STATE},
    {"name": "q_11", "units": "fmol", "component": "SLCT11_BG", "type": VariableType.STATE},
    {"name": "q_12", "units": "fmol", "component": "SLCT11_BG", "type": VariableType.STATE},
    {"name": "q_13", "units": "fmol", "component": "SLCT11_BG", "type": VariableType.STATE},
    {"name": "q_14", "units": "fmol", "component": "SLCT11_BG", "type": VariableType.STATE},
    {"name": "q_15", "units": "fmol", "component": "SLCT11_BG", "type": VariableType.STATE},
    {"name": "q_16", "units": "fmol", "component": "SLCT11_BG", "type": VariableType.STATE},
    {"name": "q_17", "units": "fmol", "component": "SLCT11_BG", "type": VariableType.STATE},
    {"name": "q_18", "units": "fmol", "component": "SLCT11_BG", "type": VariableType.STATE}
]

VARIABLE_INFO = [
    {"name": "v_Ki", "units": "fmol_per_sec", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_Ki", "units": "fmol", "component": "SLCT11_BG_io", "type": VariableType.CONSTANT},
    {"name": "v_Ko", "units": "fmol_per_sec", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_Ko", "units": "fmol", "component": "SLCT11_BG_io", "type": VariableType.CONSTANT},
    {"name": "v_Nai", "units": "fmol_per_sec", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_Nai", "units": "fmol", "component": "SLCT11_BG_io", "type": VariableType.CONSTANT},
    {"name": "v_Nao", "units": "fmol_per_sec", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_Nao", "units": "fmol", "component": "SLCT11_BG_io", "type": VariableType.CONSTANT},
    {"name": "v_So", "units": "fmol_per_sec", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_So", "units": "fmol", "component": "SLCT11_BG_io", "type": VariableType.CONSTANT},
    {"name": "v_Si", "units": "fmol_per_sec", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_Si", "units": "fmol", "component": "SLCT11_BG_io", "type": VariableType.CONSTANT},
    {"name": "v_Clo", "units": "fmol_per_sec", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_Clo", "units": "fmol", "component": "SLCT11_BG_io", "type": VariableType.CONSTANT},
    {"name": "v_Cli", "units": "fmol_per_sec", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_Cli", "units": "fmol", "component": "SLCT11_BG_io", "type": VariableType.CONSTANT},
    {"name": "mu_Ki", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "R", "units": "J_per_K_per_mol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_Ki", "units": "per_fmol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "T", "units": "kelvin", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_Ko", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "K_Ko", "units": "per_fmol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_Nai", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "K_Nai", "units": "per_fmol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_Nao", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "K_Nao", "units": "per_fmol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_So", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "K_So", "units": "per_fmol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_Si", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "K_Si", "units": "per_fmol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_Clo", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "K_Clo", "units": "per_fmol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_Cli", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "K_Cli", "units": "per_fmol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_9", "units": "fmol_per_sec", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_9", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_9", "units": "per_fmol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_10", "units": "fmol_per_sec", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_10", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_10", "units": "per_fmol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_11", "units": "fmol_per_sec", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_11", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_11", "units": "per_fmol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_12", "units": "fmol_per_sec", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_12", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_12", "units": "per_fmol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_13", "units": "fmol_per_sec", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_13", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_13", "units": "per_fmol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_14", "units": "fmol_per_sec", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_14", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_14", "units": "per_fmol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_15", "units": "fmol_per_sec", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_15", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_15", "units": "per_fmol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_16", "units": "fmol_per_sec", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_16", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_16", "units": "per_fmol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_17", "units": "fmol_per_sec", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_17", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_17", "units": "per_fmol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_18", "units": "fmol_per_sec", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_18", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_18", "units": "per_fmol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_re1", "units": "fmol_per_sec", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re1", "units": "fmol_per_sec", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re1_in", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re1_out", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re2", "units": "fmol_per_sec", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re2", "units": "fmol_per_sec", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re2_in", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re2_out", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re3", "units": "fmol_per_sec", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re3", "units": "fmol_per_sec", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re3_in", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re3_out", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re4", "units": "fmol_per_sec", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re4", "units": "fmol_per_sec", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re4_in", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re4_out", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re5", "units": "fmol_per_sec", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re5", "units": "fmol_per_sec", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re5_in", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re5_out", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re6", "units": "fmol_per_sec", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re6", "units": "fmol_per_sec", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re6_in", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re6_out", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re7", "units": "fmol_per_sec", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re7", "units": "fmol_per_sec", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re7_in", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re7_out", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re8", "units": "fmol_per_sec", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re8", "units": "fmol_per_sec", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re8_in", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re8_out", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re9", "units": "fmol_per_sec", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re9", "units": "fmol_per_sec", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re9_in", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re9_out", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re10", "units": "fmol_per_sec", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re10", "units": "fmol_per_sec", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re10_in", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re10_out", "units": "J_per_mol", "component": "SLCT11_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_9_init", "units": "fmol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_10_init", "units": "fmol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_11_init", "units": "fmol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_12_init", "units": "fmol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_13_init", "units": "fmol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_14_init", "units": "fmol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_15_init", "units": "fmol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_16_init", "units": "fmol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_17_init", "units": "fmol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_18_init", "units": "fmol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT},
    {"name": "F", "units": "C_per_mol", "component": "SLCT11_BG_param", "type": VariableType.CONSTANT}
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
    variables[15] = 1.0
    variables[17] = 8.31
    variables[18] = 1.0
    variables[19] = 293.0
    variables[21] = 1.0
    variables[23] = 1.0
    variables[25] = 1.0
    variables[27] = 1.0
    variables[29] = 1.0
    variables[31] = 1.0
    variables[33] = 1.0
    variables[36] = 1.0
    variables[39] = 1.0
    variables[42] = 1.0
    variables[45] = 1.0
    variables[48] = 1.0
    variables[51] = 1.0
    variables[54] = 1.0
    variables[57] = 1.0
    variables[60] = 1.0
    variables[63] = 1.0
    variables[65] = 1.0
    variables[69] = 1.0
    variables[73] = 1.0
    variables[77] = 1.0
    variables[81] = 1.0
    variables[85] = 1.0
    variables[89] = 1.0
    variables[93] = 1.0
    variables[97] = 1.0
    variables[101] = 1.0
    variables[104] = 1.0
    variables[105] = 1.0
    variables[106] = 1.0
    variables[107] = 1.0
    variables[108] = 1.0
    variables[109] = 1.0
    variables[110] = 1.0
    variables[111] = 1.0
    variables[112] = 1.0
    variables[113] = 1.0
    variables[114] = 96485.0
    states[0] = variables[104]
    states[1] = variables[105]
    states[2] = variables[106]
    states[3] = variables[107]
    states[4] = variables[108]
    states[5] = variables[109]
    states[6] = variables[110]
    states[7] = variables[111]
    states[8] = variables[112]
    states[9] = variables[113]


def compute_computed_constants(variables):
    variables[16] = variables[17]*variables[19]*log(variables[18]*variables[1])
    variables[20] = variables[17]*variables[19]*log(variables[21]*variables[3])
    variables[22] = variables[17]*variables[19]*log(variables[23]*variables[5])
    variables[24] = variables[17]*variables[19]*log(variables[25]*variables[7])
    variables[26] = variables[17]*variables[19]*log(variables[27]*variables[9])
    variables[28] = variables[17]*variables[19]*log(variables[29]*variables[11])
    variables[30] = variables[17]*variables[19]*log(variables[31]*variables[13])
    variables[32] = variables[17]*variables[19]*log(variables[33]*variables[15])


def compute_rates(voi, states, rates, variables):
    variables[35] = variables[17]*variables[19]*log(variables[36]*states[0])
    variables[74] = variables[26]+variables[35]
    variables[41] = variables[17]*variables[19]*log(variables[42]*states[2])
    variables[75] = variables[41]
    variables[72] = variables[73]*(exp(variables[74]/(variables[17]*variables[19]))-exp(variables[75]/(variables[17]*variables[19])))
    variables[53] = variables[17]*variables[19]*log(variables[54]*states[6])
    variables[66] = variables[24]+variables[53]
    variables[67] = variables[35]
    variables[64] = variables[65]*(exp(variables[66]/(variables[17]*variables[19]))-exp(variables[67]/(variables[17]*variables[19])))
    variables[34] = -variables[72]+variables[64]
    rates[0] = variables[34]
    variables[38] = variables[17]*variables[19]*log(variables[39]*states[1])
    variables[70] = variables[38]
    variables[56] = variables[17]*variables[19]*log(variables[57]*states[7])
    variables[71] = variables[22]+variables[56]
    variables[68] = variables[69]*(exp(variables[70]/(variables[17]*variables[19]))-exp(variables[71]/(variables[17]*variables[19])))
    variables[44] = variables[17]*variables[19]*log(variables[45]*states[3])
    variables[78] = variables[44]
    variables[79] = variables[28]+variables[38]
    variables[76] = variables[77]*(exp(variables[78]/(variables[17]*variables[19]))-exp(variables[79]/(variables[17]*variables[19])))
    variables[37] = -variables[68]+variables[76]
    rates[1] = variables[37]
    variables[82] = variables[30]+variables[41]
    variables[47] = variables[17]*variables[19]*log(variables[48]*states[4])
    variables[83] = variables[47]
    variables[80] = variables[81]*(exp(variables[82]/(variables[17]*variables[19]))-exp(variables[83]/(variables[17]*variables[19])))
    variables[40] = -variables[80]+variables[72]
    rates[2] = variables[40]
    variables[50] = variables[17]*variables[19]*log(variables[51]*states[5])
    variables[86] = variables[50]
    variables[87] = variables[32]+variables[44]
    variables[84] = variables[85]*(exp(variables[86]/(variables[17]*variables[19]))-exp(variables[87]/(variables[17]*variables[19])))
    variables[43] = -variables[76]+variables[84]
    rates[3] = variables[43]
    variables[98] = variables[47]
    variables[99] = variables[50]
    variables[96] = variables[97]*(exp(variables[98]/(variables[17]*variables[19]))-exp(variables[99]/(variables[17]*variables[19])))
    variables[46] = -variables[96]+variables[80]
    rates[4] = variables[46]
    variables[49] = -variables[84]+variables[96]
    rates[5] = variables[49]
    variables[59] = variables[17]*variables[19]*log(variables[60]*states[8])
    variables[90] = variables[59]
    variables[91] = variables[20]+variables[53]
    variables[88] = variables[89]*(exp(variables[90]/(variables[17]*variables[19]))-exp(variables[91]/(variables[17]*variables[19])))
    variables[52] = -variables[64]+variables[88]
    rates[6] = variables[52]
    variables[94] = variables[16]+variables[56]
    variables[62] = variables[17]*variables[19]*log(variables[63]*states[9])
    variables[95] = variables[62]
    variables[92] = variables[93]*(exp(variables[94]/(variables[17]*variables[19]))-exp(variables[95]/(variables[17]*variables[19])))
    variables[55] = -variables[92]+variables[68]
    rates[7] = variables[55]
    variables[102] = variables[62]
    variables[103] = variables[59]
    variables[100] = variables[101]*(exp(variables[102]/(variables[17]*variables[19]))-exp(variables[103]/(variables[17]*variables[19])))
    variables[58] = -variables[88]+variables[100]
    rates[8] = variables[58]
    variables[61] = -variables[100]+variables[92]
    rates[9] = variables[61]


def compute_variables(voi, states, rates, variables):
    variables[35] = variables[17]*variables[19]*log(variables[36]*states[0])
    variables[38] = variables[17]*variables[19]*log(variables[39]*states[1])
    variables[41] = variables[17]*variables[19]*log(variables[42]*states[2])
    variables[44] = variables[17]*variables[19]*log(variables[45]*states[3])
    variables[47] = variables[17]*variables[19]*log(variables[48]*states[4])
    variables[50] = variables[17]*variables[19]*log(variables[51]*states[5])
    variables[53] = variables[17]*variables[19]*log(variables[54]*states[6])
    variables[56] = variables[17]*variables[19]*log(variables[57]*states[7])
    variables[59] = variables[17]*variables[19]*log(variables[60]*states[8])
    variables[62] = variables[17]*variables[19]*log(variables[63]*states[9])
    variables[66] = variables[24]+variables[53]
    variables[67] = variables[35]
    variables[64] = variables[65]*(exp(variables[66]/(variables[17]*variables[19]))-exp(variables[67]/(variables[17]*variables[19])))
    variables[70] = variables[38]
    variables[71] = variables[22]+variables[56]
    variables[68] = variables[69]*(exp(variables[70]/(variables[17]*variables[19]))-exp(variables[71]/(variables[17]*variables[19])))
    variables[74] = variables[26]+variables[35]
    variables[75] = variables[41]
    variables[72] = variables[73]*(exp(variables[74]/(variables[17]*variables[19]))-exp(variables[75]/(variables[17]*variables[19])))
    variables[78] = variables[44]
    variables[79] = variables[28]+variables[38]
    variables[76] = variables[77]*(exp(variables[78]/(variables[17]*variables[19]))-exp(variables[79]/(variables[17]*variables[19])))
    variables[82] = variables[30]+variables[41]
    variables[83] = variables[47]
    variables[80] = variables[81]*(exp(variables[82]/(variables[17]*variables[19]))-exp(variables[83]/(variables[17]*variables[19])))
    variables[86] = variables[50]
    variables[87] = variables[32]+variables[44]
    variables[84] = variables[85]*(exp(variables[86]/(variables[17]*variables[19]))-exp(variables[87]/(variables[17]*variables[19])))
    variables[90] = variables[59]
    variables[91] = variables[20]+variables[53]
    variables[88] = variables[89]*(exp(variables[90]/(variables[17]*variables[19]))-exp(variables[91]/(variables[17]*variables[19])))
    variables[94] = variables[16]+variables[56]
    variables[95] = variables[62]
    variables[92] = variables[93]*(exp(variables[94]/(variables[17]*variables[19]))-exp(variables[95]/(variables[17]*variables[19])))
    variables[98] = variables[47]
    variables[99] = variables[50]
    variables[96] = variables[97]*(exp(variables[98]/(variables[17]*variables[19]))-exp(variables[99]/(variables[17]*variables[19])))
    variables[102] = variables[62]
    variables[103] = variables[59]
    variables[100] = variables[101]*(exp(variables[102]/(variables[17]*variables[19]))-exp(variables[103]/(variables[17]*variables[19])))
    variables[0] = -variables[92]
    variables[2] = variables[88]
    variables[4] = variables[68]
    variables[6] = -variables[64]
    variables[8] = -variables[72]
    variables[10] = variables[76]
    variables[12] = -variables[80]
    variables[14] = variables[84]
    variables[34] = -variables[72]+variables[64]
    variables[37] = -variables[68]+variables[76]
    variables[40] = -variables[80]+variables[72]
    variables[43] = -variables[76]+variables[84]
    variables[46] = -variables[96]+variables[80]
    variables[49] = -variables[84]+variables[96]
    variables[52] = -variables[64]+variables[88]
    variables[55] = -variables[92]+variables[68]
    variables[58] = -variables[88]+variables[100]
    variables[61] = -variables[100]+variables[92]
