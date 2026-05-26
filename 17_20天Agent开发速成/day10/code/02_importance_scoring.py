
# -*- coding: utf-8 -*-
"""
Day10 代码示例 02: 重要性评分
"""

import time
import sys
import io
from typing import Dict, Any

# 处理 Windows 编码问题
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# 1. 记忆项（增加重要性计算）
class MemoryItemWithImportance:
    """带重要性的记忆项"""
    
    def __init__(self, content: str):
        self.content = content
        self.timestamp = time.time()
        self.access_count = 0
        self.last_access = self.timestamp
        self.importance = self.calculate_importance()
    
    def access(self):
        self.access_count += 1
        self.last_access = time.time()
        # 访问时重新计算重要性
        self.importance = self.calculate_importance()
    
    def calculate_importance(self) -> float:
        """计算重要性分数 [0, 1]"""
        score = 0.0
        
        # 维度 1: 内容特征
        # 1a: 关键词
        important_keywords = ["重要", "关键", "必须", "记住", "生日", "密码", "会议"]
        keyword_count = sum(1 for kw in important_keywords if kw in self.content)
        score += min(keyword_count * 0.1, 0.3)
        
        # 1b: 长度（越长越可能重要）
        length_score = min(len(self.content) / 500, 0.2)
        score += length_score
        
        # 1c: 完整性（有标点、有结构）
        if any(p in self.content for p in ["。", "！", "？", "."]):
            score += 0.1
        
        # 维度 2: 访问频率
        access_score = min(self.access_count / 10, 0.2)
        score += access_score
        
        # 维度 3: 时间衰减（最近访问过的更重要）
        days_since_access = (time.time() - self.last_access) / (24 * 3600)
        time_score = max(0, 1 - days_since_access / 30)  # 30天衰减
        score += 0.2 * time_score
        
        # 归一化
        return min(score, 1.0)
    
    def __repr__(self):
        return (f"MemoryItem(importance={self.importance:.3f}, "
                f"content='{self.content[:20]}...')")


# 2. 重要性评分演示
if __name__ == "__main__":
    print("="*60)
    print("📊 重要性评分演示")
    print("="*60)
    
    # 测试记忆
    test_memories = [
        "这是一条普通的消息",
        "重要！今天的会议改到下午3点了",
        "用户的生日是12月25日，每年都要记得送礼物",
        "随便说点什么",
        "会议要点：1. 项目延期 2. 预算调整 3. 下周汇报",
    ]
    
    print("\n📝 测试记忆项:")
    for i, content in enumerate(test_memories, 1):
        item = MemoryItemWithImportance(content)
        print(f"\n{i}. 内容: {content}")
        print(f"   重要性: {item.importance:.3f}")
        
        # 模拟访问几次
        if i in [2, 3]:
            for _ in range(3):
                item.access()
            print(f"   访问 {item.access_count} 次后重要性: {item.importance:.3f}")
    
    # 排序演示
    print("\n" + "="*60)
    print("🔽 按重要性排序:")
    print("="*60)
    
    items = [MemoryItemWithImportance(c) for c in test_memories]
    items.sort(key=lambda x: x.importance, reverse=True)
    
    for i, item in enumerate(items, 1):
        print(f"{i}. [重要性: {item.importance:.3f}] {item.content[:30]}...")
    
    print("\n🎉 重要性评分示例完成!")
