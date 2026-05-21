#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenAI 客户端统一封装
提供统一的 API 调用接口和错误处理
"""

import os
from typing import Optional, Dict, Any, List, Union
from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionMessage

# 全局客户端实例
_client: Optional[OpenAI] = None


def get_client(api_key: Optional[str] = None) -> OpenAI:
    """
    获取 OpenAI 客户端实例
    
    :param api_key: OpenAI API Key，若未提供则从环境变量 OPENAI_API_KEY 获取
    :return: OpenAI 客户端实例
    :raises ValueError: 未提供 API Key 且环境变量中也未设置
    """
    global _client
    
    if _client is None:
        key = api_key or os.environ.get("OPENAI_API_KEY")
        if not key:
            raise ValueError(
                "API Key 未设置！请提供 api_key 参数或设置环境变量 OPENAI_API_KEY"
            )
        _client = OpenAI(api_key=key)
    
    return _client


def chat_completion(
    model: str = "gpt-3.5-turbo",
    messages: List[Dict[str, str]],
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    response_format: Optional[Dict[str, str]] = None,
    tools: Optional[List[Dict[str, Any]]] = None,
    tool_choice: Optional[Union[str, Dict[str, Any]]] = None,
    api_key: Optional[str] = None,
) -> ChatCompletion:
    """
    调用 OpenAI Chat Completion API
    
    :param model: 模型名称，默认为 gpt-3.5-turbo
    :param messages: 消息列表，每个消息包含 role 和 content
    :param temperature: 温度参数，控制输出随机性，0-2
    :param max_tokens: 最大输出 token 数
    :param response_format: 响应格式，如 {"type": "json_object"}
    :param tools: 工具列表，用于 function calling
    :param tool_choice: 工具选择策略
    :param api_key: OpenAI API Key
    :return: ChatCompletion 对象
    :raises Exception: API 调用失败时抛出异常
    """
    client = get_client(api_key)
    
    try:
        params: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }
        
        if max_tokens is not None:
            params["max_tokens"] = max_tokens
        
        if response_format is not None:
            params["response_format"] = response_format
        
        if tools is not None:
            params["tools"] = tools
        
        if tool_choice is not None:
            params["tool_choice"] = tool_choice
        
        response = client.chat.completions.create(**params)
        return response
    
    except Exception as e:
        raise Exception(f"OpenAI API 调用失败: {str(e)}") from e


def get_response_content(response: ChatCompletion) -> str:
    """
    从 ChatCompletion 响应中提取内容
    
    :param response: ChatCompletion 对象
    :return: 响应内容字符串
    """
    if response.choices and response.choices[0].message:
        return response.choices[0].message.content or ""
    return ""


def get_tool_call_args(response: ChatCompletion) -> Optional[str]:
    """
    从响应中提取工具调用参数
    
    :param response: ChatCompletion 对象
    :return: 工具调用参数的 JSON 字符串
    """
    message: ChatCompletionMessage = response.choices[0].message
    if message.tool_calls and message.tool_calls[0]:
        return message.tool_calls[0].function.arguments
    return None


def set_api_key(api_key: str) -> None:
    """
    设置全局 API Key（会重置客户端）
    
    :param api_key: OpenAI API Key
    """
    global _client
    _client = None
    os.environ["OPENAI_API_KEY"] = api_key