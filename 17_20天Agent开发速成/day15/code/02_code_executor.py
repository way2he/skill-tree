
# -*- coding: utf-8 -*-
"""
Day15 Code 02: 安全的代码执行器
"""

import sys
import io
import time
import traceback
from typing import Dict, Any, Optional
from dataclasses import dataclass

print("=" * 60)
print("Day15 - 安全的代码执行器")
print("=" * 60)


@dataclass
class ExecutionResult:
    """代码执行结果"""
    success: bool
    stdout: str
    stderr: str
    output: Any = None
    execution_time: float = 0.0
    exception: Optional[Exception] = None


class SafeCodeExecutor:
    """安全的代码执行器"""

    def __init__(self, max_execution_time: int = 30):
        self.max_execution_time = max_execution_time
        # 安全的全局变量（只允许一些安全的模块）
        self.safe_globals = {
            '__builtins__': {
                'print': print,
                'len': len,
                'range': range,
                'str': str,
                'int': int,
                'float': float,
                'list': list,
                'dict': dict,
                'tuple': tuple,
                'set': set,
                'abs': abs,
                'sum': sum,
                'min': min,
                'max': max,
            }
        }
        # 可以安全导入的模块
        self.allowed_modules = {
            'math': __import__('math'),
            'random': __import__('random'),
            'datetime': __import__('datetime'),
        }

    def _add_allowed_modules(self, globals_dict: dict):
        """添加允许的模块"""
        for name, module in self.allowed_modules.items():
            globals_dict[name] = module

    def execute(self, code: str, safe_mode: bool = True) -&gt; ExecutionResult:
        """
        执行代码

        Args:
            code: 要执行的代码
            safe_mode: 是否使用安全模式

        Returns:
            执行结果
        """
        start_time = time.time()

        # 重定向 stdout 和 stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        old_stdout = sys.stdout
        old_stderr = sys.stderr

        success = False
        exception = None

        try:
            sys.stdout = stdout_capture
            sys.stderr = stderr_capture

            # 准备 globals 和 locals
            exec_globals = {}
            if safe_mode:
                exec_globals.update(self.safe_globals)
                self._add_allowed_modules(exec_globals)

            exec_locals = {}

            # 执行代码
            exec(code, exec_globals, exec_locals)

            # 尝试获取返回值
            output = exec_locals.get('_result', None)

            success = True

        except Exception as e:
            exception = e
            traceback.print_exc()

        finally:
            # 恢复 stdout 和 stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        execution_time = time.time() - start_time

        result = ExecutionResult(
            success=success,
            stdout=stdout_capture.getvalue(),
            stderr=stderr_capture.getvalue(),
            output=output if success else None,
            execution_time=execution_time,
            exception=exception
        )

        return result


# ==========================================
# 演示
# ==========================================

print("\n[1/4] 初始化安全代码执行器...")
executor = SafeCodeExecutor(max_execution_time=30)

print("\n[2/4] 测试 1: 简单的数学计算...")
code1 = """
import math

# 计算一些数学
result = math.sqrt(16) + math.pow(2, 3)
print(f"结果: {result}")

# 也可以把结果存在 _result 里
_result = result
"""
result1 = executor.execute(code1)
print(f"✅ 成功: {result1.success}")
print(f"⏱️  耗时: {result1.execution_time:.2f}秒")
print(f"📤 输出:\n{result1.stdout}")

print("\n[3/4] 测试 2: 列表操作...")
code2 = """
# 列表操作
numbers = [1, 2, 3, 4, 5]
squares = [x*x for x in numbers]
print(f"原列表: {numbers}")
print(f"平方: {squares}")
print(f"和: {sum(squares)}")

_result = squares
"""
result2 = executor.execute(code2)
print(f"✅ 成功: {result2.success}")
print(f"📤 输出:\n{result2.stdout}")

print("\n[4/4] 测试 3: 故意出错（看错误处理）...")
code3 = """
# 这会出错
x = 1 / 0
"""
result3 = executor.execute(code3)
print(f"✅ 成功: {result3.success}")
print(f"❌ 错误:\n{result3.stderr}")

print("\n" + "=" * 60)
print("✅ 安全代码执行器演示完成！")
print("=" * 60)
print("\n总结:")
print("- 可以安全地执行代码")
print("- 限制可以用的模块和函数")
print("- 捕获 stdout 和 stderr")
print("- 处理异常，不会让整个程序崩溃")

