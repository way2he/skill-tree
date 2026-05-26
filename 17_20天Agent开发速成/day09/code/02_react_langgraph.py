
# -*- coding: utf-8 -*-
"""
Day09 代码示例 02: LangGraph 版 ReAct
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from operator import add
import sys
import io
import time

# 处理 Windows 编码问题
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# 1. 模拟工具
class MockTools:
    @staticmethod
    def search(query):
        print(f"🔍 搜索: {query}")
        time.sleep(0.3)
        if "GDP" in query:
            return "2023年中国GDP为126万亿元"
        return f"关于 {query} 的搜索结果"


# 2. 定义状态
class ReActState(TypedDict):
    messages: Annotated[list, add]
    question: str
    thought: str
    action: str
    action_input: str
    observation: str
    step: int
    done: bool


# 3. 定义节点
def agent_thought(state: ReActState):
    """思考节点"""
    print(f"\n💭 思考中 (步骤 {state['step']})...")
    time.sleep(0.3)
    
    # 模拟思考
    if state['step'] == 1:
        thought = "我需要搜索相关信息"
        action = "Search"
        action_input = state['question']
    else:
        thought = "我找到了答案"
        action = "Finish"
        action_input = state['observation']
    
    return {
        "thought": thought,
        "action": action,
        "action_input": action_input,
        "step": state['step'] + 1
    }


def tool_execute(state: ReActState):
    """执行工具"""
    print(f"🎯 执行工具: {state['action']}")
    
    if state['action'] == "Search":
        observation = MockTools.search(state['action_input'])
    else:
        observation = "未知工具"
    
    return {"observation": observation}


def router(state: ReActState):
    """路由"""
    if state['action'] == "Finish" or state['step'] > 3:
        return "finish"
    elif state['observation']:
        return "finish"
    else:
        return "tool_execute"


# 4. 构建图
graph = StateGraph(ReActState)
graph.add_node("agent_thought", agent_thought)
graph.add_node("tool_execute", tool_execute)
graph.set_entry_point("agent_thought")
graph.add_conditional_edges("agent_thought", router)
graph.add_edge("tool_execute", "agent_thought")

app = graph.compile()


# 5. 测试
print("="*60)
print("LangGraph 版 ReAct")
print("="*60)

initial_state = {
    "messages": [],
    "question": "2023年中国GDP是多少？",
    "thought": "",
    "action": "",
    "action_input": "",
    "observation": "",
    "step": 1,
    "done": False
}

result = app.invoke(initial_state)

print(f"\n✅ 完成！")
print(f"最终答案: {result.get('observation') or result.get('action_input')}")

print("\n🎉 LangGraph 版 ReAct 示例完成！")
