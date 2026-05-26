#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM 客户端统一封装
支持 OpenAI、Doubao（火山引擎）、Ollama 多种协议
提供统一的 API 调用接口和错误处理
"""

import json
import os
from typing import Optional, Dict, Any, List, Union, Literal

import requests

# 全局客户端实例
_clients: Dict[str, Any] = {}


def get_client(
    provider: Literal["openai", "doubao", "ollama"] = "openai",
    api_key: Optional[str] = None,
    **kwargs
) -> Any:
    """
    获取 LLM 客户端实例
    
    :param provider: 提供商类型，支持 openai、doubao、ollama
    :param api_key: API Key，若未提供则从环境变量获取
    :param kwargs: 额外参数，如 base_url, model, region 等
    :return: 客户端实例
    :raises ValueError: 未提供 API Key 且环境变量中也未设置
    """
    client_key = f"{provider}_{api_key or 'default'}"
    
    if client_key not in _clients:
        if provider == "openai":
            _clients[client_key] = _create_openai_client(api_key, **kwargs)
        elif provider == "doubao":
            _clients[client_key] = _create_doubao_client(api_key, **kwargs)
        elif provider == "ollama":
            _clients[client_key] = _create_ollama_client(**kwargs)
        else:
            raise ValueError(f"不支持的提供商: {provider}")
    
    return _clients[client_key]


def _create_openai_client(
    api_key: Optional[str] = None,
    base_url: str = "https://api.openai.com/v1",
    **kwargs
) -> Dict[str, Any]:
    """创建 OpenAI 客户端配置"""
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("API Key 未设置！请提供 api_key 参数或设置环境变量 OPENAI_API_KEY")
    
    return {
        "provider": "openai",
        "api_key": key,
        "base_url": base_url.rstrip("/"),
        **kwargs
    }


def _create_doubao_client(
    api_key: Optional[str] = None,
    region: str = "cn-beijing",
    **kwargs
) -> Dict[str, Any]:
    """创建 Doubao 客户端配置"""
    key = api_key or os.environ.get("VOLCENGINE_API_KEY")
    if not key:
        raise ValueError("API Key 未设置！请提供 api_key 参数或设置环境变量 VOLCENGINE_API_KEY")
    
    regions = {
        "cn-beijing": "ark.cn-beijing.volces.com",
        "cn-guangzhou": "ark.cn-guangzhou.volces.com",
        "cn-shanghai": "ark.cn-shanghai.volces.com",
        "cn-hangzhou": "ark.cn-hangzhou.volces.com",
    }
    
    return {
        "provider": "doubao",
        "api_key": key,
        "base_url": f"https://{regions.get(region, region)}/api/v3",
        **kwargs
    }


def _create_ollama_client(
    base_url: str = "http://localhost:11434",
    **kwargs
) -> Dict[str, Any]:
    """创建 Ollama 客户端配置"""
    return {
        "provider": "ollama",
        "base_url": base_url.rstrip("/"),
        **kwargs
    }


def _build_request_headers(client: Dict[str, Any]) -> Dict[str, str]:
    """构建请求头"""
    headers = {"Content-Type": "application/json"}
    
    if client["provider"] in ("openai", "doubao"):
        headers["Authorization"] = f"Bearer {client['api_key']}"
    
    return headers


def _build_messages(
    messages: List[Dict[str, str]],
    system_prompt: Optional[str] = None
) -> List[Dict[str, str]]:
    """构建消息列表，添加系统提示词"""
    result = []
    if system_prompt:
        result.append({"role": "system", "content": system_prompt})
    result.extend(messages)
    return result


def chat_completion(
    model: str = "gpt-3.5-turbo",
    messages: List[Dict[str, str]] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    response_format: Optional[Dict[str, str]] = None,
    tools: Optional[List[Dict[str, Any]]] = None,
    tool_choice: Optional[Union[str, Dict[str, Any]]] = None,
    api_key: Optional[str] = None,
    provider: Literal["openai", "doubao", "ollama"] = "openai",
    base_url: Optional[str] = None,
    region: str = "cn-beijing",
    system_prompt: Optional[str] = None,
    timeout: int = 60,
) -> Dict[str, Any]:
    """
    调用 LLM Chat Completion API
    
    :param model: 模型名称
    :param messages: 消息列表，每个消息包含 role 和 content
    :param temperature: 温度参数，控制输出随机性，0-2
    :param max_tokens: 最大输出 token 数
    :param response_format: 响应格式，如 {"type": "json_object"}
    :param tools: 工具列表，用于 function calling
    :param tool_choice: 工具选择策略
    :param api_key: API Key
    :param provider: 提供商类型，支持 openai、doubao、ollama
    :param base_url: API 基础地址
    :param region: Doubao 区域标识
    :param system_prompt: 系统提示词
    :param timeout: 请求超时时间（秒）
    :return: ChatCompletion 响应字典
    :raises Exception: API 调用失败时抛出异常
    """
    if messages is None:
        messages = []
    
    client_kwargs = {}
    if base_url:
        client_kwargs["base_url"] = base_url
    if provider == "doubao":
        client_kwargs["region"] = region
    
    client = get_client(provider=provider, api_key=api_key, **client_kwargs)
    
    try:
        params: Dict[str, Any] = {
            "model": model,
            "messages": _build_messages(messages, system_prompt),
            "temperature": temperature,
        }
        
        if max_tokens is not None:
            params["max_tokens"] = max_tokens
        
        if response_format is not None:
            params["response_format"] = response_format
        
        if tools is not None and provider != "ollama":
            params["tools"] = tools
        
        if tool_choice is not None and provider != "ollama":
            params["tool_choice"] = tool_choice
        
        if provider == "ollama":
            params["stream"] = False
            if "response_format" in params and params["response_format"].get("type") == "json_object":
                params["format"] = "json"
                del params["response_format"]
            url = f"{client['base_url']}/api/generate"
        else:
            url = f"{client['base_url']}/chat/completions"
        
        headers = _build_request_headers(client)
        
        response = requests.post(
            url,
            headers=headers,
            json=params,
            timeout=timeout
        )
        response.raise_for_status()
        
        response_json = response.json()
        
        if provider == "ollama":
            return {
                "choices": [{
                    "message": {
                        "content": response_json.get("response", ""),
                        "role": "assistant"
                    },
                    "finish_reason": response_json.get("done", "stop")
                }],
                "model": model,
                "usage": {
                    "prompt_tokens": response_json.get("prompt_eval_count", 0),
                    "completion_tokens": response_json.get("eval_count", 0),
                    "total_tokens": response_json.get("prompt_eval_count", 0) + response_json.get("eval_count", 0)
                }
            }
        
        return response_json
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"{provider.capitalize()} API 调用失败: {str(e)}") from e
    except Exception as e:
        raise Exception(f"{provider.capitalize()} API 处理失败: {str(e)}") from e


def get_response_content(response: Dict[str, Any]) -> str:
    """
    从 ChatCompletion 响应中提取内容
    
    :param response: ChatCompletion 响应字典
    :return: 响应内容字符串
    """
    if response.get("choices") and response["choices"][0].get("message"):
        return response["choices"][0]["message"].get("content", "")
    return ""


def get_tool_call_args(response: Dict[str, Any]) -> Optional[str]:
    """
    从响应中提取工具调用参数
    
    :param response: ChatCompletion 响应字典
    :return: 工具调用参数的 JSON 字符串
    """
    message = response.get("choices", [{}])[0].get("message", {})
    if message.get("tool_calls") and message["tool_calls"][0]:
        return message["tool_calls"][0]["function"].get("arguments")
    return None


def set_api_key(api_key: str, provider: Literal["openai", "doubao"] = "openai") -> None:
    """
    设置全局 API Key（会重置客户端）
    
    :param api_key: API Key
    :param provider: 提供商类型
    """
    global _clients
    env_var = "OPENAI_API_KEY" if provider == "openai" else "VOLCENGINE_API_KEY"
    os.environ[env_var] = api_key
    _clients = {}


def generate_json(
    prompt: str,
    model: str = "gpt-3.5-turbo",
    provider: Literal["openai", "doubao", "ollama"] = "openai",
    api_key: Optional[str] = None,
    **kwargs
) -> str:
    """
    生成 JSON 格式响应
    
    :param prompt: 用户提示词
    :param model: 模型名称
    :param provider: 提供商类型
    :param api_key: API Key
    :param kwargs: 其他参数
    :return: JSON 字符串
    """
    messages = [{"role": "user", "content": prompt}]
    
    response = chat_completion(
        model=model,
        messages=messages,
        temperature=kwargs.get("temperature", 0.3),
        response_format={"type": "json_object"},
        api_key=api_key,
        provider=provider,
        **kwargs
    )
    
    return get_response_content(response)