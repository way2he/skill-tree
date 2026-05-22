# Python `openai` 包详解

> **当前最新版本**: v2.37.0 (2026-05-13)
> **最低 Python 版本**: 3.9+
> **HTTP 底层**: httpx（同步/异步）
> **许可证**: Apache-2.0
> **官方仓库**: https://github.com/openai/openai-python

---

## 一、安装与环境配置

### 1.1 安装

```bash
# 基础安装
pip install openai

# 如需使用 aiohttp 作为异步 HTTP 后端（更高并发性能）
pip install openai[aiohttp]
```

### 1.2 API Key 配置

```python
import os
from openai import OpenAI

# 方式一：通过环境变量（推荐）
# 在 .env 文件中设置: OPENAI_API_KEY="sk-xxx"
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 方式二：直接传入（不推荐，避免泄露）
client = OpenAI(api_key="sk-xxx")

# 方式三：使用 python-dotenv
# pip install python-dotenv
from dotenv import load_dotenv
load_dotenv()  # 加载 .env 文件
client = OpenAI()
```

### 1.3 自定义 Base URL（兼容第三方服务）

```python
from openai import OpenAI

# 连接兼容 OpenAI 接口的第三方服务（如 Azure、本地模型等）
client = OpenAI(
    api_key="your-key",
    base_url="https://your-endpoint/v1",  # 自定义 API 地址
)
```

---

## 二、包整体架构

```
openai/
├── OpenAI()              # 同步客户端（主入口）
├── AsyncOpenAI()         # 异步客户端
├── _client.py            # 客户端核心实现
├── types/                # 类型定义（Pydantic 模型 + TypedDict）
├── resources/            # API 资源模块（核心功能）
│   ├── responses         # ⭐ Responses API（新一代推荐接口）
│   ├── chat/             # Chat Completions API（经典接口）
│   ├── embeddings        # 文本嵌入
│   ├── images            # 图像生成/编辑
│   ├── audio             # 语音转文字/文字转语音
│   ├── models            # 模型管理
│   ├── files             # 文件上传/管理
│   ├── fine_tuning/      # 微调任务管理
│   ├── moderations       # 内容审核
│   ├── batches/          # 批量任务
│   ├── uploads/          # 上传管理
│   ├── admin/            # 管理员 API
│   └── ...
├── auth/                 # 认证模块（Workload Identity 等）
├── realtime/             # Realtime API（WebSocket 实时对话）
└── helpers/              # 辅助工具函数
```

---

## 三、核心客户端

### 3.1 同步客户端 `OpenAI`

```python
from openai import OpenAI

client = OpenAI()  # 自动从环境变量读取 OPENAI_API_KEY
```

**主要构造参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `api_key` | `str` | API 密钥 |
| `base_url` | `str` | 自定义 API 基础 URL |
| `organization` | `str` | 组织 ID |
| `project` | `str` | 项目 ID |
| `timeout` | `float / httpx.Timeout` | 请求超时时间 |
| `max_retries` | `int` | 最大重试次数（默认 2） |
| `default_headers` | `dict` | 自定义请求头 |
| `http_client` | `httpx.Client` | 自定义 HTTP 客户端 |

### 3.2 异步客户端 `AsyncOpenAI`

```python
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI()

async def main() -> None:
    response = await client.responses.create(
        model="gpt-4o",
        input="你好！"
    )
    print(response.output_text)

asyncio.run(main())
```

> **同步与异步客户端功能完全一致**，唯一区别是异步客户端需要 `await`。

### 3.3 使用 aiohttp 作为异步后端

```python
import asyncio
from openai import AsyncOpenAI, DefaultAioHttpClient

async def main() -> None:
    async with AsyncOpenAI(
        http_client=DefaultAioHttpClient(),
    ) as client:
        response = await client.responses.create(
            model="gpt-4o",
            input="Hello!"
        )

asyncio.run(main())
```

---

## 四、核心 API 详解

### 4.1 ⭐ Responses API（新一代推荐接口）

> OpenAI 官方推荐的新一代交互接口，于 2025 年推出，用于替代 Chat Completions API。

#### 基础用法

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-4o",
    instructions="你是一个编程助手，说话像海盗。",
    input="Python 中如何检查一个对象是否是某个类的实例？",
)

print(response.output_text)
```

#### 多轮对话

```python
response = client.responses.create(
    model="gpt-4o",
    input=[
        {"role": "user", "content": "什么是机器学习？"},
        {"role": "assistant", "content": "机器学习是人工智能的一个分支..."},
        {"role": "user", "content": "给我举一个例子"},
    ],
)
```

#### 视觉理解（图片输入）

```python
import base64
from openai import OpenAI

client = OpenAI()

# 方式一：通过 URL
response = client.responses.create(
    model="gpt-4o",
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "这张图片里有什么？"},
                {"type": "input_image", "image_url": "https://example.com/image.jpg"},
            ],
        }
    ],
)

# 方式二：通过 Base64 编码
with open("image.png", "rb") as f:
    b64_image = base64.b64encode(f.read()).decode("utf-8")

response = client.responses.create(
    model="gpt-4o",
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "描述这张图片"},
                {"type": "input_image", "image_url": f"data:image/png;base64,{b64_image}"},
            ],
        }
    ],
)
```

#### 流式输出

```python
stream = client.responses.create(
    model="gpt-4o",
    input="写一个关于独角兽的睡前故事。",
    stream=True,
)

for event in stream:
    print(event)
```

#### 指定输出格式（JSON）

```python
response = client.responses.create(
    model="gpt-4o",
    input=[
        {"role": "user", "content": "列出3种编程语言"},
    ],
    response_format={"type": "json_object"},
)
```

#### 工具调用（Function Calling）

```python
import json
from openai import OpenAI

client = OpenAI()

# 定义工具
tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "获取指定城市的天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称",
                },
            },
            "required": ["city"],
        },
    }
]

response = client.responses.create(
    model="gpt-4o",
    input="北京今天天气怎么样？",
    tools=tools,
)

# 解析工具调用
for item in response.output:
    if item.type == "function_call":
        function_name = item.name
        arguments = json.loads(item.arguments)
        print(f"调用函数: {function_name}, 参数: {arguments}")
```

---

### 4.2 Chat Completions API（经典接口）

> 经典的对话补全接口，OpenAI 宣布将长期支持，但推荐新项目使用 Responses API。

#### 基础用法

```python
from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "developer", "content": "你是一个有帮助的助手。"},
        {"role": "user", "content": "你好！"},
    ],
)

print(completion.choices[0].message.content)
```

#### 响应对象结构

```python
completion.id           # 补全 ID，如 "chatcmpl-abc123"
completion.model        # 实际使用的模型
completion.object       # 对象类型，固定为 "chat.completion"
completion.created      # 创建时间戳
completion.choices      # 选择列表
completion.usage        # Token 使用量
```

**`completion.choices[0]` 结构：**

```python
choice.index           # 选择索引
choice.message         # 消息对象
choice.finish_reason   # 结束原因: "stop" | "length" | "tool_calls" | "content_filter"
```

**`completion.usage` 结构：**

```python
usage.prompt_tokens      # 输入 Token 数
usage.completion_tokens  # 输出 Token 数
usage.total_tokens       # 总 Token 数
```

#### 流式输出

```python
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "写一首诗"}],
    stream=True,
)

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

#### 工具调用

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "获取指定城市的当前天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "城市名"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
    }
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "北京天气如何？"}],
    tools=tools,
)

# 检查是否有工具调用
message = response.choices[0].message
if message.tool_calls:
    for tool_call in message.tool_calls:
        print(f"函数: {tool_call.function.name}")
        print(f"参数: {tool_call.function.arguments}")
```

#### 角色说明

| 角色 | 说明 |
|------|------|
| `system` | 系统指令（旧版） |
| `developer` | 开发者指令（新版推荐，替代 system） |
| `user` | 用户消息 |
| `assistant` | 助手回复 |
| `tool` | 工具调用结果 |

---

### 4.3 Embeddings API（文本嵌入）

> 将文本转换为高维向量，用于语义搜索、聚类、推荐等。

```python
from openai import OpenAI

client = OpenAI()

response = client.embeddings.create(
    model="text-embedding-3-small",  # 或 text-embedding-3-large
    input="这段文本将被转换为向量",
    encoding_format="float",         # 或 "base64"
)

# 获取嵌入向量
embedding = response.data[0].embedding
print(f"向量维度: {len(embedding)}")  # small=1536, large=3072
print(f"Token 使用量: {response.usage.total_tokens}")
```

**可用模型：**

| 模型 | 维度 | 最大输入 | 价格 |
|------|------|---------|------|
| `text-embedding-3-small` | 1536 | 8191 tokens | 最低 |
| `text-embedding-3-large` | 3072 | 8191 tokens | 较高 |

**批量嵌入：**

```python
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=["文本一", "文本二", "文本三"],
)

for item in response.data:
    print(f"索引 {item.index}: 向量长度 {len(item.embedding)}")
```

**自定义维度（降维）：**

```python
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="文本",
    dimensions=512,  # 将 1536 维压缩到 512 维
)
```

---

### 4.4 Images API（图像生成）

```python
from openai import OpenAI

client = OpenAI()

# DALL·E 生成图像
response = client.images.generate(
    model="dall-e-3",
    prompt="一只穿着太空服的猫在月球上",
    size="1024x1024",       # 1024x1024, 1792x1024, 1024x1792
    quality="hd",           # "standard" 或 "hd"
    n=1,                    # 生成数量（dall-e-3 仅支持 1）
    response_format="url",  # "url" 或 "b64_json"
)

print(response.data[0].url)  # 图片 URL
```

**编辑图像：**

```python
response = client.images.edit(
    model="dall-e-2",
    image=open("original.png", "rb"),
    mask=open("mask.png", "rb"),    # 遮罩图片（白色=保留，透明=重绘）
    prompt="在背景中添加彩虹",
    size="1024x1024",
)
```

**生成图像变体：**

```python
response = client.images.create_variation(
    model="dall-e-2",
    image=open("image.png", "rb"),
    n=1,
    size="1024x1024",
)
```

---

### 4.5 Audio API（语音处理）

#### 语音转文字（Whisper）

```python
from openai import OpenAI

client = OpenAI()

# 文件转录
with open("audio.mp3", "rb") as audio_file:
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language="zh",              # 指定语言（可选）
        response_format="json",     # json, text, srt, vtt, verbose_json
        prompt="这是一段关于AI的演讲",  # 上下文提示（可选）
    )

print(transcription.text)
```

#### 文字转语音（TTS）

```python
response = client.audio.speech.create(
    model="tts-1",           # 或 "tts-1-hd"（更高质量）
    voice="alloy",           # alloy, echo, fable, onyx, nova, shimmer
    input="你好，欢迎使用 OpenAI 语音合成！",
    response_format="mp3",   # mp3, opus, aac, flac, wav, pcm
    speed=1.0,               # 0.25 ~ 4.0
)

# 保存音频文件
with open("output.mp3", "wb") as f:
    for chunk in response.iter_bytes():
        f.write(chunk)
```

**可用语音：**

| 语音 | 特点 |
|------|------|
| `alloy` | 中性、平衡 |
| `echo` | 男性、温暖 |
| `fable` | 英式、叙事感 |
| `onyx` | 深沉、权威 |
| `nova` | 女性、活力 |
| `shimmer` | 柔和、清晰 |

---

### 4.6 Models API（模型管理）

```python
from openai import OpenAI

client = OpenAI()

# 列出所有可用模型
models = client.models.list()
for model in models.data:
    print(f"{model.id} - {model.owned_by}")

# 获取特定模型详情
model = client.models.retrieve("gpt-4o")
print(model.id, model.created)
```

---

### 4.7 Files API（文件管理）

```python
from pathlib import Path
from openai import OpenAI

client = OpenAI()

# 上传文件
file = client.files.create(
    file=Path("training_data.jsonl"),
    purpose="fine-tune",  # fine-tune, assistants, batch
)
print(f"文件 ID: {file.id}")

# 列出所有文件
files = client.files.list()
for f in files.data:
    print(f"{f.id} - {f.filename} - {f.status}")

# 获取文件信息
file_info = client.files.retrieve("file-abc123")

# 删除文件
client.files.delete("file-abc123")

# 下载文件内容
content = client.files.content("file-abc123")
print(content.text)
```

---

### 4.8 Fine Tuning API（模型微调）

```python
from openai import OpenAI

client = OpenAI()

# 创建微调任务
fine_tune = client.fine_tuning.jobs.create(
    model="gpt-4o-mini",
    training_file="file-abc123",
    hyperparameters={
        "n_epochs": 3,          # 训练轮数
        "batch_size": "auto",   # 批量大小
        "learning_rate_multiplier": "auto",
    },
)

print(f"微调任务 ID: {fine_tune.id}")

# 列出微调任务（自动分页）
for job in client.fine_tuning.jobs.list(limit=20):
    print(f"{job.id} - {job.status} - {job.model}")

# 查看微调任务详情
job = client.fine_tuning.jobs.retrieve("ftjob-abc123")

# 取消微调任务
client.fine_tuning.jobs.cancel("ftjob-abc123")

# 列出微调事件
events = client.fine_tuning.jobs.list_events("ftjob-abc123")
```

---

### 4.9 Moderations API（内容审核）

```python
from openai import OpenAI

client = OpenAI()

response = client.moderations.create(
    model="omni-moderation-latest",
    input="这是一段需要审核的文本内容",
)

result = response.results[0]
print(f"是否违规: {result.flagged}")

# 各类别审核结果
for category, flagged in result.categories.model_dump().items():
    if flagged:
        print(f"  ⚠️ {category}: 违规")
```

**审核类别包括：**
- 暴力 (violence)
- 自残 (self-harm)
- 性内容 (sexual)
- 仇恨 (hate)
- 骚扰 (harassment)

---

### 4.10 Batches API（批量处理）

```python
from openai import OpenAI

client = OpenAI()

# 创建批量任务
batch = client.batches.create(
    input_file_id="file-abc123",
    endpoint="/v1/chat/completions",
    completion_window="24h",  # 24h 或 168h
)

# 列出批量任务
for b in client.batches.list():
    print(f"{b.id} - {b.status} - 请求: {b.request_counts}")

# 取消批量任务
client.batches.cancel("batch_abc123")
```

---

## 五、Realtime API（实时对话）

> 通过 WebSocket 实现低延迟、多模态（文本+语音）的实时对话体验。

### 5.1 基础文本对话

```python
import asyncio
from openai import AsyncOpenAI

async def main() -> None:
    client = AsyncOpenAI()

    async with client.realtime.connect(model="gpt-realtime") as connection:
        # 配置会话
        await connection.session.update(
            session={"type": "realtime", "output_modalities": ["text"]}
        )

        # 发送用户消息
        await connection.conversation.item.create(
            item={
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": "你好！"}],
            }
        )

        # 请求模型回复
        await connection.response.create()

        # 接收事件流
        async for event in connection:
            if event.type == "response.output_text.delta":
                print(event.delta, flush=True, end="")
            elif event.type == "response.output_text.done":
                print()
            elif event.type == "response.done":
                break

asyncio.run(main())
```

### 5.2 错误处理

```python
async with client.realtime.connect(model="gpt-realtime") as connection:
    async for event in connection:
        if event.type == "error":
            print(f"错误类型: {event.error.type}")
            print(f"错误代码: {event.error.code}")
            print(f"错误信息: {event.error.message}")
            # 连接不会断开，可以继续使用
```

---

## 六、Workload Identity 认证

> 适用于 Kubernetes、Azure、GCP 等云环境，使用短期令牌替代长期 API Key。

### 6.1 Kubernetes（Service Account Token）

```python
from openai import OpenAI
from openai.auth import k8s_service_account_token_provider

client = OpenAI(
    workload_identity={
        "identity_provider_id": "idp-123",
        "service_account_id": "sa-456",
        "provider": k8s_service_account_token_provider(
            "/var/run/secrets/kubernetes.io/serviceaccount/token"
        ),
    },
)
```

### 6.2 Azure（Managed Identity）

```python
from openai import OpenAI
from openai.auth import azure_managed_identity_token_provider

client = OpenAI(
    workload_identity={
        "identity_provider_id": "idp-123",
        "service_account_id": "sa-456",
        "provider": azure_managed_identity_token_provider(
            resource="https://management.azure.com/",
        ),
    },
)
```

### 6.3 GCP（Compute Engine Metadata）

```python
from openai import OpenAI
from openai.auth import gcp_id_token_provider

client = OpenAI(
    workload_identity={
        "identity_provider_id": "idp-123",
        "service_account_id": "sa-456",
        "provider": gcp_id_token_provider(audience="https://api.openai.com/v1"),
    },
)
```

### 6.4 自定义 Token Provider

```python
from openai import OpenAI

def get_custom_token() -> str:
    """获取自定义 JWT Token"""
    return "your-jwt-token"

client = OpenAI(
    workload_identity={
        "identity_provider_id": "idp-123",
        "service_account_id": "sa-456",
        "provider": {
            "token_type": "jwt",
            "get_token": get_custom_token,
        },
    }
)
```

---

## 七、类型系统

### 7.1 请求参数（TypedDict）

嵌套请求参数使用 `TypedDict` 类型，提供编辑器自动补全：

```python
from openai import OpenAI

client = OpenAI()

# response_format 参数有类型提示
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}],
    response_format={"type": "json_object"},  # TypedDict
)
```

### 7.2 响应对象（Pydantic 模型）

响应对象是 Pydantic 模型，提供实用方法：

```python
response = client.responses.create(...)

# 序列化为 JSON
json_str = response.to_json()

# 转换为字典
data_dict = response.to_dict()
```

### 7.3 VS Code 类型检查

在 VS Code 的 `settings.json` 中设置：

```json
{
    "python.analysis.typeCheckingMode": "basic"
}
```

---

## 八、分页（Pagination）

### 8.1 自动分页迭代

```python
from openai import OpenAI

client = OpenAI()

# 自动获取所有页
all_jobs = []
for job in client.fine_tuning.jobs.list(limit=20):
    all_jobs.append(job)
```

### 8.2 异步自动分页

```python
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI()

async def main() -> None:
    all_jobs = []
    async for job in client.fine_tuning.jobs.list(limit=20):
        all_jobs.append(job)

asyncio.run(main())
```

### 8.3 手动分页控制

```python
first_page = client.fine_tuning.jobs.list(limit=20)

# 检查是否有下一页
if first_page.has_next_page():
    print(f"下一页信息: {first_page.next_page_info()}")
    next_page = first_page.get_next_page()

# 直接访问数据
print(f"游标: {first_page.after}")
for job in first_page.data:
    print(job.id)
```

---

## 九、错误处理

### 9.1 异常层次结构

```
openai.APIError                    # 所有 API 错误的基类
├── openai.APIConnectionError      # 网络连接错误
├── openai.RateLimitError          # 速率限制错误（429）
├── openai.APIStatusError          # HTTP 状态码错误
│   ├── openai.BadRequestError     # 400 - 请求参数错误
│   ├── openai.AuthenticationError # 401 - 认证失败
│   ├── openai.PermissionDeniedError # 403 - 权限不足
│   ├── openai.NotFoundError       # 404 - 资源不存在
│   ├── openai.ConflictError       # 409 - 资源冲突
│   └── openai.UnprocessableEntityError # 422 - 无法处理的实体
└── openai.APIResponseValidationError # 响应验证错误
```

### 9.2 错误处理最佳实践

```python
from openai import OpenAI, APIError, RateLimitError, APIConnectionError

client = OpenAI()

try:
    response = client.responses.create(
        model="gpt-4o",
        input="你好！",
    )

except RateLimitError as e:
    """速率限制：等待后重试"""
    import time
    retry_after = float(e.response.headers.get("retry-after", 5))
    print(f"速率限制，等待 {retry_after} 秒后重试...")
    time.sleep(retry_after)

except APIConnectionError as e:
    """网络连接错误"""
    print(f"网络连接失败: {e}")

except APIError as e:
    """其他 API 错误"""
    print(f"API 错误: {e.status_code} - {e.message}")
```

---

## 十、Webhook 验证

```python
from openai import OpenAI
from flask import Flask, request

app = Flask(__name__)
client = OpenAI()

@app.route("/webhooks", methods=["POST"])
def webhook() -> dict:
    """处理 OpenAI Webhook 事件"""
    try:
        # 验证签名并解析 payload
        event = client.webhooks.unwrap(
            body=request.data.decode("utf-8"),
            headers=request.headers,
        )
        print(f"收到事件: {event.type}")
        return {"status": "ok"}

    except Exception as e:
        print(f"Webhook 验证失败: {e}")
        return {"status": "error"}, 400
```

---

## 十一、高级用法

### 11.1 自定义 HTTP 客户端

```python
import httpx
from openai import OpenAI

# 自定义超时和重试
client = OpenAI(
    http_client=httpx.Client(
        timeout=httpx.Timeout(60.0, connect=10.0),
        limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
    ),
)
```

### 11.2 代理设置

```python
import httpx
from openai import OpenAI

client = OpenAI(
    http_client=httpx.Client(proxy="http://your-proxy:8080"),
)
```

### 11.3 日志记录

```python
import logging

# 启用 httpx 日志
logging.basicConfig(level=logging.DEBUG)
```

### 11.4 结构化输出（Structured Outputs）

```python
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI()

# 定义输出结构
class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

response = client.responses.parse(
    model="gpt-4o",
    input="下周三下午3点，Alice 和 Bob 开会讨论项目进度",
    text_format=CalendarEvent,
)

event = response.output_parsed
print(f"事件: {event.name}")
print(f"日期: {event.date}")
print(f"参与者: {event.participants}")
```

---

## 十二、Responses API vs Chat Completions API 对比

| 特性 | Responses API | Chat Completions API |
|------|--------------|---------------------|
| 状态 | ⭐ 新一代推荐 | 经典接口（长期支持） |
| 入口 | `client.responses.create()` | `client.chat.completions.create()` |
| 系统指令 | `instructions` 参数 | `messages` 中的 `system/developer` 角色 |
| 输入格式 | `input` 参数 | `messages` 参数 |
| 输出获取 | `response.output_text` | `completion.choices[0].message.content` |
| 多模态 | 原生支持 | 原生支持 |
| 工具调用 | 更简洁的工具定义 | 经典 function calling |
| 结构化输出 | `response.parse()` + Pydantic | `response_format` |
| 流式输出 | SSE 事件流 | SSE 块流 |
| Agent 能力 | 内置支持 | 需要自行实现 |

---

## 十三、最佳实践

### 13.1 安全性
- ✅ 使用环境变量或 `.env` 文件存储 API Key
- ✅ 将 `.env` 添加到 `.gitignore`
- ✅ 在生产环境使用 Workload Identity
- ❌ 不要将 API Key 硬编码在代码中

### 13.2 性能优化
- 使用异步客户端 (`AsyncOpenAI`) 处理高并发
- 合理设置 `timeout` 和 `max_retries`
- 使用流式输出 (`stream=True`) 提升用户体验
- 批量请求使用 Batches API

### 13.3 成本控制
- 选择合适的模型（gpt-4o-mini 比 gpt-4o 便宜 10 倍）
- 控制 `max_tokens` 参数限制输出长度
- 使用 Embeddings 做缓存减少重复调用
- 监控 `usage` 字段跟踪 Token 消耗

---

## 十四、常用依赖

```
openai
├── httpx          # HTTP 客户端（必需）
├── pydantic       # 数据验证（必需）
├── anyio          # 异步支持（必需）
├── distro         # 系统信息（必需）
├── typing-extensions  # 类型扩展（必需）
├── aiohttp        # 可选异步后端
└── python-dotenv  # 推荐：环境变量管理
```

---

> **参考文档：**
> - 官方 API 文档: https://platform.openai.com/docs/api-reference
> - SDK 完整 API: https://github.com/openai/openai-python/blob/main/api.md
> - GitHub 仓库: https://github.com/openai/openai-python
