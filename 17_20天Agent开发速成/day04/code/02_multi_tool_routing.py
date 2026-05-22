# -*- coding: utf-8 -*-
"""
Day04 - 02: 多工具智能路由（语义向量召回 Top-K）
功能：当工具数量很大时，按用户 query 用 embedding 余弦相似度召回最相关的 K 个工具
"""
import os
import numpy as np
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "your-key"))


# ============ 1. 所有可用工具及其描述 ============
ALL_TOOLS = {
    "get_weather": "查询城市的实时天气，包括温度和天气状况",
    "search_web": "联网搜索最新的新闻、资讯、知识等公开信息",
    "search_knowledge_base": "搜索企业内部知识库的产品文档、规章制度",
    "send_email": "发送电子邮件给指定收件人",
    "create_calendar_event": "创建日历事件，安排会议或提醒",
    "query_order": "根据订单号查询订单详情和物流状态",
    "calc_electricity_bill": "计算指定月份的电费账单",
    "translate_text": "将文本翻译成指定语言",
    "summarize_document": "对长文档进行摘要总结",
    "generate_image": "根据文字描述生成图片",
}


# ============ 2. 离线把所有工具描述向量化（生产环境存 Milvus/Qdrant）============
def embed(text: str) -> np.ndarray:
    resp = client.embeddings.create(model="text-embedding-3-large", input=text)
    return np.array(resp.data[0].embedding)


print("📦 正在为所有工具生成 embedding（首次需要 10-20s）...")
TOOL_VECTORS = {name: embed(desc) for name, desc in ALL_TOOLS.items()}


# ============ 3. 运行时路由：按 query 召回 Top-K 工具 ============
def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def route_tools(user_query: str, top_k: int = 3) -> list:
    """根据用户 query 召回最相关的 K 个工具"""
    q_vec = embed(user_query)
    scored = [
        (name, cosine_similarity(q_vec, vec))
        for name, vec in TOOL_VECTORS.items()
    ]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]


# ============ 4. 演示 ============
if __name__ == "__main__":
    test_queries = [
        "上海明天会下雨吗？",
        "帮我查一下订单 ORD-2026052201 的物流",
        "把这份合同翻译成英文",
        "5 月份用了 380 度电，电费多少？",
    ]

    for query in test_queries:
        print(f"\n👤 Query: {query}")
        results = route_tools(query, top_k=3)
        print("🎯 召回 Top-3 工具：")
        for name, score in results:
            print(f"  - {name:30s} 相似度: {score:.4f}")
        print(f"💰 Token 节省：从 10 工具 → 3 工具，约节省 70%")
