#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day03 必写代码 3：Token 计数工具
功能：计算文本和对话消息的 Token 数量，并进行成本估算
"""

import tiktoken


def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """计算文本的 Token 数量"""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def count_messages_tokens(messages: list, model: str = "gpt-3.5-turbo") -> int:
    """
    计算对话消息的总 Token 数量
    
    注意：OpenAI 的消息计数有固定开销：
    - 每轮消息有 3 个 Token 的基础开销
    - name 字段额外加 1 个 Token
    - 最后有 3 个 Token 的收尾开销
    """
    encoding = tiktoken.encoding_for_model(model)
    
    tokens_per_message = 3
    tokens_per_name = 1
    
    total_tokens = 0
    for message in messages:
        total_tokens += tokens_per_message
        for key, value in message.items():
            total_tokens += len(encoding.encode(value))
            if key == "name":
                total_tokens += tokens_per_name
    
    # 最后有固定的 3 个 Token 开销
    total_tokens += 3
    return total_tokens


def estimate_cost(input_tokens: int, output_tokens: int, model: str = "gpt-3.5-turbo") -> float:
    """
    估算 API 调用成本（美元）
    
    价格参考（2024年）：
    - gpt-3.5-turbo: $0.5 / 1M 输入，$1.5 / 1M 输出
    - gpt-4o: $5 / 1M 输入，$15 / 1M 输出
    """
    price_map = {
        "gpt-3.5-turbo": (0.5 / 1_000_000, 1.5 / 1_000_000),
        "gpt-4o": (5.0 / 1_000_000, 15.0 / 1_000_000),
    }
    
    input_price, output_price = price_map.get(model, (0.5 / 1_000_000, 1.5 / 1_000_000))
    return input_tokens * input_price + output_tokens * output_price


if __name__ == "__main__":
    # 测试：纯文本 Token 计数
    text = "你好，我想了解一下什么是大模型 Agent。"
    token_count = count_tokens(text)
    print(f"文本内容：{text}")
    print(f"Token 数量：{token_count}")
    print()
    
    # 测试：对话消息 Token 计数
    messages = [
        {"role": "system", "content": "你是一个 helpful 的助手。"},
        {"role": "user", "content": "什么是大模型 Agent？"}
    ]
    
    message_tokens = count_messages_tokens(messages)
    print(f"对话消息 Token 数量：{message_tokens}")
    
    # 成本估算
    estimated_output_tokens = 100  # 假设输出 100 Token
    cost = estimate_cost(message_tokens, estimated_output_tokens, "gpt-3.5-turbo")
    print(f"预估成本（GPT-3.5）：${cost:.6f}")
    print()
    
    # 中文 vs 英文 Token 对比
    chinese_text = "我想学习大模型 Agent 开发，你能给我一些建议吗？"
    english_text = "I want to learn LLM Agent development, can you give me some advice?"
    
    chinese_tokens = count_tokens(chinese_text)
    english_tokens = count_tokens(english_text)
    
    print("中文 vs 英文 Token 对比：")
    print(f"  中文（{len(chinese_text)}字）：{chinese_tokens} Token")
    print(f"  英文（{len(english_text.split())}词）：{english_tokens} Token")
    print(f"  比例：中文/英文 = {chinese_tokens/english_tokens:.2f}")
