# -*- coding: utf-8 -*-
"""
零配置 Demo —— 调用方完全不写厂商名

调用方代码就一行：
    from llm.core import get_llm
    print(get_llm().generate("你好"))

厂商解析在 llm.core.default 内部完成，优先级：
    LLM_PROVIDER 环境变量 > llm_config.yaml 里 default_provider > "ollama"

apikey 仍由各厂商 XxxClient 自动 os.getenv 取。

运行：
    cd 17_20天Agent开发速成

    # 完全零参数
    set LLM_PROVIDER=deepseek
    set DEEPSEEK_API_KEY=***
    python -m llm.demo.demo_zero_config

    # 临时换厂商问个别问题
    python -m llm.demo.demo_zero_config "解释 ReAct 模式"

    # 看支持哪些厂商
    python -m llm.demo.demo_zero_config --list

    # 枚举入参演示（IDE 能补全）
    python -m llm.demo.demo_zero_config --enum
"""

import sys
import io
from pathlib import Path
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# 将项目根目录加入 Python 模块搜索路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from llm.core import get_llm, current_provider, list_providers, ProviderName


def demo_enum_usage() -> None:
    """演示 ProviderName 枚举用法。不发起真实网络调用，只看类型与缓存。"""
    print("=== ProviderName 枚举完整示例 ===")
    print("枚举总数 :", len(list(ProviderName)))
    print("前 5 个   :", [p.name for p in list(ProviderName)[:5]])
    print("反查名  :", ProviderName.DEEPSEEK.name, "=", ProviderName.DEEPSEEK.value)

    # 三种等价写法命中同一个缓存实例
    a = get_llm(ProviderName.OLLAMA)
    b = get_llm("ollama")
    print("枚举==字符串 同实例?", a is b)

    # 拼写错误立即报错
    try:
        ProviderName("deeppseek")
    except ValueError as e:
        print("拼写错报错:", e)


def main() -> None:
    # --list 子命令
    if len(sys.argv) > 1 and sys.argv[1] in ("--list", "-l", "list"):
        print(f"🎯 当前默认提供商：{current_provider()}")
        print("\n📋 已注册的提供商：")
        for p in list_providers():
            print(f"  - {p}")
        return

    # --enum 子命令：只看枚举用法，不发网络
    if len(sys.argv) > 1 and sys.argv[1] in ("--enum", "-e"):
        demo_enum_usage()
        return

    prompt = sys.argv[1] if len(sys.argv) > 1 else "用一句话介绍你自己"

    # ↓↓↓ 调用方代码就这两行，没有任何厂商名 ↓↓↓
    llm = get_llm()
    resp = llm.generate_with_response(prompt)
    # ↑↑↑

    print(f"🎯 提供商（由 llm.core 解析）：{current_provider()}")
    print(f"📝 模型：{resp.model}\n")
    print(resp.content)
    print(f"\n⏱  {resp.latency_ms} ms  |  🔢 {resp.total_tokens} tokens")


if __name__ == "__main__":
    main()
