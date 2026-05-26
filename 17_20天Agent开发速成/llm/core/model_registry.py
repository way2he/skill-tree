# -*- coding: utf-8 -*-
"""
模型版本注册表（维护最新模型名）

根据 MEMORY.md 规则：第三方厂商大模型版本必须保持最新

规则说明（来自 MEMORY.md）:
  - OpenAI: GPT-5.5（旗舰）/ GPT-5.4（性价比）- 严禁 GPT-4/GPT-4o/GPT-3.5
  - Anthropic: Claude Opus 4.7 / Claude Sonnet 4.6
  - Google: Gemini 3.1 Pro / Gemini 3 Pro
  - DeepSeek: DeepSeek V4 Pro / DeepSeek V4 Flash
  - Kimi: Kimi K2.6
  - GLM: GLM-5.1
  - Qwen: Qwen3-Max / Qwen3-Max-Thinking
  - MiniMax: MiniMax M2.5
  - 小米: MiMo V2.5 Pro
  - 文心: 文心一言 5.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import warnings


@dataclass
class ModelInfo:
    """模型信息"""
    name: str                    # 模型名（如 "gpt-5.5"）
    provider: str                # 厂商
    is_latest: bool = True       # 是否最新
    is_deprecated: bool = False  # 是否废弃
    deprecated_by: Optional[str] = None  # 由哪个替代
    price_per_1k_input: Optional[float] = None  # 输入价格（USD）
    price_per_1k_output: Optional[float] = None  # 输出价格（USD）
    last_updated: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        status = []
        if self.is_latest:
            status.append("最新")
        if self.is_deprecated:
            status.append("已废弃")
            if self.deprecated_by:
                status.append(f"建议使用: {self.deprecated_by}")
        return f"{self.name} ({', '.join(status) if status else '稳定'})"


class ModelRegistry:
    """
    模型版本注册表（单例）

    用于管理和验证各厂商的模型版本，确保使用最新模型。
    """

    _instance: Optional["ModelRegistry"] = None
    _initialized: bool = False

    def __new__(cls) -> "ModelRegistry":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._models: Dict[str, Dict[str, ModelInfo]] = {}
        self._init_models()
        self._initialized = True

    def _init_models(self) -> None:
        """
        初始化最新模型（根据 MEMORY.md 规则，2026-05-22 基准）

        注意：每 3 个月需要做一次「模型时效巡检」
        """

        # =====================================================================
        # OpenAI
        # =====================================================================
        self._models["openai"] = {
            "gpt-5.5": ModelInfo(
                name="gpt-5.5",
                provider="openai",
                is_latest=True,
                price_per_1k_input=0.015,
                price_per_1k_output=0.060,
            ),
            "gpt-5.4": ModelInfo(
                name="gpt-5.4",
                provider="openai",
                is_latest=True,
                price_per_1k_input=0.010,
                price_per_1k_output=0.030,
            ),
            "gpt-4.1": ModelInfo(
                name="gpt-4.1",
                provider="openai",
                is_latest=False,
                is_deprecated=True,
                deprecated_by="gpt-5.4",
            ),
            "gpt-4": ModelInfo(
                name="gpt-4",
                provider="openai",
                is_latest=False,
                is_deprecated=True,
                deprecated_by="gpt-5.4",
            ),
            "gpt-4o": ModelInfo(
                name="gpt-4o",
                provider="openai",
                is_latest=False,
                is_deprecated=True,
                deprecated_by="gpt-5.4",
            ),
            "gpt-3.5-turbo": ModelInfo(
                name="gpt-3.5-turbo",
                provider="openai",
                is_latest=False,
                is_deprecated=True,
                deprecated_by="gpt-5.4",
            ),
        }

        # =====================================================================
        # Anthropic
        # =====================================================================
        self._models["anthropic"] = {
            "claude-opus-4.7": ModelInfo(
                name="claude-opus-4.7",
                provider="anthropic",
                is_latest=True,
                price_per_1k_input=0.015,
                price_per_1k_output=0.075,
            ),
            "claude-sonnet-4.6": ModelInfo(
                name="claude-sonnet-4.6",
                provider="anthropic",
                is_latest=True,
                price_per_1k_input=0.003,
                price_per_1k_output=0.015,
            ),
        }

        # =====================================================================
        # Google
        # =====================================================================
        self._models["google"] = {
            "gemini-3.1-pro": ModelInfo(
                name="gemini-3.1-pro",
                provider="google",
                is_latest=True,
            ),
            "gemini-3-pro": ModelInfo(
                name="gemini-3-pro",
                provider="google",
                is_latest=True,
            ),
        }

        # =====================================================================
        # DeepSeek
        # =====================================================================
        self._models["deepseek"] = {
            "deepseek-v4-pro": ModelInfo(
                name="deepseek-v4-pro",
                provider="deepseek",
                is_latest=True,
            ),
            "deepseek-v4-flash": ModelInfo(
                name="deepseek-v4-flash",
                provider="deepseek",
                is_latest=True,
            ),
        }

        # =====================================================================
        # Kimi (月之暗面)
        # =====================================================================
        self._models["kimi"] = {
            "kimi-k2.6": ModelInfo(
                name="kimi-k2.6",
                provider="kimi",
                is_latest=True,
            ),
        }

        # =====================================================================
        # GLM (智谱)
        # =====================================================================
        self._models["glm"] = {
            "glm-5.1": ModelInfo(
                name="glm-5.1",
                provider="glm",
                is_latest=True,
            ),
        }

        # =====================================================================
        # Qwen (阿里)
        # =====================================================================
        self._models["qwen"] = {
            "qwen3-max": ModelInfo(
                name="qwen3-max",
                provider="qwen",
                is_latest=True,
            ),
            "qwen3-max-thinking": ModelInfo(
                name="qwen3-max-thinking",
                provider="qwen",
                is_latest=True,
            ),
        }

        # =====================================================================
        # MiniMax
        # =====================================================================
        self._models["minimax"] = {
            "minimax-m2.5": ModelInfo(
                name="minimax-m2.5",
                provider="minimax",
                is_latest=True,
            ),
        }

        # =====================================================================
        # 小米
        # =====================================================================
        self._models["mimo"] = {
            "mimo-v2.5-pro": ModelInfo(
                name="mimo-v2.5-pro",
                provider="mimo",
                is_latest=True,
            ),
        }

        # =====================================================================
        # 文心 (百度)
        # =====================================================================
        self._models["wenxin"] = {
            "ernie-5.0": ModelInfo(
                name="ernie-5.0",
                provider="wenxin",
                is_latest=True,
            ),
        }

        # =====================================================================
        # 其他厂商（仅保留最新模型标识）
        # =====================================================================
        self._models["doubao"] = {}
        self._models["hunyuan"] = {}
        self._models["cohere"] = {}
        self._models["mistral"] = {}
        self._models["together"] = {}
        self._models["xai"] = {}
        self._models["meta"] = {}
        self._models["shangtang"] = {}
        self._models["stepfun"] = {}
        self._models["tiangong"] = {}
        self._models["spark"] = {}
        self._models["baichuan"] = {}
        self._models["yi"] = {}
        self._models["pangu"] = {}
        self._models["milm"] = {}
        self._models["groq"] = {}

        # Ollama（本地模型，不强制版本）
        self._models["ollama"] = {}

    def get_latest(self, provider: str) -> Optional[str]:
        """
        获取指定厂商的最新模型

        Args:
            provider: 厂商名称

        Returns:
            最新模型名，如果没有则返回 None
        """
        if provider not in self._models:
            return None

        for model in self._models[provider].values():
            if model.is_latest:
                return model.name

        return None

    def get_latest_models(self, provider: str) -> List[ModelInfo]:
        """
        获取指定厂商的所有最新模型

        Args:
            provider: 厂商名称

        Returns:
            最新模型列表
        """
        if provider not in self._models:
            return []

        return [m for m in self._models[provider].values() if m.is_latest]

    def get_model_info(self, provider: str, model: str) -> Optional[ModelInfo]:
        """
        获取模型信息

        Args:
            provider: 厂商名称
            model: 模型名称

        Returns:
            模型信息，如果不存在则返回 None
        """
        if provider not in self._models:
            return None

        return self._models[provider].get(model)

    def validate_model(
        self,
        provider: str,
        model: str,
        warn: bool = True
    ) -> Tuple[bool, Optional[str]]:
        """
        验证模型是否是最新

        Args:
            provider: 厂商名称
            model: 模型名称
            warn: 是否发出警告

        Returns:
            (是否最新, 建议替代的模型)
        """
        # 未知厂商，放过
        if provider not in self._models:
            return True, None

        # 模型未知，放过
        if model not in self._models[provider]:
            return True, None

        info = self._models[provider][model]

        if info.is_deprecated:
            recommended = info.deprecated_by or self.get_latest(provider)
            if warn:
                msg = (
                    f"模型 '{model}' ({provider}) 已过期。"
                )
                if recommended:
                    msg += f" 建议使用 '{recommended}'。"
                warnings.warn(msg, DeprecationWarning, stacklevel=2)
            return False, recommended

        return True, None

    def list_providers(self) -> List[str]:
        """列出所有有模型记录的厂商"""
        return list(self._models.keys())

    def list_all_models(self, provider: str) -> List[ModelInfo]:
        """列出指定厂商的所有模型"""
        if provider not in self._models:
            return []
        return list(self._models[provider].values())

    def add_model(self, provider: str, model_info: ModelInfo) -> None:
        """
        添加或更新模型信息

        Args:
            provider: 厂商名称
            model_info: 模型信息
        """
        if provider not in self._models:
            self._models[provider] = {}
        self._models[provider][model_info.name] = model_info

    def mark_deprecated(
        self,
        provider: str,
        model: str,
        deprecated_by: Optional[str] = None
    ) -> bool:
        """
        标记模型为已废弃

        Args:
            provider: 厂商名称
            model: 模型名称
            deprecated_by: 替代模型

        Returns:
            是否成功
        """
        info = self.get_model_info(provider, model)
        if info:
            info.is_deprecated = True
            info.is_latest = False
            info.deprecated_by = deprecated_by
            return True
        return False

    def run_audit(self) -> Dict[str, List[str]]:
        """
        运行模型时效巡检

        Returns:
            巡检报告：{provider: [deprecated_models]}
        """
        report = {}
        for provider, models in self._models.items():
            deprecated = [
                m.name for m in models.values()
                if m.is_deprecated
            ]
            if deprecated:
                report[provider] = deprecated
        return report

    def __str__(self) -> str:
        total = sum(len(m) for m in self._models.values())
        latest = sum(
            1 for models in self._models.values()
            for m in models.values() if m.is_latest
        )
        deprecated = sum(
            1 for models in self._models.values()
            for m in models.values() if m.is_deprecated
        )
        return (
            f"ModelRegistry({len(self._models)} providers, "
            f"{total} models, {latest} latest, {deprecated} deprecated)"
        )


# =============================================================================
# 全局便捷函数
# =============================================================================

_model_registry_instance: Optional[ModelRegistry] = None


def get_model_registry() -> ModelRegistry:
    """获取全局模型注册表实例"""
    global _model_registry_instance
    if _model_registry_instance is None:
        _model_registry_instance = ModelRegistry()
    return _model_registry_instance


def validate_model(
    provider: str,
    model: str,
    warn: bool = True
) -> Tuple[bool, Optional[str]]:
    """
    验证模型是否是最新（便捷函数）

    Args:
        provider: 厂商名称
        model: 模型名称
        warn: 是否发出警告

    Returns:
        (是否最新, 建议替代的模型)
    """
    return get_model_registry().validate_model(provider, model, warn)


def get_latest_model(provider: str) -> Optional[str]:
    """
    获取指定厂商的最新模型（便捷函数）

    Args:
        provider: 厂商名称

    Returns:
        最新模型名
    """
    return get_model_registry().get_latest(provider)


# =============================================================================
# 执行脚本
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("模型版本注册表")
    print("=" * 60)
    print()

    registry = get_model_registry()
    print(registry)
    print()

    # 列出各厂商最新模型
    print("各厂商最新模型:")
    print("-" * 60)
    for provider in sorted(registry.list_providers()):
        latest = registry.get_latest_models(provider)
        if latest:
            model_names = ", ".join(m.name for m in latest)
            print(f"  {provider:12s} -> {model_names}")
    print()

    # 运行时效巡检
    print("模型时效巡检:")
    print("-" * 60)
    audit = registry.run_audit()
    if audit:
        for provider, models in audit.items():
            print(f"  {provider:12s} 过期: {', '.join(models)}")
    else:
        print("  ✓ 所有模型都是最新的")
    print()

    # 测试验证
    print("测试验证:")
    print("-" * 60)

    test_cases = [
        ("openai", "gpt-5.5"),
        ("openai", "gpt-4"),
        ("deepseek", "deepseek-v4-pro"),
        ("anthropic", "claude-opus-4.7"),
    ]

    for provider, model in test_cases:
        is_latest, recommended = registry.validate_model(provider, model, warn=False)
        status = "✓ 最新" if is_latest else "✗ 过期"
        rec = f" -> {recommended}" if recommended else ""
        print