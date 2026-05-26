
# -*- coding: utf-8 -*-
"""
Day12 Code 02: 产品调研团队
"""

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

print("=" * 60)
print("Day12 - 产品调研团队")
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

# Agent 1: 市场研究员
market_researcher = Agent(
    role="市场研究员",
    goal="调研市场规模、趋势和竞争格局",
    backstory="""
    你是一位资深市场研究员，有10年咨询公司经验，
    曾服务过麦肯锡、BCG等顶级咨询公司，擅长用数据说话。
    你的专长：市场规模测算、竞争格局分析、趋势预测。
    """,
    llm=llm,
    verbose=True
)

# Agent 2: 用户研究员
user_researcher = Agent(
    role="用户研究员",
    goal="深入理解用户需求、痛点和行为",
    backstory="""
    你是一位资深用户研究员，有8年互联网公司经验，
    曾在腾讯、网易负责用户研究，擅长从用户反馈中发现真实需求。
    你的专长：用户访谈、问卷设计、需求洞察。
    """,
    llm=llm,
    verbose=True
)

# Agent 3: 竞品分析师
competitor_analyst = Agent(
    role="竞品分析师",
    goal="深入分析竞争对手的优缺点",
    backstory="""
    你是一位竞品分析专家，曾在多家头部互联网公司做战略分析，
    对竞品的功能、体验、商业模式有敏锐的洞察力。
    你的专长：功能对比、体验分析、商业模式拆解。
    """,
    llm=llm,
    verbose=True
)

# Agent 4: 报告撰写人
report_writer = Agent(
    role="报告撰写人",
    goal="整合调研结果，输出清晰可执行的调研报告",
    backstory="""
    你是一位资深商业分析师，擅长把复杂的信息整合成清晰的报告，
    你的报告总是能帮助决策者快速理解现状并做出正确决策。
    """,
    llm=llm,
    verbose=True
)

print(f"✅ 创建了 4 个 Agents")

# ===================== 3. 创建 Tasks =====================
print("\n[3/5] 创建 Tasks...")

# Task 1: 市场调研
task_market = Task(
    description="""
    对"AI 编程助手"市场进行调研：
    1. 市场规模：现在有多大？未来3年增长预期？
    2. 发展趋势：技术趋势、用户趋势、商业模式趋势？
    3. 市场格局：有哪些主要玩家？市场份额如何？

    请用数据支撑你的分析。
    """,
    agent=market_researcher,
    expected_output="市场调研报告（500字）"
)

# Task 2: 用户调研
task_user = Task(
    description="""
    分析"AI 编程助手"的目标用户：
    1. 用户画像：谁在用？年龄、职业、经验水平？
    2. 核心需求：用户最需要什么功能？
    3. 痛点：现在的产品有什么不满意的地方？
    4. 使用场景：在什么情况下用？
    """,
    agent=user_researcher,
    expected_output="用户调研报告（500字）"
)

# Task 3: 竞品分析
task_competitor = Task(
    description="""
    分析主要竞品（GitHub Copilot、Cursor、通义灵码）：
    1. 功能对比：各有什么特色功能？
    2. 体验对比：谁更好用？为什么？
    3. 商业模式：怎么收费？
    4. 优缺点：每个竞品的优势和劣势是什么？
    """,
    agent=competitor_analyst,
    expected_output="竞品分析报告（600字）"
)

# Task 4: 整合报告
task_report = Task(
    description="""
    整合前面3份报告，输出一份完整的市场进入建议：
    1. 市场机会：我们能不能进？机会有多大？
    2. 差异化定位：我们和竞品有什么不同？
    3. 核心功能：我们应该做什么功能？
    4. 实施建议：第一步做什么？

    要求：逻辑清晰，建议可执行。
    """,
    agent=report_writer,
    expected_output="完整调研报告（1000字）",
    context=[task_market, task_user, task_competitor]
)

print(f"✅ 创建了 4 个 Tasks")

# ===================== 4. 创建 Crew =====================
print("\n[4/5] 创建 Crew...")

crew = Crew(
    agents=[market_researcher, user_researcher, competitor_analyst, report_writer],
    tasks=[task_market, task_user, task_competitor, task_report],
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

