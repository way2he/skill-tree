
# -*- coding: utf-8 -*-
"""
Day15 Code 01: 核心模块骨架
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass

print("=" * 60)
print("Day15 - 核心模块骨架")
print("=" * 60)


# ==========================================
# 数据模型
# ==========================================

@dataclass
class ExecutionResult:
    """代码执行结果"""
    success: bool
    stdout: str
    stderr: str
    output: Any = None
    execution_time: float = 0.0


@dataclass
class CodeInterpreterResponse:
    """代码解释器的最终响应"""
    user_query: str
    generated_code: str
    execution_result: ExecutionResult
    interpretation: str
    success: bool


# ==========================================
# 核心模块接口
# ==========================================

class BaseModule:
    """模块基类"""

    def __init__(self, name: str):
        self.name = name

    def initialize(self):
        """初始化"""
        pass


class CodeGenerator(BaseModule):
    """代码生成器"""

    def __init__(self, llm=None):
        super().__init__("CodeGenerator")
        self.llm = llm

    def generate(self, user_query: str, context: Optional[str] = None) -&gt; str:
        """
        生成代码

        Args:
            user_query: 用户的查询
            context: 上下文（可选）

        Returns:
            生成的代码
        """
        print(f"\n🤖 代码生成器: 理解用户请求 '{user_query[:30]}...'")
        # 这里应该调用 LLM 生成代码
        # 为了演示，我们返回模拟代码
        return """
import pandas as pd

# 创建简单的 DataFrame
data = {
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'score': [85, 90, 95]
}
df = pd.DataFrame(data)
print("数据:")
print(df)
print("\\n平均分:", df['score'].mean())
"""


class CodeExecutor(BaseModule):
    """代码执行器"""

    def __init__(self):
        super().__init__("CodeExecutor")
        self.max_execution_time = 30  # 30秒超时

    def execute(self, code: str) -&gt; ExecutionResult:
        """
        执行代码

        Args:
            code: 要执行的代码

        Returns:
            执行结果
        """
        print(f"\n⚙️  代码执行器: 执行代码...")
        # 这里应该在沙箱中执行代码
        # 为了演示，我们返回模拟结果
        return ExecutionResult(
            success=True,
            stdout="""
数据:
      name  age  score
0    Alice   25     85
1      Bob   30     90
2  Charlie   35     95

平均分: 90.0
""",
            stderr="",
            output=None,
            execution_time=0.5
        )


class ResultInterpreter(BaseModule):
    """结果解释器"""

    def __init__(self, llm=None):
        super().__init__("ResultInterpreter")
        self.llm = llm

    def interpret(self, execution_result: ExecutionResult, user_query: str) -&gt; str:
        """
        解释执行结果

        Args:
            execution_result: 执行结果
            user_query: 用户的查询

        Returns:
            自然语言解释
        """
        print(f"\n📊 结果解释器: 解释结果...")
        # 这里应该调用 LLM 解释结果
        # 为了演示，我们返回模拟解释
        if execution_result.success:
            return """
✅ 代码执行成功！

执行结果:
1. 创建了一个包含 3 条数据的 DataFrame
2. 数据包含姓名、年龄、分数信息
3. 计算了平均分：90.0

这就是你要的结果！
"""
        else:
            return f"""
❌ 代码执行出错！

错误信息:
{execution_result.stderr}
"""


class CodeInterpreterOrchestrator(BaseModule):
    """协调器 - 整个系统的核心"""

    def __init__(self, llm=None):
        super().__init__("Orchestrator")
        self.code_generator = CodeGenerator(llm)
        self.code_executor = CodeExecutor()
        self.result_interpreter = ResultInterpreter(llm)

    def run(self, user_query: str) -&gt; CodeInterpreterResponse:
        """
        运行整个流程

        Args:
            user_query: 用户的查询

        Returns:
            最终响应
        """
        print("\n" + "=" * 60)
        print(f"🚀 代码解释器启动: '{user_query}'")
        print("=" * 60)

        # 步骤 1: 生成代码
        code = self.code_generator.generate(user_query)

        # 步骤 2: 执行代码
        execution_result = self.code_executor.execute(code)

        # 步骤 3: 解释结果
        interpretation = self.result_interpreter.interpret(
            execution_result,
            user_query
        )

        # 返回完整响应
        return CodeInterpreterResponse(
            user_query=user_query,
            generated_code=code,
            execution_result=execution_result,
            interpretation=interpretation,
            success=execution_result.success
        )


# ==========================================
# 演示
# ==========================================

print("\n[1/2] 初始化代码解释器...")
interpreter = CodeInterpreterOrchestrator()

print("\n[2/2] 运行示例查询...")
user_query = "帮我创建一个简单的 DataFrame 并计算平均分"
response = interpreter.run(user_query)

print("\n" + "=" * 60)
print("✅ 代码解释器运行完成！")
print("=" * 60)
print("\n📋 最终响应:")
print("-" * 60)
print(response.interpretation)
print("=" * 60)

