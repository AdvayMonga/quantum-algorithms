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

# The Deutsch-Josza algorithm is a quantum algorithm that determines
# whether a function is "balanced" (half 0s, half 1s) or
# "constant" (all same output) in just one evaluation.

# number of qubits
n = int(input("how many qubits? "))

# constant or balanced - randomly selected
oracleType, oracleValue = np.random.randint(2), np.random.randint(2)
if oracleType == 0:
  print('the oracle returns a constant value', oracleValue)
else:
  print("the oracle returns a balanced function")
  a = np.random.randint(1,2**n)

# initalize the circuit
qr = QuantumRegister(n+1)
cr = ClassicalRegister(n)
circuitName = 'DeutschJozsa'
djCircuit=QuantumCircuit(qr,cr) # circuit object

# Algorithm

# Step 1: apply not gate to last qubit
djCircuit.x(qr[n])

# Step 2: apply hadamard gate to all qubits
for qubit in range(n+1):
  djCircuit.h(qr[qubit])
djCircuit.barrier() # only for visualization

# Step 3: apply the function
if oracleType==0:
  if oracleValue==1:
    djCircuit.x(qr[n]) #if the function is constant at 1, apply this function
  else:
    djCircuit.id(qr[n]) #if the function is constant at 0, apply this function

# if the function is balanced instead of constant
else:
  for i in range(n):
    if (a & (1<<i)):
      djCircuit.cx(qr[i],qr[n])

djCircuit.barrier() # only for visualization

# Step 4: apply hadamard gate to first n qubits
for i in range(n):
  djCircuit.h(qr[i])

djCircuit.barrier() # only for visualization

# Step 5: measure the first n qubits
for i in range(n):
  djCircuit.measure(qr[i],cr[i])

# visualize the circuit
djCircuit.draw(output='mpl', scale=1.0, interactive=True)
plt.show()