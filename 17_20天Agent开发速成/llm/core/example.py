"""
LLM 统一接口层 - 使用示例
"""

def example_basic_usage():
    """基础使用示例"""
    print("=== 基础使用示例 ===")
    
    # 导入核心模块
    from llm.core import (
        create_llm,
        list_providers,
        LLMResponse,
    )
    
    # 列出所有可用的提供者
    providers = list_providers()
    print(f"可用的 LLM 提供者: {providers}")
    
    # 示例创建（实际使用时需要提供正确的 api_key）
    print("\n提示: 使用 create_llm('provider_name', api_key='your_api_key') 创建实例")
    print("\n示例代码:")
    print("""
    # 创建 DeepSeek 实例
    llm = create_llm('deepseek', api_key='your_api_key')
    
    # 生成文本
    result = llm.generate('你好，请介绍一下自己')
    print(result)
    
    # 生成完整响应（包含元数据）
    response = llm.generate_with_response('你好')
    print(f"内容: {response.content}")
    print(f"模型: {response.model}")
    print(f"延迟: {response.latency_ms}ms")
    """)


def example_config_usage():
    """配置文件使用示例"""
    print("\n=== 配置文件使用示例 ===")
    print("\n1. 创建 llm_config.yaml 文件（已提供示例）")
    print("\n2. 设置环境变量（可选）:")
    print("   export DEEPSEEK_API_KEY='your_api_key'")
    print("   export ANTHROPIC_API_KEY='your_api_key'")
    print("\n3. 使用配置文件创建实例:")
    print("""
    from llm.core import create_llm_from_config
    
    # 使用默认提供者
    llm = create_llm_from_config('llm_config.yaml')
    
    # 使用指定提供者
    llm = create_llm_from_config('llm_config.yaml', provider_name='anthropic')
    """)


def example_resilience():
    """弹性机制使用示例"""
    print("\n=== 弹性机制使用示例 ===")
    
    from llm.core import (
        resilient,
        ResilienceConfig,
        with_retry,
        RetryPolicy,
        CircuitBreaker,
        CircuitBreakerConfig,
    )
    
    print("\n1. 使用单独的重试装饰器:")
    print("""
    @with_retry(RetryPolicy(max_retries=3))
    def my_function():
        # 可能失败的代码
        pass
    """)
    
    print("\n2. 使用完整的弹性装饰器:")
    print("""
    config = ResilienceConfig(
        retry_max_retries=3,
        circuit_breaker_enabled=True,
        circuit_breaker_failure_threshold=5,
        rate_limiter_enabled=True,
        rate_limiter_requests_per_minute=60,
    )
    
    @resilient(config)
    def my_resilient_function():
        # 具有重试、熔断、限流保护的代码
        pass
    """)
    
    print("\n3. 使用熔断器:")
    print("""
    breaker = CircuitBreaker(CircuitBreakerConfig(
        failure_threshold=5,
        recovery_timeout=30.0,
    ))
    
    @breaker
    def protected_function():
        # 受熔断器保护的代码
        pass
    """)


def example_observer():
    """观察者模式使用示例"""
    print("\n=== 观察者模式使用示例 ===")
    
    from llm.core import (
        LoggingHandler,
        MetricsHandler,
        subscribe,
        EventType,
    )
    
    print("\n1. 日志处理器:")
    print("""
    handler = LoggingHandler(log_prompt=True)
    subscribe(None, handler)  # 订阅所有事件
    """)
    
    print("\n2. 指标处理器:")
    print("""
    metrics_handler = MetricsHandler()
    subscribe(None, metrics_handler)
    
    # 使用后获取指标
    metrics = metrics_handler.get_metrics()
    print(f"请求数: {metrics['total_requests']}")
    print(f"成功率: {metrics['success_rate']}")
    print(f"平均延迟: {metrics['avg_latency_ms']}ms")
    """)


def example_async():
    """异步使用示例"""
    print("\n=== 异步使用示例 ===")
    print("""
    import asyncio
    from llm.core import create_async_llm
    
    async def main():
        llm = await create_async_llm('deepseek', api_key='your_api_key')
        result = await llm.generate('你好')
        print(result)
    
    asyncio.run(main())
    """)


def main():
    """主函数"""
    print("=" * 60)
    print("LLM 统一接口层 - 使用示例")
    print("=" * 60)
    
    example_basic_usage()
    example_config_usage()
    example_resilience()
    example_observer()
    example_async()
    
    print("\n" + "=" * 60)
    print("更多详细信息请查看:")
    print("- llm/core/README.md")
    print("- llm/core/llm_config.yaml")
    print("=" * 60)


if __name__ == "__main__":
    main()
