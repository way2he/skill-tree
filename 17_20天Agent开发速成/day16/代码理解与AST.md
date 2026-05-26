
---
name: 代码理解与AST
description: 代码理解与AST分析技术完整详解
type: knowledge
tags: ["AST", "代码理解", "语法树"]
summary: 代码理解与AST分析技术完整详解
created_at: 2026-05-26
updated_at: 2026-05-26
version: interview
---

# 代码理解与AST 🌳

&gt; 🎯 **本章目标**：理解如何用AST分析和理解代码  
&gt; ⏰ **预计时间**：60 分钟

---

## 一、什么是AST？

### 定义

**AST** = **A**bstract **S**yntax **T**ree（抽象语法树）

它是源代码的抽象语法结构的树状表示。

### 示例

**代码：**
```python
x = 1 + 2
```

**对应的AST：**
```
        Assign
       /     \
    Name     BinOp
     |       /   \
     x     Add  Num
                 / \
                1   2
```

---

## 二、Python的ast模块

### 1. 基础用法

```python
import ast

# 解析代码
code = """
x = 1 + 2
print(x)
"""

tree = ast.parse(code)
print(ast.dump(tree, indent=2))
```

**输出：**
```
Module(
  body=[
    Assign(
      targets=[Name(id='x', ctx=Store())],
      value=BinOp(
        left=Constant(value=1),
        op=Add(),
        right=Constant(value=2)
      )
    ),
    Expr(
      value=Call(
        func=Name(id='print', ctx=Load()),
        args=[Name(id='x', ctx=Load())],
        keywords=[]
      )
    )
  ]
)
```

### 2. 访问AST节点

```python
import ast

class MyVisitor(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        print(f"函数定义：{node.name}")
        print(f"  参数：{[arg.arg for arg in node.args.args]}")
        self.generic_visit(node)
        
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            print(f"函数调用：{node.func.id}")
        self.generic_visit(node)
        
    def visit_Assign(self, node):
        print(f"赋值语句")
        self.generic_visit(node)

# 使用示例
code = """
def add(a, b):
    return a + b

x = add(1, 2)
print(x)
"""

tree = ast.parse(code)
visitor = MyVisitor()
visitor.visit(tree)
```

**输出：**
```
函数定义：add
  参数：['a', 'b']
赋值语句
函数调用：add
函数调用：print
```

---

## 三、AST应用场景

### 1. 代码检查

```python
import ast

class SecurityChecker(ast.NodeVisitor):
    def __init__(self):
        self.dangerous_calls = []
        
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name in ["eval", "exec", "compile"]:
                self.dangerous_calls.append(f"危险函数调用：{func_name}")
        self.generic_visit(node)
        
    def visit_Import(self, node):
        for name in node.names:
            if name.name in ["os", "subprocess", "sys"]:
                self.dangerous_calls.append(f"危险导入：{name.name}")
        self.generic_visit(node)

# 使用示例
code = """
import os
os.system("rm -rf /")
eval("__import__('os').system('ls')")
"""

tree = ast.parse(code)
checker = SecurityChecker()
checker.visit(tree)
print(checker.dangerous_calls)
```

### 2. 代码统计

```python
import ast

class CodeMetrics(ast.NodeVisitor):
    def __init__(self):
        self.function_count = 0
        self.class_count = 0
        self.call_count = 0
        self.assign_count = 0
        
    def visit_FunctionDef(self, node):
        self.function_count += 1
        self.generic_visit(node)
        
    def visit_ClassDef(self, node):
        self.class_count += 1
        self.generic_visit(node)
        
    def visit_Call(self, node):
        self.call_count += 1
        self.generic_visit(node)
        
    def visit_Assign(self, node):
        self.assign_count += 1
        self.generic_visit(node)

# 使用示例
code = """
class Calculator:
    def add(self, a, b):
        return a + b
        
    def multiply(self, a, b):
        return a * b

calc = Calculator()
x = calc.add(1, 2)
y = calc.multiply(x, 3)
print(y)
"""

tree = ast.parse(code)
metrics = CodeMetrics()
metrics.visit(tree)
print(f"函数数：{metrics.function_count}")
print(f"类数：{metrics.class_count}")
print(f"调用数：{metrics.call_count}")
print(f"赋值数：{metrics.assign_count}")
```

### 3. 代码转换

```python
import ast
import astor

class PrintToLogger(ast.NodeTransformer):
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            # 把 print 改为 logger.info
            return ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='logger', ctx=ast.Load()),
                    attr='info',
                    ctx=ast.Load()
                ),
                args=node.args,
                keywords=node.keywords
            )
        return node

# 使用示例
code = """
print("Hello")
print("World", 123)
"""

tree = ast.parse(code)
transformer = PrintToLogger()
new_tree = transformer.visit(tree)
new_code = astor.to_source(new_tree)
print(new_code)
```

**输出：**
```python
logger.info("Hello")
logger.info("World", 123)
```

---

## 四、实战练习

### 练习1：写一个AST检查器

**任务：**
写一个AST Visitor，检查代码中是否有：
1. 未使用的变量
2. 过长的函数（超过50行）
3. 过深的嵌套（超过4层）

---

### 练习2：写一个代码转换器

**任务：**
写一个AST Transformer，把代码中的：
1. `for i in range(len(lst)):` 改为 `for i, item in enumerate(lst):`
2. `x = x + 1` 改为 `x += 1`

---

## 五、面试要点

### 高频面试题

1. **AST有什么用？**
   - 代码检查（linting）
   - 代码转换（自动重构）
   - 代码分析（统计指标）
   - 代码生成（模版引擎）

2. **如何用Python的ast模块？**
   - ast.parse() 解析代码
   - ast.NodeVisitor 访问节点
   - ast.NodeTransformer 修改节点
   - astor 或 ast.unparse 还原代码

---

**🎉 本章完成！Day16学习完毕！**
