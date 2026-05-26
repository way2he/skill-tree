
# -*- coding: utf-8 -*-
"""
Day14 Code 03: 量化概念演示（内存计算）
"""

print("=" * 60)
print("Day14 - 量化概念演示")
print("=" * 60)


def calculate_model_size(params_count: int, bits: int) -&gt; dict:
    """
    计算模型大小

    Args:
        params_count: 参数数量
        bits: 每个参数的位数
    """
    bytes_per_param = bits / 8
    total_bytes = params_count * bytes_per_param

    return {
        "bits": bits,
        "params": params_count,
        "bytes": total_bytes,
        "MB": total_bytes / (1024 * 1024),
        "GB": total_bytes / (1024 * 1024 * 1024)
    }


print("\n[1/4] 不同大小的模型参数...")
models = {
    "7B": 7_000_000_000,
    "13B": 13_000_000_000,
    "70B": 70_000_000_000
}

print("\n[2/4] 对比不同量化级别...")
print("-" * 80)
print(f"{'模型':&lt;10}{'精度':&lt;10}{'大小 (GB)':&lt;15}{'相对大小':&lt;10}")
print("-" * 80)

for model_name, params in models.items():
    fp32 = calculate_model_size(params, 32)
    fp16 = calculate_model_size(params, 16)
    int8 = calculate_model_size(params, 8)
    int4 = calculate_model_size(params, 4)

    print(f"{model_name:10}FP32      {fp32['GB']:&lt;10.2f}     100%")
    print(f"          FP16      {fp16['GB']:&lt;10.2f}      50%")
    print(f"          INT8      {int8['GB']:&lt;10.2f}      25%")
    print(f"          INT4      {int4['GB']:&lt;10.2f}      12.5%")
    print()

print("\n[3/4] 显存使用对比...")
print("7B 模型:")
print(f"  FP32: ~28 GB  (高端显卡才能跑)")
print(f"  FP16: ~14 GB  (高端显卡)")
print(f"  INT8: ~7 GB   (中端显卡)")
print(f"  INT4: ~3.5 GB (入门显卡都能跑!)")

print("\n[4/4] 量化的权衡...")
print("-" * 80)
print(f"{'量化级别':&lt;15}{'显存节省':&lt;15}{'速度提升':&lt;15}{'质量影响':&lt;15}")
print("-" * 80)
print("FP16          50%             1.5-2x          很小")
print("INT8          75%             2-3x            可接受")
print("INT4          87.5%           3-4x            有一些损失")

print("\n" + "=" * 60)
print("✅ 量化概念演示完成！")
print("=" * 60)
print("\n总结:")
print("- 量化通过减少参数位数来节省显存")
print("- INT4 可以把显存降低到 1/8！")
print("- 轻微的质量损失通常可以接受")
print("- QLoRA = INT4 + LoRA，是现在最流行的方式")

