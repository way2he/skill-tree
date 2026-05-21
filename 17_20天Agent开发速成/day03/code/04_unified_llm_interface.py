#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day03 必写代码 4：统一接口层完整实现
功能：策略模式 + 工厂模式，统一 OpenAI、DeepSeek 等多家模型接口
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Generator
import os


class BaseLLM(ABC):
    """LLM 抽象基类，定义统一接口"""
    
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """非流式聊天接口"""
        pass
    
    @abstractmethod
    def stream_chat(self, messages: List[Dict[str, str]], **kwargs) -> Generator[str, None, None]:
        """流式聊天接口"""
        pass


class OpenAILLM(BaseLLM):
    """OpenAI 模型实现"""
    
    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo"):
        from openai import OpenAI
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 2000),
        )
        return response.choices[0].message.content
    
    def stream_chat(self, messages: List[Dict[str, str]], **kwargs) -> Generator[str, None, None]:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 2000),
            stream=True,
        )
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


class DeepSeekLLM(BaseLLM):
    """DeepSeek 国产模型实现"""
    
    def __init__(self, api_key: str = None, model: str = "deepseek-chat"):
        from openai import OpenAI  # DeepSeek 兼容 OpenAI SDK
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com/v1"
        )
        self.model = model
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 2000),
        )
        return response.choices[0].message.content
    
    def stream_chat(self, messages: List[Dict[str, str]], **kwargs) -> Generator[str, None, None]:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 2000),
            stream=True,
        )
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


class LLMFactory:
    """LLM 工厂类，根据配置创建对应的模型实例"""
    
    @staticmethod
    def create_llm(llm_type: str, **kwargs) -> BaseLLM:
        """
        创建 LLM 实例
        
        Args:
            llm_type: 模型类型，支持 "openai", "deepseek"
            **kwargs: 其他参数，如 api_key, model
        
        Returns:
            BaseLLM 实例
        """
        llm_map = {
            "openai": OpenAILLM,
            "deepseek": DeepSeekLLM,
        }
        
        if llm_type not in llm_map:
            raise ValueError(f"不支持的模型类型: {llm_type}, 支持的类型: {list(llm_map.keys())}")
        
        return llm_map[llm_type](**kwargs)


# 使用示例
if __name__ == "__main__":
    # 方式 1：直接创建模型实例
    print("=" * 60)
    print("方式 1：直接创建 OpenAI 实例")
    print("=" * 60)
    openai_llm = OpenAILLM(api_key="your-key", model="gpt-3.5-turbo")
    # result = openai_llm.chat([{"role": "user", "content": "你好"}])
    # print(result)
    
    # 方式 2：使用工厂模式创建（推荐）
    print("\n" + "=" * 60)
    print("方式 2：使用工厂模式创建（换模型只改一行配置）")
    print("=" * 60)
    
    # 配置可以放在配置文件或环境变量中
    config = {
        "llm_type": "deepseek",  # 改成 "openai" 就自动切换
        "api_key": "your-key",
        "model": "deepseek-chat"
    }
    
    llm = LLMFactory.create_llm(**config)
    
    # 业务代码完全不需要改
    messages = [{"role": "user", "content": "什么是大模型 Agent？"}]
    # result = llm.chat(messages)
    # print(result)
    
    print("\n✅ 统一接口层的好处：")
    print("  1. 换模型不需要改业务代码，只改配置")
    print("  2. 统一的错误处理、重试、日志")
    print("  3. 方便添加监控和统计")
    print("  4. 符合开闭原则：对扩展开放，对修改关闭")
