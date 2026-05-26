
# -*- coding: utf-8 -*-
"""
Day14 Code 02: KV Cache 概念演示（简化版）
"""

import time
from typing import List, Tuple

print("=" * 60)
print("Day14 - KV Cache 概念演示")
print("=" * 60)


class MockTransformer:
    """模拟的 Transformer 模型"""

    def __init__(self):
        self.computation_count = 0

    def _compute_kv(self, token: str) -&gt; Tuple[List[float], List[float]]:
        """模拟计算 K 和 V"""
        self.computation_count += 1
        # 模拟计算耗时
        time.sleep(0.1)
        # 返回模拟的 KV
        return [hash(token) % 100] * 8, [hash(token + "_v") % 100] * 8

    def generate_without_cache(self, tokens: List[str]) -&gt; List[str]:
        """不使用 KV Cache 的生成"""
        print("\n🚀 不使用 KV Cache:")
        self.computation_count = 0
        start_time = time.time()

        generated = []
        for i in range(len(tokens)):
            # 每次都重新计算所有之前的 KV
            current_tokens = tokens[:i+1]
            print(f"  步骤 {i+1}: 计算 {len(current_tokens)} 个 token 的 KV...")

            for token in current_tokens:
                self._compute_kv(token)

            # 模拟生成下一个 token
            generated.append(f"token_{i}")

        elapsed = time.time() - start_time
        print(f"  ⏱️  耗时: {elapsed:.2f}秒")
        print(f"  🧮  总计算次数: {self.computation_count}")
        return generated

    def generate_with_cache(self, tokens: List[str]) -&gt; List[str]:
        """使用 KV Cache 的生成"""
        print("\n🚀 使用 KV Cache:")
        self.computation_count = 0
        start_time = time.time()

        kv_cache = []
        generated = []

        for i, token in enumerate(tokens):
            print(f"  步骤 {i+1}: ", end="")

            if i == 0:
                print("计算第 1 个 token 的 KV...")
                k, v = self._compute_kv(token)
                kv_cache.append((k, v))
            else:
                print(f"用前 {i} 个的 Cache，计算第 {i+1} 个 token 的 KV...")
                k, v = self._compute_kv(token)
                kv_cache.append((k, v))

            # 模拟生成下一个 token
            generated.append(f"token_{i}")

        elapsed = time.time() - start_time
        print(f"  ⏱️  耗时: {elapsed:.2f}秒")
        print(f"  🧮  总计算次数: {self.computation_count}")
        return generated


print("\n[1/3] 初始化模拟模型...")
model = MockTransformer()

print("\n[2/3] 生成输入 tokens...")
tokens = ["What", "is", "the", "capital", "of", "France", "?"]
print(f"输入 tokens: {tokens}")

print("\n[3/3] 对比两种方式...")
_ = model.generate_without_cache(tokens)
_ = model.generate_with_cache(tokens)

print("\n" + "=" * 60)
print("✅ KV Cache 演示完成！")
print("=" * 60)
print("\n总结:")
print("- 无 Cache: O(n²) 复杂度，n个token需要n²次计算")
print("- 有 Cache: O(n) 复杂度，n个token只需要n次计算")
print("- 对于长文本，Cache 带来的加速非常显著")

