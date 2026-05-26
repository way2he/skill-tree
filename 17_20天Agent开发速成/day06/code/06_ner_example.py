
# -*- coding: utf-8 -*-
"""
Day06 Code 06：NER 实战
"""

print("=" * 60)
print("Day06 - NER（命名实体识别）演示")
print("=" * 60)

text = "张三在 2024 年 1 月去北京的阿里巴巴出差，开会讨论 AI 项目。"
print(f"\n输入文本: {text}")

# 模拟 NER 输出
print("\nNER 识别结果:")
print("  [人名] 张三")
print("  [时间] 2024 年 1 月")
print("  [地名] 北京")
print("  [组织名] 阿里巴巴")

print("\n" + "=" * 60)
print("NER 常用方法:")
print("=" * 60)
print("""
1. 规则/词典: 简单场景，维护成本高
2. CRF: 传统方法，效果不错
3. BiLSTM-CRF: 深度学习经典组合
4. BERT/ERNIE + 分类头: 效果最好
""")
