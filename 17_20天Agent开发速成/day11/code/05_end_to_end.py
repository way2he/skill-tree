
# -*- coding: utf-8 -*-
"""
Day11 代码示例 05: 端到端 Plan-and-Execute + 多模态
"""

import time
import sys
import io
import random
from typing import List, Dict, Any

# 处理 Windows 编码问题
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# ==================== 1. 基础组件 ====================

class SubTask:
    def __init__(self, id: int, description: str, 
                 tool: str = None, depends_on: List[int] = None,
                 multimodal_input: Dict = None):
        self.id = id
        self.description = description
        self.tool = tool
        self.depends_on = depends_on or []
        self.multimodal_input = multimodal_input or {}


class Plan:
    def __init__(self, task: str, steps: List[SubTask]):
        self.task = task
        self.steps = steps


class PlanState:
    def __init__(self, plan: Plan):
        self.plan = plan
        self.current_step = 0
        self.completed: List[int] = []
        self.results: Dict[int, Any] = {}
        self.status = "in_progress"
        self.multimodal_context = {}


# ==================== 2. 任务拆解器 ====================

class Decomposer:
    def decompose(self, task: str) -> Plan:
        print(f"📋 拆解任务: {task}")
        steps = []
        
        if "旅行" in task:
            steps = [
                SubTask(1, "确定目的地", tool="search"),
                SubTask(2, "搜索目的地照片", tool="image_search", depends_on=[1],
                       multimodal_input={"needs_image": True}),
                SubTask(3, "预订机票", tool="booking", depends_on=[1]),
                SubTask(4, "生成行程单", tool="planner", depends_on=[2, 3],
                       multimodal_input={"needs_text": True, "needs_image": True}),
            ]
        elif "报告" in task:
            steps = [
                SubTask(1, "收集数据", tool="data_collect"),
                SubTask(2, "生成图表", tool="chart_generator", depends_on=[1],
                       multimodal_input={"needs_image": True}),
                SubTask(3, "撰写报告", tool="writer", depends_on=[2],
                       multimodal_input={"needs_text": True}),
                SubTask(4, "生成演示文稿", tool="ppt_generator", depends_on=[3],
                       multimodal_input={"needs_image": True, "needs_text": True}),
            ]
        else:
            steps = [
                SubTask(1, "理解需求", tool="llm"),
                SubTask(2, "执行任务", tool="tool", depends_on=[1]),
                SubTask(3, "总结结果", tool="llm", depends_on=[2]),
            ]
        
        print(f"   拆解为 {len(steps)} 步")
        for step in steps:
            print(f"   {step.id}. {step.description}")
        
        return Plan(task, steps)


# ==================== 3. 多模态工具 ====================

class MultimodalToolkit:
    def search(self, query: str) -> str:
        print(f"   🔍 搜索: {query}")
        time.sleep(0.3)
        return f"搜索结果: {query}"
    
    def image_search(self, query: str) -> str:
        print(f"   🖼️  图像搜索: {query}")
        time.sleep(0.3)
        return f"[图像: {query} 的照片]"
    
    def booking(self, info: str) -> str:
        print(f"   ✈️  预订: {info}")
        time.sleep(0.3)
        return "预订成功！"
    
    def planner(self, info: str, context: Dict) -> Dict:
        print(f"   📋 生成行程单...")
        time.sleep(0.3)
        return {
            "text": "行程单内容...",
            "image": "行程图片..."
        }
    
    def chart_generator(self, data: str) -> str:
        print(f"   📊 生成图表...")
        time.sleep(0.3)
        return "[图表图片]"
    
    def writer(self, content: str, context: Dict) -> str:
        print(f"   ✍️  撰写报告...")
        time.sleep(0.3)
        return "报告内容..."
    
    def ppt_generator(self, content: str, context: Dict) -> Dict:
        print(f"   📽️  生成演示文稿...")
        time.sleep(0.3)
        return {
            "text": "演示文稿文本",
            "image": "演示文稿插图"
        }
    
    def llm(self, prompt: str) -> str:
        print(f"   🤖 LLM 处理...")
        time.sleep(0.3)
        return "LLM 完成"


# ==================== 4. 执行器 ====================

class Executor:
    def __init__(self):
        self.tools = MultimodalToolkit()
    
    def execute_step(self, step: SubTask, state: PlanState) -> Any:
        print(f"\n▶️  步骤 {step.id}: {step.description}")
        
        # 检查依赖
        unmet = [d for d in step.depends_on if d not in state.completed]
        if unmet:
            print(f"   ⏳ 等待依赖: {unmet}")
            return None
        
        # 执行
        tool_name = step.tool
        if hasattr(self.tools, tool_name):
            tool_func = getattr(self.tools, tool_name)
            if tool_name in ["planner", "writer", "ppt_generator"]:
                result = tool_func(step.description, state.multimodal_context)
            else:
                result = tool_func(step.description)
        else:
            result = f"执行: {step.description}"
        
        print(f"   ✅ 完成: {result}")
        
        # 更新多模态上下文
        if step.multimodal_input.get("needs_image"):
            if isinstance(result, dict):
                state.multimodal_context.update(result)
        
        return result


# ==================== 5. 端到端 Agent ====================

class EndToEndAgent:
    def __init__(self):
        self.decomposer = Decomposer()
        self.executor = Executor()
    
    def run(self, task: str) -> PlanState:
        print("="*60)
        print(f"🚀 端到端 Plan-and-Execute: {task}")
        print("="*60)
        
        # 1. 拆解
        plan = self.decomposer.decompose(task)
        state = PlanState(plan)
        
        # 2. 执行
        while not state.current_step >= len(plan.steps):
            step = plan.steps[state.current_step]
            
            result = self.executor.execute_step(step, state)
            
            if result is not None:
                state.completed.append(step.id)
                state.results[step.id] = result
                state.current_step += 1
        
        state.status = "success"
        
        print("\n" + "="*60)
        print(f"✅ 任务完成！共执行 {len(state.completed)} 步")
        print("="*60)
        
        return state


# ==================== 6. 测试 ====================

if __name__ == "__main__":
    agent = EndToEndAgent()
    
    # 测试 1: 计划旅行（多模态）
    print("\n" + "="*60)
    print("1️⃣  测试任务: 计划一次海边旅行")
    print("="*60)
    state1 = agent.run("计划一次海边旅行")
    
    # 测试 2: 写报告（多模态）
    print("\n" + "="*60)
    print("2️⃣  测试任务: 写一份年度报告")
    print("="*60)
    state2 = agent.run("写一份年度报告")
    
    print("\n" + "="*60)
    print("🎉 端到端示例完成！20天学习圆满结束！")
    print("="*60)
    print("\n📚 我们学习了：")
    print("   - LangGraph, Checkpoint, 流式输出")
    print("   - ReAct, Plan-and-Execute")
    print("   - 注意力机制, 记忆系统")
    print("   - 多模态能力")
    print("\n🚀 继续探索，构建更智能的 Agent！")
