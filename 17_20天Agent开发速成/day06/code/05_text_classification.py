
# -*- coding: utf-8 -*-
"""
Day06 Code 05：文本分类
"""

print("=" * 60)
print("Day06 - 文本分类演示")
print("=" * 60)

# 文本分类例子
texts = [
    "iPhone 15 降价促销，现在买很划算",
    "Python 3.12 发布，新特性很多",
    "今天天气真好，适合出去走走",
    "机器学习入门教程，从基础到实践",
    "2024 年奥运会即将举办"
]

labels = ["科技", "科技", "生活", "科技", "体育"]

print("\n文本分类例子:")
for text, label in zip(texts, labels):
    print(f"\n文本: {text}")
    print(f"分类: {label}")

print("\n" + "=" * 60)
print("文本分类方法:")
print("=" * 60)
print("""
传统 ML:
1. TF-IDF + SVM / Logistic Regression
2. FastText

深度学习:
1. BERT / ERNIE 等预训练模型
2. TextCNN
3. BiLSTM
""")
