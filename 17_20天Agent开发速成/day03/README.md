---
name: Day03 - 大模型API深度使用 + 评估指标（面试高频）
description: Day03 完整学习计划：精确到分钟，每个知识点对应面试考点，统一接口封装 + Agent效果评估
type: learning
tags: ["大模型API", "流式输出", "评估指标", "统一接口", "降级策略", "面试"]
created_at: 2026-05-21
updated_at: 2026-05-21
version: interview
---

# 🚀 Day 03：大模型 API 深度使用 + 评估指标（面试高频）

- **学习日期**：第 3 天 / 共 20 天
- **学习时长**：8 小时（精确到分钟）
- **核心目标**：能写出兼容 3 家模型的统一接口层，能设计完整的 Agent 效果评估方案，掌握 Token 成本优化

---

## ⏰ 今日学习时间表（精确到分钟）

| 时间段 | 学习内容 | 完成情况 |
|--------|---------|---------|
| **09:00-10:00** | OpenAI API 完整指南：流式/非流式、错误重试 | ⬜️ / ✅ |
| **10:00-11:00** | 国产模型对比：DeepSeek、Qwen、通义千问、文心一言 | ⬜️ / ✅ |
| **11:00-12:00** | Token 计费原理 + 成本估算 + 成本优化 5 大招 | ⬜️ / ✅ |
| **14:00-15:00** | 统一接口层封装：换模型只需要改一行配置 | ⬜️ / ✅ |
| **15:00-16:00** | 降级策略：模型挂了怎么办？怎么优雅降级？ | ⬜️ / ✅ |
| **16:00-17:00** | ML基础：评估指标（准确率、精确率、召回率、F1） | ⬜️ / ✅ |
| **19:00-20:00** | 【面试题专项】Day03 7 道大模型 API 面试题 | ⬜️ / ✅ |
| **20:00-21:00** | 复盘 + 整理面试话术 + 统一接口代码实战 | ⬜️ / ✅ |

---

## 🎯 09:00-10:00：OpenAI API 完整指南

### 📝 核心知识点 + 对应面试考点

#### 知识点 1：流式输出原理
- **面试考点**：流式输出的原理是什么？有什么好处？
- **回答要点**：
  1. SSE（Server-Sent Events）技术
  2. 分块生成，逐字返回，用户体验好
  3. 降低首字延迟（TTFT），不需要等完整生成
  4. 内存占用小，适合长文本生成

#### 知识点 2：非流式 vs 流式
- **面试考点**：什么时候用流式，什么时候用非流式？
- **回答要点**：
  1. 流式：聊天、写作、实时交互场景
  2. 非流式：API调用、批量处理、需要完整结果才继续
  3. Agent内部思考：一般用非流式，用户界面：用流式

#### 知识点 3：错误类型
- **面试考点**：大模型 API 常见错误有哪些？怎么处理？
- **回答要点**：
  1. 429：限流 → 指数退避重试
  2. 401：认证失败 → 检查 API Key
  3. 400：参数错误 → 检查输入格式
  4. 5xx：服务端错误 → 重试或降级

### 💻 必写代码 1：流式输出完整实现

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

# 流式输出
def stream_chat(messages):
    response = client.chat.completions.create(
        model="gpt-5.4",
        messages=messages,
        stream=True  # 关键参数
    )
    
    full_content = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            full_content += content
            print(content, end="", flush=True)  # 逐字打印
    
    return full_content

# 非流式输出
def normal_chat(messages):
    response = client.chat.completions.create(
        model="gpt-5.4",
        messages=messages,
        stream=False
    )
    return response.choices[0].message.content

# 使用
messages = [{"role": "user", "content": "什么是大模型 Agent？"}]
print("流式输出：")
stream_chat(messages)
print("\n\n非流式输出：")
print(normal_chat(messages))
```

### 💻 必写代码 2：指数退避重试装饰器

```python
import time
import random
from functools import wraps

def retry_with_exponential_backoff(
    max_retries=5,
    initial_delay=1,
    max_delay=30,
    backoff_factor=2,
    jitter=True
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise  # 最后一次重试失败，抛出异常
                    
                    # 计算延迟时间
                    if jitter:
                        delay = min(max_delay, delay * backoff_factor) * random.uniform(0.5, 1.5)
                    else:
                        delay = min(max_delay, delay * backoff_factor)
                    
                    print(f"第 {attempt + 1} 次尝试失败，{delay:.1f}秒后重试：{str(e)}")
                    time.sleep(delay)
            
            return None
        return wrapper
    return decorator

# 使用
@retry_with_exponential_backoff(max_retries=5)
def chat_with_retry(messages):
    return client.chat.completions.create(
        model="gpt-5.4",
        messages=messages
    )
```

### ⭐ 面试官追问：指数退避为什么要加 jitter（随机抖动）？

> **3分钟回答模板**：
> 
> 指数退避加 jitter 是为了避免「惊群效应」（Thundering Herd）。假设没有 jitter，100 个请求同时遇到 429 错误，它们会在 1 秒后同时重试，然后 2 秒后又同时重试，4 秒后又同时重试... 这样会形成请求风暴，把服务打垮。
> 
> 加上随机抖动后，每个请求的重试时间会分散开，不会同时打过去，能让服务更平滑地恢复。这是分布式系统中非常经典的设计思想。

---

## 🎯 10:00-11:00：主流模型对比与选型（2026-05 最新格局）

> 📆 **时效快照**：本节针对 2026-05-22 产客能拿到的主流模型状态。大模型迭代速度 ~2.8 天/款，每 2-3 个月建议重刷一次对比表。

### 📝 核心知识点 + 对应面试考点

#### 知识点 1：模型选型
- **面试考点**：各个模型的优缺点是什么？怎么选型？
- **回答要点**：
  1. GPT-5.5：旗舰通用，代码+Agent 最强，但贵
  2. Claude Opus 4.7：编程 SWE-bench 王者，工具调用最稳
  3. DeepSeek V4：性价比之王（约 .42/.84），开源可私部
  4. Gemini 3.1 Pro：多模态像素级最强，1M 上下文
  5. 国产：Kimi K2.6 多智能体并行、GLM-5.1 代码跨文件理解

#### 知识点 2：成本对比
- **面试考点**：不同模型的成本差异有多大？
- **回答要点**：
  1. GPT-5.5: / per 1M tokens
  2. Claude Opus 4.7: /
  3. Claude Sonnet 4.6: /（≈Opus 1/5 价，性能接近）
  4. DeepSeek V4 Pro: ≈.42/.84（2.5折优惠期）
  5. DeepSeek V4 Flash: ≈.14/.28
  6. **旗舰 vs 性价比差距约 10-60 倍

#### 知识点 3：能力差异
- **面试考点**：国产模型和 GPT 比，能力差距在哪里？
- **回答要点**：
  1. Agent 编码：GPT-5.5 / Claude Opus 4.7 领先，SWE-bench 明显强
  2. 工具调用：Claude 最稳，GPT 次之，国产 V4 已大幅改善
  3. 多模态：Gemini 像素级空间定位独一无二
  4. 中文：国产模型更好，本土文化/公文/成语理解强
  5. 开源私部：DeepSeek V4 MIT 协议，Kimi K2.5 Apache 2.0

### 📊 主流模型详细对比表（2026-05）

| 模型 | 价格（输入/输出 per 1M） | 上下文 | 代码能力 | Agent能力 | 推理能力 | 推荐场景 |
|------|------------------------|-------|---------|----------|---------|---------|
| **GPT-5.5** |  /  | 1M | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 旗舰通用、复杂 Agent、编码 |
| **GPT-5.4** | .5 /  | 1M | ⭐⭐⭐⭐½ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐½ | 中高负载、成本可控 |
| **Claude Opus 4.7** |  /  | 200K | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 编程之王、安全合规 |
| **Claude Sonnet 4.6** |  /  | 200K | ⭐⭐⭐⭐½ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **性价比首选**、大规模部署 |
| **Gemini 3.1 Pro** | ~ / ~ | 1M | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐½ | 多模态、视频、1M上下文 |
| **DeepSeek V4 Pro** | ≈.42 / .84 | 128K | ⭐⭐⭐⭐ | ⭐⭐⭐½ | ⭐⭐⭐⭐ | 开源私部、极致性价比 |
| **DeepSeek V4 Flash** | ≈.14 / .28 | 128K | ⭐⭐⭐½ | ⭐⭐⭐ | ⭐⭐⭐½ | 大批量/低延迟/成本敏感 |
| **Kimi K2.6** | 旗舰区间 | 1M+ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐½ | ⭐⭐⭐⭐ | 多智能体并行、开源私部 |
| **GLM-5.1** | 中端 | 200K | ⭐⭐⭐⭐½ | ⭐⭐⭐½ | ⭐⭐⭐⭐ | 跨文件代码理解、企业合规 |
| **Qwen3-Max** | 中端 | 128K+ | ⭐⭐⭐½ | ⭐⭐⭐ | ⭐⭐⭐⭐ | 中文场景、本地部署 |

### 💡 选型决策树（2026 版）

`
开始
  ↓
有数据合规/不出境要求吗？
  ├─ 是 → 只能选国产模型
  │      ├─ 需要本地化部署 → DeepSeek V4（MIT 开源）/ Kimi K2.5（Apache 2.0）
  │      ├─ 编码为主 → GLM-5.1
  │      └─ 通用+性价比 → DeepSeek V4 Pro / Qwen3-Max
  └─ 否 → 可以用海外模型
         ├─ Agent 编码核心逻辑 → Claude Opus 4.7（SWE-bench 最强）
         ├─ 通用旗舰 + Operator → GPT-5.5
         ├─ 多模态/视频/1M 上下文 → Gemini 3.1 Pro
         ├─ 大规模部署 + 成本敏感 → Claude Sonnet 4.6（Opus 1/5 价）
         └─ 极致性价比 → DeepSeek V4 Flash（≈旗舰 1/60 价）
`

### ⭐ 面试加分：2026 大模型格局的 3 个关键趋势

> **3 分钟回答模板**：
>
> **趋势一：从「生成」到「行动」**。2026 年竞争核心不是谁跑分高，而是谁的 Agent 编码能力强——编码能力直接决定 Agent 成功率、执行时间和 Token 消耗。Coding 强弱 = Agent 好不好用。
>
> **趋势二：成本效益成主战场**。Claude Sonnet 4.6 以 Opus 1/5 的价格提供了接近 Opus 的性能，直接颠覆了定价逻辑。企业选型从「最强」转向「最合适的性价比」。
>
> **趋势三：开源追赶闭源**。DeepSeek V4 和 Kimi K2.5/K2.6 在 Agent benchmark 上已经逼近 GPT-5.4 水平，且完全开源可私部。对数据安全敏感的企业，开源模型的竞争力已经够用了。

---

## 🎯 11:00-12:00：Token 计费原理与成本优化

### 📝 核心知识点 + 对应面试考点

#### 知识点 1：Token 定义
- **面试考点**：1K Token 大概是多少字？中英文有区别吗？
- **回答要点**：
  1. 英文：约 750 个单词 = 1K Token
  2. 中文：约 500 个汉字 = 1K Token（因为中文每个字占 2 个 Token）
  3. 所以同样长度的中文，Token 消耗是英文的 1.5 倍

#### 知识点 2：计费方式
- **面试考点**：Token 是怎么计费的？输入和输出分开算吗？
- **回答要点**：
  1. 输入 Token：你的 prompt 长度，算一次
  2. 输出 Token：模型生成的内容，算一次
  3. 输出通常比输入贵 2-3 倍
  4. 长上下文模型 Token 单价更贵

#### 知识点 3：成本优化
- **面试考点**：怎么降低 Token 成本？
- **回答要点**：
  1. 用更便宜的模型（降本 5-10 倍）
  2. 精简 System Prompt，去掉废话
  3. 上下文压缩，只保留相关信息
  4. 输出限制长度，不要让模型瞎扯
  5. 批量处理，减少 API 调用次数

### 💻 必写代码 3：Token 计数工具

```python
import tiktoken

def count_tokens(text: str, model: str = "gpt-5.4") -> int:
    """计算文本的 Token 数量"""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def count_messages_tokens(messages: list, model: str = "gpt-5.4") -> int:
    """计算对话消息的总 Token 数量"""
    encoding = tiktoken.encoding_for_model(model)
    
    # 每轮消息有固定开销
    tokens_per_message = 3
    tokens_per_name = 1
    
    total_tokens = 0
    for message in messages:
        total_tokens += tokens_per_message
        for key, value in message.items():
            total_tokens += len(encoding.encode(value))
            if key == "name":
                total_tokens += tokens_per_name
    
    # 最后有固定的 3 个 Token 开销
    total_tokens += 3
    return total_tokens

# 使用示例
text = "你好，我想了解一下什么是大模型 Agent。"
print(f"文本 Token 数：{count_tokens(text)}")

messages = [
    {"role": "system", "content": "你是一个 helpful 的助手。"},
    {"role": "user", "content": "什么是大模型 Agent？"}
]
print(f"对话 Token 数：{count_messages_tokens(messages)}")

# 成本估算（GPT-5.4: $2.5/1M 输入，$10/1M 输出，2026-05 价）
input_tokens = count_messages_tokens(messages)
output_tokens = 100  # 假设输出 100 Token
input_cost = input_tokens * 2.5 / 1_000_000
output_cost = output_tokens * 10.0 / 1_000_000
print(f"预估成本：${input_cost + output_cost:.6f}")
```

### 📊 成本优化 5 大招效果对比

| 优化方法 | 降本幅度 | 实现难度 | 对效果影响 |
|---------|---------|---------|-----------|
| 换更便宜的模型 | 50-90% | ⭐ | 可能有轻微下降 |
| 精简 System Prompt | 10-30% | ⭐⭐ | 几乎无影响 |
| 上下文压缩 | 30-70% | ⭐⭐⭐ | 可能丢失关键信息 |
| 限制输出长度 | 20-50% | ⭐ | 可控 |
| 缓存重复请求 | 0-90% | ⭐⭐⭐ | 完全相同的请求效果好 |

---

## 🎯 14:00-15:00：统一接口层封装

### 📝 核心知识点 + 对应面试考点

#### 知识点 1：为什么要封装
- **面试考点**：为什么要设计统一接口层？直接调 SDK 不行吗？
- **回答要点**：
  1. 换模型不需要改业务代码，只改配置
  2. 统一错误处理、重试、日志
  3. 方便添加监控和统计
  4. 符合开闭原则：对扩展开放，对修改关闭

#### 知识点 2：设计模式
- **面试考点**：用什么设计模式来设计统一接口层？
- **回答要点**：
  1. 策略模式：每个模型一个策略类
  2. 工厂模式：根据配置创建对应的实例
  3. 适配器模式：统一不同 SDK 的接口

#### 知识点 3：抽象维度
- **面试考点**：统一接口需要抽象哪些维度？
- **回答要点**：
  1. chat 方法：输入 messages，输出响应
  2. stream_chat 方法：流式输出
  3. embed 方法：文本向量化
  4. 通用参数：model, temperature, max_tokens

### 💻 必写代码 4：统一接口层完整实现

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Generator

class BaseLLM(ABC):
    """LLM 抽象基类"""
    
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """非流式聊天"""
        pass
    
    @abstractmethod
    def stream_chat(self, messages: List[Dict[str, str]], **kwargs) -> Generator[str, None, None]:
        """流式聊天"""
        pass

class OpenAILLM(BaseLLM):
    """OpenAI 模型实现"""

    def __init__(self, api_key: str, model: str = "gpt-5.4"):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 2000),
        )
        return response.choices[0].message.content

    def stream_chat(self, messages, **kwargs):
        response = self.client.chat.completions.create(
            model=self.model, messages=messages, stream=True,
        )
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


class DeepSeekLLM(BaseLLM):
    """DeepSeek 国产模型实现（兼容 OpenAI SDK）"""

    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")
        self.model = model

    def chat(self, messages, **kwargs):
        response = self.client.chat.completions.create(
            model=self.model, messages=messages,
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 2000),
        )
        return response.choices[0].message.content

    def stream_chat(self, messages, **kwargs):
        response = self.client.chat.completions.create(
            model=self.model, messages=messages, stream=True,
        )
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


class LLMFactory:
    """LLM 工厂类"""

    @staticmethod
    def create_llm(llm_type: str, **kwargs) -> BaseLLM:
        llm_map = {"openai": OpenAILLM, "deepseek": DeepSeekLLM}
        if llm_type not in llm_map:
            raise ValueError(f"不支持的模型: {llm_type}")
        return llm_map[llm_type](**kwargs)


# 使用示例：换模型只需要改一行配置
config = {"llm_type": "deepseek", "api_key": "xxx", "model": "deepseek-chat"}
llm = LLMFactory.create_llm(**config)
result = llm.chat([{"role": "user", "content": "什么是 Agent？"}])
```

### ⭐ 面试官追问：抽象类（ABC）和接口（interface）有什么区别？

> **3 分钟回答模板**：
>
> Python 没有原生的 interface，用 `abc.ABC` + `@abstractmethod` 模拟接口。区别在于：抽象类可以有默认实现的具体方法，子类可以选择性覆盖；而纯接口只定义方法签名。在统一接口层这种场景下，BaseLLM 里通常只放抽象方法，让子类必须实现 chat 和 stream_chat，保证所有 LLM 都遵循同一份契约——这就是「面向接口编程」。

---

## 🎯 15:00-16:00：降级策略——模型挂了怎么办？

### 📝 核心知识点 + 对应面试考点

#### 知识点 1：为什么需要降级
- **面试考点**：大模型 API 不稳定会带来什么问题？
- **回答要点**：
  1. OpenAI/DeepSeek 都有过大面积宕机
  2. 单点依赖 = 单点故障
  3. 没降级 = 全线业务挂掉
  4. 生产系统必须多模型 + 自动切换

#### 知识点 2：降级三件套
- **面试考点**：降级、熔断、限流三者区别？
- **回答要点**：
  1. **降级**：A 模型挂了切 B 模型，保证服务可用
  2. **熔断**：连续失败 N 次，暂停调用一段时间避免雪崩
  3. **限流**：QPS 太高时主动拒绝，保护下游

#### 知识点 3：优先级排序
- **面试考点**：降级链怎么排序？
- **回答要点**：
  1. 按效果排：GPT-5.5 → Claude Opus 4.7 → DeepSeek V4
  2. 按成本排：DeepSeek V4 Flash → Sonnet 4.6 → GPT-5.4
  3. 实战中混合：高优场景按效果，常规场景按成本

### 💻 必写代码 5：降级策略（含熔断）

```python
import time
from typing import List

class FallbackLLM:
    """带熔断的多模型降级器"""

    def __init__(self, llm_chain: List[BaseLLM], failure_threshold: int = 3, recovery_seconds: int = 60):
        self.llm_chain = llm_chain  # 按优先级排序的模型列表
        self.failure_threshold = failure_threshold
        self.recovery_seconds = recovery_seconds
        # 每个模型的失败计数与熔断时间
        self.state = {id(llm): {"failures": 0, "blocked_until": 0} for llm in llm_chain}

    def _is_available(self, llm) -> bool:
        """检查模型是否处于熔断恢复期"""
        return time.time() >= self.state[id(llm)]["blocked_until"]

    def _record_failure(self, llm):
        s = self.state[id(llm)]
        s["failures"] += 1
        if s["failures"] >= self.failure_threshold:
            s["blocked_until"] = time.time() + self.recovery_seconds
            s["failures"] = 0  # 重置，等恢复后再算
            print(f"⚡ 模型 {llm.__class__.__name__} 已熔断 {self.recovery_seconds}s")

    def _record_success(self, llm):
        self.state[id(llm)]["failures"] = 0

    def chat(self, messages, **kwargs) -> str:
        last_err = None
        for llm in self.llm_chain:
            if not self._is_available(llm):
                continue  # 跳过被熔断的模型
            try:
                result = llm.chat(messages, **kwargs)
                self._record_success(llm)
                return result
            except Exception as e:
                last_err = e
                self._record_failure(llm)
                print(f"❌ {llm.__class__.__name__} 调用失败：{e}，切下一个")
        raise RuntimeError(f"所有模型均不可用，最后错误：{last_err}")


# 使用：DeepSeek V4 优先（便宜），Sonnet 4.6 兜底，GPT-5.5 最后保命
fallback_llm = FallbackLLM([
    DeepSeekLLM(api_key="xxx"),
    OpenAILLM(api_key="xxx", model="gpt-5.4"),
    OpenAILLM(api_key="xxx", model="gpt-5.5"),
])
result = fallback_llm.chat([{"role": "user", "content": "你好"}])
```

### ⭐ 面试官追问：熔断为什么要有「半开」状态？

> **3 分钟回答模板**：
>
> 熔断器有三个状态：关闭（正常调用）、打开（直接拒绝）、半开（试探性放一个请求过去）。
>
> 如果只有「打开」和「关闭」两个状态，熔断时间到了之后会突然把所有请求都放过去，万一下游还没恢复，瞬间就被打挂，又回到熔断状态——这就是「重试风暴」。
>
> 半开状态的作用是：熔断时间到了之后，先只放 1 个请求过去试探，成功了才完全恢复，失败了立刻回到打开状态再等一个周期。这样可以避免「假性恢复」造成的二次雪崩。Hystrix、Resilience4j、Sentinel 都是这个套路。

---

## 🎯 16:00-17:00：ML 基础——评估指标（面试高频！）

> 📖 **本段完整内容见同目录下的**：[评估指标与Agent效果评估.md](评估指标与Agent效果评估.md)。下面是面试背诵版。

### 📝 核心考点速查表

#### 分类指标（4 大核心）

| 指标 | 公式 | 一句话记忆 | 适用场景 |
|------|------|-----------|---------|
| **准确率 Accuracy** | (TP+TN)/全部 | 整体预测对不对 | 样本均衡的分类 |
| **精确率 Precision** | TP/(TP+FP) | 别误报，宁放过不杀错 | 垃圾邮件、司法判决 |
| **召回率 Recall** | TP/(TP+FN) | 别漏报，宁杀错不放过 | 新冠检测、癌症筛查 |
| **F1** | 2PR/(P+R) | 两者的调和平均 | 两者都重要 |

#### 回归指标（5 大核心）

| 指标 | 公式 | 一句话记忆 | 适用场景 |
|------|------|-----------|---------|
| **MAE** | Σ\|y-ŷ\|/n | 平均偏了多少 | 要可解释、对异常值鲁棒 |
| **MSE** | Σ(y-ŷ)²/n | 重罚大误差 | 损失函数首选 |
| **RMSE** | √MSE | MSE 开根，与 y 同量纲 | Kaggle 、对外报告 |
| **R²** | 1-SSres/SStot | 比猜均值好多少 | 模型解释力 |
| **MAPE** | 平均偏差% | 偏了百分之多少 | 业务方沟通 |

> 💡 **面试一句话区分**：分类看「预测对不对」，回归看「预测偏了多少」。

### ⭐ 面试高频 3 问

**1）准确率 99.9% 为什么还可能完全没用？**
样本不均衡。例：1000 封邮件 999 正常 + 1 垃圾，全预测为正常，准确率 99.9% 但垃圾邮件召回率 0%。原因是准确率被多数类带偏了，完全遮蔽了少数类的表现。

**2）精确率和召回率为什么是此消彼长？**
阈值调低→预测为正例变多→召回率上升，但 FP 也变多→精确率下降。阈值调高反之。要看业务上 FP 和 FN 哪个代价更大来选。

**3）F1 为什么用调和平均而不是算术平均？**
调和平均会被小的那个拉低。P=0.1, R=1.0，算术平均 0.55、F1=0.18。这保证了只有 P 和 R 都高时 F1 才会高，避免「单边倒」骗 F1。

### 📊 对齐 Agent 场景：Agent 上怎么用这些指标？

| Agent 评估题 | 属于什么指标 | 举例 |
|----------------|-----------------|------|
| 工具选择是否正确 | 分类问题 | 该调搜索的调了计算器→FN |
| 参数提取是否准确 | 抓取 / 召回 | 含日期/金额的 NER |
| RAG 检索是否命中 | 召回率@K | 前 K 个中是否含金文档 |
| RAG 生成是否准确 | 事实一致性 | 需大模型打分或人工判定 |

---

## 🎯 19:00-20:00：【面试题专项】Day03 7 道大模型 API 面试题

> 📖 **完整题目见**：[面试题.md](面试题.md) | **标准答案见**：[面试题_标准答案.md](面试题_标准答案.md)

### 📝 题目清单

| # | 题目 | 难度 | 时长 |
|---|------|------|------|
| 1 | 流式输出的原理是什么？有什么好处？ | ⭐ | 2 分钟 |
| 2 | 1K Token 大概是多少字？中英文有区别吗？Token 是怎么计费的？ | ⭐ | 2 分钟 |
| 3 | 精确率和召回率的区别是什么？分别在什么场景下使用？ | ⭐⭐ | 3 分钟 |
| 4 | 指数退避重试为什么要加 jitter（随机抖动）？不加会有什么问题？ | ⭐⭐⭐ | 3 分钟 |
| 5 | 为什么要设计统一接口层？直接调用各家 SDK 不行吗？用什么设计模式？ | ⭐⭐⭐ | 3 分钟 |
| 6 | 准确率有什么陷阱？举一个准确率很高但模型完全没用的例子。 | ⭐⭐⭐ | 3 分钟 |
| 7 | 怎么设计一个完整的 Agent 效果评估方案？从哪些维度评估？ | ⭐⭐⭐⭐ | 5 分钟 |

### 🎯 答题节奏建议

1. **前 3 道基础题**：3×2 + 1 = 7 分钟，控制在 10 分钟内
2. **进阶 3 道**：3×3 = 9 分钟，控制在 15 分钟内
3. **开放题 1 道**：5 分钟回答 + 5 分钟自我点评

### ❗ 必背 3 个一句话杀手锏

1. **流式输出**：「SSE 长连接、TTFT 低、用户感知像真人打字。」
2. **jitter**：「不加就是请求风暴，服务被重试自己打死，叫惊群效应。」
3. **准确率陷阱**：「999 正 1 负，全预测正，准确率 99.9%，但 1 个垃圾邮件都没抓到。」

---

## 🎯 20:00-21:00：复盘 + 整理面试话术 + 统一接口代码实战

### ✅ 今日学习自检清单

- [ ] 能默写指数退避重试装饰器，且能讲清楚 jitter 的作用
- [ ] 能默写统一接口层 BaseLLM + LLMFactory 的骨架
- [ ] 能讲清楚 TP/FP/FN/TN、精确率、召回率、F1 的公式与场景
- [ ] 能举出 3 个看精确率的场景、3 个看召回率的场景
- [ ] 能讲清楚熔断器三态（关闭/打开/半开）
- [ ] 能讲清楚 Agent 评估 4 维度：正确性 / 工具使用 / 效率 / 用户体验

### 📝 必背话术（背到脱口而出）

#### 话术 1：流式输出为什么好
> 流式基于 SSE 长连接，模型每生成一个 token 就 push 一个 token。好处有三：用户体验逐字显示像真人打字、首字延迟 TTFT 从几秒降到几百毫秒、服务端不用缓存完整响应。Agent 内部链路用非流式，对用户的 UI 层用流式。

#### 话术 2：为什么需要统一接口层
> 直接调 SDK 当然能跑，但项目大了换模型要改业务代码，每处都要写错误处理重试，违反开闭原则。统一接口层用策略模式（每个模型一个策略类）+ 工厂模式（按配置创建）+ 适配器模式（统一不同 SDK），把模型选择从代码问题变成配置问题。

#### 话术 3：怎么评估 Agent 效果
> 五步法：定测试集（覆盖正常/边界/异常，每场景 20-30 例）→ 定指标（正确性 P/R/F1、工具使用成功率、效率耗时/Token、用户体验 1-5 分）→ 自动化跑批 → Bad Case 分类复盘 → 持续迭代版本对比。一句话：没有量化就没有优化。

### 💻 实战练习（必做）

1. 跑通 `code/04_unified_llm_interface.py`，把 DeepSeek 和 OpenAI 都接上
2. 跑通 `code/05_fallback_strategy.py`，模拟主模型挂掉，看降级是否生效
3. 用 `code/03_token_counter.py` 算一下你昨天的 Prompt 一次调用成本是多少
4. 把 `评估指标与Agent效果评估.md` 中的 AgentEvaluator 改成你自己业务的评估脚本

### 🎯 明日预告：Day04

- Function Calling 底层原理与最佳实践
- 工具参数 JSON Schema 设计
- 工具调用错误处理与重试
- 多工具选择策略（智能路由）
- 实战：搭建一个能查天气 + 算账单 + 发邮件的多工具 Agent

---

## 🏁 Day03 收尾

> **一句话总结**：模型是变量，工程是常量。今天把「换模型只改一行配置」「挂了能自动切」「效果能量化评估」三件事做完，Agent 工程化就上了一个台阶。

**✅ Day03 完成！继续保持节奏，明天 Function Calling！🚀**


