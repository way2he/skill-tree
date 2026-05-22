# -*- coding: utf-8 -*-
"""
Day04 - 05: 实战 - 天气 + 账单 + 邮件多工具 Agent
功能：完整三工具闭环 + 死循环防护 + 错误处理
"""
import json
import os
import time
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "your-key"))

MAX_ITERATIONS = 5


# ============ 1. 三个工具定义（按 Day04 10:00 节最佳实践设计 schema）============
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询中国大陆城市的实时天气。不支持海外、港澳台。",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市中文名，如 上海、北京。不要用拼音或英文。"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calc_electricity_bill",
            "description": "计算指定月份的电费账单。电费单价为 0.6 元/度。",
            "parameters": {
                "type": "object",
                "properties": {
                    "month": {
                        "type": "string",
                        "description": "月份，格式 YYYY-MM，如 2026-05。",
                        "pattern": r"^\d{4}-\d{2}$"
                    },
                    "kwh": {
                        "type": "number",
                        "description": "本月用电度数，必须大于 0",
                        "minimum": 0
                    }
                },
                "required": ["month", "kwh"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "发送电子邮件给指定收件人。",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {
                        "type": "string",
                        "description": "收件人邮箱，必须是有效邮箱格式",
                        "pattern": r"^[\w.+-]+@[\w-]+\.[\w.-]+$"
                    },
                    "subject": {"type": "string", "description": "邮件标题"},
                    "body": {"type": "string", "description": "邮件正文内容"}
                },
                "required": ["to", "subject", "body"]
            }
        }
    }
]


# ============ 2. 真实函数实现（mock）============
def get_weather(city: str) -> str:
    weather_db = {
        "上海": "22°C 多云，东南风 3 级", "北京": "18°C 晴，无风",
        "广州": "28°C 小雨，南风 4 级", "深圳": "27°C 多云",
    }
    return weather_db.get(city, f"暂无 {city} 数据")


def calc_electricity_bill(month: str, kwh: float) -> str:
    if kwh < 0:
        return "ERROR: 用电度数不能为负数"
    bill = kwh * 0.6
    return f"{month} 用电 {kwh} 度，电费 {bill:.2f} 元"


def send_email(to: str, subject: str, body: str) -> str:
    # 实际可对接 SMTP / SendGrid / 飞书等
    print(f"\n  📧 [Mock Email]\n  收件人: {to}\n  标题: {subject}\n  正文:\n{body}\n")
    return f"邮件已成功发送到 {to}"


FUNCTIONS = {
    "get_weather": get_weather,
    "calc_electricity_bill": calc_electricity_bill,
    "send_email": send_email,
}


# ============ 3. Agent 主循环（含死循环防护）============
def run_agent(user_input: str) -> str:
    messages = [
        {"role": "system", "content": "你是一个能调用工具完成多步骤任务的助手。一次任务可能需要按顺序调用多个工具。"},
        {"role": "user", "content": user_input}
    ]
    seen = set()

    for iteration in range(MAX_ITERATIONS):
        print(f"\n━━━ 第 {iteration + 1} 轮 ━━━")
        resp = client.chat.completions.create(
            model="gpt-5.4", messages=messages, tools=TOOLS
        )
        msg = resp.choices[0].message
        messages.append(msg)

        # 没有 tool_calls = 任务完成
        if not msg.tool_calls:
            return msg.content or "(无回复)"

        # 处理每个工具调用
        for tc in msg.tool_calls:
            name = tc.function.name
            args_str = tc.function.arguments

            # 死循环防护：重复参数检测
            key = (name, args_str)
            if key in seen:
                print(f"  🚫 检测到重复调用 {name}({args_str})，注入防循环提示")
                messages.append({
                    "role": "tool", "tool_call_id": tc.id,
                    "content": "ERROR: 你已经用相同参数调过这个工具，请换思路或换参数"
                })
                continue
            seen.add(key)

            # 执行
            try:
                args = json.loads(args_str)
                print(f"  🔧 调用 {name}({args})")
                start = time.time()
                result = FUNCTIONS[name](**args)
                duration = (time.time() - start) * 1000
                print(f"  ✅ 结果: {result} (耗时 {duration:.0f}ms)")
            except Exception as e:
                result = f"ERROR: {type(e).__name__}: {e}"
                print(f"  ❌ 失败: {result}")

            messages.append({
                "role": "tool", "tool_call_id": tc.id,
                "content": str(result)
            })

    return "达到最大调用次数，任务未完成"


# ============ 4. 运行 ============
if __name__ == "__main__":
    task = (
        "帮我查上海今天天气，"
        "再算 2026 年 5 月用了 380 度电的电费，"
        "最后把这两个信息整理成邮件发给 boss@company.com，"
        "标题写'本月用电与天气速报'"
    )
    print(f"📋 任务：{task}\n")
    answer = run_agent(task)
    print(f"\n{'='*60}\n🎯 最终回复：\n{answer}\n{'='*60}")
