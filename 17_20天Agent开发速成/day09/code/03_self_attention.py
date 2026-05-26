
# -*- coding: utf-8 -*-
"""
Day09 代码示例 03: 自注意力实现
"""

import numpy as np
import sys
import io

# 处理 Windows 编码问题
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# 1. Softmax 函数
def softmax(x):
    """Softmax 函数"""
    # 减去最大值防止溢出
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)


# 2. 自注意力实现
def self_attention(Q, K, V, mask=None):
    """
    自注意力实现
    
    Args:
        Q: Query, shape (batch, seq_len, d_k)
        K: Key, shape (batch, seq_len, d_k)
        V: Value, shape (batch, seq_len, d_v)
        mask: Mask, shape (batch, seq_len, seq_len)
    
    Returns:
        output: 输出, shape (batch, seq_len, d_v)
        attention_weights: 注意力权重
    """
    d_k = Q.shape[-1]
    
    print(f"\n🔢 自注意力计算步骤:")
    print(f"   Q shape: {Q.shape}")
    print(f"   K shape: {K.shape}")
    print(f"   V shape: {V.shape}")
    
    # 步骤 1: Q × K^T
    print(f"\n1️⃣  步骤 1: Q × K^T")
    scores = np.matmul(Q, K.swapaxes(-2, -1))
    print(f"   Scores shape: {scores.shape}")
    print(f"   Scores:\n{scores}")
    
    # 步骤 2: 缩放 / √d_k
    print(f"\n2️⃣  步骤 2: 缩放 / √d_k (d_k = {d_k})")
    scores = scores / np.sqrt(d_k)
    print(f"   Scaled scores:\n{scores}")
    
    # 步骤 3: Mask (可选)
    if mask is not None:
        print(f"\n3️⃣  步骤 3: 应用 Mask")
        scores = np.where(mask == 0, -1e9, scores)
        print(f"   Masked scores:\n{scores}")
    
    # 步骤 4: Softmax
    print(f"\n4️⃣  步骤 4: Softmax")
    attention_weights = softmax(scores)
    print(f"   Attention weights:\n{attention_weights}")
    
    # 步骤 5: × V
    print(f"\n5️⃣  步骤 5: × V")
    output = np.matmul(attention_weights, V)
    print(f"   Output shape: {output.shape}")
    print(f"   Output:\n{output}")
    
    return output, attention_weights


# 3. 测试自注意力
if __name__ == "__main__":
    print("="*60)
    print("自注意力实现 (NumPy 版本)")
    print("="*60)
    
    # 创建一个简单的例子
    batch_size = 1
    seq_len = 3
    d_k = 4
    d_v = 4
    
    print(f"\n📊 测试参数:")
    print(f"   batch_size: {batch_size}")
    print(f"   seq_len: {seq_len}")
    print(f"   d_k: {d_k}")
    print(f"   d_v: {d_v}")
    
    # 模拟输入（简单起见，让 Q/K/V 相同）
    Q = np.array([[
        [1, 0, 1, 0],  # "我"
        [0, 1, 0, 1],  # "爱"
        [1, 1, 1, 1]   # "你"
    ]], dtype=np.float32)
    
    K = Q.copy()
    V = Q.copy()
    
    print(f"\n📥 输入 Q/K/V:")
    print(Q)
    
    # 计算自注意力
    output, weights = self_attention(Q, K, V)
    
    print(f"\n✅ 自注意力计算完成!")
    print(f"\n📊 注意力权重可视化:")
    tokens = ["我", "爱", "你"]
    for i in range(seq_len):
        print(f"\n   '{tokens[i]}' 的注意力:")
        for j in range(seq_len):
            print(f"     → '{tokens[j]}': {weights[0, i, j]:.4f}")
    
    print(f"\n📤 最终输出:")
    print(output)
    
    print("\n🎉 自注意力示例完成!")
