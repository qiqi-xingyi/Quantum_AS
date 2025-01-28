# --*-- conding:utf-8 --*--
# @Time : 1/28/25 5:28 PM
# @Author : Yuqi Zhang
# @Email : yzhan135@kent.edu
# @File : get_info.py

from qiskit.circuit.library import EfficientSU2

# Adjust import paths according to your project structure
from Protein_Folding import Peptide
from Protein_Folding.interactions.miyazawa_jernigan_interaction import MiyazawaJerniganInteraction
from Protein_Folding.penalty_parameters import PenaltyParameters
from Protein_Folding.protein_folding_problem import ProteinFoldingProblem

def build_protein_and_get_qubit_info(main_chain_sequence: str, protein_id: str):
    """
    Build a protein folding Hamiltonian for the given amino-acid sequence,
    then return the required number of qubits and the depth of an EfficientSU2 ansatz.

    :param main_chain_sequence: Amino-acid sequence of the protein
    :param protein_id: Name or identifier of the protein
    :return: A tuple (qubits_num, circuit_depth)
    """
    print(f"========== Processing protein: {protein_id}, sequence: {main_chain_sequence} ==========")

    # Construct empty side chains (demo: empty side chains for each residue)
    side_chain_sequences = ['' for _ in range(len(main_chain_sequence))]

    # 1. Build the peptide object
    peptide = Peptide(main_chain_sequence, side_chain_sequences)

    # 2. Use Miyazawa-Jernigan interaction model
    mj_interaction = MiyazawaJerniganInteraction()

    # 3. Set penalty parameters (adjust if needed)
    penalty_terms = PenaltyParameters(10, 10, 10)

    # 4. Construct the protein folding problem and obtain the Hamiltonian
    protein_folding_problem = ProteinFoldingProblem(peptide, mj_interaction, penalty_terms)
    hamiltonian = protein_folding_problem.qubit_op()

    # 5. Calculate the number of qubits required (+5 is just an example)
    qubits_num = hamiltonian.num_qubits + 5
    print(f"Required number of qubits for {protein_id}: {qubits_num}")

    # 6. Build the EfficientSU2 circuit and calculate its depth
    ansatz = EfficientSU2(num_qubits=qubits_num, entanglement='linear', reps=3)
    decomposed_circuit = ansatz.decompose()
    circuit_depth = decomposed_circuit.depth()
    print(f"EfficientSU2 circuit depth: {circuit_depth}\n")

    return qubits_num, circuit_depth


if __name__ == '__main__':
    protein_list = [
        ("DGKMKGLAF", "1qin"),
        ("IHGIGGFI",  "1a9m"),
        ("KSIVDSGTTNLR", "1fkn"),
        ("NNLGTIAKSGT", "3b26"),
        ("GAVEDGATMTFF", "2xxx"),
        ("DWGGM", "3ans"),
        ("YAGYS", "6mu3")
    ]

    # Write qubit number and circuit depth into a txt file
    log_file = "qubit_depth_log.txt"
    with open(log_file, 'w') as file:
        file.write("Protein_ID,Qubit_Num,Circuit_Depth\n")  # Header

        for sequence, protein_name in protein_list:
            qubits_num, circuit_depth = build_protein_and_get_qubit_info(sequence, protein_name)
            # Write into the log file
            file.write(f"{protein_name},{qubits_num},{circuit_depth}\n")

    print(f"All results have been written to {log_file}")

