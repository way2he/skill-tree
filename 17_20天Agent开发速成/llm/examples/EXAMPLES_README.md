# Examples（原 demo）

本目录包含所有使用示例和测试脚本。

---

## 📁 目录结构

```
examples/
├── EXAMPLES_README.md             # 本文件
├── demo_basic.py                  # 基础使用示例
├── demo_stream.py                 # 流式响应示例
├── demo_json.py                   # JSON 生成示例
├── demo_zero_config.py            # 零配置示例
├── demo_backend_selector.py       # Backend 选择器示例
├── demo_backend_async.py          # 异步调用示例
├── demo_logging.py                # 日志记录示例
├── demo_resilience.py             # 弹性机制示例
├── demo_resilience_full.py        # 完整弹性示例
├── demo_config.py                 # 配置示例
├── demo_register.py               # 注册 Provider 示例
├── demo_compare.py                # 对比示例
├── demo_ollama_requests.py        # Ollama 直接调用示例
├── _selftest_ollama.py            # Ollama 自测试
├── setup_ollama_test.py           # 🔧 Ollama 测试环境配置
├── test_ollama_qwen35.py          # 🧪 Ollama 完整测试套件
├── test_ollama_independent.py     # 🎯 Ollama 独立测试
└── TEST_README.md                 # Ollama 测试使用文档
```

---

## 🚀 快速使用

### 运行 Ollama 完整测试
```bash
cd examples
python test_ollama_qwen35.py
```

### 配置 Ollama 测试环境
```bash
python setup_ollama_test.py check
python setup_ollama_test.py pull
```

---

## 📋 文件分类

### 原始 Demo 文件
- `demo_*.py` - 各种使用示例（保留参考）

### 测试工具
- `setup_ollama_test.py` - 环境配置工具
- `test_ollama_qwen35.py` - 完整测试套件
- `test_ollama_independent.py` - 独立测试
- `_selftest_ollama.py` - 自测试

### 文档
- `EXAMPLES_README.md` - 本文件
- `TEST_README.md` - 详细测试文档

---

## 📖 更多信息

详细的测试使用说明请查看 `TEST_README.md`。

