
# -*- coding: utf-8 -*-
"""
Day10 代码示例 03: 检索策略
"""

import time
import sys
import io
from typing import List, Tuple

# 处理 Windows 编码问题
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# 1. 简化的记忆项
class MemoryItem:
    def __init__(self, content: str, timestamp: float = None):
        self.content = content
        self.timestamp = timestamp or time.time()
        self.importance = 0.5  # 默认重要性


# 2. 简单的向量相似度（用 Jaccard 模拟）
def jaccard_similarity(a: str, b: str) -> float:
    """Jaccard 相似度（模拟向量相似度）"""
    set_a = set(a.lower().split())
    set_b = set(b.lower().split())
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


# 3. 关键词匹配
def keyword_match(query: str, content: str) -> float:
    """关键词匹配分数"""
    query_words = query.lower().split()
    content_words = content.lower().split()
    matches = sum(1 for word in query_words if word in content_words)
    return matches / len(query_words) if query_words else 0.0


# 4. 时间衰减分数
def time_decay_score(timestamp: float) -> float:
    """时间衰减分数 [0, 1]，最近的更高"""
    days_ago = (time.time() - timestamp) / (24 * 3600)
    return max(0, 1 - days_ago / 30)  # 30天衰减


# 5. 各种检索策略
class RetrievalStrategies:
    """检索策略集合"""
    
    def __init__(self, memories: List[MemoryItem]):
        self.memories = memories
    
    def vector_retrieval(self, query: str, top_k: int = 5) -> List[Tuple[MemoryItem, float]]:
        """向量检索（语义相似度）"""
        print(f"🔍 向量检索: '{query}'")
        results = []
        for mem in self.memories:
            score = jaccard_similarity(query, mem.content)
            results.append((mem, score))
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
    
    def keyword_retrieval(self, query: str, top_k: int = 5) -> List[Tuple[MemoryItem, float]]:
        """关键词检索"""
        print(f"🔍 关键词检索: '{query}'")
        results = []
        for mem in self.memories:
            score = keyword_match(query, mem.content)
            results.append((mem, score))
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
    
    def time_retrieval(self, top_k: int = 5) -> List[Tuple[MemoryItem, float]]:
        """时间检索"""
        print(f"🔍 时间检索 (最近优先)")
        results = [(mem, time_decay_score(mem.timestamp)) for mem in self.memories]
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
    
    def hybrid_retrieval(self, query: str, top_k: int = 5) -> List[Tuple[MemoryItem, float]]:
        """混合检索"""
        print(f"🔍 混合检索: '{query}'")
        
        # 多路召回
        vector_results = self.vector_retrieval(query, top_k * 2)
        keyword_results = self.keyword_retrieval(query, top_k * 2)
        
        # 合并去重
        seen = set()
        candidates = {}
        for mem, score in vector_results:
            if id(mem) not in seen:
                seen.add(id(mem))
                candidates[mem] = {"vector": score, "keyword": 0.0, "time": 0.0}
        
        for mem, score in keyword_results:
            if id(mem) in candidates:
                candidates[mem]["keyword"] = score
            elif id(mem) not in seen:
                seen.add(id(mem))
                candidates[mem] = {"vector": 0.0, "keyword": score, "time": 0.0}
        
        # 计算时间分数
        for mem in candidates:
            candidates[mem]["time"] = time_decay_score(mem.timestamp)
        
        # 重排序
        final_results = []
        for mem, scores in candidates.items():
            # 加权求和
            total_score = (
                0.5 * scores["vector"] +
                0.3 * scores["keyword"] +
                0.2 * scores["time"]
            )
            final_results.append((mem, total_score))
        
        final_results.sort(key=lambda x: x[1], reverse=True)
        return final_results[:top_k]


# 6. 测试
if __name__ == "__main__":
    print("="*60)
    print("🔍 检索策略演示")
    print("="*60)
    
    # 创建测试记忆
    now = time.time()
    memories = [
        MemoryItem("用户喜欢吃火锅，特别是辣的", now - 86400 * 7),  # 7天前
        MemoryItem("用户住在北京，经常出差", now - 86400 * 3),  # 3天前
        MemoryItem("今天的会议改到下午3点了", now),  # 今天
        MemoryItem("用户的生日是12月25日", now - 86400 * 14),  # 14天前
        MemoryItem("火锅很好吃，我也喜欢辣的", now - 86400 * 1),  # 1天前
    ]
    
    strategies = RetrievalStrategies(memories)
    query = "用户喜欢吃火锅"
    
    # 各种检索策略
    print(f"\n\n1️⃣  向量检索:")
    for i, (mem, score) in enumerate(strategies.vector_retrieval(query), 1):
        print(f"   {i}. [score={score:.3f}] {mem.content[:30]}")
    
    print(f"\n\n2️⃣  关键词检索:")
    for i, (mem, score) in enumerate(strategies.keyword_retrieval(query), 1):
        print(f"   {i}. [score={score:.3f}] {mem.content[:30]}")
    
    print(f"\n\n3️⃣  时间检索:")
    for i, (mem, score) in enumerate(strategies.time_retrieval(), 1):
        print(f"   {i}. [score={score:.3f}] {mem.content[:30]}")
    
    print(f"\n\n4️⃣  混合检索:")
    for i, (mem, score) in enumerate(strategies.hybrid_retrieval(query), 1):
        print(f"   {i}. [score={score:.3f}] {mem.content[:30]}")
    
    print("\n🎉 检索策略示例完成!")
