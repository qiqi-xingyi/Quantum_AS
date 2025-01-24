# --*-- conding:utf-8 --*--
# @Time : 1/24/25 12:47 AM
# @Author : Yuqi Zhang
# @Email : yzhan135@kent.edu
# @File : plt_Affinity.py

import os
import re
import matplotlib.pyplot as plt
import numpy as np

# 假设这 7 个子文件夹的名字如下
subfolders = [
    "docking_output_1a9m",
    "docking_output_1fkn",
    "docking_output_1qin",
    "docking_output_2xxx",
    "docking_output_3ans",
    "docking_output_3b26",
    "docking_output_6mu3"
]

if __name__ == '__main__':
    plt.rcParams['font.family'] = 'Arial'

    for folder in subfolders:
        file_path = os.path.join(folder, "summary_results.txt")

        # 定义存储 Quantum / AF3 Affinity 数据的列表
        quantum_affinity = []
        af3_affinity = []

        # 读取文件内容
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # 找到 Quantum Results: 和 AF3 Results: 的起始行索引
        q_start = None
        a_start = None
        for i, line in enumerate(lines):
            if "Quantum Results:" in line:
                q_start = i + 1  # 下面 20 行是 Quantum 的数据
            if "AF3 Results:" in line:
                a_start = i + 1  # 下面 20 行是 AF3 的数据

        # 使用正则表达式解析行中 Affinity、RMSD Lower、RMSD Upper 的数值
        pattern = r"Affinity\s*=\s*([-0-9\.]+).*Lower Bound\s*=\s*([-0-9\.]+).*Upper Bound\s*=\s*([-0-9\.]+)"

        # 解析 Quantum 的 20 组数据
        for i in range(q_start, q_start + 20):
            match = re.search(pattern, lines[i])
            if match:
                aff_val = float(match.group(1))
                quantum_affinity.append(aff_val)

        # 解析 AF3 的 20 组数据
        for i in range(a_start, a_start + 20):
            match = re.search(pattern, lines[i])
            if match:
                aff_val = float(match.group(1))
                af3_affinity.append(aff_val)

        af3_affinity = [
            (val if val <= 0 else -2) for val in af3_affinity
        ]

        # 准备 x 轴：Trial 编号 1~20
        # x = range(1, 21)

        # 创建图表（仅 1 个子图）
        # plt.figure(figsize=(5, 4))

        x = np.arange(20)

        bar_width = 0.35

        plt.figure(figsize=(5, 4))

        # 画 Quantum 柱状图（向左/右偏移 bar_width/2）
        plt.bar(x - bar_width / 2, quantum_affinity, width=bar_width,
                color='tab:orange', label='Quantum',alpha=0.7)

        # 画 AF3 柱状图（向左/右偏移 bar_width/2）
        plt.bar(x + bar_width / 2, af3_affinity, width=bar_width,
                color='tab:blue', label='AF3',alpha=0.7)

        # 设置 X 轴刻度标签为 Trial 1~20
        plt.xticks(x, [str(i) for i in range(1, 21)])

        title = folder[-4:]
        # 设置标题、坐标轴标签、图例等
        plt.title(f"{title}")
        plt.xlabel("Trial")
        plt.ylabel("Affinity")
        plt.legend()
        plt.tight_layout()

        # 保存图像到 img 文件夹下
        out_fig_path = os.path.join("img_Affinity", f"{folder}_results.png")
        plt.savefig(out_fig_path, dpi=600)
        plt.close()
