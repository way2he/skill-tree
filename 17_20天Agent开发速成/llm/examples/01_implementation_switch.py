# -*- coding: utf-8 -*-
"""
示例：自由切换底层实现方式

展示如何在不同的实现方式之间自由切换。
"""

from llm.core.factory import create_llm


def example_with_requests():
    """使用 requests 实现（默认）"""
    print("=" * 60)
    print("使用 requests 实现（默认）")
    print("=" * 60)
    
    # 使用默认实现（不需要指定 implementation）
    llm = create_llm("openai", api_key="test-key")
    print("✅ 创建成功: requests 实现")
    print()


def example_with_aiohttp():
    """使用 aiohttp 实现"""
    print("=" * 60)
    print("使用 aiohttp 实现")
    print("=" * 60)
    
    # 指定使用 aiohttp 实现
    llm = create_llm("openai", implementation="aiohttp", api_key="test-key")
    print("✅ 创建成功: aiohttp 实现")
    print()


def example_with_openai_sdk():
    """使用 OpenAI SDK 实现"""
    print("=" * 60)
    print("使用 OpenAI SDK 实现")
    print("=" * 60)
    
    # 指定使用 OpenAI SDK 实现
    llm = create_llm("openai", implementation="openai_sdk", api_key="test-key")
    print("✅ 创建成功: OpenAI SDK 实现")
    print()


def example_with_anthropic_sdk():
    """使用 Anthropic SDK 实现"""
    print("=" * 60)
    print("使用 Anthropic SDK 实现")
    print("=" * 60)
    
    # 指定使用 Anthropic SDK 实现
    llm = create_llm("anthropic", implementation="anthropic_sdk", api_key="test-key")
    print("✅ 创建成功: Anthropic SDK 实现")
    print()


if __name__ == "__main__":
    print("🎯 LLM 实现方式切换演示")
    print()
    
    example_with_requests()
    example_with_aiohttp()
    example_with_openai_sdk()
    example_with_anthropic_sdk()
    
    print("✨ 所有示例完成！")
    print()
    print("💡 支持的实现方式:")
    print("  - requests (默认)")
    print("  - aiohttp")
    print("  - openai_sdk")
    print("  - anthropic_sdk")
    print("  - qwen_sdk")
    print("  - glm_sdk")
    print("  - wenxin_sdk")
    print("  - doubao_sdk")
    print("  - cohere_sdk")
    print("  - gemini_sdk")
    print("  - groq_sdk")
    print("  - mistral_sdk")
