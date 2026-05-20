# -*- coding: utf-8 -*-
"""
Day02 - Prompt 工程：JSON 结构化输出 + 校验 + 重试
学习版：不需要任何外部依赖，直接运行看效果
Python 3.12+ 兼容
"""
import json
import re
import time
from typing import Optional

from pydantic import BaseModel, Field, ValidationError


# ==================== 1. Pydantic 数据模型 ====================
class CodeReview(BaseModel):
    """代码审查结果模型"""
    review_result: str = Field(
        ...,
        pattern=r"^(approve|reject)$",
        description="审查结果：approve 或 reject"
    )
    confidence: float = Field(..., ge=0.0, le=1.0, description="置信度，0-1之间")
    comments: str = Field(..., min_length=5, description="审查意见")
    suggestions: list[str] = Field(..., description="改进建议列表")


# ==================== 2. 系统提示词模板 ====================
SYSTEM_PROMPT_TEMPLATE = """你是一个代码审查专家。审查代码，以 JSON 格式输出结果，不输出其他任何内容。

【输出要求 - 必须严格遵守】
1. 只输出纯 JSON 字符串，不要输出任何其他内容
2. 不要输出 markdown 代码块标记（```json 或 ```）
3. 不要输出解释、说明、前缀、后缀
4. 必须严格符合以下 JSON Schema：

{schema}

【输出示例】
{example}

只输出 JSON，不要解释。"""


def generate_system_prompt() -> str:
    """生成完整的系统提示词"""
    example = CodeReview(
        review_result="approve",
        confidence=0.95,
        comments="代码质量良好，逻辑清晰，风格规范",
        suggestions=["可以添加更多单元测试", "建议添加类型注解"],
    ).model_dump()

    schema = json.dumps(CodeReview.model_json_schema(), indent=2, ensure_ascii=False)

    return SYSTEM_PROMPT_TEMPLATE.format(
        schema=schema,
        example=json.dumps(example, ensure_ascii=False)
    )


# ==================== 3. JSON 清理与校验函数 ====================
def clean_and_validate_json(output: str) -> Optional[CodeReview]:
    """
    清理模型输出的垃圾内容，然后用 Pydantic 校验
    处理各种常见的格式问题：
    - 包裹了 ```json ... ```
    - 前面有废话后面才是 JSON
    - 后面有解释说明
    """
    try:
        output = output.strip()

        # 处理 markdown 代码块包裹
        if output.startswith("```json"):
            output = output[7:]
        if output.startswith("```"):
            output = output[3:]
        if output.endswith("```"):
            output = output[:-3]

        # 处理："以下是JSON结果：{...}" 这种情况
        # 找到第一个 { 和最后一个 }，只取中间的内容
        if "{" in output and "}" in output:
            start = output.find("{")
            end = output.rfind("}") + 1
            output = output[start:end]

        output = output.strip()

        # Pydantic 强校验
        return CodeReview.model_validate_json(output)

    except ValidationError as e:
        print(f"❌ 校验失败: {e}")
        return None
    except Exception as e:
        print(f"❌ 解析异常: {e}")
        return None


# ==================== 4. 模拟大模型输出（学习用） ====================
def mock_llm_output(quality: str = "good") -> str:
    """
    模拟大模型的不同质量的输出，用于测试
    quality: good / with_markdown / with_prefix / wrong_format
    """
    if quality == "good":
        # ✅ 完全正确的格式
        return json.dumps({
            "review_result": "reject",
            "confidence": 0.85,
            "comments": "代码存在潜在的空指针问题，错误处理不完善",
            "suggestions": ["添加 None 检查", "完善异常处理", "增加边界条件测试"]
        }, ensure_ascii=False)

    elif quality == "with_markdown":
        # ❌ 加了 markdown 代码块（大模型经常犯这个错）
        return """```json
{
  "review_result": "approve",
  "confidence": 0.9,
  "comments": "代码质量不错",
  "suggestions": ["优化性能"]
}
```"""

    elif quality == "with_prefix":
        # ❌ 前面加了废话
        return """好的，我来审查一下这段代码。
这是我的审查结果：

{"review_result": "reject", "confidence": 0.7, "comments": "有bug", "suggestions": ["修复bug"]}

希望对你有帮助！"""

    elif quality == "wrong_format":
        # ❌ 格式错误，字段不对
        return """{"result": "approve", "score": 90, "message": "很好"}"""

    else:
        return ""


# ==================== 5. 自动重试机制 ====================
def generate_json_with_retry(max_retries: int = 3, base_delay: float = 1.0) -> Optional[CodeReview]:
    """
    带重试的 JSON 生成函数
    生产环境中这里是真正调用大模型 API
    学习环境中我们用不同质量的模拟输出测试
    """
    test_qualities = ["wrong_format", "with_prefix", "good"]  # 模拟第一次错，第二次错，第三次对

    for attempt in range(max_retries):
        print(f"\n🔄 第 {attempt + 1} 次尝试...")

        # 模拟：每次调用可能返回不同质量的结果
        quality = test_qualities[min(attempt, len(test_qualities) - 1)]
        raw_output = mock_llm_output(quality)

        print(f"📤 模型原始输出（{quality}）：")
        print(raw_output[:200] + "..." if len(raw_output) > 200 else raw_output)
        print()

        result = clean_and_validate_json(raw_output)
        if result:
            print(f"✅ 第 {attempt + 1} 次尝试成功！")
            return result

        print(f"⚠️  第 {attempt + 1} 次校验失败")

        if attempt < max_retries - 1:
            delay = base_delay * (2 ** attempt)  # 指数退避
            print(f"⏳ {delay} 秒后重试...")
            time.sleep(delay)

    print(f"\n❌ {max_retries} 次全部失败")
    return None


# ==================== 6. 演示程序 ====================
def demo_different_scenarios():
    """演示各种场景的校验效果"""
    print("=" * 80)
    print("演示：各种输出格式的校验效果")
    print("=" * 80)

    scenarios = [
        ("✅ 完全正确的格式", "good"),
        ("❌ 加了 markdown 代码块", "with_markdown"),
        ("❌ 前面有废话说明", "with_prefix"),
        ("❌ 字段名错误", "wrong_format"),
    ]

    for name, quality in scenarios:
        print(f"\n{name}")
        print("-" * 50)
        raw = mock_llm_output(quality)
        print("原始输出：")
        print(raw)
        print()
        result = clean_and_validate_json(raw)
        if result:
            print("✅ 校验通过！")
            print(f"   review_result: {result.review_result}")
            print(f"   confidence: {result.confidence}")
        else:
            print("❌ 校验失败")
        print()


def demo_retry_mechanism():
    """演示重试机制的效果"""
    print("=" * 80)
    print("演示：自动重试机制（模拟前两次失败，第三次成功）")
    print("=" * 80)

    result = generate_json_with_retry(max_retries=3)
    if result:
        print("\n" + "=" * 80)
        print("🎉 最终成功拿到校验通过的结果！")
        print("=" * 80)
        print(f"review_result: {result.review_result}")
        print(f"confidence: {result.confidence}")
        print(f"comments: {result.comments}")
        print(f"suggestions: {result.suggestions}")


def print_summary():
    """总结要点"""
    print("\n" + "=" * 80)
    print("📝 JSON 稳定输出三要素总结")
    print("=" * 80)
    print()
    print("1. 📝 提示词控制")
    print("   - 明确说：只输出 JSON，不要输出任何其他内容")
    print("   - 给完整的 JSON Schema")
    print("   - 给正确的示例输出")
    print()
    print("2. ✅ Pydantic 校验")
    print("   - 字段类型、范围、正则表达式的强校验")
    print("   - 格式不对立刻就知道，不会把错误数据传给下游")
    print()
    print("3. 🔄 自动重试")
    print("   - 校验失败自动重试 2-3 次")
    print("   - 指数退避，不要猛打 API")
    print("   - 99% 的情况 3 次以内就能成功")
    print()
    print("=" * 80)
    print("💡 经验：只要做到这三点，JSON 输出成功率可以到 99.9%")
    print("=" * 80)


if __name__ == "__main__":
    print("\n" + "🚀 " * 20)
    print("Day02 - JSON 结构化输出 + 校验 + 重试 练习")
    print("🚀 " * 20 + "\n")

    # 演示1：各种场景的校验效果
    demo_different_scenarios()

    input("\n按回车键继续看自动重试机制演示...\n")

    # 演示2：自动重试机制
    demo_retry_mechanism()

    # 总结
    print_summary()

    print("\n✅ JSON 结构化输出学习完成！")
    print("   现在你知道怎么让大模型 100% 稳定输出 JSON 了吧 🎯")
