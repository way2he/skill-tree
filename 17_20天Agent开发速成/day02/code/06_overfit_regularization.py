#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day02 必写代码 6：欠拟合 / 过拟合 / 5 种正则化（ML 概念 + Prompt 工程双重演示）

学习目标：
- 用 PyTorch 一个最小可跑的回归任务，亲眼看到欠拟合 / 过拟合 / 刚好的差异
- 把 L1、L2、Dropout、Early Stopping、Data Augmentation 全部演示一遍
- 同一段代码顺手把每一种正则化 1:1 映射到 Prompt 工程上

面试考点（必背 1 句话答法）：
- 欠拟合：模型太简单，训练/测试都差
- 过拟合：模型太复杂，训练好但测试差
- L1：权重稀疏，自动特征选择（Prompt: 删废话）
- L2：权重平滑，不让某个权重特别大（Prompt: 不走极端、留余地）
- Dropout：训练时随机失活，防止依赖某神经元（Prompt: 示例多样化）
- Early Stopping：验证集不再下降就停（Prompt: 约束够了就停）
- Data Augmentation：增加数据多样性（Prompt: 覆盖各种边界示例）
"""

from __future__ import annotations

import sys
import io
import math
import random
from dataclasses import dataclass
from typing import Callable, List, Tuple

# Windows GBK -> UTF-8 兼容（项目铁律）
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

try:
    import torch
    import torch.nn as nn
    from torch.utils.data import DataLoader, TensorDataset
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    print("⚠️ 未安装 PyTorch，将只演示概念解释 + Prompt 工程映射。")
    print("   安装命令：pip install torch")


# ============================================================
# 0. 通用工具：固定随机种子，结果可复现
# ============================================================
def set_seed(seed: int = 42) -> None:
    random.seed(seed)
    if HAS_TORCH:
        torch.manual_seed(seed)


# ============================================================
# 1. 构造数据：真实函数 y = sin(x) + 噪声
#    - 训练集只有少量点 → 容易过拟合
#    - 测试集是完整曲线 → 用来评估泛化
# ============================================================
def make_dataset(n_train: int = 15, n_test: int = 200, noise: float = 0.25):
    """生成一个一维回归数据集，模拟现实中的小样本场景"""
    if not HAS_TORCH:
        return None
    set_seed(42)
    x_train = torch.linspace(-3, 3, n_train).unsqueeze(1)
    y_train = torch.sin(x_train) + noise * torch.randn_like(x_train)
    x_test = torch.linspace(-3, 3, n_test).unsqueeze(1)
    y_test = torch.sin(x_test)  # 测试集用真值，无噪声
    return x_train, y_train, x_test, y_test


# ============================================================
# 2. 模型定义：故意提供「简单 / 适中 / 复杂」三套
#    - 简单：1 层 4 神经元   → 演示「欠拟合」
#    - 适中：2 层 32 神经元  → 演示「刚好」
#    - 复杂：4 层 256 神经元 → 演示「过拟合」
# ============================================================
if HAS_TORCH:
    class TinyNet(nn.Module):
        """简单模型：必然欠拟合"""
        def __init__(self):
            super().__init__()
            self.net = nn.Sequential(nn.Linear(1, 4), nn.Tanh(), nn.Linear(4, 1))
        def forward(self, x): return self.net(x)

    class MidNet(nn.Module):
        """适中模型 + 可选 Dropout：可以做到刚好拟合"""
        def __init__(self, dropout: float = 0.0):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(1, 32), nn.Tanh(),
                nn.Dropout(dropout),      # ⭐ 正则化方法 3：Dropout
                nn.Linear(32, 32), nn.Tanh(),
                nn.Dropout(dropout),
                nn.Linear(32, 1),
            )
        def forward(self, x): return self.net(x)

    class BigNet(nn.Module):
        """复杂模型：在小数据上必然过拟合"""
        def __init__(self):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(1, 256), nn.Tanh(),
                nn.Linear(256, 256), nn.Tanh(),
                nn.Linear(256, 256), nn.Tanh(),
                nn.Linear(256, 1),
            )
        def forward(self, x): return self.net(x)


# ============================================================
# 3. 训练函数：同时演示 L1、L2、Early Stopping
#    - weight_decay   = L2 正则化（PyTorch 内置）
#    - l1_lambda      = L1 正则化（手写）
#    - early_stop     = 验证集 patience 轮不下降就停
# ============================================================
if HAS_TORCH:
    @dataclass
    class TrainResult:
        train_losses: List[float]
        val_losses: List[float]
        best_epoch: int
        best_val: float

    def train_model(
        model: nn.Module,
        x_train, y_train, x_val, y_val,
        epochs: int = 2000,
        lr: float = 1e-2,
        weight_decay: float = 0.0,   # ⭐ L2 正则化
        l1_lambda: float = 0.0,      # ⭐ L1 正则化
        early_stop: bool = False,    # ⭐ 早停
        patience: int = 50,
        verbose: bool = True,
    ) -> TrainResult:
        opt = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
        loss_fn = nn.MSELoss()
        train_losses, val_losses = [], []
        best_val, best_epoch, bad_epochs = float("inf"), 0, 0

        for ep in range(epochs):
            model.train()
            pred = model(x_train)
            mse = loss_fn(pred, y_train)

            # L1 正则项：所有权重绝对值之和
            if l1_lambda > 0:
                l1 = sum(p.abs().sum() for p in model.parameters())
                loss = mse + l1_lambda * l1
            else:
                loss = mse

            opt.zero_grad()
            loss.backward()
            opt.step()

            model.eval()
            with torch.no_grad():
                val_loss = loss_fn(model(x_val), y_val).item()
            train_losses.append(mse.item())
            val_losses.append(val_loss)

            # 早停逻辑：patience 轮验证集未改善就终止
            if val_loss < best_val - 1e-5:
                best_val, best_epoch, bad_epochs = val_loss, ep, 0
            else:
                bad_epochs += 1
                if early_stop and bad_epochs >= patience:
                    if verbose:
                        print(f"  ⏹  Early Stopping @ epoch {ep}, best @ {best_epoch}")
                    break
        return TrainResult(train_losses, val_losses, best_epoch, best_val)


# ============================================================
# 4. 正则化方法 5：Data Augmentation（数据增强）
#    一维回归场景：给输入加轻微高斯噪声 + 随机平移
#    NLP / Prompt 场景：同义词替换、反译、改写问法
# ============================================================
if HAS_TORCH:
    def augment(x: torch.Tensor, y: torch.Tensor,
                times: int = 3, noise: float = 0.05) -> Tuple[torch.Tensor, torch.Tensor]:
        """把训练集 x,y 复制 times 份，每份加不同噪声→ 扩充数据多样性"""
        xs, ys = [x], [y]
        for _ in range(times):
            xs.append(x + noise * torch.randn_like(x))
            ys.append(y + noise * torch.randn_like(y))
        return torch.cat(xs, dim=0), torch.cat(ys, dim=0)


# ============================================================
# 5. 主 Demo：一次跨越 6 个实验，打印训练 vs 验证误差，一眼看出区别
# ============================================================
def run_ml_demo() -> None:
    if not HAS_TORCH:
        print("跳过实验演示：未安装 torch。")
        return
    data = make_dataset()
    x_tr, y_tr, x_te, y_te = data
    print("=" * 64)
    print("🔬 PyTorch 演示：欠拟合 / 过拟合 / 5 种正则化")
    print("数据：y = sin(x) + 噪声，训练集15点，验证集200点真值")
    print("=" * 64)

    cases = []

    # 实验 1：欠拟合（小模型）
    set_seed(42); m = TinyNet()
    r = train_model(m, x_tr, y_tr, x_te, y_te, epochs=1500, verbose=False)
    cases.append(("1. 欠拟合 (TinyNet)", r))

    # 实验 2：过拟合（大模型无正则化）
    set_seed(42); m = BigNet()
    r = train_model(m, x_tr, y_tr, x_te, y_te, epochs=1500, verbose=False)
    cases.append(("2. 过拟合 (BigNet)", r))

    # 实验 3：L2 正则化
    set_seed(42); m = BigNet()
    r = train_model(m, x_tr, y_tr, x_te, y_te, epochs=1500, weight_decay=1e-2, verbose=False)
    cases.append(("3. + L2 (weight_decay=1e-2)", r))

    # 实验 4：L1 正则化
    set_seed(42); m = BigNet()
    r = train_model(m, x_tr, y_tr, x_te, y_te, epochs=1500, l1_lambda=1e-4, verbose=False)
    cases.append(("4. + L1 (lambda=1e-4)", r))

    # 实验 5：Dropout
    set_seed(42); m = MidNet(dropout=0.3)
    r = train_model(m, x_tr, y_tr, x_te, y_te, epochs=1500, verbose=False)
    cases.append(("5. + Dropout(p=0.3)", r))

    # 实验 6：Early Stopping
    set_seed(42); m = BigNet()
    r = train_model(m, x_tr, y_tr, x_te, y_te, epochs=1500, early_stop=True, patience=50, verbose=True)
    cases.append(("6. + Early Stopping", r))

    # 实验 7：Data Augmentation
    set_seed(42); m = BigNet()
    x_aug, y_aug = augment(x_tr, y_tr, times=4, noise=0.1)
    r = train_model(m, x_aug, y_aug, x_te, y_te, epochs=1500, verbose=False)
    cases.append((f"7. + Data Aug (训练集{x_tr.size(0)}→{x_aug.size(0)})", r))

    print("\n【结果】训练 MSE vs 验证 MSE（验证越低越好）")
    print("-" * 64)
    print(f"{'实验':38} {'train':>10} {'val':>10}")
    print("-" * 64)
    for name, r in cases:
        train_mse = r.train_losses[-1]
        print(f"{name:38} {train_mse:>10.4f} {r.best_val:>10.4f}")
    print("-" * 64)
    print("典型现象：")
    print("  · 实验1 train高 + val高 → 欠拟合")
    print("  · 实验2 train低 + val高 → 过拟合")
    print("  · 实验3~7 train略高 + val明显下降 → 正则化生效")


# ============================================================
# 6. 双重映射：同一个概念在 ML 和 Prompt 工程里怎么用
#    这一段是 Day02 的灵魂——面试考过拟合/正则化时，
#    能顺带说出 Prompt 工程对照，面试官眼前一亮！
# ============================================================
PROMPT_MAPPING: List[Tuple[str, str, str, str]] = [
    # (概念, ML 含义, Prompt 工程含义, 一句话背诵)
    ("欠拟合 Underfitting",
     "模型太简单，训练/测试都差",
     "Prompt 太简单，示例内/示例外都答不准",
     "加角色 + 加背景 + 加任务 + 加示例 + 加格式"),
    ("过拟合 Overfitting",
     "模型太复杂 + 数据太少，训练好但测试差",
     "Prompt 太长太死，示例多但单一，只能处理见过的问题",
     "信号词：『换个问法就崩』"),
    ("L1 正则化",
     "loss += λ·Σ|w|，权重稀疏，自动特征选择",
     "删废话，只保留有效字段",
     "少即是多：Prompt 100~300 字最佳"),
    ("L2 正则化",
     "loss += λ·Σw²，权重平滑，不让某权重特别大",
     "不说『必须/绝对/一字不差』，改成『尽量/建议/参考』",
     "不走极端，留有余地"),
    ("Dropout",
     "训练时随机让一部分神经元失活",
     "示例多样化，3~5 个不同情况，别只给一种",
     "鸡蛋不要放在一个篮子里"),
    ("Early Stopping",
     "验证集 loss 不再下降就停止训练",
     "约束加到 3~5 条够了就停，不要无限叠加",
     "够了就停，不要贪多"),
    ("Data Augmentation",
     "对输入做变换（旋转/裁剪/加噪），增加数据多样性",
     "示例覆盖正常 + 异常 + 边界 + 极端，泛化能力↑",
     "见过的情况越多，越不容易被难倒"),
]


def print_prompt_mapping() -> None:
    print("\n" + "=" * 64)
    print("🔁 ML 概念 ←→ Prompt 工程 1:1 映射表（面试金句）")
    print("=" * 64)
    for name, ml, prompt, oneliner in PROMPT_MAPPING:
        print(f"\n🧩 {name}")
        print(f"  • ML    : {ml}")
        print(f"  • Prompt: {prompt}")
        print(f"  • 金句  : {oneliner}")


# ============================================================
# 7. Prompt 工程实战：5 种正则化 → 5 种 Prompt 优化（before/after）
# ============================================================
PROMPT_DEMO = {
    "L1（删废话）": {
        "before": "你是一个非常非常厉害的、拿过图灵奖的、在 Google 工作过 20 年的、"
                  "全世界最好的 AI 助手，我特别特别喜欢你...",
        "after":  "你是一个有 10 年经验的高级 Python 代码审查专家。",
    },
    "L2（不走极端）": {
        "before": "你必须严格按 JSON 输出，一个字都不能错，标点错了就完蛋！",
        "after":  "请按以下 JSON 格式输出，字段名严格保持一致即可。",
    },
    "Dropout（示例多样化）": {
        "before": "示例1：def add(a,b): return a+b → {\"bug\": 0}\n"
                  "示例2：def add(a,b): return a+b → {\"bug\": 0}",
        "after":  "示例1：正常加法（无 bug）\n示例2：除零错误\n示例3：SQL 注入\n示例4：性能问题（O(n²)）",
    },
    "Early Stopping（约束够了就停）": {
        "before": "约束1~10：必须中文/分点/每点≤3行/必须有例子/例子必须 Python/...",
        "after":  "约束：① 中文分点 ② 建议具体可执行 ③ 严重 bug 优先",
    },
    "Data Augmentation（覆盖边界）": {
        "before": "示例：1+1=? 2+3=? 5+5=?（全是简单加法）",
        "after":  "示例：正常加法 / 减法 / 带括号 / 除零 / 超大整数（覆盖边界）",
    },
}


def print_prompt_demo() -> None:
    print("\n" + "=" * 64)
    print("🛠 实战：5 种正则化对应的 Prompt before/after")
    print("=" * 64)
    for name, pair in PROMPT_DEMO.items():
        print(f"\n📌 {name}")
        print("  ❌ Before:")
        for line in pair["before"].splitlines():
            print(f"     {line}")
        print("  ✅ After:")
        for line in pair["after"].splitlines():
            print(f"     {line}")


# ============================================================
# ⭐ 面试 30 秒答法（背下来直接用）
# ============================================================
INTERVIEW_ANSWER = """
Q: 什么是过拟合，怎么解决？
A: 过拟合 = 模型在训练集表现很好、在测试集表现很差，本质是模型容量
   超过数据信息量。常用 5 种解法：
   ① L1 / L2 正则化：在 loss 里加权重惩罚，L1 稀疏化、L2 平滑化；
   ② Dropout：训练时随机失活，防止依赖某个神经元；
   ③ Early Stopping：验证集不再下降就停；
   ④ Data Augmentation：增加数据多样性；
   ⑤ 加大数据量 / 减小模型容量。
   这套思想 1:1 可以迁移到 Prompt 工程：
   L1=删废话，L2=不走极端，Dropout=示例多样化，
   Early Stopping=约束够了就停，Data Aug=覆盖边界示例。
"""


if __name__ == "__main__":
    run_ml_demo()          # 1. ML 实验对比
    print_prompt_mapping() # 2. ML ↔ Prompt 映射
    print_prompt_demo()    # 3. Prompt before/after 实战
    print("\n" + "=" * 64)
    print(INTERVIEW_ANSWER)
    print("=" * 64)
