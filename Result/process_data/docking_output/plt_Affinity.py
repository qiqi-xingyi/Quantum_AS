# --*-- conding:utf-8 --*--
# @Time : 1/24/25 12:47 AM
# @Author : Yuqi Zhang
# @Email : yzhan135@kent.edu
# @File : plt_Affinity.py

import os
import re
import matplotlib.pyplot as plt
import numpy as np

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

        quantum_affinity = []
        af3_affinity = []

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()


        q_start = None
        a_start = None
        for i, line in enumerate(lines):
            if "Quantum Results:" in line:
                q_start = i + 1
            if "AF3 Results:" in line:
                a_start = i + 1

        pattern = r"Affinity\s*=\s*([-0-9\.]+).*Lower Bound\s*=\s*([-0-9\.]+).*Upper Bound\s*=\s*([-0-9\.]+)"

        for i in range(q_start, q_start + 20):
            match = re.search(pattern, lines[i])
            if match:
                aff_val = float(match.group(1))
                quantum_affinity.append(aff_val)

        for i in range(a_start, a_start + 20):
            match = re.search(pattern, lines[i])
            if match:
                aff_val = float(match.group(1))
                af3_affinity.append(aff_val)

        af3_affinity = [
            (val if val <= 0 else -2) for val in af3_affinity
        ]



        x = np.arange(20)

        bar_width = 0.35

        plt.figure(figsize=(5, 4))


        plt.bar(x - bar_width / 2, quantum_affinity, width=bar_width,
                color='tab:orange', label='Quantum',alpha=0.7)


        plt.bar(x + bar_width / 2, af3_affinity, width=bar_width,
                color='tab:blue', label='AF3',alpha=0.7)

        plt.xticks(x, [str(i) for i in range(1, 21)])

        title = folder[-4:]

        plt.title(f"{title}")
        plt.xlabel("Trial")
        plt.ylabel("Affinity")

        plt.tight_layout()


        out_fig_path = os.path.join("img_Affinity", f"{folder}_results.png")
        plt.savefig(out_fig_path, dpi=600)
        plt.close()
