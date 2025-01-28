# --*-- conding:utf-8 --*--
# @Time : 11/19/24 2:07 PM
# @Author : Yuqi Zhang
# @Email : yzhan135@kent.edu
# @File : plt_line.py

import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':

    plt.rcParams['font.family'] = 'Arial'

    protein = '6mu3'

    # Load energy data from the file
    file_path = f'best_group/{protein}/System_Enegry/energy_list_{protein}.txt'
    with open(file_path, 'r') as file:
        energy_data = [float(line.strip()) for line in file]

    # Convert to numpy array for easier manipulation
    energy_data = np.array(energy_data)

    # Find the indices of the 6 lowest points (convert to integers if necessary)
    lowest_indices = np.argsort(energy_data)[:1]  # Get indices of 6 smallest values
    lowest_indices = lowest_indices.astype(int)  # Ensure indices are integers
    lowest_values = energy_data[lowest_indices]  # Get corresponding values

    # Plot the energy data
    plt.figure(figsize=(21, 6))
    plt.plot(range(1, len(energy_data) + 1), energy_data, marker='o', linestyle='-', color='blue', label='Energy')

    # Highlight the lowest points
    plt.scatter(lowest_indices+1 , lowest_values, color='purple', label='Lowest Points', zorder=5)

    # Annotate the lowest points with their values
    for idx, value in zip(lowest_indices, lowest_values):
        plt.text(idx+1.6, value-0.02, f'{value:.2f}', color='purple', fontsize=12, ha='left', va='center')

    # Add labels and title
    # plt.title('Energy changes during the first stage of the VQE optimization process', fontsize=16)
    plt.xlabel('Optimization Steps', fontsize=16)
    plt.ylabel('System Energy', fontsize=16)

    # Adjust tick label size
    plt.tick_params(axis='both', which='major', labelsize=14)  # Increase tick label size

    # Add grid and legend
    plt.grid(True, linestyle='--', alpha=0.8)
    plt.legend(fontsize=12)

    # Save the plot
    plt.savefig(f'./img/energy_variation_{protein}.png', dpi=600, bbox_inches='tight')

    # Show the plot
    plt.tight_layout()
    plt.show()
