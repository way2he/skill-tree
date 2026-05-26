
# -*- coding: utf-8 -*-
"""
Day13 Code 01: 辩论团队 - 正反方 Agent 辩论
"""

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("Day13 - 辩论团队")
print("=" * 60)

# 1. 初始化 LLM
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.8,
    api_key=os.getenv("OPENAI_API_KEY")
)

# 2. 创建 Agents
print("\n[1/4] 创建辩论 Agents...")

# 正方 Agent
affirmative = Agent(
    role="正方辩手",
    goal="全力论证'AI 会让更多人失业'这个观点",
    backstory="""
    你是一位资深辩手，擅长用数据和案例支持你的观点，
    你坚信 AI 的发展会导致大规模失业，这是不可避免的趋势。
    """,
    llm=llm,
    verbose=True
)

# 反方 Agent
negative = Agent(
    role="反方辩手",
    goal="全力论证'AI 不会让更多人失业，反而会创造更多就业'这个观点",
    backstory="""
    你是一位资深辩手，擅长从历史和发展的角度看问题，
    你坚信技术进步最终会创造更多就业，这是历史的规律。
    """,
    llm=llm,
    verbose=True
)

# 评委 Agent
judge = Agent(
    role="评委",
    goal="根据正反方的辩论，做出公正的评判",
    backstory="""
    你是一位公正的评委，善于倾听双方的论点，
    基于逻辑和证据做出评判，不偏不倚。
    """,
    llm=llm,
    verbose=True
)

# 3. 创建 Tasks
print("\n[2/4] 创建辩论 Tasks...")

task_affirmative = Task(
    description="""
    作为正方，陈述你的观点：
    1. 你的核心论点是什么？
    2. 有什么数据和案例支持？
    3. 如何反驳反方可能的质疑？
    """,
    agent=affirmative,
    expected_output="正方论点陈述（300字）"
)

task_negative = Task(
    description="""
    作为反方，先听了正方的观点，然后陈述你的反驳：
    1. 你如何反驳正方的论点？
    2. 你的核心论点是什么？
    3. 有什么数据和案例支持？
    """,
    agent=negative,
    expected_output="反方反驳和论点（300字）",
    context=[task_affirmative]
)

task_judge = Task(
    description="""
    听了正反方的辩论，请做出评判：
    1. 双方的论点各是什么？
    2. 谁的论证更有说服力？为什么？
    3. 最终的获胜方是？
    """,
    agent=judge,
    expected_output="评判结果（300字）",
    context=[task_affirmative, task_negative]
)

# 4. 创建并运行 Crew
print("\n[3/4] 创建 Crew...")
crew = Crew(
    agents=[affirmative, negative, judge],
    tasks=[task_affirmative, task_negative, task_judge],
    process=Process.sequential,
    verbose=True
)

print("\n[4/4] 开始辩论...")
print("=" * 60)

result = crew.kickoff()

print("\n" + "=" * 60)
print("✅ 辩论结束！")
print("=" * 60)
print(result)

