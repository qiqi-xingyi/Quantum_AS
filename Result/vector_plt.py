# --*-- conding:utf-8 --*--
# @Time : 12/14/24 8:42 PM
# @Author : Yuqi Zhang
# @Email : yzhan135@kent.edu
# @File : vector_plt.py

import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
from scipy.stats import gaussian_kde

def read_xyz_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        num_atoms = int(lines[0].strip())
        atoms = []
        coords = []
        for line in lines[2:2+num_atoms]:
            parts = line.strip().split()
            atoms.append(parts[0])
            coords.append([float(parts[1]), float(parts[2]), float(parts[3])])
    return atoms, np.array(coords)

if __name__ == '__main__':
    protein_name = 'Abeta_A'
    output_dir = f"{protein_name}"
    window_size = 7

    # 读取最终整合的结构作为全局参考坐标
    final_xyz_file = os.path.join(output_dir, f'{protein_name}_final.xyz')
    final_atoms, final_coords = read_xyz_file(final_xyz_file)
    protein_length = len(final_atoms)

    # 按window编号读取所有window文件
    xyz_files = sorted([f for f in os.listdir(output_dir) if f.endswith('.xyz') and 'window' in f],
                       key=lambda x: int(x.split('_window_')[1].split('.xyz')[0]))
    total_windows = len(xyz_files)

    # 使用Seaborn风格
    sns.set_theme(style="whitegrid", context="talk")

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # 使用矢量表示主链(骨架)的方向
    # 对final_coords中每两个相邻点使用quiver画箭头
    for i in range(protein_length - 1):
        start = final_coords[i]
        end = final_coords[i+1]
        direction = end - start
        # 使用quiver绘制主链向量，减少arrow_length_ratio可以让箭头更像直线矢量
        ax.quiver(start[0], start[1], start[2],
                  direction[0], direction[1], direction[2],
                  length=np.linalg.norm(direction),
                  normalize=False, arrow_length_ratio=0.1,
                  color='black', linewidth=2)

    # 收集所有窗口方向向量的终点坐标并映射至全局坐标
    endpoints = []
    for w_idx, xyz_file in enumerate(xyz_files):
        file_path = os.path.join(output_dir, xyz_file)
        atoms, coords = read_xyz_file(file_path)

        # 将该window的第一个坐标对齐到final_coords[w_idx]
        global_start = final_coords[w_idx]
        local_start = coords[0]
        shift = global_start - local_start
        coords_global = coords + shift

        # 计算方向向量的终点
        for i in range(len(coords_global) - 1):
            start_point = coords_global[i]
            direction = coords_global[i+1] - coords_global[i]
            end_point = start_point + direction
            endpoints.append(end_point)

    endpoints = np.array(endpoints)
    if len(endpoints) > 0:
        # 对endpoints进行核密度估计
        data = endpoints.T
        kde = gaussian_kde(data)
        density = kde(data)

        # 将密度归一化并用颜色表示
        density_norm = (density - density.min()) / (density.max() - density.min())
        cmap = cm.get_cmap('plasma')
        colors = cmap(density_norm)

        # 为了展示类似“云”的效果：
        # - 使用较大的散点大小(s)
        # - 将alpha设置较低（如0.2或0.3）让点有半透明的叠加
        # - 去掉边框（edgecolors='none'）
        ax.scatter(endpoints[:,0], endpoints[:,1], endpoints[:,2],
                   c=colors, s=400, alpha=0.25, linewidth=0, edgecolors='none')

        # 添加颜色条表示密度
        mappable = cm.ScalarMappable(cmap=cmap)
        mappable.set_array(density)
        cbar = plt.colorbar(mappable, ax=ax, fraction=0.02, pad=0.1)
        cbar.set_label('Density', fontsize=14)

    # 设置视角
    ax.view_init(elev=20, azim=-60)
    ax.set_title('Protein Backbone as Vectors and Endpoint Density Cloud', pad=20)
    ax.set_xlabel('X', labelpad=10)
    ax.set_ylabel('Y', labelpad=10)
    ax.set_zlabel('Z', labelpad=10)

    plt.tight_layout()

    output_dir = "./img_Abeta"
    output_file = "Abeta_pro.png"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, output_file)
    plt.savefig(output_path,dpi=600 ,format='png', bbox_inches='tight')

    plt.show()





