#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day02 必写代码 4：JSON 结构化输出 100% 稳定方案
功能：4 种方案保证大模型 100% 输出可解析的 JSON

面试考点：
- 怎么保证大模型 100% 输出 JSON？
- response_format 和 Pydantic 哪个好？
- JSON 解析失败怎么办？
- 4 种方案的优缺点对比？
"""

import json
from openai import OpenAI
from pydantic import BaseModel, Field

client = OpenAI(api_key="your-api-key")


# ============================================================
# 方案 1：Prompt 约束 + 后处理（最基础，不推荐）
# ============================================================
def get_json_v1_prompt_only(query: str) -> dict:
    """方案 1：只靠 Prompt 约束输出 JSON"""
    prompt = f"""
请提取下面文本中的人物信息，输出 JSON 格式：
{{"name": "姓名", "age": 年龄, "occupation": "职业"}}

只输出 JSON，不要任何其他文字！

文本：{query}
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.choices[0].message.content
    
    # 需要手动清洗（容易失败）
    text = text.strip().replace("```json", "").replace("```", "")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"error": "解析失败", "raw": text}


# ============================================================
# 方案 2：response_format JSON Mode（OpenAI 官方）
# ============================================================
def get_json_v2_response_format(query: str) -> dict:
    """方案 2：用 OpenAI 的 JSON Mode（必须在 prompt 里也提到 JSON）"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",  # 必须是支持 JSON Mode 的版本
        messages=[
            {"role": "system", "content": "你必须返回有效的 JSON。"},
            {"role": "user", "content": f"提取人物信息（JSON）：{query}"}
        ],
        response_format={"type": "json_object"},  # ⭐ 关键参数
    )
    return json.loads(response.choices[0].message.content)


# ============================================================
# 方案 3：Pydantic + Function Calling（推荐 ⭐）
# ============================================================
class Person(BaseModel):
    """人物信息模型"""
    name: str = Field(description="姓名")
    age: int = Field(description="年龄", ge=0, le=150)
    occupation: str = Field(description="职业")
    skills: list[str] = Field(default=[], description="技能列表")


def get_json_v3_pydantic(query: str) -> Person:
    """方案 3：Pydantic 定义 schema + Function Calling 严格输出"""
    
    # Pydantic 模型自动转 JSON Schema
    schema = Person.model_json_schema()
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"提取信息：{query}"}],
        tools=[{
            "type": "function",
            "function": {
                "name": "extract_person",
                "description": "提取人物信息",
                "parameters": schema,
            }
        }],
        tool_choice={"type": "function", "function": {"name": "extract_person"}},
    )
    
    # 拿到结构化结果
    args = response.choices[0].message.tool_calls[0].function.arguments
    return Person.model_validate_json(args)  # 自动校验！


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
# 容错策略：重试 + 默认值
# ============================================================
def get_json_with_retry(query: str, max_retries: int = 3) -> dict:
    """带重试的 JSON 解析"""
    for attempt in range(max_retries):
        try:
            result = get_json_v2_response_format(query)
            return result
        except (json.JSONDecodeError, KeyError) as e:
            print(f"第 {attempt + 1} 次解析失败：{e}")
            if attempt == max_retries - 1:
                # 兜底：返回默认值，不让程序崩溃
                return {
                    "name": "unknown",
                    "age": 0,
                    "occupation": "unknown",
                    "error": "解析失败超过最大重试次数"
                }
    return {}


# ============================================================
# 4 种方案对比
# ============================================================
COMPARISON_TABLE = """
方案对比：

| 方案 | 稳定性 | 性能 | 易用性 | 推荐场景 |
|------|--------|------|--------|---------|
| 1. Prompt 约束 | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 简单场景，能容忍失败 |
| 2. JSON Mode | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | OpenAI 模型，简单结构 |
| 3. Pydantic + Function Calling | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 生产环境 ⭐⭐⭐ |
| 4. Outlines 受限解码 | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | 必须 100% 稳定的场景 |

💡 推荐：方案 3（Pydantic + Function Calling）
- 类型安全 + 自动校验
- 不需要手动写 JSON Schema
- 大部分模型都支持
- IDE 自动补全
"""


# ⭐ 面试官追问：怎么保证大模型 100% 输出 JSON？
"""
3 分钟回答模板：

100% 保证 JSON 输出有 4 层方案，从弱到强：

第 1 层：Prompt 约束（最基础）
- 在 prompt 里明确要求"只输出 JSON"
- 给出 JSON 格式示例
- 加 temperature=0 降低随机性
- 缺点：仍然可能出错，约 5-10% 失败率

第 2 层：JSON Mode（OpenAI 官方）
- 加 response_format={"type": "json_object"}
- 模型层面强制输出合法 JSON
- 缺点：不保证 schema 正确（字段可能缺）

第 3 层：Function Calling + Pydantic（推荐）
- Pydantic 定义 schema，自动生成 JSON Schema
- Function Calling 让模型按 schema 输出
- Pydantic 自动校验字段类型和约束
- 工业级方案，生产环境首选

第 4 层：受限解码（Outlines/Guidance）
- 底层 logits 强制约束，100% 保证 schema 正确
- 适合金融、医疗等容错率为 0 的场景

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
    
    print("\n方案 2：JSON Mode")
    # print(get_json_v2_response_format(query))
    
    print("\n方案 3：Pydantic + Function Calling（推荐 ⭐）")
    # person = get_json_v3_pydantic(query)
    # print(f"  姓名：{person.name}")
    # print(f"  年龄：{person.age}")
    # print(f"  职业：{person.occupation}")
    # print(f"  技能：{person.skills}")
    
    print("\n" + COMPARISON_TABLE)
