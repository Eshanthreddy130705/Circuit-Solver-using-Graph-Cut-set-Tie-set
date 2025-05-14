import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# Define symbolic variables
s, t = sp.symbols('s t')

# Define the matrix elements in the Laplace domain
laplace_matrix = [
    [0.5/(s*(1.0e-6*s + 0.0005))],
    [0.5/(s*(1.0e-6*s + 0.0005))],
    [1000.0/(s*(2000.0 + 1000000.0/s))],
    [-1000.0/(s*(2000.0 + 1000000.0/s))]
]

# Compute the inverse Laplace transform for each element
time_domain_matrix = []
for row in laplace_matrix:
    time_row = []
    for elem in row:
        time_elem = sp.inverse_laplace_transform(elem, s, t)
        time_row.append(time_elem)
    time_domain_matrix.append(time_row)

# Print the time-domain functions for verification
for row in time_domain_matrix:
    print(row)

# Convert symbolic expressions to numerical functions for plotting
time_funcs = [sp.lambdify(t, row[0], 'numpy') for row in time_domain_matrix]

# Generate time values for plotting
time_values = np.linspace(0, 0.1, 1000)  # Adjust the time range as needed

# Plot each function
plt.figure(figsize=(10, 6))
for i, func in enumerate(time_funcs, 1):
    plt.plot(time_values, func(time_values), label=f'Function {i}')

plt.xlabel('Time (t)')
plt.ylabel('Amplitude')
plt.title('Inverse Laplace Transforms')
plt.legend()
plt.grid(True)
plt.show()
