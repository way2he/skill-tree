
# -*- coding: utf-8 -*-
"""
Day13 Code 03: 头脑风暴 - 多 Agent 创意激发
"""

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("Day13 - 头脑风暴")
print("=" * 60)

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=1.0,  # 高温度，更有创意
    api_key=os.getenv("OPENAI_API_KEY")
)

print("\n[1/4] 创建创意 Agents...")

# Agent 1: 梦想家（天马行空）
dreamer = Agent(
    role="梦想家",
    goal="提出大胆、有想象力的创意",
    backstory="""
    你是一位梦想家，思维不受限制，总能提出让人眼前一亮的想法，
    你相信"如果不显得荒谬，那可能就不是好想法"。
    """,
    llm=llm,
    verbose=True
)

# Agent 2: 现实派（可行性）
realist = Agent(
    role="现实派",
    goal="评估创意的可行性，提出落地建议",
    backstory="""
    你是一位现实派，擅长把天马行空的想法变成可落地的方案，
    你相信"好想法 + 好执行 = 成功"。
    """,
    llm=llm,
    verbose=True
)

# Agent 3: 批评家（找问题）
critic = Agent(
    role="批评家",
    goal="找出创意中的问题和风险",
    backstory="""
    你是一位批评家，善于发现潜在问题，让想法变得更完善，
    你相信"找到问题不是打击，而是让想法更好的机会"。
    """,
    llm=llm,
    verbose=True
)

# Agent 4: 整合者（汇总）
integrator = Agent(
    role="整合者",
    goal="汇总各方意见，形成最终方案",
    backstory="""
    你是一位整合者，善于把不同的想法融合在一起，形成更好的方案，
    你相信"三个臭皮匠，顶个诸葛亮"。
    """,
    llm=llm,
    verbose=True
)

TOPIC = "AI 时代的新型教育产品"

print(f"\n[2/4] 头脑风暴主题: {TOPIC}")

task_dream = Task(
    description=f"""
    针对主题'{TOPIC}'，提出 5 个大胆、有想象力的创意：
    1. 不要怕不切实际
    2. 越有创意越好
    3. 每个创意用 1-2 句话描述
    """,
    agent=dreamer,
    expected_output="5 个创意想法（300字）"
)

task_realize = Task(
    description=f"""
    看了梦想家的创意，从可行性角度分析：
    1. 哪些创意是可行的？
    2. 哪些需要调整？怎么调整？
    3. 你的建议是？
    """,
    agent=realist,
    expected_output="可行性分析（300字）",
    context=[task_dream]
)

task_criticize = Task(
    description=f"""
    看了前面的想法，从批评角度分析：
    1. 潜在问题和风险是什么？
    2. 可能会遇到什么挑战？
    3. 如何规避这些问题？
    """,
    agent=critic,
    expected_output="问题分析（300字）",
    context=[task_dream, task_realize]
)

task_integrate = Task(
    description=f"""
    汇总各方意见，形成最终方案：
    1. 整合后的核心创意是什么？
    2. 分阶段实施计划是什么？
    3. 风险和应对措施是什么？
    """,
    agent=integrator,
    expected_output="最终方案（500字）",
    context=[task_dream, task_realize, task_criticize]
)

print("\n[3/4] 创建 Crew...")
crew = Crew(
    agents=[dreamer, realist, critic, integrator],
    tasks=[task_dream, task_realize, task_criticize, task_integrate],
    process=Process.sequential,
    verbose=True
)

print("\n[4/4] 开始头脑风暴...")
print("=" * 60)

result = crew.kickoff()

print("\n" + "=" * 60)
print("✅ 头脑风暴完成！")
print("=" * 60)
print(result)

