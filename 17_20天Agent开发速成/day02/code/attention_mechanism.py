# -*- coding: utf-8 -*-
"""
Day02 - 注意力机制极简实现
参考 miniGPT 源码，100行理解注意力核心原理
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class SimpleSelfAttention(nn.Module):
    """
    最简自注意力实现 - 单头
    """

    def __init__(self, d_model: int):
        super().__init__()
        self.d_model = d_model

        # Q, K, V 三个线性投影层
        self.Wq = nn.Linear(d_model, d_model)  # Query 投影
        self.Wk = nn.Linear(d_model, d_model)  # Key 投影
        self.Wv = nn.Linear(d_model, d_model)  # Value 投影

        # 输出投影
        self.Wo = nn.Linear(d_model, d_model)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        x: (batch_size, seq_len, d_model)
        """
        batch_size, seq_len, d_model = x.shape

        # 1. 投影得到 Q, K, V
        Q = self.Wq(x)  # (batch_size, seq_len, d_model)
        K = self.Wk(x)  # (batch_size, seq_len, d_model)
        V = self.Wv(x)  # (batch_size, seq_len, d_model)

        # 2. 计算注意力分数：Q @ K^T / sqrt(d_k)
        # 为什么除以 sqrt(d_k)？防止内积太大导致 softmax 梯度消失
        attention_scores = Q @ K.transpose(-2, -1) / (d_model**0.5)
        # (batch_size, seq_len, seq_len)

        # 3. softmax 归一化得到权重
        attention_weights = F.softmax(attention_scores, dim=-1)
        # (batch_size, seq_len, seq_len)

        # 4. 加权求和得到输出：Attention(Q,K,V) = softmax(QK^T/√d_k) V
        output = attention_weights @ V  # (batch_size, seq_len, d_model)

        # 5. 输出投影
        output = self.Wo(output)

        return output, attention_weights


class MultiHeadAttention(nn.Module):
    """
    多头注意力实现
    """

    def __init__(self, d_model: int, n_heads: int):
        super().__init__()
        assert d_model % n_heads == 0, "d_model 必须能被 n_heads 整除"

        self.d_model = d_model
        self.n_heads = n_heads
        self.d_head = d_model // n_heads  # 每个头的维度

        # Q, K, V 投影（合并成一个矩阵，效率更高）
        self.Wqkv = nn.Linear(d_model, 3 * d_model)

        # 输出投影
        self.Wo = nn.Linear(d_model, d_model)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        x: (batch_size, seq_len, d_model)
        """
        batch_size, seq_len, d_model = x.shape

        # 1. 一次性投影得到 Q, K, V
        qkv = self.Wqkv(x)  # (batch_size, seq_len, 3*d_model)
        Q, K, V = qkv.chunk(3, dim=-1)  # 每个都是 (batch_size, seq_len, d_model)

        # 2. 拆分成多个头
        # (batch_size, seq_len, d_model) -> (batch_size, n_heads, seq_len, d_head)
        Q = Q.view(batch_size, seq_len, self.n_heads, self.d_head).transpose(1, 2)
        K = K.view(batch_size, seq_len, self.n_heads, self.d_head).transpose(1, 2)
        V = V.view(batch_size, seq_len, self.n_heads, self.d_head).transpose(1, 2)

        # 3. 计算注意力分数
        attention_scores = Q @ K.transpose(-2, -1) / (self.d_head**0.5)
        # (batch_size, n_heads, seq_len, seq_len)

        # 4. softmax
        attention_weights = F.softmax(attention_scores, dim=-1)

        # 5. 加权求和
        output = attention_weights @ V  # (batch_size, n_heads, seq_len, d_head)

        # 6. 合并所有头
        output = output.transpose(1, 2).contiguous().view(batch_size, seq_len, d_model)

        # 7. 输出投影
        output = self.Wo(output)

        return output, attention_weights


# ==================== 测试 ====================
if __name__ == "__main__":
    print("=" * 80)
    print("🧠 注意力机制极简实现")
    print("=" * 80)

    # 参数
    d_model = 64  # 模型维度
    n_heads = 4  # 头数
    seq_len = 10  # 序列长度
    batch_size = 2

    # 随机输入
    x = torch.randn(batch_size, seq_len, d_model)
    print(f"\n📥 输入 shape: {x.shape}")
    print(f"   batch_size={batch_size}, seq_len={seq_len}, d_model={d_model}")

    # 测试单头注意力
    print("\n" + "-" * 80)
    print("🔍 测试单头自注意力...")
    single_attention = SimpleSelfAttention(d_model)
    output, weights = single_attention(x)
    print(f"   输出 shape: {output.shape}")
    print(f"   注意力权重 shape: {weights.shape}")
    print(f"   ✅ 单头注意力测试通过！")

    # 测试多头注意力
    print("\n" + "-" * 80)
    print("🔍 测试多头注意力...")
    multi_attention = MultiHeadAttention(d_model, n_heads)
    output, weights = multi_attention(x)
    print(f"   输出 shape: {output.shape}")
    print(f"   注意力权重 shape: {weights.shape} (batch, heads, seq, seq)")
    print(f"   ✅ 多头注意力测试通过！")

    print("\n" + "=" * 80)
    print("💡 核心公式理解：")
    print("   Attention(Q, K, V) = softmax(QK^T / √d_k) * V")
    print("   Q = 查询向量 - 我要找什么")
    print("   K = 键向量   - 我有什么")
    print("   V = 值向量   - 我实际的内容")
    print("   多头 = 并行关注多种不同的语义关系")
    print("=" * 80)
    print("\n🎉 Day02 - 注意力机制原理演示完成！")
