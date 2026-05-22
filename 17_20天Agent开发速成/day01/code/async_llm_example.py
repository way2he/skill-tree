# -*- coding: utf-8 -*-
"""
异步 LLM 客户端使用示例
演示如何使用异步 LLM 客户端调用各种大模型
"""

import asyncio
import sys

sys.path.insert(0, "../../")


async def example_basic_usage():
    """基础使用示例"""
    print("=" * 60)
    print("示例1: 基础使用")
    print("=" * 60)

    from llm.aiohttp import create_async_llm_client

    # 创建 Ollama 客户端（本地模型，无需 API Key）
    try:
        client = create_async_llm_client("ollama", model="qwen3.5:9b")
        print(f"正在使用 Ollama 客户端，模型: {client.model}")
        print("注意: 请确保 Ollama 服务正在运行，且已下载 qwen3.5:9b 模型")
    except Exception as e:
        print(f"创建客户端失败: {e}")
        print("\n提示: Ollama 示例需要本地运行 Ollama 服务")
        print("你可以尝试其他示例或配置 API Key 使用云服务")


async def example_concurrent_calls():
    """并发调用示例"""
    print("\n" + "=" * 60)
    print("示例2: 并发调用（演示异步能力）")
    print("=" * 60)

    from llm.aiohttp import async_llm_generate

    # 这个示例演示并发能力，但我们不实际调用 API
    # 因为需要 API Key
    print("并发调用示例（模拟）:")
    print("""
import asyncio
from llm.aiohttp import async_llm_generate

async def call_model(prompt, provider):
    return await async_llm_generate(prompt, provider=provider, ...)

async def main():
    # 并发调用多个模型
    tasks = [
        call_model("你好", "openai"),
        call_model("你好", "doubao"),
        call_model("你好", "qwen"),
    ]
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)
""")


async def example_json_generation():
    """JSON 生成示例"""
    print("\n" + "=" * 60)
    print("示例3: 生成结构化 JSON")
    print("=" * 60)

    from llm.aiohttp import async_llm_generate_json
    from pydantic import BaseModel

    # 定义输出格式
    class User(BaseModel):
        name: str
        age: int
        email: str

    print("使用 Pydantic 模型定义输出格式:")
    print("class User(BaseModel):")
    print("    name: str")
    print("    age: int")
    print("    email: str")

    print("\n使用示例:")
    print("""
from llm.aiohttp import async_generate_from_pydantic

result = await async_generate_from_pydantic(
    "生成一个随机用户信息",
    model_class=User,
    provider="ollama"
)
if result:
    print(f"姓名: {result.name}")
    print(f"年龄: {result.age}")
    print(f"邮箱: {result.email}")
""")


async def example_all_providers():
    """所有支持的提供商"""
    print("\n" + "=" * 60)
    print("示例4: 支持的所有提供商")
    print("=" * 60)

    providers = [
        ("ollama", "本地模型，无需 API Key", "OLLAMA"),
        ("openai", "OpenAI / GPT", "OPENAI_API_KEY"),
        ("anthropic", "Anthropic / Claude", "ANTHROPIC_API_KEY"),
        ("doubao", "火山引擎 / 豆包", "VOLCENGINE_API_KEY"),
        ("qwen", "阿里云 / 通义千问", "DASHSCOPE_API_KEY"),
        ("glm", "智谱 AI / GLM", "ZHIPUAI_API_KEY"),
        ("wenxin", "百度 / 文心一言", "BAIDU_ACCESS_TOKEN"),
        ("kimi", "月之暗面 / Kimi", "MOONSHOT_API_KEY"),
        ("deepseek", "深度求索 / DeepSeek", "DEEPSEEK_API_KEY"),
        ("minimax", "MiniMax", "MINIMAX_API_KEY"),
        ("xai", "xAI / Grok", "XAI_API_KEY"),
        ("cohere", "Cohere", "COHERE_API_KEY"),
        ("hunyuan", "腾讯云混元", "TENCENT_HUNYUAN_API_KEY"),
        ("pangu", "华为云盘古", "HUAWEI_API_KEY"),
        ("mistral", "Mistral AI", "MISTRAL_API_KEY"),
        ("together", "Together.ai（开源模型平台）", "TOGETHER_API_KEY"),
        ("milm", "小米小爱大模型", "XIAOMI_API_KEY"),
    ]

    for provider, description, env_var in providers:
        print(f"\n{provider.upper()}: {description}")
        print(f"  环境变量: {env_var}")


async def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("异步 LLM 客户端示例")
    print("=" * 60)

    await example_basic_usage()
    await example_concurrent_calls()
    await example_json_generation()
    await example_all_providers()

    print("\n" + "=" * 60)
    print("快速开始:")
    print("=" * 60)
    print("""
1. 安装依赖:
   pip install -e .

2. 使用 Ollama（推荐本地测试）:
   - 下载并安装 Ollama: https://ollama.com
   - 拉取模型: ollama pull qwen3.5:9b
   - 运行示例

3. 使用云服务:
   - 设置相应的环境变量（如 OPENAI_API_KEY）
   - 选择对应的 provider
   - 调用 API
""")


if __name__ == "__main__":
    asyncio.run(main())
