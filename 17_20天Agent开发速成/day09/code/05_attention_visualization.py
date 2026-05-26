
# -*- coding: utf-8 -*-
"""
Day09 代码示例 05: 注意力可视化（概念演示）
"""

import numpy as np
import sys
import io

# 处理 Windows 编码问题
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# 1. 简单的热力图可视化（文本版）
def visualize_attention_text(attention_weights, tokens):
    """
    文本版注意力可视化
    
    Args:
        attention_weights: (seq_len, seq_len)
        tokens: token 列表
    """
    seq_len = len(tokens)
    
    print(f"\n📊 注意力热力图:")
    print(f"   " + " ".join([f"{token:>4}" for token in tokens]))
    print(f"   " + " " * 4 + "-" * (5 * seq_len))
    
    for i in range(seq_len):
        row_str = f"{tokens[i]:>4} |"
        for j in range(seq_len):
            w = attention_weights[i, j]
            # 用字符表示权重大小
            if w > 0.7:
                char = "█"
            elif w > 0.5:
                char = "▓"
            elif w > 0.3:
                char = "▒"
            elif w > 0.1:
                char = "░"
            else:
                char = "·"
            row_str += f" {char:^3}"
        print(row_str)


# 2. 连线可视化
def visualize_attention_lines(attention_weights, tokens, threshold=0.3):
    """
    文本版连线可视化
    
    Args:
        attention_weights: (seq_len, seq_len)
        tokens: token 列表
        threshold: 只显示权重大于阈值的
    """
    print(f"\n🔗 注意力连线 (阈值 = {threshold}):")
    
    for i in range(len(tokens)):
        print(f"\n   '{tokens[i]}' 关注:")
        for j in range(len(tokens)):
            w = attention_weights[i, j]
            if w > threshold and i != j:
                print(f"     → '{tokens[j]}' (权重: {w:.3f})")


# 3. 模拟注意力模式
def create_demo_attention():
    """创建演示用的注意力模式"""
    seq_len = 4
    tokens = ["我", "爱", "北京", "天安门"]
    
    # 模拟模式 1: 主语-动词
    attention1 = np.array([
        [0.8, 0.2, 0.0, 0.0],  # "我" 主要关注自己
        [0.6, 0.3, 0.1, 0.0],  # "爱" 关注主语 "我"
        [0.1, 0.5, 0.3, 0.1],  # "北京" 关注动词 "爱"
        [0.0, 0.1, 0.6, 0.3],  # "天安门" 关注 "北京"
    ])
    
    # 模拟模式 2: 指代关系
    attention2 = np.array([
        [0.7, 0.2, 0.1, 0.0],
        [0.2, 0.6, 0.2, 0.0],
        [0.0, 0.2, 0.7, 0.1],
        [0.0, 0.0, 0.2, 0.8],
    ])
    
    return tokens, attention1, attention2


# 4. 演示
if __name__ == "__main__":
    print("="*60)
    print("注意力可视化（概念演示）")
    print("="*60)
    
    tokens, attn1, attn2 = create_demo_attention()
    
    print(f"\n📝 Token 序列: {' '.join(tokens)}")
    
    # 模式 1
    print(f"\n" + "="*60)
    print("模式 1: 主语-动词-宾语关系")
    print("="*60)
    visualize_attention_text(attn1, tokens)
    visualize_attention_lines(attn1, tokens)
    
    # 模式 2
    print(f"\n" + "="*60)
    print("模式 2: 局部相邻关系")
    print("="*60)
    visualize_attention_text(attn2, tokens)
    visualize_attention_lines(attn2, tokens)
    
    # 总结
    print(f"\n" + "="*60)
    print("💡 可观察到的模式:")
    print("="*60)
    print(f"  1. 语法关系: 主语 ↔ 动词 ↔ 宾语")
    print(f"  2. 指代关系: 代词关注它指代的名词")
    print(f"  3. 位置模式: 注意力集中在相邻词")
    print(f"  4. 头的分工: 不同头关注不同模式")
    
    print("\n🎉 注意力可视化示例完成!")
