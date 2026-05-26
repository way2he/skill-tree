
---
name: Day14-推理加速+LoRA微调
description: Day14完整学习资料：死循环防护、KV Cache、量化、vLLM、LoRA微调
type: learning-material
tags: ["推理加速", "LoRA", "vLLM", "量化"]
summary: Day14推理加速与LoRA微调完整学习资料
created_at: 2026-05-26
updated_at: 2026-05-26
version: interview
---

# Day14: 推理加速 + LoRA/QLoRA 微调 🚀

&gt; 📅 **学习日期**：2026-05-26  
&gt; ⏰ **总时长**：8 小时  
&gt; 🎯 **验收标准**：能优化模型推理速度，能用 LoRA 微调模型

---

## 今日学习内容清单

| 时间 | 学习内容 | 时长 | 对应文档 |
|------|---------|------|---------|
| **09:00-10:00** | 死循环防护 - 如何避免 Agent 陷入无限循环 | 1h | [死循环防护.md](./死循环防护.md) |
| **10:00-11:00** | KV Cache - 利用缓存加速推理 | 1h | [KV Cache详解.md](./KV Cache详解.md) |
| **11:00-12:00** | 量化推理 - INT8/INT4 量化提升速度 | 1h | [量化推理.md](./量化推理.md) |
| **14:00-15:00** | vLLM - 高性能推理引擎 | 1h | [vLLM实战.md](./vLLM实战.md) |
| **15:00-16:00** | LoRA/QLoRA 微调入门 | 1h | [LoRA微调入门.md](./LoRA微调入门.md) |
| **16:00-17:00** | 代码实战 - LoRA 微调实战 | 1h | [code/01_lora_finetuning.py](./code/01_lora_finetuning.py) |
| **19:00-20:00** | 面试题专项 - Day14 6 道面试题 | 1h | [面试题.md](./面试题.md) |
| **20:00-21:00** | 复盘 + 整理面试话术 | 1h | [今日串讲.md](./今日串讲.md) |

---

## 今日验收标准

### 理论验收
- ✅ 能解释 KV Cache 的工作原理
- ✅ 知道 3 种以上量化技术
- ✅ 能解释 LoRA 的工作原理

### 代码验收
- ✅ 能实现死循环防护逻辑
- ✅ 能配置和使用 vLLM
- ✅ 能用 LoRA/QLoRA 微调一个小模型

---

## 今日核心知识点

### 推理加速技术
- **KV Cache** - 缓存 Key 和 Value，避免重复计算
- **量化** - INT8/INT4 量化，减少内存和计算
- **vLLM** - PagedAttention 技术，高吞吐量推理
- **批处理** - 同时处理多个请求

### 微调技术
- **LoRA** - Low-Rank Adaptation，低秩适应
- **QLoRA** - Quantized LoRA，量化版 LoRA
- **Adapter** - 轻量级微调方法

---

## 今日代码实战

### 代码文件清单
- [code/01_loop_detection.py](./code/01_loop_detection.py) - 死循环检测
- [code/02_kv_cache.py](./code/02_kv_cache.py) - KV Cache 演示
- [code/03_quantization.py](./code/03_quantization.py) - 量化推理
- [code/04_vllm_inference.py](./code/04_vllm_inference.py) - vLLM 推理
- [code/05_lora_finetuning.py](./code/05_lora_finetuning.py) - LoRA 微调

---

## 今日面试考点（6 道）

### 基础题（3 道）
1. 什么是 KV Cache？它如何加速推理？
2. 什么是模型量化？INT8 和 INT4 有什么区别？
3. 什么是 LoRA？它有什么优点？

### 进阶题（3 道）
4. vLLM 的 PagedAttention 是如何工作的？相比传统 Attention 有什么优势？
5. QLoRA 相比 LoRA 有什么改进？它是如何做到既能节省内存又能保持效果的？
6. 在实际项目中，如何选择合适的推理优化技术？请给出一个决策树。

---

**🚀 让我们开始 Day14 的学习！**

