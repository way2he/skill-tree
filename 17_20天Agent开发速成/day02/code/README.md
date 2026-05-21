# Day02 代码目录

## 代码清单

| 文件名 | 功能 |
|--------|------|
| 01_role_setting.py | 角色设定方法论 |
| 02_cot_techniques.py | 思维链 CoT 4 种技巧 |
| 03_fewshot_best_practice.py | Few-shot 最佳实践 |
| 04_structured_json.py | JSON 结构化输出 100% 稳定方案 |
| 05_prompt_injection.py | 提示注入攻击与防护 |
| 06_overfit_regularization.py | 欠拟合/过拟合 + L1/L2/Dropout/Early Stopping/Data Aug（ML 实验 + Prompt 工程映射） |

## 学习顺序

01 -> 02 -> 03 -> 04 -> 05 -> 06

## 每个代码文件的学习要点

### 01_role_setting.py
- System Prompt 黄金五要素：角色 + 背景 + 任务 + 格式 + 约束
- 欠拟合（太简单）vs 过拟合（太复杂）的 Prompt 对比
- 长度 100-300 字，约束 3-5 条

### 02_cot_techniques.py
- 4 种 CoT 技巧：Zero-shot、Few-shot、Self-Consistency、分步求解
- CoT 让 GPT-3.5 数学题准确率从 17% 提升到 78%
- 不该用 CoT 的场景：创意写作、简单查询、闲聊

### 03_fewshot_best_practice.py
- 5 个原则：类别覆盖、数量适中（3-5）、分布一致、顺序优化、格式统一
- 相似示例放最后（近因效应）

### 04_structured_json.py
- 4 种方案：Prompt / JSON Mode / Pydantic+FC / Outlines
- 推荐方案 3：Pydantic + Function Calling

### 05_prompt_injection.py
- 5 种攻击：覆盖、角色扮演、编码、数据注入、间接注入
- 5 层防护：输入过滤 + Prompt 加固 + 数据隔离 + 输出过滤 + 多 Agent

### 06_overfit_regularization.py
- 一份代码同时演示：欠拟合、过拟合、L1、L2、Dropout、Early Stopping、Data Augmentation
- 每一种 ML 正则化都给出 Prompt 工程 1:1 对照表与 before/after
- 面试金句：L1=删废话、L2=不走极端、Dropout=示例多样化、Early Stopping=约束够了就停、Data Aug=覆盖边界示例
- 依赖：torch（未装也能跑后半段映射/Prompt 演示）

## 面试必背

1. 角色设定黄金五要素结构
2. Pydantic + Function Calling 模板
3. 5 层安全防护架构

## 拓展思考

1. Prompt 怎么自动压缩到 100 字以内？
2. 怎么自动评估 Prompt 的过拟合程度？
3. 多模态输入怎么做提示注入防护？
4. 怎么设计 Prompt 灰度发布系统？
