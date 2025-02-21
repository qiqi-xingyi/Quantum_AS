# --*-- conding:utf-8 --*--
# @Time : 2/21/25 4:04 PM
# @Author : Yuqi Zhang
# @Email : yzhan135@kent.edu
# @File : RMSD.py

import os
from Bio.PDB import PDBParser, MMCIFParser, Superimposer
# 如果要保存对齐后的结构，需要用到：
# from Bio.PDB import PDBIO

def get_structure(file_path, structure_id="structure"):
    """
    根据文件扩展名自动判断使用 PDBParser 还是 MMCIFParser。
    支持 .pdb 或 .cif 文件。
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdb":
        parser = PDBParser(QUIET=True)
    elif ext == ".cif":
        parser = MMCIFParser(QUIET=True)
    else:
        raise ValueError(f"不支持的文件格式: {ext}，请使用 .pdb 或 .cif")
    return parser.get_structure(structure_id, file_path)


def calculate_rmsd(
    full_structure,
    frag_structure,
    full_chain_id='A',
    start_resid=10,
    end_resid=20,
    fragment_chain_id='A',
    selection='CA'
):
    """
    full_structure       : 完整蛋白的 Bio.PDB.Structure 对象
    frag_structure       : 片段的 Bio.PDB.Structure 对象
    full_chain_id        : 完整蛋白中需要对比的链名（默认 'A'）
    start_resid, end_resid : 完整蛋白中需要对比的残基编号范围（含端点）
    fragment_chain_id    : 片段中对应的链名
    selection            : 'CA' 或 'all'
                           - 'CA'  : 仅使用 Cα 原子
                           - 'all' : 使用对应残基的所有原子
    return               : superimposer.rms (RMSD 值, Å)
    """
    # 取第一个 model（大多数情况下 PDB/CIF 只有一个 model）
    full_model = full_structure[0]
    frag_model = frag_structure[0]

    # 获取完整蛋白指定链
    try:
        full_chain = full_model[full_chain_id]
    except KeyError:
        raise ValueError(f"完整蛋白中不存在链 {full_chain_id}")

    # 获取片段中的对应链
    try:
        frag_chain = frag_model[fragment_chain_id]
    except KeyError:
        raise ValueError(f"片段结构中不存在链 {fragment_chain_id}")

    # 从完整蛋白中获取指定残基范围
    full_residues = [
        residue for residue in full_chain
        if start_resid <= residue.id[1] <= end_resid
    ]
    # 获取片段中的所有残基（如果你知道片段的残基区间，也可额外筛选）
    frag_residues = [res for res in frag_chain]

    # 检查残基数目是否一致（简单情形）
    if len(full_residues) != len(frag_residues):
        raise ValueError(
            f"选取的完整蛋白片段残基数({len(full_residues)}) "
            f"与片段文件残基数({len(frag_residues)})不匹配，请检查。"
        )

    full_atoms = []
    frag_atoms = []

    # 根据选项选择原子
    for fr, rr in zip(full_residues, frag_residues):
        if selection == 'CA':
            # 仅选 Cα
            full_atoms.append(fr['CA'])
            frag_atoms.append(rr['CA'])
        elif selection == 'all':
            # 获取两个残基的所有原子，但需确保原子命名对应相同
            fr_atoms_dict = {atom.name: atom for atom in fr if atom.name.strip()}
            rr_atoms_dict = {atom.name: atom for atom in rr if atom.name.strip()}

            common_atom_names = set(fr_atoms_dict.keys()) & set(rr_atoms_dict.keys())
            if not common_atom_names:
                raise ValueError(
                    f"残基 {fr} 与 {rr} 没有共同的原子用于对齐，请检查命名或结构。"
                )
            for atom_name in sorted(common_atom_names):
                full_atoms.append(fr_atoms_dict[atom_name])
                frag_atoms.append(rr_atoms_dict[atom_name])
        else:
            raise ValueError("selection 参数必须是 'CA' 或 'all'")

    # 进行叠合
    super_imposer = Superimposer()
    super_imposer.set_atoms(full_atoms, frag_atoms)
    rmsd_value = super_imposer.rms  # Å

    # 如果需要将对齐变换应用到片段结构，可以在此处执行：
    # super_imposer.apply(frag_model.get_atoms())

    return rmsd_value


# 1) 指定完整蛋白和片段的文件路径（可分别为 .pdb 或 .cif）
full_structure_file = "./6mu3/PDBbind_data/6mu3/6mu3_protein.pdb"  # 或 .cif
fragment_structure_file = "./6mu3/ca_model.pdb"  # 或 .pdb

# 2) 完整蛋白中需要进行比对的链和残基范围
full_chain_id = "L"
start_resid = 91
end_resid = 95

# 3) 片段对应的链名
frag_chain_id = "L"

# 4) 比对策略：'CA' 或 'all'
selection_mode = "CA"

# 5) 输出 RMSD 的文本文件名
output_file_name = "./6mu3/rmsd_result_Q.txt"

# =========== 主程序部分 ===========

if __name__ == "__main__":
    # 读取两个结构（自动识别 pdb/cif）
    full_structure = get_structure(full_structure_file, "full_protein")
    frag_structure = get_structure(fragment_structure_file, "fragment")

    # 计算 RMSD
    rmsd_value = calculate_rmsd(
        full_structure,
        frag_structure,
        full_chain_id=full_chain_id,
        start_resid=start_resid,
        end_resid=end_resid,
        fragment_chain_id=frag_chain_id,
        selection=selection_mode
    )

    # 打印并保存结果
    msg = (f"对比文件:\n"
           f"  完整蛋白: {os.path.basename(full_structure_file)} (链 {full_chain_id}, 残基 {start_resid}-{end_resid})\n"
           f"  片段: {os.path.basename(fragment_structure_file)} (链 {frag_chain_id})\n"
           f"比对策略: {selection_mode}\n"
           f"RMSD: {rmsd_value:.3f} Å\n")

    print(msg)

    with open(output_file_name, "w", encoding="utf-8") as f:
        f.write(msg)

    print(f"RMSD 已保存至文件: {output_file_name}")

    # 如果需要将对齐后的片段写出为 PDB 文件，取消以下注释：
    """
    # 应用叠合变换
    from Bio.PDB import PDBIO
    super_imposer = Superimposer()
    # 按与 calculate_rmsd 相同的方式获取要对齐的原子
    # 或者直接在 calculate_rmsd 函数内先 super_imposer.set_atoms(...)，再取出来
    super_imposer.set_atoms(full_atoms, frag_atoms)  
    super_imposer.apply(frag_model.get_atoms())

    io = PDBIO()
    io.set_structure(frag_structure)  # 已经变换好的片段结构
    io.save("aligned_fragment.pdb")
    """
