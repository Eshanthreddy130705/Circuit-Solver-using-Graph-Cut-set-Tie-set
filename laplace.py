import sympy as sp
import numpy as np
from sympy.matrices import Matrix
from sympy.core.rules import Transform
from sympy import Float
s=sp.Symbol('s')

def calculate_LT_(V_I):
    if len(V_I)==2:
        return V_I[0]/s
    # else:
    #     w=2*np.pi*V_I[1]
    #     w=np.round(w,5)
    #     a=np.pi*V_I[2]/180
    #     return (V_I[0]*(w*np.round(np.cos(a),5)+s*np.round(np.sin(a),5))/(s**2+w**2))

def calculate_VI(V_I):
    mat=Matrix(np.zeros(len(V_I)))
    for i in range(len(V_I)):
        mat[i]=calculate_LT_(V_I[i])
    return mat

def calculate_C(C):
    mat=Matrix(np.zeros(len(C)))
    for i in range(len(C)):
        if C[i]==0:
            mat[i]=0
        else:
            mat[i]=1/(s*C[i])
    return mat

def calculate_L(L):
    mat=Matrix(np.zeros(len(L)))
    for i in range(len(L)):
        mat[i]=s*L[i]
    return mat

def calculate_R(R):
    mat=Matrix(np.zeros(len(R)))
    for i in range(len(R)):
        mat[i]=R[i]
    return mat

def LT(R_list,C_list,L_list,V_list,I_list,branch_src_list,branch_dest_list):
    R_mat= calculate_R(R_list)
    C_mat=calculate_C(C_list)
    L_mat=calculate_L(L_list)
    V_mat=calculate_VI(V_list)
    I_mat=calculate_VI(I_list)
    temp1=[]
    temp2=[]
    for V in V_mat:
        temp1.append(V.xreplace(Transform(lambda x: x.round(4), lambda x: isinstance(x,Float))))
    for I in I_mat:
        temp2.append(I.xreplace(Transform(lambda x: x.round(4), lambda x: isinstance(x,Float))))
    I_mat=Matrix(temp2)
    V_mat=Matrix(temp1)
    return R_mat,C_mat,L_mat,V_mat,I_mat
