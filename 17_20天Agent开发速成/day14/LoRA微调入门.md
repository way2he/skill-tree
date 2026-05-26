
---
name: LoRA微调入门
description: LoRA微调入门
type: learning-material
tags: ["LoRA", "微调", "PEFT"]
summary: LoRA微调入门详解
created_at: 2026-05-26
updated_at: 2026-05-26
version: interview
---

# LoRA 微调入门 🎯

## 什么是 LoRA？

**LoRA = Low-Rank Adaptation（低秩适应）**

在预训练模型旁边加小的"适配器"（Adapter），只训练这些适配器，不修改原模型。

## 为什么用 LoRA？

| 方式 | 显存 | 时间 | 效果 | 存储 |
|------|------|------|------|------|
| **全量微调** | 很大 | 很长 | 好 | 大 |
| **LoRA** | 很小 | 短 | 接近全量 | 小（几十MB） |

## LoRA 核心思想

```
原模型参数（冻结）：W
新增小参数（训练）：A × B （低秩矩阵）
最终输出：W + A × B
```

## 关键参数

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| **r** | Rank（秩） | 8-64 |
| **lora_alpha** | 缩放系数 | 16-64 |
| **lora_dropout** | Dropout | 0-0.1 |
| **target_modules** | 目标层 | ["q_proj", "v_proj"] |

## 代码示例

```python
from peft import LoraConfig, get_peft_model
import torch

# LoRA 配置
lora_config = LoraConfig(
    r=8,  # Rank
    lora_alpha=32,  # 缩放
    target_modules=["q_proj", "v_proj"],  # 目标层
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# 把 LoRA 加到模型上
model = get_peft_model(model, lora_config)

# 打印可训练的参数
model.print_trainable_parameters()
# 输出: trainable params: 3,145,728 || all params: 7,068,928,000 || trainable%: 0.04%
```

## QLoRA = Quantized LoRA

在 LoRA 基础上加量化（INT4），更省显存：

```python
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

model = AutoModelForCausalLM.from_pretrained(
    "model_name",
    quantization_config=bnb_config,
    ...
)
```

---
