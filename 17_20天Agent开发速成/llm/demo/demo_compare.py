# -*- coding: utf-8 -*-
"""
零配置多厂商对比 Demo —— 同一个问题，多家模型横向对照

底层已封装 apikey 取值，这里只列出想对比的提供商名字即可。

运行：
    cd 17_20天Agent开发速成
    python -m llm.demo.demo_compare
    python -m llm.demo.demo_compare "解释一下 RAG 中的 Rerank"
"""

import sys
import io
import time
import traceback

if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from llm.core import create_llm


# 想对比哪几家就列哪几家，环境变量缺失的会自动跳过
PROVIDERS = [
    "deepseek",
    "qwen",
    "glm",
    "kimi",
    "doubao",
    # "openai",
    # "anthropic",
]


def run_one(provider: str, prompt: str) -> dict:
    """跑单家，返回结果字典"""
    t0 = time.time()
    try:
        llm = create_llm(provider)            # ← 零配置
        resp = llm.generate_with_response(prompt)
        return {
            "provider": provider,
            "model": resp.model,
            "content": resp.content,
            "latency_ms": resp.latency_ms or int((time.time() - t0) * 1000),
            "tokens": resp.total_tokens,
            "ok": True,
        }
    except Exception as e:
        return {
            "provider": provider,
            "ok": False,
            "error": f"{type(e).__name__}: {e}",
        }


def main() -> None:
    prompt = sys.argv[1] if len(sys.argv) > 1 else "用一句话解释 Function Calling"

    print(f"📝 问题：{prompt}")
    print(f"🎯 对比厂商：{PROVIDERS}\n")

    results = [run_one(p, prompt) for p in PROVIDERS]

    # 简洁报告
    print("=" * 70)
    for r in results:
        head = f"【{r['provider']}】"
        if not r["ok"]:
            print(f"{head} ❌ {r['error']}\n")
            continue
        print(f"{head} ✅ {r['model']}  |  {r['latency_ms']} ms  |  {r['tokens']} tokens")
        print(f"{r['content']}\n")

    # 速度排行
    ok = [r for r in results if r["ok"]]
    if ok:
        ok.sort(key=lambda x: x["latency_ms"] or 9e9)
        print("=" * 70)
        print("🏁 速度排行：")
        for i, r in enumerate(ok, 1):
            print(f"  {i}. {r['provider']:10s} {r['latency_ms']:>6} ms")


if __name__ == "__main__":
    main()
