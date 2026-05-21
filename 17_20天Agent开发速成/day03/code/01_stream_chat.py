#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day03 必写代码 1：流式输出完整实现
功能：演示 OpenAI API 的流式输出和非流式输出对比
"""

from openai import OpenAI

client = OpenAI(api_key="your-api-key")


def stream_chat(messages):
    """流式输出，逐字打印"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True  # 关键参数：开启流式输出
    )
    
    full_content = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            full_content += content
            print(content, end="", flush=True)  # 逐字打印，不换行
    
    return full_content


def normal_chat(messages):
    """非流式输出，等全部生成完才返回"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=False
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    messages = [{"role": "user", "content": "什么是大模型 Agent？"}]
    
    print("=" * 50)
    print("流式输出演示：")
    print("=" * 50)
    stream_chat(messages)
    
    print("\n\n" + "=" * 50)
    print("非流式输出演示：")
    print("=" * 50)
    result = normal_chat(messages)
    print(result)
