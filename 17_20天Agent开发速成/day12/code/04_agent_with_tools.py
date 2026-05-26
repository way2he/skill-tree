
# -*- coding: utf-8 -*-
"""
Day12 Code 04: 带工具的 Agent
"""

from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

print("=" * 60)
print("Day12 - 带工具的 Agent")
print("=" * 60)

# ===================== 1. 初始化 LLM 和工具 =====================
print("\n[1/5] 初始化 LLM 和工具...")
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

# 初始化工具
search_tool = SerperDevTool()  # 需要 SERPER_API_KEY
scrape_tool = ScrapeWebsiteTool()

print("✅ LLM 和工具初始化完成")

# ===================== 2. 创建 Agents =====================
print("\n[2/5] 创建 Agents...")

# Agent 1: 市场调研员（带搜索工具）
researcher = Agent(
    role="市场调研员",
    goal="搜索最新市场信息，分析趋势",
    backstory="""
    你是一位资深市场调研员，擅长通过网络搜索获取最新信息，
    你总能找到别人找不到的数据和趋势。
    """,
    tools=[search_tool, scrape_tool],  # 给工具
    llm=llm,
    verbose=True
)

# Agent 2: 分析师
analyst = Agent(
    role="数据分析师",
    goal="分析调研数据，输出洞察",
    backstory="""
    你是一位资深数据分析师，擅长从数据中发现洞察，
    你的分析总是逻辑清晰、有数据支撑。
    """,
    llm=llm,
    verbose=True
)

# Agent 3: 报告撰写人
writer = Agent(
    role="报告撰写人",
    goal="把分析结果写成清晰的报告",
    backstory="""
    你是一位专业的报告撰写人，擅长把复杂信息整合成清晰的报告。
    """,
    llm=llm,
    verbose=True
)

print(f"✅ 创建了 3 个 Agents")

# ===================== 3. 创建 Tasks =====================
print("\n[3/5] 创建 Tasks...")

# Task 1: 市场调研（会用到搜索工具）
task_research = Task(
    description="""
    搜索"大模型应用开发平台"市场的最新信息：
    1. 2024年最新的市场规模和增长率
    2. 主要玩家有哪些？各自的市场份额？
    3. 最新的技术趋势和产品方向
    4. 用户最关注的功能点

    请使用搜索工具获取真实的最新信息。
    """,
    agent=researcher,
    expected_output="市场调研报告（600字）"
)

# Task 2: 数据分析
task_analyze = Task(
    description="""
    分析调研结果，回答：
    1. 这个市场值不值得进入？
    2. 如果进入，机会点在哪里？
    3. 差异化策略是什么？
    4. 风险是什么？如何规避？
    """,
    agent=analyst,
    expected_output="分析报告（500字）",
    context=[task_research]
)

# Task 3: 撰写报告
task_write = Task(
    description="""
    整合调研和分析结果，写一份商业计划书摘要：
    1. 市场机会
    2. 我们的解决方案
    3. 商业模式
    4. 实施计划
    """,
    agent=writer,
    expected_output="商业计划书摘要（800字）",
    context=[task_research, task_analyze]
)

print(f"✅ 创建了 3 个 Tasks")

# ===================== 4. 创建 Crew =====================
print("\n[4/5] 创建 Crew...")

crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[task_research, task_analyze, task_write],
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
print("\n" + "=" * 60)

