import numpy as np
from sympy import *
from scipy.linalg import null_space
import sympy as sym
init_printing(use_unicode=True)
x, y, z = symbols("x y z")
expr = x**4 - 4*x**3 + 4*x**2 - 2*x + 3
replacements = [(x**i, y**i) for i in range(5) if i % 2 == 0]
expr.subs(replacements)
newexpr=expr.subs(replacements)
a=factor(x**3 - x**2 + x - 1)

N = np.array([[-1, 1],[1, -1]])
K = null_space(N)
N = np.array([[-1, 1, 0, 0],[1, -1, -1, 1],[0, 0, 1, -1]])
K = null_space(N)
cycle=len(K[0,:])
M = Matrix([[-1, 1, 0, 0],[1, -1, -1, 1],[0, 0, 1, -1]])
M.nullspace()
pprint(M.nullspace(), use_unicode=True)
#-4*x**3 - 2*x + y**4 + 4*y**2 + 3
N_cd=Matrix([[1, 0, -1, 0],[0, -1, 1, 0],[-1, 0, 0, 1],[0, 1, 0, -1]])
kappa_1, kappa_2, kappa_3, kappa_4 = symbols("kappa_1 kappa_2 kappa_3 kappa_4")
K_1, K_2, K_3, K_4,K_5,K_6 = symbols("K_1 K_2 K_3 K_4 K_5 K_6")
q_1, q_2, q_3, q_4,q_5,q_6 = symbols("q_1 q_2 q_3 q_4 q_5 q_6")
E = symbols("E")
kappa=Matrix([[kappa_1, 0, 0, 0],[0, kappa_2, 0, 0],[0, 0, kappa_3, 0],[0, 0, 0, kappa_4]])
kappa=diag(kappa_1, kappa_2, kappa_3, kappa_4)
B_f=Matrix([[1, 0, 0, 0],[0, K_2*q_2, 0, 0],[0, 0, 1, 0],[0, 0, 0, 1]])
B_r=Matrix([[K_1*q_1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 1, 0],[0, 0, 0, 1]])
N_cd_r=Matrix([[1, 0, 0, 0],[0, 0, 1, 0],[0, 0, 0, 1],[0, 1, 0, 0]])
N_cd_f=Matrix([[0, 0, 1, 0],[0, 1, 0, 0],[1, 0, 0, 0],[0, 0, 0, 1]])
K_cd =Matrix([[K_3, 0, 0, 0],[0, K_4, 0, 0],[0, 0, K_5, 0],[0, 0, 0, K_6]])
K_cd=diag(K_3, K_4, K_5, K_6)
q_cd=Matrix([[q_3],[q_4],[q_5],[q_6]])
b= Matrix([0, 0, 0, E ])

M_ss = N_cd*(kappa*(B_f*N_cd_f.T-B_r*N_cd_r.T)*K_cd)
M_G = Matrix([[1, 1, 1, 1]])
M_ss_red=M_ss[0:3,:]
M=M_ss_red.col_join(M_G)
q = (M.LUsolve(b))
a = factor(q[0])
print(a)

