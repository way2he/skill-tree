# Ollama 常用命令

## 模型管理

### 拉取模型
```bash
ollama pull <model_name>
```
从 Ollama 仓库下载指定的模型。

### 运行模型
```bash
ollama run <model_name>
```
启动并进入与指定模型的交互式对话。

### 列出本地模型
```bash
ollama list
```
显示本地已下载的所有模型列表。

### 删除模型
```bash
ollama rm <model_name>
```
删除本地指定的模型。

### 查看模型信息
```bash
ollama show <model_name>
```
显示指定模型的详细信息。

## 服务管理

### 启动 Ollama 服务
```bash
ollama serve
```
启动 Ollama 服务（通常在后台运行）。

### 查看版本
```bash
ollama -v
# 或
ollama --version
```
显示当前安装的 Ollama 版本。

## 创建自定义模型

### 从 Modelfile 创建模型
```bash
ollama create <model_name> -f <path_to_modelfile>
```
根据 Modelfile 创建自定义模型。

### 复制模型
```bash
ollama cp <source_model> <target_model>
```
复制一个模型到新的名称。

## 其他命令

### 查看帮助
```bash
ollama help
# 或
ollama --help
```
显示所有可用命令的帮助信息。

### 查看特定命令帮助
```bash
ollama <command> --help
```
显示指定命令的详细帮助信息。

## 常用模型示例

| 模型名称 | 说明 |
|---------|------|
| llama3 | Meta Llama 3 |
| llama3.1 | Meta Llama 3.1 |
| llama3.2 | Meta Llama 3.2 |
| mistral | Mistral AI |
| qwen2.5 | 通义千问 2.5 |
| deepseek-r1 | DeepSeek R1 |
| gemma2 | Google Gemma 2 |
| phi4 | Microsoft Phi-4 |

## 使用示例

```bash
# 下载并运行 Llama 3
ollama run llama3

# 下载通义千问
ollama pull qwen2.5

# 列出所有本地模型
ollama list

# 删除不再需要的模型
ollama rm llama3
```