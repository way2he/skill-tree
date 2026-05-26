# -*- coding: utf-8 -*-
"""
demo 自测（ollama + requests）—— 最小集合

慢机器友好版：每项 timeout=300s，prompt 强约束 ≤ 10 字。
"""

import os
import sys
import io
import subprocess
import time
from pathlib import Path

if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

os.environ["LLM_PROVIDER"] = "ollama"
os.environ["LLM_BACKEND"] = "requests"
os.environ.setdefault("LLM_MODEL", "qwen3.5:9b")

ROOT = Path(__file__).resolve().parent.parent.parent
PROMPT = "回答一个字：好"


def run(name: str, args: list[str], timeout: int = 300) -> dict:
    cmd = [sys.executable, "-X", "utf8", "-u", "-m", f"llm.demo.{name}", *args]
    t0 = time.time()
    try:
        proc = subprocess.run(
            cmd, cwd=ROOT, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=timeout,
            env={**os.environ},
        )
        dur = time.time() - t0
        out = proc.stdout or ""
        err = proc.stderr or ""
        lines = [ln for ln in out.splitlines() if ln.strip()]
        tail = "\n".join(lines[-6:]) if lines else "(空输出)"
        return {
            "name": name, "args": args, "ok": proc.returncode == 0,
            "code": proc.returncode, "dur": dur, "tail": tail,
            "err_tail": "\n".join(err.splitlines()[-3:]) if err.strip() else "",
        }
    except subprocess.TimeoutExpired:
        return {"name": name, "args": args, "ok": False, "code": -1,
                "dur": timeout, "tail": "TIMEOUT", "err_tail": ""}


TESTS_OFFLINE = [
    ("demo_zero_config",      ["--list"],                   15),
    ("demo_zero_config",      ["--enum"],                   15),
    ("demo_stream",           ["--list"],                   15),
    ("demo_register",         [],                           60),
    ("demo_resilience_full",  [],                           60),
    ("demo_backend_selector", [],                           30),
    ("demo_backend_async",    [],                           30),
]

TESTS_ONLINE = [
    ("demo_zero_config",      [PROMPT],                    300),
    ("demo_stream",           ["ollama", PROMPT],          300),
    ("demo_stream",           ["ollama", PROMPT, "--async"], 300),
    ("demo_basic",            [],                          300),
    ("demo_json",             [],                          300),
]


def run_batch(tests, label: str):
    print(f"\n{'='*70}\n📦 {label}（{len(tests)} 项）\n{'='*70}")
    results = []
    for i, (name, args, to) in enumerate(tests, 1):
        argstr = " ".join(args) if args else "(空)"
        print(f"\n[{i:2}/{len(tests)}] {name} {argstr}")
        r = run(name, args, timeout=to)
        results.append(r)
        flag = "✅" if r["ok"] else "❌"
        print(f"        {flag} code={r['code']}  dur={r['dur']:.1f}s")
        if r["tail"]:
            for ln in r["tail"].splitlines()[-3:]:
                print(f"        | {ln[:120]}")
        if r["err_tail"] and not r["ok"]:
            for ln in r["err_tail"].splitlines()[-2:]:
                print(f"        E {ln[:120]}")
    return results


def main():
    print(f"📦 ROOT     : {ROOT}")
    print(f"🎯 provider : {os.environ['LLM_PROVIDER']}")
    print(f"🔧 backend  : {os.environ['LLM_BACKEND']}")
    print(f"🤖 model    : {os.environ['LLM_MODEL']}")
    print(f"❓ prompt   : {PROMPT}")

    r1 = run_batch(TESTS_OFFLINE, "离线测试（必通过）")
    r2 = run_batch(TESTS_ONLINE,  "在线测试（真调 ollama）")
    all_r = r1 + r2

    ok = sum(1 for r in all_r if r["ok"])
    print(f"\n{'='*70}\n🎯 总结：{ok}/{len(all_r)} 通过 ({len(r1)} 离线 + {len(r2)} 在线)\n")
    for r in all_r:
        flag = "✅" if r["ok"] else "❌"
        argstr = " ".join(r["args"]) if r["args"] else "(空)"
        print(f"  {flag} {r['name']:24s} {argstr:30s} ({r['dur']:5.1f}s)")


if __name__ == "__main__":
    main()
