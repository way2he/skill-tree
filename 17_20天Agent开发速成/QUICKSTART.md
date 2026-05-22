# 快速入门指南

## 1. 环境准备

### 1.1 确保Python版本
```bash
python --version
# 需要 >= 3.12
```

### 1.2 激活虚拟环境（如果你使用项目中提到的）
```bash
# 如果你有自己的虚拟环境，直接激活
C:\Users\robotAi\installSoftware\pyenv\agent-dev\Scripts\activate
```

或者创建新的虚拟环境：
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

## 2. 安装依赖

### 2.1 安装基础依赖
```bash
pip install -e .
```

### 2.2 安装开发依赖（推荐）
```bash
pip install -e ".[dev]"
```

### 2.3 安装全部依赖（包括GUI）
```bash
pip install -e ".[full]"
```

## 3. 配置环境变量

### 3.1 复制环境变量模板
```bash
copy .env.example .env
```

### 3.2 编辑.env文件，填入你的API密钥
```env
# 至少需要配置一个大模型的API密钥
OPENAI_API_KEY=your-key-here
# 或者
DEEPSEEK_API_KEY=your-key-here
```

## 4. 验证安装

### 4.1 运行测试检查
```bash
python -c "
import sys
print(f'Python version: {sys.version}')
try:
    import openai
    print('openai OK')
    import langchain
    print('langchain OK')
    import langgraph
    print('langgraph OK')
    print('✅ 所有核心依赖安装成功！')
except ImportError as e:
    print(f'❌ 缺少依赖: {e}')
"
```

## 5. 开始学习

按照主README.md的建议，从Day01开始学习！

## 常见问题

### 问题1：pip安装慢怎么办？
使用国内镜像源：
```bash
pip install -e . -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题2：faiss安装失败？
Windows上可以先安装faiss-cpu：
```bash
pip install faiss-cpu -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题3：虚拟环境忘记怎么激活？
```bash
# Windows
C:\Users\robotAi\installSoftware\pyenv\agent-dev\Scripts\activate
```
