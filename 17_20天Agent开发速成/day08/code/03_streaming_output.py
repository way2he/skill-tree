
# -*- coding: utf-8 -*-
"""
Day08 代码示例 03: 流式输出
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from operator import add
import sys
import io
import time
import asyncio

# 处理 Windows 编码问题
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# 1. 定义状态
class AgentState(TypedDict):
    messages: Annotated[list, add]


# 2. 模拟流式节点
def streaming_node(state: AgentState):
    """模拟流式输出的节点"""
    response = "这是一个流式输出的示例，逐个字输出..."
    
    # 实际项目中，这里会调用 LLM 的流式接口
    # for chunk in llm.stream("..."):
    #     yield chunk
    
    print(f"\n📡 开始流式输出:")
    for char in response:
        print(char, end="", flush=True)
        time.sleep(0.05)  # 模拟延迟
    
    print("\n✅ 流式输出完成")
    return {"messages": [("assistant", response)]}


# 3. 构建图
graph = StateGraph(AgentState)
graph.add_node("streaming", streaming_node)
graph.set_entry_point("streaming")
graph.add_edge("streaming", END)

app = graph.compile()


# 4. 模拟流式输出 (同步版)
print("="*50)
print("示例 1: 模拟同步流式输出")
print("="*50)

initial_state = {"messages": []}
result = app.invoke(initial_state)


# 5. 异步流式示例 (概念演示)
print("\n" + "="*50)
print("示例 2: 异步流式概念演示")
print("="*50)

print("""
💡 实际项目中，LangGraph 支持异步流式:

async for event in app.astream(state, stream_mode="updates"):
    for node_name, output in event.items():
        if "messages" in output:
            msg = output["messages"][-1]
            print(msg.content, end="", flush=True)
""")


# 6. 简单的 Token 生成器模拟
print("\n" + "="*50)
print("示例 3: Token 生成器")
print("="*50)


def token_generator(text, delay=0.03):
    """模拟 Token 生成器"""
    for char in text:
        yield char
        time.sleep(delay)


print("\n📝 生成中: ", end="", flush=True)
for token in token_generator("这是一段逐字生成的文本..."):
    print(token, end="", flush=True)
print("\n✅ 完成!")


# 7. 不同的流模式
print("\n" + "="*50)
print("LangGraph 流模式说明")
print("="*50)

print("""
📊 LangGraph 支持多种流模式:

1. stream_mode="values"
   - 返回完整的状态值
   - 适用: 需要完整状态更新

2. stream_mode="updates"
   - 只返回增量更新
   - 适用: 高效的前端更新

3. stream_mode="messages"
   - 只返回新消息
   - 适用: 对话系统

4. stream_mode="custom"
   - 自定义事件
   - 适用: 复杂的交互需求
""")


print("\n🎉 流式输出示例完成!")
