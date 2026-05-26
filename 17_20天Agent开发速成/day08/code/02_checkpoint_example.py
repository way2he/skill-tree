
# -*- coding: utf-8 -*-
"""
Day08 代码示例 02: Checkpoint 机制
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from operator import add
import sys
import io
import os

# 处理 Windows 编码问题
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# 1. 定义状态
class AgentState(TypedDict):
    messages: Annotated[list, add]
    step: int
    data: str


# 2. 定义节点
def step1(state: AgentState):
    print(f"🔹 执行步骤 1")
    return {
        "messages": [("assistant", "步骤 1 完成")],
        "step": 1,
        "data": "第一步的数据"
    }


def step2(state: AgentState):
    print(f"🔹 执行步骤 2")
    return {
        "messages": [("assistant", "步骤 2 完成")],
        "step": 2,
        "data": state["data"] + " + 第二步的数据"
    }


def step3(state: AgentState):
    print(f"🔹 执行步骤 3")
    return {
        "messages": [("assistant", "步骤 3 完成")],
        "step": 3,
        "data": state["data"] + " + 第三步的数据"
    }


# 3. 构建图
graph = StateGraph(AgentState)
graph.add_node("step1", step1)
graph.add_node("step2", step2)
graph.add_node("step3", step3)
graph.set_entry_point("step1")
graph.add_edge("step1", "step2")
graph.add_edge("step2", "step3")
graph.add_edge("step3", END)

# 4. 创建 Checkpoint 存储
checkpoint_db = "checkpoints_example.db"
if os.path.exists(checkpoint_db):
    os.remove(checkpoint_db)
    print(f"🗑️  已清理旧的 Checkpoint 数据库")

checkpointer = SqliteSaver.from_conn_string(checkpoint_db)
print(f"💾 Checkpoint 数据库: {checkpoint_db}")

# 5. 编译图（启用 Checkpoint）
app = graph.compile(checkpointer=checkpointer)

# 6. 第一次执行
print("\n" + "="*50)
print("第一次执行 (完整流程)")
print("="*50)

config = {"configurable": {"thread_id": "session_001"}}
initial_state = {"messages": [], "step": 0, "data": ""}
result = app.invoke(initial_state, config=config)
print(f"\n✅ 完成! 最终状态:")
print(f"  Step: {result['step']}")
print(f"  Data: {result['data']}")

# 7. 查看历史状态
print("\n" + "="*50)
print("查看历史状态")
print("="*50)

history = list(app.get_state_history(config))
print(f"📜 历史记录数: {len(history)}")
for i, state in enumerate(reversed(history)):
    print(f"\n⏪ 历史状态 {i}:")
    print(f"  Next: {state.next}")
    print(f"  Step: {state.values.get('step')}")
    print(f"  Data: {state.values.get('data')}")

# 8. 模拟中断恢复（从头开始，用相同的 thread_id）
print("\n" + "="*50)
print("模拟中断恢复 (重新运行，使用相同的 thread_id)")
print("="*50)

print("\n🔄 重新调用 (Checkpoint 会跳过已执行的步骤)...")
# 注意：实际生产中，这里可以是程序重启后
result2 = app.invoke(None, config=config)  # 传入 None 表示继续
print(f"\n✅ 恢复完成!")
print(f"  Step: {result2['step']}")
print(f"  Data: {result2['data']}")

# 9. 演示：新会话
print("\n" + "="*50)
print("新会话 (不同的 thread_id)")
print("="*50)

config2 = {"configurable": {"thread_id": "session_002"}}
result3 = app.invoke(initial_state, config=config2)
print(f"\n✅ 新会话完成!")
print(f"  Step: {result3['step']}")

print("\n🎉 Checkpoint 示例完成!")
print(f"\n💡 提示: Checkpoint 数据库文件保存在: {os.path.abspath(checkpoint_db)}")
