# -*- coding: utf-8 -*-
"""
检查 LLM 包导入是否正常
"""

import sys
import io

# 修复 Windows 控制台编码
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def check_imports():
    print("Testing imports...")
    
    try:
        from core import get_llm, get_async_llm
        print("  [OK] get_llm / get_async_llm")
    except Exception as e:
        print(f"  [FAIL] get_llm: {e}")
        return False
    
    try:
        from core import get_model_registry, validate_model, get_latest_model
        print("  [OK] model registry")
    except Exception as e:
        print(f"  [FAIL] model registry: {e}")
        return False
    
    try:
        from core import create_llm, list_providers, ProviderName
        print("  [OK] factory")
    except Exception as e:
        print(f"  [FAIL] factory: {e}")
        return False
    
    try:
        from core import (
            EventType, LLMEvent, EventBus,
            LoggingHandler, MetricsHandler,
            enable_logging, get_metrics_handler
        )
        print("  [OK] observer")
    except Exception as e:
        print(f"  [FAIL] observer: {e}")
        return False
    
    print()
    print("Testing model registry...")
    try:
        registry = get_model_registry()
        print(f"  [OK] Registry: {registry}")
        
        latest = registry.get_latest("openai")
        print(f"  [OK] openai latest: {latest}")
        
        is_latest, recommended = registry.validate_model("openai", "gpt-4", warn=False)
        print(f"  [OK] gpt-4 validation: is_latest={is_latest}, recommended={recommended}")
    except Exception as e:
        print(f"  [FAIL] model registry test: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    print("Testing list providers...")
    try:
        providers = list_providers()
        print(f"  [OK] {len(providers)} providers: {providers[:10]}...")
    except Exception as e:
        print(f"  [FAIL] list providers: {e}")
        return False
    
    print()
    print("=" * 60)
    print("[OK] All imports work correctly!")
    print("=" * 60)
    print()
    print("Check OPTIMIZATION_SUMMARY.md for complete documentation.")
    return True


if __name__ == "__main__":
    success = check_imports()
    sys.exit(0 if success else 1)
