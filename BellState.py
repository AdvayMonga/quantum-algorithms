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

# Bell States
# There are 4 Bell states
# |B00⟩ = (|00⟩ + |11⟩)/√2
# |B01⟩ = (|00⟩ - |11⟩)/√2
# |B10⟩ = (|01⟩ + |10⟩)/√2
# |B11⟩ = (|01⟩ - |10⟩)/√2

# Bell State |B00⟩ = (|00⟩ + |11⟩)/√2
B00 = QuantumCircuit(2, 2)
B00.h(0)
B00.cx(0, 1)

# Bell State |B01⟩ = (|00⟩ - |11⟩)/√2
B01 = QuantumCircuit(2, 2)
B01.h(0)
B01.cx(0, 1)
B01.z(0)  # adds phase to flip + to -

# Bell State |B10⟩ = (|01⟩ + |10⟩)/√2
B10 = QuantumCircuit(2, 2)
B10.h(0)
B10.cx(0, 1)
B10.x(1)  # flips second qubit

# Bell State |B11⟩ = (|01⟩ - |10⟩)/√2
B11 = QuantumCircuit(2, 2)
B11.h(0)
B11.cx(0, 1)
B11.x(1)
B11.z(0)

# Draw all 4 Bell states
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
B00.draw(output='mpl', ax=axes[0,0])
axes[0,0].set_title('|B00⟩ = (|00⟩ + |11⟩)/√2')

B01.draw(output='mpl', ax=axes[0,1])
axes[0,1].set_title('|B01⟩ = (|00⟩ - |11⟩)/√2')

B10.draw(output='mpl', ax=axes[1,0])
axes[1,0].set_title('|B10⟩ = (|01⟩ + |10⟩)/√2')

B11.draw(output='mpl', ax=axes[1,1])
axes[1,1].set_title('|B11⟩ = (|01⟩ - |10⟩)/√2')

plt.tight_layout()
plt.show()