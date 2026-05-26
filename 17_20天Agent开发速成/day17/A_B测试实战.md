
---
name: A_B测试实战
description: A_B测试实战完整指南：实验设计、指标分析、结果解读
type: knowledge
tags: ["A/B测试", "实验", "统计"]
summary: A_B测试实战完整指南
created_at: 2026-05-26
updated_at: 2026-05-26
version: interview
---

# A/B测试实战 🧪

&gt; 🎯 **本章目标**：理解如何设计和分析A/B测试  
&gt; ⏰ **预计时间**：60 分钟

---

## 一、A/B测试简介

### 什么是A/B测试？

- 对照组（A）：原方案
- 实验组（B）：新方案
- 随机分流，对比效果

---

## 二、A/B测试步骤

### 完整流程

1. **确定目标**：要改进什么指标？（点击率、转化率...）
2. **设计实验**：确定样本量、流量分配、实验时长
3. **开发上线**：实现两个版本
4. **收集数据**：埋点记录用户行为
5. **统计分析**：检验显著性
6. **决策**：是否上线新方案？

---

## 三、统计显著性检验

### 简化示例（卡方检验）

```python
import math

def chi_square_test(a_impressions, a_conversions, b_impressions, b_conversions):
    """简化的卡方检验"""
    # 计算转化率
    a_rate = a_conversions / a_impressions
    b_rate = b_conversions / b_impressions
    
    # 计算期望
    total_conversions = a_conversions + b_conversions
    total_impressions = a_impressions + b_impressions
    expected_rate = total_conversions / total_impressions
    
    a_expected = a_impressions * expected_rate
    b_expected = b_impressions * expected_rate
    a_expected_neg = a_impressions * (1 - expected_rate)
    b_expected_neg = b_impressions * (1 - expected_rate)
    
    # 卡方值
    chi_square = (
        ((a_conversions - a_expected) ** 2) / a_expected +
        ((a_impressions - a_conversions - a_expected_neg) ** 2) / a_expected_neg +
        ((b_conversions - b_expected) ** 2) / b_expected +
        ((b_impressions - b_conversions - b_expected_neg) ** 2) / b_expected_neg
    )
    
    # p值（简化：用卡方值估算）
    # 自由度1的卡方分布：3.84对应p=0.05
    if chi_square &lt; 3.84:
        p_value = "&gt; 0.05 (不显著)"
        significant = False
    else:
        p_value = "&lt; 0.05 (显著)"
        significant = True
        
    return {
        "a_rate": round(a_rate * 100, 2),
        "b_rate": round(b_rate * 100, 2),
        "lift": round((b_rate - a_rate) / a_rate * 100, 2),
        "chi_square": round(chi_square, 2),
        "p_value": p_value,
        "significant": significant
    }

# 示例
print("案例1：差异显著")
result1 = chi_square_test(1000, 100, 1000, 130)
print(f"  A组：{result1['a_rate']}%")
print(f"  B组：{result1['b_rate']}%")
print(f"  提升：{result1['lift']}%")
print(f"  显著：{result1['significant']} ({result1['p_value']})")

print("\n案例2：差异不显著")
result2 = chi_square_test(1000, 100, 1000, 105)
print(f"  A组：{result2['a_rate']}%")
print(f"  B组：{result2['b_rate']}%")
print(f"  提升：{result2['lift']}%")
print(f"  显著：{result2['significant']} ({result2['p_value']})")
```

---

## 四、面试要点

### 高频面试题

1. **什么是A/B测试？**
   - 随机将用户分成两组
   - A组：对照组（旧方案）
   - B组：实验组（新方案）
   - 对比指标差异，统计显著性

2. **如何判断A/B测试结果是否显著？**
   - p值 &lt; 0.05：统计显著
   - 置信区间不包含0

3. **A/B测试需要注意什么？**
   - 样本量足够
   - 随机分流
   - 实验时间足够长（避免新奇效应）
   - 只改一个变量
   - 不偷看中期结果

---

**🎉 本章完成！**
