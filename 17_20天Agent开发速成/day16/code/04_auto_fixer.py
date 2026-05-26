
"""
自动修正器示例
"""

import sys
import os

# 添加上级目录到路径，方便导入
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from day16.code.01_code_generator import SimpleCodeGenerator
from day16.code.02_sandbox_executor import LightweightSandbox
from day16.code.03_error_analyzer import SimpleErrorAnalyzer


class SimpleAutoFixer:
    """简单的自动修正器"""
    
    def __init__(self, max_attempts=3):
        self.code_generator = SimpleCodeGenerator()
        self.sandbox = LightweightSandbox()
        self.error_analyzer = SimpleErrorAnalyzer()
        self.max_attempts = max_attempts
        
    def auto_fix(self, requirement, initial_code=None):
        """自动修正"""
        current_code = initial_code or self.code_generator.generate(requirement)
        attempts = 0
        history = []
        
        while attempts &lt; self.max_attempts:
            attempts += 1
            print(f"尝试 {attempts}/{self.max_attempts}...")
            
            # 执行代码
            result = self.sandbox.execute_code(current_code)
            
            # 记录历史
            history.append({
                "attempt": attempts,
                "code": current_code,
                "result": result
            })
            
            # 检查是否成功
            if result["success"]:
                print("✅ 成功！")
                return {
                    "success": True,
                    "final_code": current_code,
                    "result": result,
                    "attempts": attempts,
                    "history": history
                }
            
            # 分析错误
            error_output = result.get("error", "") or result.get("output", "")
            analysis = self.error_analyzer.analyze(current_code, error_output)
            print(f"❌ 失败：{analysis}")
            
            # 简单修复：对于演示，我们手动处理几个常见情况
            current_code = self._simple_fix(requirement, current_code, analysis, attempts)
            
        # 达到最大尝试次数
        print("❌ 达到最大尝试次数，放弃")
        return {
            "success": False,
            "final_code": current_code,
            "attempts": attempts,
            "history": history
        }
        
    def _simple_fix(self, requirement, current_code, analysis, attempt):
        """简单的修复逻辑（演示用）"""
        error_type = analysis.get("error_type", "")
        
        if error_type == "ZeroDivisionError":
            # 修复除零错误
            if "average" in requirement.lower():
                return """def calculate_average(numbers):
    \"\"\"计算列表的平均值\"\"\"
    if not numbers:
        return None
    total = sum(numbers)
    count = len(numbers)
    return total / count

# 使用示例
if __name__ == "__main__":
    print(calculate_average([1, 2, 3, 4, 5]))  # 3.0
    print(calculate_average([]))  # None
"""
        
        # 默认返回原代码
        return current_code


# 使用示例
if __name__ == "__main__":
    fixer = SimpleAutoFixer()
    
    print("测试：自动修复平均值函数（初始版本有除零错误）")
    initial_code = """def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    return total / count

# 测试
result = calculate_average([])
print(result)
"""
    
    result = fixer.auto_fix("写一个计算平均值的函数", initial_code)
    print(f"\n最终结果：{'成功' if result['success'] else '失败'}")
    if result['success']:
        print(f"\n最终代码：\n{result['final_code']}")
