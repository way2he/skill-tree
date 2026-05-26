# -*- coding: utf-8 -*-
"""
llm/core 配置驱动 Demo —— 从 YAML 加载并支持降级 / 多厂商切换

前置：
1. 设置好 .env 或 shell 环境变量（DEEPSEEK_API_KEY / ANTHROPIC_API_KEY 等）
2. llm/core/llm_config.yaml 已存在

运行：
    python -m llm.demo.demo_config
"""

import os
import sys
import io
import asyncio
from pathlib import Path

if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# 将项目根目录加入 Python 模块搜索路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from llm.core import (
    create_llm_from_config,
    create_llm_async_from_config,
    load_config,
)

CONFIG_PATH = Path(__file__).parent.parent / "core" / "llm_config.yaml"


def main():
    # 1. 先看一眼解析后的配置（方便排查环境变量是否替换成功）
    cfg = load_config(str(CONFIG_PATH))
    print("【默认厂商】", cfg.default_provider)
    print("【厂商列表】", list(cfg.providers.keys()))
    print("【降级链】 ", cfg.resilience.fallback_providers)

    # 2. 用默认厂商创建（YAML 里 default_provider: local，对应 ollama）
    #    如果本机没装 ollama，传 provider_name 显式切换
    provider = os.getenv("DEMO_PROVIDER", "local")
    llm = create_llm_from_config(str(CONFIG_PATH), provider_name=provider)

    # 3. 像普通对象一样调用
    resp = llm.generate_with_response(
        "用三句话总结一下 LangGraph 的核心概念：State / Node / Edge"
    )
    print(f"\n【{provider} 响应】")
    print(resp.content)
    print(f"\n延迟 {resp.latency_ms} ms | tokens {resp.total_tokens}")


async def main_async():
    """异步版：覆盖 create_llm_async_from_config"""
    provider = os.getenv("DEMO_PROVIDER", "local")
    llm = create_llm_async_from_config(str(CONFIG_PATH), provider_name=provider)
    text = await llm.generate("用一句话介绍你自己")
    print(f"\n【异步 {provider}】 {text}")


if __name__ == "__main__":
    main()
    if any(a in ("--async", "-a") for a in sys.argv[1:]):
        asyncio.run(main_async())
