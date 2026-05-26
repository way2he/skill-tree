
# -*- coding: utf-8 -*-
"""
Day11 代码示例 03: 动态调整
"""

import time
import sys
import io
import random
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


# 2. 计划与状态
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
        self.adjustments = 0


# 3. 调整策略
class AdjustmentStrategy:
    RETRY = "retry"
    REPLACE = "replace"
    REORDER = "reorder"
    REPLAN = "replan"


# 4. 调整引擎
class AdjustmentEngine:
    """调整引擎"""
    
    def analyze(self, state: PlanState, step: SubTask, error: Exception) -> str:
        """分析失败原因，选择策略"""
        print(f"\n🔍 分析失败: {step.description}")
        print(f"   错误: {error}")
        
        # 简单规则，实际应该用 LLM
        if "timeout" in str(error).lower():
            strategy = AdjustmentStrategy.RETRY
            reason = "超时错误，可能是临时问题"
        elif "not found" in str(error).lower():
            strategy = AdjustmentStrategy.REPLACE
            reason = "工具不可用，换一种方法"
        elif len(state.completed) > len(state.plan.steps) / 2:
            strategy = AdjustmentStrategy.REPLAN
            reason = "已完成过半，建议重新规划"
        else:
            strategy = AdjustmentStrategy.RETRY
            reason = "未知错误，先重试"
        
        print(f"   策略: {strategy}")
        print(f"   原因: {reason}")
        return strategy
    
    def apply(self, state: PlanState, strategy: str) -> Plan:
        """应用调整"""
        print(f"🔧 应用调整: {strategy}")
        
        current_plan = state.plan
        state.adjustments += 1
        
        if strategy == AdjustmentStrategy.RETRY:
            # 重试，不改变计划
            return current_plan
        
        elif strategy == AdjustmentStrategy.REPLACE:
            # 替换方法（模拟）
            new_steps = []
            for step in current_plan.steps:
                if step.id == state.current_step + 1:
                    new_step = SubTask(
                        step.id,
                        step.description + " (换方法)",
                        tool=step.tool + "_alternative" if step.tool else None,
                        depends_on=step.depends_on
                    )
                    new_steps.append(new_step)
                else:
                    new_steps.append(step)
            return Plan(current_plan.task, new_steps)
        
        elif strategy == AdjustmentStrategy.REPLAN:
            # 重规划（模拟）
            print("   重新规划任务...")
            new_steps = [
                SubTask(1, "重新理解任务"),
                SubTask(2, "简化目标"),
                SubTask(3, "执行简化版本"),
            ]
            return Plan(current_plan.task + " (简化版)", new_steps)
        
        return current_plan


# 5. 带调整的执行器
class ExecutorWithAdjustment:
    def __init__(self, max_retries: int = 2):
        self.max_retries = max_retries
        self.adjustment_engine = AdjustmentEngine()
    
    def execute(self, task: str, steps: List[SubTask]) -> PlanState:
        """执行，带调整"""
        plan = Plan(task, steps)
        state = PlanState(plan)
        
        retry_count = 0
        
        while not state.current_step >= len(plan.steps):
            step = plan.steps[state.current_step]
            
            try:
                print(f"\n▶️  执行: {step.description}")
                # 模拟随机失败
                if random.random() < 0.3 and retry_count < self.max_retries:
                    raise Exception("模拟失败: timeout error")
                
                # 成功
                time.sleep(0.3)
                result = f"✅ {step.description} 完成"
                print(f"   {result}")
                state.completed.append(step.id)
                state.results[step.id] = result
                state.current_step += 1
                retry_count = 0
            
            except Exception as e:
                # 失败，处理
                retry_count += 1
                print(f"   ❌ 失败 (重试 {retry_count}/{self.max_retries})")
                
                if retry_count > self.max_retries:
                    # 超过重试上限，调整
                    strategy = self.adjustment_engine.analyze(state, step, e)
                    plan = self.adjustment_engine.apply(state, strategy)
                    state.plan = plan
                    retry_count = 0
        
        state.status = "success"
        return state


# 6. 测试
if __name__ == "__main__":
    print("="*60)
    print("🔧 动态调整演示")
    print("="*60)
    
    executor = ExecutorWithAdjustment(max_retries=1)
    
    # 测试任务
    test_steps = [
        SubTask(1, "步骤1: 收集信息"),
        SubTask(2, "步骤2: 处理数据"),
        SubTask(3, "步骤3: 生成报告"),
        SubTask(4, "步骤4: 发送结果"),
    ]
    
    state = executor.execute("测试任务", test_steps)
    
    print(f"\n📊 执行完成:")
    print(f"   状态: {state.status}")
    print(f"   调整次数: {state.adjustments}")
    print(f"   完成步骤: {len(state.completed)}/{len(state.plan.steps)}")
    
    print("\n🎉 动态调整示例完成!")
