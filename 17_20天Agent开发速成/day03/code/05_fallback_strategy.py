#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day03 必写代码 5：降级策略
功能：模型挂了怎么办？优雅降级、故障转移、熔断机制
"""

import time
from typing import List, Dict
from dataclasses import dataclass
from 04_unified_llm_interface import BaseLLM, OpenAILLM, DeepSeekLLM


@dataclass
class ModelConfig:
    """模型配置"""
    name: str
    priority: int  # 优先级，数字越小优先级越高
    enabled: bool = True
    failure_count: int = 0
    last_failure_time: float = 0
    circuit_breaker_timeout: int = 60  # 熔断时间（秒）


class FallbackLLM:
    """
    带降级策略的 LLM 包装器
    
    支持的降级策略：
    1. 故障转移：主模型挂了自动切备用模型
    2. 熔断机制：连续失败几次暂时禁用该模型
    3. 优先级排序：按优先级依次尝试
    """
    
    def __init__(self, models: List[tuple]):
        """
        Args:
            models: 模型列表，每个元素是 (配置字典, 优先级)
        """
        self.model_configs = []
        self.llm_instances = {}
        
        for i, (config, priority) in enumerate(models):
            model_name = config.get("model", f"model_{i}")
            self.model_configs.append(ModelConfig(
                name=model_name,
                priority=priority
            ))
            
            # 创建模型实例
            if config["llm_type"] == "openai":
                self.llm_instances[model_name] = OpenAILLM(
                    api_key=config.get("api_key"),
                    model=config.get("model", "gpt-3.5-turbo")
                )
            elif config["llm_type"] == "deepseek":
                self.llm_instances[model_name] = DeepSeekLLM(
                    api_key=config.get("api_key"),
                    model=config.get("model", "deepseek-chat")
                )
    
    def _get_available_models(self) -> List[str]:
        """获取当前可用的模型列表（按优先级排序）"""
        available = []
        now = time.time()
        
        for config in sorted(self.model_configs, key=lambda x: x.priority):
            if not config.enabled:
                continue
            
            # 检查是否在熔断中
            if config.failure_count >= 3:
                if now - config.last_failure_time < config.circuit_breaker_timeout:
                    print(f"⚠️ 模型 {config.name} 正在熔断中，跳过")
                    continue
                else:
                    # 熔断超时，重置失败计数
                    config.failure_count = 0
                    print(f"✅ 模型 {config.name} 熔断超时，恢复可用")
            
            available.append(config.name)
        
        return available
    
    def _mark_failure(self, model_name: str):
        """标记模型调用失败"""
        for config in self.model_configs:
            if config.name == model_name:
                config.failure_count += 1
                config.last_failure_time = time.time()
                print(f"❌ 模型 {model_name} 调用失败，累计失败 {config.failure_count} 次")
                break
    
    def _mark_success(self, model_name: str):
        """标记模型调用成功"""
        for config in self.model_configs:
            if config.name == model_name:
                config.failure_count = 0  # 成功则重置失败计数
                break
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        带降级策略的聊天接口
        
        依次尝试可用的模型，直到有一个成功
        """
        available_models = self._get_available_models()
        
        if not available_models:
            raise RuntimeError("没有可用的模型！")
        
        for model_name in available_models:
            try:
                print(f"🔄 尝试使用模型：{model_name}")
                result = self.llm_instances[model_name].chat(messages, **kwargs)
                self._mark_success(model_name)
                print(f"✅ 模型 {model_name} 调用成功")
                return result
            except Exception as e:
                self._mark_failure(model_name)
                print(f"❌ 模型 {model_name} 调用失败：{str(e)}")
                continue
        
        raise RuntimeError("所有模型都调用失败！")


# 使用示例
if __name__ == "__main__":
    # 配置多个模型，优先级依次降低
    models_config = [
        ({"llm_type": "openai", "api_key": "key1", "model": "gpt-4o"}, 1),  # 主模型，优先级最高
        ({"llm_type": "openai", "api_key": "key2", "model": "gpt-3.5-turbo"}, 2),  # 降级模型1
        ({"llm_type": "deepseek", "api_key": "key3", "model": "deepseek-chat"}, 3),  # 降级模型2
    ]
    
    fallback_llm = FallbackLLM(models_config)
    
    messages = [{"role": "user", "content": "什么是大模型 Agent？"}]
    
    try:
        result = fallback_llm.chat(messages)
        print("\n最终结果：")
        print(result)
    except Exception as e:
        print(f"\n所有模型都失败了：{str(e)}")
    
    print("\n✅ 降级策略总结：")
    print("  1. 故障转移：主模型挂了自动切备用")
    print("  2. 熔断机制：连续失败3次，暂停使用1分钟")
    print("  3. 自动恢复：熔断超时后自动恢复可用")
    print("  4. 优先级排序：按优先级依次尝试，保证效果最好的优先")
