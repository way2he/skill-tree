
# -*- coding: utf-8 -*-
"""
Day12 Code 05: 自定义输出格式
"""

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import os
import json
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

print("=" * 60)
print("Day12 - 自定义输出格式")
print("=" * 60)

# ===================== 1. 初始化 LLM =====================
print("\n[1/5] 初始化 LLM...")
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

# ===================== 2. 创建 Agents =====================
print("\n[2/5] 创建 Agents...")

# Agent 1: 产品策划
planner = Agent(
    role="产品策划",
    goal="规划产品功能和特性",
    backstory="你是一位资深产品策划，擅长把想法转化为清晰的产品规划。",
    llm=llm,
    verbose=True
)

# Agent 2: 功能分析师
analyst = Agent(
    role="功能分析师",
    goal="细化每个功能的需求",
    backstory="你是一位严谨的功能分析师，擅长把产品规划拆分成详细的需求。",
    llm=llm,
    verbose=True
)

print(f"✅ 创建了 2 个 Agents")

# ===================== 3. 创建 Tasks (指定输出格式) =====================
print("\n[3/5] 创建 Tasks...")

# Task 1: 产品规划 (JSON 输出)
task_plan = Task(
    description="""
    规划一个"AI 英语学习"App的核心功能：
    1. 产品定位
    2. 目标用户
    3. 核心功能列表（5-7个）
    """,
    agent=planner,
    expected_output="""
    请输出严格的 JSON 格式，不要有其他文字：
    {
        "product_name": "产品名称",
        "positioning": "产品定位",
        "target_users": ["用户1", "用户2"],
        "core_features": [
            {
                "name": "功能名称",
                "description": "功能描述",
                "priority": "高/中/低"
            }
        ]
    }
    """
)

# Task 2: 功能细化 (Markdown 表格输出)
task_detail = Task(
    description="""
    对每个功能进行细化：
    1. 用户故事
    2. 验收标准
    3. 优先级
    """,
    agent=analyst,
    expected_output="""
    请用 Markdown 表格输出：

    | 功能名称 | 用户故事 | 验收标准 | 优先级 |
    |---------|---------|---------|--------|
    | 功能1 | ... | ... | ... |
    | 功能2 | ... | ... | ... |

    然后在表格下面写一段 200 字的总结。
    """,
    context=[task_plan]
)

print(f"✅ 创建了 2 个 Tasks")

# ===================== 4. 创建 Crew =====================
print("\n[4/5] 创建 Crew...")

crew = Crew(
    agents=[planner, analyst],
    tasks=[task_plan, task_detail],
    process=Process.sequential,
    verbose=True
)

print("✅ Crew 组装完成！")

# ===================== 5. 运行 Crew =====================
print("\n[5/5] 开始运行 Crew...")
print("=" * 60)

result = crew.kickoff()

print("\n" + "=" * 60)
print("✅ 运行完成！最终输出：")
print("=" * 60)
print(result)

# 尝试解析 JSON (如果第一个任务的输出是 JSON)
print("\n" + "=" * 60)
print("💡 提示：第一个任务的输出应该是 JSON 格式")
print("=" * 60)

