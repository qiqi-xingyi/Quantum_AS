# --*-- conding:utf-8 --*--
# @Time : 1/19/25 5:59 PM
# @Author : Yuqi Zhang
# @Email : yzhan135@kent.edu
# @File : compute_rmsd.py

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import MDAnalysis as mda
from MDAnalysis.analysis import align
from MDAnalysis.analysis.rms import rmsd

# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import MDAnalysis as mda
from MDAnalysis.analysis import align
from MDAnalysis.analysis.rms import rmsd


def main():
    # ------------------------
    # Configuration Variables
    # ------------------------
    reference_file = "1a9m/PDBbind_data/1a9m/1a9m_pocket.pdb"  # Path to reference PDB
    predicted_file = "1a9m/full_model_trans.pdb"  # Path to predicted structure (PDB or CIF)

    ref_chain_id = "A"  # Chain ID in reference structure
    pred_chain_id = "A"  # Chain ID in predicted structure

    start_res = 47  # Start residue number (inclusive)
    end_res = 54  # End residue number (inclusive)

    # Select only CA atoms. You could modify this selection if needed (e.g., backbone atoms)
    ref_selection_str = f"(chainID {ref_chain_id} and resid {start_res}:{end_res} and name CA)"
    pred_selection_str = f"(chainID {pred_chain_id} and resid {start_res}:{end_res} and name CA)"

    # Load reference and predicted structures
    ref_universe = mda.Universe(reference_file)
    pred_universe = mda.Universe(predicted_file)

    # Select atoms
    ref_atoms = ref_universe.select_atoms(ref_selection_str)
    pred_atoms = pred_universe.select_atoms(pred_selection_str)

    if len(ref_atoms) == 0:
        raise ValueError(f"No atoms found in the reference structure with selection: {ref_selection_str}")
    if len(pred_atoms) == 0:
        raise ValueError(f"No atoms found in the predicted structure with selection: {pred_selection_str}")

    # Align predicted structure to reference based on the selected atoms
    align.alignto(
        pred_universe,
        ref_universe,
        select=pred_selection_str,
        reference_selection=ref_selection_str
    )

    # Calculate RMSD
    # center=True, superposition=True means both sets of atoms are centered and superimposed before RMSD calculation
    rmsd_value = rmsd(
        pred_atoms.positions,
        ref_atoms.positions,
        center=True,
        superposition=True
    )

    print("Reference selection:", ref_selection_str)
    print("Predicted selection:", pred_selection_str)
    print(f"RMSD = {rmsd_value:.3f} Å")

if __name__ == "__main__":
    main()

