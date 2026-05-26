
# -*- coding: utf-8 -*-
"""
Day14 Code 05: LoRA 微调完整流程（概念演示）
"""

print("=" * 60)
print("Day14 - LoRA 微调完整流程")
print("=" * 60)


def print_section(title: str):
    print(f"\n{'='*60}")
    print(f"📚 {title}")
    print(f"{'='*60}")


print_section("1. 理解 LoRA 原理")
print("""
LoRA = Low-Rank Adaptation（低秩适应）

原模型参数（冻结）: W (大矩阵，不训练)
新增小参数（训练）: A × B (两个小矩阵，低秩)
最终输出: W + A × B

为什么有效？
- 预训练模型已经有很多知识了
- 只需要少量参数来适应新任务
- 低秩矩阵足以捕捉任务特定的变化
""")

print_section("2. 关键超参数")
print("""
r (Rank): 低秩的维度
  - 越小: 参数越少，效果可能稍差
  - 越大: 参数越多，效果越好，但显存也越大
  - 推荐值: 8, 16, 32, 64

lora_alpha: 缩放系数
  - 通常设为 r 的 2 倍
  - 推荐值: 16, 32, 64

target_modules: 目标层
  - 通常选注意力层
  - 推荐: ["q_proj", "v_proj"]

lora_dropout: 防止过拟合
  - 推荐: 0.05-0.1
""")

print_section("3. 完整流程")
print("""
步骤 1: 准备数据
  - 收集或标注任务相关的数据
  - 格式: 指令 (prompt) + 回答 (completion)

步骤 2: 加载基础模型
  - 可以用 INT4/INT8 量化加载，节省显存
  - 用 QLoRA 的话，7B 模型在 8GB 显存就能跑

步骤 3: 配置 LoRA
  - 选择 r, lora_alpha, target_modules
  - 用 PEFT 库的 LoraConfig

步骤 4: 训练
  - 只训练 LoRA 参数，冻结原模型
  - 用 SFTTrainer (Hugging Face)

步骤 5: 保存
  - LoRA adapter 只有几十 MB！
  - 保存为: adapter_model/

步骤 6: 推理
  - 加载原模型 + LoRA adapter
  - 合并推理，或分别加载
""")

print_section("4. LoRA vs 全量微调对比")
print("""
指标          LoRA                全量微调
-----------------------------------------------------
显存需求      很小 (10-20%)       很大 (100%)
训练时间      短                  长
存储需求      小 (几十MB)         大 (完整模型)
效果          接近全量            最好
通用性        可以在不同任务间切换  每次都要重新训练
""")

print_section("5. 代码示意")
print("""
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM

# 1. 配置 LoRA
lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    task_type="CAUSAL_LM"
)

# 2. 加载模型，应用 LoRA
model = AutoModelForCausalLM.from_pretrained("base_model")
model = get_peft_model(model, lora_config)

# 3. 打印可训练参数（会发现只有很少！）
model.print_trainable_parameters()

# 4. 训练后，保存 LoRA adapter
model.save_pretrained("my_lora_adapter")

# 5. 推理时加载
from peft import PeftModel

model = AutoModelForCausalLM.from_pretrained("base_model")
model = PeftModel.from_pretrained(model, "my_lora_adapter")
""")

print("\n" + "=" * 60)
print("✅ LoRA 微调完整流程演示完成！")
print("=" * 60)
print("\n总结:")
print("- LoRA 是现在最流行的微调方式")
print("- QLoRA = 量化 + LoRA，更省显存")
print("- LoRA adapter 很小，方便分享和部署")
print("- 效果通常接近全量微调！")

