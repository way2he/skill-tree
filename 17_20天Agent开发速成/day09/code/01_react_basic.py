
# -*- coding: utf-8 -*-
"""
Day09 代码示例 01: ReAct 基础实现
"""

import sys
import io
import time

# 处理 Windows 编码问题
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# 1. 模拟工具
class MockTools:
    """模拟工具集"""
    
    @staticmethod
    def search(query):
        """模拟搜索"""
        print(f"🔍 搜索: {query}")
        time.sleep(0.5)
        
        # 模拟搜索结果
        if "GDP" in query and "2023" in query:
            return "2023年中国GDP为126万亿元"
        elif "人口" in query and "2023" in query:
            return "2023年中国人口约为14.1亿"
        elif "首都" in query:
            return "中国的首都是北京"
        else:
            return f"关于 '{query}' 的搜索结果..."
    
    @staticmethod
    def calculate(expression):
        """模拟计算"""
        print(f"🧮 计算: {expression}")
        time.sleep(0.3)
        try:
            # 简单的安全计算
            allowed_chars = set("0123456789+-*/(). ")
            if all(c in allowed_chars for c in expression):
                result = eval(expression)
                return str(result)
            else:
                return "无效的表达式"
        except:
            return "计算错误"


# 2. 模拟 LLM（为了演示，这里用规则模拟）
def mock_llm(prompt):
    """模拟 LLM 的 ReAct 输出"""
    print(f"\n💭 LLM 思考中...")
    time.sleep(0.5)
    
    # 从 prompt 中提取问题
    if "GDP" in prompt:
        return (
            "Thought: 我需要搜索 2023年中国GDP\n"
            "Action: Search\n"
            "Action Input: 2023年中国GDP"
        )
    elif "搜索结果" in prompt:
        if "126万亿元" in prompt:
            return (
                "Thought: 我找到了答案，可以回答了\n"
                "Action: Finish\n"
                "Action Input: 2023年中国GDP为126万亿元"
            )
    elif "人口" in prompt:
        return (
            "Thought: 我需要搜索 2023年中国人口\n"
            "Action: Search\n"
            "Action Input: 2023年中国人口"
        )
    else:
        return (
            "Thought: 让我搜索一下\n"
            "Action: Search\n"
            "Action Input: " + prompt.split("问题:")[-1].strip()
        )


# 3. 解析 ReAct 输出
def parse_react_output(output):
    """解析 ReAct 格式输出"""
    thought = ""
    action = ""
    action_input = ""
    
    lines = output.strip().split("\n")
    for line in lines:
        if line.startswith("Thought:"):
            thought = line[len("Thought:"):].strip()
        elif line.startswith("Action:"):
            action = line[len("Action:"):].strip()
        elif line.startswith("Action Input:"):
            action_input = line[len("Action Input:"):].strip()
    
    return thought, action, action_input


# 4. ReAct 循环
def react_loop(question, tools, max_steps=5):
    """ReAct 主循环"""
    print("="*60)
    print(f"🤔 问题: {question}")
    print("="*60)
    
    history = []
    tools_map = {
        "Search": tools.search,
        "Calculate": tools.calculate
    }
    
    for step in range(1, max_steps + 1):
        print(f"\n--- 步骤 {step} ---")
        
        # 构建 prompt
        prompt = build_react_prompt(question, history)
        
        # 调用 LLM
        output = mock_llm(prompt)
        print(f"📤 LLM 输出:\n{output}")
        
        # 解析输出
        thought, action, action_input = parse_react_output(output)
        
        print(f"\n💭 Thought: {thought}")
        print(f"🎯 Action: {action}")
        print(f"📥 Action Input: {action_input}")
        
        # 执行行动
        if action == "Finish":
            print(f"\n✅ 完成！答案: {action_input}")
            return action_input
        elif action in tools_map:
            observation = tools_map[action](action_input)
            print(f"👁️  Observation: {observation}")
        else:
            observation = f"未知工具: {action}"
            print(f"⚠️  {observation}")
        
        # 记录历史
        history.append({
            "thought": thought,
            "action": action,
            "action_input": action_input,
            "observation": observation
        })
        
        # 检查是否在观察中找到了答案（模拟）
        if "126万亿元" in observation or "14.1亿" in observation:
            print(f"\n💭 (模拟 LLM 看到结果后决定结束)")
            print(f"✅ 完成！答案: {observation}")
            return observation
    
    print("\n❌ 未能在规定步骤内解决问题")
    return None


# 5. 构建 ReAct 提示词
def build_react_prompt(question, history):
    """构建 ReAct 提示词"""
    prompt = """你是一个有帮助的助手。你可以使用以下工具：

- Search: 搜索信息
- Calculate: 计算
- Finish: 结束并给出答案

按照以下格式输出：

Thought: 你的思考
Action: 工具名称
Action Input: 工具输入
Observation: 工具输出
...（重复）

Thought: 我知道最终答案了
Action: Finish
Action Input: 最终答案

现在开始！
"""
    
    prompt += f"问题: {question}\n\n"
    
    # 加入历史
    for item in history:
        prompt += f"Thought: {item['thought']}\n"
        prompt += f"Action: {item['action']}\n"
        prompt += f"Action Input: {item['action_input']}\n"
        prompt += f"Observation: {item['observation']}\n\n"
    
    return prompt


# 6. 测试
if __name__ == "__main__":
    tools = MockTools()
    
    # 测试 1
    react_loop("2023年中国GDP是多少？", tools)
    
    print("\n" + "="*60)
    print("🎉 ReAct 基础示例完成！")
    print("="*60)
