
# -*- coding: utf-8 -*-
"""
Day11 代码示例 01: Plan-and-Execute 基础
"""

import time
import sys
import io
from typing import List, Dict, Any

# 处理 Windows 编码问题
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# 1. 子任务
class SubTask:
    def __init__(self, id: int, description: str, tool: str = None, depends_on: List[int] = None):
        self.id = id
        self.description = description
        self.tool = tool
        self.depends_on = depends_on or []
    
    def __repr__(self):
        return f"SubTask(id={self.id}, description='{self.description}')"


# 2. 计划
class Plan:
    def __init__(self, task: str, steps: List[SubTask]):
        self.task = task
        self.steps = steps
    
    def __repr__(self):
        return f"Plan(task='{self.task}', steps={len(self.steps)})"


# 3. 计划状态
class PlanState:
    def __init__(self, plan: Plan):
        self.plan = plan
        self.current_step = 0
        self.completed: List[int] = []
        self.results: Dict[int, Any] = {}
        self.status = "in_progress"  # in_progress/success/failed
        self.error = None
    
    def complete_step(self, step_id: int, result: Any):
        self.completed.append(step_id)
        self.results[step_id] = result
        self.current_step += 1
    
    def is_done(self) -> bool:
        return self.current_step >= len(self.plan.steps)


# 4. 简单的任务拆解器（模拟）
class SimpleTaskDecomposer:
    def decompose(self, task: str) -> Plan:
        """模拟任务拆解"""
        print(f"📋 拆解任务: {task}")
        
        # 这里应该调用 LLM，我们用规则模拟
        if "旅行" in task or "旅游" in task:
            steps = [
                SubTask(1, "确定目的地", "search"),
                SubTask(2, "预订机票", "booking", depends_on=[1]),
                SubTask(3, "预订酒店", "booking", depends_on=[1]),
                SubTask(4, "制定行程", "planner", depends_on=[2, 3]),
            ]
        elif "聚会" in task or "派对" in task:
            steps = [
                SubTask(1, "确定时间地点", "calendar"),
                SubTask(2, "邀请朋友", "email", depends_on=[1]),
                SubTask(3, "准备食物", "shop", depends_on=[1]),
            ]
        else:
            steps = [
                SubTask(1, "理解需求", "llm"),
                SubTask(2, "执行任务", "tool"),
                SubTask(3, "总结结果", "llm"),
            ]
        
        print(f"   拆解为 {len(steps)} 个子任务")
        for step in steps:
            dep_str = f" (依赖: {step.depends_on})" if step.depends_on else ""
            print(f"   {step.id}. {step.description}{dep_str}")
        
        return Plan(task, steps)


# 5. 简单的执行器
class SimpleExecutor:
    def __init__(self):
        self.tools = {
            "search": self._mock_search,
            "booking": self._mock_booking,
            "planner": self._mock_planner,
            "calendar": self._mock_calendar,
            "email": self._mock_email,
            "shop": self._mock_shop,
            "llm": self._mock_llm,
            "tool": self._mock_tool,
        }
    
    def execute(self, task: SubTask) -> Any:
        """执行子任务"""
        print(f"\n▶️  执行: {task.description}")
        time.sleep(0.5)
        
        tool_func = self.tools.get(task.tool, self._mock_tool)
        result = tool_func(task.description)
        
        print(f"   ✅ 完成: {result}")
        return result
    
    def _mock_search(self, description: str) -> str:
        return "搜索结果: 找到相关信息"
    
    def _mock_booking(self, description: str) -> str:
        return "预订成功！"
    
    def _mock_planner(self, description: str) -> str:
        return "行程制定完成！"
    
    def _mock_calendar(self, description: str) -> str:
        return "时间地点已确定！"
    
    def _mock_email(self, description: str) -> str:
        return "邀请已发送！"
    
    def _mock_shop(self, description: str) -> str:
        return "购物清单准备完成！"
    
    def _mock_llm(self, description: str) -> str:
        return "LLM 处理完成！"
    
    def _mock_tool(self, description: str) -> str:
        return "工具执行完成！"


# 6. Plan-and-Execute Agent
class PlanAndExecuteAgent:
    def __init__(self):
        self.decomposer = SimpleTaskDecomposer()
        self.executor = SimpleExecutor()
    
    def run(self, task: str) -> PlanState:
        """运行 P&E"""
        print("="*60)
        print(f"📋 Plan-and-Execute: {task}")
        print("="*60)
        
        # 1. 拆解任务
        plan = self.decomposer.decompose(task)
        
        # 2. 执行计划
        state = PlanState(plan)
        
        while not state.is_done():
            current_step = plan.steps[state.current_step]
            
            # 检查依赖
            unmet_deps = [d for d in current_step.depends_on if d not in state.completed]
            if unmet_deps:
                print(f"⏳ 等待依赖: {unmet_deps}")
                time.sleep(0.3)
                continue
            
            # 执行
            try:
                result = self.executor.execute(current_step)
                state.complete_step(current_step.id, result)
            except Exception as e:
                state.status = "failed"
                state.error = str(e)
                print(f"❌ 失败: {e}")
                break
        
        # 完成
        if state.status != "failed":
            state.status = "success"
        
        print("\n" + "="*60)
        if state.status == "success":
            print("✅ 计划执行成功！")
        else:
            print(f"❌ 执行失败: {state.error}")
        print(f"   完成步骤: {len(state.completed)}/{len(plan.steps)}")
        print("="*60)
        
        return state


# 7. 测试
if __name__ == "__main__":
    agent = PlanAndExecuteAgent()
    
    # 测试任务
    task = "组织一次周末聚会"
    state = agent.run(task)
    
    print(f"\n🎉 Plan-and-Execute 基础示例完成!")
