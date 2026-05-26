
---
name: CrewAI快速入门
description: CrewAI快速入门：核心概念、安装、第一个Crew实战
type: learning-material
tags: ["CrewAI", "快速入门", "多Agent"]
summary: CrewAI快速入门教程，包含核心概念、安装步骤、第一个Crew实战
created_at: 2026-05-26
updated_at: 2026-05-26
version: interview
---

# CrewAI 快速入门 🚀

&gt; 📖 **本讲学习目标**：理解 CrewAI 核心概念，能安装并运行第一个 Crew  
&gt; ⏰ **预计学习时间**：1 小时

---

## 什么是 CrewAI？

### 定义
**CrewAI** 是一个用于编排多 Agent 协作的框架，让多个 AI 智能体像团队一样协作完成复杂任务。

### 核心思想
```
多个专长 Agent 组成 Crew（团队）
  ↓
按照 Process（流程）协作
  ↓
完成 Task（任务）
```

### 为什么选择 CrewAI？

| 特性 | 说明 |
|------|------|
| **角色扮演** | Agent 可以有明确的角色、目标、背景故事 |
| **自动任务分配** | 自动根据 Agent 能力分配任务 |
| **任务依赖** | 支持任务之间的依赖关系 |
| **工具使用** | Agent 可以使用搜索、代码执行等工具 |
| **灵活流程** | 支持顺序、分层、异步等多种流程 |

---

## 核心概念速览

### 1. Agent（智能体）
**有角色、有目标、有工具的独立个体**

```python
Agent(
    role="高级文案策划",           # 角色
    goal="创作吸引人的营销文案",   # 目标
    backstory="有10年文案经验...",  # 背景故事
    tools=[search_tool, ...],       # 可用工具
    llm=llm                         # 大模型
)
```

### 2. Task（任务）
**给 Agent 的具体工作任务**

```python
Task(
    description="撰写产品介绍文案",  # 任务描述
    agent=copywriter_agent,          # 执行者
    expected_output="500字营销文案", # 期望输出
    context=[previous_task]          # 上下文（可选）
)
```

### 3. Crew（团队）
**多个 Agent 组成的协作团队**

```python
Crew(
    agents=[agent1, agent2, agent3],  # 团队成员
    tasks=[task1, task2, task3],      # 任务列表
    process=Process.sequential        # 协作流程
)
```

### 4. Process（流程）
**团队协作的方式**

| 流程 | 说明 |
|------|------|
| **sequential** | 顺序执行 |
| **hierarchical** | 分层管理（有管理者） |
| **async** | 异步并行 |

---

## 安装 CrewAI

### 基础安装
```bash
pip install crewai
```

### 完整安装（包含工具）
```bash
pip install 'crewai[tools]'
```

### 验证安装
```python
import crewai
print(f"CrewAI 版本: {crewai.__version__}")
```

---

## 第一个 Crew：Hello World！

### 完整代码示例

```python
# -*- coding: utf-8 -*-
"""
第一个 CrewAI 示例：简单的写作团队
"""

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 1. 初始化 LLM
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

# 2. 创建 Agent
# Agent 1：创意策划
planner = Agent(
    role="创意策划",
    goal="为产品创作引人入胜的创意概念",
    backstory="你是一位资深创意策划，有10年广告行业经验，擅长把普通产品变成有趣的故事。",
    llm=llm,
    verbose=True
)

# Agent 2：文案撰写
writer = Agent(
    role="文案撰写",
    goal="根据创意概念撰写吸引人的营销文案",
    backstory="你是一位金牌文案，笔下的产品总能打动人心，让读者忍不住想购买。",
    llm=llm,
    verbose=True
)

# Agent 3：编辑校对
editor = Agent(
    role="编辑校对",
    goal="润色文案，确保没有错误，并且更有感染力",
    backstory="你是一位资深编辑，对文字有极高要求，能让好文案变得更出色。",
    llm=llm,
    verbose=True
)

# 3. 创建 Task
# Task 1：创意策划
task_plan = Task(
    description="为一款智能水杯创作创意概念",
    agent=planner,
    expected_output="300字创意概念描述"
)

# Task 2：文案撰写
task_write = Task(
    description="根据创意概念撰写营销文案",
    agent=writer,
    expected_output="500字营销文案",
    context=[task_plan]  # 依赖前一个任务的输出
)

# Task 3：编辑校对
task_edit = Task(
    description="润色营销文案，提升感染力",
    agent=editor,
    expected_output="最终版营销文案",
    context=[task_write]
)

# 4. 创建 Crew
crew = Crew(
    agents=[planner, writer, editor],
    tasks=[task_plan, task_write, task_edit],
    process=Process.sequential,  # 顺序执行
    verbose=True
)

# 5. 运行 Crew
print("=" * 60)
print("🚀 开始运行第一个 Crew！")
print("=" * 60)

result = crew.kickoff()

print("\n" + "=" * 60)
print("✅ 运行完成！最终输出：")
print("=" * 60)
print(result)
```

### 运行步骤

1. **创建 .env 文件**
```
OPENAI_API_KEY=your-api-key-here
```

2. **安装依赖**
```bash
pip install crewai python-dotenv langchain-openai
```

3. **运行代码**
```bash
python first_crew.py
```

---

## CrewAI 核心 API 速查

### Agent 参数详解

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| **role** | str | ✅ | Agent 的角色 |
| **goal** | str | ✅ | Agent 的目标 |
| **backstory** | str | ✅ | Agent 的背景故事 |
| **tools** | List[Tool] | ❌ | Agent 可用的工具 |
| **llm** | LLM | ❌ | 使用的大模型 |
| **verbose** | bool | ❌ | 是否输出详细日志 |
| **allow_delegation** | bool | ❌ | 是否允许委托任务 |

### Task 参数详解

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| **description** | str | ✅ | 任务描述 |
| **agent** | Agent | ✅ | 执行任务的 Agent |
| **expected_output** | str | ✅ | 期望的输出格式 |
| **context** | List[Task] | ❌ | 依赖的前置任务 |
| **tools** | List[Tool] | ❌ | 此任务专用工具 |
| **async_execution** | bool | ❌ | 是否异步执行 |

### Crew 参数详解

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| **agents** | List[Agent] | ✅ | 团队成员 |
| **tasks** | List[Task] | ✅ | 任务列表 |
| **process** | Process | ❌ | 协作流程（默认 sequential） |
| **verbose** | bool | ❌ | 是否输出详细日志 |
| **memory** | bool | ❌ | 是否启用记忆 |
| **cache** | bool | ❌ | 是否启用缓存 |

---

## 常见问题 FAQ

### Q1: CrewAI 和 AutoGen 有什么区别？

| 维度 | CrewAI | AutoGen |
|------|--------|---------|
| **设计理念** | 角色扮演 + 任务驱动 | 多 Agent 对话 |
| **易用性** | 更简单，API 更清晰 | 更灵活，复杂度高 |
| **工具生态** | 内置常用工具 | 需要自己集成 |
| **适用场景** | 有明确流程的任务 | 开放式对话协作 |

### Q2: 如何选择合适的 LLM？

| 场景 | 推荐模型 |
|------|---------|
| **开发测试** | GPT-3.5-turbo |
| **生产环境** | GPT-4o / Claude 3 Opus |
| **成本敏感** | 国产模型（通义千问、文心一言） |

---

## 本讲小结 ✅

### CrewAI 核心概念
1. **Agent**：有角色、有目标的智能体
2. **Task**：给 Agent 的具体任务
3. **Crew**：Agent 组成的团队
4. **Process**：协作流程

### 关键步骤
1. 初始化 LLM
2. 创建 Agent
3. 创建 Task
4. 组装 Crew
5. kickoff 运行

### 下讲预告
下一讲：Agent 角色定义实战（如何设计一个好的 Agent）

---
