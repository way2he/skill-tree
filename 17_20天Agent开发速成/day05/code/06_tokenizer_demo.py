
# -*- coding: utf-8 -*-
"""
Day05 Code 06: Tokenizer 演示
"""

print("=" * 60)
print("Day05 - Tokenizer 演示")
print("=" * 60)

# ===================== 1. 简单分词演示 =====================
text = "我喜欢用 Python 编程"
print(f"\n原始句子: {text}")

# 简单按空格分词
simple_tokens = text.split()
print(f"\n简单空格分词: {simple_tokens}")

# 按字符
char_tokens = list(text)
print(f"按字符分词: {char_tokens}")

# ===================== 2. HuggingFace Tokenizer =====================
print("\n" + "=" * 60)
print("HuggingFace Tokenizer")
print("=" * 60)

try:
    from transformers import AutoTokenizer
    
    # 加载 BERT 中文 Tokenizer
    print("\n加载 BERT 中文 Tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")
    
    # 分词
    tokens = tokenizer.tokenize(text)
    print(f"\n分词结果 (BERT): {tokens}")
    
    # 转 ID
    input_ids = tokenizer.encode(text)
    print(f"Token IDs: {input_ids}")
    
    # 解码
    decoded = tokenizer.decode(input_ids)
    print(f"解码: {decoded}")
    
    # 完整输出
    print("\n完整输出:")
    output = tokenizer(text)
    for k, v in output.items():
        print(f"  {k}: {v}")
    
except ImportError:
    print("\n请先安装: pip install transformers")

# ===================== 3. BPE 简化演示 =====================
print("\n" + "=" * 60)
print("BPE 简化演示")
print("=" * 60)
print("""
BPE 核心思想: 合并高频出现的字符对

训练过程:
1. 初始词表: 单个字符 (a, b, c, ...)
2. 统计字符对频率
3. 合并最高频的字符对
4. 重复直到词表达标

例子:
初始: l, o, w, n, e, r, ...
合并: 'l'+'o' = 'lo'
合并: 'lo'+'w' = 'low'
最终词表包含: 'low', 'new', 'year', ...
""")

print("\n" + "=" * 60)
print("为什么大模型都用 BPE？")
print("=" * 60)
print("""
1. 词表大小可控（不用存百万级词汇）
2. 可以处理未登录词（拆成子词）
3. 平衡语义和粒度

对比:
- 整词分词: 词表太大，OOV 严重
- 字符分词: 词表小，但没语义
- BPE（子词）: 折中方案，最佳！
""")

print("\n" + "=" * 60)
print("✅ Tokenizer 演示完成！")
print("=" * 60)
