# --*-- conding:utf-8 --*--
# @Time : 1/24/25 6:31 PM
# @Author : Yuqi Zhang
# @Email : yzhan135@kent.edu
# @File : plt_bar.py

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

if __name__ == '__main__':

    plt.rcParams['font.family'] = 'Arial'

    # 1. 创建图表，添加一个子图
    fig = plt.figure(figsize=(4, 3))
    ax = fig.add_subplot(111)

    # 2. 隐藏坐标轴，让它看起来没有任何主图
    ax.axis('off')

    # 3. 人为构造一些“图例句柄”，比如两条线 + 两个色块，代表想要显示的“图例项”
    # line_blue = Line2D([0], [0], color='blue',   marker='o', label='Line Blue')
    # line_red  = Line2D([0], [0], color='red',    marker='s', label='Line Red', linestyle='--')
    patch_green  = Patch(color='tab:orange', label='Quantum',alpha=0.7)
    patch_orange = Patch(color='tab:blue', label='AF3',alpha=0.7)

    handles = [patch_green, patch_orange]

    # 4. 在整个 figure 范围内放置图例（仅图例，没有任何数据可视化）
    fig.legend(
        handles,
        [h.get_label() for h in handles],
        loc='center',       # 你也可以用 'upper center', 'lower right', etc.
        ncol=1              # 图例每行放多少项
    )

    # 5. 展示或保存
    plt.tight_layout()
    # plt.show()
    plt.savefig("img_Affinity/legend.png", dpi=600)
    # plt.close()
