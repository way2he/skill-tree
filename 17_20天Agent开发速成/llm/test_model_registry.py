# -*- coding: utf-8 -*-
"""
测试模型注册表

验证模型版本是否符合 MEMORY.md 规则
"""

import sys
import warnings
from pathlib import Path

# 修复 Windows 控制台编码问题
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 添加当前目录到路径
llm_dir = Path(__file__).parent
sys.path.insert(0, str(llm_dir))


def test_model_registry_import():
    """测试导入模型注册表"""
    print("=" * 60)
    print("测试 1: 导入模型注册表")
    print("=" * 60)
    
    from core import get_model_registry, validate_model, get_latest_model
    
    registry = get_model_registry()
    print(f"[OK] 注册表加载成功: {registry}")
    print()
    return registry


def test_latest_models(registry):
    """测试获取最新模型"""
    print("=" * 60)
    print("测试 2: 获取各厂商最新模型")
    print("=" * 60)
    
    test_providers = ["openai", "anthropic", "deepseek", "qwen", "kimi", "glm"]
    
    for provider in test_providers:
        latest = registry.get_latest(provider)
        if latest:
            print(f"  [OK] {provider:12s} -> {latest}")
        else:
            print(f"  [??] {provider:12s} -> (无最新模型记录)")
    print()


def test_validation(registry):
    """测试模型验证"""
    print("=" * 60)
    print("测试 3: 模型验证")
    print("=" * 60)
    
    test_cases = [
        ("openai", "gpt-5.5", True, None),
        ("openai", "gpt-5.4", True, None),
        ("openai", "gpt-4", False, "gpt-5.4"),
        ("openai", "gpt-3.5-turbo", False, "gpt-5.4"),
        ("anthropic", "claude-opus-4.7", True, None),
        ("deepseek", "deepseek-v4-pro", True, None),
        ("unknown_provider", "unknown_model", True, None),
    ]
    
    all_passed = True
    for provider, model, should_pass, expected_recommendation in test_cases:
        is_latest, recommended = registry.validate_model(provider, model, warn=False)
        
        status_ok = is_latest == should_pass
        rec_ok = recommended == expected_recommendation
        
        if not status_ok or not rec_ok:
            all_passed = False
        
        status = "[OK]" if status_ok else "[FAIL]"
        print(
            f"  {status} {provider:18s} {model:20s} "
            f"latest={is_latest} rec={recommended or '-'}"
        )
    
    print()
    return all_passed


def test_deprecation_warning():
    """测试过期警告"""
    print("=" * 60)
    print("测试 4: 过期警告")
    print("=" * 60)
    
    from core import validate_model
    
    # 捕获警告
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        validate_model("openai", "gpt-4", warn=True)
        
        if w and issubclass(w[-1].category, DeprecationWarning):
            print(f"  [OK] 收到 DeprecationWarning: {w[-1].message}")
        else:
            print(f"  [FAIL] 未收到预期警告")
    
    print()


def test_audit(registry):
    """测试时效巡检"""
    print("=" * 60)
    print("测试 5: 模型时效巡检")
    print("=" * 60)
    
    audit = registry.run_audit()
    
    if audit:
        print("  发现过期模型:")
        for provider, models in audit.items():
            print(f"    {provider:12s}: {', '.join(models)}")
    else:
        print("  [OK] 没有发现过期模型")
    
    print()


def test_convenience_functions():
    """测试便捷函数"""
    print("=" * 60)
    print("测试 6: 便捷函数")
    print("=" * 60)
    
    from core import get_latest_model, validate_model
    
    # 测试 get_latest_model
    latest = get_latest_model("openai")
    print(f"  get_latest_model('openai') -> {latest}")
    
    # 测试 validate_model
    result = validate_model("openai", "gpt-5.5")
    print(f"  validate_model('openai', 'gpt-5.5') -> {result}")
    
    print()


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("模型注册表测试套件")
    print("=" * 60)
    print()
    
    try:
        # 测试 1
        registry = test_model_registry_import()
        
        # 测试 2
        test_latest_models(registry)
        
        # 测试 3
        validation_ok = test_validation(registry)
        
        # 测试 4
        test_deprecation_warning()
        
        # 测试 5
        test_audit(registry)
        
        # 测试 6
        test_convenience_functions()
        
        # 总结
        print("=" * 60)
        if validation_ok:
            print("[OK] 所有测试通过！")
        else:
            print("[FAIL] 部分测试失败")
        print("=" * 60)
        print()
        
        # 打印使用说明
        print("使用说明:")
        print("  1. 导入: from core import get_model_registry, validate_model")
        print("  2. 验证: validate_model(provider, model)")
        print("  3. 巡检: get_model_registry().run_audit()")
        print("  4. 每 3 个月需要做一次「模型时效巡检」")
        print()
        
        return 0 if validation_ok else 1
        
    except Exception as e:
        print(f"\n[FAIL] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
