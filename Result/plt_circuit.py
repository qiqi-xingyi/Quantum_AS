# --*-- conding:utf-8 --*--
# @Time : 1/28/25 2:13 AM
# @Author : Yuqi Zhang
# @Email : yzhan135@kent.edu
# @File : plt_circuit.py

# from qiskit.circuit.library import EfficientSU2
#
# num_qubits = 5
# reps = 3
# entanglement = "linear"
#
# if __name__ == '__main__':
#
#     qc = EfficientSU2(
#         num_qubits=num_qubits,
#         reps=reps,
#         entanglement=entanglement,
#     )
#
#     print(f"Depth（reps={reps}）:", qc.depth())

from qiskit.circuit.library import EfficientSU2
from qiskit.visualization import circuit_drawer
import matplotlib.pyplot as plt

# 创建 EfficientSU2 电路
num_qubits = 15  # 指定量子比特数
entanglement = 'linear'
reps = 3  # 指定循环层数

if __name__ == '__main__':

    efficient_su2_circuit = EfficientSU2(num_qubits=num_qubits)

    decomposed_circuit = efficient_su2_circuit.decompose()

    print(f"Depth（reps={reps}）:", decomposed_circuit.depth())

    circuit_image = circuit_drawer(
        decomposed_circuit,
        output='mpl',  # 使用 matplotlib 方式输出
        fold=-1,  # 不换行，显示完整电路
        idle_wires=True,  # 显示所有闲置的量子比特
        cregbundle=True,  # 不合并经典位，逐个位显示
        plot_barriers=True,  # 显示电路中的障碍
        # style='iqx'        # 如果想使用特定主题，可以打开此行
    )
    plt.show()

    circuit_image.savefig("efficient_su2_circuit.png",dpi=600)