import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from calc import calculate,matrices
from graph import graph,branch 
from laplace import LT
from utils import reorder,get_args,from_txt

np.set_printoptions(linewidth=np.inf)

def run_solver(filename):
 t=sp.Symbol('t')
 s=sp.Symbol('s')

 R_list,C_list,L_list,V_list,I_list,branch_src_list,branch_dest_list=from_txt(filename)
 g=graph()
 g.generate(branch_src_list,branch_dest_list)
 g.generate_matrix()
 t=g.generate_tree()
 l=g.get_links()
 loops=g.get_loops()
 R_list,L_list,C_list,V_list,I_list=reorder(g,R_list,C_list,L_list,V_list,I_list,branch_src_list,branch_dest_list)
 R_LT,C_LT,L_LT,V_LT,I_LT=LT(R_list,C_list,L_list,V_list,I_list,branch_src_list,branch_dest_list)
 B_f,Q_f,Z,Y=matrices(t,loops,R_LT,C_LT,L_LT)
 I=calculate(B_f,Q_f,Z,Y,V_LT,I_LT,len(g.tree))


 return I,Z,V_LT
def voltage(I,Z,V_LT):
#computing voltage with the help of I and z
    vol_list2= np.array(V_LT).reshape(-1, 1)
    return Z*I+vol_list2
s, t = sp.symbols('s t')
#finding the inverse laplace and plotting themj in time domain
def plot_laplace_transform(V, I):
    def compute_time_domain(vector):
        time_domain_funcs = []
        for elem in vector:
            time_elem = sp.inverse_laplace_transform(elem, s, t)
            real_time_element=sp.re(time_elem)
            time_domain_funcs.append(sp.lambdify(t, real_time_element, 'numpy'))
        return time_domain_funcs

    
    time_funcs_V = compute_time_domain(V)
    time_funcs_I = compute_time_domain(I)

    
    time_values = np.linspace(0, 1, 1000)

    # Plot voltage functions
    plt.figure(figsize=(12, 12))
    for i, func in enumerate(time_funcs_V, 1):
        plt.subplot(len(V) + len(I), 1, i)
        plt.plot(time_values, func(time_values), label=f'Voltage{i}')
        plt.xlabel('Time (t)')
        plt.ylabel('Amplitude')
        plt.title(f'Voltage{i}')
        plt.legend()
        plt.grid(True)

    # Plot current functions
    for i, func in enumerate(time_funcs_I, len(V) + 1):
        plt.subplot(len(V) + len(I), 1, i)
        plt.plot(time_values, func(time_values), label=f'Current{i - len(V)}')
        plt.xlabel('Time (t)')
        plt.ylabel('Amplitude')
        plt.title(f' Current{i - len(V)}')
        plt.legend()
        plt.grid(True)

    plt.tight_layout() 
    plt.subplots_adjust(hspace=2)
    plt.show()

if __name__=="__main__":
    args = get_args()
    I,Z,V_LT=run_solver(r"C:/semester 3/project/Circuit-Solver-main/project vs code/test_data.txt")
    V=voltage(I,Z,V_LT)
    #print(V,I)
    #print("impedenccce",Z)
    #print(V_list)
# Define symbolic variables
plot_laplace_transform(V,I)

# Function to compute inverse Laplace transform and plot results
