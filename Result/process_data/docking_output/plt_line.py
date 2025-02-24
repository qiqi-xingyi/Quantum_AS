# --*-- conding:utf-8 --*--
# @Time : 1/23/25 11:30 PM
# @Author : Yuqi Zhang
# @Email : yzhan135@kent.edu
# @File : plt_line.py

import os
import re
import matplotlib.pyplot as plt

# 假设这 7 个子文件夹的名字如下
subfolders = ["docking_output_1a9m", "docking_output_1fkn", "docking_output_1qin", "docking_output_2xxx",
              "docking_output_3ans", "docking_output_3b26", "docking_output_6mu3"]

if __name__ == '__main__':

    for folder in subfolders:
        file_path = os.path.join(folder, "summary_results.txt")

        # 定义存储 Quantum / AF3 数据的列表
        quantum_affinity = []
        quantum_rmsd_lower = []
        quantum_rmsd_upper = []

        af3_affinity = []
        af3_rmsd_lower = []
        af3_rmsd_upper = []

        # 读取文件内容
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # 找到 Quantum Results: 和 AF3 Results: 的起始行索引
        q_start = None
        a_start = None
        for i, line in enumerate(lines):
            if "Quantum Results:" in line:
                q_start = i + 1  # 下 20 行是 Quantum 的数据
            if "AF3 Results:" in line:
                a_start = i + 1  # 下 20 行是 AF3 的数据

        # 使用正则表达式解析行中 Affinity、RMSD.txt Lower、RMSD.txt Upper 的数值
        pattern = r"Affinity\s*=\s*([-0-9\.]+).*Lower Bound\s*=\s*([-0-9\.]+).*Upper Bound\s*=\s*([-0-9\.]+)"

        # 解析 Quantum 的 20 组数据
        for i in range(q_start, q_start + 20):
            match = re.search(pattern, lines[i])
            if match:
                aff_val = float(match.group(1))
                lb_val = float(match.group(2))
                ub_val = float(match.group(3))
                quantum_affinity.append(aff_val)
                quantum_rmsd_lower.append(lb_val)
                quantum_rmsd_upper.append(ub_val)

        # 解析 AF3 的 20 组数据
        for i in range(a_start, a_start + 20):
            match = re.search(pattern, lines[i])
            if match:
                aff_val = float(match.group(1))
                lb_val = float(match.group(2))
                ub_val = float(match.group(3))
                af3_affinity.append(aff_val)
                af3_rmsd_lower.append(lb_val)
                af3_rmsd_upper.append(ub_val)

        # 准备 x 轴：Trial 编号 1~20
        x = range(1, 21)

        # 创建画布和子图：3 个子图并排 (1 行 3 列)
        fig, axs = plt.subplots(1, 3, figsize=(15, 5), sharex=True)

        # 图 1：Affinity
        axs[0].plot(x, quantum_affinity, marker='o', label="Quantum")
        axs[0].plot(x, af3_affinity, marker='s', label="AF3")
        axs[0].set_title("Affinity")
        axs[0].set_xlabel("Trial")
        axs[0].set_ylabel("Affinity")
        axs[0].legend()

        # 图 2：RMSD.txt Lower Bound
        axs[1].plot(x, quantum_rmsd_lower, marker='o', label="Quantum")
        axs[1].plot(x, af3_rmsd_lower, marker='s', label="AF3")
        axs[1].set_title("RMSD.txt Lower Bound")
        axs[1].set_xlabel("Trial")
        axs[1].set_ylabel("RMSD.txt Lower")

        # 图 3：RMSD.txt Upper Bound
        axs[2].plot(x, quantum_rmsd_upper, marker='o', label="Quantum")
        axs[2].plot(x, af3_rmsd_upper, marker='s', label="AF3")
        axs[2].set_title("RMSD.txt Upper Bound")
        axs[2].set_xlabel("Trial")
        axs[2].set_ylabel("RMSD.txt Upper")

        # 设置总标题，表示是哪一个子文件夹
        # plt.suptitle(f"Results for {folder}")

        # 调整子图布局，防止标题和标签重叠
        plt.tight_layout()

        # 显示或保存
        # 如果要显示图像（互动环境下）
        # plt.show()

        # 如果想直接保存图像，而不在屏幕上显示，可以使用：
        out_fig_path = os.path.join(f"img/{folder}_results.png")
        plt.savefig(out_fig_path, dpi=600)
        plt.close()
