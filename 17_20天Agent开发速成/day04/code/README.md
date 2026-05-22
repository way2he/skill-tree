# 📁 Day04 代码目录

## 代码清单

| 文件名 | 功能说明 | 对应知识点 |
|--------|---------|-----------|
| `01_basic_function_call.py` | 最简 FC 完整闭环 | 三步舞协议、tool_calls 解析、role=tool 回灌 |
| `02_multi_tool_routing.py` | 多工具语义向量召回 | embedding + 余弦相似度 + Top-K 召回 |
| `03_json_schema_design.py` | 烂 Schema vs 好 Schema 对比 | 5 大设计原则、自动 schema 审计 |
| `04_tool_error_retry.py` | 错误处理 + 幂等 + 死循环防护 | 业务错误回灌、request_id 去重、MAX_ITER |
| `05_weather_billing_agent.py` | 实战：三工具 Agent 闭环 | 工具循环、死循环防护、完整端到端 |

---

## 学习顺序

```
01_basic_function_call.py
    ↓
03_json_schema_design.py
    ↓
04_tool_error_retry.py
    ↓
02_multi_tool_routing.py
    ↓
05_weather_billing_agent.py  ← 综合实战
```

---

## 每个代码文件的学习要点

### 📌 01_basic_function_call.py
- 理解 FC 三步舞：模型决策 → 本地执行 → 结果回灌
- 看清 `tool_calls`、`tool_call_id`、`role=tool` 的关系
- 能默写最简闭环（面试常考）

### 📌 02_multi_tool_routing.py
- 理解为什么不能把 100 个工具全塞进去
- 学会用 embedding 做语义相似度路由
- 思考生产环境如何把工具向量存入 Milvus / Qdrant

### 📌 03_json_schema_design.py
- 对比烂 Schema 和好 Schema 的差异
- 用 `audit_schema()` 函数对自己写的 schema 做质量检查
- 记住 5 大设计原则

### 📌 04_tool_error_retry.py
- 4 类工具错误的处理策略
- `safe_tool` 装饰器：把异常转结构化 JSON 回灌
- `idempotent` 装饰器：request_id 去重避免重复扣款
- `ToolLoopGuard`：MAX_ITER + 重复参数检测

### 📌 05_weather_billing_agent.py
- 把今天学的全部串起来的综合实战
- 完整三工具 Agent，能完成"查天气 → 算账单 → 发邮件"链路
- 含死循环防护，可直接当生产代码改造

---

## 面试必背代码

以下 3 段代码是面试高频，建议能默写出核心逻辑：

### 1. FC 最简闭环（01）
- 重点：第一轮决策 + 本地执行 + 第二轮回灌
- 面试官问「FC 怎么工作」能默写出这段就稳了

### 2. 错误处理装饰器（04 的 safe_tool）
- 重点：把异常转成 `{"ok": false, "hint": "..."}` 回灌
- 体现工程思维：错误也要让模型能理解

### 3. 死循环防护（04 的 ToolLoopGuard）
- 重点：MAX_ITER + (name, args_hash) 去重
- 面试官问「死循环怎么办」必背

---

## 拓展思考

1. 如果要把工具向量存入生产级向量库（Milvus/Qdrant），代码要怎么改？
2. 如果要给 Agent 加观测（OpenTelemetry / LangSmith），切入点在哪？
3. 如果要支持并行工具调用（parallel_tool_calls），代码要怎么改？
4. 如果要把 Agent 改成"长流程任务"（Plan-Execute-Reflect），用 LangGraph 怎么搭？

---

## 依赖安装

```bash
pip install openai>=1.40.0 numpy
# 可选：用 Pydantic 做参数校验
pip install pydantic>=2.5
```

设置环境变量：
```bash
# Linux/Mac
export OPENAI_API_KEY="your-key"
# Windows PowerShell
$env:OPENAI_API_KEY="your-key"
```

---

**💡 提示：这些代码不只是面试用，更是真实生产环境每天都在用的工程化模式！**
