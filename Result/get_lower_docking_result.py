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
    """
    读取给定日志文件，从“-----+------------+----------+----------”这一行
    开始，固定读取后面 9 行，并分别解析：
      - affinity (列2)
      - rmsd lower bound (列3)
      - rmsd upper bound (列4)
    返回 (avg_affinity, avg_rmsd_lower, avg_rmsd_upper) 三元组。
    若解析不到数据，则返回 (None, None, None)。
    """
    with open(log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 1) 找到分割线 "-----+------------+----------+----------"
    start_index = None
    for i, line in enumerate(lines):
        if line.strip().startswith("-----+"):
            start_index = i
            break

    # 如果找不到这行，则无数据
    if start_index is None:
        return (None, None, None)

    # 2) 取分割线下面的 9 行
    data_lines = lines[start_index + 1 : start_index + 10]

    affinity_list = []
    rmsd_lower_list = []
    rmsd_upper_list = []

    for dl in data_lines:
        # 每行类似： "   1       -3.721          0          0"
        parts = dl.strip().split()
        if len(parts) >= 4:
            try:
                aff = float(parts[1])  # 第2列 = affinity
                rmsd_l = float(parts[2])  # 第3列 = rmsd lower
                rmsd_u = float(parts[3])  # 第4列 = rmsd upper
                affinity_list.append(aff)
                rmsd_lower_list.append(rmsd_l)
                rmsd_upper_list.append(rmsd_u)
            except:
                # 解析失败则跳过
                pass

    # 若有数据则求平均
    if affinity_list:
        avg_aff = sum(affinity_list) / len(affinity_list)
        avg_rmsd_l = sum(rmsd_lower_list) / len(rmsd_lower_list)
        avg_rmsd_u = sum(rmsd_upper_list) / len(rmsd_upper_list)
        return (avg_aff, avg_rmsd_l, avg_rmsd_u)
    else:
        return (None, None, None)


def get_protein_id_and_top(chain_id):
    """
    假设日志文件名包含 'xxx_top_1_full_model' 之类，
    用正则提取 'top_数字' 返回，如 'top_1'；若没匹配到则返回 None。
    """
    match = re.search(r"_top_(\d+)_", chain_id)
    if match:
        return f"top_{match.group(1)}"
    return None


def parse_and_summarize_all_logs(
    docking_root="process_data/lower_energy_docking",
    pattern="docking_log_*.txt"
):
    """
    遍历 docking_root/<protein_id>/ 目录下所有 docking_log_*.txt 文件，
    对每个文件解析 (Affinity, RMSD lower, RMSD upper) 三项平均值，
    最终在 summary_{protein_id}.txt 中用一行写出：
      top_1=Affinity=-3.1686, RMSD Lower Bound=2.2758, RMSD Upper Bound=5.0687
      top_2=...
    """
    # 字典结构: results[protein_id][top_name] = (aff_avg, rmsd_l_avg, rmsd_u_avg)
    results = defaultdict(dict)

    # 如果日志文件都在一层： docking_root/<protein_id>/docking_log_XXX.txt
    log_files = glob.glob(os.path.join(docking_root, "*", pattern))
    # 如果日志更深层，则可改成:
    # log_files = glob.glob(os.path.join(docking_root, "**", pattern), recursive=True)

    for log_file in log_files:
        folder_name = os.path.basename(os.path.dirname(log_file))  # protein_id
        file_name   = os.path.basename(log_file)                   # docking_log_....txt

        # 解析平均值
        avg_affinity, avg_rmsd_l, avg_rmsd_u = parse_vina_log(log_file)

        # 提取 top_x
        chain_id = file_name.replace("docking_log_", "").replace(".txt", "")
        top_name = get_protein_id_and_top(chain_id)
        if top_name is None:
            print(f"[WARN] Cannot parse top from {file_name}, skipped.")
            continue

        # 存在字典
        results[folder_name][top_name] = (avg_affinity, avg_rmsd_l, avg_rmsd_u)

    # 输出 summary_{protein_id}.txt
    for protein_id, top_info in results.items():
        out_dir = os.path.join(docking_root, protein_id)
        os.makedirs(out_dir, exist_ok=True)

        summary_path = os.path.join(out_dir, f"summary_{protein_id}.txt")
        # 按 top_1, top_2, ... 排序
        sorted_tops = sorted(top_info.keys(), key=lambda x: int(x.split('_')[1]))

        lines = []
        for top_name in sorted_tops:
            aff, rmsd_l, rmsd_u = top_info[top_name]

            # 如果解析失败则写成NA
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

        # 根据需要，每个 top 构象输出一行 or 多个放一起
        # 此处演示每个 top 构象占一行
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



