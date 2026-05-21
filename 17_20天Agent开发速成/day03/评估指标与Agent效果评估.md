---
name: 评估指标与 Agent 效果评估
description: Day03 配套学习内容：机器学习评估指标，以及如何设计完整的 Agent 效果评估方案
type: tutorial
tags: ["评估指标", "准确率", "精确率", "召回率", "F1", "Agent评估"]
created_at: 2026-05-21
updated_at: 2026-05-21
version: interview
---

# 📊 Day03 配套学习：评估指标与 Agent 效果评估

> 💡 **核心思想**：没有量化评估，就没有优化方向。你说你的 Agent 好，怎么证明？用数据说话！

---

## 🎯 学习目标

1. 理解准确率、精确率、召回率、F1 的区别与联系
2. 知道什么时候用精确率，什么时候用召回率
3. 能设计完整的 Agent 效果评估方案
4. ✅ **最重要**：面试时能清晰回答「怎么评估 Agent 的效果？」

---

## 📚 一、混淆矩阵：所有评估指标的基础

所有评估指标都来自混淆矩阵（Confusion Matrix），先把这个搞懂！

### 1.1 二分类混淆矩阵

假设我们在做「垃圾邮件分类」：

| | 预测为正例（垃圾邮件） | 预测为负例（正常邮件） |
|---|-----------------------|-----------------------|
| **实际为正例** | ✅ **TP** True Positive 真正例<br>确实是垃圾邮件，也被识别成垃圾邮件 | ❌ **FN** False Negative 假负例<br>是垃圾邮件，但被当成正常邮件放行了 |
| **实际为负例** | ❌ **FP** False Positive 假正例<br>是正常邮件，但被误判成垃圾邮件了 | ✅ **TN** True Negative 真负例<br>确实是正常邮件，也被识别成正常邮件 |

### 💡 记住这个口诀：

```
第一个字母：预测对不对？
  T = True  预测对了
  F = False 预测错了

第二个字母：预测的是什么？
  P = Positive 预测是正例
  N = Negative 预测是负例
```

### 🎯 面试高频：举例子区分 TP/FP/FN/TN

| 场景 | TP | FP | FN | TN |
|------|----|----|----|----|
| **新冠检测** | 确实阳性，检测也阳 | 没病，检测说阳了 | 有病，检测说阴 | 没病，检测说阴 |
| **人脸识别** | 是你，识别成你 | 不是你，识别成你 | 是你，没识别出来 | 不是你，也没识别成你 |
| **代码审查** | 确实有bug，被发现了 | 没问题，被误报有bug | 有bug，没发现 | 没问题，也没误报 |

---

## 📚 二、四大核心评估指标

### 2.1 准确率 Accuracy

```
准确率 = 预测对的 / 全部 = (TP + TN) / (TP + FP + FN + TN)
```

#### 什么意思？
- 所有预测中，有多少是对的
- 看起来最直观，但**最容易误导人**！

#### ❌ 准确率的陷阱：样本不均衡

例子：1000 个邮件，其中 999 个正常，1 个垃圾
- 模型 A：全部预测成正常邮件
- 准确率 = 999 / 1000 = **99.9%**
- 但这个模型**完全没用**！

> 💡 **面试官常问**：准确率这么高，为什么模型还不行？
> 
> **3分钟回答模板**：
> 
> 准确率高不代表模型好，特别是在样本不均衡的场景下。比如风控场景，1000 个用户里只有 1 个是欺诈用户，模型全部预测成正常，准确率 99.9%，但完全没抓到任何欺诈用户。
> 
> 这就是为什么我们需要精确率和召回率，它们能更真实地反映模型在少数类上的表现。

---

### 2.2 精确率 Precision

```
精确率 = 预测为正例中，真正是正例的比例
       = TP / (TP + FP)
```

#### 什么意思？
- 「你说它是，它到底是不是？」
- 「宁放过，不杀错」

#### 🎯 什么时候看重精确率？

| 场景 | 为什么要精确率高？ | FP 的代价是什么？ |
|------|------------------|-----------------|
| **垃圾邮件** | 宁可放过垃圾邮件，也不能把正常邮件扔垃圾箱 | 客户重要邮件被当成垃圾，损失巨大 |
| **司法判决** | 宁可放过坏人，也不能冤枉好人 | 冤枉好人的代价太大 |
| **医疗诊断（做手术）** | 没病绝不能随便开刀 | 误诊让健康人做手术，后果严重 |

---

### 2.3 召回率 Recall / Sensitivity

```
召回率 = 真正是正例中，被你识别出来的比例
       = TP / (TP + FN)
```

#### 什么意思？
- 「真正是的，有多少被你找到了？」
- 「宁可杀错，不可放过」

#### 🎯 什么时候看重召回率？

| 场景 | 为什么要召回率高？ | FN 的代价是什么？ |
|------|------------------|-----------------|
| **新冠检测** | 宁可多隔离，也不能放跑感染者 | 漏放一个感染者，可能传染一片 |
| **安全漏洞扫描** | 宁可多报，也不能漏掉一个高危漏洞 | 漏掉一个高危漏洞，可能被黑客利用 |
| **癌症筛查** | 宁可误诊，也不能漏掉真正的癌症患者 | 漏掉一个癌症，可能耽误治疗致命 |

---

### 2.4 F1 Score

```
F1 = 2 * (精确率 * 召回率) / (精确率 + 召回率)
```

#### 什么意思？
- 精确率和召回率的调和平均数
- 当精确率和召回率都重要时，用 F1
- F1 高，说明精确率和召回率都不低

---

### 📊 指标对比总结

| 指标 | 公式 | 核心思想 | 看重什么？ |
|------|------|---------|-----------|
| **准确率** | (TP+TN)/全部 | 整体对不对 | 样本均衡时看 |
| **精确率** | TP/(TP+FP) | 别误报 | 宁放过，不杀错 |
| **召回率** | TP/(TP+FN) | 别漏报 | 宁杀错，不放过 |
| **F1** | 2PR/(P+R) | 两者兼顾 | 都重要时看 |

### ⭐ 面试官追问：精确率和召回率矛盾，怎么权衡？

> **3分钟回答模板**：
> 
> 精确率和召回率是此消彼长的关系，需要根据业务场景来权衡。
> 
> 比如垃圾邮件过滤，我们更看重精确率——宁可让一些垃圾邮件进收件箱，也不能把客户的重要邮件扔进垃圾箱。
> 
> 但如果是新冠检测，我们更看重召回率——宁可多隔离一些疑似病例，也不能漏掉任何一个感染者，否则可能造成大面积传播。
> 
> 没有绝对的好坏，关键是看 FP 和 FN 哪个代价更大，选择代价更小的那个。

---

## 📚 三、Agent 效果评估方案设计

### 3.1 为什么 Agent 评估特别难？

Agent 和普通分类器不一样，评估要复杂得多：

1. **输出不是非黑即白**：回答对不对，好不好，是主观的，不是 0/1
2. **工具调用的正确性**：工具调用参数对不对，时机对不对
3. **多轮交互的连贯性**：不是单轮，是一个完整的思考链
4. **最终任务完成度**：最终有没有解决用户的问题

---

### 3.2 Agent 评估的 4 个维度

| 维度 | 评估内容 | 评估方法 |
|------|---------|---------|
| **正确性** | 回答对不对，有没有事实错误 | 标准答案对比 + 大模型打分 + 人工抽样 |
| **工具使用** | 工具调用时机对不对，参数对不对 | 日志分析 + 规则校验 + 成功统计 |
| **效率** | 用了多少步，花了多少 Token，用了多少时间 | 步数统计 + Token 统计 + 耗时统计 |
| **用户体验** | 回复是不是流畅，逻辑是不是清晰 | 用户评分 + 对话流畅度打分 |

---

### 3.3 完整的 Agent 评估方案设计

#### 第一步：定义测试集

```
测试集设计原则：
  1. 覆盖所有典型场景（正常、边界、异常）
  2. 每个场景至少 20-30 个测试用例
  3. 有标准答案或评估标准
  4. 测试集一旦确定，不要随便改（方便版本对比）

例子：代码审查 Agent 测试集
  - 正常场景：有明显bug的代码 20 条
  - 边界场景：没有bug的代码 10 条（测试误报率）
  - 异常场景：语法错误的代码 5 条
  - 复杂场景：多个bug嵌套的代码 5 条
```

#### 第二步：定义评估指标

```
代码审查 Agent 评估指标：

1. Bug 发现率（召回率）
   = 被正确识别的bug数 / 总bug数
   目标：≥ 90%

2. 误报率（1 - 精确率）
   = 被误报成bug的数量 / 总报告bug数
   目标：≤ 10%

3. 平均响应时间
   = 总耗时 / 测试用例数
   目标：≤ 10 秒

4. Token 消耗量
   = 总 Token / 测试用例数
   目标：≤ 2000 Token

5. 用户满意度（人工评分）
   = 1-5 分评分的平均值
   目标：≥ 4.0 分
```

#### 第三步：自动化评估脚本

```python
import json
from typing import List, Dict

class AgentEvaluator:
    def __init__(self, test_cases: List[Dict]):
        self.test_cases = test_cases
        self.results = []
    
    def evaluate_single(self, test_case: Dict, agent_output: Dict) -> Dict:
        """评估单个测试用例"""
        expected_bugs = set(test_case["expected_bugs"])
        actual_bugs = set(b["id"] for b in agent_output["bugs"])
        
        tp = len(expected_bugs & actual_bugs)
        fp = len(actual_bugs - expected_bugs)
        fn = len(expected_bugs - actual_bugs)
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        
        return {
            "test_case_id": test_case["id"],
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "token_used": agent_output.get("token_used", 0),
            "time_used": agent_output.get("time_used", 0)
        }
    
    def evaluate_all(self, agent_outputs: List[Dict]) -> Dict:
        """评估所有测试用例，输出汇总报告"""
        for test_case, output in zip(self.test_cases, agent_outputs):
            self.results.append(self.evaluate_single(test_case, output))
        
        # 汇总统计
        total_tp = sum(r["tp"] for r in self.results)
        total_fp = sum(r["fp"] for r in self.results)
        total_fn = sum(r["fn"] for r in self.results)
        
        avg_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
        avg_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0
        avg_f1 = 2 * avg_precision * avg_recall / (avg_precision + avg_recall) if (avg_precision + avg_recall) > 0 else 0
        
        avg_token = sum(r["token_used"] for r in self.results) / len(self.results)
        avg_time = sum(r["time_used"] for r in self.results) / len(self.results)
        
        return {
            "summary": {
                "precision": round(avg_precision, 4),
                "recall": round(avg_recall, 4),
                "f1": round(avg_f1, 4),
                "avg_token": round(avg_token, 0),
                "avg_time_seconds": round(avg_time, 2),
                "total_test_cases": len(self.results)
            },
            "details": self.results
        }

# 使用示例
if __name__ == "__main__":
    test_cases = [
        {"id": 1, "code": "...", "expected_bugs": ["bug1", "bug2"]},
        {"id": 2, "code": "...", "expected_bugs": []}
    ]
    
    agent_outputs = [
        {"bugs": [{"id": "bug1"}], "token_used": 1500, "time_used": 8.5},
        {"bugs": [], "token_used": 1200, "time_used": 6.2}
    ]
    
    evaluator = AgentEvaluator(test_cases)
    report = evaluator.evaluate_all(agent_outputs)
    print(json.dumps(report, indent=2, ensure_ascii=False))
```

---

## 📚 四、面试话术整理

### 4.1 面试官问：怎么评估 Agent 的效果？

> **3分钟回答模板**：
> 
> 评估 Agent 效果需要从多个维度入手，我一般会设计一个完整的评估方案，包含以下几个部分：
> 
> 第一，先定义测试集。要覆盖所有典型场景，包括正常场景、边界场景、异常场景，每个场景至少 20-30 个测试用例，而且要有明确的评估标准。
> 
> 第二，定义评估指标。从四个维度来看：一是正确性，用精确率和召回率评估任务完成度；二是工具使用正确性，统计工具调用的成功率和参数正确率；三是效率，统计平均耗时、Token 消耗量、思考步数；四是用户体验，人工评分对话流畅度和逻辑性。
> 
> 第三，自动化评估。写脚本批量跑测试集，输出标准化的评估报告，这样每次版本迭代都能快速对比效果。
> 
> 第四，人工抽样审核。对于自动化评估出来的 bad case，人工复盘，找出问题原因，指导下一轮优化。
> 
> 最后，最重要的是：评估不是一次性的，而是持续的。每次版本迭代都要跑同样的测试集，确保优化是真的有效果，而不是拆东墙补西墙。

### 4.2 面试官问：精确率和召回率怎么选？

> **3分钟回答模板**：
> 
> 精确率和召回率是此消彼长的关系，没有绝对的好坏，关键看业务场景中 FP 和 FN 哪个代价更大。
> 
> 如果 FP 的代价大——比如垃圾邮件过滤，把正常邮件判成垃圾邮件的代价很大——那我们就看重精确率，宁放过不杀错。
> 
> 如果 FN 的代价大——比如新冠检测，漏掉一个感染者的代价很大——那我们就看重召回率，宁杀错不放过。
> 
> 如果两者都重要，就用 F1 Score，它是精确率和召回率的调和平均数。
> 
> 一句话总结：看误报和漏报哪个你更不能接受，不能接受误报就看精确率，不能接受漏报就看召回率。

---

**🎉 恭喜学完评估指标！现在你的 Agent 优化终于有了量化的方向！ 🚀**
