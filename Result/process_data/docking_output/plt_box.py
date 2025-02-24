# --*-- conding:utf-8 --*--
# @Time : 1/23/25 11:59 PM
# @Author : Yuqi Zhang
# @Email : yzhan135@kent.edu
# @File : plt_box.py

import os
import re
import numpy as np
import matplotlib.pyplot as plt

# 假设这 7 个子文件夹的名字如下（可以换成自己的实际目录名）
subfolders = ["docking_output_1a9m", "docking_output_1fkn", "docking_output_1qin", "docking_output_2xxx",
              "docking_output_3ans", "docking_output_3b26", "docking_output_6mu3"]

if __name__ == '__main__':

    plt.rcParams['font.family'] = 'Arial'
    # 准备存储每个子文件夹提取出的平均值
    quantum_mean_affinity_list = []
    af3_mean_affinity_list = []

    quantum_mean_rmsd_lower_list = []
    af3_mean_rmsd_lower_list = []

    quantum_mean_rmsd_upper_list = []
    af3_mean_rmsd_upper_list = []

    # ---------------------------
    # 1. 读取并解析文件，提取 Overall Average 的数值
    # ---------------------------
    for folder in subfolders:
        file_path = os.path.join(folder, "summary_results.txt")

        # 先读取所有行
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # 找到 Quantum Results: 和 AF3 Results: 的起始行
        q_start = None
        a_start = None
        for i, line in enumerate(lines):
            if "Quantum Results:" in line:
                q_start = i + 1
            if "AF3 Results:" in line:
                a_start = i + 1

        # Quantum 的 Overall Average 行通常在 20 行试验数据之后（即 q_start+20）
        # AF3 的 Overall Average 行在 a_start+20
        # 我们用正则表达式来解析 "Overall Average: Affinity = x, RMSD.txt Lower Bound = y, RMSD.txt Upper Bound = z"
        avg_pattern = r"Overall Average:\s*Affinity\s*=\s*([-0-9\.]+).*Lower Bound\s*=\s*([-0-9\.]+).*Upper Bound\s*=\s*([-0-9\.]+)"

        # 提取 Quantum 的 Overall Average
        quantum_avg_line = lines[q_start + 20]
        q_match = re.search(avg_pattern, quantum_avg_line)
        if q_match:
            q_aff = float(q_match.group(1))  # Affinity
            q_lb = float(q_match.group(2))  # RMSD.txt Lower
            q_ub = float(q_match.group(3))  # RMSD.txt Upper
        else:
            # 如果没匹配到，可自行处理报错或默认值
            q_aff, q_lb, q_ub = np.nan, np.nan, np.nan

        # 提取 AF3 的 Overall Average
        af3_avg_line = lines[a_start + 20]
        a_match = re.search(avg_pattern, af3_avg_line)
        if a_match:
            a_aff = float(a_match.group(1))  # Affinity
            a_lb = float(a_match.group(2))  # RMSD.txt Lower
            a_ub = float(a_match.group(3))  # RMSD.txt Upper
        else:
            a_aff, a_lb, a_ub = np.nan, np.nan, np.nan

        # 存储到相应的列表
        quantum_mean_affinity_list.append(q_aff)
        quantum_mean_rmsd_lower_list.append(q_lb)
        quantum_mean_rmsd_upper_list.append(q_ub)

        af3_mean_affinity_list.append(a_aff)
        af3_mean_rmsd_lower_list.append(a_lb)
        af3_mean_rmsd_upper_list.append(a_ub)

    # ---------------------------
    # 2. 绘制柱状图
    #    - 图 1: Affinity
    #    - 图 2: RMSD.txt Lower Bound
    #    - 图 3: RMSD.txt Upper Bound
    # ---------------------------

    labels = [sf[-4:] for sf in subfolders]
    # x 轴的刻度位置
    x = np.arange(len(subfolders))  # 0, 1, 2, ..., 6 对应 7 个文件夹
    bar_width = 0.25  # 柱子的宽度

    # (A) Affinity 柱状图
    plt.figure(figsize=(6, 3))
    plt.bar(x - bar_width / 2, quantum_mean_affinity_list, width=bar_width,color='tab:orange', label='Quantum', alpha=0.7)
    plt.bar(x + bar_width / 2, af3_mean_affinity_list, width=bar_width,color='tab:blue', label='AF3', alpha=0.7)
    plt.xticks(x, labels, rotation=30)
    plt.ylabel("Affinity")
    # plt.title("Overall Average Affinity Comparison (Quantum vs AF3)")
    plt.legend()
    plt.tight_layout()

    # for i, bar in enumerate(bars):
    #     # facecolor 表示柱子的填充颜色(RGBA)
    #     face_color = bar.get_facecolor()
    #     print(f"Bar Quantum {i} face color:", face_color)
    # plt.show()
    # 如果要保存图像，可以使用：
    plt.savefig("img_box/Affinity_comparison.png", dpi=600)
    # plt.close()

    # (B) RMSD.txt Lower Bound 柱状图
    plt.figure(figsize=(6, 3))
    plt.bar(x - bar_width / 2, quantum_mean_rmsd_lower_list, width=bar_width,color='tab:orange', label='Quantum', alpha=0.7)
    plt.bar(x + bar_width / 2, af3_mean_rmsd_lower_list, width=bar_width,color='tab:blue', label='AF3', alpha=0.7)
    plt.xticks(x, labels, rotation=30)
    plt.ylabel("RMSD.txt Lower Bound")
    # plt.title("Overall Average RMSD.txt Lower Bound Comparison (Quantum vs AF3)")
    plt.legend()
    plt.tight_layout()
    # plt.show()
    plt.savefig("img_box/RLB.png", dpi=600)

    # (C) RMSD.txt Upper Bound 柱状图
    plt.figure(figsize=(6, 3))
    plt.bar(x - bar_width / 2, quantum_mean_rmsd_upper_list, width=bar_width,color='tab:orange', label='Quantum', alpha=0.7)
    plt.bar(x + bar_width / 2, af3_mean_rmsd_upper_list, width=bar_width,color='tab:blue', label='AF3', alpha=0.7)
    plt.xticks(x, labels, rotation=30)
    plt.ylabel("RMSD.txt Upper Bound")
    # plt.title("Overall Average RMSD.txt Upper Bound Comparison (Quantum vs AF3)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("img_box/RUB.png", dpi=600)
    # plt.show()
