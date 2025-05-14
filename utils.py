#for operating with command line inputs
import argparse
from argparse import ArgumentParser
import pandas as pd
from shared_utils import check_float
from conv import convert,convert_VI
#aligning voltage and current direction with that pf branch
def correct_VI(V_list,I_list,branch_src_list,branch_dest_list):
    for i in range(len(branch_src_list)):
        if branch_dest_list[i]<branch_src_list[i]:
            V_list[i][0]=-V_list[i][0]
            I_list[i][0]=-I_list[i][0]
    return V_list,I_list

def print_list(l):
    for item in l:
        print("{:.3e}".format(item))

def print_VI(l):
    for item in l:
        if len(item)==2:
            print("{:.3e}".format(item[0]))
        else:
            print("{:.3e},".format(item[0]),"{:.3e}<".format(item[1]),"{:.3e}".format(item[2]))
#combines the nodes lists into pairs(source node,dest code)
def combine(l1,l2):
    return list(map(lambda x, y:(min(x,y),max(x,y)), l1, l2))
#for creating lists for resistances,c,v,i.
def create_list(src,g,list):
    src=src.copy()
    l=[]
    for b in g.tree:
        for c in range(len(src)):
            if b[0]==src[c][0] and b[1]==src[c][1]:
                l.append(list[c])
                del src[c]
                del list[c]
                break
    for b in g.links:
        for c in range(len(src)):
            if b[0]==src[c][0] and b[1]==src[c][1]:
                l.append(list[c])
                del src[c]
                del list[c]
                # print(R_list)
                break
    return l

def RLCVI(src,g,R_list,L_list,C_list,V_list,I_list):
    R=create_list(src,g,R_list)
    L=create_list(src,g,L_list)
    C=create_list(src,g,C_list)
    V=create_list(src,g,V_list)
    I=create_list(src,g,I_list)
    return R,L,C,V,I

def reorder(g,R_list,C_list,L_list,V_list,I_list,branch_src_list,branch_dest_list):
    V_list,I_list=correct_VI(V_list,I_list,branch_src_list,branch_dest_list)
    temp=combine(branch_src_list,branch_dest_list)
    return RLCVI(temp,g,R_list,L_list,C_list,V_list,I_list)

def get_args():
    parser = ArgumentParser()
    parser.add_argument(
        "--file_name",
        "-file",
        default="input/test_data.txt",
        help="The name of file containing input. Default: test_data.txt")
    return parser.parse_args()
#taking input from text file 
def from_txt(file):
    X=pd.read_csv(file,sep=' ')
    R_list=[]
    C_list=[]
    L_list=[]
    V_list=[]
    I_list=[]
    branch_src_list=X['Branch_origin'].to_numpy()
    branch_dest_list=X['Branch_dest'].to_numpy()
    convert(X['R'],R_list)
    convert(X['C'],C_list)
    convert(X['L'],L_list)
    convert_VI(X['V'],V_list)
    convert_VI(X['I'],I_list)
    return R_list,C_list,L_list,V_list,I_list,branch_src_list,branch_dest_list