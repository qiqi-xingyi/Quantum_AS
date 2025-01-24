# --*-- conding:utf-8 --*--
# @Time : 12/14/24 5:20 PM
# @Author : Yuqi Zhang
# @Email : yzhan135@kent.edu
# @File : plt_line_2.py

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import seaborn as sns

if __name__ == '__main__':
    protein_name = '6mu3'

    # 使用Seaborn主题
    sns.set_theme(style="whitegrid")

    # 读取能量数据
    file_path = f'./{protein_name}/System_Enegry/energy_list.txt'
    with open(file_path, 'r') as file:
        energy_data = [float(line.strip()) for line in file]

    # 原始数据的x坐标（训练步数）
    x = np.arange(1, len(energy_data) + 1)

    # 使用样条插值，使曲线更加平滑
    # 这里将数据点插值到300个点左右，可根据需求调整
    x_smooth = np.linspace(x.min(), x.max(), 300)
    spline = make_interp_spline(x, energy_data, k=3)  # k=3为立方样条
    energy_smooth = spline(x_smooth)

    # 调整图像尺寸(宽一点，便于展示更多细节)
    plt.figure(figsize=(20, 6))

    # 绘制平滑曲线
    plt.plot(x_smooth, energy_smooth, color='#4169E1', linestyle='-', linewidth=3, label='Energy')

    # 添加标题和坐标轴标签
    plt.title('Energy Variation During Training', fontsize=20, pad=15)
    plt.xlabel('Training Step', fontsize=18, labelpad=10)
    plt.ylabel('Energy', fontsize=18, labelpad=10)

    # 显示网格和图例
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=16)

    # 如果横坐标需要显示更多刻度，可手动设置或根据数据自动适应
    # 例如：每隔20步显示一个刻度
    plt.xticks(np.arange(0, len(energy_data)+1, step=20))

    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    # 保存并显示图像
    plt.savefig(f'./img_e/energy_variation_{protein_name}.png', dpi=600, bbox_inches='tight')
    plt.tight_layout()
    plt.show()
