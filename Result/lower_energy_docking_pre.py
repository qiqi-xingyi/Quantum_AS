# --*-- conding:utf-8 --*--
# @Time : 1/19/25 7:51 PM
# @Author : Yuqi Zhang
# @Email : yzhan135@kent.edu
# @File : lower_energy_docking_pre.py

import os
import shutil
from files_tool import QuantumResult, DockingFilePreparer


def create_full_protein(xyz_path):
    """
    调用 QuantumResult 从 xyz 文件生成 Modeller 输出:
      1. 读取并缩放坐标
      2. 输出 Cα PDB
      3. 生成用于 Modeller 的对齐文件
      4. 通过 Modeller 生成完整蛋白结构(protein_full.B99990001.pdb)
    """
    quantum_result = QuantumResult(xyz_path)
    quantum_result.read_xyz()
    quantum_result.adjust_scale()
    quantum_result.write_ca_pdb()
    quantum_result.prepare_alignment()
    quantum_result.generate_full_model()


def rename_and_move_file(current_path, new_name, target_directory):
    """
    将 Modeller 输出的 protein_full.B99990001.pdb 重命名并挪到
    xyz 文件所在目录下，避免互相覆盖。
    """
    new_path = os.path.join(os.path.dirname(current_path), new_name)
    os.rename(current_path, new_path)
    print(f"[INFO] File renamed to {new_name}")

    os.makedirs(target_directory, exist_ok=True)
    target_path = os.path.join(target_directory, new_name)
    shutil.move(new_path, target_path)
    print(f"[INFO] File moved to {target_path}")


def create_docking_file(pdb_file_path, base_name):
    """
    给定刚生成的 full_model.pdb 路径，调用 DockingFilePreparer
    生成对接所需的 pdbqt 文件。为防止互相覆盖，
    输出文件同样带上 base_name 前缀。
    """
    folder = os.path.dirname(pdb_file_path)
    # 生成一个独立名字, 如 1a9m_top_1_full_model_trans.pdb
    translated_pdb = os.path.join(folder, f"{base_name}_full_model_trans.pdb")

    # DockingFilePreparer会在相同名字下生成对应 .pdbqt 文件
    preparer = DockingFilePreparer(pdb_file_path)
    preparer.prepare_pdbqt(translate=True, output_translated_file=translated_pdb)

    print(f"[INFO] Docking files generated: {translated_pdb} / {translated_pdb}.pdbqt")


def process_single_xyz(xyz_file_path):
    """
    针对单个 xyz 文件，生成独立的 pdb / pdbqt 文件:
      - 先用 Modeller 输出 protein_full.B99990001.pdb
      - 重命名并移到 xyz 同目录下 (加上 xyz 文件名前缀)
      - 最后调用 create_docking_file() 生成对应 pdbqt
    """
    # 取得不带后缀的文件名, 如 "1a9m_top_1"
    base_name = os.path.splitext(os.path.basename(xyz_file_path))[0]

    # 1. 调用 Modeller 生成 protein_full.B99990001.pdb
    create_full_protein(xyz_file_path)

    # 2. 重命名并移到 xyz 同目录, 如 "1a9m_top_1_full_model.pdb"
    modeller_output = "protein_full.B99990001.pdb"
    unique_pdb_name = f"{base_name}_full_model.pdb"
    target_directory = os.path.dirname(xyz_file_path)
    rename_and_move_file(
        modeller_output,
        unique_pdb_name,
        target_directory
    )

    # 3. 基于重命名后的 pdb, 生成对接所需的 pdbqt
    full_model_path = os.path.join(target_directory, unique_pdb_name)
    create_docking_file(full_model_path, base_name)


def process_all_xyz(root_dir="process_data/create_structure"):
    """
    遍历 root_dir 下所有子文件夹，找到每个 xyz 文件，
    逐个执行完整处理流程，避免互相覆盖。
    """
    for current_root, dirs, files in os.walk(root_dir):
        for file_name in files:
            if file_name.endswith(".xyz"):
                xyz_path = os.path.join(current_root, file_name)
                print(f"\n[INFO] Now processing: {xyz_path}")
                try:
                    process_single_xyz(xyz_path)
                except Exception as e:
                    print(f"[ERROR] Failed to process {xyz_path}: {e}")


if __name__ == "__main__":
    # 修改为你实际存放 xyz 文件的路径
    process_all_xyz("process_data/create_structure")




