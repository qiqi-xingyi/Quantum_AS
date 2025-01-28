# --*-- conding:utf-8 --*--
# @Time : 1/28/25 2:13 AM
# @Author : Yuqi Zhang
# @Email : yzhan135@kent.edu
# @File : Test.py

from qiskit.circuit.library import EfficientSU2

num_qubits = 5
reps = 3
entanglement = "linear"

if __name__ == '__main__':

    qc = EfficientSU2(
        num_qubits=num_qubits,
        reps=reps,
        entanglement=entanglement,
    )

    print(f"Depth（reps={reps}）:", qc.depth())