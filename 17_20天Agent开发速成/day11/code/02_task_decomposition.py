
# -*- coding: utf-8 -*-
"""
Day11 代码示例 02: 任务拆解
"""

import sys
import io
from typing import List, Dict, Any

# 处理 Windows 编码问题
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# 1. 子任务
class SubTask:
    def __init__(self, id: int, description: str, 
                 tool: str = None, depends_on: List[int] = None,
                 expected_output: str = None):
        self.id = id
        self.description = description
        self.tool = tool
        self.depends_on = depends_on or []
        self.expected_output = expected_output
    
    def __repr__(self):
        return f"SubTask(id={self.id}, '{self.description[:20]}...')"


# 2. 任务拆解器
class TaskDecomposer:
    """任务拆解器"""
    
    def __init__(self):
        self.decomposition_strategies = {
            "sequential": self._decompose_sequential,
            "by_component": self._decompose_by_component,
            "by_abstraction": self._decompose_by_abstraction,
        }
    
    def decompose(self, task: str, strategy: str = "sequential") -> List[SubTask]:
        """拆解任务"""
        print(f"📋 拆解任务: {task}")
        print(f"   策略: {strategy}")
        
        strat_func = self.decomposition_strategies.get(strategy, self._decompose_sequential)
        subtasks = strat_func(task)
        
        print(f"   拆解为 {len(subtasks)} 个子任务")
        for st in subtasks:
            dep_str = f" [依赖: {st.depends_on}]" if st.depends_on else ""
            print(f"   {st.id}. {st.description}{dep_str}")
        
        return subtasks
    
    def _decompose_sequential(self, task: str) -> List[SubTask]:
        """按步骤拆解"""
        # 实际应该调用 LLM，这里用规则模拟
        subtasks = []
        
        if "网站" in task or "系统" in task:
            subtasks = [
                SubTask(1, "收集需求，明确功能", "requirements"),
                SubTask(2, "设计系统架构", "design", depends_on=[1]),
                SubTask(3, "开发前端", "frontend", depends_on=[2]),
                SubTask(4, "开发后端", "backend", depends_on=[2]),
                SubTask(5, "设计数据库", "database", depends_on=[2]),
                SubTask(6, "测试与调试", "testing", depends_on=[3, 4, 5]),
                SubTask(7, "部署上线", "deploy", depends_on=[6]),
            ]
        elif "文章" in task or "写作" in task:
            subtasks = [
                SubTask(1, "确定主题和大纲", "planning"),
                SubTask(2, "收集资料和素材", "research", depends_on=[1]),
                SubTask(3, "撰写初稿", "writing", depends_on=[2]),
                SubTask(4, "修改和润色", "editing", depends_on=[3]),
                SubTask(5, "最终定稿", "finalize", depends_on=[4]),
            ]
        else:
            subtasks = [
                SubTask(1, "理解任务", "understand"),
                SubTask(2, "制定计划", "planning", depends_on=[1]),
                SubTask(3, "执行计划", "execute", depends_on=[2]),
                SubTask(4, "总结结果", "summarize", depends_on=[3]),
            ]
        
        return subtasks
    
    def _decompose_by_component(self, task: str) -> List[SubTask]:
        """按组件拆解"""
        # 模拟
        return [
            SubTask(1, "组件A: 用户界面"),
            SubTask(2, "组件B: 业务逻辑"),
            SubTask(3, "组件C: 数据存储"),
            SubTask(4, "组件D: 集成测试"),
        ]
    
    def _decompose_by_abstraction(self, task: str) -> List[SubTask]:
        """按抽象层次拆解"""
        # 模拟
        return [
            SubTask(1, "层级1: 顶层设计"),
            SubTask(2, "层级2: 模块设计", depends_on=[1]),
            SubTask(3, "层级3: 详细实现", depends_on=[2]),
            SubTask(4, "层级4: 测试验证", depends_on=[3]),
        ]


# 3. 拆解策略对比
if __name__ == "__main__":
    print("="*60)
    print("🔪 任务拆解演示")
    print("="*60)
    
    decomposer = TaskDecomposer()
    
    test_task = "开发一个个人博客网站"
    
    print("\n" + "="*60)
    print("1️⃣  按步骤拆解:")
    print("="*60)
    decomposer.decompose(test_task, strategy="sequential")
    
    print("\n" + "="*60)
    print("2️⃣  按组件拆解:")
    print("="*60)
    decomposer.decompose(test_task, strategy="by_component")
    
    print("\n" + "="*60)
    print("3️⃣  按抽象层次拆解:")
    print("="*60)
    decomposer.decompose(test_task, strategy="by_abstraction")
    
    # 另一个测试
    print("\n" + "="*60)
    print("📝 另一个任务: 写一篇关于AI的文章")
    print("="*60)
    decomposer.decompose("写一篇关于AI的文章", strategy="sequential")
    
    print("\n🎉 任务拆解示例完成!")
