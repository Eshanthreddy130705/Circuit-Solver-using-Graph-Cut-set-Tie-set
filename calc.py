import sympy as sp
import numpy as np
from sympy.matrices import Matrix

from matrix_utils import inv

def reciprocal(a):
    if a==0:
        return a
    return 1/a
#gives the currrent direction for the loop elements in notes odf see d,e,f
def B_t(tree,loop):
    b=len(tree)+len(loop)
    n=len(tree)
    mat=np.zeros((b-n,n),dtype=int)
    for i in range(len(loop)):
        for j in range(len(tree)):
            mat[i][j]=tree[j].get_dir(loop[i])
    return mat
#concatinating with identity matrix give fundamental cut set matreix
def B_f(mat):
    return np.concatenate((mat,np.eye(mat.shape[0],dtype=int)),axis=1)
#transposing fundamental cut set and concatinating guves relation between branch voltage and node voltage 
def Q_f(B_t):
    Q_l=-B_t.transpose()
    Q_l=Q_l.astype(int)
    return np.concatenate((np.eye(Q_l.shape[0],dtype=int),Q_l),axis=1)

def generate_Z(R_list,C_list,L_list):
    Z=Matrix(len(R_list),len(R_list),lambda i,j: R_list[i]+C_list[i]+L_list[i] if i==j else 0)
    return Z

def generate_Y(R_list,C_list,L_list):
    Y=Matrix(len(R_list),len(R_list),lambda i,j: reciprocal(R_list[i])+reciprocal(C_list[i])+reciprocal(L_list[i]) if i==j else 0)
    return Y 

def matrices(tree,loop,R_list,C_list,L_list):
    '''
    Returns (B_f,Q_f,Z_f,Y_f)
    '''
    Bt=B_t(tree,loop)
    B_mat=B_f(Bt)
    Z=generate_Z(R_list,C_list,L_list)
    Y=generate_Y(R_list,C_list,L_list)
    return (B_mat,Q_f(Bt),Z,Y)

def calculate(B,Q,Z,Y,Vg,Ig,n):
    s=sp.Symbol('s')
    Vg=Matrix(Vg)
    Vgt=Matrix(Vg[0:n])
    Vgl=Matrix(Vg[n:])
    Ig=Matrix(Ig)
    Igt=Matrix(Ig[0:n])
    Igl=Matrix(Ig[n:])
    Bf=Matrix(B)
    Qf=Matrix(Q)
    #impedence matrix
    Zf=Bf*Z*Bf.T
    #relation (equation)
    E=Bf*(Vg+Z*Bf.T*Igl-Z*Ig)
    if Zf.shape[0]>2: 
        Il=(inv(Zf))*E
    else:
        Il=(Zf.inv('ADJ'))*E
        #link currents to toatalo
    I=Bf.T*Il
    Yf=Qf*Y*Qf.T
    return I
    # J=Qf*(Ig+Y*Qf.T*Vgt-Y*Vg)
    # if Yf.shape[0]>2:
    #     Vt=(inv(Yf))*J
    # else:
    #     Vt=(Yf.inv('ADJ'))*J
    # V=Qf.T*Vt
    # return V,I