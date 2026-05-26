
# -*- coding: utf-8 -*-
"""
Day13 Code 02: 评审委员会 - 多 Agent 投票决策
"""

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("Day13 - 评审委员会")
print("=" * 60)

# 1. 初始化 LLM
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

# 2. 创建评审专家 Agents
print("\n[1/4] 创建评审专家...")

# 专家 1: 技术专家
tech_expert = Agent(
    role="技术专家",
    goal="从技术角度评估方案的可行性",
    backstory="""
    你是一位资深技术专家，有20年开发经验，
    擅长评估技术方案的可行性、风险、技术 debt。
    """,
    llm=llm,
    verbose=True
)

# 专家 2: 产品专家
product_expert = Agent(
    role="产品专家",
    goal="从产品角度评估方案的用户价值",
    backstory="""
    你是一位资深产品专家，有15年产品经验，
    擅长评估产品方案的用户价值、市场前景、竞争力。
    """,
    llm=llm,
    verbose=True
)

# 专家 3: 商业专家
business_expert = Agent(
    role="商业专家",
    goal="从商业角度评估方案的 ROI",
    backstory="""
    你是一位资深商业专家，有18年投资经验，
    擅长评估商业方案的 ROI、盈利模式、市场规模。
    """,
    llm=llm,
    verbose=True
)

# 专家 4: 设计专家
design_expert = Agent(
    role="设计专家",
    goal="从设计角度评估方案的用户体验",
    backstory="""
    你是一位资深设计专家，有12年设计经验，
    擅长评估产品的用户体验、视觉设计、交互设计。
    """,
    llm=llm,
    verbose=True
)

# 主席：最终决策
chairperson = Agent(
    role="评审主席",
    goal="汇总专家意见，做出最终决策",
    backstory="""
    你是一位经验丰富的评审主席，善于综合各方意见，
    做出明智的决策，平衡技术、产品、商业、设计各方面。
    """,
    llm=llm,
    verbose=True
)

# 待评审的方案
PROPOSAL = """
方案：AI 驱动的智能客服系统
- 功能：自动回答用户问题，智能路由，数据分析
- 技术：用大语言模型 + 向量知识库
- 预期效果：降低 50% 人工客服成本，提升用户满意度
- 投入：3 个开发，3 个月，50 万预算
"""

# 3. 创建评审 Tasks
print("\n[2/4] 创建评审 Tasks...")

task_tech = Task(
    description=f"""
    从技术角度评审这个方案：
    {PROPOSAL}

    请回答：
    1. 技术上可行吗？有什么风险？
    2. 技术选型合理吗？有更好的方案吗？
    3. 3 个月能完成吗？
    4. 你的建议是？（通过 / 有条件通过 / 不通过）
    """,
    agent=tech_expert,
    expected_output="技术评审意见（300字）"
)

task_product = Task(
    description=f"""
    从产品角度评审这个方案：
    {PROPOSAL}

    请回答：
    1. 用户价值是什么？足够大吗？
    2. 市场前景如何？有竞争力吗？
    3. 你的建议是？（通过 / 有条件通过 / 不通过）
    """,
    agent=product_expert,
    expected_output="产品评审意见（300字）"
)

task_business = Task(
    description=f"""
    从商业角度评审这个方案：
    {PROPOSAL}

    请回答：
    1. ROI 如何？值得投入吗？
    2. 盈利模式清晰吗？
    3. 你的建议是？（通过 / 有条件通过 / 不通过）
    """,
    agent=business_expert,
    expected_output="商业评审意见（300字）"
)

task_design = Task(
    description=f"""
    从设计角度评审这个方案：
    {PROPOSAL}

    请回答：
    1. 用户体验会好吗？
    2. 设计上有什么风险或挑战？
    3. 你的建议是？（通过 / 有条件通过 / 不通过）
    """,
    agent=design_expert,
    expected_output="设计评审意见（300字）"
)

task_decision = Task(
    description="""
    汇总各位专家的评审意见，做出最终决策：
    1. 各位专家的意见各是什么？
    2. 有什么共识和分歧？
    3. 最终建议是？（通过 / 有条件通过 / 不通过）
    4. 如果通过，需要注意什么？如果不通过，原因是什么？
    """,
    agent=chairperson,
    expected_output="最终决策（400字）",
    context=[task_tech, task_product, task_business, task_design]
)

# 4. 创建并运行 Crew
print("\n[3/4] 创建 Crew...")
crew = Crew(
    agents=[tech_expert, product_expert, business_expert, design_expert, chairperson],
    tasks=[task_tech, task_product, task_business, task_design, task_decision],
    process=Process.sequential,
    verbose=True
)

print("\n[4/4] 开始评审...")
print("=" * 60)

result = crew.kickoff()

print("\n" + "=" * 60)
print("✅ 评审完成！")
print("=" * 60)
print(result)

