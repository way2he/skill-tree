
# -*- coding: utf-8 -*-
"""
Day12 Code 01: 简单的写作团队 - 三 Agent 协作
"""

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

print("=" * 60)
print("Day12 - 简单写作团队")
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

# Agent 1: 创意策划
planner = Agent(
    role="创意策划",
    goal="为产品创作引人入胜的创意概念和故事线",
    backstory="""
    你是一位资深创意策划，有10年4A广告公司经验，
    曾服务过耐克、可口可乐等知名品牌，擅长把普通产品变成有故事的IP。
    你相信："好的创意不是凭空想出来的，而是从产品本质中生长出来的"
    """,
    llm=llm,
    verbose=True
)

# Agent 2: 文案撰写
writer = Agent(
    role="金牌文案",
    goal="根据创意概念撰写打动人心的营销文案",
    backstory="""
    你是一位金牌文案，笔下的产品总能让读者心动，
    多篇文案成为行业经典案例，全网传播量过亿。
    你的写作风格：开头有钩子，中间有故事，结尾有金句。
    """,
    llm=llm,
    verbose=True
)

# Agent 3: 编辑校对
editor = Agent(
    role="资深编辑",
    goal="润色文案，提升感染力，确保零错误",
    backstory="""
    你是一位资深编辑，对文字有极高的要求，
    能让好文案变得更出色，让普通文案变得优秀。
    你特别擅长：标题优化、节奏调整、金句打磨。
    """,
    llm=llm,
    verbose=True
)

print(f"✅ 创建了 {len([planner, writer, editor])} 个 Agents")

# ===================== 3. 创建 Tasks =====================
print("\n[3/5] 创建 Tasks...")

# Task 1: 创意策划
task_plan = Task(
    description="""
    为一款"智能保温杯"创作创意概念：
    1. 产品定位：给什么样的人用？
    2. 核心卖点：最打动人的3个点是什么？
    3. 故事线：如何讲一个温暖的故事？
    4. Slogan：一句让人记住的话

    产品特点：
    - 24小时恒温
    - APP可以提醒喝水
    - 显示水温，不会烫嘴
    - 材质安全，婴儿级
    """,
    agent=planner,
    expected_output="一份完整的创意策划文档（300字）"
)

# Task 2: 文案撰写
task_write = Task(
    description="""
    根据创意策划撰写一篇营销文案，要求：
    1. 开头有吸引力（让人想继续读）
    2. 中间有故事（用场景打动人）
    3. 结尾有行动召唤（让人想买）
    4. 500字左右
    """,
    agent=writer,
    expected_output="500字营销文案",
    context=[task_plan]
)

# Task 3: 编辑校对
task_edit = Task(
    description="""
    润色营销文案，提升感染力：
    1. 优化标题，更吸引人
    2. 调整节奏，更流畅
    3. 打磨金句，更 memorable
    4. 检查错别字和语法
    """,
    agent=editor,
    expected_output="最终版营销文案",
    context=[task_write]
)

print(f"✅ 创建了 {len([task_plan, task_write, task_edit])} 个 Tasks")

# ===================== 4. 创建 Crew =====================
print("\n[4/5] 创建 Crew...")

crew = Crew(
    agents=[planner, writer, editor],
    tasks=[task_plan, task_write, task_edit],
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

