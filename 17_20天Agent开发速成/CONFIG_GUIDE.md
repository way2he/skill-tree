# 项目配置文件介绍

本项目使用了现代 Python 开发工具链，以下是主要配置文件的详细说明。

## 1. pyproject.toml

`pyproject.toml` 是 Python 项目的核心配置文件，采用 TOML 格式编写，定义了项目的构建系统、依赖和开发工具配置。

### 主要内容

#### 1.1 构建系统配置
```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```
- 指定使用 `setuptools` 作为构建工具
- 要求 setuptools 版本 >= 61.0

#### 1.2 项目元数据
```toml
[project]
name = "agent-dev-course"
version = "1.0.0"
description = "20天Agent开发速成课程代码"
requires-python = ">=3.12"
```
- 项目名称和版本
- 要求 Python 3.12 及以上版本

#### 1.3 项目依赖
```toml
dependencies = [
    "requests>=2.31.0",      # HTTP 请求库
    "pydantic>=2.0.0",      # 数据验证和序列化库
    "aiohttp>=3.9.0",       # 异步 HTTP 客户端/服务器库
]
```

#### 1.4 代码格式化工具 - Black
```toml
[tool.black]
line-length = 88
target-version = ["py312"]
```
- 自动格式化 Python 代码
- 行宽限制为 88 字符
- 针对 Python 3.12 优化

#### 1.5 代码检查工具 - Flake8
```toml
[tool.flake8]
max-line-length = 88
select = ["E", "W", "F", "B", "C90"]
ignore = ["E501", "W503", "E203"]
```
- 检查代码风格和潜在 bug
- 集成了 `flake8-bugbear` 插件
- 忽略部分与 Black 冲突的规则

#### 1.6 类型检查工具 - MyPy
```toml
[tool.mypy]
python_version = "3.12"
strict = true
```
- 严格模式类型检查
- 显示错误代码
- 不允许缺失导入和未定义的类型

#### 1.7 导入排序工具 - isort
```toml
[tool.isort]
profile = "black"
line_length = 88
```
- 自动排序 import 语句
- 使用与 Black 兼容的配置

---

## 2. .pre-commit-config.yaml

`.pre-commit-config.yaml` 配置了 Git 提交前的钩子（hooks），在代码提交时自动执行一系列检查和格式化操作。

### 主要钩子

#### 2.1 基础检查钩子 (pre-commit-hooks)
```yaml
- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: v4.6.0
  hooks:
  - id: trailing-whitespace       # 移除行尾空格
  - id: end-of-file-fixer         # 确保文件以换行结尾
  - id: check-yaml                # 检查 YAML 文件语法
  - id: check-json                # 检查 JSON 文件语法
  - id: check-added-large-files   # 检查大文件
  - id: debug-statements          # 检查调试语句
  - id: check-merge-conflict      # 检查合并冲突标记
```

#### 2.2 代码格式化 (Black)
```yaml
- repo: https://github.com/psf/black
  rev: 26.5.1
  hooks:
  - id: black
    args: ["--target-version=py312"]
```

#### 2.3 代码检查 (Flake8)
```yaml
- repo: https://github.com/PyCQA/flake8
  rev: 7.3.0
  hooks:
  - id: flake8
    additional_dependencies: [flake8-bugbear]
```

#### 2.4 导入排序 (isort)
```yaml
- repo: https://github.com/PyCQA/isort
  rev: 8.0.1
  hooks:
  - id: isort
    args: ["--profile=black"]
```

#### 2.5 类型检查 (MyPy)
```yaml
- repo: https://github.com/python/mypy
  rev: v1.10.1
  hooks:
  - id: mypy
    args: ["--strict", "--show-error-codes"]
```

### 使用方法

1. **安装 pre-commit**：
   ```bash
   pip install pre-commit
   ```

2. **安装 Git 钩子**：
   ```bash
   pre-commit install
   ```

3. **运行所有钩子**（在提交前）：
   ```bash
   pre-commit run --all-files
   ```

4. **只运行特定钩子**：
   ```bash
   pre-commit run black --all-files
   ```

---

## 3. .mypy_cache/ 目录

`.mypy_cache/` 是 MyPy 类型检查工具的缓存目录。

### 作用
- 存储 MyPy 的类型检查缓存
- 加速后续的类型检查过程
- 避免重复检查未修改的文件

### 注意事项
- ⚠️ **此目录应该被 Git 忽略**
- 通常在 `.gitignore` 中添加：
  ```
  .mypy_cache/
  __pycache__/
  *.pyc
  ```
- 可以安全删除，MyPy 会在下次运行时重新生成

---

## 4. 完整开发工作流程

### 安装项目依赖
```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境（Windows）
.venv\Scripts\activate

# 安装依赖
pip install -e .

# 安装开发工具
pip install black flake8 isort mypy pre-commit

# 安装 Git 钩子
pre-commit install
```

### 日常开发
1. 编写代码
2. 运行测试
3. 使用 Black 格式化代码
4. 运行 MyPy 类型检查
5. Git 提交（pre-commit 钩子自动执行）

### 提交代码时的流程
```
git add .
git commit -m "your message"
  ↓
pre-commit 钩子运行
  ├─ 检查 trailing-whitespace
  ├─ 检查 end-of-file
  ├─ 运行 Black 格式化
  ├─ 运行 isort 排序导入
  ├─ 运行 flake8 检查
  └─ 运行 mypy 类型检查
  ↓
所有检查通过 → 提交成功
有检查失败 → 提交被阻止，修复后重新提交
```

---

## 5. 工具链总结

| 工具 | 用途 | 配置文件 |
|------|------|----------|
| **Black** | 代码自动格式化 | pyproject.toml |
| **isort** | Import 语句排序 | pyproject.toml |
| **Flake8** | 代码风格和 Bug 检查 | pyproject.toml |
| **MyPy** | 类型检查 | pyproject.toml |
| **pre-commit** | Git 提交前钩子 | .pre-commit-config.yaml |

---

## 6. 常见问题

### Q: 如何跳过 pre-commit 检查？
A: 不建议跳过，但如确实需要：
```bash
git commit --no-verify -m "message"
```

### Q: 如何更新 pre-commit 钩子版本？
A:
```bash
pre-commit autoupdate
```

### Q: MyPy 缓存占用空间太大怎么办？
A: 删除缓存目录：
```bash
rm -rf .mypy_cache/
```
