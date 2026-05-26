
---
name: KV Cache详解
description: KV Cache详解
type: learning-material
tags: ["KV Cache", "推理加速"]
summary: KV Cache详解
created_at: 2026-05-26
updated_at: 2026-05-26
version: interview
---

# KV Cache 详解 💾

## 什么是 KV Cache？

在 Transformer 模型推理时，缓存之前计算的 Key 和 Value，避免重复计算。

## 工作原理

### 没有 Cache 的情况
```
输入 tokens: [A, B, C, D, E]
每一步都要重新计算所有之前的 KV
```

### 有 Cache 的情况
```
输入 tokens: [A, B, C, D, E]
第一步: 计算 A 的 KV，缓存
第二步: 用 A 的缓存 KV，计算 B 的 KV，缓存
第三步: 用 AB 的缓存 KV，计算 C 的 KV，缓存
...
```

## 效果

| 指标 | 无 Cache | 有 Cache |
|------|---------|---------|
| **计算量** | O(n²) | O(n) |
| **推理速度** | 基准 | 快 2-5 倍 |
| **内存使用** | 基准 | 多一些（存储 KV） |

## 代码示意

```python
kv_cache = None

for i in range(len(tokens)):
    current_token = tokens[i:i+1]

    if kv_cache is not None:
        # 用之前的 KV Cache
        output, kv_cache = model(current_token, kv_cache=kv_cache)
    else:
        # 第一次，计算所有 KV
        output, kv_cache = model(current_token)

    # kv_cache 会被带到下一轮
```

## 常用框架支持

- Hugging Face Transformers: `use_cache=True`
- vLLM: 自动支持
- TensorRT-LLM: 优化支持

---
