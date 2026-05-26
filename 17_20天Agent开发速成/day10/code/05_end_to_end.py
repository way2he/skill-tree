
# -*- coding: utf-8 -*-
"""
Day10 代码示例 05: 端到端记忆系统
"""

import time
import sys
import io
from typing import List, Tuple

# 处理 Windows 编码问题
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# 1. 完整的记忆项
class MemoryItem:
    def __init__(self, content: str, memory_type: str = "general"):
        self.id = str(id(self))
        self.content = content
        self.memory_type = memory_type
        self.timestamp = time.time()
        self.last_access = self.timestamp
        self.access_count = 0
        self.importance = self._calculate_importance()
    
    def _calculate_importance(self) -> float:
        """计算重要性"""
        score = 0.0
        # 关键词
        keywords = ["重要", "关键", "必须", "记住", "生日", "会议", "密码"]
        score += min(sum(1 for kw in keywords if kw in self.content) * 0.15, 0.4)
        # 长度
        score += min(len(self.content) / 500, 0.3)
        # 访问次数
        score += min(self.access_count / 10, 0.3)
        return min(score, 1.0)
    
    def access(self):
        self.access_count += 1
        self.last_access = time.time()
        self.importance = self._calculate_importance()


# 2. 端到端记忆系统
class EndToEndMemorySystem:
    """端到端记忆系统"""
    
    def __init__(self, max_long_term: int = 50):
        self.short_term: List[MemoryItem] = []
        self.long_term: List[MemoryItem] = []
        self.max_short_term = 20
        self.max_long_term = max_long_term
    
    def add(self, content: str, memory_type: str = "general"):
        """添加记忆"""
        item = MemoryItem(content, memory_type)
        
        # 添加到短期记忆
        self.short_term.append(item)
        if len(self.short_term) > self.max_short_term:
            self.short_term.pop(0)
        
        # 添加到长期记忆
        self.long_term.append(item)
        if len(self.long_term) > self.max_long_term:
            self._forget()
        
        print(f"🧠 添加: {content[:25]}...")
    
    def _jaccard(self, a: str, b: str) -> float:
        """Jaccard 相似度"""
        set_a = set(a.lower().split())
        set_b = set(b.lower().split())
        if not set_a or not set_b:
            return 0
        return len(set_a & set_b) / len(set_a | set_b)
    
    def _time_decay(self, timestamp: float) -> float:
        """时间衰减"""
        days = (time.time() - timestamp) / (24 * 3600)
        return max(0, 1 - days / 30)
    
    def retrieve(self, query: str, top_k: int = 5) -> List[MemoryItem]:
        """检索"""
        print(f"\n🔍 查询: '{query}'")
        
        # 1. 短期记忆检索
        short_candidates = []
        for item in self.short_term:
            sim = self._jaccard(query, item.content)
            if sim > 0:
                short_candidates.append((item, 0.6 * sim + 0.4 * self._time_decay(item.timestamp)))
        
        # 2. 长期记忆检索（混合）
        long_candidates = []
        for item in self.long_term:
            sim = self._jaccard(query, item.content)
            if sim > 0:
                score = (
                    0.4 * sim +
                    0.4 * item.importance +
                    0.2 * self._time_decay(item.last_access)
                )
                long_candidates.append((item, score))
        
        # 3. 合并结果
        all_candidates = short_candidates + long_candidates
        seen = set()
        unique = []
        for item, score in all_candidates:
            if item.id not in seen:
                seen.add(item.id)
                unique.append((item, score))
        
        # 4. 排序
        unique.sort(key=lambda x: x[1], reverse=True)
        
        # 5. 标记访问
        results = []
        for i, (item, score) in enumerate(unique[:top_k], 1):
            item.access()
            results.append(item)
            print(f"   {i}. [score={score:.3f}] {item.content[:40]}")
        
        return results
    
    def _forget(self):
        """遗忘"""
        print(f"🔰 遗忘触发 (当前 {len(self.long_term)}/{self.max_long_term})")
        
        # 计算遗忘分数
        scored = []
        for item in self.long_term:
            forget_score = 0.7 * (1 - item.importance) + 0.3 * (1 - self._time_decay(item.last_access))
            scored.append((item, forget_score))
        
        # 排序删除
        scored.sort(key=lambda x: x[1], reverse=True)
        num_to_delete = len(self.long_term) - self.max_long_term
        to_delete = [item for item, _ in scored[:num_to_delete]]
        
        for item in to_delete:
            self.long_term.remove(item)
            print(f"   ❌ 删除: {item.content[:20]}...")
    
    def status(self):
        """状态"""
        print(f"\n📊 记忆状态:")
        print(f"   短期记忆: {len(self.short_term)} 条")
        print(f"   长期记忆: {len(self.long_term)} 条")


# 3. 测试
if __name__ == "__main__":
    print("="*60)
    print("🧠 端到端记忆系统演示")
    print("="*60)
    
    memory = EndToEndMemorySystem(max_long_term=10)
    
    # 添加一些记忆
    print("\n📝 添加记忆:")
    memory.add("用户喜欢吃火锅，特别是辣的")
    memory.add("用户住在北京，经常出差")
    memory.add("重要！今天的会议改到下午3点了")
    memory.add("用户的生日是12月25日，别忘了")
    memory.add("明天天气可能会下雨，记得带伞")
    memory.add("这个项目的截止日期是下周五")
    
    # 检索
    print("\n" + "="*60)
    print("🔍 检索测试:")
    print("="*60)
    
    results = memory.retrieve("用户")
    results = memory.retrieve("会议")
    
    # 状态
    memory.status()
    
    print("\n🎉 端到端记忆系统示例完成!")
