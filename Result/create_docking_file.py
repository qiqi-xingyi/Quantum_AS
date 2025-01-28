# --*-- conding:utf-8 --*--
# @Time : 11/14/24 12:48 AM
# @Author : Yuqi Zhang
# @Email : yzhan135@kent.edu
# @File : create_docking_file.py


from files_tool import DockingFilePreparer


if __name__ == "__main__":

    preparer = DockingFilePreparer("process_data/best_group/1fkn/protein_full.B99990001.pdb")
    preparer.prepare_pdbqt()


