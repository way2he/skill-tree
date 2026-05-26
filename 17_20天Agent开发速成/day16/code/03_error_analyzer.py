
"""
错误分析器示例
"""

import re


class SimpleErrorAnalyzer:
    """简单的错误分析器"""
    
    def analyze(self, code, error_output):
        """分析错误"""
        if not error_output:
            return {
                "error_type": "UnknownError",
                "error_message": "",
                "analysis": "没有错误信息"
            }
            
        # 解析错误类型
        error_type = self._extract_error_type(error_output)
        
        # 解析错误信息
        error_msg = self._extract_error_message(error_output)
        
        # 分析原因
        analysis = self._analyze_cause(error_type, error_msg)
        
        return {
            "error_type": error_type,
            "error_message": error_msg,
            "analysis": analysis
        }
        
    def _extract_error_type(self, error_output):
        lines = error_output.strip().split("\n")
        last_line = lines[-1] if lines else ""
        
        match = re.match(r"(\w+):", last_line)
        if match:
            return match.group(1)
        return "UnknownError"
        
    def _extract_error_message(self, error_output):
        lines = error_output.strip().split("\n")
        last_line = lines[-1] if lines else ""
        
        match = re.match(r"\w+:\s*(.+)", last_line)
        if match:
            return match.group(1)
        return last_line
        
    def _analyze_cause(self, error_type, error_msg):
        if error_type == "NameError":
            return self._analyze_name_error(error_msg)
        elif error_type == "TypeError":
            return self._analyze_type_error(error_msg)
        elif error_type == "ZeroDivisionError":
            return self._analyze_zero_division(error_msg)
        elif error_type == "IndexError":
            return self._analyze_index_error(error_msg)
        elif error_type == "KeyError":
            return self._analyze_key_error(error_msg)
        else:
            return {"cause": f"{error_type}: {error_msg}", "suggestion": "检查代码逻辑"}
            
    def _analyze_name_error(self, error_msg):
        match = re.search(r"name '(.+?)' is not defined", error_msg)
        if match:
            var_name = match.group(1)
            return {
                "cause": f"变量/函数 '{var_name}' 未定义",
                "suggestion": f"检查 '{var_name}' 的拼写和作用域"
            }
        return {"cause": "名称错误", "suggestion": "检查变量/函数名"}
        
    def _analyze_type_error(self, error_msg):
        if "unsupported operand type" in error_msg:
            return {
                "cause": "操作数类型不匹配",
                "suggestion": "检查参与运算的变量类型"
            }
        elif "division by zero" in error_msg:
            return {
                "cause": "除零错误",
                "suggestion": "检查除数是否为0"
            }
        return {"cause": "类型错误", "suggestion": "检查变量类型"}
        
    def _analyze_zero_division(self, error_msg):
        return {
            "cause": "除零错误",
            "suggestion": "检查除数是否为0，添加判断"
        }
        
    def _analyze_index_error(self, error_msg):
        return {
            "cause": "索引越界或访问空序列",
            "suggestion": "检查索引范围和列表是否为空"
        }
        
    def _analyze_key_error(self, error_msg):
        match = re.search(r"KeyError: '(.+?)'", error_msg)
        if match:
            key = match.group(1)
            return {
                "cause": f"字典中不存在键 '{key}'",
                "suggestion": f"使用 get() 方法或先检查键是否存在"
            }
        return {"cause": "键错误", "suggestion": "检查字典键是否存在"}


# 使用示例
if __name__ == "__main__":
    analyzer = SimpleErrorAnalyzer()
    
    print("测试1：NameError")
    code1 = "print(unknown_var)"
    error1 = "Traceback (most recent call last):\n  File \"test.py\", line 1, in <module>\n    print(unknown_var)\nNameError: name 'unknown_var' is not defined"
    result1 = analyzer.analyze(code1, error1)
    print(result1)
    print()
    
    print("测试2：ZeroDivisionError")
    code2 = "1 / 0"
    error2 = "Traceback (most recent call last):\n  File \"test.py\", line 1, in <module>\n    1 / 0\nZeroDivisionError: division by zero"
    result2 = analyzer.analyze(code2, error2)
    print(result2)
    print()
    
    print("测试3：KeyError")
    code3 = "{}['a']"
    error3 = "Traceback (most recent call last):\n  File \"test.py\", line 1, in <module>\n    {}['a']\nKeyError: 'a'"
    result3 = analyzer.analyze(code3, error3)
    print(result3)
