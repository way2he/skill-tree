
# -*- coding: utf-8 -*-
"""
Day07 Code 04：激活函数对比
"""

print("=" * 60)
print("Day07 - 激活函数对比")
print("=" * 60)

print("\n常见激活函数:")
print("  1. ReLU: max(0, x) → 最常用，计算快")
print("  2. GELU: 高斯误差线性单元 → GPT/BERT 都用，效果好")
print("  3. Sigmoid: σ(x)=1/(1+e⁻ˣ) → (0,1)，二分类输出层")
print("  4. Tanh: tanh(x) → (-1,1)，零均值")

print("\n" + "=" * 60)
print("怎么选激活函数？")
print("=" * 60)
print("  - 默认选 GELU")
print("  - 快一点选 ReLU")
print("  - 二分类最后一层选 Sigmoid")
print("  - 多分类最后一层选 Softmax")
