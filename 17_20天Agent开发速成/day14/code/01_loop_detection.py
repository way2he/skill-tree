
# -*- coding: utf-8 -*-
"""
Day14 Code 01: 死循环检测
"""

import time
from collections import deque

print("=" * 60)
print("Day14 - 死循环检测")
print("=" * 60)


class LoopDetector:
    def __init__(self, max_steps=20, timeout=300, history_size=10):
        self.max_steps = max_steps
        self.timeout = timeout
        self.history = deque(maxlen=history_size)
        self.start_time = None
        self.current_step = 0

    def start(self):
        """开始检测"""
        self.start_time = time.time()
        self.current_step = 0
        self.history.clear()

    def check(self, state: str) -&gt; dict:
        """
        检查是否陷入循环

        Returns:
            dict: {
                "should_continue": bool,
                "reason": str,
                "step": int
            }
        """
        self.current_step += 1

        # 1. 检查步数
        if self.current_step &gt; self.max_steps:
            return {
                "should_continue": False,
                "reason": f"超过最大步数 {self.max_steps}",
                "step": self.current_step
            }

        # 2. 检查超时
        if time.time() - self.start_time &gt; self.timeout:
            return {
                "should_continue": False,
                "reason": f"超时 ({self.timeout}秒)",
                "step": self.current_step
            }

        # 3. 检查重复状态
        if state in self.history:
            return {
                "should_continue": False,
                "reason": f"检测到重复状态: {state}",
                "step": self.current_step
            }

        self.history.append(state)

        return {
            "should_continue": True,
            "reason": "正常",
            "step": self.current_step
        }


print("\n[1/2] 初始化循环检测器...")
detector = LoopDetector(
    max_steps=10,
    timeout=60,
    history_size=5
)

print("\n[2/2] 模拟一个可能循环的任务...")
detector.start()

# 模拟一些状态
states = [
    "思考中...",
    "查阅资料...",
    "分析结果...",
    "思考中...",  # 重复了！
    "查阅资料...",
    "最终答案"
]

for i, state in enumerate(states):
    print(f"\n步骤 {i+1}: {state}")
    result = detector.check(state)

    print(f"  检测结果: {result}")

    if not result["should_continue"]:
        print(f"  ❌ 停止: {result['reason']}")
        break
    else:
        print(f"  ✅ 继续...")

print("\n" + "=" * 60)
print("✅ 死循环检测演示完成！")
print("=" * 60)
print("\n总结:")
print("- 可以检测步数超限")
print("- 可以检测超时")
print("- 可以检测重复状态")
print("- 及早发现循环，避免资源浪费")

