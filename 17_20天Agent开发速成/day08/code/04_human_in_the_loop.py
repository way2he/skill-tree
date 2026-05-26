
# -*- coding: utf-8 -*-
"""
Day08 代码示例 04: Human-in-the-loop
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
class HITLState(TypedDict):
    messages: Annotated[list, add]
    proposal: str
    human_feedback: str
    approved: bool
    step: int


# 2. 定义节点
def ai_propose(state: HITLState):
    """AI 生成提案"""
    print("🤖 AI: 正在生成方案...")
    proposal = "这是 AI 生成的方案：我们应该这样做..."
    return {
        "messages": [("assistant", proposal)],
        "proposal": proposal,
        "step": 1
    }


def human_confirmation(state: HITLState):
    """等待人类确认（这里只是占位，实际会中断）"""
    print("⏸️  等待人类确认...")
    return state  # 实际不会执行到这里，会在 interrupt_before 暂停


def execute_plan(state: HITLState):
    """执行方案"""
    if state.get("approved"):
        print(f"✅ 执行方案: {state['proposal']}")
        if state.get("human_feedback"):
            print(f"💡 参考人类反馈: {state['human_feedback']}")
        return {
            "messages": [("assistant", "方案执行完成！")],
            "step": 3
        }
    else:
        print("❌ 方案已取消")
        return {
            "messages": [("assistant", "方案已取消")],
            "step": 3
        }


# 3. 条件路由
def router(state: HITLState):
    if state.get("approved") is None:
        # 还没确认，需要人类确认
        return "human_confirmation"
    elif state["approved"]:
        return "execute_plan"
    else:
        return END


# 4. 构建图
graph = StateGraph(HITLState)
graph.add_node("ai_propose", ai_propose)
graph.add_node("human_confirmation", human_confirmation)
graph.add_node("execute_plan", execute_plan)
graph.set_entry_point("ai_propose")
graph.add_conditional_edges("ai_propose", router)
graph.add_edge("execute_plan", END)

# 5. 创建 Checkpoint
checkpoint_db = "hitl_checkpoints.db"
if os.path.exists(checkpoint_db):
    os.remove(checkpoint_db)
checkpointer = SqliteSaver.from_conn_string(checkpoint_db)

# 6. 编译图（设置中断点）
app = graph.compile(
    checkpointer=checkpointer,
    interrupt_before=["human_confirmation"]  # 在人类确认前中断
)

# 7. 演示 Human-in-the-loop
print("="*50)
print("Human-in-the-loop 演示")
print("="*50)

config = {"configurable": {"thread_id": "hitl_demo_001"}}
initial_state = {
    "messages": [],
    "proposal": "",
    "human_feedback": "",
    "approved": None,
    "step": 0
}

# 第一步：AI 生成提案，然后中断
print("\n🚀 第一步：AI 生成提案...")
result = app.invoke(initial_state, config=config)
print(f"\n⏸️  已中断！当前状态:")
print(f"  提案: {result['proposal']}")
print(f"  是否批准: {result['approved']}")

# 查看当前状态
current_state = app.get_state(config)
print(f"\n📍 当前下一步: {current_state.next}")

# 第二步：模拟人类确认（在实际应用中，这是用户在前端操作）
print("\n" + "="*50)
print("第二步：人类确认")
print("="*50)

# 这里模拟人类输入
human_input = {
    "approved": True,
    "human_feedback": "这个方案很好，但是需要注意细节"
}

print(f"\n👤 人类输入:")
print(f"  批准: {human_input['approved']}")
print(f"  反馈: {human_input['human_feedback']}")

# 更新状态
app.update_state(config, human_input)

# 第三步：继续执行
print("\n" + "="*50)
print("第三步：继续执行")
print("="*50)

result = app.invoke(None, config=config)
print(f"\n✅ 完成！最终状态:")
print(f"  Step: {result['step']}")
print(f"  Messages: {result['messages']}")

# 查看历史
print("\n" + "="*50)
print("执行历史")
print("="*50)

history = list(app.get_state_history(config))
for i, state in enumerate(reversed(history)):
    print(f"\n⏪ 步骤 {i}:")
    print(f"  Next: {state.next}")
    print(f"  Approved: {state.values.get('approved')}")


print("\n🎉 Human-in-the-loop 演示完成!")
print("\n💡 关键点:")
print("  1. 使用 interrupt_before 设置中断点")
print("  2. 使用 update_state 更新人类输入")
print("  3. 调用 invoke(None, ...) 继续执行")
