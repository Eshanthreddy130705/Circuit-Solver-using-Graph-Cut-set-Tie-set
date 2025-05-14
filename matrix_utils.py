'''entire code helps to get inverse or det of matrices'''
import sympy as sp
import numpy as np
#for the matrix manupulation
from sympy.matrices import Matrix
import warnings
from functools import reduce
from sympy.tensor.functions import shape

warnings.filterwarnings("ignore", category=DeprecationWarning) 
'''used for calculating det as the sum of minors
 multiplied by corresponding elements'''
def getMatrixMinor(m,i,j):
    return m.minor_submatrix(i,j)

def det(m):
    #base case for 2x2 matrix
    if m.shape[0] == 2:
        return m[0,0]*m[1,1]-m[0,1]*m[1,0]

    determinant = 0
    for c in range(m.shape[0]):
        determinant += ((-1)**c)*m[0,c]*det(getMatrixMinor(m,0,c))
        determinant =sp.expand(determinant)
    return determinant
#inverse of the matrix
def inv(m):
    d=det(m)
    mat=sp.zeros(m.shape[0],m.shape[1])
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            mat[i,j]=det(getMatrixMinor(m,i,j))*(np.power(-1,i+j))
            mat[i,j]=sp.expand(mat[i,j])
    mat=mat.T
    mat=mat/d
    return mat

