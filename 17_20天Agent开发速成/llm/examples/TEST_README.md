# Ollama Qwen3.5:4b 测试套件

## 📁 文件说明

| 文件名 | 说明 |
|--------|------|
| `setup_ollama_test.py` | 环境配置工具 |
| `test_ollama_qwen35.py` | 完整测试套件 |
| `test_ollama_independent.py` | 独立测试（可单独运行） |
| `demo_basic.py` | 原 demo 文件（保留） |
| `demo_stream.py` | 原 demo 文件（保留） |
| ... | 其他原 demo 文件 |

---

## 🚀 快速开始

### 1. 环境检查
```bash
cd C:\Users\robotAi\Documents\ClawWorksapce\knowledge-base\raw\skill-tree\17_20天Agent开发速成\llm\demo

python setup_ollama_test.py check
```

### 2. 启动 Ollama
```bash
# 在另一个终端窗口运行
ollama serve
```

### 3. 拉取模型
```bash
python setup_ollama_test.py pull
# 或手动运行: ollama pull qwen2.5:4b
```

### 4. 运行完整测试
```bash
python test_ollama_qwen35.py
```

---

## 📋 测试内容

### 完整测试套件 (`test_ollama_qwen35.py`)

| 测试编号 | 测试项 | 对应 Demo |
|---------|--------|-----------|
| TEST #0 | Ollama 服务连接 | - |
| TEST #1 | 基础调用 | demo_basic.py |
| TEST #2 | 流式响应 | demo_stream.py |
| TEST #3 | JSON 生成 | demo_json.py |
| TEST #4 | 零配置 | demo_zero_config.py |
| TEST #5 | Backend 选择器 | demo_backend_selector.py |
| TEST #6 | 异步调用 | demo_backend_async.py |
| TEST #7 | 日志记录 | demo_logging.py |
| TEST #8 | 弹性机制 | demo_resilience.py |
| TEST #9 | 直接 Provider | demo_ollama_requests.py |

### 独立测试 (`test_ollama_independent.py`)

```bash
# 运行所有独立测试
python test_ollama_independent.py all

# 运行单个测试（1-9）
python test_ollama_independent.py 1
python test_ollama_independent.py 2
python test_ollama_independent.py 3
...
```

---

## 🔧 环境配置工具 (`setup_ollama_test.py`)

### 检查环境
```bash
python setup_ollama_test.py check
```

### 拉取模型
```bash
python setup_ollama_test.py pull
# 指定模型: python setup_ollama_test.py pull --model qwen3.5:4b
```

### 一键配置
```bash
python setup_ollama_test.py all
```

---

## 📝 测试模型

**默认模型**: `qwen2.5:4b`

**备用模型**: `qwen3.5:4b`

**修改模型**: 编辑测试文件顶部的 `TEST_MODEL` 变量

---

## 🎯 使用示例

### 示例 1: 快速测试
```bash
# 1. 检查环境
python setup_ollama_test.py check

# 2. 启动 ollama serve（另一个终端）
ollama serve

# 3. 运行完整测试
python test_ollama_qwen35.py
```

### 示例 2: 只测试流式响应
```bash
python test_ollama_independent.py 2
```

### 示例 3: 只测试 JSON 生成
```bash
python test_ollama_independent.py 3
```

---

## ⚠️ 前置条件

1. **Ollama 已安装**
   - 下载: https://ollama.com/download

2. **Ollama 服务已启动**
   ```bash
   ollama serve
   ```

3. **测试模型已拉取**
   ```bash
   ollama pull qwen2.5:4b
   ```

---

## 📊 测试输出示例

```
============================================================
  Ollama Qwen3.5:4b 完整测试套件
============================================================

TEST #0: Ollama 服务连接测试
============================================================
[OK] Ollama 服务已连接
[OK] 可用模型: ['qwen2.5:4b']
[OK] 测试模型 qwen2.5:4b 已存在

TEST #1: 基础调用测试
============================================================
[OK] 已注册厂商: [...]
[OK] generate 返回: ...
[OK] generate_with_response:
...

============================================================
  测试总结
============================================================
[OK] 连接
[OK] 基础调用
[OK] 流式响应
[OK] JSON 生成
...

============================================================
  总计: 10/10 测试通过
============================================================

🎉 所有测试通过！
```

---

## 🔍 故障排除

### 问题: 无法连接 Ollama
```
[FAIL] 无法连接 Ollama 服务
```
**解决**: 运行 `ollama serve` 启动服务

### 问题: 模型未找到
```
[FAIL] 模型 qwen2.5:4b 未找到
```
**解决**: 运行 `ollama pull qwen2.5:4b`

### 问题: 导入错误
```
ModuleNotFoundError: No module named 'llm'
```
**解决**: 确保在正确的目录运行脚本

---

## 📚 相关文件

- 原 Demo 文件: `demo_*.py` (保留参考)
- 新测试文件: `test_*.py` (新增)
- 配置工具: `setup_ollama_test.py` (新增)

