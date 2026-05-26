# -*- coding: utf-8 -*-
"""
运行 LLM 包所有单元测试
"""

import sys
import io
from pathlib import Path

# 修复 Windows 控制台编码
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 添加当前目录到路径
llm_dir = Path(__file__).parent
sys.path.insert(0, str(llm_dir))


def run_tests():
    """运行所有测试"""
    try:
        import pytest
    except ImportError:
        print("[ERROR] pytest 未安装，请先运行: pip install pytest")
        return 1
    
    print("=" * 60)
    print("LLM 包单元测试套件")
    print("=" * 60)
    print()
    
    # 测试文件列表
    test_files = [
        "tests/test_factory.py",
        "tests/test_default.py",
        "tests/test_cache.py",
        "tests/test_observer.py",
        "test_model_registry.py",  # 这个在根目录
    ]
    
    # 过滤掉不存在的文件
    existing_tests = []
    for f in test_files:
        path = llm_dir / f
        if path.exists():
            existing_tests.append(str(path))
        else:
            print(f"[SKIP] {f} (不存在)")
    
    if not existing_tests:
        print("[ERROR] 没有找到测试文件")
        return 1
    
    print()
    print(f"运行 {len(existing_tests)} 个测试文件...")
    print()
    
    # 运行 pytest
    args = ["-v", "--tb=short"] + existing_tests
    result = pytest.main(args)
    
    print()
    print("=" * 60)
    if result == 0:
        print("[OK] 所有测试通过！")
    else:
        print(f"[FAIL] 测试失败 (退出码: {result})")
    print("=" * 60)
    
    return result


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
