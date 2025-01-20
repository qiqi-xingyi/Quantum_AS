# --*-- conding:utf-8 --*--
# @Time : 1/19/25 8:55 PM
# @Author : Yuqi Zhang
# @Email : yzhan135@kent.edu
# @File : get_lower_docking_result.py

import os
import re
import glob
from collections import defaultdict

def parse_vina_log(log_path):

    with open(log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    start_index = None
    for i, line in enumerate(lines):
        if line.strip().startswith("-----+"):
            start_index = i
            break

    if start_index is None:
        return (None, None, None)

    data_lines = lines[start_index + 1 : start_index + 10]

    affinity_list = []
    rmsd_lower_list = []
    rmsd_upper_list = []

    for dl in data_lines:

        parts = dl.strip().split()
        if len(parts) >= 4:
            try:
                aff = float(parts[1])
                rmsd_l = float(parts[2])
                rmsd_u = float(parts[3])
                affinity_list.append(aff)
                rmsd_lower_list.append(rmsd_l)
                rmsd_upper_list.append(rmsd_u)
            except:
                pass

    if affinity_list:
        avg_aff = sum(affinity_list) / len(affinity_list)
        avg_rmsd_l = sum(rmsd_lower_list) / len(rmsd_lower_list)
        avg_rmsd_u = sum(rmsd_upper_list) / len(rmsd_upper_list)
        return (avg_aff, avg_rmsd_l, avg_rmsd_u)
    else:
        return (None, None, None)


def get_protein_id_and_top(chain_id):

    match = re.search(r"_top_(\d+)_", chain_id)
    if match:
        return f"top_{match.group(1)}"
    return None


def parse_and_summarize_all_logs(
    docking_root="process_data/lower_energy_docking",
    pattern="docking_log_*.txt"
):

    results = defaultdict(dict)

    log_files = glob.glob(os.path.join(docking_root, "*", pattern))

    for log_file in log_files:
        folder_name = os.path.basename(os.path.dirname(log_file))  # protein_id
        file_name   = os.path.basename(log_file)                   # docking_log_....txt

        avg_affinity, avg_rmsd_l, avg_rmsd_u = parse_vina_log(log_file)

        chain_id = file_name.replace("docking_log_", "").replace(".txt", "")
        top_name = get_protein_id_and_top(chain_id)
        if top_name is None:
            print(f"[WARN] Cannot parse top from {file_name}, skipped.")
            continue

        results[folder_name][top_name] = (avg_affinity, avg_rmsd_l, avg_rmsd_u)

    for protein_id, top_info in results.items():
        out_dir = os.path.join(docking_root, protein_id)
        os.makedirs(out_dir, exist_ok=True)

        summary_path = os.path.join(out_dir, f"summary_{protein_id}.txt")

        sorted_tops = sorted(top_info.keys(), key=lambda x: int(x.split('_')[1]))

        lines = []
        for top_name in sorted_tops:
            aff, rmsd_l, rmsd_u = top_info[top_name]

            if aff is None:
                line_str = f"{top_name}=Affinity=NA, RMSD Lower Bound=NA, RMSD Upper Bound=NA"
            else:
                line_str = (
                    f"{top_name}="
                    f"Affinity={aff:.4f}, "
                    f"RMSD Lower Bound={rmsd_l:.4f}, "
                    f"RMSD Upper Bound={rmsd_u:.4f}"
                )
            lines.append(line_str)

        summary_text = "\n".join(lines)

        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary_text + "\n")

        print(f"[INFO] Summary written for {protein_id} -> {summary_path}")

    print("\n[DONE] All summaries generated.")

if __name__ == "__main__":
    parse_and_summarize_all_logs(
        docking_root="process_data/lower_energy_docking",
        pattern="docking_log_*.txt"
    )



