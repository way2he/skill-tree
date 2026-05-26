
# -*- coding: utf-8 -*-
"""
Day06 Code 03：查询重写
"""

print("=" * 60)
print("Day06 - 查询重写演示")
print("=" * 60)

# 查询重写提示词模板
QUERY_REWRITE_TEMPLATE = """
你是一个查询重写助手，把用户查询改写成更适合做向量检索的形式。

要求:
1. 简洁明了，保留关键信息
2. 可以适当扩展相关关键词
3. 输出 3-5 种不同的查询表达

用户查询: {query}

重写后的查询（每行一个）:
"""

# 例子
query = "我想知道怎么系统地学习 Python，有没有推荐的路线？"

print(f"\n原查询:\n{query}")
print("\n" + "=" * 60)
print("重写后的查询:")
print("=" * 60)
print("1. Python 系统学习路线")
print("2. Python 学习路径推荐")
print("3. 如何系统学习 Python")
print("4. Python 入门到精通学习路线")
print("5. Python 学习规划")

print("\n" + "=" * 60)
print("4 种查询重写方法:")
print("=" * 60)
print("""
1. 查询精简: 把啰嗦的变简洁
2. 查询扩展: 增加相关关键词
3. 查询拆解: 复杂问题拆成子问题
4. 多查询生成: 生成多个不同表达
""")
