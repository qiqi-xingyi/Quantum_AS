# --*-- conding:utf-8 --*--
# @Time : 11/18/24 9:43 AM
# @Author : Yuqi Zhang
# @Email : yzhan135@kent.edu
# @File : plt_line.py

import os
import re
import matplotlib.pyplot as plt

def read_data_from_txt(file_path):
    quantum_data = {"affinity": [], "rmsd_lower": [], "rmsd_upper": []}
    af3_data = {"affinity": [], "rmsd_lower": [], "rmsd_upper": []}
    is_quantum = True

    with open(file_path, 'r') as file:
        for line in file:
            if line.strip().startswith("Quantum Results:"):
                is_quantum = True
            elif line.strip().startswith("AF2 Results:"):
                is_quantum = False
            elif "Affinity" in line:
                # Extract Affinity, RMSD.txt Lower Bound, RMSD.txt Upper Bound
                affinity = float(line.split("Affinity =")[1].split(",")[0].strip())
                rmsd_lower = float(line.split("RMSD.txt Lower Bound =")[1].split(",")[0].strip())
                rmsd_upper = float(line.split("RMSD.txt Upper Bound =")[1].strip())

                if is_quantum:
                    quantum_data["affinity"].append(affinity)
                    quantum_data["rmsd_lower"].append(rmsd_lower)
                    quantum_data["rmsd_upper"].append(rmsd_upper)
                else:
                    af3_data["affinity"].append(affinity)
                    af3_data["rmsd_lower"].append(rmsd_lower)
                    af3_data["rmsd_upper"].append(rmsd_upper)

    return quantum_data, af3_data


if __name__ == '__main__':

    # Font and figure style config
    plt.rcParams.update({
        'font.size': 18,
        'axes.titlesize': 20,
        'axes.labelsize': 18,
        'xtick.labelsize': 16,
        'ytick.labelsize': 16,
        'legend.fontsize': 16,
        'figure.titlesize': 22
    })

    # Read data from text file
    file_path = 'docking_output_6mu3/summary_results.txt'
    quantum_data, af3_data = read_data_from_txt(file_path)

    # Define each subplot's data type and title
    data_types = ["affinity", "rmsd_lower", "rmsd_upper"]
    titles = ["Affinity Scores", "RMSD.txt Lower Bound", "RMSD.txt Upper Bound"]

    # Create a single figure with 3 subplots horizontally
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))

    # Iterate over each data type to create boxplots on each axis
    for i, data_type in enumerate(data_types):
        ax = axes[i]

        # Prepare data for boxplot
        # We'll have two boxes: [quantum_data[data_type], af2_data[data_type]]
        bp = ax.boxplot(
            [quantum_data[data_type], af3_data[data_type]],
            labels=['Quantum', 'AF3'],
            patch_artist=True,
            boxprops=dict(linewidth=2),
            medianprops=dict(color='#800000', linewidth=2),
            whiskerprops=dict(color='#191970', linewidth=2.5, linestyle='-'),
            capprops=dict(color='#191970', linewidth=2.5),
            flierprops=dict(marker='o', color='#191970', alpha=0.8, markeredgewidth=2),
            widths=0.4
        )

        # Manually set facecolors to red (Quantum) and blue (AF2)
        # bp['boxes'] is a list of two boxes
        # box 0 => quantum, box 1 => af3
        box_colors = ['lightcoral', 'lightblue']
        for j, box in enumerate(bp['boxes']):
            box.set(facecolor=box_colors[j])

        # Title, axis label, and grid
        # ax.set_title(titles[i])
        ax.set_ylabel(titles[i])
        ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Adjust spacing between subplots if needed
    plt.tight_layout()

    # Save the combined figure as one file
    os.makedirs('img', exist_ok=True)
    plt.savefig('./img/combined_boxplot.png', dpi=600, bbox_inches='tight')

    # Show the combined figure
    plt.show()

