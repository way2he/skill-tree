
---
name: Day12-多Agent协作上-基础模式
description: Day12完整学习资料：多Agent架构模式、CrewAI、角色定义、任务分配
type: learning-material
tags: ["多Agent", "CrewAI", "协作", "架构模式"]
summary: 多Agent基础篇完整学习资料，包含架构模式、CrewAI使用、角色定义、任务分配及配套代码
created_at: 2026-05-26
updated_at: 2026-05-26
version: interview
---

# Day12：多 Agent 协作（上）- 基础模式 🤝

&gt; 📅 **学习日期**：2026-05-26  
&gt; ⏰ **总时长**：8 小时  
&gt; 🎯 **验收标准**：能使用 CrewAI 搭建一个多 Agent 协作系统，能定义清晰的角色和任务

---

## 📋 本日学习内容清单

| 时间 | 学习内容 | 时长 | 对应文档 |
|------|---------|------|---------|
| **09:00-10:00** | 多 Agent 协作架构模式：顺序、并行、层次、混合 | 1h | [多Agent架构模式详解.md](./多Agent架构模式详解.md) |
| **10:00-11:00** | CrewAI 入门：核心概念、安装、第一个 Crew | 1h | [CrewAI快速入门.md](./CrewAI快速入门.md) |
| **11:00-12:00** | Agent 角色定义：角色设定、目标、背景故事、工具 | 1h | [Agent角色定义实战.md](./Agent角色定义实战.md) |
| **14:00-15:00** | 任务分配与编排：Task 定义、依赖关系、输出格式 | 1h | [任务分配与编排.md](./任务分配与编排.md) |
| **15:00-16:00** | 代码实战 1：简单的三 Agent 写作团队 | 1h | [code/01_simple_writing_crew.py](./code/01_simple_writing_crew.py) |
| **16:00-17:00** | 代码实战 2：产品调研 + 竞品分析 | 1h | [code/02_research_crew.py](./code/02_research_crew.py) |
| **19:00-20:00** | 【面试题专项】Day12 6 道多 Agent 面试题 | 1h | [面试题.md](./面试题.md) + [面试题_标准答案.md](./面试题_标准答案.md) |
| **20:00-21:00** | 复盘 + 整理面试话术 | 1h | [今日串讲.md](./今日串讲.md) |

---

## 🎯 本日验收标准

### 理论验收（面试必答）
- ✅ 能说出 4 种以上多 Agent 架构模式
- ✅ 能解释 CrewAI 的核心概念（Agent/Task/Crew/Process）
- ✅ 能设计合理的 Agent 角色和目标
- ✅ 能定义任务之间的依赖关系

### 代码验收（手写代码）
- ✅ 能使用 CrewAI 创建 3 个以上 Agent
- ✅ 能定义带依赖关系的 Task 序列
- ✅ 能跑通一个完整的多 Agent 协作流程

---

## 📚 本日核心知识点

### 多 Agent 架构模式 🏗️
```
顺序模式 → 并行模式 → 层次模式 → 混合模式
```

### CrewAI 核心概念速查
| 概念 | 一句话说明 |
|------|-----------|
| **Agent** | 有角色、有目标、有工具的智能体 |
| **Task** | 给 Agent 的具体任务，有输入输出 |
| **Crew** | Agent 组成的团队 |
| **Process** | 团队协作的流程（顺序/分层/异步） |
| **Tool** | Agent 可以使用的工具（搜索/代码等） |

---

## 💻 本日代码实战

### 代码文件清单
- [code/01_simple_writing_crew.py](./code/01_simple_writing_crew.py) - 简单写作团队
- [code/02_research_crew.py](./code/02_research_crew.py) - 产品调研团队
- [code/03_hierarchical_crew.py](./code/03_hierarchical_crew.py) - 分层管理团队
- [code/04_agent_with_tools.py](./code/04_agent_with_tools.py) - 带工具的 Agent
- [code/05_custom_output.py](./code/05_custom_output.py) - 自定义输出格式

### 快速启动
```bash
# 安装依赖
pip install crewai 'crewai[tools]' python-dotenv

# 运行简单写作团队
python code/01_simple_writing_crew.py
```

---

## 📌 本日面试考点（6 道题）

### 基础题（3 道）
1. 多 Agent 协作有哪些常见架构模式？各自优缺点是什么？
2. CrewAI 的核心组件是什么？各自的作用是什么？
3. 如何设计一个好的 Agent 角色？需要考虑哪些要素？

### 进阶题（3 道）
4. 单 Agent 和多 Agent 怎么选？各自适用什么场景？
5. 如何处理 Agent 之间的任务依赖关系？有哪些编排策略？
6. 多 Agent 协作中如何避免重复工作？如何确保信息一致性？

&gt; 💡 **答案详见**：[面试题_标准答案.md](./面试题_标准答案.md)

---

## 🔗 相关资料链接

- 官方文档
  - 📖 [CrewAI 官方文档](https://docs.crewai.com/)
  - 📖 [CrewAI GitHub](https://github.com/joaomdmoura/crewAI)

- 相关论文
  - 📄 AutoGen: Enabling Next-Gen LLM Applications
  - 📄 AgentBench: Evaluating LLMs as Agents
  - 📄 CAMEL: Communicative Agents for "Mind" Exploration

---

## 📝 今日学习计划（建议）

### 上午（3小时）
1. **09:00-10:00**：理解多 Agent 架构模式，画示意图
2. **10:00-11:00**：CrewAI 入门，跑通第一个例子
3. **11:00-12:00**：学习如何定义 Agent 角色

### 下午（3小时）
1. **14:00-15:00**：学习任务分配与编排
2. **15:00-16:00**：代码实战 1：写作团队
3. **16:00-17:00**：代码实战 2：调研团队

### 晚上（2小时）
1. **19:00-20:00**：做 6 道面试题，对照标准答案
2. **20:00-21:00**：复盘整理，准备 Day13

---

**🚀 让我们开始 Day12 的学习吧！先从多 Agent 架构模式开始！**

---
