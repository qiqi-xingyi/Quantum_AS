# --*-- conding:utf-8 --*--
# @Time : 1/14/25 8:36 AM
# @Author : Yuqi Zhang
# @Email : yzhan135@kent.edu
# @File : lower_energy_docking.py

import os
import glob
import random
from Autodock_tool import AutoDockDocking


def run_docking_for_all_pdbqts(
        root_dir="process_data/create_structure",    # 存放所有 pdbqt 的根目录
        output_root="process_data/lower_energy_docking",  # 对接结果存放根目录
        ligand_suffix="_ligand_trans.mol2",          # 每个蛋白对应的配体文件后缀
        default_seed=69652
):
    """
    递归查找 root_dir 下每个 .pdbqt 文件，对其执行 AutoDockDocking，
    并将结果放到 output_root，保持和 root_dir 相同的子文件夹结构。

    假设 ligand 文件与蛋白ID相关。例如当子文件夹名称为 '6mu3' 时，
    配体文件默认为: ./process_data/best_group/6mu3/PDBbind_data/6mu3/6mu3_ligand_trans.mol2
    如有不同需求，可在脚本内对 ligand_path 的拼法做调整。
    """

    # 1) 准备一个 seed_log，用于记录对接时使用的随机种子
    seed_log_file = os.path.join(output_root, "seed_log.txt")
    os.makedirs(output_root, exist_ok=True)
    with open(seed_log_file, "w", encoding="utf-8") as seed_file:
        seed_file.write("PDBQT_File\tSeed\n")

    # 2) 遍历 root_dir 下所有子文件夹，搜集所有 .pdbqt 文件
    for current_root, dirs, files in os.walk(root_dir):
        for file_name in files:
            if file_name.endswith(".pdbqt"):
                # (a) 拼出当前 pdbqt 文件的绝对路径
                pdbqt_file = os.path.join(current_root, file_name)

                # (b) 计算 output_subdir (在 output_root 中保留与 root_dir 相同的子结构)
                rel_path = os.path.relpath(current_root, root_dir)
                output_subdir = os.path.join(output_root, rel_path)
                os.makedirs(output_subdir, exist_ok=True)

                # (c) 使用文件夹名作为蛋白ID，例如 create_structure/6mu3 => "6mu3"
                protein_id = os.path.basename(os.path.normpath(current_root))

                # (d) 配体路径
                # process_data/best_group/{protein_id}/PDBbind_data/{protein_id}/{protein_id}_ligand_trans.mol2
                ligand_path = os.path.join(
                    "process_data/best_group", protein_id,
                    "PDBbind_data", protein_id,
                    protein_id + ligand_suffix
                )

                # (e) 种子（可固定，可随机）
                seed = default_seed  # 或者 random.randint(1, 99999)

                print(f"[INFO] Docking: {pdbqt_file} -> {output_subdir}, seed={seed}")

                # (f) 写入 seed_log
                with open(seed_log_file, "a", encoding="utf-8") as seed_file:
                    seed_file.write(f"{pdbqt_file}\t{seed}\n")

                # (g) 生成日志文件名（只要“文件名”，不带路径）
                chain_id = os.path.splitext(file_name)[0]
                docking_log_name = f"docking_log_{chain_id}.txt"

                # (h) 调用 AutoDockDocking。第三个参数是输出目录，第四个参数只传文件名
                docking = AutoDockDocking(
                    pdbqt_file,
                    ligand_path,
                    output_subdir,       # docking 结果输出目录
                    docking_log_name,    # 只传"文件名"
                    seed
                )

                # (i) 执行对接
                try:
                    docking.run_docking()
                    print(f"[INFO] Docking for {pdbqt_file} completed.\n")
                except Exception as e:
                    print(f"[ERROR] Docking failed for {pdbqt_file}: {e}\n")


if __name__ == "__main__":
    run_docking_for_all_pdbqts(
        root_dir="process_data/create_structure",
        output_root="process_data/lower_energy_docking",
        ligand_suffix="_ligand_trans.mol2",  # 如果你的配体命名有别，可以在此修改
        default_seed=69652
    )


