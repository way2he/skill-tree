
---
name: Plan-and-Execute模式
description: Plan-and-Execute模式：任务拆解、计划执行
type: learning-material
tags: ["Plan-and-Execute", "Agent", "任务拆解"]
summary: Plan-and-Execute模式：任务拆解、计划执行
created_at: 2026-05-26
updated_at: 2026-05-26
version: interview
---

# Plan-and-Execute 模式 📋

&gt; 🎯 **学习目标**：理解并实现 Plan-and-Execute 模式

---

## 一、Plan-and-Execute 概述

### 1.1 核心思想

```
先想好怎么做，再一步步做
```

**ReAct vs Plan-and-Execute 对比**：

| ReAct | Plan-and-Execute |
|-------|------------------|
| 边想边做，每步行动前思考 | 先整体规划，再一步步执行 |
| 灵活，适合探索性任务 | 结构清晰，适合复杂任务 |
| 可能重复或走弯路 | 效率更高，避免弯路 |

---

### 1.2 完整流程

```
1. 理解任务 (Understand)
   ↓
2. 制定计划 (Plan)
   - 拆解子任务
   - 确定顺序
   - 分配工具
   ↓
3. 执行计划 (Execute)
   - 按顺序执行
   - 记录状态
   ↓
4. 检查结果 (Review)
   - 是否成功？
   - 是否需要调整？
   ↓
5. 调整计划 (Adjust) [如需要]
   - 修改计划
   - 重新执行
   ↓
6. 完成 (Finish)
```

---

## 二、任务拆解

### 2.1 拆解方法

| 方法 | 说明 | 示例 |
|------|------|------|
| **按步骤** | 时间/逻辑顺序 | 注册→登录→填写信息→提交 |
| **按组件** | 系统组件 | 前端+后端+数据库+部署 |
| **按抽象层次** | 从粗到细 | 设计→实现→测试→发布 |

---

### 2.2 拆解器实现

```python
class TaskDecomposer:
    def decompose(self, task: str) -> List[SubTask]:
        """拆解任务"""
        prompt = f"""
将以下任务拆解为子任务，按执行顺序排列：
任务：{task}

要求：
1. 每个子任务明确可执行
2. 说明依赖关系
3. 标注所需工具
"""
        # 调用 LLM 获取子任务
        subtasks = self.llm(prompt)
        return self.parse_subtasks(subtasks)
```

---

## 三、计划执行

### 3.1 状态追踪

```python
class PlanState:
    def __init__(self, plan: Plan):
        self.plan = plan
        self.current_step = 0
        self.completed = []
        self.results = {}
        self.status = "in_progress"  # in_progress/success/failed
    
    def complete_step(self, step: int, result: Any):
        """完成一步"""
        self.completed.append(step)
        self.results[step] = result
        self.current_step += 1
    
    def is_done(self) -> bool:
        return self.current_step >= len(self.plan.steps)
```

---

### 3.2 执行循环

```python
class PlanExecutor:
    def execute(self, plan: Plan) -> PlanState:
        """执行计划"""
        state = PlanState(plan)
        
        while not state.is_done():
            step = plan.steps[state.current_step]
            
            try:
                # 执行当前步骤
                result = self.execute_step(step, state)
                state.complete_step(state.current_step, result)
                
                # 检查是否需要调整
                if self.needs_adjustment(result, step):
                    # 调整计划
                    plan = self.adjust_plan(plan, state, result)
                    
            except Exception as e:
                # 异常处理
                state.status = "failed"
                state.error = str(e)
                break
        
        return state
```

---

## 四、设计要点

### 4.1 计划表示

```yaml
plan:
  task: "组织一次生日聚会"
  steps:
    - id: 1
      description: "确定时间和地点"
      tool: "calendar"
      depends_on: []
    - id: 2
      description: "邀请朋友"
      tool: "email"
      depends_on: [1]
    - id: 3
      description: "预订蛋糕"
      tool: "shop"
      depends_on: [1]
```

---

### 4.2 原子性设计

```
每个子任务 = 原子操作 → 可独立验证结果
```

---

## 五、面试关键点

1. **P&E vs ReAct**：先规划 vs 边想边做
2. **任务拆解**：方法和原则
3. **状态管理**：追踪执行进度
4. **动态调整**：如何处理意外情况

---

**💡 实践建议**：从简单任务开始，逐步增加复杂度！
