#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day02 必写代码 2：思维链 CoT (Chain of Thought)
功能：演示 4 种 CoT 技巧，让大模型从「直觉输出」变成「理性思考」

面试考点：
- CoT 为什么有效？
- Zero-shot CoT 和 Few-shot CoT 的区别？
- 什么场景用 CoT，什么场景不用？
- CoT 的副作用是什么？
"""

import sys
from pathlib import Path

# 将项目根目录加入 sys.path，确保能导入 llm 库
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from llm.core import get_llm


# ============================================================
# 技巧 1：Zero-shot CoT —— 加一句"让我一步步思考"
# ============================================================
def cot_zero_shot(question: str) -> str:
    """
    Zero-shot CoT：最简单，加一句魔法话术

    Args:
        question: 用户提出的问题

    Returns:
        str: 模型生成的思考过程和答案
    """
    prompt = f"""{question}

请你一步步思考，先列出已知条件，再分析未知量，最后给出答案。"""
    try:
        llm = get_llm()
        return llm.generate(prompt=prompt, temperature=0.3)
    except Exception as e:
        return f"调用 LLM 失败: {e}"


# ============================================================
# 技巧 2：Few-shot CoT —— 给思考过程示例
# ============================================================
def cot_few_shot(question: str) -> str:
    """
    Few-shot CoT：给几个完整的思考示例

    Args:
        question: 用户提出的问题

    Returns:
        str: 模型按示例格式生成的思考过程和答案
    """
    prompt = f"""
示例 1：
问题：小明有 5 个苹果，吃了 2 个，又买了 3 个，他现在有几个？
思考：
  - 初始数量：5 个
  - 吃了 2 个：5 - 2 = 3 个
  - 买了 3 个：3 + 3 = 6 个
答案：6 个

示例 2：
问题：一辆车每小时跑 60 公里，3 小时跑多远？
思考：
  - 速度：60 公里/小时
  - 时间：3 小时
  - 距离 = 速度 × 时间 = 60 × 3 = 180 公里
答案：180 公里

现在请按同样的格式解答：
问题：{question}
"""
    try:
        llm = get_llm()
        return llm.generate(prompt=prompt, temperature=0.3)
    except Exception as e:
        return f"调用 LLM 失败: {e}"


# ============================================================
# 技巧 3：Self-Consistency —— 多次采样取多数
# ============================================================
def cot_self_consistency(question: str, n: int = 5) -> dict:
    """
    Self-Consistency：让模型回答 n 次，取出现次数最多的答案

    Args:
        question: 用户提出的问题
        n: 采样次数，默认 5 次

    Returns:
        dict: 包含 all_answers / final_answer / vote_count / confidence
    """
    from collections import Counter

    llm = get_llm()
    answers = []

    for i in range(n):
        try:
            prompt = f"{question}\n\n一步步思考，给出最终答案。"
            text = llm.generate(prompt=prompt, temperature=0.9)
            # 取最后一行作为答案
            answers.append(text.split("\n")[-1].strip())
        except Exception as e:
            answers.append(f"[第{i+1}次调用失败: {e}]")

    # 取出现次数最多的答案
    most_common = Counter(answers).most_common(1)[0]
    return {
        "all_answers": answers,
        "final_answer": most_common[0],
        "vote_count": most_common[1],
        "confidence": most_common[1] / n,
    }


# ============================================================
# 技巧 4：分步求解 —— 拆解复杂任务
# ============================================================
DECOMPOSITION_SYSTEM = """
你是一个复杂任务分解专家。

请把用户的复杂问题拆解成 3-5 个子问题，然后依次解答每个子问题，
最后综合得出最终答案。

输出格式：
【任务分解】
子问题 1：...
子问题 2：...
...

【依次解答】
子问题 1 的答案：...
子问题 2 的答案：...
...

【综合答案】
...
"""


def cot_decomposition(question: str) -> str:
    """
    分步求解：复杂任务先拆解再综合

    Args:
        question: 用户提出的复杂问题

    Returns:
        str: 模型生成的任务分解和综合答案
    """
    try:
        llm = get_llm()
        return llm.generate(
            prompt=question,
            system=DECOMPOSITION_SYSTEM,
            temperature=0.3,
        )
    except Exception as e:
        return f"调用 LLM 失败: {e}"


# ============================================================
# 反面教材：不该用 CoT 的场景
# ============================================================
def when_not_to_use_cot() -> None:
    """什么场景不该用 CoT"""
    print("\n❌ 不该用 CoT 的场景：")
    print("  1. 简单的事实查询（如：今天星期几）→ 多此一举")
    print("  2. 创意写作（如：写一首诗）→ CoT 会限制创造力")
    print("  3. 闲聊对话 → 反而显得机器人")
    print("  4. 翻译、摘要 → 不需要推理")
    print("  5. 已经训练过的简单任务 → 浪费 Token")


# ⭐ 面试官追问：CoT 为什么有效？
"""
3 分钟回答模板：

CoT 有效的核心原因有 3 个：

1. 分解复杂问题：大模型本质是 token 级别的 next-token-prediction，
   一步算到底容易出错。CoT 把问题拆成多个小步骤，每一步都简单很多。

2. 利用 in-context learning：大模型见过大量「推理过程→答案」的训练数据，
   提示它「一步步思考」激活了这部分能力。

3. 自我验证机制：思考过程暴露后，模型能在生成中自我检查，
   类似人脑「写下来反而想得更清楚」。

实测效果（GPT-3.5 解数学题）：
- 不加 CoT：准确率 17%
- Zero-shot CoT（"Let's think step by step"）：准确率 78%

代价：
- Token 消耗增加 3-5 倍
- 响应时间增加 2-3 倍
- 不适合所有任务（创意、简单事实查询不该用）
"""


if __name__ == "__main__":
    question = "一个班 30 个学生，其中 60% 是女生，男生比女生少几个？"

    print("=" * 60)
    print(f"问题：{question}")
    print("=" * 60)

    print("\n🎯 技巧 1：Zero-shot CoT")
    print(cot_zero_shot(question))

    # print("\n🎯 技巧 2：Few-shot CoT")
    # print(cot_few_shot(question))

    # print("\n🎯 技巧 3：Self-Consistency（多次采样取多数）")
    # result = cot_self_consistency(question, n=5)
    # print(f"最终答案：{result['final_answer']}")
    # print(f"置信度：{result['confidence']:.0%}")

    # print("\n🎯 技巧 4：分步求解（复杂任务）")
    # complex_q = "如果地球人口每年增长 1.1%，现在 80 亿，多少年后会达到 100 亿？"
    # print(cot_decomposition(complex_q))

    when_not_to_use_cot()
