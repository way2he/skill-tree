
# -*- coding: utf-8 -*-
"""
Day06 Code 01：分块策略演示
"""

print("=" * 60)
print("Day06 - 分块策略演示")
print("=" * 60)

# 1. 简单固定大小分块
print("\n" + "=" * 60)
print("1. 固定大小分块")
print("=" * 60)
sample_text = """Python 是一种解释型、高级、通用的编程语言，由 Guido van Rossum 于 1991 年首次发布。Python 的设计哲学强调代码的可读性，使用显著的缩进。

Python 支持多种编程范式，包括面向对象、命令式、函数式和过程式编程。Python 的标准库提供了丰富的功能，被称为'电池包括'哲学。

Python 广泛应用于 Web 开发、数据分析、人工智能、科学计算等领域。

JavaScript 主要用于网页前端开发，也可以通过 Node.js 做后端开发。
Java 是编译型语言，运行在 JVM 上，是企业级应用的首选。
"""

def simple_chunking(text, chunk_size=100, overlap=20):
    """简单固定大小分块"""
    chunks = []
    i = 0
    while i &lt; len(text):
        chunks.append(text[i:i+chunk_size])
        i += (chunk_size - overlap)
    return chunks

chunks = simple_chunking(sample_text, chunk_size=120, overlap=30)
print(f"\n原文长度: {len(sample_text)} 字符")
print(f"分成: {len(chunks)} 块")
for i, chunk in enumerate(chunks[:3], 1):
    print(f"\n--- 块 {i} ---")
    print(chunk)

# 2. 语义分块（按段落）
print("\n" + "=" * 60)
print("2. 语义分块（按段落）")
print("=" * 60)
paragraphs = sample_text.split("\n\n")
print(f"\n分成: {len(paragraphs)} 段落")
for i, para in enumerate(paragraphs, 1):
    print(f"\n--- 段落 {i} ---")
    print(para[:80] + "..." if len(para) &gt; 80 else para)

print("\n" + "=" * 60)
print("三种分块策略对比")
print("=" * 60)
print("""
1. 固定大小: 简单但可能切断语义
2. 语义分块: 按段落/标题切，推荐
3. 父子分块: 兼顾召回和精准，效果最好
""")
