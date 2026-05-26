
# -*- coding: utf-8 -*-
"""
Day10 代码示例 04: 遗忘机制
"""

import time
import sys
import io
from typing import List

# 处理 Windows 编码问题
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# 1. 记忆项
class MemoryItem:
    def __init__(self, content: str, importance: float = 0.5):
        self.content = content
        self.timestamp = time.time()
        self.last_access = self.timestamp
        self.access_count = 0
        self.importance = importance
    
    def access(self):
        self.access_count += 1
        self.last_access = time.time()
    
    def __repr__(self):
        return f"MemoryItem(imp={self.importance:.2f}, content='{self.content[:15]}...')"


# 2. 带遗忘的记忆存储
class MemoryStoreWithForgetting:
    """带遗忘的记忆存储"""
    
    def __init__(self, max_size: int = 10):
        self.items: List[MemoryItem] = []
        self.max_size = max_size
    
    def add(self, item: MemoryItem):
        """添加记忆"""
        self.items.append(item)
        print(f"➕ 添加: {item}")
        
        # 检查是否需要遗忘
        if len(self.items) > self.max_size:
            self.forget()
    
    def calculate_forget_score(self, item: MemoryItem) -> float:
        """
        计算遗忘分数 [0, 1]，分数越高越应该被删除
        """
        score = 0.0
        
        # 1. 重要性 (权重 0.7)：越不重要，分数越高
        score += 0.7 * (1 - item.importance)
        
        # 2. 未访问时间 (权重 0.3)：越久没访问，分数越高
        days_since_access = (time.time() - item.last_access) / (24 * 3600)
        time_score = min(days_since_access / 365, 1.0)  # 最多1年
        score += 0.3 * time_score
        
        return score
    
    def forget(self):
        """执行遗忘"""
        print(f"\n🔰 触发遗忘！当前 {len(self.items)} 条，上限 {self.max_size}")
        
        # 计算每个记忆的遗忘分数
        scored = []
        for item in self.items:
            forget_score = self.calculate_forget_score(item)
            scored.append((item, forget_score))
            print(f"   {item.content[:20]}... -> 遗忘分数: {forget_score:.3f}")
        
        # 按遗忘分数排序（分数高的在前）
        scored.sort(key=lambda x: x[1], reverse=True)
        
        # 删除遗忘分数最高的
        num_to_delete = len(self.items) - self.max_size
        to_delete = [item for item, score in scored[:num_to_delete]]
        
        for item in to_delete:
            self.items.remove(item)
            print(f"❌ 删除: {item.content[:20]}...")
        
        print(f"✅ 遗忘完成！当前 {len(self.items)} 条\n")
    
    def __len__(self):
        return len(self.items)


# 3. 测试遗忘机制
if __name__ == "__main__":
    print("="*60)
    print("🔰 遗忘机制演示 (max_size=5)")
    print("="*60)
    
    store = MemoryStoreWithForgetting(max_size=5)
    
    # 添加一些记忆
    print("\n📝 添加记忆:")
    store.add(MemoryItem("普通消息 1", importance=0.2))
    store.add(MemoryItem("普通消息 2", importance=0.3))
    store.add(MemoryItem("重要会议！", importance=0.9))
    store.add(MemoryItem("普通消息 3", importance=0.2))
    store.add(MemoryItem("用户生日", importance=0.8))
    
    # 再添加，触发遗忘
    print("📝 继续添加，触发遗忘:")
    store.add(MemoryItem("普通消息 4", importance=0.2))
    store.add(MemoryItem("普通消息 5", importance=0.3))
    
    # 模拟访问某些记忆
    print("🔄 模拟访问重要记忆:")
    for item in store.items:
        if "会议" in item.content or "生日" in item.content:
            item.access()
            item.access()  # 访问两次
    
    # 再添加
    print("\n📝 再添加，观察遗忘:")
    store.add(MemoryItem("普通消息 6", importance=0.2))
    store.add(MemoryItem("普通消息 7", importance=0.3))
    
    # 查看当前记忆
    print("\n📋 当前记忆:")
    for item in store.items:
        days_since = (time.time() - item.timestamp) / (24 * 3600)
        print(f"   {item}, 访问次数: {item.access_count}")
    
    print("\n🎉 遗忘机制示例完成!")
