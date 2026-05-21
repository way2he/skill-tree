#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day02 必写代码 1：角色设定方法论
功能：好的 System Prompt vs 坏的 System Prompt 对比

面试考点：
- 为什么要给大模型设定角色？
- 一个好的系统提示词应该包含哪些部分？
- 角色设定能让输出质量提升多少？
"""

import sys
sys.path.append("..")
from llm.openai import chat_completion, get_response_content


# ============================================================
# ❌ 坏的 Prompt：欠拟合（太简单）
# ============================================================
BAD_PROMPT = "你是个助手，帮我看代码。"


# ============================================================
# ❌ 坏的 Prompt：过拟合（太严格）
# ============================================================
OVERFIT_PROMPT = """
你是全世界最好的代码审查专家，拥有30年经验，
获得过图灵奖，在Google工作过20年，
你必须严格按照JSON格式输出，一个字都不能错，
标点符号都不能错，错了就完蛋了！
你必须列出100个bug，不能少一个！
"""


# ============================================================
# ✅ 好的 Prompt：黄金五要素
# ============================================================
GOOD_PROMPT = """
# 角色定位
你是一个拥有10年经验的高级 Python 代码审查专家。

# 背景描述
你擅长发现代码中的 bug、性能问题、安全隐患和不规范的写法。
你审查过 1000+ 真实生产项目。

# 任务要求
审查用户提供的 Python 代码，给出具体的改进建议。

# 输出格式
{
  "bug_count": 发现的bug数量,
  "bugs": [
    {
      "line": 行号,
      "severity": "高/中/低",
      "problem": "问题描述",
      "suggestion": "改进建议"
    }
  ],
  "overall_score": 0-100,
  "summary": "一句话总结"
}

# 约束条件
1. 只审查 Python 代码，其他语言返回不支持
2. 严重 bug 优先级最高
3. 建议要具体可执行，不要泛泛而谈
"""


# ============================================================
# 测试代码
# ============================================================
TEST_CODE = """
def get_user(user_id):
    sql = "SELECT * FROM users WHERE id = " + user_id  # SQL 注入！
    result = db.execute(sql)
    return result.fetchone()
"""


def review_code(system_prompt: str, code: str) -> str:
    """用指定的 system prompt 审查代码"""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"请审查这段代码：\n{code}"}
    ]
    response = chat_completion(model="gpt-3.5-turbo", messages=messages, temperature=0.3)
    return get_response_content(response)


def compare_prompts():
    """对比三种 Prompt 的效果"""
    print("=" * 60)
    print("📝 同一段代码，三种 Prompt 的对比")
    print("=" * 60)
    
    print("\n❌ 坏的 Prompt（欠拟合）：")
    print(f"  {BAD_PROMPT}\n")
    # result1 = review_code(BAD_PROMPT, TEST_CODE)
    # print(f"  输出（预期：很发散，没有结构）：\n{result1}\n")
    
    print("\n❌ 过拟合的 Prompt：")
    print(f"  {OVERFIT_PROMPT[:100]}...\n")
    # result2 = review_code(OVERFIT_PROMPT, TEST_CODE)
    # print(f"  输出（预期：可能编造bug凑数）：\n{result2}\n")
    
    print("\n✅ 好的 Prompt（黄金五要素）：")
    print(f"  长度：{len(GOOD_PROMPT)} 字符")
    # result3 = review_code(GOOD_PROMPT, TEST_CODE)
    # print(f"  输出（预期：结构化、准确、可执行）：\n{result3}\n")


# ⭐ 面试官追问：为什么要给大模型设定角色？
"""
3 分钟回答模板：

设定角色有 4 个关键作用：

1. 激活领域知识：大模型在训练时学过海量不同领域的内容，设定「高级安全工程师」
   能激活模型对应的安全领域参数，输出更专业的结果。

2. 设定语境，减少幻觉：明确角色让模型在专业框架内思考，比让模型自由发挥
   错误率降低 30-50%。

3. 控制输出风格：「资深架构师」的回答会更系统化，「初学者老师」的回答会更通俗。

4. 隐式提升质量：实测显示，加角色设定后输出质量评分平均提升 20-30%。

但要注意：
- 角色不要叠太多（"全世界最好的、拿过图灵奖的..."）= 过拟合
- 角色要和任务匹配（让前端工程师审 SQL 就不合适）
- 角色 + 任务 + 输出格式 + 约束，缺一不可
"""


# 🎯 黄金公式总结
GOLDEN_FORMULA = """
好的 System Prompt 黄金五要素：

# 角色定位（你是谁）
# 背景描述（你的经验和专长）
# 任务要求（你要做什么）
# 输出格式（怎么输出）
# 约束条件（边界和规则）

长度建议：100-300 字
约束条件：3-5 条最佳
示例数量：3-5 个最佳（如果用 Few-shot）
"""


if __name__ == "__main__":
    compare_prompts()
    print("\n" + "=" * 60)
    print(GOLDEN_FORMULA)
    print("=" * 60)
