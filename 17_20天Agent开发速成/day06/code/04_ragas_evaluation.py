
# -*- coding: utf-8 -*-
"""
Day06 Code 04：RAGAS 评估
"""

print("=" * 60)
print("Day06 - RAGAS 评估演示")
print("=" * 60)

# RAGAS 评估数据格式
sample_data = {
    "question": "Python 是谁创建的？",
    "answer": "Python 由 Guido van Rossum 于 1991 年创建。",
    "contexts": [
        "Python 是一种解释型语言，由 Guido van Rossum 于 1991 年首次发布。",
        "Python 的设计哲学强调代码可读性。"
    ],
    "ground_truth": "Python 由 Guido van Rossum 创建，发布于 1991 年。"
}

print("\n评估数据格式:")
print(f"  question: {sample_data['question']}")
print(f"  answer: {sample_data['answer']}")
print(f"  contexts: {len(sample_data['contexts'])} 个")
print(f"  ground_truth: {sample_data['ground_truth']}")

print("\n" + "=" * 60)
print("RAGAS 5 个核心评估指标:")
print("=" * 60)
print("""
1. Faithfulness: 答案是否忠实于上下文？
2. Answer Relevance: 答案是否相关？
3. Context Precision: 上下文精准度？
4. Context Recall: 上下文召回率？
5. Context Relevance: 上下文相关性？
""")

print("\n" + "=" * 60)
print("安装 RAGAS:")
print("  pip install ragas")
print("=" * 60)
