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
        root_dir="process_data/create_structure",
        output_root="process_data/lower_energy_docking",
        ligand_suffix="_ligand_trans.mol2",
        default_seed=69652
):

    seed_log_file = os.path.join(output_root, "seed_log.txt")
    os.makedirs(output_root, exist_ok=True)
    with open(seed_log_file, "w", encoding="utf-8") as seed_file:
        seed_file.write("PDBQT_File\tSeed\n")

    for current_root, dirs, files in os.walk(root_dir):
        for file_name in files:
            if file_name.endswith(".pdbqt"):

                pdbqt_file = os.path.join(current_root, file_name)

                rel_path = os.path.relpath(current_root, root_dir)
                output_subdir = os.path.join(output_root, rel_path)
                os.makedirs(output_subdir, exist_ok=True)

                protein_id = os.path.basename(os.path.normpath(current_root))

                ligand_path = os.path.join(
                    "process_data/best_group", protein_id,
                    "PDBbind_data", protein_id,
                    protein_id + ligand_suffix
                )

                seed = default_seed

                print(f"[INFO] Docking: {pdbqt_file} -> {output_subdir}, seed={seed}")

                with open(seed_log_file, "a", encoding="utf-8") as seed_file:
                    seed_file.write(f"{pdbqt_file}\t{seed}\n")

                chain_id = os.path.splitext(file_name)[0]
                docking_log_name = f"docking_log_{chain_id}.txt"

                docking = AutoDockDocking(
                    pdbqt_file,
                    ligand_path,
                    output_subdir,
                    docking_log_name,
                    seed
                )

                try:
                    docking.run_docking()
                    print(f"[INFO] Docking for {pdbqt_file} completed.\n")
                except Exception as e:
                    print(f"[ERROR] Docking failed for {pdbqt_file}: {e}\n")

if __name__ == "__main__":
    run_docking_for_all_pdbqts(
        root_dir="process_data/create_structure",
        output_root="process_data/lower_energy_docking",
        ligand_suffix="_ligand_trans.mol2",
        default_seed=69652
    )


