
"""
代码生成器示例
"""

class SimpleCodeGenerator:
    """简单的代码生成器（演示用）"""
    
    def generate(self, requirement):
        """根据需求生成代码"""
        # 这里应该接入真实的LLM
        # 为了演示，我们用硬编码的代码
        
        if "average" in requirement.lower() or "平均值" in requirement:
            return self._generate_average_code()
        elif "hello" in requirement.lower():
            return self._generate_hello_code()
        else:
            return self._generate_default_code()
            
    def _generate_average_code(self):
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
        
    def _generate_hello_code(self):
        return """def hello_world():
    \"\"\"简单的hello world函数\"\"\"
    return "Hello, World!"

if __name__ == "__main__":
    print(hello_world())
"""
        
    def _generate_default_code(self):
        return """def main():
    \"\"\"主函数\"\"\"
    print("这是一个默认生成的程序")

if __name__ == "__main__":
    main()
"""

# 使用示例
if __name__ == "__main__":
    generator = SimpleCodeGenerator()
    
    print("测试1：生成平均值代码")
    code1 = generator.generate("写一个计算平均值的函数")
    print(code1)
    print("\n" + "="*50 + "\n")
    
    print("测试2：生成hello world代码")
    code2 = generator.generate("写一个hello world程序")
    print(code2)
