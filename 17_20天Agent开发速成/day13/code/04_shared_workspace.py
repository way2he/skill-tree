
# -*- coding: utf-8 -*-
"""
Day13 Code 04: 共享工作空间 - Agent 之间共享信息
"""

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("Day13 - 共享工作空间")
print("=" * 60)

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

# 共享工作空间（简单的字典实现）
shared_workspace = {
    "progress": "初始化",
    "current_task": None,
    "notes": [],
    "decisions": [],
    "questions": []
}

print("\n[1/4] 创建 Agents...")

# Agent 1: 研究员
researcher = Agent(
    role="研究员",
    goal="收集信息，记录到共享工作空间",
    backstory="你负责收集信息，会把发现记录到共享空间。",
    llm=llm,
    verbose=True
)

# Agent 2: 分析师
analyst = Agent(
    role="分析师",
    goal="分析共享空间的信息，添加洞察",
    backstory="你会读取共享空间的信息，添加你的分析。",
    llm=llm,
    verbose=True
)

# Agent 3: 报告撰写人
writer = Agent(
    role="报告撰写人",
    goal="根据共享空间的信息写报告",
    backstory="你会汇总共享空间的所有信息，写成最终报告。",
    llm=llm,
    verbose=True
)

TOPIC = "2024 年 AI Agent 发展趋势"

task_research = Task(
    description=f"""
    研究'{TOPIC}'这个主题，然后回答：
    1. 有哪些关键趋势？
    2. 有哪些重要的玩家？
    3. 有什么值得注意的事件？

    请在你的输出开头明确写：
    "【更新共享工作空间】"
    然后列出你的发现。
    """,
    agent=researcher,
    expected_output="研究发现（400字）"
)

task_analyze = Task(
    description=f"""
    基于前面的研究，请分析：
    1. 这些趋势意味着什么？
    2. 有什么机会和风险？
    3. 对未来 1-2 年的预测？

    请在你的输出开头明确写：
    "【更新共享工作空间】"
    然后列出你的分析。
    """,
    agent=analyst,
    expected_output="分析洞察（400字）",
    context=[task_research]
)

task_write = Task(
    description=f"""
    基于共享工作空间的所有信息（研究 + 分析），写一份完整的报告：
    1. 概述
    2. 关键趋势
    3. 机会与风险
    4. 未来展望
    5. 建议

    请用清晰的结构撰写。
    """,
    agent=writer,
    expected_output="最终报告（800字）",
    context=[task_research, task_analyze]
)

print("\n[2/4] 创建 Crew (开启 memory)...")
crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[task_research, task_analyze, task_write],
    process=Process.sequential,
    memory=True,  # 开启共享记忆
    verbose=True
)

print("\n[3/4] 开始运行...")
print("=" * 60)
print(f"初始共享工作空间: {json.dumps(shared_workspace, ensure_ascii=False, indent=2)}")
print("=" * 60)

result = crew.kickoff()

print("\n" + "=" * 60)
print("✅ 运行完成！")
print("=" * 60)
print(result)

