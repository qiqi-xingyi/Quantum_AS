# --*-- conding:utf-8 --*--
# @Time : 11/14/24 9:26 PM
# @Author : Yuqi Zhang
# @Email : yzhan135@kent.edu
# @File : prepare_docking.py

from files_tool import QuantumResult
import os
import shutil
from files_tool import DockingFilePreparer
from files_tool import Mol2Translator

def create_full_protein(path):
    quantum_result = QuantumResult(path)

    # Read xyz process_data
    quantum_result.read_xyz()

    # Adjust the coordinate scale to match the average Cα-Cα distance
    quantum_result.adjust_scale()

    # Write the Cα PDB file using the scaled coordinates
    quantum_result.write_ca_pdb()

    # Prepare the alignment file required by Modeller
    quantum_result.prepare_alignment()

    # Generate the full atomic model using Modeller
    quantum_result.generate_full_model()


def rename_and_move_file(current_path, new_name, target_directory):

    new_path = os.path.join(os.path.dirname(current_path), new_name)
    os.rename(current_path, new_path)
    print(f"File renamed to {new_name}")
    os.makedirs(target_directory, exist_ok=True)
    target_path = os.path.join(target_directory, new_name)
    shutil.move(new_path, target_path)
    print(f"File moved to {target_path}")

def create_docking_file(Q_res_path, AF2_res_path, id):

    preparer = DockingFilePreparer(Q_res_path)
    q_translated_pdb = f"./process_data/best_group/{id}/full_model_trans.pdb"
    preparer.prepare_pdbqt(translate=True, output_translated_file=q_translated_pdb)

    preparer = DockingFilePreparer(AF2_res_path)
    af_translated_pdb = f"process_data/best_group/{id}/alphafold_predicted/fold_model_trans.pdb"
    preparer.prepare_pdbqt(translate=True, output_translated_file=af_translated_pdb)
    preparer.prepare_pdbqt()


if __name__ == '__main__':
    protein_id= "1a9m"

    xyz_file_path = f'process_data/best_group/{protein_id}/{protein_id}.xyz'
    Q_res_path = f"process_data/best_group/{protein_id}/full_model.pdb"
    AF3_res_path = f"process_data/best_group/{protein_id}/alphafold_predicted/fold_model_3.cif"

    create_full_protein(xyz_file_path)

    rename_and_move_file(f'protein_full.B99990001.pdb', 'full_model.pdb', f'./process_data/best_group/{protein_id}')

    create_docking_file(Q_res_path, AF3_res_path, protein_id)

    # Initialize the translator with input and output file paths
    translator = Mol2Translator(f"./process_data/best_group/{protein_id}/PDBbind_data/{protein_id}/{protein_id}_ligand.mol2",
                                f"./process_data/best_group/{protein_id}/PDBbind_data/{protein_id}/{protein_id}_ligand_trans.mol2")

    # Perform the translation
    translator.prepare_translated_mol2()