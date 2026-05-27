#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day02 必写代码 4：JSON 结构化输出 100% 稳定方案
功能：5 种方案保证大模型 100% 输出可解析的 JSON

面试考点：
- 怎么保证大模型 100% 输出 JSON？
- response_format 和 Pydantic 哪个好？
- JSON 解析失败怎么办？
- 5 种方案的优缺点对比？
"""

import json
import sys
from pathlib import Path

# 将项目根目录加入 sys.path，确保能导入 llm 库
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pydantic import BaseModel, Field
from llm.core import get_llm


# ============================================================
# 公共数据模型
# ============================================================
class Person(BaseModel):
    """人物信息模型"""
    name: str = Field(description="姓名")
    age: int = Field(description="年龄", ge=0, le=150)
    occupation: str = Field(description="职业")
    skills: list[str] = Field(default=[], description="技能列表")


# ============================================================
# 方案 1：Prompt 约束 + 后处理（最基础，不推荐）
# ============================================================
def get_json_v1_prompt_only(query: str) -> dict:
    """
    方案 1：只靠 Prompt 约束输出 JSON

    Args:
        query: 包含人物信息的自然语言文本

    Returns:
        dict: 解析后的 JSON 字典，失败时返回 error 字段
    """
    prompt = f"""请提取下面文本中的人物信息，输出 JSON 格式：
{{"name": "姓名", "age": 年龄, "occupation": "职业"}}

只输出 JSON，不要任何其他文字！

文本：{query}"""
    try:
        llm = get_llm()
        text = llm.generate(prompt=prompt, temperature=0.0)

        # 需要手动清洗（容易失败）
        text = text.strip().replace("```json", "").replace("```", "")
        return json.loads(text)
    except json.JSONDecodeError:
        return {"error": "解析失败", "raw": text}
    except Exception as e:
        return {"error": f"调用 LLM 失败: {e}"}


# ============================================================
# 方案 2：System Prompt 强化 + 后处理（通用方案）
# ============================================================
def get_json_v2_system_prompt(query: str) -> dict:
    """
    方案 2：用 System Prompt 强化 JSON 输出约束

    Args:
        query: 包含人物信息的自然语言文本

    Returns:
        dict: 解析后的 JSON 字典，失败时返回 error 字段
    """
    try:
        llm = get_llm()
        text = llm.generate(
            prompt=f"提取人物信息（JSON）：{query}",
            system="你必须返回有效的 JSON，不要输出任何其他文字。",
            temperature=0.0,
        )
        return json.loads(text.strip())
    except json.JSONDecodeError:
        return {"error": "JSON 解析失败", "raw": text}
    except Exception as e:
        return {"error": f"调用 LLM 失败: {e}"}


# ============================================================
# 方案 3：Pydantic + generate_json（推荐 ⭐）
# ============================================================
def get_json_v3_pydantic(query: str) -> Person:
    """
    方案 3：Pydantic 定义 schema + generate_json 严格输出

    利用 llm 库的 generate_json() 方法，传入 Pydantic 模型的
    JSON Schema，让模型按 schema 输出，再用 Pydantic 自动校验。

    Args:
        query: 包含人物信息的自然语言文本

    Returns:
        Person: 校验通过的人物信息对象
    """
    # Pydantic 模型自动转 JSON Schema
    schema = Person.model_json_schema()

    prompt = f"""请从以下文本中提取人物信息：
{query}

要求：严格按照提供的 JSON Schema 输出。"""

    try:
        llm = get_llm()
        # 使用 llm 库的 generate_json，传入 schema 约束输出格式
        json_str = llm.generate_json(prompt=prompt, schema=schema, temperature=0.0)
        return Person.model_validate_json(json_str)  # Pydantic 自动校验
    except Exception as e:
        # 校验失败时返回默认值
        return Person(name="unknown", age=0, occupation="unknown", skills=[])


# ============================================================
# 方案 4：Outlines / Guidance（受限解码，100% 保证）
# ============================================================
"""
方案 4：使用 Outlines 库

pip install outlines

from outlines import models, generate

model = models.openai("gpt-3.5-turbo")
generator = generate.json(model, Person)
result = generator("提取信息：...")  # 100% 输出符合 Person schema

优点：
- 底层强制约束输出，100% 保证 schema 正确
- 不需要重试

缺点：
- 部分模型/API 不支持
- 比 Function Calling 慢
"""


# ============================================================
# 方案 5：llm 库 generate_json + 重试 + Pydantic 校验（生产级 ⭐⭐）
# ============================================================
def get_json_v5_production(query: str, max_retries: int = 3) -> Person:
    """
    方案 5：生产级方案 —— generate_json + 指数退避重试 + Pydantic 校验 + 默认值兜底

    结合 llm 库的 generate_json()、重试机制和 Pydantic 强校验，
    形成三层防护：Prompt 约束 → Schema 约束 → 类型校验。

    Args:
        query: 包含人物信息的自然语言文本
        max_retries: 最大重试次数，默认 3 次

    Returns:
        Person: 校验通过的人物信息对象，失败时返回默认值
    """
    import time

    schema = Person.model_json_schema()
    prompt = f"""请从以下文本中提取人物信息：
{query}

要求：严格按照提供的 JSON Schema 输出，字段类型和约束必须匹配。"""

    llm = get_llm()

    for attempt in range(max_retries):
        try:
            # 指数退避：第 1 次立即重试，之后等待 1s, 2s, 4s ...
            if attempt > 0:
                wait_time = 2 ** (attempt - 1)
                time.sleep(wait_time)

            json_str = llm.generate_json(
                prompt=prompt,
                schema=schema,
                temperature=0.0,
            )
            # Pydantic 强校验：字段类型、范围、必填项
            return Person.model_validate_json(json_str)

        except Exception as e:
            print(f"  ⚠️ 第 {attempt + 1} 次尝试失败：{e}")

    # 兜底：所有重试都失败，返回默认值，不让程序崩溃
    print(f"  ❌ {max_retries} 次重试均失败，返回默认值")
    return Person(name="unknown", age=0, occupation="unknown", skills=[])


# ============================================================
# 容错策略：重试 + 默认值
# ============================================================
def get_json_with_retry(query: str, max_retries: int = 3) -> dict:
    """
    带重试的 JSON 解析（方案 2 的增强版）

    Args:
        query: 包含人物信息的自然语言文本
        max_retries: 最大重试次数，默认 3 次

    Returns:
        dict: 解析后的 JSON 字典，失败时返回默认值
    """
    for attempt in range(max_retries):
        try:
            result = get_json_v2_system_prompt(query)
            return result
        except (json.JSONDecodeError, KeyError) as e:
            print(f"第 {attempt + 1} 次解析失败：{e}")
            if attempt == max_retries - 1:
                return {
                    "name": "unknown",
                    "age": 0,
                    "occupation": "unknown",
                    "error": "解析失败超过最大重试次数",
                }
    return {}


# ============================================================
# 5 种方案对比
# ============================================================
COMPARISON_TABLE = """
方案对比：

| 方案 | 稳定性 | 性能 | 易用性 | 推荐场景 |
|------|--------|------|--------|---------|
| 1. Prompt 约束 | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 简单场景，能容忍失败 |
| 2. System Prompt 强化 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 通用场景，快速原型 |
| 3. Pydantic + generate_json | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 生产环境 ⭐⭐⭐ |
| 4. Outlines 受限解码 | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | 必须 100% 稳定的场景 |
| 5. generate_json + 重试 + 校验 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 生产环境（最高保障）⭐⭐⭐ |

💡 推荐：
- 日常开发：方案 3（Pydantic + generate_json）
- 关键业务：方案 5（generate_json + 重试 + Pydantic 校验）
- 类型安全 + 自动校验 + 不需要手动写 JSON Schema + IDE 自动补全
"""


# ⭐ 面试官追问：怎么保证大模型 100% 输出 JSON？
"""
3 分钟回答模板：

100% 保证 JSON 输出有 5 层方案，从弱到强：

第 1 层：Prompt 约束（最基础）
- 在 prompt 里明确要求"只输出 JSON"
- 给出 JSON 格式示例
- 加 temperature=0 降低随机性
- 缺点：仍然可能出错，约 5-10% 失败率

第 2 层：System Prompt 强化
- 用 system 参数明确要求返回合法 JSON
- 比纯 Prompt 约束更稳定
- 缺点：不保证 schema 正确（字段可能缺）

第 3 层：generate_json + Pydantic（推荐）
- Pydantic 定义 schema，自动生成 JSON Schema
- generate_json() 让模型按 schema 输出
- Pydantic 自动校验字段类型和约束
- 工业级方案，生产环境首选

第 4 层：受限解码（Outlines/Guidance）
- 底层 logits 强制约束，100% 保证 schema 正确
- 适合金融、医疗等容错率为 0 的场景

第 5 层：generate_json + 重试 + Pydantic 校验（最高保障）
- 在方案 3 基础上增加指数退避重试
- 三层防护：Prompt → Schema → 类型校验
- 失败时返回默认值兜底，程序永不崩溃

兜底策略：
- 多次重试（指数退避）
- 解析失败时返回默认值
- 记录失败 case，分析 prompt 问题
"""


if __name__ == "__main__":
    query = "张三今年 28 岁，是一名 Python 工程师，会 FastAPI 和 Docker。"

    print("=" * 60)
    print(f"输入：{query}")
    print("=" * 60)

    print("\n方案 1：Prompt 约束")
    # print(get_json_v1_prompt_only(query))

    print("\n方案 2：System Prompt 强化")
    # print(get_json_v2_system_prompt(query))

    print("\n方案 3：Pydantic + generate_json（推荐 ⭐）")
    # person = get_json_v3_pydantic(query)
    # print(f"  姓名：{person.name}")
    # print(f"  年龄：{person.age}")
    # print(f"  职业：{person.occupation}")
    # print(f"  技能：{person.skills}")

    print("\n方案 5：generate_json + 重试 + Pydantic 校验（生产级 ⭐⭐）")
    # person = get_json_v5_production(query)
    # print(f"  姓名：{person.name}")
    # print(f"  年龄：{person.age}")
    # print(f"  职业：{person.occupation}")
    # print(f"  技能：{person.skills}")

    print("\n" + COMPARISON_TABLE)
