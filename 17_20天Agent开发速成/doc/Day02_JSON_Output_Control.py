# -*- coding: utf-8 -*-
"""
Day 02 实战任务2: 让大模型100%输出指定格式JSON
20天Agent开发速成 - 第2天

核心技巧：
1. 明确的角色设定
2. 详细的格式规范
3. Few-shot示例
4. 严格的约束条件
5. 输出验证机制
"""

import json
import re
from typing import Any, Dict, List

# =============================================================================
# 技巧1: 基础JSON输出提示词
# =============================================================================

BASIC_JSON_PROMPT = """\
你是一个JSON格式专家。你的任务是将用户输入转换为指定的JSON格式。

## 输出格式要求
你必须严格按照以下JSON Schema输出，不要添加任何其他内容：

{
    "name": "字符串，用户姓名",
    "age": "整数，用户年龄",
    "skills": ["技能1", "技能2", ...],
    "experience_years": "整数，工作年限"
}

## 重要约束
1. 只输出JSON，不要任何解释文字
2. 不要添加markdown代码块标记（```json）
3. 确保JSON格式合法，可以被json.loads()解析
4. 如果信息缺失，使用null而不是省略字段

## 示例
输入：张三，28岁，会Python和Java，工作5年
输出：{"name": "张三", "age": 28, "skills": ["Python", "Java"], "experience_years": 5}

现在请处理以下输入：
"""


# =============================================================================
# 技巧2: 高级JSON输出提示词（多层嵌套）
# =============================================================================

ADVANCED_JSON_PROMPT = """\
你是一位专业的数据结构化专家。请将以下信息转换为严格的JSON格式。

## 输出Schema定义
```json
{
    "project": {
        "name": "项目名称，字符串",
        "type": "项目类型，枚举值：web|mobile|desktop|api",
        "status": "项目状态，枚举值：planning|development|testing|production"
    },
    "team": {
        "lead": "负责人姓名",
        "members": [
            {
                "name": "成员姓名",
                "role": "角色，如：frontend|backend|devops|qa",
                "level": "级别，枚举值：junior|mid|senior|lead"
            }
        ],
        "size": "团队总人数，整数"
    },
    "timeline": {
        "start_date": "开始日期，格式YYYY-MM-DD",
        "end_date": "结束日期，格式YYYY-MM-DD",
        "milestones": [
            {
                "name": "里程碑名称",
                "date": "日期，格式YYYY-MM-DD",
                "deliverables": ["交付物1", "交付物2"]
            }
        ]
    },
    "metadata": {
        "created_at": "创建时间ISO格式",
        "version": "数据版本，如1.0.0"
    }
}
```

## 格式约束（必须遵守）
1. ✅ 所有字符串使用双引号
2. ✅ 日期格式严格为 YYYY-MM-DD
3. ✅ 枚举值必须来自指定选项
4. ✅ 数组不能为空（至少一个元素）
5. ✅ 数字类型不加引号
6. ❌ 禁止添加注释
7. ❌ 禁止尾随逗号
8. ❌ 禁止单引号

## Few-shot示例

示例1：
输入：电商网站项目，负责人李雷，团队成员：前端小王 junior，后端小张 mid，预计6个月完成
输出：
{
    "project": {
        "name": "电商网站",
        "type": "web",
        "status": "planning"
    },
    "team": {
        "lead": "李雷",
        "members": [
            {"name": "小王", "role": "frontend", "level": "junior"},
            {"name": "小张", "role": "backend", "level": "mid"}
        ],
        "size": 3
    },
    "timeline": {
        "start_date": "2024-01-01",
        "end_date": "2024-06-30",
        "milestones": [
            {
                "name": "项目启动",
                "date": "2024-01-01",
                "deliverables": ["需求文档", "技术方案"]
            }
        ]
    },
    "metadata": {
        "created_at": "2024-01-01T00:00:00Z",
        "version": "1.0.0"
    }
}

现在请处理：
"""


# =============================================================================
# 技巧3: 强制JSON输出的终极提示词
# =============================================================================

ULTIMATE_JSON_PROMPT = """\
[SYSTEM_INSTRUCTION]
你是JSON生成器。你的唯一任务是输出合法JSON。
任何非JSON内容都是严重错误。

[OUTPUT_SCHEMA]
{
    "task_analysis": {
        "intent": "用户意图，一句话描述",
        "complexity": "复杂度，枚举：low|medium|high",
        "domain": "领域，如：技术/商务/生活"
    },
    "action_plan": {
        "steps": [
            {
                "step_number": "步骤序号，整数",
                "action": "具体行动",
                "estimated_time": "预估时间，分钟",
                "dependencies": ["依赖的步骤序号"]
            }
        ],
        "total_time": "总预估时间，分钟",
        "risk_level": "风险等级，枚举：low|medium|high"
    },
    "resources": {
        "tools": ["需要的工具1", "工具2"],
        "knowledge": ["需要的知识点1", "知识点2"],
        "references": ["参考资料链接或名称"]
    },
    "success_criteria": ["成功标准1", "标准2"]
}

[CONSTRAINTS]
1. 输出必须是合法JSON
2. 字段不能缺失
3. 类型必须匹配schema
4. 枚举值必须来自指定选项
5. 数组至少包含1个元素

[VALIDATION_RULES]
- 检查所有引号是否配对
- 检查括号是否平衡
- 检查逗号位置是否正确
- 检查没有尾随逗号

[EXAMPLE]
输入：我想学习Python机器学习，计划3个月掌握基础
输出：
{"task_analysis":{"intent":"学习Python机器学习基础","complexity":"medium","domain":"技术"},"action_plan":{"steps":[{"step_number":1,"action":"学习Python基础语法","estimated_time":120,"dependencies":[]},{"step_number":2,"action":"学习NumPy和Pandas","estimated_time":180,"dependencies":[1]},{"step_number":3,"action":"学习Scikit-learn基础","estimated_time":240,"dependencies":[2]}],"total_time":540,"risk_level":"low"},"resources":{"tools":["Python 3.9+","Jupyter Notebook","VS Code"],"knowledge":["Python基础","线性代数","统计学基础"],"references":["Scikit-learn官方文档","Hands-On Machine Learning"]},"success_criteria":["能独立完成数据预处理","能使用sklearn构建基础模型","理解模型评估指标"]}

[OUTPUT]
直接输出JSON，不要任何其他文字：
"""


# =============================================================================
# JSON输出验证和修复工具
# =============================================================================


class JSONValidator:
    """
    JSON输出验证器，确保大模型输出符合要求
    """

    @staticmethod
    def extract_json(text: str) -> str:
        """
        从文本中提取JSON内容

        Args:
            text: 可能包含markdown代码块或其他内容的文本

        Returns:
            纯净的JSON字符串
        """
        # 尝试匹配markdown代码块
        patterns = [
            r"```json\s*(.*?)\s*```",  # ```json ... ```
            r"```\s*(.*?)\s*```",  # ``` ... ```
            r"\{.*\}",  # 直接匹配JSON对象
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            if matches:
                return matches[0].strip()

        return text.strip()

    @staticmethod
    def validate_json(json_str: str) -> tuple[bool, Any]:
        """
        验证JSON是否合法

        Args:
            json_str: JSON字符串

        Returns:
            (是否合法, 解析后的数据或错误信息)
        """
        try:
            data = json.loads(json_str)
            return True, data
        except json.JSONDecodeError as e:
            return False, str(e)

    @staticmethod
    def fix_common_issues(json_str: str) -> str:
        """
        修复常见的JSON格式问题

        Args:
            json_str: 可能有问题的JSON字符串

        Returns:
            修复后的JSON字符串
        """
        fixes = [
            # 移除BOM标记
            (r"^\ufeff", ""),
            # 将单引号替换为双引号（但要小心嵌套情况）
            (r"(?<!\\)'", '"'),
            # 移除尾随逗号
            (r",(\s*[}\]])", r"\1"),
            # 移除注释
            (r"//.*?\n", "\n"),
            (r"/\*.*?\*/", "", re.DOTALL),
        ]

        result = json_str
        for pattern, replacement, *flags in fixes:
            flag = flags[0] if flags else 0
            result = re.sub(pattern, replacement, result, flags=flag)

        return result.strip()


def demonstrate_json_techniques():
    """
    演示各种JSON输出控制技巧
    """
    print("🎯 Day 02 实战任务2: JSON输出控制技巧")
    print("=" * 70)

    # 技巧1：基础提示词
    print("\n📌 技巧1: 基础JSON输出提示词")
    print("-" * 70)
    print(BASIC_JSON_PROMPT[:500] + "...\n")

    # 技巧2：高级提示词
    print("\n📌 技巧2: 高级嵌套JSON输出提示词")
    print("-" * 70)
    print(ADVANCED_JSON_PROMPT[:600] + "...\n")

    # 技巧3：终极提示词
    print("\n📌 技巧3: 强制JSON输出终极提示词")
    print("-" * 70)
    print(ULTIMATE_JSON_PROMPT[:700] + "...\n")

    # 演示验证工具
    print("\n🔧 JSON验证工具演示")
    print("=" * 70)

    # 示例1：干净的JSON
    clean_json = '{"name": "张三", "age": 28}'
    print(f"\n✅ 测试干净JSON: {clean_json}")
    is_valid, result = JSONValidator.validate_json(clean_json)
    print(f"   验证结果: {'通过' if is_valid else '失败'}")

    # 示例2：带markdown的JSON
    markdown_json = '```json\n{"name": "李四", "age": 30}\n```'
    print(f"\n📄 测试带markdown的JSON")
    extracted = JSONValidator.extract_json(markdown_json)
    print(f"   提取后: {extracted}")
    is_valid, result = JSONValidator.validate_json(extracted)
    print(f"   验证结果: {'通过' if is_valid else '失败'}")

    # 示例3：有问题的JSON
    broken_json = "{'name': '王五', 'age': 25,}"
    print(f"\n❌ 测试有问题的JSON: {broken_json}")
    is_valid, error = JSONValidator.validate_json(broken_json)
    print(f"   原始验证: 失败 - {error}")

    fixed = JSONValidator.fix_common_issues(broken_json)
    print(f"   修复后: {fixed}")
    is_valid, result = JSONValidator.validate_json(fixed)
    print(f"   修复后验证: {'通过' if is_valid else '失败'}")

    # 生成完整提示词文件
    print("\n\n💾 生成完整提示词文件...")
    return {
        "basic_prompt": BASIC_JSON_PROMPT,
        "advanced_prompt": ADVANCED_JSON_PROMPT,
        "ultimate_prompt": ULTIMATE_JSON_PROMPT,
        "tips": [
            "明确的角色设定让模型知道应该输出什么格式",
            "详细的schema定义减少歧义",
            "Few-shot示例展示期望的输出",
            "严格的约束条件强制执行",
            "输出验证机制作为最后保障",
        ],
    }


def main():
    """
    主函数
    """
    result = demonstrate_json_techniques()

    # 保存提示词到文件
    output_path = r"c:\Users\robotAi\Documents\ClawWorksapce\knowledge-base\Day02_json_prompts.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 完整提示词已保存至: {output_path}")
    print("\n🎉 实战任务2完成！")
    print("\n核心要点:")
    for i, tip in enumerate(result["tips"], 1):
        print(f"  {i}. {tip}")


if __name__ == "__main__":
    main()
