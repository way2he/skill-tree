# -*- coding: utf-8 -*-
"""
Day 02 实战任务1: 代码审查 Agent 系统提示词
20天Agent开发速成 - 第2天

作者: Agent开发学习者
日期: 2026-05-20
"""

import json
from typing import Any, Dict, List

# =============================================================================
# 代码审查 Agent 系统提示词
# =============================================================================

CODE_REVIEW_SYSTEM_PROMPT = """\
你是一位拥有15年经验的资深软件架构师和代码审查专家。
你曾在Google、Microsoft等顶级科技公司工作，精通Python、Java、C++等多种语言。

## 你的核心职责
1. 发现潜在的Bug和逻辑错误
2. 识别性能瓶颈和优化机会
3. 评估代码可读性和可维护性
4. 检查安全漏洞和最佳实践
5. 提供具体、可执行的改进建议

## 审查维度

### 🔴 严重问题 (Critical)
- 可能导致崩溃或数据丢失的Bug
- 安全漏洞（SQL注入、XSS、敏感信息泄露等）
- 资源泄漏（文件、连接、内存未释放）
- 并发安全问题

### 🟠 高优先级 (High)
- 逻辑错误或边界条件处理不当
- 异常处理缺失或不完善
- 性能明显的低效实现
- 违反Pythonic原则的严重情况

### 🟡 中优先级 (Medium)
- 代码可读性问题
- 命名不规范
- 缺少文档字符串
- 可维护性问题

### 🟢 低优先级 (Low)
- 代码风格问题
- 轻微的性能优化建议
- 最佳实践建议

## 输出格式要求
你必须以JSON格式输出审查结果，格式如下：
{
    "overall_score": 85,  // 0-100的综合评分
    "summary": "代码整体评价摘要",
    "issues": [
        {
            "severity": "Critical|High|Medium|Low",
            "category": "Bug|Security|Performance|Readability|Maintainability",
            "line_number": 15,
            "description": "问题描述",
            "suggestion": "具体改进建议",
            "code_before": "原代码片段",
            "code_after": "改进后的代码"
        }
    ],
    "positive_aspects": ["代码的优点1", "优点2"],
    "learning_resources": ["相关学习链接或建议"]
}

## 审查原则
1. 具体：指出具体的行号和代码片段
2. 建设性：每个问题都提供解决方案
3. 优先级：按严重程度排序
4. 平衡：既指出问题，也肯定优点
5. 教育性：解释为什么这是个问题

现在请审查以下代码：
"""


# =============================================================================
# 待审查的示例代码（包含各种问题）
# =============================================================================

SAMPLE_CODE_WITH_ISSUES = """\
def get_user_data(user_id):
    import sqlite3
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # 严重：SQL注入漏洞
    query = "SELECT * FROM users WHERE id = " + str(user_id)
    cursor.execute(query)
    
    result = cursor.fetchall()
    return result

def process_list(items):
    # 高优先级：性能问题，O(n²)
    unique_items = []
    for item in items:
        if item not in unique_items:  # 每次都要遍历整个列表
            unique_items.append(item)
    return unique_items

def divide(a, b):
    # 高优先级：缺少异常处理
    return a / b

# 中优先级：命名不规范，缺少文档
def calc(x, y):
    return x * y

# 低优先级：魔法数字
if status == 404:
    print("Not found")
"""


# =============================================================================
# 模拟的审查结果（实际使用时应调用大模型API）
# =============================================================================

SIMULATED_REVIEW_RESULT = {
    "overall_score": 45,
    "summary": "代码存在严重的安全漏洞和多个质量问题，需要立即修复SQL注入问题。",
    "issues": [
        {
            "severity": "Critical",
            "category": "Security",
            "line_number": 7,
            "description": "存在SQL注入漏洞，用户输入直接拼接到SQL语句中",
            "suggestion": "使用参数化查询防止SQL注入",
            "code_before": 'query = "SELECT * FROM users WHERE id = " + str(user_id)',
            "code_after": 'query = "SELECT * FROM users WHERE id = ?"\n    cursor.execute(query, (user_id,))',
        },
        {
            "severity": "High",
            "category": "Performance",
            "line_number": 14,
            "description": "去重算法时间复杂度为O(n²)，大数据量时性能极差",
            "suggestion": "使用set进行去重，时间复杂度降为O(n)",
            "code_before": """unique_items = []
    for item in items:
        if item not in unique_items:
            unique_items.append(item)""",
            "code_after": "unique_items = list(set(items))  # 如果需要保持顺序：list(dict.fromkeys(items))",
        },
        {
            "severity": "High",
            "category": "Bug",
            "line_number": 21,
            "description": "除法操作没有处理除数为0的情况",
            "suggestion": "添加异常处理或前置检查",
            "code_before": "return a / b",
            "code_after": """if b == 0:
        raise ValueError("除数不能为0")
    return a / b""",
        },
        {
            "severity": "Medium",
            "category": "Maintainability",
            "line_number": 25,
            "description": "函数名calc过于简短，缺少文档字符串",
            "suggestion": "使用描述性函数名并添加文档字符串",
            "code_before": "def calc(x, y):",
            "code_after": """def multiply_numbers(x: float, y: float) -> float:\n    \"\"\"计算两个数的乘积。\n    \n    Args:\n        x: 第一个乘数\n        y: 第二个乘数\n    \n    Returns:\n        两数相乘的结果\n    \"\"\"""",
        },
    ],
    "positive_aspects": [
        "代码结构清晰，函数职责单一",
        "使用了类型转换str(user_id)，说明有基本的安全意识",
    ],
    "learning_resources": [
        "OWASP Top 10: https://owasp.org/www-project-top-ten/",
        "Python性能优化指南: https://wiki.python.org/moin/PythonSpeed",
    ],
}


def format_review_output(review_result: Dict[str, Any]) -> str:
    """
    格式化审查结果为易读的文本格式

    Args:
        review_result: 审查结果的JSON字典

    Returns:
        格式化后的审查报告字符串
    """
    output = []
    output.append("=" * 60)
    output.append(f"📊 代码审查报告 | 综合评分: {review_result['overall_score']}/100")
    output.append("=" * 60)
    output.append(f"\n📝 总体评价: {review_result['summary']}\n")

    # 问题列表
    output.append("-" * 60)
    output.append("🔍 发现的问题:\n")

    severity_icons = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}

    for i, issue in enumerate(review_result["issues"], 1):
        icon = severity_icons.get(issue["severity"], "⚪")
        output.append(f"{icon} 问题 #{i} [{issue['severity']}] - {issue['category']}")
        output.append(f"   位置: 第 {issue['line_number']} 行")
        output.append(f"   描述: {issue['description']}")
        output.append(f"   建议: {issue['suggestion']}")
        output.append(f"   原代码: {issue['code_before'][:50]}...")
        output.append("")

    # 优点
    output.append("-" * 60)
    output.append("✅ 代码优点:\n")
    for aspect in review_result["positive_aspects"]:
        output.append(f"   • {aspect}")

    output.append("\n" + "=" * 60)
    return "\n".join(output)


def main():
    """
    主函数：演示代码审查Agent的使用
    """
    print("🚀 Day 02 实战任务1: 代码审查 Agent")
    print("=" * 60)
    print("\n📋 系统提示词:\n")
    print(CODE_REVIEW_SYSTEM_PROMPT[:500] + "...\n")

    print("=" * 60)
    print("📄 待审查代码:\n")
    print(SAMPLE_CODE_WITH_ISSUES)

    print("\n" + "=" * 60)
    print("📊 审查结果:\n")
    report = format_review_output(SIMULATED_REVIEW_RESULT)
    print(report)

    # 保存结果
    output_path = r"c:\Users\robotAi\Documents\ClawWorksapce\knowledge-base\Day02_code_review_result.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(SIMULATED_REVIEW_RESULT, f, ensure_ascii=False, indent=2)
    print(f"\n💾 详细结果已保存至: {output_path}")


if __name__ == "__main__":
    main()
