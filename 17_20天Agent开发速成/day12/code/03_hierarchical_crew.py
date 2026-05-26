
# -*- coding: utf-8 -*-
"""
Day12 Code 03: 分层管理团队 - 有管理者的 Crew
"""

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

print("=" * 60)
print("Day12 - 分层管理团队")
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

# Agent 1: 项目经理（管理者）
project_manager = Agent(
    role="项目经理",
    goal="协调团队，确保项目按时高质量交付",
    backstory="""
    你是一位资深项目经理，PMP认证，有10年项目管理经验，
    曾带领20人团队完成多个百万级项目，擅长协调资源、管控风险。
    你的管理风格：目标导向、结果为王，但也关心团队成员成长。
    """,
    llm=llm,
    verbose=True
)

# Agent 2: 产品设计师
product_designer = Agent(
    role="产品设计师",
    goal="设计用户友好、美观实用的产品界面和流程",
    backstory="""
    你是一位资深产品设计师，曾在字节跳动负责过多款日活百万产品的设计，
    你的设计理念："好的设计是让用户感觉不到设计的存在"。
    你擅长：用户体验设计、交互设计、视觉设计。
    """,
    llm=llm,
    verbose=True
)

# Agent 3: 后端开发
backend_developer = Agent(
    role="后端开发工程师",
    goal="开发稳定、高效、可扩展的后端服务",
    backstory="""
    你是一位资深后端工程师，有8年开发经验，
    擅长使用 Python、Go 构建高性能服务，对系统架构有深入理解。
    你的代码原则：简洁、可维护、有测试、有文档。
    """,
    llm=llm,
    verbose=True
)

# Agent 4: 测试工程师
test_engineer = Agent(
    role="测试工程师",
    goal="确保产品质量，发现并帮助修复Bug",
    backstory="""
    你是一位资深测试工程师，有7年测试经验，
    擅长功能测试、性能测试、自动化测试，能发现别人发现不了的问题。
    你的信条："没有Bug的产品是不存在的，但我们可以无限接近"。
    """,
    llm=llm,
    verbose=True
)

print(f"✅ 创建了 4 个 Agents")

# ===================== 3. 创建 Tasks =====================
print("\n[3/5] 创建 Tasks...")

# Task 1: 产品设计
task_design = Task(
    description="""
    设计一个"AI 读书笔记"App的产品方案：
    1. 核心功能：有哪些主要功能？
    2. 用户流程：用户怎么使用？
    3. 界面设计：大概的界面布局？
    4. 关键页面：首页、阅读页、笔记页
    """,
    agent=product_designer,
    expected_output="产品设计方案（600字）"
)

# Task 2: 后端开发
task_backend = Task(
    description="""
    根据产品设计，设计后端架构：
    1. 技术选型：用什么框架、数据库？
    2. API 设计：有哪些接口？
    3. 数据模型：数据库表结构？
    4. 核心逻辑：关键业务流程？
    """,
    agent=backend_developer,
    expected_output="后端架构设计（600字）",
    context=[task_design]
)

# Task 3: 测试计划
task_test = Task(
    description="""
    制定测试计划：
    1. 测试范围：要测试哪些功能？
    2. 测试用例：核心功能的测试用例？
    3. 质量标准：达到什么标准可以上线？
    4. 风险评估：可能有什么风险？如何应对？
    """,
    agent=test_engineer,
    expected_output="测试计划（500字）",
    context=[task_design, task_backend]
)

print(f"✅ 创建了 3 个 Tasks")

# ===================== 4. 创建 Crew (分层模式) =====================
print("\n[4/5] 创建 Crew (分层模式)...")

crew = Crew(
    agents=[project_manager, product_designer, backend_developer, test_engineer],
    tasks=[task_design, task_backend, task_test],
    process=Process.hierarchical,  # 分层管理模式
    manager_llm=llm,  # 管理者用的 LLM
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

