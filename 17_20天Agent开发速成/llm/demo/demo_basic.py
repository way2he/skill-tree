# -*- coding: utf-8 -*-
"""
llm/core 最小使用 Demo —— 同步版

运行方式（在 17_20天Agent开发速成/ 目录下）：
    set DEEPSEEK_API_KEY=sk-xxx     # Windows
    export DEEPSEEK_API_KEY=sk-xxx  # macOS/Linux
    python -m llm.demo.demo_basic
"""

import os
import sys
import io

# Windows 控制台中文友好
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from llm.core import create_llm, list_providers


def main():
    # 1. 看看支持哪些厂商
    print("【已注册同步厂商】", list_providers())

    # 2. 创建实例（这里以 DeepSeek 为例，换成 openai/qwen/glm 都行）
    llm = create_llm(
        "deepseek",
        api_key=os.getenv("DEEPSEEK_API_KEY", ""),
        model="deepseek-chat",
    )

    # 3. 简单生成 —— 只要字符串
    text = llm.generate("用一句话解释什么是 Function Calling")
    print("\n【generate 返回】\n", text)

    # 4. 完整响应 —— 拿到 token、延迟、模型名等元数据
    resp = llm.generate_with_response(
        "请用 JSON 输出：{\"answer\": \"...\"}，回答 1+1=?"
    )
    print("\n【generate_with_response 返回】")
    print("  内容    :", resp.content)
    print("  模型    :", resp.model)
    print("  厂商    :", resp.provider)
    print("  延迟(ms):", resp.latency_ms)
    print("  tokens  :", resp.total_tokens)


if __name__ == "__main__":
    main()
