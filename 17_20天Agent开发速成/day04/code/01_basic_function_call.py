# -*- coding: utf-8 -*-
"""
Day04 - 01: Function Calling 最简完整闭环
功能：演示模型决策 → 本地执行 → 结果回灌的三步舞
"""
import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "your-key"))

# ============ 1. 工具定义 ============
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "查询中国大陆城市的实时天气，返回温度和天气状况",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市中文名，如 上海、北京。不要使用拼音或英文名"
                }
            },
            "required": ["city"]
        }
    }
}]


# ============ 2. 真实函数实现（mock）============
def get_weather(city: str) -> str:
    weather_db = {
        "上海": "22°C 多云", "北京": "18°C 晴", "广州": "28°C 小雨",
        "深圳": "27°C 多云", "成都": "20°C 阴",
    }
    return weather_db.get(city, f"{city}: 无数据")


FUNCTIONS = {"get_weather": get_weather}


# ============ 3. 完整闭环 ============
def chat_with_tools(user_input: str) -> str:
    messages = [{"role": "user", "content": user_input}]

    # 第一轮：模型决策
    resp = client.chat.completions.create(
        model="gpt-5.4", messages=messages, tools=tools
    )
    msg = resp.choices[0].message
    messages.append(msg)

    # 如果模型决定调工具
    if msg.tool_calls:
        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments)
            print(f"  🔧 模型决定调用：{tc.function.name}({args})")

            # 本地执行
            func = FUNCTIONS[tc.function.name]
            result = func(**args)
            print(f"  ✅ 执行结果：{result}")

            # 回灌结果
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": result
            })

        # 第二轮：基于结果生成最终回复
        final = client.chat.completions.create(
            model="gpt-5.4", messages=messages, tools=tools
        )
        return final.choices[0].message.content

    return msg.content


if __name__ == "__main__":
    questions = [
        "上海今天天气怎么样？",
        "帮我查一下北京和广州的天气，对比一下哪个更适合出门",
    ]
    for q in questions:
        print(f"\n👤 用户：{q}")
        answer = chat_with_tools(q)
        print(f"🤖 助手：{answer}")
