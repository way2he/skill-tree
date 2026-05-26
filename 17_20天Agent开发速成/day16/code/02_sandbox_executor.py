
"""
沙箱执行器示例
"""

import subprocess
import tempfile
import os
import resource


class LightweightSandbox:
    """轻量级沙箱执行器"""
    
    def __init__(self):
        pass
        
    def execute_code(self, code, timeout=30):
        """执行代码"""
        with tempfile.TemporaryDirectory() as tmpdir:
            code_path = os.path.join(tmpdir, "main.py")
            with open(code_path, "w", encoding="utf-8") as f:
                f.write(code)
            
            # 设置资源限制（仅Linux有效）
            def set_limits():
                if os.name != "nt":  # 不是Windows
                    # CPU时间限制
                    resource.setrlimit(resource.RLIMIT_CPU, (timeout, timeout))
                    # 内存限制
                    resource.setrlimit(resource.RLIMIT_AS, (128 * 1024 * 1024, 128 * 1024 * 1024))
                    # 文件大小限制
                    resource.setrlimit(resource.RLIMIT_FSIZE, (64 * 1024 * 1024, 64 * 1024 * 1024))
                    # 进程数限制
                    resource.setrlimit(resource.RLIMIT_NPROC, (64, 64))
            
            try:
                result = subprocess.run(
                    ["python", code_path],
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    cwd=tmpdir,
                    preexec_fn=set_limits if os.name != "nt" else None
                )
                
                return {
                    "success": result.returncode == 0,
                    "exit_code": result.returncode,
                    "output": result.stdout,
                    "error": result.stderr
                }
                
            except subprocess.TimeoutExpired:
                return {
                    "success": False,
                    "error": "执行超时",
                    "exit_code": -1
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "exit_code": -1
                }


# 使用示例
if __name__ == "__main__":
    sandbox = LightweightSandbox()
    
    print("测试1：正常代码")
    result1 = sandbox.execute_code("print('Hello, World!')")
    print(f"成功：{result1['success']}")
    print(f"输出：{result1['output']}")
    print()
    
    print("测试2：有错误的代码")
    result2 = sandbox.execute_code("print(1 / 0)")
    print(f"成功：{result2['success']}")
    print(f"错误：{result2['error']}")
    print()
    
    print("测试3：超时的代码")
    result3 = sandbox.execute_code("while True: pass", timeout=1)
    print(f"成功：{result3['success']}")
    print(f"错误：{result3['error']}")
