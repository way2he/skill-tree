
# -*- coding: utf-8 -*-
"""
Day10 代码示例 01: 记忆系统基础
"""

from typing import List, Dict, Any
import time
import sys
import io

# 处理 Windows 编码问题
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# 1. 记忆项
class MemoryItem:
    """记忆项"""
    
    def __init__(self, content: str, memory_type: str = "general"):
        self.id = str(id(self))
        self.content = content
        self.memory_type = memory_type
        self.timestamp = time.time()
        self.access_count = 0
        self.importance = 0.5  # 默认重要性
    
    def access(self):
        """访问时更新"""
        self.access_count += 1
        self.last_access = time.time()
    
    def __repr__(self):
        return f"MemoryItem(content='{self.content[:20]}...', importance={self.importance})"


# 2. 短期记忆
class ShortTermMemory:
    """短期/工作记忆"""
    
    def __init__(self, max_items: int = 20):
        self.items: List[MemoryItem] = []
        self.max_items = max_items
    
    def add(self, item: MemoryItem):
        """添加记忆"""
        self.items.append(item)
        # 超过容量，删除最早的
        if len(self.items) > self.max_items:
            self.items.pop(0)
        print(f"🧠 短期记忆: 添加 '{item.content[:20]}...'")
    
    def get_recent(self, n: int = 5) -> List[MemoryItem]:
        """获取最近的 n 条"""
        return self.items[-n:]
    
    def clear(self):
        """清空"""
        self.items = []


# 3. 长期记忆（简化版）
class LongTermMemory:
    """长期记忆"""
    
    def __init__(self):
        self.items: Dict[str, MemoryItem] = {}
        print("💾 长期记忆: 初始化")
    
    def add(self, item: MemoryItem):
        """添加记忆"""
        self.items[item.id] = item
        print(f"💾 长期记忆: 保存 '{item.content[:20]}...'")
    
    def retrieve(self, query: str, top_k: int = 5) -> List[MemoryItem]:
        """检索（简化版关键词匹配）"""
        print(f"🔍 长期记忆: 检索 '{query}'")
        
        # 简化：关键词匹配 + 按重要性和时间排序
        candidates = []
        for item in self.items.values():
            if query.lower() in item.content.lower():
                candidates.append(item)
        
        # 排序：重要性 + 时间
        candidates.sort(
            key=lambda x: (x.importance, x.timestamp),
            reverse=True
        )
        
        result = candidates[:top_k]
        print(f"   找到 {len(result)} 条相关记忆")
        return result


# 4. 三层记忆系统
class ThreeLayerMemorySystem:
    """三层记忆系统"""
    
    def __init__(self):
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory()
        print("="*60)
        print("🧠 三层记忆系统初始化完成")
        print("="*60)
    
    def add(self, content: str, memory_type: str = "general"):
        """添加记忆"""
        item = MemoryItem(content, memory_type)
        
        # 添加到短期记忆
        self.short_term.add(item)
        
        # 同时添加到长期记忆（简化，实际应该是异步或筛选）
        self.long_term.add(item)
    
    def retrieve(self, query: str, top_k: int = 5) -> List[MemoryItem]:
        """检索"""
        print(f"\n🤔 查询: {query}")
        
        # 先从短期记忆找
        results = []
        recent = self.short_term.get_recent(top_k)
        for item in recent:
            if query.lower() in item.content.lower():
                item.access()
                results.append(item)
        
        # 不够，从长期记忆补充
        if len(results) < top_k:
            more = self.long_term.retrieve(query, top_k - len(results))
            for item in more:
                if item not in results:
                    item.access()
                    results.append(item)
        
        print(f"✅ 共找到 {len(results)} 条相关记忆")
        return results


# 5. 测试
if __name__ == "__main__":
    memory = ThreeLayerMemorySystem()
    
    # 添加一些记忆
    print("\n📝 添加记忆:")
    memory.add("用户喜欢吃火锅，特别是辣的")
    memory.add("用户住在北京，经常出差")
    memory.add("用户的生日是12月25日")
    memory.add("今天的会议改到下午3点了")
    
    # 检索
    print("\n" + "="*60)
    print("🔍 检索测试:")
    print("="*60)
    
    results = memory.retrieve("用户")
    for i, item in enumerate(results, 1):
        print(f"\n{i}. {item.content}")
        print(f"   重要性: {item.importance}, 访问次数: {item.access_count}")
    
    print("\n🎉 记忆系统基础示例完成!")
