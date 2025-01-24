# --*-- conding:utf-8 --*--
# @Time : 11/19/24 2:09 PM
# @Author : Yuqi Zhang
# @Email : yzhan135@kent.edu
# @File : plt_state.py

import matplotlib.pyplot as plt
import numpy as np

file_path = 'best_group/6mu3/Prob_distribution/prob_distribution.txt'
x_labels = []
y_labels = []
z_values = []

if __name__ == '__main__':

    plt.rcParams['font.family'] = 'Arial'

    with open(file_path, 'r') as file:
        for line in file:
            state, count = line.strip().split(':')
            state = state.strip()
            count = int(count.strip())
            x_labels.append(state[:4])  # First 4 qubits as x-axis labels
            y_labels.append(state[4:])  # Last 3 qubits as y-axis labels
            z_values.append(count)

    # Convert binary labels to integers for plotting
    x_indices = [int(x, 2) for x in x_labels]
    y_indices = [int(y, 2) for y in y_labels]

    # Get unique x and y indices for the grid
    x_unique = sorted(set(x_indices))
    y_unique = sorted(set(y_indices))

    # Create a 2D grid and populate it with z-values
    z_grid = np.zeros((len(y_unique), len(x_unique)))

    for x, y, z in zip(x_indices, y_indices, z_values):
        x_idx = x_unique.index(x)
        y_idx = y_unique.index(y)
        z_grid[y_idx, x_idx] = z

    # Plot the 3D heatmap
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Create a meshgrid for x, y coordinates
    X, Y = np.meshgrid(x_unique, y_unique)

    # Flatten the grid for bar3d
    x = X.flatten()
    y = Y.flatten()
    z = np.zeros_like(x)
    dx = dy = 0.8
    dz = z_grid.flatten()

    cmap = plt.cm.plasma
    # Normalize and map frequencies to colormap
    colors = cmap(dz / dz.max() if dz.max() != 0 else dz)

    # Plot the 3D bar chart with softer edgecolor
    ax.bar3d(x, y, z, dx, dy, dz,color=colors , edgecolor='none', shade=True)

    # Customize the plot
    # ax.set_xlabel('First 4 Qubits', fontsize=14, labelpad=19)
    # ax.set_ylabel('Last 3 Qubits', fontsize=14, labelpad=10)
    # ax.set_zlabel('Frequency', fontsize=14, labelpad=2)

    # Adjust tick labels
    ax.set_xticks(x_unique)
    ax.set_xticklabels([bin(val)[2:].zfill(4) for val in x_unique], rotation=45, ha='right', fontsize=12)
    ax.set_yticks(y_unique)
    ax.set_yticklabels([bin(val)[2:].zfill(3) for val in y_unique], fontsize=12)

    ax.zaxis.set_tick_params(pad=3)
    # ax.view_init(elev=20, azim=45)

    # mappable = plt.cm.ScalarMappable(cmap=cmap)
    # mappable.set_array(dz)
    # cbar = fig.colorbar(mappable, ax=ax, fraction=0.02, pad=0.1)
    # cbar.set_label('Frequency Scale', fontsize=14)

    # plt.tight_layout()
    # plt.savefig('./img_6mu3/qubit_state_styled.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('./img/qubit_state.png', dpi=600, bbox_inches='tight', format='png')
    plt.show()
