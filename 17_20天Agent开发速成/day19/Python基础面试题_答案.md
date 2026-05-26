
# Day19 Python 基础面试题答案 ✅

---

## 基础题答案

### 1. list vs tuple

| 特性 | list | tuple |
|------|------|-------|
| 可变性 | 可变 | 不可变 |
| 语法 | `[1, 2]` | `(1, 2)` |
| 方法 | append、pop 等 | 少（count、index） |
| 性能 | 稍慢 | 稍快 |
| 用途 | 存储可变序列 | 固定数据、字典 key |

---

### 2. *args 和 **kwargs

```python
# *args: 可变位置参数，接收 tuple
def func1(*args):
    print(args)  # (1, 2, 3)

func1(1, 2, 3)

# **kwargs: 可变关键字参数，接收 dict
def func2(**kwargs):
    print(kwargs)  # {'a': 1, 'b': 2}

func2(a=1, b=2)

# 同时使用
def func3(*args, **kwargs):
    pass
```

---

### 3. 装饰器

```python
# 简单装饰器
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("函数执行前")
        result = func(*args, **kwargs)
        print("函数执行后")
        return result
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
```

---

### 4. 生成器

```python
# 生成器函数
def count(n):
    for i in range(n):
        yield i

# 生成器表达式
gen = (i for i in range(10))

# 特点：惰性计算，节省内存
```

**对比：**

| 特性 | 列表 | 生成器 |
|------|------|--------|
| 内存 | 一次性占用 | 惰性计算 |
| 速度 | 快 | 稍慢 |
| 重用 | 可多次遍历 | 只能一次 |

---

### 5-15（略）

---

## 💡 小结

Python 基础是面试必考内容！

---
