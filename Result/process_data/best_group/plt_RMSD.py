# --*-- conding:utf-8 --*--
# @Time : 2/24/25 1:45 PM
# @Author : Yuqi Zhang
# @Email : yzhan135@kent.edu
# @File : plt_RMSD.py

import matplotlib.pyplot as plt
import pandas as pd


data = {
    "PDB ID": ["1a9m", "1fkn", "1qin", "2xxx", "3ans", "3b26", "6mu3"],
    "AF3": [3.583, 5.919, 3.473, 4.537, 2.781, 3.635, 2.721],
    "VQE": [3.192, 4.917, 3.068, 4.320, 2.605, 2.970, 2.755],
    "NUM": [8, 12, 9, 12, 5, 11, 5],
}

if __name__ == '__main__':


    df = pd.DataFrame(data)


    df = df.sort_values(by="NUM")


    plt.figure(figsize=(8, 5))
    plt.plot(df["NUM"], df["AF3"], marker="o", linestyle="-", label="AF3")
    plt.plot(df["NUM"], df["VQE"], marker="s", linestyle="-", label="VQE")


    plt.xlabel("NUM")
    plt.ylabel("Value")
    plt.title("AF3 and VQE Changes with NUM")
    plt.legend()
    plt.grid(True)


    plt.savefig("af3_vqe_plot.png", dpi=600)
    plt.savefig("af3_vqe_plot.pdf")


    plt.show()
