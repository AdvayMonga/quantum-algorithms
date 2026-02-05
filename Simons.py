import qiskit
print(qiskit.__version__)

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.circuit import Parameter
from qiskit_ibm_runtime import EstimatorV2 as Estimator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.quantum_info import Pauli, SparsePauliOp
import numpy as np
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
# Simon's algorithm finds a hidden period (secret string s) in a function
# where f(x) = f(y) if and only if x XOR y = s or x = y.
# Exponential speedup over classical algorithms.

# number of qubits
n = int(input("how many qubits? "))

# the secret string s (what we want to find)
# s = 0 means function is one-to-one, s != 0 means two-to-one
secret = np.random.randint(1, 2**n)  # exclude 0 for interesting case
print(f"secret string s: {secret} (binary: {format(secret, f'0{n}b')})")

# initialize the circuit (n input qubits + n output qubits)
qr = QuantumRegister(2*n)
cr = ClassicalRegister(n)
circuitName = 'Simons'
simonCircuit = QuantumCircuit(qr, cr)

# Algorithm

# Step 1: apply hadamard gate to first n qubits (input register)
for qubit in range(n):
    simonCircuit.h(qr[qubit])
simonCircuit.barrier()

# Step 2: apply the oracle f(x)
# copy input to output: |x>|0> -> |x>|x>
for i in range(n):
    simonCircuit.cx(qr[i], qr[n+i])

# apply XOR with secret s if first qubit is 1
# this makes f(x) = f(x XOR s)
for i in range(n):
    if secret & (1 << i):
        simonCircuit.cx(qr[0], qr[n+i])

simonCircuit.barrier()

# Step 3: apply hadamard gate to first n qubits again
for qubit in range(n):
    simonCircuit.h(qr[qubit])
simonCircuit.barrier()

# Step 4: measure the first n qubits
# results will satisfy y dot s = 0 (mod 2)
for i in range(n):
    simonCircuit.measure(qr[i], cr[i])

# run the circuit multiple times to get enough equations
print("\nrunning circuit to find equations y where y dot s = 0...")
simulator = AerSimulator()
compiled = transpile(simonCircuit, simulator)
result = simulator.run(compiled, shots=1024).result()
counts = result.get_counts()
print(f"measurement results: {counts}")

# visualize the circuit
simonCircuit.draw(output='mpl', scale=1.0, interactive=True)
plt.show()
