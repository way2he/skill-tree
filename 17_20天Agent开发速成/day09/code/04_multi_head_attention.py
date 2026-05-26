
# -*- coding: utf-8 -*-
"""
Day09 代码示例 04: 多头注意力
"""

import numpy as np
import sys
import io

# 处理 Windows 编码问题
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# 1. 辅助函数
def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)


# 2. 单头自注意力
def single_head_attention(Q, K, V, mask=None):
    d_k = Q.shape[-1]
    scores = np.matmul(Q, K.swapaxes(-2, -1)) / np.sqrt(d_k)
    if mask is not None:
        scores = np.where(mask == 0, -1e9, scores)
    weights = softmax(scores)
    return np.matmul(weights, V), weights


# 3. 多头注意力
def multi_head_attention(Q, K, V, num_heads=2, mask=None):
    """
    多头注意力实现
    
    Args:
        Q, K, V: 输入
        num_heads: 头数
    """
    batch_size, seq_len, d_model = Q.shape
    d_k = d_model // num_heads
    
    print(f"\n🔢 多头注意力计算步骤 (num_heads={num_heads}):")
    print(f"   d_model: {d_model}, d_k: {d_k}")
    
    # 步骤 1: 分头
    print(f"\n1️⃣  步骤 1: 将 Q/K/V 分成 {num_heads} 个头")
    Q = Q.reshape(batch_size, seq_len, num_heads, d_k).swapaxes(1, 2)
    K = K.reshape(batch_size, seq_len, num_heads, d_k).swapaxes(1, 2)
    V = V.reshape(batch_size, seq_len, num_heads, d_k).swapaxes(1, 2)
    print(f"   Q shape after split: {Q.shape}")
    
    # 步骤 2: 每个头计算自注意力
    print(f"\n2️⃣  步骤 2: 每个头独立计算自注意力")
    outputs = []
    all_weights = []
    for h in range(num_heads):
        print(f"\n   头 {h + 1}:")
        head_output, head_weights = single_head_attention(
            Q[:, h], K[:, h], V[:, h], mask
        )
        outputs.append(head_output)
        all_weights.append(head_weights)
        print(f"      输出 shape: {head_output.shape}")
    
    # 步骤 3: 拼接
    print(f"\n3️⃣  步骤 3: 拼接所有头的结果")
    outputs = np.stack(outputs, axis=1)
    concat_output = outputs.swapaxes(1, 2).reshape(batch_size, seq_len, -1)
    print(f"   拼接后 shape: {concat_output.shape}")
    
    # 步骤 4: 线性投影（这里简化，直接拼接作为输出）
    final_output = concat_output  # 简化，实际还需要线性层
    
    return final_output, all_weights


# 4. 测试多头注意力
if __name__ == "__main__":
    print("="*60)
    print("多头注意力实现 (NumPy 版本)")
    print("="*60)
    
    # 参数
    batch_size = 1
    seq_len = 3
    d_model = 8
    num_heads = 2
    
    print(f"\n📊 测试参数:")
    print(f"   batch_size: {batch_size}")
    print(f"   seq_len: {seq_len}")
    print(f"   d_model: {d_model}")
    print(f"   num_heads: {num_heads}")
    
    # 随机输入
    np.random.seed(42)
    Q = np.random.randn(batch_size, seq_len, d_model).astype(np.float32)
    K = Q.copy()
    V = Q.copy()
    
    print(f"\n📥 输入 Q (前 4 个维度):")
    print(Q[:, :, :4])
    
    # 计算多头注意力
    output, head_weights = multi_head_attention(Q, K, V, num_heads=num_heads)
    
    print(f"\n✅ 多头注意力计算完成!")
    print(f"\n📤 输出 shape: {output.shape}")
    print(f"   输出 (前 4 个维度):")
    print(output[:, :, :4])
    
    print(f"\n🔍 每个头的注意力模式:")
    tokens = ["我", "爱", "你"]
    for h in range(num_heads):
        print(f"\n   头 {h + 1}:")
        for i in range(seq_len):
            print(f"     '{tokens[i]}': ", end="")
            for j in range(seq_len):
                w = head_weights[h][0, i, j]
                print(f"[{tokens[j]}: {w:.2f}] ", end="")
            print()
    
    print("\n🎉 多头注意力示例完成!")
