# PyTorch GPU 版本与 CPU 版本：深度理解与安装指南

---

## 一、任务重述

本文旨在全面、深入地介绍 PyTorch 的 GPU 版本与 CPU 版本，包括：
- 两者的核心架构差异与适用场景
- 性能对比与选型建议
- 详细的安装步骤（Windows/Linux/macOS）
- CUDA、ROCm 等底层计算平台的关系
- 常见问题与排错指南

---

## 二、PyTorch 版本概览

### 2.1 什么是 PyTorch？

PyTorch 是由 Meta（Facebook）AI 研究团队开发的**开源深度学习框架**，以动态计算图（Eager Mode）和 Pythonic 的 API 设计著称。它支持从研究原型到生产部署的完整工作流。

### 2.2 当前最新版本（截至 2025 年）

| 项目 | 信息 |
|------|------|
| 最新稳定版 | **PyTorch 2.12.0** |
| Python 要求 | **3.10 - 3.14** |
| 支持的 CUDA 版本 | CUDA 12.6 / 13.0 / 13.2 |
| 支持的 ROCm 版本 | ROCm 7.2（AMD GPU） |
| 支持 CPU | 是（所有平台） |

### 2.3 两个版本的本质区别

```
┌─────────────────────────────────────────────────────────┐
│                    PyTorch 发行版                        │
├──────────────────────┬──────────────────────────────────┤
│     CPU 版本          │         GPU 版本                  │
├──────────────────────┼──────────────────────────────────┤
│ 仅含 CPU 后端         │ 包含 CPU + CUDA/ROCm 后端        │
│ 体积较小 (~200MB)     │ 体积较大 (~2-3GB)                │
│ 无需 NVIDIA 驱动      │ 需要 NVIDIA 驱动 + CUDA Toolkit  │
│ 适用于学习/轻量推理    │ 适用于训练/大规模推理             │
│ pip install torch     │ pip install torch --index-url    │
│                      │   https://download.pytorch.org   │
│                      │   /whl/cu126                     │
└──────────────────────┴──────────────────────────────────┘
```

**关键点**：GPU 版本**向下兼容** CPU。安装 GPU 版本后，即使没有可用 GPU，PyTorch 也会自动回退到 CPU 模式运行。因此，**通常只需安装 GPU 版本即可同时覆盖两种场景**。

---

## 三、深度理解：CPU vs GPU 计算架构

### 3.1 CPU（Central Processing Unit）

```
┌─────────────────────────────────────┐
│              CPU 核心                │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐   │
│  │Core0│ │Core1│ │Core2│ │Core3│   │
│  │(强) │ │(强) │ │(强) │ │(强) │   │
│  └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘   │
│     │       │       │       │       │
│  ┌──▼───────▼───────▼───────▼──┐   │
│  │      大容量 L3 Cache        │   │
│  └──────────┬──────────────────┘   │
│             │                      │
│  ┌──────────▼──────────────────┐   │
│  │     内存控制器 (DDR5)        │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
特点：少量强核心，擅长复杂逻辑/串行任务
```

**CPU 的优势**：
- **高时钟频率**（通常 3-6 GHz），单线程性能强
- **大容量缓存**（L1/L2/L3），低延迟访问
- **复杂指令集**（分支预测、乱序执行等）
- **通用性强**，适合各种计算任务

**CPU 的劣势**：
- 核心数量有限（通常 4-64 个）
- 并行计算能力有限
- 浮点运算吞吐量远低于 GPU

### 3.2 GPU（Graphics Processing Unit）

```
┌─────────────────────────────────────────────────────┐
│                    GPU 架构                          │
│  ┌─────────────────────────────────────────────┐    │
│  │  SM 0    SM 1    SM 2    ...    SM N        │    │
│  │ ┌───┐   ┌───┐   ┌───┐          ┌───┐       │    │
│  │ │Core│x32│Core│x32│Core│x32     │Core│x32   │    │
│  │ └───┘   └───┘   └───┘          └───┘       │    │
│  └─────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────┐    │
│  │          高带宽显存 (GDDR6/HBM)              │    │
│  │       带宽: 500 GB/s ~ 3 TB/s               │    │
│  └─────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
特点：海量弱核心，擅长大规模并行/矩阵运算
```

**GPU 的优势**：
- **海量并行核心**（数千到数万个 CUDA Core）
- **极高显存带宽**（500 GB/s - 3 TB/s，远超 CPU 的 ~100 GB/s）
- **专为矩阵运算优化**（Tensor Core 支持混合精度）
- **深度学习加速器**（如 NVIDIA 的 Tensor Core）

**GPU 的劣势**：
- 单线程性能弱于 CPU
- 显存容量有限（通常 8-80 GB）
- 数据传输有 PCIe 开销（CPU↔GPU）
- 不适合复杂分支逻辑

### 3.3 为什么深度学习需要 GPU？

深度学习的核心运算是**大规模矩阵乘法**和**卷积运算**，这些操作具有：
1. **高度并行性** — 数百万个乘加操作可同时执行
2. **计算密集** — 单次前向/反向传播涉及数十亿次浮点运算
3. **低精度容忍** — FP16/BF16 精度已足够，适合 Tensor Core 加速

**性能对比参考**（训练 ResNet-50）：

| 硬件 | 训练时间 (epoch) | 相对速度 |
|------|------------------|----------|
| Intel i9 CPU | ~120 分钟 | 1x |
| NVIDIA RTX 4090 | ~0.5 分钟 | **~240x** |
| NVIDIA A100 | ~0.3 分钟 | **~400x** |

> 注：实际性能因模型大小、batch size、精度等因素而异，上述数据为量级参考。

---

## 四、PyTorch 中的设备管理

### 4.1 检测可用设备

```python
import torch

# 检查 CUDA（NVIDIA GPU）是否可用
print(f"CUDA 可用: {torch.cuda.is_available()}")

# 检查 CUDA 版本
if torch.cuda.is_available():
    print(f"CUDA 版本: {torch.version.cuda}")
    print(f"GPU 数量: {torch.cuda.device_count()}")
    print(f"当前 GPU: {torch.cuda.get_device_name(0)}")
    print(f"GPU 显存: {torch.cuda.get_device_properties(0).total_mem / 1024**3:.1f} GB")

# 检查 ROCm（AMD GPU）是否可用
# ROCm 在 PyTorch API 层复用 CUDA 接口
# torch.cuda.is_available() 对 ROCm 同样返回 True

# 检查 MPS（Apple Silicon）是否可用
print(f"MPS 可用: {torch.backends.mps.is_available()}")

# 获取最佳可用设备
def get_device() -> torch.device:
    """自动选择最佳可用计算设备"""
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif torch.backends.mps.is_available():
        return torch.device("mps")
    else:
        return torch.device("cpu")

device = get_device()
print(f"使用设备: {device}")
```

### 4.2 张量（Tensor）的设备管理

```python
import torch

# 创建 CPU 张量
x_cpu = torch.randn(1000, 1000)
print(f"x_cpu 设备: {x_cpu.device}")  # cpu

# 将张量移动到 GPU
if torch.cuda.is_available():
    x_gpu = x_cpu.to("cuda")          # 方式1：字符串
    # 或
    x_gpu = x_cpu.to(torch.device("cuda:0"))  # 方式2：指定 GPU 编号
    # 或
    x_gpu = x_cpu.cuda()              # 方式3：便捷方法
    print(f"x_gpu 设备: {x_gpu.device}")  # cuda:0

    # 将张量移回 CPU
    x_back = x_gpu.cpu()
    print(f"x_back 设备: {x_back.device}")  # cpu

# 直接在 GPU 上创建张量
if torch.cuda.is_available():
    x_direct = torch.randn(1000, 1000, device="cuda")
    print(f"x_direct 设备: {x_direct.device}")  # cuda:0
```

### 4.3 模型的设备管理

```python
import torch
import torch.nn as nn

class SimpleModel(nn.Module):
    """简单的全连接模型"""
    def __init__(self) -> None:
        super().__init__()
        self.fc1 = nn.Linear(784, 256)
        self.fc2 = nn.Linear(256, 10)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = torch.relu(self.fc1(x))
        return self.fc2(x)

model = SimpleModel()

# 将模型移到 GPU
if torch.cuda.is_available():
    model = model.to("cuda")
    # 或 model.cuda()

# 验证模型参数所在设备
print(f"模型参数设备: {next(model.parameters()).device}")
```

### 4.4 ⚠️ 常见陷阱：设备不匹配

```python
# 错误示例：模型在 GPU，数据在 CPU
model = model.to("cuda")
x = torch.randn(64, 784)  # 默认在 CPU
# output = model(x)  # RuntimeError: Expected all tensors to be on the same device

# 正确做法：确保数据和模型在同一设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
x = x.to(device)
output = model(x)  # 正常运行
```

---

## 五、安装指南

### 5.1 安装前的准备

#### 检查 GPU 信息（NVIDIA）

```powershell
# 在 PowerShell 或 CMD 中执行
nvidia-smi
```

输出示例：
```
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 560.35.03              Driver Version: 560.35.03      CUDA Version: 12.6   |
|-----------------------------------------+------------------------+---------------------+
| GPU  Name                 Persistence-M | Bus-Id         Disp.A | Volatile Uncorr. ECC|
| Fan  Temp   Perf          Pwr:Usage/Cap |          Memory-Usage | GPU-Util  Compute M.|
|=========================================+========================+=====================|
|   0  NVIDIA GeForce RTX 4090     Off    | 00000000:01:00.0  On  |                  0 |
| 30%   42C    P8             20W / 450W  |    512MiB / 24564MiB  |      2%      Default |
+-----------------------------------------+------------------------+---------------------+
```

**关键信息**：
- **Driver Version**：NVIDIA 驱动版本
- **CUDA Version**：驱动支持的最高 CUDA 版本（这是你系统可用的 CUDA 上限）

#### CUDA 版本兼容性

```
NVIDIA 驱动版本  →  支持的最高 CUDA 版本
     560.x      →       CUDA 12.6
     550.x      →       CUDA 12.4
     535.x      →       CUDA 12.2
     525.x      →       CUDA 12.0
```

> **重要**：PyTorch 的 GPU 版本**自带 CUDA 运行时库**，你不需要单独安装 CUDA Toolkit（除非你要从源码编译 PyTorch）。你只需要确保 NVIDIA 驱动版本足够新即可。

### 5.2 Windows 安装（你的环境）

#### 方式一：pip 安装（推荐）

```powershell
# 激活你的虚拟环境
C:\Users\robotAi\installSoftware\pyenv\agent-dev\Scripts\Activate.ps1

# 安装 GPU 版本（CUDA 12.6）— 推荐
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126

# 或者安装 CUDA 13.0 版本
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu130

# 或者安装 CUDA 13.2 版本（最新）
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu132

# 安装 CPU 版本（如果没有 NVIDIA GPU）
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

#### 方式二：conda 安装

```powershell
# GPU 版本（CUDA 12.6）
conda install pytorch torchvision pytorch-cuda=12.6 -c pytorch -c nvidia

# CPU 版本
conda install pytorch torchvision cpuonly -c pytorch
```

#### 安装验证

```python
import torch

# 基础验证
print(f"PyTorch 版本: {torch.__version__}")

# CUDA 验证
print(f"CUDA 是否可用: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA 版本: {torch.version.cuda}")
    print(f"cuDNN 版本: {torch.backends.cudnn.version()}")
    print(f"GPU 名称: {torch.cuda.get_device_name(0)}")

    # 快速性能测试
    import time
    size = 5000

    # CPU 测试
    x_cpu = torch.randn(size, size)
    start = time.time()
    for _ in range(10):
        _ = torch.mm(x_cpu, x_cpu)
    cpu_time = time.time() - start
    print(f"CPU 矩阵乘法 (10次): {cpu_time:.4f} 秒")

    # GPU 测试
    x_gpu = x_cpu.cuda()
    # 预热
    _ = torch.mm(x_gpu, x_gpu)
    torch.cuda.synchronize()

    start = time.time()
    for _ in range(10):
        _ = torch.mm(x_gpu, x_gpu)
    torch.cuda.synchronize()
    gpu_time = time.time() - start
    print(f"GPU 矩阵乘法 (10次): {gpu_time:.4f} 秒")
    print(f"GPU 加速比: {cpu_time/gpu_time:.1f}x")
else:
    print("未检测到 CUDA GPU，将使用 CPU 模式")
```

### 5.3 Linux 安装

```bash
# GPU 版本（CUDA 12.6）
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126

# AMD GPU 版本（ROCm 7.2）
pip install torch torchvision --index-url https://download.pytorch.org/whl/rocm72

# CPU 版本
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### 5.4 macOS 安装

```bash
# macOS 使用 Metal Performance Shaders (MPS) 加速
# Apple Silicon (M1/M2/M3/M4) 芯片支持 GPU 加速
pip install torch torchvision

# 验证 MPS
python -c "import torch; print(f'MPS 可用: {torch.backends.mps.is_available()}')"
```

---

## 六、CUDA 生态深度理解

### 6.1 CUDA 软件栈

```
┌─────────────────────────────────────────┐
│          用户应用 (PyTorch)              │
├─────────────────────────────────────────┤
│        PyTorch CUDA 扩展                │
├─────────────────────────────────────────┤
│   cuDNN (深度神经网络加速库)             │
│   cuBLAS (基础线性代数子程序)            │
│   cuRAND (随机数生成)                    │
│   NCCL (多 GPU 通信)                    │
├─────────────────────────────────────────┤
│        CUDA Runtime API                 │
├─────────────────────────────────────────┤
│        CUDA Driver (NVIDIA 驱动)        │
├─────────────────────────────────────────┤
│        NVIDIA GPU 硬件                  │
└─────────────────────────────────────────┘
```

### 6.2 各组件作用

| 组件 | 全称 | 作用 |
|------|------|------|
| **CUDA** | Compute Unified Device Architecture | NVIDIA GPU 通用并行计算平台 |
| **cuDNN** | CUDA Deep Neural Network library | 深度学习 primitives 加速（卷积、池化、激活等） |
| **cuBLAS** | CUDA Basic Linear Algebra Subprograms | 矩阵乘法、向量运算加速 |
| **NCCL** | NVIDIA Collective Communications Library | 多 GPU / 多节点分布式训练通信 |
| **Tensor Core** | — | 混合精度矩阵乘法硬件单元（FP16/BF16/INT8） |

### 6.3 PyTorch 如何使用 CUDA

```python
import torch

# 1. 自动混合精度（AMP）— 利用 Tensor Core 加速
from torch.cuda.amp import autocast, GradScaler

model = model.cuda()
optimizer = torch.optim.Adam(model.parameters())
scaler = GradScaler()  # 梯度缩放，防止 FP16 下溢

for data, target in dataloader:
    data, target = data.cuda(), target.cuda()

    with autocast():  # 自动将合适操作转为 FP16
        output = model(data)
        loss = torch.nn.functional.cross_entropy(output, target)

    scaler.scale(loss).backward()       # 缩放梯度
    scaler.step(optimizer)              # 更新参数
    scaler.update()                     # 更新缩放因子
```

### 6.4 多 GPU 训练

```python
import torch
import torch.nn as nn

# 方式1：DataParallel（简单但效率较低）
model = nn.DataParallel(model)  # 自动将数据拆分到多个 GPU

# 方式2：DistributedDataParallel（推荐，效率更高）
# 需要使用 torchrun 启动
# torchrun --nproc_per_node=4 train.py

# 在训练脚本中：
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

dist.init_process_group("nccl")
model = model.to("cuda")
model = DDP(model, device_ids=[local_rank])
```

---

## 七、版本选择决策树

```
开始
 │
 ├─ 有 NVIDIA GPU？
 │   ├─ 是 → 安装 GPU 版本（选择匹配的 CUDA 版本）
 │   │       pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126
 │   │
 │   └─ 否 → 有 AMD GPU？
 │       ├─ 是（Linux）→ 安装 ROCm 版本
 │       │               pip install torch torchvision --index-url https://download.pytorch.org/whl/rocm72
 │       │
 │       └─ 否 → 有 Apple Silicon (M1+)？
 │           ├─ 是 → 安装标准版本（自动支持 MPS）
 │           │       pip install torch torchvision
 │           │
 │           └─ 否 → 安装 CPU 版本
 │                   pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
 │
 └─ 仅用于学习/推理小模型？
     ├─ 是 → CPU 版本即可
     └─ 否 → 强烈建议 GPU 版本
```

---

## 八、常见问题与排错

### 8.1 安装 GPU 版本但 `torch.cuda.is_available()` 返回 False

**可能原因及解决方案**：

| 原因 | 解决方案 |
|------|----------|
| NVIDIA 驱动版本过低 | 更新驱动到最新版 |
| 安装了 CPU 版本而非 GPU 版本 | 检查：`pip show torch`，确认安装来源 |
| CUDA 版本与驱动不兼容 | 降低 CUDA 版本或更新驱动 |
| conda 安装时未指定 CUDA | `conda install pytorch torchvision pytorch-cuda=12.6 -c pytorch -c nvidia` |

### 8.2 conda 安装 GPU 版本却安装了 CPU 版本

这是**最常见的坑**。conda 默认可能解析到 CPU 版本。

**解决方案**：
```bash
# 方法1：显式指定 CUDA 包
conda install pytorch torchvision pytorch-cuda=12.6 -c pytorch -c nvidia

# 方法2：改用 pip（更可靠）
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126

# 方法3：创建干净的虚拟环境后重新安装
conda create -n pytorch_gpu python=3.12 -y
conda activate pytorch_gpu
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126
```

### 8.3 CUDA Out of Memory（显存不足）

```python
# 解决方案1：减小 batch size
batch_size = 16  # 从 64 减小到 16

# 解决方案2：使用梯度累积
accumulation_steps = 4
optimizer.zero_grad()
for i, (data, target) in enumerate(dataloader):
    output = model(data)
    loss = criterion(output, target)
    loss = loss / accumulation_steps  # 归一化
    loss.backward()
    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()

# 解决方案3：使用混合精度训练
from torch.cuda.amp import autocast
with autocast():
    output = model(data)  # 自动使用 FP16，节省约 50% 显存

# 解决方案4：启用梯度检查点（gradient checkpointing）
model = torch.utils.checkpoint.checkpoint_sequential(model, segments=4)

# 解决方案5：清理显存缓存
torch.cuda.empty_cache()
```

### 8.4 RuntimeError: CUDA error: no kernel image is available

**原因**：GPU 架构（compute capability）与 CUDA 版本不兼容。

```python
# 检查 GPU 计算能力
print(f"GPU 计算能力: {torch.cuda.get_device_capability(0)}")

# 常见 GPU 计算能力：
# RTX 40 系列: 8.9
# RTX 30 系列: 8.6
# RTX 20 系列: 7.5
# GTX 10 系列: 6.1
# V100: 7.0
# A100: 8.0
```

---

## 九、性能优化最佳实践

### 9.1 数据加载优化

```python
from torch.utils.data import DataLoader

# 使用多进程加载 + pin_memory 加速 CPU→GPU 传输
dataloader = DataLoader(
    dataset,
    batch_size=64,
    shuffle=True,
    num_workers=4,        # 多进程预加载数据
    pin_memory=True,      # 使用页锁定内存，加速 GPU 传输
    persistent_workers=True  # 保持 worker 进程存活
)

# 训练循环中
for data, target in dataloader:
    # non_blocking=True 允许数据传输与计算重叠
    data = data.to("cuda", non_blocking=True)
    target = target.to("cuda", non_blocking=True)
```

### 9.2 避免不必要的 CPU-GPU 数据传输

```python
# ❌ 错误：每个 batch 都打印 loss（触发 GPU→CPU 传输）
for data, target in dataloader:
    loss = model(data)
    print(loss.item())  # .item() 会触发同步

# ✅ 正确：定期打印
for i, (data, target) in enumerate(dataloader):
    loss = model(data)
    if i % 100 == 0:
        print(f"Step {i}, Loss: {loss.item()}")

# ✅ 正确：使用 loss.detach() 避免计算图跟踪
log_loss = loss.detach()
```

### 9.3 使用 torch.compile() 加速（PyTorch 2.x）

```python
import torch

# PyTorch 2.0+ 的编译优化（JIT 编译）
# 可获得 20%-200% 的加速（取决于模型）
compiled_model = torch.compile(model)

# 训练时使用编译后的模型
for data, target in dataloader:
    output = compiled_model(data)  # 第一次会编译，之后使用缓存
    loss = criterion(output, target)
    loss.backward()
    optimizer.step()
```

---

## 十、总结

| 维度 | CPU 版本 | GPU 版本 |
|------|----------|----------|
| **安装复杂度** | 简单，无额外依赖 | 需要 NVIDIA 驱动 |
| **包体积** | ~200 MB | ~2-3 GB |
| **训练速度** | 基准 (1x) | 10x - 400x |
| **推理速度** | 适合小模型 | 适合大模型/批量推理 |
| **适用场景** | 学习、调试、小模型 | 训练、大模型、生产部署 |
| **向下兼容** | — | ✅ 自动回退到 CPU |
| **推荐人群** | 无 GPU 的学习者 | 所有有 GPU 的用户 |

**核心建议**：
1. **有 NVIDIA GPU → 直接安装 GPU 版本**，它同时支持 CPU 和 GPU
2. **无 GPU → 安装 CPU 版本**，用于学习和开发
3. **注意 CUDA 版本匹配**：驱动支持的 CUDA 版本 ≥ PyTorch 所需的 CUDA 版本
4. **优先使用 pip 安装**，conda 安装 GPU 版本时容易出现版本解析问题
5. **使用混合精度训练**（AMP）可显著提升速度并节省显存

---

## 参考资料

- [PyTorch 官方安装页面](https://pytorch.org/get-started/locally/)
- [PyTorch CUDA 支持](https://pytorch.org/docs/stable/cuda.html)
- [NVIDIA CUDA 下载](https://developer.nvidia.com/cuda-downloads)
- [PyTorch 历史版本](https://pytorch.org/get-started/previous-versions/)
