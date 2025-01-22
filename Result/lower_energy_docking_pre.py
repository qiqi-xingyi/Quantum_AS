# --*-- conding:utf-8 --*--
# @Time : 1/19/25 7:51 PM
# @Author : Yuqi Zhang
# @Email : yzhan135@kent.edu
# @File : lower_energy_docking_pre.py

import os
import shutil
from files_tool import QuantumResult, DockingFilePreparer


def create_full_protein(xyz_path):

    quantum_result = QuantumResult(xyz_path)
    quantum_result.read_xyz()
    quantum_result.adjust_scale()
    quantum_result.write_ca_pdb()
    quantum_result.prepare_alignment()
    quantum_result.generate_full_model()


def rename_and_move_file(current_path, new_name, target_directory):

    new_path = os.path.join(os.path.dirname(current_path), new_name)
    os.rename(current_path, new_path)
    print(f"[INFO] File renamed to {new_name}")

    os.makedirs(target_directory, exist_ok=True)
    target_path = os.path.join(target_directory, new_name)
    shutil.move(new_path, target_path)
    print(f"[INFO] File moved to {target_path}")


def create_docking_file(pdb_file_path, base_name):

    folder = os.path.dirname(pdb_file_path)

    translated_pdb = os.path.join(folder, f"{base_name}_full_model_trans.pdb")


    preparer = DockingFilePreparer(pdb_file_path)
    preparer.prepare_pdbqt(translate=True, output_translated_file=translated_pdb)

    print(f"[INFO] Docking files generated: {translated_pdb} / {translated_pdb}.pdbqt")


def process_single_xyz(xyz_file_path):

    base_name = os.path.splitext(os.path.basename(xyz_file_path))[0]


    create_full_protein(xyz_file_path)


    modeller_output = "protein_full.B99990001.pdb"
    unique_pdb_name = f"{base_name}_full_model.pdb"
    target_directory = os.path.dirname(xyz_file_path)
    rename_and_move_file(
        modeller_output,
        unique_pdb_name,
        target_directory
    )


    full_model_path = os.path.join(target_directory, unique_pdb_name)
    create_docking_file(full_model_path, base_name)


def process_all_xyz(root_dir="process_data/create_structure"):

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

    process_all_xyz("process_data/create_structure")




