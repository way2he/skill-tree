
# -*- coding: utf-8 -*-
"""
Day08 代码示例 05: 预训练模型三大家族对比
"""

import sys
import io

# 处理 Windows 编码问题
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# 1. 模型家族对比表格
print("="*80)
print("预训练模型三大家族对比")
print("="*80)

model_families = [
    {
        "name": "BERT 家族",
        "architecture": "Encoder-only",
        "attention": "双向",
        "strengths": "上下文理解能力强",
        "weaknesses": "不适合长文本生成",
        "use_cases": "文本分类、NER、信息抽取",
        "examples": ["BERT", "RoBERTa", "ALBERT", "DistilBERT"]
    },
    {
        "name": "GPT 家族",
        "architecture": "Decoder-only",
        "attention": "单向（自回归）",
        "strengths": "文本生成能力强",
        "weaknesses": "只能看到上文",
        "use_cases": "写作、对话、代码生成",
        "examples": ["GPT-2/3/4", "LLaMA", "Mistral", "Qwen"]
    },
    {
        "name": "T5 家族",
        "architecture": "Encoder-Decoder",
        "attention": "编码双向 + 解码单向",
        "strengths": "统一框架，灵活通用",
        "weaknesses": "参数量通常较大",
        "use_cases": "翻译、摘要、多任务",
        "examples": ["T5", "FLAN-T5", "UL2"]
    }
]

for family in model_families:
    print(f"\n🔷 {family['name']}")
    print(f"  架构: {family['architecture']}")
    print(f"  注意力: {family['attention']}")
    print(f"  优势: {family['strengths']}")
    print(f"  局限: {family['weaknesses']}")
    print(f"  适用: {family['use_cases']}")
    print(f"  代表: {', '.join(family['examples'])}")


# 2. 架构图示
print("\n" + "="*80)
print("模型架构图示")
print("="*80)

print("\n📐 BERT (Encoder-only):")
print("""
  [CLS]  今天  天气  真好  [SEP]
    ↓     ↓     ↓     ↓     ↓
  ┌───────────────────────────┐
  │   双向注意力 (都能看到)   │
  └───────────────────────────┘
    ↓     ↓     ↓     ↓     ↓
  [CLS]  今天  天气  真好  [SEP]
  (用于分类) (用于 Token 级任务)
""")

print("\n📐 GPT (Decoder-only):")
print("""
  今天  天气  真好  。
    ↓     ↓     ↓     ↓
  ┌───────────────────────┐
  │  单向注意力 (只看前面) │
  └───────────────────────┘
    ↓     ↓     ↓     ↓
  今天  天气  真好  。
              (自回归生成)
""")

print("\n📐 T5 (Encoder-Decoder):")
print("""
  ┌─────────────────────────────────────┐
  │  输入: 翻译 英→中: Hello            │
  └──────────────┬──────────────────────┘
                 ↓
         ┌───────────────┐
         │    编码器     │ (双向注意力)
         └───────┬───────┘
                 ↓
         ┌───────────────┐
         │    解码器     │ (单向注意力)
         └───────┬───────┘
                 ↓
  ┌─────────────────────────────────────┐
  │  输出: 你好                          │
  └─────────────────────────────────────┘
""")


# 3. 选型建议
print("\n" + "="*80)
print("选型建议")
print("="*80)

use_cases = [
    ("文本分类、情感分析", "BERT/RoBERTa"),
    ("命名实体识别 (NER)", "BERT/RoBERTa"),
    ("信息抽取", "BERT/RoBERTa"),
    ("文本生成、写作", "GPT/LLaMA"),
    ("对话系统", "GPT/LLaMA"),
    ("代码生成", "GPT/CodeLLaMA"),
    ("机器翻译", "T5/FLAN-T5"),
    ("文本摘要", "T5/FLAN-T5"),
    ("多任务统一系统", "T5/FLAN-T5"),
]

print("\n📋 任务-模型映射:")
for task, model in use_cases:
    print(f"  {task:<25} → {model}")


# 4. T5 的 Text-to-Text 示例
print("\n" + "="*80)
print("T5 Text-to-Text 示例")
print("="*80)

t5_examples = [
    {
        "task": "文本分类",
        "input": "分类: 这部电影真的很好看！",
        "output": "正面"
    },
    {
        "task": "情感分析",
        "input": "情感: 今天心情很差",
        "output": "负面"
    },
    {
        "task": "翻译",
        "input": "翻译 英→中: How are you?",
        "output": "你好吗？"
    },
    {
        "task": "摘要",
        "input": "摘要: [长文...]",
        "output": "[摘要...]"
    },
    {
        "task": "问答",
        "input": "问答: 中国首都是哪里？",
        "output": "北京"
    },
]

for example in t5_examples:
    print(f"\n📝 {example['task']}:")
    print(f"   输入: {example['input']}")
    print(f"   输出: {example['output']}")


print("\n🎉 预训练模型三大家族对比完成!")
print("\n💡 总结:")
print("  • 理解类任务 → BERT")
print("  • 生成类任务 → GPT")
print("  • 灵活统一 → T5")
