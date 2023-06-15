# The content of this file was generated using the Python profile of libCellML 0.4.0.

from enum import Enum
from math import *


__version__ = "0.4.0"
LIBCELLML_VERSION = "0.4.0"

STATE_COUNT = 6
VARIABLE_COUNT = 71


class VariableType(Enum):
    VARIABLE_OF_INTEGRATION = 0
    STATE = 1
    CONSTANT = 2
    COMPUTED_CONSTANT = 3
    ALGEBRAIC = 4


VOI_INFO = {"name": "t", "units": "second", "component": "SLCT5_BG", "type": VariableType.VARIABLE_OF_INTEGRATION}

STATE_INFO = [
    {"name": "q_5", "units": "fmol", "component": "SLCT5_BG", "type": VariableType.STATE},
    {"name": "q_6", "units": "fmol", "component": "SLCT5_BG", "type": VariableType.STATE},
    {"name": "q_7", "units": "fmol", "component": "SLCT5_BG", "type": VariableType.STATE},
    {"name": "q_8", "units": "fmol", "component": "SLCT5_BG", "type": VariableType.STATE},
    {"name": "q_9", "units": "fmol", "component": "SLCT5_BG", "type": VariableType.STATE},
    {"name": "q_10", "units": "fmol", "component": "SLCT5_BG", "type": VariableType.STATE}
]

VARIABLE_INFO = [
    {"name": "v_Nao", "units": "fmol_per_sec", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_Nao", "units": "fmol", "component": "SLCT5_BG_io", "type": VariableType.CONSTANT},
    {"name": "v_Nai", "units": "fmol_per_sec", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_Nai", "units": "fmol", "component": "SLCT5_BG_io", "type": VariableType.CONSTANT},
    {"name": "v_HCO3o", "units": "fmol_per_sec", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_HCO3o", "units": "fmol", "component": "SLCT5_BG_io", "type": VariableType.CONSTANT},
    {"name": "v_HCO3i", "units": "fmol_per_sec", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_HCO3i", "units": "fmol", "component": "SLCT5_BG_io", "type": VariableType.CONSTANT},
    {"name": "I_m", "units": "fA", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "q_m", "units": "fC", "component": "SLCT5_BG_io", "type": VariableType.CONSTANT},
    {"name": "mu_Nao", "units": "J_per_mol", "component": "SLCT5_BG", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "R", "units": "J_per_K_per_mol", "component": "SLCT5_BG_param", "type": VariableType.CONSTANT},
    {"name": "K_Nao", "units": "per_fmol", "component": "SLCT5_BG_param", "type": VariableType.CONSTANT},
    {"name": "T", "units": "kelvin", "component": "SLCT5_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_Nai", "units": "J_per_mol", "component": "SLCT5_BG", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "K_Nai", "units": "per_fmol", "component": "SLCT5_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_HCO3o", "units": "J_per_mol", "component": "SLCT5_BG", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "K_HCO3o", "units": "per_fmol", "component": "SLCT5_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_HCO3i", "units": "J_per_mol", "component": "SLCT5_BG", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "K_HCO3i", "units": "per_fmol", "component": "SLCT5_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_5", "units": "fmol_per_sec", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_5", "units": "J_per_mol", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_5", "units": "per_fmol", "component": "SLCT5_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_6", "units": "fmol_per_sec", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_6", "units": "J_per_mol", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_6", "units": "per_fmol", "component": "SLCT5_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_7", "units": "fmol_per_sec", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_7", "units": "J_per_mol", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_7", "units": "per_fmol", "component": "SLCT5_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_8", "units": "fmol_per_sec", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_8", "units": "J_per_mol", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_8", "units": "per_fmol", "component": "SLCT5_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_9", "units": "fmol_per_sec", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_9", "units": "J_per_mol", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_9", "units": "per_fmol", "component": "SLCT5_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_10", "units": "fmol_per_sec", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_10", "units": "J_per_mol", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "K_10", "units": "per_fmol", "component": "SLCT5_BG_param", "type": VariableType.CONSTANT},
    {"name": "V_m", "units": "volt", "component": "SLCT5_BG", "type": VariableType.COMPUTED_CONSTANT},
    {"name": "C_m", "units": "fF", "component": "SLCT5_BG_param", "type": VariableType.CONSTANT},
    {"name": "v_re1", "units": "fmol_per_sec", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re1", "units": "fmol_per_sec", "component": "SLCT5_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re1_in", "units": "J_per_mol", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re1_out", "units": "J_per_mol", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re2", "units": "fmol_per_sec", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re2", "units": "fmol_per_sec", "component": "SLCT5_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re2_in", "units": "J_per_mol", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re2_out", "units": "J_per_mol", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re3", "units": "fmol_per_sec", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re3", "units": "fmol_per_sec", "component": "SLCT5_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re3_in", "units": "J_per_mol", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re3_out", "units": "J_per_mol", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re4", "units": "fmol_per_sec", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re4", "units": "fmol_per_sec", "component": "SLCT5_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re4_in", "units": "J_per_mol", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re4_out", "units": "J_per_mol", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re5", "units": "fmol_per_sec", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re5", "units": "fmol_per_sec", "component": "SLCT5_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re5_in", "units": "J_per_mol", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re5_out", "units": "J_per_mol", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "v_re6", "units": "fmol_per_sec", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "kappa_re6", "units": "fmol_per_sec", "component": "SLCT5_BG_param", "type": VariableType.CONSTANT},
    {"name": "mu_re6_in", "units": "J_per_mol", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "mu_re6_out", "units": "J_per_mol", "component": "SLCT5_BG", "type": VariableType.ALGEBRAIC},
    {"name": "F", "units": "C_per_mol", "component": "SLCT5_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_5_init", "units": "fmol", "component": "SLCT5_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_6_init", "units": "fmol", "component": "SLCT5_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_7_init", "units": "fmol", "component": "SLCT5_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_8_init", "units": "fmol", "component": "SLCT5_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_9_init", "units": "fmol", "component": "SLCT5_BG_param", "type": VariableType.CONSTANT},
    {"name": "q_10_init", "units": "fmol", "component": "SLCT5_BG_param", "type": VariableType.CONSTANT}
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
    variables[11] = 8.31
    variables[12] = 1.0
    variables[13] = 293.0
    variables[15] = 1.0
    variables[17] = 1.0
    variables[19] = 1.0
    variables[22] = 1.0
    variables[25] = 1.0
    variables[28] = 1.0
    variables[31] = 1.0
    variables[34] = 1.0
    variables[37] = 1.0
    variables[39] = 1.0
    variables[41] = 1.0
    variables[45] = 1.0
    variables[49] = 1.0
    variables[53] = 1.0
    variables[57] = 1.0
    variables[61] = 1.0
    variables[64] = 96485.0
    variables[65] = 1.0
    variables[66] = 1.0
    variables[67] = 1.0
    variables[68] = 1.0
    variables[69] = 1.0
    variables[70] = 1.0
    states[0] = variables[65]
    states[1] = variables[66]
    states[2] = variables[67]
    states[3] = variables[68]
    states[4] = variables[69]
    states[5] = variables[70]


def compute_computed_constants(variables):
    variables[10] = variables[11]*variables[13]*log(variables[12]*variables[1])
    variables[14] = variables[11]*variables[13]*log(variables[15]*variables[3])
    variables[16] = variables[11]*variables[13]*log(variables[17]*variables[5])
    variables[18] = variables[11]*variables[13]*log(variables[19]*variables[7])
    variables[38] = variables[9]/variables[39]


def compute_rates(voi, states, rates, variables):
    variables[21] = variables[11]*variables[13]*log(variables[22]*states[0])
    variables[50] = variables[16]+variables[21]
    variables[27] = variables[11]*variables[13]*log(variables[28]*states[2])
    variables[51] = variables[27]
    variables[48] = variables[49]*(exp(variables[50]/(variables[11]*variables[13]))-exp(variables[51]/(variables[11]*variables[13])))
    variables[33] = variables[11]*variables[13]*log(variables[34]*states[4])
    variables[42] = variables[10]+variables[33]+variables[64]*variables[38]
    variables[43] = variables[21]
    variables[40] = variables[41]*(exp(variables[42]/(variables[11]*variables[13]))-exp(variables[43]/(variables[11]*variables[13])))
    variables[20] = -variables[48]+variables[40]
    rates[0] = variables[20]
    variables[24] = variables[11]*variables[13]*log(variables[25]*states[1])
    variables[46] = variables[24]
    variables[36] = variables[11]*variables[13]*log(variables[37]*states[5])
    variables[47] = variables[14]+variables[36]
    variables[44] = variables[45]*(exp(variables[46]/(variables[11]*variables[13]))-exp(variables[47]/(variables[11]*variables[13])))
    variables[30] = variables[11]*variables[13]*log(variables[31]*states[3])
    variables[54] = variables[30]
    variables[55] = variables[18]+variables[24]
    variables[52] = variables[53]*(exp(variables[54]/(variables[11]*variables[13]))-exp(variables[55]/(variables[11]*variables[13])))
    variables[23] = -variables[44]+variables[52]
    rates[1] = variables[23]
    variables[58] = variables[27]
    variables[59] = variables[30]
    variables[56] = variables[57]*(exp(variables[58]/(variables[11]*variables[13]))-exp(variables[59]/(variables[11]*variables[13])))
    variables[26] = -variables[56]+variables[48]
    rates[2] = variables[26]
    variables[29] = -variables[52]+variables[56]
    rates[3] = variables[29]
    variables[62] = variables[36]
    variables[63] = variables[33]
    variables[60] = variables[61]*(exp(variables[62]/(variables[11]*variables[13]))-exp(variables[63]/(variables[11]*variables[13])))
    variables[32] = -variables[40]+variables[60]
    rates[4] = variables[32]
    variables[35] = -variables[60]+variables[44]
    rates[5] = variables[35]


def compute_variables(voi, states, rates, variables):
    variables[21] = variables[11]*variables[13]*log(variables[22]*states[0])
    variables[24] = variables[11]*variables[13]*log(variables[25]*states[1])
    variables[27] = variables[11]*variables[13]*log(variables[28]*states[2])
    variables[30] = variables[11]*variables[13]*log(variables[31]*states[3])
    variables[33] = variables[11]*variables[13]*log(variables[34]*states[4])
    variables[36] = variables[11]*variables[13]*log(variables[37]*states[5])
    variables[42] = variables[10]+variables[33]+variables[64]*variables[38]
    variables[43] = variables[21]
    variables[40] = variables[41]*(exp(variables[42]/(variables[11]*variables[13]))-exp(variables[43]/(variables[11]*variables[13])))
    variables[46] = variables[24]
    variables[47] = variables[14]+variables[36]
    variables[44] = variables[45]*(exp(variables[46]/(variables[11]*variables[13]))-exp(variables[47]/(variables[11]*variables[13])))
    variables[50] = variables[16]+variables[21]
    variables[51] = variables[27]
    variables[48] = variables[49]*(exp(variables[50]/(variables[11]*variables[13]))-exp(variables[51]/(variables[11]*variables[13])))
    variables[54] = variables[30]
    variables[55] = variables[18]+variables[24]
    variables[52] = variables[53]*(exp(variables[54]/(variables[11]*variables[13]))-exp(variables[55]/(variables[11]*variables[13])))
    variables[58] = variables[27]
    variables[59] = variables[30]
    variables[56] = variables[57]*(exp(variables[58]/(variables[11]*variables[13]))-exp(variables[59]/(variables[11]*variables[13])))
    variables[62] = variables[36]
    variables[63] = variables[33]
    variables[60] = variables[61]*(exp(variables[62]/(variables[11]*variables[13]))-exp(variables[63]/(variables[11]*variables[13])))
    variables[0] = -variables[40]
    variables[2] = variables[44]
    variables[4] = -variables[48]
    variables[6] = variables[52]
    variables[20] = -variables[48]+variables[40]
    variables[23] = -variables[44]+variables[52]
    variables[26] = -variables[56]+variables[48]
    variables[29] = -variables[52]+variables[56]
    variables[32] = -variables[40]+variables[60]
    variables[35] = -variables[60]+variables[44]
    variables[8] = -variables[64]*variables[40]
