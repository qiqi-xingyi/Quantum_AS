# --*-- conding:utf-8 --*--
# @Time : 1/3/25 11:12 AM
# @Author : Yuqi Zhang
# @Email : yzhan135@kent.edu
# @File : plt_point.py

import os
import re
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator

# root_path = "docking_output_6mu3"  #6mu3
root_path = "./docking_output_4zb8" #4zb8
num_trials = 20   # number of trials for each method
num_modes = 9     # each trial has 9 docking results


plt.rcParams.update({
    "font.size": 18,          # 全局字体大小
    "axes.titlesize": 24,     # 子图标题字体大小
    "axes.labelsize": 28,     # 坐标轴标签字体大小
    "xtick.labelsize": 22,    # x轴刻度标签字体大小
    "ytick.labelsize": 22,    # y轴刻度标签字体大小
    "legend.fontsize": 20,    # 图例字体大小
    "figure.titlesize": 18    # 整体图标题字体大小
})



def parse_log_file(log_file_path):
    """
    Parse a docking log file, extract 9 lines of results:
    (mode, affinity, rmsd_lb, rmsd_ub).
    Return a list of tuples [(mode, aff, lb, ub), ...].
    """
    results = []
    if not os.path.isfile(log_file_path):
        print(f"Warning: file {log_file_path} does not exist, skipping.")
        return results

    with open(log_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    data_start = None
    for i, line in enumerate(lines):
        if line.strip().startswith("mode |") and ("affinity" in line):
            data_start = i + 3  # data lines start after the header/separator
            break

    if data_start is not None and data_start + num_modes <= len(lines):
        for j in range(data_start, data_start + num_modes):
            row = lines[j].strip()
            items = re.split(r"\s+", row)
            if len(items) >= 4:
                try:
                    mode = int(items[0])
                    affinity = float(items[1])
                    rmsd_lb = float(items[2])
                    rmsd_ub = float(items[3])
                    results.append((mode, affinity, rmsd_lb, rmsd_ub))
                except ValueError:
                    pass
    else:
        print(f"Warning: file {log_file_path} has unexpected format, skipping.")
    return results

if __name__ == '__main__':

    results = {
        "quantum": {},
        "af3": {}
    }

    for i in range(1, num_trials + 1):
        # quantum
        q_folder = f"quantum_trial_{i}"
        q_log_name = f"docking_log_trial_{i}.txt"
        q_log_path = os.path.join(root_path, q_folder, q_log_name)
        q_data = parse_log_file(q_log_path)
        results["quantum"][i] = q_data

        # af3
        a_folder = f"af2_trial_{i}"
        a_log_name = f"af2_docking_log_trial_{i}.txt"
        a_log_path = os.path.join(root_path, a_folder, a_log_name)
        a_data = parse_log_file(a_log_path)
        results["af3"][i] = a_data

    quantum_cmap = plt.cm.Reds_r
    af3_cmap     = plt.cm.Blues_r

    fig = plt.figure(figsize=(35, 13))  # adjust size as needed

    # 4.1 Subplot 1 for Affinity (<0)
    ax1 = fig.add_subplot(1, 3, 1, projection="3d")
    # ax1.set_title("Docking Affinity")
    ax1.set_xlabel("Trial",labelpad=26)
    ax1.set_ylabel("Mode",labelpad=24)
    ax1.set_zlabel("Affinity (kcal/mol)",labelpad=26)
    ax1.set_xticks(range(1, num_trials + 1))
    ax1.set_xticklabels([str(i) for i in range(1, num_trials + 1)], rotation=45)
    ax1.tick_params(axis='x', pad=5)
    ax1.tick_params(axis='y', pad=5)
    ax1.tick_params(axis='z', pad=10)

    # We'll store handles/labels so that we can create one legend at the figure level
    plotted_methods = {}  # e.g. "quantum": handle, "af2": handle

    # Plot quantum & af2 on subplot 1
    vmin_mode, vmax_mode = 1, 9
    for method, cmap in zip(["quantum", "af3"], [quantum_cmap, af3_cmap]):
        x_vals, y_vals, z_vals = [], [], []
        colors = []
        for trial_idx in range(1, num_trials + 1):
            for (mode, aff, lb, ub) in results[method][trial_idx]:
                if aff < 0:  # only negative affinity
                    x_vals.append(trial_idx)
                    y_vals.append(mode)
                    z_vals.append(aff)
                    normed = (mode - vmin_mode) / (vmax_mode - vmin_mode)
                    # reduce gradient if needed
                    reduced = 0.1 + 0.6 * normed
                    c = cmap(reduced)
                    colors.append(c)
        scatter_obj = ax1.scatter(
            x_vals, y_vals, z_vals,
            c=colors,
            alpha=0.8,
            marker="o" if method == "quantum" else "^",
            s=80,
            label=method
        )
        plotted_methods[method] = scatter_obj  # store the handle

    # 4.2 Subplot 2 for RMSD.txt l.b. (skip mode=1)
    ax2 = fig.add_subplot(1, 3, 2, projection="3d")
    # ax2.set_title("Docking RMSD.txt Lower Bound")
    ax2.set_xlabel("Trial",labelpad=26)
    ax2.set_ylabel("Mode",labelpad=24)
    ax2.set_zlabel("RMSD.txt Lower Bound",labelpad=17)
    ax2.set_xticks(range(1, num_trials + 1))
    ax2.set_xticklabels([str(i) for i in range(1, num_trials + 1)], rotation=45)

    vmin_mode_rmsd, vmax_mode_rmsd = 2, 9  # skip mode=1
    for method, cmap in zip(["quantum", "af3"], [quantum_cmap, af3_cmap]):
        x_vals, y_vals, z_vals = [], [], []
        colors = []
        for trial_idx in range(1, num_trials + 1):
            for (mode, aff, lb, ub) in results[method][trial_idx]:
                if mode == 1:
                    continue
                x_vals.append(trial_idx)
                y_vals.append(mode)
                z_vals.append(lb)
                normed = (mode - vmin_mode_rmsd) / (vmax_mode_rmsd - vmin_mode_rmsd)
                reduced = 0.1 + 0.6 * normed
                c = cmap(reduced)
                colors.append(c)
        ax2.scatter(
            x_vals, y_vals, z_vals,
            c=colors,
            alpha=0.8,
            marker="o" if method == "quantum" else "^",
            s=80,
            # no need for label here,
            # we already got it from subplot 1
        )

    # 4.3 Subplot 3 for RMSD.txt u.b. (skip mode=1)
    ax3 = fig.add_subplot(1, 3, 3, projection="3d")
    # ax3.set_title("Docking RMSD.txt Upper Bound")
    ax3.set_xlabel("Trial",labelpad=26)
    ax3.set_ylabel("Mode",labelpad=24)
    ax3.set_zlabel("RMSD.txt Upper Bound",labelpad=17)
    ax3.set_xticks(range(1, num_trials + 1))
    ax3.set_xticklabels([str(i) for i in range(1, num_trials + 1)], rotation=45)

    for method, cmap in zip(["quantum", "af3"], [quantum_cmap, af3_cmap]):
        x_vals, y_vals, z_vals = [], [], []
        colors = []
        for trial_idx in range(1, num_trials + 1):
            for (mode, aff, lb, ub) in results[method][trial_idx]:
                if mode == 1:
                    continue
                x_vals.append(trial_idx)
                y_vals.append(mode)
                z_vals.append(ub)
                normed = (mode - vmin_mode_rmsd) / (vmax_mode_rmsd - vmin_mode_rmsd)
                reduced = 0.1 + 0.6 * normed
                c = cmap(reduced)
                colors.append(c)
        ax3.scatter(
            x_vals, y_vals, z_vals,
            c=colors,
            alpha=0.8,
            marker="o" if method == "quantum" else "^",
            s=80,
        )

    # We already captured the quantum/af2 handles in subplot 1
    handles = list(plotted_methods.values())
    labels  = list(plotted_methods.keys())

    ax1.xaxis.set_major_locator(MultipleLocator(2))
    ax2.xaxis.set_major_locator(MultipleLocator(2))
    ax3.xaxis.set_major_locator(MultipleLocator(2))

    # fig.tight_layout()

    sm_quantum = plt.cm.ScalarMappable(
        cmap=quantum_cmap,
        norm=plt.Normalize(vmin=vmin_mode, vmax=vmax_mode)
    )
    sm_quantum.set_array([])

    sm_af3 = plt.cm.ScalarMappable(
        cmap=af3_cmap,
        norm=plt.Normalize(vmin=vmin_mode, vmax=vmax_mode)
    )
    sm_af3.set_array([])

    cax1 = fig.add_axes((0.08, 0.38, 0.004, 0.20))  # [left, bottom, width, height]
    cax2 = fig.add_axes((0.11, 0.38, 0.004, 0.20))

    cbar_quantum = plt.colorbar(sm_quantum, cax=cax1)
    cbar_quantum.set_label("Mode (Quantum)", fontsize=18)

    cbar_af3 = plt.colorbar(sm_af3, cax=cax2)
    cbar_af3.set_label("Mode (AF3)", fontsize=18)

    # save_dir = "./img_point_6mu3"
    save_dir = "./img_point_4zb8"
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, "3D_combined_new.png")
    fig.savefig(save_path, dpi=600, bbox_inches="tight", pad_inches=0.7)
    # fig.savefig(save_path, dpi=600)

    plt.show()