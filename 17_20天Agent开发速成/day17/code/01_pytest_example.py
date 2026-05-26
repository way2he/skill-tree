
"""
pytest示例
注意：这个文件是示例，实际运行需要先安装pytest
"""

# calculator.py
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为0")
    return a / b


# test_calculator.py
"""
import pytest
from calculator import add, subtract, multiply, divide

def test_add():
    assert add(1, 2) == 3
    assert add(0, 0) == 0
    assert add(-1, 1) == 0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 5) == -5

def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(0, 5) == 0

def test_divide():
    assert divide(6, 2) == 3
    assert divide(5, 2) == 2.5
    
    with pytest.raises(ValueError):
        divide(1, 0)
"""


# fixture示例
"""
import pytest

@pytest.fixture
def sample_list():
    return [1, 2, 3, 4, 5]

@pytest.fixture
def sample_dict():
    return {"a": 1, "b": 2, "c": 3}

def test_sum(sample_list):
    assert sum(sample_list) == 15

def test_len(sample_list, sample_dict):
    assert len(sample_list) == 5
    assert len(sample_dict) == 3
"""


# 参数化测试示例
"""
import pytest

@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (5, 5, 10),
])
def test_add_param(a, b, expected):
    assert add(a, b) == expected
"""

if __name__ == "__main__":
    print("这是pytest示例文件")
    print("请安装pytest：pip install pytest")
    print("然后运行：pytest test_calculator.py -v")
