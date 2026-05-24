# -*- coding: utf-8 -*-
"""
底层实现选择器使用示例

演示如何使用一键配置、Builder 模式、运行时切换功能
"""

import os
from llm.core import (
    # 一键配置
    set_default_backend,
    get_default_backend,
    reset_default_backend,
    get_llm,
    # Builder 模式
    LLMClientBuilder,
    BackendType,
    # 便捷函数
    create_client,
    create_async_client,
    # 运行时切换
    BackendSwitcher,
)


def demo_one_click_config():
    """演示一键配置功能"""
    print("=" * 60)
    print("一键配置示例")
    print("=" * 60)

    # 方式一：代码全局设置
    print("\n--- 方式一：代码全局设置 ---")
    set_default_backend("openai_sdk")
    print(f"当前默认 backend: {get_default_backend()}")

    # 之后所有 get_llm() 自动使用 openai_sdk
    # client = get_llm("deepseek")  # 实际调用需要 API 密钥
    print("设置成功！后续 get_llm() 会自动使用 openai_sdk")

    # 重置
    reset_default_backend()
    print(f"重置后: {get_default_backend()}")

    # 方式二：环境变量（最简单）
    print("\n--- 方式二：环境变量 ---")
    print("在 .env 文件中添加：LLM_BACKEND=openai_sdk")
    print("或在代码中设置：os.environ['LLM_BACKEND'] = 'openai_sdk'")

    # 方式三：YAML 配置（最持久）
    print("\n--- 方式三：YAML 配置 ---")
    print("在 llm/core/llm_config.yaml 中添加：")
    print("  default_backend: openai_sdk")


def demo_builder_pattern():
    """演示 Builder 模式"""
    print("\n" + "=" * 60)
    print("Builder 模式示例")
    print("=" * 60)

    # 示例 1：使用 requests 实现
    print("\n--- 示例 1：requests 实现 ---")
    builder1 = (
        LLMClientBuilder()
        .provider("deepseek")
        .requests()  # 或 .backend("requests")
        .api_key("${DEEPSEEK_API_KEY}")
        .model("deepseek-chat")
        .temperature(0.7)
    )
    print(f"配置: provider={builder1.get_config().provider}, "
          f"backend={builder1.get_config().backend}")
    # client1 = builder1.build()  # 实际调用需要有效 API 密钥

    # 示例 2：使用 OpenAI SDK
    print("\n--- 示例 2：OpenAI SDK ---")
    builder2 = (
        LLMClientBuilder()
        .provider("deepseek")
        .openai_sdk()
        .api_key("${DEEPSEEK_API_KEY}")
        .base_url("https://api.deepseek.com/v1")
        .model("deepseek-chat")
    )
    print(f"配置: provider={builder2.get_config().provider}, "
          f"backend={builder2.get_config().backend}")

    # 示例 3：使用 BackendType 枚举
    print("\n--- 示例 3：BackendType 枚举 ---")
    builder3 = (
        LLMClientBuilder()
        .provider("openai")
        .backend(BackendType.OPENAI_SDK)
        .api_key("${OPENAI_API_KEY}")
    )
    print(f"配置: provider={builder3.get_config().provider}, "
          f"backend={builder3.get_config().backend}")

    # 示例 4：创建异步客户端
    print("\n--- 示例 4：异步客户端 ---")
    builder4 = (
        LLMClientBuilder()
        .provider("deepseek")
        .aiohttp()  # 异步实现
        .api_key("${DEEPSEEK_API_KEY}")
    )
    print(f"配置: provider={builder4.get_config().provider}, "
          f"backend={builder4.get_config().backend}")
    # async_client = builder4.build_async()


def demo_convenience_functions():
    """演示便捷函数"""
    print("\n" + "=" * 60)
    print("便捷函数示例")
    print("=" * 60)

    # 示例 1：创建同步客户端
    print("\n--- 示例 1：同步客户端 ---")
    print("client = create_client('deepseek', 'requests', api_key='sk-xxx')")
    print("client = create_client('deepseek', BackendType.REQUESTS, api_key='sk-xxx')")

    # 示例 2：创建异步客户端
    print("\n--- 示例 2：异步客户端 ---")
    print("async_client = create_async_client('deepseek', 'aiohttp', api_key='sk-xxx')")

    # 示例 3：不指定 backend（使用全局默认）
    print("\n--- 示例 3：使用全局默认 ---")
    set_default_backend("openai_sdk")
    print("set_default_backend('openai_sdk')")
    print("client = create_client('deepseek', api_key='sk-xxx')  # 自动使用 openai_sdk")
    reset_default_backend()


def demo_backend_switcher():
    """演示运行时切换"""
    print("\n" + "=" * 60)
    print("运行时切换示例")
    print("=" * 60)

    # 创建切换器
    print("\n--- 创建切换器 ---")
    switcher = (
        BackendSwitcher("deepseek")
        .add_backend("requests", api_key="${DEEPSEEK_API_KEY}")
        .add_backend("openai_sdk", api_key="${DEEPSEEK_API_KEY}",
                     base_url="https://api.deepseek.com/v1")
    )
    print(f"已配置实现: {switcher.list_backends()}")
    print(f"当前实现: {switcher.current_backend()}")

    # 切换实现
    print("\n--- 切换实现 ---")
    print("switcher.switch_to('openai_sdk')")
    switcher.switch_to("openai_sdk")
    print(f"切换后: {switcher.current_backend()}")

    # 故障转移
    print("\n--- 故障转移 ---")
    print("client = switcher.get_client_with_fallback(['openai_sdk', 'requests'])")
    print("# 按优先级尝试，第一个成功的返回")


def demo_backend_type():
    """演示 BackendType 枚举"""
    print("\n" + "=" * 60)
    print("BackendType 枚举示例")
    print("=" * 60)

    # 创建枚举
    print("\n--- 基本用法 ---")
    backend = BackendType.REQUESTS
    print(f"BackendType.REQUESTS = {backend.value}")
    print(f"is_async: {backend.is_async()}")
    print(f"is_sdk: {backend.is_sdk()}")

    # 从字符串解析
    print("\n--- 从字符串解析 ---")
    aliases = ["requests", "http", "sync", "aiohttp", "async",
               "openai_sdk", "openai", "native_sdk", "sdk"]
    for alias in aliases:
        try:
            parsed = BackendType.from_string(alias)
            print(f"  '{alias}' -> {parsed.value}")
        except ValueError as e:
            print(f"  '{alias}' -> 错误: {e}")


def demo_priority_resolution():
    """演示优先级解析"""
    print("\n" + "=" * 60)
    print("Backend 解析优先级")
    print("=" * 60)

    print("""
优先级（从高到低）：

1. Builder/便捷函数 显式指定 backend= 参数
   client = create_client('deepseek', 'openai_sdk')

2. YAML 配置中该厂商的 backend 字段
   providers:
     deepseek:
       backend: openai_sdk

3. 代码 set_default_backend() 设置的全局默认
   set_default_backend('openai_sdk')

4. 环境变量 LLM_BACKEND
   export LLM_BACKEND=openai_sdk

5. YAML 配置中的 default_backend 字段
   default_backend: openai_sdk

6. 兜底值: requests（同步）/ aiohttp（异步）
""")


if __name__ == "__main__":
    demo_one_click_config()
    demo_builder_pattern()
    demo_convenience_functions()
    demo_backend_switcher()
    demo_backend_type()
    demo_priority_resolution()

    print("\n" + "=" * 60)
    print("所有示例演示完成！")
    print("=" * 60)
    print("\n提示：实际调用 LLM 需要有效的 API 密钥")
    print("      本示例仅展示 API 用法，未实际调用 LLM")
