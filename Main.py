# --*-- conding:utf-8 --*--
# @Time : 1/17/25 11:14 PM
# @Author : Yuqi Zhang
# @Email : yzhan135@kent.edu
# @File : Main.py

import os
from Protein_Folding import Peptide
from Protein_Folding.interactions.miyazawa_jernigan_interaction import MiyazawaJerniganInteraction
from Protein_Folding.penalty_parameters import PenaltyParameters
from Protein_Folding.protein_folding_problem import ProteinFoldingProblem
from qiskit_ibm_runtime import QiskitRuntimeService
from Qiskit_VQE import VQE5
from Qiskit_VQE import StateCalculator

def predict_protein_structure(
    main_chain_sequence: str,
    protein_id: str,
    service: QiskitRuntimeService,
    max_iter: int = 150
):
    """
    Use the given quantum VQE workflow to predict a protein structure based on the
    specified amino acid sequence, and store the results in corresponding directories.

    :param main_chain_sequence: The main chain amino acid sequence (single-letter representation).
    :param protein_id: The identifier/name for the protein (used to name output files).
    :param service: An instance of QiskitRuntimeService for submitting quantum jobs.
    :param max_iter: Maximum iteration count for VQE, default=150.
    """

    print(f"Starting prediction for protein: {protein_id}, sequence: {main_chain_sequence}")

    # Create side chain sequences (empty in this demo)
    side_chain_sequences = ['' for _ in range(len(main_chain_sequence))]

    # Print basic information
    chain_length = len(main_chain_sequence)
    print(f"Number of amino acids: {chain_length}")

    side_chain_count = len(side_chain_sequences)
    print(f"Number of side chain sites: {side_chain_count}")

    # 1. Create a Peptide object
    peptide = Peptide(main_chain_sequence, side_chain_sequences)

    # 2. Define the interaction model (Miyazawa-Jernigan)
    mj_interaction = MiyazawaJerniganInteraction()

    # 3. Define the penalty parameters
    penalty_terms = PenaltyParameters(10, 10, 10)

    # 4. Create a Protein Folding Problem
    protein_folding_problem = ProteinFoldingProblem(peptide, mj_interaction, penalty_terms)

    # 5. Build the quantum Hamiltonian
    hamiltonian = protein_folding_problem.qubit_op()

    # 6. Calculate required number of qubits (+2 is an example, depending on your project requirements)
    qubits_num = hamiltonian.num_qubits + 2
    print(f"Number of qubits: {qubits_num}")

    # 7. Create and run VQE
    vqe_instance = VQE5(
        service=service,
        hamiltonian=hamiltonian,
        min_qubit_num=qubits_num,
        maxiter=max_iter
    )

    energy_list, res, ansatz, top_results = vqe_instance.run_vqe()

    # 8. Save the energy list
    output_energy_path = f"Result/process_data/{protein_id}/System_Enegry"
    os.makedirs(output_energy_path, exist_ok=True)
    with open(f"{output_energy_path}/energy_list_{protein_id}.txt", 'w') as file:
        for item in energy_list:
            file.write(str(item) + '\n')

    # 9. Calculate the probability distribution
    state_calculator = StateCalculator(service, qubits_num, ansatz)
    probability_distribution = state_calculator.get_probability_distribution(res)

    # 10. Interpret the distribution to get the protein's 3D structure
    protein_result = protein_folding_problem.interpret(probability_distribution)

    # 11. Save probability distribution
    output_prob_path = f"Result/process_data/{protein_id}/Prob_distribution"
    os.makedirs(output_prob_path, exist_ok=True)
    with open(f"{output_prob_path}/prob_distribution.txt", 'w') as file:
        for key, value in probability_distribution.items():
            file.write(f'{key}: {value}\n')

    # 12. Save 3D coordinates (.xyz)
    output_dir = f"Result/process_data/{protein_id}"
    os.makedirs(output_dir, exist_ok=True)
    protein_result.save_xyz_file(name=protein_id, path=output_dir)
    print("Protein structure saved as .xyz file")

    # 13. Save the top-ranked results (if there are multiple local minima or best parameter sets)
    for rank, (energy_val, best_params) in enumerate(top_results, start=1):
        print(f"Top {rank} best energy = {energy_val}")

        prob_dist_best = state_calculator.get_probability_distribution(best_params)
        protein_result_best = protein_folding_problem.interpret(prob_dist_best)
        protein_result_best.save_xyz_file(
            name=f"{protein_id}_top_{rank}",
            path=output_dir
        )
        print(f"Protein structure for top {rank} best result has been saved.")

    print(f"Finished processing: {protein_id} \n")


if __name__ == '__main__':

    service = QiskitRuntimeService(
        channel='ibm_quantum',
        instance=' ',  # Replace with your real instance
        token=' '      # Replace with your real token
    )

    #    (Here, we have four sequences and their corresponding IDs.)
    protein_list = [
        ("GSLTTPPLL", "6ugp"),
        ("DGKMKGLAF", "1qin"),
        ("ARVYSNS",   "4f5y"),
        ("IHGIGGFI",  "1a9m"),
        ("NNLGTIAKSGT", "3b26"),
        ("GAVEDGATMTFF", "2xxx")
    ]

    for sequence, protein_name in protein_list:
        predict_protein_structure(
            main_chain_sequence=sequence,
            protein_id=protein_name,
            service=service,
            max_iter=150
        )
