
---
name: Day13-多Agent协作下-高级模式
description: Day13完整学习资料：协调者模式、冲突解决、共享工作空间
type: learning-material
tags: ["多Agent", "协调者", "冲突解决", "CrewAI"]
summary: Day13多Agent高级模式完整学习资料
created_at: 2026-05-26
updated_at: 2026-05-26
version: interview
---

# Day13: 多 Agent 协作（下）- 高级模式 🚀

&gt; 📅 **学习日期**：2026-05-26  
&gt; ⏰ **总时长**：8 小时  
&gt; 🎯 **验收标准**：能处理 Agent 之间的协调、冲突解决、共享信息

---

## 今日学习内容清单

| 时间 | 学习内容 | 时长 | 对应文档 |
|------|---------|------|---------|
| **09:00-10:00** | 协调者模式 - Agent 之间如何对话和协调 | 1h | [协调者模式.md](./协调者模式.md) |
| **10:00-11:00** | 冲突解决 - Agent 意见不一致怎么办 | 1h | [冲突解决.md](./冲突解决.md) |
| **11:00-12:00** | 共享工作空间 - Agent 如何共享信息 | 1h | [共享工作空间.md](./共享工作空间.md) |
| **14:00-15:00** | 实战 1: 辩论团队 - 正反方 Agent 辩论 | 1h | [code/01_debate_crew.py](./code/01_debate_crew.py) |
| **15:00-16:00** | 实战 2: 评审委员会 - 多 Agent 评审决策 | 1h | [code/02_review_committee.py](./code/02_review_committee.py) |
| **16:00-17:00** | 实战 3: 头脑风暴 - 多 Agent 创意激发 | 1h | [code/03_brainstorming.py](./code/03_brainstorming.py) |
| **19:00-20:00** | 面试题专项 - Day13 6 道面试题 | 1h | [面试题.md](./面试题.md) |
| **20:00-21:00** | 复盘 + 整理面试话术 | 1h | [今日串讲.md](./今日串讲.md) |

---

## 今日验收标准

### 理论验收
- ✅ 能设计协调者 Agent，让 Agent 之间有效对话
- ✅ 知道 3 种以上解决 Agent 冲突的策略
- ✅ 能实现共享工作空间，让 Agent 共享信息

### 代码验收
- ✅ 能实现辩论团队（正反方 Agent）
- ✅ 能实现评审委员会（多 Agent 投票决策）
- ✅ 能实现头脑风暴（多 Agent 相互激发创意）

---

## 今日核心知识点

### 协调者模式
- 有一个中心协调者 Agent
- 其他 Agent 向协调者汇报
- 协调者做最终决策

### 冲突解决策略
1. **投票制**：多个 Agent 投票，少数服从多数
2. **层级制**：高级别的 Agent 做最终决定
3. **协商制**：Agent 之间对话协商，直到达成一致
4. **仲裁制**：请第三方 Agent 来仲裁

### 共享工作空间
- 共享的记忆/上下文
- 共享的工具/资源
- 共享的状态/进度

---

## 今日代码实战

### 代码文件清单
- [code/01_debate_crew.py](./code/01_debate_crew.py) - 辩论团队
- [code/02_review_committee.py](./code/02_review_committee.py) - 评审委员会
- [code/03_brainstorming.py](./code/03_brainstorming.py) - 头脑风暴
- [code/04_shared_workspace.py](./code/04_shared_workspace.py) - 共享工作空间
- [code/05_negotiation.py](./code/05_negotiation.py) - Agent 协商

---

## 今日面试考点（6 道）

### 基础题（3 道）
1. 什么是协调者模式？有什么优缺点？
2. Agent 之间产生冲突怎么办？有哪些解决策略？
3. 如何让多个 Agent 共享信息？有哪些方式？

### 进阶题（3 道）
4. 请设计一个"评审委员会"系统，多个专家 Agent 评审一个方案，最终达成一致决策。
5. 在多 Agent 系统中，如何避免"群体思维"？如何保证意见多样性？
6. Agent 之间如何进行有效的协商？请设计一个协商流程。

---

**🚀 让我们开始 Day13 的学习！**

