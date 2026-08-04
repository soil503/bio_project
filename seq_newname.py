import sys
import pandas as pd
from Bio import SeqIO

# 1. 读取处理后的 GFF，索引是 mRNA ID（第1列，比如 PNS24245）
data = pd.read_csv(sys.argv[1], sep="\t", header=None, index_col=1)

# 2. 构建 ID 映射字典：{mRNA_ID: 目标ID}
# 示例1：如果要把 PNS24245 → 基因 ID（比如去掉转录本后缀）
# data.index = data.index.str[:-3]  # 按需启用
# id_dict = data[0].to_dict()  # 键=mRNA ID，值=染色体号（或基因 ID）

# 示例2：如果要把 PNS24245 → BRADI_xxxx（适配你的 Bd 数据）
id_dict = {k: f"BRADI_{k[3:]}" for k in data.index}

print(data.head())

seqs = []
n = 0

# 3. 遍历 pep.fasta，重命名 ID
for seq_record in SeqIO.parse(sys.argv[2], "fasta"):
    if seq_record.id in id_dict:
        seq_record.id = id_dict[seq_record.id]
        n += 1
    # 保留所有序列，不要 else: continue
    seqs.append(seq_record)

# 4. 写入新的 fasta 文件
SeqIO.write(seqs, sys.argv[3], "fasta")
print(f"重命名完成，共处理 {n} 条序列")