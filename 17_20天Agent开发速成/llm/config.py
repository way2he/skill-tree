# -*- coding: utf-8 -*-
"""
项目配置管理模块

统一管理所有环境变量和配置项，支持类型安全的访问。
"""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class LLMConfig(BaseSettings):
    """大模型API配置"""
    
    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-4o-mini"
    
    # Anthropic
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-20241022"
    
    # DeepSeek
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"
    DEEPSEEK_MODEL: str = "deepseek-chat"
    
    # 通义千问
    DASHSCOPE_API_KEY: str = ""
    QWEN_MODEL: str = "qwen-max"
    
    # 智谱
    ZHIPU_API_KEY: str = ""
    ZHIPU_MODEL: str = "glm-4"
    
    # 默认LLM厂商
    DEFAULT_LLM_PROVIDER: str = "openai"


class VectorDBConfig(BaseSettings):
    """向量数据库配置"""
    
    model_config = SettingsConfigDict(env_prefix="QDRANT_", case_sensitive=False)
    
    HOST: str = "localhost"
    PORT: int = 6333
    API_KEY: str = ""
    
    @property
    def URL(self) -> str:
        """获取完整的Qdrant URL"""
        return f"http://{self.HOST}:{self.PORT}"


class AppConfig(BaseSettings):
    """应用主配置"""
    
    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)
    
    # 应用基础配置
    APP_NAME: str = "Agent Dev Course"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # API服务器配置
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    # 子配置
    llm: LLMConfig = LLMConfig()
    qdrant: VectorDBConfig = VectorDBConfig()


@lru_cache()
def get_config() -> AppConfig:
    """获取单例配置对象"""
    return AppConfig()
