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

# Grover's algorithm finds a marked item in an unstructured database
# with quadratic speedup over classical search.
# For N items, classical needs O(N) queries, Grover needs O(sqrt(N)).

# number of qubits
n = 2

# the secret state we want to find (randomly selected)
secret = np.random.randint(0, 2**n)
print(f"searching for state: {secret} (binary: {format(secret, f'0{n}b')})")

# optimal number of iterations for grover's algorithm
num_iterations = int(np.floor(np.pi/4 * np.sqrt(2**n)))
print(f"number of grover iterations: {num_iterations}")

# initialize the circuit
qr = QuantumRegister(n)
cr = ClassicalRegister(n)
circuitName = 'Grovers'
groverCircuit = QuantumCircuit(qr, cr)

# Algorithm

# Step 1: apply hadamard gate to all qubits (create superposition)
for qubit in range(n):
    groverCircuit.h(qr[qubit])
groverCircuit.barrier()

# repeat the grover iteration optimal number of times
for iteration in range(num_iterations):

    # Step 2: apply the oracle (marks the secret state with negative phase)
    # flip qubits where secret bit is 0
    for i in range(n):
        if not (secret & (1 << i)):
            groverCircuit.x(qr[i])

    # multi-controlled Z gate (marks the state)
    groverCircuit.h(qr[n-1])
    groverCircuit.mcx(list(range(n-1)), n-1)  # multi-controlled X
    groverCircuit.h(qr[n-1])

    # unflip the qubits
    for i in range(n):
        if not (secret & (1 << i)):
            groverCircuit.x(qr[i])

    groverCircuit.barrier()

    # Step 3: apply the diffusion operator (amplifies marked state)
    # apply hadamard to all qubits
    for qubit in range(n):
        groverCircuit.h(qr[qubit])

    # apply X to all qubits
    for qubit in range(n):
        groverCircuit.x(qr[qubit])

    # multi-controlled Z gate
    groverCircuit.h(qr[n-1])
    groverCircuit.mcx(list(range(n-1)), n-1)
    groverCircuit.h(qr[n-1])

    # apply X to all qubits
    for qubit in range(n):
        groverCircuit.x(qr[qubit])

    # apply hadamard to all qubits
    for qubit in range(n):
        groverCircuit.h(qr[qubit])

    groverCircuit.barrier()

# Step 4: measure all qubits
for i in range(n):
    groverCircuit.measure(qr[i], cr[i])

# visualize the circuit
groverCircuit.draw(output='mpl', scale=0.25, interactive=True)
plt.show()
