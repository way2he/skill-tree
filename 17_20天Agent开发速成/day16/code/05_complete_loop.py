
"""
完整闭环示例
"""

import sys
import os

# 添加上级目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from day16.code.01_code_generator import SimpleCodeGenerator
from day16.code.02_sandbox_executor import LightweightSandbox
from day16.code.03_error_analyzer import SimpleErrorAnalyzer
from day16.code.04_auto_fixer import SimpleAutoFixer


class CodeInterpreter:
    """完整的代码解释器"""
    
    def __init__(self):
        self.code_generator = SimpleCodeGenerator()
        self.sandbox = LightweightSandbox()
        self.error_analyzer = SimpleErrorAnalyzer()
        self.auto_fixer = SimpleAutoFixer()
        
    def run(self, requirement):
        """运行完整流程"""
        print("="*60)
        print(f"🚀 代码解释器启动")
        print(f"📝 需求：{requirement}")
        print("="*60)
        print()
        
        # Step 1: 生成代码
        print("Step 1: 生成代码...")
        code = self.code_generator.generate(requirement)
        print(f"✅ 代码生成完成")
        print("-"*60)
        print(code)
        print("-"*60)
        print()
        
        # Step 2: 执行代码
        print("Step 2: 执行代码...")
        result = self.sandbox.execute_code(code)
        
        if result["success"]:
            print("✅ 执行成功！")
            print(f"📤 输出：{result['output']}")
            print()
            return {
                "success": True,
                "code": code,
                "result": result
            }
        else:
            print("❌ 执行失败")
            print(f"💥 错误：{result.get('error') or result.get('output')}")
            print()
            
            # Step 3: 自动修正
            print("Step 3: 尝试自动修正...")
            fix_result = self.auto_fixer.auto_fix(requirement, code)
            
            if fix_result["success"]:
                print()
                print("🎉 自动修正成功！")
                print("-"*60)
                print(fix_result["final_code"])
                print("-"*60)
                print(f"📤 输出：{fix_result['result']['output']}")
                return fix_result
            else:
                print()
                print("❌ 自动修正失败")
                return fix_result


# 使用示例
if __name__ == "__main__":
    interpreter = CodeInterpreter()
    
    # 测试1：hello world
    print("\n" + "="*60)
    print("测试1：Hello World")
    print("="*60)
    result1 = interpreter.run("写一个hello world程序")
    
    # 测试2：计算平均值（需要修正的版本）
    print("\n" + "="*60)
    print("测试2：计算平均值")
    print("="*60)
    initial_code = """def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    return total / count

# 测试
print(calculate_average([1, 2, 3]))
print(calculate_average([]))
"""
    result2 = interpreter.auto_fixer.auto_fix(
        "写一个计算平均值的函数，空列表返回None", 
        initial_code
    )
