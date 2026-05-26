# -*- coding: utf-8 -*-
"""
LLM 工具函数模块
提供 JSON 校验、重试机制等通用功能
"""

import json
import time
from typing import Any, Callable, Literal, Type

from pydantic import BaseModel


def validate_json_output(
    json_str: str, model_class: Type[BaseModel] | None = None
) -> Any:
    """
    校验 JSON 输出是否符合格式

    Args:
        json_str: 模型输出的 JSON 字符串
        model_class: 可选的 Pydantic 模型类，用于校验和解析

    Returns:
        如果提供了 model_class，返回模型实例；否则返回 dict
        如果校验失败返回 None
    """
    try:
        json_str = json_str.strip()

        if json_str.startswith("```json"):
            json_str = json_str[7:]
        if json_str.startswith("```"):
            json_str = json_str[3:]
        if json_str.endswith("```"):
            json_str = json_str[:-3]
        json_str = json_str.strip()

        if model_class:
            return model_class.model_validate_json(json_str)
        else:
            return json.loads(json_str)
    except Exception as e:
        print(f"[ERROR] 校验失败: {e}")
        return None


def generate_with_retry(
    generate_func: Callable[[], str],
    model_class: Type[BaseModel] | None = None,
    max_retries: int = 3,
    backoff: float = 1.0,
) -> Any:
    """
    带重试的生成函数

    Args:
        generate_func: 实际调用大模型的函数
        model_class: 可选的 Pydantic 模型类，用于校验输出
        max_retries: 最大重试次数
        backoff: 退避时间（秒）

    Returns:
        校验后的结果，如果全部重试失败返回 None
    """
    for attempt in range(max_retries):
        try:
            output = generate_func()
            result = validate_json_output(output, model_class)
            if result:
                print(f"[SUCCESS] 第 {attempt + 1} 次尝试成功！")
                return result
        except Exception as e:
            print(f"[WARNING] 第 {attempt + 1} 次尝试失败: {e}")

        if attempt < max_retries - 1:
            sleep_time = backoff * (2**attempt)
            print(f"[INFO] {sleep_time} 秒后重试...")
            time.sleep(sleep_time)

    print(f"[ERROR] {max_retries} 次重试全部失败")
    return None


def generate_from_pydantic(
    prompt: str,
    model_class: Type[BaseModel],
    provider: Literal["ollama", "openai", "doubao", "anthropic"] = "ollama",
    max_retries: int = 3,
    **kwargs: Any,
) -> Any:
    """
    基于 Pydantic 模型的生成函数

    Args:
        prompt: 用户提示词
        model_class: Pydantic 模型类，用于定义输出格式
        provider: LLM 提供商类型
        max_retries: 最大重试次数
        **kwargs: 传递给 LLM 客户端的其他参数

    Returns:
        模型实例，如果失败返回 None
    """
    from .clients import llm_generate_json

    json_schema = model_class.model_json_schema()

    def generate_func() -> str:
        return llm_generate_json(
            prompt, schema=json_schema, provider=provider, **kwargs
        )

    return generate_with_retry(generate_func, model_class, max_retries)
