---
name: Day04 - Function Calling 从入门到精通（面试高频）
description: Day04 完整学习计划：精确到分钟，工具调用底层协议 + JSON Schema 设计 + 多工具路由 + 错误处理 + 实战 Agent
type: learning
tags: ["Function Calling", "工具调用", "JSON Schema", "Agent", "梯度下降", "面试"]
created_at: 2026-05-22
updated_at: 2026-05-22
version: interview
---

# 🛠️ Day 04：Function Calling 从入门到精通（面试高频）

- **学习日期**：第 4 天 / 共 20 天
- **学习时长**：8 小时（精确到分钟）
- **核心目标**：吃透 Function Calling 协议、能设计高质量 JSON Schema、能实现多工具智能路由、能搭出真正可用的多工具 Agent

---

## ⏰ 今日学习时间表（精确到分钟）

| 时间段 | 学习内容 | 完成情况 |
|--------|---------|---------|
| **09:00-10:00** | Function Calling 基础原理与协议解析 | ⬜️ / ✅ |
| **10:00-11:00** | JSON Schema 工具参数设计最佳实践 | ⬜️ / ✅ |
| **11:00-12:00** | 工具调用错误处理与重试（含幂等设计） | ⬜️ / ✅ |
| **14:00-15:00** | 多工具选择策略与智能路由（含成本路由） | ⬜️ / ✅ |
| **15:00-16:00** | OpenAI vs Anthropic Function Calling 协议对比 | ⬜️ / ✅ |
| **16:00-17:00** | ML 基础：梯度下降与优化器（SGD/Adam/AdamW） | ⬜️ / ✅ |
| **19:00-20:00** | 【面试题专项】Day04 7 道 Function Calling 面试题 | ⬜️ / ✅ |
| **20:00-21:00** | 实战：天气 + 账单 + 邮件三工具 Agent | ⬜️ / ✅ |

---

## 🎯 09:00-10:00：Function Calling 基础原理与协议解析

### 📝 核心知识点 + 对应面试考点

#### 知识点 1：Function Calling 是什么

1. **本质**：让大模型能"指挥"外部函数完成无法靠纯文本完成的事（查天气、调 API、读数据库）
2. **关键认知**：**模型本身不执行函数**，它只输出"我想调用 xxx 函数、参数是 yyy"的结构化 JSON
3. **真正执行函数的是你的代码**，再把执行结果回灌给模型继续推理
4. **面试一句话**：「Function Calling = 模型负责决策，代码负责执行，再把结果回灌让模型继续生成。」

#### 知识点 2：标准协议三步舞

1. **第一轮**：用户提问 + 工具清单 → 模型返回 `tool_calls`（包含函数名 + 参数 JSON）
2. **本地执行**：你的代码解析 JSON，调用真实函数，拿到结果
3. **第二轮**：把 `tool_call_id` + 函数结果作为 `role=tool` 消息回传 → 模型生成最终自然语言回复

#### 知识点 3：tools 参数三要素

1. **name**：函数名，必须英文，蛇形命名（`get_weather`）
2. **description**：函数描述，**模型靠它决定要不要调用此工具**，必须清晰精准
3. **parameters**：JSON Schema 描述参数结构（type/properties/required）

### 💻 必写代码 1：最简 Function Calling 完整闭环

```python
from openai import OpenAI
import json

client = OpenAI()

# 1. 定义工具
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "查询指定城市的实时天气",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名，如 上海、北京"}
            },
            "required": ["city"]
        }
    }
}]

# 2. 真实函数实现
def get_weather(city: str) -> str:
    # 实际可调外部 API，这里 mock
    return f"{city} 当前 22°C 多云"

# 3. 第一轮：模型决策
messages = [{"role": "user", "content": "上海今天天气怎么样？"}]
resp = client.chat.completions.create(
    model="gpt-5.4", messages=messages, tools=tools
)
msg = resp.choices[0].message
messages.append(msg)

# 4. 本地执行 + 第二轮：回灌结果
if msg.tool_calls:
    for tc in msg.tool_calls:
        args = json.loads(tc.function.arguments)
        result = get_weather(**args)
        messages.append({
            "role": "tool",
            "tool_call_id": tc.id,
            "content": result
        })
    final = client.chat.completions.create(
        model="gpt-5.4", messages=messages, tools=tools
    )
    print(final.choices[0].message.content)
```

### ⭐ 面试官追问：Function Calling 和 Prompt Engineering 让模型输出 JSON 有什么本质区别？

> **3 分钟回答模板**：
>
> 表面看都是输出结构化 JSON，但本质完全不同：
>
> 1. **训练方式**：Function Calling 是模型在 SFT 阶段就专门训练过的能力，输出格式有专门的特殊 token 控制；Prompt 让模型输 JSON 是"骗"模型按格式输出，没有任何强约束
> 2. **稳定性**：FC 的 JSON 格式准确率 99%+，纯 Prompt 经常出现引号、逗号、转义错误
> 3. **可扩展**：FC 协议层就支持多工具并行调用（parallel tool calls）、流式工具调用、工具结果回灌等，Prompt 方案要靠自己解析
> 4. **生态**：OpenAI/Anthropic/Gemini/DeepSeek 都遵循类似协议，工具定义可复用

---


## 🎯 10:00-11:00：JSON Schema 工具参数设计最佳实践

### 📝 核心知识点 + 对应面试考点

#### 知识点 1：JSON Schema 7 大字段

1. **type**：参数类型（string / number / integer / boolean / array / object）
2. **description**：参数说明，**模型靠它理解每个参数的含义**
3. **enum**：枚举值约束（如 ["sunny", "rainy", "snowy"]）
4. **default**：默认值（模型可省略此参数）
5. **required**：必填字段数组（在 properties 外层）
6. **items**：数组元素的 Schema（type=array 时必填）
7. **properties**：对象嵌套字段定义

#### 知识点 2：好 Schema 的 5 大原则

1. **描述精准胜过简短**："description": "城市的中文名称，如 上海" 比 "city name" 强 10 倍
2. **能枚举不用 string**：让模型从 enum 选，避免"上海市/上海/SH"歧义
3. **数字加范围约束**：minimum/maximum 避免模型给出离谱值
4. **能省的字段就别要**：参数越多模型越容易乱填
5. **失败示例写进 description**："日期格式 YYYY-MM-DD，不要写成 2026/05/22"

#### 知识点 3：常见反例

| 反例 | 问题 | 正解 |
|------|------|------|
| description 写英文给中文模型用 | 理解打折扣 | 跟随对话语言 |
| 必填字段写 8 个 | 模型经常乱填 | 必填 ≤3 个，其余给 default |
| 接受任意字符串日期 | 格式五花八门 | 用 pattern 正则约束 |
| 用 number 表示状态码 | 模型可能输出 200.0 | 用 integer + enum |

### 💻 必写代码 2：高质量 Schema 模板

`python
# ❌ 烂 Schema
bad_tool = {
    "name": "book_flight",
    "description": "book a flight",
    "parameters": {
        "type": "object",
        "properties": {
            "from": {"type": "string"},
            "to": {"type": "string"},
            "date": {"type": "string"},
            "class": {"type": "string"},
            "passengers": {"type": "number"}
        }
    }
}

# ✅ 好 Schema
good_tool = {
    "name": "book_flight",
    "description": "预订国内航班机票。仅支持中国大陆机场，不支持港澳台和国际航班。",
    "parameters": {
        "type": "object",
        "properties": {
            "from_city": {
                "type": "string",
                "description": "出发城市的中文名，如 上海、北京。不要使用机场代码。"
            },
            "to_city": {
                "type": "string",
                "description": "到达城市的中文名，如 广州、成都。不要使用机场代码。"
            },
            "date": {
                "type": "string",
                "description": "出发日期，格式必须为 YYYY-MM-DD，例如 2026-05-22。不要使用 2026/05/22 或 5月22日。",
                "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
            },
            "cabin_class": {
                "type": "string",
                "description": "舱位等级，默认经济舱",
                "enum": ["经济舱", "商务舱", "头等舱"],
                "default": "经济舱"
            },
            "passenger_count": {
                "type": "integer",
                "description": "乘客人数，默认 1 人",
                "minimum": 1,
                "maximum": 9,
                "default": 1
            }
        },
        "required": ["from_city", "to_city", "date"]
    }
}
`

### ⭐ 面试官追问：description 写得多详细才合适？

> **3 分钟回答模板**：
>
> 黄金法则：**让模型读完 description 就能正确填参数，不需要靠猜**。
>
> 实操经验：
> 1. 函数级 description 写「做什么 + 不做什么」（边界），约 30-80 字
> 2. 参数级 description 写「含义 + 格式 + 反例」，约 20-60 字
> 3. 复杂场景给一两个 example，能显著降低错误率
> 4. 如果模型频繁填错某字段，直接在 description 里加「不要写成 xxx」
>
> 真实数据：把 description 从 5 字优化到 50 字，参数准确率从 60% 提升到 95%+ 是常态。

---

## 🎯 11:00-12:00：工具调用错误处理与重试（含幂等设计）

### 📝 核心知识点 + 对应面试考点

#### 知识点 1：4 类工具调用错误

1. **参数错误**：模型给的参数不符合 Schema（缺字段、格式错、类型错）
2. **业务错误**：参数对但业务失败（城市不存在、余额不足、订单已取消）
3. **网络/超时错误**：外部 API 不通、超时
4. **模型幻觉**：调用了不存在的工具、捏造参数

#### 知识点 2：处理策略矩阵

1. **参数错误** → 返回结构化错误给模型，让模型自纠正重试（最多 2 次）
2. **业务错误** → 把业务报错原文回灌，让模型改用其他参数或换工具
3. **网络错误** → 工具层用指数退避重试（与 Day03 思路一致）
4. **幻觉调用** → 严格校验函数名，未注册的函数直接报错，记录日志

#### 知识点 3：幂等性设计

1. **幂等定义**：同样参数调 N 次和调 1 次效果一样（GET 天然幂等、POST 默认不幂等）
2. **为什么重要**：模型可能因超时重试，幂等保证不会重复扣款/重复下单
3. **实现方式**：
   - 业务层：用 equest_id 去重（推荐）
   - 数据库层：唯一索引
   - 函数层：先查询再操作

### 💻 必写代码 3：错误处理装饰器 + 结构化错误返回

`python
import json
from functools import wraps

class ToolError(Exception):
    """工具调用业务错误"""
    def __init__(self, code: str, message: str, hint: str = ""):
        self.code = code
        self.message = message
        self.hint = hint  # 给模型的修复建议

def safe_tool(func):
    """工具安全执行装饰器：统一错误格式返回给模型"""
    @wraps(func)
    def wrapper(**kwargs):
        try:
            result = func(**kwargs)
            return json.dumps({"ok": True, "data": result}, ensure_ascii=False)
        except ToolError as e:
            # 业务错误：把 hint 回灌让模型改参数
            return json.dumps({
                "ok": False, "code": e.code,
                "message": e.message, "hint": e.hint
            }, ensure_ascii=False)
        except Exception as e:
            # 未知错误：兜底
            return json.dumps({
                "ok": False, "code": "UNKNOWN",
                "message": str(e), "hint": "请稍后重试或换个参数"
            }, ensure_ascii=False)
    return wrapper

@safe_tool
def get_weather(city: str) -> dict:
    valid_cities = {"上海", "北京", "广州", "深圳"}
    if city not in valid_cities:
        raise ToolError(
            code="CITY_NOT_FOUND",
            message=f"城市 {city} 不在支持列表",
            hint=f"请改用以下城市之一：{', '.join(valid_cities)}"
        )
    return {"city": city, "temp": 22, "weather": "多云"}

# 测试错误自纠正
print(get_weather(city="火星"))
# 输出：{"ok": false, "code": "CITY_NOT_FOUND", "message": "...", "hint": "请改用以下城市之一：上海, 北京, ..."}
`

### ⭐ 面试官追问：模型反复调错工具陷入死循环怎么办？

> **3 分钟回答模板**：
>
> 三道防线：
> 1. **最大调用次数限制**：单次对话最多 5-10 次 tool_calls，超出强制终止并报错
> 2. **重复调用检测**：相同函数 + 相同参数连续调用 2 次以上，认为陷入循环，主动 break
> 3. **降级回退**：循环时切换到"直接回答用户"模式，告知"我尝试了 N 次都失败，问题是 xxx"
>
> 工程上一般用 MAX_TOOL_ITERATIONS = 5 这种硬上限，加上 (name, args_hash) 的去重集合，能解决 99% 的死循环问题。LangChain、LangGraph 都有内置的 recursion_limit。

---

## 🎯 14:00-15:00：多工具选择策略与智能路由

### 📝 核心知识点 + 对应面试考点

#### 知识点 1：多工具选择三难题

1. **工具太多模型选不准**：超过 20 个工具，模型准确率显著下降
2. **相似工具选错**：如 search_web vs search_knowledge_base 容易混淆
3. **成本失控**：每次都把所有 100 个工具塞进去，token 消耗巨大

#### 知识点 2：智能路由四大策略

1. **关键词路由**：用户问"天气" → 只挂天气类工具
2. **语义向量路由**：把工具 description 向量化，按用户 query 余弦相似度 top-K 召回
3. **分级 Agent**：路由 Agent 决定子领域 → 子 Agent 拿专属工具集
4. **成本路由**：简单工具用便宜模型决策，复杂工具升级到旗舰模型

#### 知识点 3：工具命名与分组规范

1. **命名前缀分组**：db_query、db_insert、pi_get、pi_post
2. **同类工具用 enum 合并**：crud(action: enum, resource: enum) 比 4 个独立工具更精准
3. **冷门工具下沉**：常用工具直接挂、冷门工具放二级 Agent

### 💻 必写代码 4：语义路由 + Top-K 工具召回

`python
from openai import OpenAI
import numpy as np

client = OpenAI()

# 1. 所有工具及其 description
all_tools = {
    "get_weather": "查询城市实时天气",
    "search_web": "联网搜索最新信息",
    "search_kb": "搜索企业内部知识库",
    "send_email": "发送邮件给指定收件人",
    "create_calendar_event": "创建日历事件",
    # ... 假设 100+ 个工具
}

# 2. 离线预先把所有 description 向量化（实际生产存 Milvus/Qdrant）
def embed(text: str) -> np.ndarray:
    resp = client.embeddings.create(model="text-embedding-3-large", input=text)
    return np.array(resp.data[0].embedding)

tool_vectors = {name: embed(desc) for name, desc in all_tools.items()}

# 3. 运行时按用户 query 召回 Top-K 工具
def route_tools(user_query: str, top_k: int = 5) -> list:
    q_vec = embed(user_query)
    scored = [
        (name, float(np.dot(q_vec, v) / (np.linalg.norm(q_vec) * np.linalg.norm(v))))
        for name, v in tool_vectors.items()
    ]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [name for name, _ in scored[:top_k]]

# 4. 只把 Top-K 挂给模型
selected = route_tools("帮我看看上海今天会不会下雨")
# 期望返回 ['get_weather', 'search_web', ...]，去掉无关的 send_email 等
`

### ⭐ 面试官追问：多工具场景下 token 成本怎么压？

> **3 分钟回答模板**：
>
> 四招组合拳：
> 1. **工具召回**：100 工具向量化，按 query 召回 Top-5，token 直接降 95%
> 2. **description 精简**：把示例和反例放到外部文档，工具内描述压到 50 字以内
> 3. **分级缓存**：相同 query 命中的工具集直接缓存，避免重复 embedding
> 4. **小模型分流**：用 gpt-5.4-mini 做路由决策，旗舰模型做最终生成
>
> 真实案例：某客服 Agent 从 200 工具全量塞入降为 Top-5 召回后，单次对话 token 从 12K 降到 1.5K，月成本下降 87%。

---

## 🎯 15:00-16:00：OpenAI vs Anthropic Function Calling 协议对比

### 📝 核心知识点 + 对应面试考点

#### 知识点 1：协议层差异速查

| 维度 | OpenAI | Anthropic Claude |
|------|--------|------------------|
| 工具定义入参 | 	ools=[{type:"function", function:{...}}] | 	ools=[{name, description, input_schema}] |
| 模型返回字段 | message.tool_calls[] | content[] 中含 	ype=tool_use 的 block |
| 参数字段 | rguments（字符串需 JSON.parse） | input（已是 dict） |
| 工具结果回灌 | ole=tool, tool_call_id, content | ole=user, content=[{type:tool_result, tool_use_id, content}] |
| 并行调用 | 默认支持，parallel_tool_calls=false 关闭 | 默认支持，无开关 |
| 强制调用 | 	ool_choice={type:"function",function:{name}} | 	ool_choice={type:"tool",name} |
| 不调用工具 | 	ool_choice="none" | 	ool_choice={type:"none"}（4.x 新增） |

#### 知识点 2：核心差异 3 个坑

1. **arguments 类型不同**：OpenAI 是 JSON 字符串需要解析，Anthropic 是已解析的 dict，混用会报错
2. **结果回灌角色不同**：OpenAI 用 ole=tool，Anthropic 用 ole=user + 	ool_result block
3. **流式协议不同**：OpenAI 流式 tool_calls 是增量拼接，Anthropic 用 content_block_delta 事件

#### 知识点 3：DeepSeek/Qwen/GLM 国产模型

1. **DeepSeek V4**：兼容 OpenAI 协议（	ools + 	ool_calls），SDK 直接复用
2. **Qwen3-Max**：兼容 OpenAI 协议，但部分老版本字段名为 unction_call（旧 API）
3. **GLM-5.1**：兼容 OpenAI 协议，工具调用稳定性 ≈ Claude Sonnet
4. **底层都向 OpenAI 协议靠拢**，国产开源模型基本可无缝迁移

### 💻 必写代码 5：跨厂商统一工具适配器

`python
from typing import Protocol
import json

class ToolAdapter(Protocol):
    def format_tools(self, tools: list) -> list: ...
    def parse_tool_calls(self, response) -> list: ...
    def format_tool_result(self, tool_call_id: str, result: str) -> dict: ...

class OpenAIAdapter:
    def format_tools(self, tools): return [{"type": "function", "function": t} for t in tools]

    def parse_tool_calls(self, response):
        msg = response.choices[0].message
        return [
            {"id": tc.id, "name": tc.function.name,
             "args": json.loads(tc.function.arguments)}
            for tc in (msg.tool_calls or [])
        ]

    def format_tool_result(self, tool_call_id, result):
        return {"role": "tool", "tool_call_id": tool_call_id, "content": result}

class AnthropicAdapter:
    def format_tools(self, tools):
        return [{"name": t["name"], "description": t["description"],
                 "input_schema": t["parameters"]} for t in tools]

    def parse_tool_calls(self, response):
        return [
            {"id": b.id, "name": b.name, "args": b.input}
            for b in response.content if b.type == "tool_use"
        ]

    def format_tool_result(self, tool_call_id, result):
        return {"role": "user", "content": [{
            "type": "tool_result", "tool_use_id": tool_call_id, "content": result
        }]}

# 业务代码不感知模型厂商，按 adapter 切换
adapter: ToolAdapter = OpenAIAdapter()  # 或 AnthropicAdapter()
`

### ⭐ 面试官追问：为什么 Anthropic 不学 OpenAI 用统一协议？

> **3 分钟回答模板**：
>
> 历史原因 + 设计哲学：
> 1. **历史包袱**：OpenAI 早期是 unction_call（单工具），后来才升级为 	ool_calls（多工具）。Anthropic 从 Claude 2.1 起步就直接是 	ool_use block 设计，没有兼容老协议的包袱
> 2. **设计哲学**：Anthropic 强调 content 是多模态 block 数组（文本 / 图片 / 工具调用 / 工具结果），所有内容平等对待。OpenAI 是消息级别分角色（role=tool）
> 3. **行业现状**：DeepSeek/Qwen/GLM/Gemini 都向 OpenAI 协议靠拢，Claude 是"少数派"。但 Claude 的 tool 调用稳定性最强、SWE-bench 第一，业务方愿意为此适配

---

## 🎯 16:00-17:00：ML 基础——梯度下降与优化器（面试高频！）

### 📝 核心知识点 + 对应面试考点

#### 知识点 1：梯度下降三种变体

1. **BGD 批量梯度下降**：用全部样本算梯度，每步精准但慢，**不适合大数据**
2. **SGD 随机梯度下降**：每次随机 1 个样本，快但震荡大、容易陷局部最优
3. **Mini-batch SGD**：每次取一个 batch（32/64/128），**实际工程的事实标准**

#### 知识点 2：5 大主流优化器演进史

1. **SGD**：朴素梯度下降，参数 = 参数 - lr × 梯度
2. **Momentum**：加入动量项，类似小球滚下山，能冲过小坑
3. **RMSProp**：按参数自适应调整学习率，频繁更新的参数学习率小
4. **Adam = Momentum + RMSProp**：综合一阶动量和二阶动量，**最常用**
5. **AdamW**：Adam + 权重衰减解耦，**Transformer/大模型训练首选**

#### 知识点 3：超参选择经验值

1. **学习率 lr**：Adam 默认 1e-3，Transformer 微调 1e-5 ~ 5e-5
2. **batch size**：算力允许尽量大，但太大会损失泛化
3. **weight decay**：AdamW 默认 0.01，大模型常用 0.1
4. **warmup**：训练前 5-10% step 学习率从 0 线性升到目标值

### 💻 必写代码 6：手写梯度下降 + PyTorch 对比

`python
import numpy as np

# 手写 SGD：拟合 y = 2x + 3
def manual_sgd():
    X = np.array([1, 2, 3, 4, 5], dtype=np.float32)
    y = np.array([5, 7, 9, 11, 13], dtype=np.float32)
    w, b = 0.0, 0.0
    lr = 0.01
    for epoch in range(1000):
        y_pred = w * X + b
        loss = np.mean((y_pred - y) ** 2)
        # 梯度：dL/dw = 2*(y_pred-y)*X，dL/db = 2*(y_pred-y)
        dw = np.mean(2 * (y_pred - y) * X)
        db = np.mean(2 * (y_pred - y))
        w -= lr * dw
        b -= lr * db
        if epoch % 200 == 0:
            print(f"epoch {epoch}: w={w:.3f}, b={b:.3f}, loss={loss:.4f}")
    return w, b

# PyTorch 版（5 行搞定）
import torch
def pytorch_adam():
    X = torch.tensor([[1.], [2.], [3.], [4.], [5.]])
    y = torch.tensor([[5.], [7.], [9.], [11.], [13.]])
    model = torch.nn.Linear(1, 1)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.01)
    loss_fn = torch.nn.MSELoss()
    for _ in range(1000):
        optimizer.zero_grad()
        loss = loss_fn(model(X), y)
        loss.backward()
        optimizer.step()
    print(f"w={model.weight.item():.3f}, b={model.bias.item():.3f}")

manual_sgd(); pytorch_adam()
`

### ⭐ 面试官追问：Adam 收敛快为什么大模型预训练还用 AdamW？

> **3 分钟回答模板**：
>
> 区别在**权重衰减**的实现方式：
> 1. **Adam 的 weight decay 实际是 L2 正则**，会被自适应学习率"稀释"，对大权重的惩罚不一致
> 2. **AdamW 把 weight decay 从梯度计算中解耦**，直接乘到参数更新上，惩罚强度恒定
> 3. **大模型训练特点**：参数量大，weight decay 是关键正则手段。Adam 的"稀释"问题在 Transformer 这种大模型上会显著影响泛化
> 4. **实证**：BERT、GPT、LLaMA 全系列都是 AdamW，Vision Transformer 也是。**Transformer = AdamW 已成行业默认**
>
> 简单说：Adam 的 weight decay 是假的，AdamW 才是真的。

---

## 🎯 19:00-20:00：面试题专项（7 道高频题）

> 完整题目见 [面试题.md](面试题.md)｜标准答案见 [面试题_标准答案.md](面试题_标准答案.md)
>
> 本节给出每题的「2 分钟核心点 + 杀手锏话术」。

### Q1 Function Calling 的本质是什么？模型真的会执行函数吗？
- 核心点：模型只输出结构化 JSON（决策），代码负责执行（行动），结果回灌让模型继续生成
- 杀手锏：「**FC = 模型决策 + 代码执行 + 结果回灌**，模型本身从不执行任何函数。」

### Q2 JSON Schema 中 description 的作用？怎么写好？
- 核心点：description 是模型理解"该不该调、参数怎么填"的唯一依据
- 杀手锏：「函数级写'做什么+不做什么'，参数级写'含义+格式+反例'。把 desc 从 5 字优化到 50 字，准确率能从 60% 提升到 95%+。」

### Q3 模型反复调错工具陷入死循环怎么办？
- 核心点：最大调用次数 + 重复检测 + 降级回退
- 杀手锏：「**MAX_TOOL_ITERATIONS=5 硬上限 + (name, args_hash) 去重集合**，能解决 99% 死循环。」

### Q4 多工具场景下 token 成本爆炸怎么解？
- 核心点：向量召回 Top-K + description 精简 + 分级缓存 + 小模型路由
- 杀手锏：「100 工具向量化后召回 Top-5，token 直接降 95%。」

### Q5 OpenAI 和 Anthropic 的工具调用协议有什么本质区别？
- 核心点：arguments 类型不同（字符串 vs dict）、结果回灌角色不同（tool vs user）
- 杀手锏：「OpenAI 是 role 级别分类，Anthropic 是 content block 级别分类。国产模型都向 OpenAI 协议靠拢。」

### Q6 工具的幂等性是什么？为什么重要？怎么实现？
- 核心点：同样参数调 N 次 = 调 1 次，避免超时重试导致的重复扣款
- 杀手锏：「**用 request_id 做去重**是工业标准。GET 天然幂等，POST 必须显式设计。」

### Q7 Adam 和 AdamW 的区别？为什么大模型都用 AdamW？
- 核心点：weight decay 实现方式不同，Adam 是 L2 正则会被学习率稀释，AdamW 是解耦的真衰减
- 杀手锏：「**Adam 的 weight decay 是假的，AdamW 才是真的。** 所以 BERT/GPT/LLaMA 全部用 AdamW。」

---

## 🎯 20:00-21:00：实战——天气 + 账单 + 邮件三工具 Agent

### 实战目标

搭建一个能完成 **"查上海今天天气 → 算 5 月份电费 → 把结果发邮件给老板"** 的多工具 Agent，把今天学的所有概念串起来：

1. 多工具定义（3 个工具 × 高质量 Schema）
2. 工具循环调用（含最大次数 + 死循环防护）
3. 错误处理（业务错误回灌让模型自纠正）
4. 真正可跑（mock 但接口完整）

### 完整代码骨架

`python
from openai import OpenAI
import json

client = OpenAI()
MAX_ITERATIONS = 5

# 3 个工具定义（精简版，完整版见 code/05_weather_billing_agent.py）
tools = [
    {"type": "function", "function": {
        "name": "get_weather",
        "description": "查询中国大陆城市的实时天气",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string", "description": "城市中文名"}},
            "required": ["city"]
        }
    }},
    {"type": "function", "function": {
        "name": "calc_electricity_bill",
        "description": "计算某月电费，单价 0.6 元/度",
        "parameters": {
            "type": "object",
            "properties": {
                "month": {"type": "string", "description": "月份 YYYY-MM"},
                "kwh": {"type": "number", "description": "本月用电度数"}
            },
            "required": ["month", "kwh"]
        }
    }},
    {"type": "function", "function": {
        "name": "send_email",
        "description": "发送邮件给指定收件人",
        "parameters": {
            "type": "object",
            "properties": {
                "to": {"type": "string", "description": "收件人邮箱"},
                "subject": {"type": "string"},
                "body": {"type": "string"}
            },
            "required": ["to", "subject", "body"]
        }
    }}
]

# 函数实现（mock）
def get_weather(city): return f"{city} 22°C 多云"
def calc_electricity_bill(month, kwh): return f"{month} 电费 {kwh*0.6:.2f} 元"
def send_email(to, subject, body): return f"邮件已发送到 {to}"
FUNCTIONS = {"get_weather": get_weather, "calc_electricity_bill": calc_electricity_bill, "send_email": send_email}

def run_agent(user_input: str):
    messages = [{"role": "user", "content": user_input}]
    seen = set()
    for iteration in range(MAX_ITERATIONS):
        resp = client.chat.completions.create(model="gpt-5.4", messages=messages, tools=tools)
        msg = resp.choices[0].message
        messages.append(msg)
        if not msg.tool_calls:
            return msg.content
        for tc in msg.tool_calls:
            key = (tc.function.name, tc.function.arguments)
            if key in seen:
                messages.append({"role": "tool", "tool_call_id": tc.id,
                                 "content": "ERROR: 重复调用相同参数，请换思路"})
                continue
            seen.add(key)
            args = json.loads(tc.function.arguments)
            try:
                result = FUNCTIONS[tc.function.name](**args)
            except Exception as e:
                result = f"ERROR: {e}"
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": str(result)})
    return "达到最大调用次数，任务未完成"

# 运行
print(run_agent("帮我查上海今天天气，再算 2026 年 5 月用了 380 度电的电费，最后把这两个信息发邮件给 boss@company.com"))
`

### 验收标准

- [ ] 工具被按合理顺序调用（天气→电费→邮件）
- [ ] 重复参数能被去重防死循环
- [ ] 业务错误能被模型理解并自纠正
- [ ] 最终输出自然语言总结，不是裸 JSON

---

## 📚 今日延伸阅读

- 同目录专题：[Function_Calling底层原理与协议.md](Function_Calling底层原理与协议.md)（深度文档）
- Day03 评估指标：[../day03/评估指标与Agent效果评估.md](../day03/评估指标与Agent效果评估.md)
- OpenAI Function Calling 官方文档：<https://platform.openai.com/docs/guides/function-calling>
- Anthropic Tool Use 官方文档：<https://docs.anthropic.com/en/docs/build-with-claude/tool-use>

---

## ✅ 今日学习自检清单

- [ ] 能讲清楚 Function Calling 的标准三步舞（决策→执行→回灌）
- [ ] 能默写 OpenAI tools 参数结构 + tool_calls 解析代码
- [ ] 能讲出 JSON Schema 5 大设计原则
- [ ] 能讲清楚 4 类工具错误及对应处理策略
- [ ] 能讲出多工具死循环的 3 道防线
- [ ] 能讲出 OpenAI vs Anthropic 协议的 3 个核心差异
- [ ] 能讲出 Adam 和 AdamW 的本质区别
- [ ] 能跑通 20:00-21:00 的三工具 Agent 实战

---

**🚀 Day04 完成！明天 Day05：Agent 框架核心组件（Planner / Memory / Tools / Executor）！**