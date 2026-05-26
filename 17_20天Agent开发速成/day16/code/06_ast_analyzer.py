
"""
AST分析器示例
"""

import ast


class SimpleASTAnalyzer:
    """简单的AST分析器"""
    
    def analyze_code(self, code):
        """分析代码"""
        try:
            tree = ast.parse(code)
            
            # 收集信息
            info = {
                "functions": [],
                "classes": [],
                "imports": [],
                "calls": [],
                "assignments": 0
            }
            
            # 访问AST
            visitor = InfoCollectorVisitor(info)
            visitor.visit(tree)
            
            return {
                "success": True,
                "info": info
            }
        except SyntaxError as e:
            return {
                "success": False,
                "error": f"语法错误：{e}"
            }


class InfoCollectorVisitor(ast.NodeVisitor):
    """信息收集访问器"""
    
    def __init__(self, info):
        self.info = info
        
    def visit_FunctionDef(self, node):
        self.info["functions"].append({
            "name": node.name,
            "args": [arg.arg for arg in node.args.args],
            "lineno": node.lineno
        })
        self.generic_visit(node)
        
    def visit_ClassDef(self, node):
        self.info["classes"].append({
            "name": node.name,
            "lineno": node.lineno
        })
        self.generic_visit(node)
        
    def visit_Import(self, node):
        for name in node.names:
            self.info["imports"].append({
                "name": name.name,
                "lineno": node.lineno
            })
        self.generic_visit(node)
        
    def visit_ImportFrom(self, node):
        for name in node.names:
            self.info["imports"].append({
                "from": node.module,
                "name": name.name,
                "lineno": node.lineno
            })
        self.generic_visit(node)
        
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.info["calls"].append({
                "name": node.func.id,
                "lineno": node.lineno
            })
        elif isinstance(node.func, ast.Attribute):
            self.info["calls"].append({
                "name": f"{ast.unparse(node.func.value)}.{node.func.attr}",
                "lineno": node.lineno
            })
        self.generic_visit(node)
        
    def visit_Assign(self, node):
        self.info["assignments"] += 1
        self.generic_visit(node)


# 使用示例
if __name__ == "__main__":
    analyzer = SimpleASTAnalyzer()
    
    code = """
import math
from datetime import datetime

class Calculator:
    def add(self, a, b):
        return a + b
        
    def multiply(self, a, b):
        return a * b

def main():
    calc = Calculator()
    x = calc.add(1, 2)
    y = calc.multiply(x, 3)
    print(y)
    print(datetime.now())

if __name__ == "__main__":
    main()
"""
    
    print("分析代码...")
    result = analyzer.analyze_code(code)
    
    if result["success"]:
        info = result["info"]
        print(f"\n✅ 分析成功！")
        print(f"\n📦 导入：{len(info['imports'])} 个")
        for imp in info["imports"]:
            print(f"  - {imp}")
            
        print(f"\n📚 类：{len(info['classes'])} 个")
        for cls in info["classes"]:
            print(f"  - {cls}")
            
        print(f"\n🔧 函数：{len(info['functions'])} 个")
        for func in info["functions"]:
            print(f"  - {func}")
            
        print(f"\n📞 调用：{len(info['calls'])} 个")
        for call in info["calls"]:
            print(f"  - {call}")
            
        print(f"\n📝 赋值：{info['assignments']} 次")
    else:
        print(f"❌ 分析失败：{result['error']}")
