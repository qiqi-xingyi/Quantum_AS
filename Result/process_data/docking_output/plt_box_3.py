# --*-- conding:utf-8 --*--
# @Time : 1/24/25 7:47 PM
# @Author : Yuqi Zhang
# @Email : yzhan135@kent.edu
# @File : plt_box_3.py

import os
import re
import matplotlib.pyplot as plt


subfolders = [
    "docking_output_1a9m",
    "docking_output_1fkn",
    "docking_output_1qin",
    "docking_output_2xxx",
    "docking_output_3ans",
    "docking_output_3b26",
    "docking_output_6mu3"
]


BOX_WIDTH = 0.4
MEDIAN_LINE_COLOR = "red"
MEDIAN_LINE_WIDTH = 2
WHISKER_COLOR = "black"
WHISKER_LINE_WIDTH = 1
CAP_COLOR = "black"
CAP_LINE_WIDTH = 1
FLIER_MARKER = "o"
FLIER_COLOR = "gray"
FLIER_SIZE = 5
FLIER_ALPHA = 0.7

if __name__ == '__main__':

    plt.rcParams['font.family'] = 'Arial'

    for folder in subfolders:
        file_path = os.path.join(folder, "summary_results.txt")


        quantum_affinity_all = []
        quantum_rmsd_lower_all = []
        quantum_rmsd_upper_all = []

        af3_affinity_all = []
        af3_rmsd_lower_all = []
        af3_rmsd_upper_all = []

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        q_start, a_start = None, None
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
                lb_val = float(match.group(2))
                ub_val = float(match.group(3))
                quantum_affinity_all.append(aff_val)
                quantum_rmsd_lower_all.append(lb_val)
                quantum_rmsd_upper_all.append(ub_val)

        for i in range(a_start, a_start + 20):
            match = re.search(pattern, lines[i])
            if match:
                aff_val = float(match.group(1))
                lb_val = float(match.group(2))
                ub_val = float(match.group(3))
                af3_affinity_all.append(aff_val)
                af3_rmsd_lower_all.append(lb_val)
                af3_rmsd_upper_all.append(ub_val)

        quantum_affinity_plot = [val for val in quantum_affinity_all if val <= 0]
        af3_affinity_plot = [val for val in af3_affinity_all if val <= 0]

        quantum_rmsd_lower_plot = quantum_rmsd_lower_all[:]  # RMSD 不排除
        af3_rmsd_lower_plot = af3_rmsd_lower_all[:]

        quantum_rmsd_upper_plot = quantum_rmsd_upper_all[:]
        af3_rmsd_upper_plot = af3_rmsd_upper_all[:]

        import numpy as np
        avg_quantum_aff = np.mean(quantum_affinity_all)
        avg_af3_aff = np.mean(af3_affinity_all)

        fig, axs = plt.subplots(1, 3, figsize=(8, 3))

        folder_suffix = folder[-4:]
        plt.suptitle(f"{folder_suffix}", fontsize=16)

        medianprops = dict(color=MEDIAN_LINE_COLOR, linewidth=MEDIAN_LINE_WIDTH)
        whiskerprops = dict(color=WHISKER_COLOR, linewidth=WHISKER_LINE_WIDTH)
        capprops = dict(color=CAP_COLOR, linewidth=CAP_LINE_WIDTH)
        flierprops = dict(
            marker=FLIER_MARKER,
            markerfacecolor=FLIER_COLOR,
            markersize=FLIER_SIZE,
            alpha=FLIER_ALPHA
        )
        boxprops = dict(facecolor="white", edgecolor="black", linewidth=1.5)

        # -- 子图 1: Affinity --
        data_aff_plot = [quantum_affinity_plot, af3_affinity_plot]
        bp_aff = axs[0].boxplot(
            data_aff_plot,
            patch_artist=True,
            tick_labels=["Quantum", "AF3"],
            widths=BOX_WIDTH,
            boxprops=boxprops,
            medianprops=medianprops,
            whiskerprops=whiskerprops,
            capprops=capprops,
            flierprops=flierprops
        )
        for patch, color in zip(bp_aff['boxes'], ["tab:orange", "tab:blue"]):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        axs[0].set_ylabel("Affinity")

        data_lb_plot = [quantum_rmsd_lower_plot, af3_rmsd_lower_plot]
        bp_lb = axs[1].boxplot(
            data_lb_plot,
            patch_artist=True,
            tick_labels=["Quantum", "AF3"],
            widths=BOX_WIDTH,
            boxprops=boxprops,
            medianprops=medianprops,
            whiskerprops=whiskerprops,
            capprops=capprops,
            flierprops=flierprops
        )
        for patch, color in zip(bp_lb['boxes'], ["tab:orange", "tab:blue"]):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        axs[1].set_ylabel("RMSD Lower Bound")

        data_ub_plot = [quantum_rmsd_upper_plot, af3_rmsd_upper_plot]
        bp_ub = axs[2].boxplot(
            data_ub_plot,
            patch_artist=True,
            tick_labels=["Quantum", "AF3"],
            widths=BOX_WIDTH,
            boxprops=boxprops,
            medianprops=medianprops,
            whiskerprops=whiskerprops,
            capprops=capprops,
            flierprops=flierprops
        )
        for patch, color in zip(bp_ub['boxes'], ["tab:orange", "tab:blue"]):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        axs[2].set_ylabel("RMSD Upper Bound")

        plt.tight_layout()

        out_fig_path = os.path.join("img_box", f"{folder}_boxplot.png")
        plt.savefig(out_fig_path, dpi=600)
        plt.close()
