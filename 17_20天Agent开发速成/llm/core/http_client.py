# -*- coding: utf-8 -*-
"""
LLM 统一接口层 - HTTP 客户端抽象 + 连接池管理

提供统一的 HTTP 客户端接口，屏蔽 requests/httpx 的差异。
支持同步和异步调用，内置连接池复用。

使用示例:
    from llm.core.http_client import RequestsHTTPClient, HttpxHTTPClient, ConnectionPoolManager

    # 方式1: 直接使用
    http = RequestsHTTPClient()
    response = http.request("POST", url, headers=headers, json_body=payload)

    # 方式2: 通过连接池管理器（推荐）
    pool = ConnectionPoolManager()
    session = pool.get_session("openai")
    http = RequestsHTTPClient(session=session)
"""

import json
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Iterator, AsyncIterator, Optional

from .types import HTTPResponse


# =============================================================================
# HTTP 客户端抽象基类
# =============================================================================

class BaseHTTPClient(ABC):
    """
    HTTP 客户端抽象基类

    子类只需实现底层请求方法，业务逻辑在 Provider 中统一处理。
    """

    @abstractmethod
    def request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        json_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> HTTPResponse:
        """
        同步 HTTP 请求

        Args:
            method: HTTP 方法 (GET/POST/...)
            url: 请求 URL
            headers: 请求头
            json_body: JSON 请求体
            timeout: 超时时间（秒）

        Returns:
            HTTPResponse 对象
        """
        ...

    @abstractmethod
    def stream_request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        json_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> Iterator[str]:
        """
        同步流式 HTTP 请求

        Args:
            method: HTTP 方法
            url: 请求 URL
            headers: 请求头
            json_body: JSON 请求体
            timeout: 超时时间（秒）

        Yields:
            逐行返回的文本
        """
        ...

    @abstractmethod
    async def arequest(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        json_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> HTTPResponse:
        """
        异步 HTTP 请求

        Args:
            method: HTTP 方法
            url: 请求 URL
            headers: 请求头
            json_body: JSON 请求体
            timeout: 超时时间（秒）

        Returns:
            HTTPResponse 对象
        """
        ...

    @abstractmethod
    async def astream_request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        json_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> AsyncIterator[str]:
        """
        异步流式 HTTP 请求

        Args:
            method: HTTP 方法
            url: 请求 URL
            headers: 请求头
            json_body: JSON 请求体
            timeout: 超时时间（秒）

        Yields:
            逐行返回的文本
        """
        ...


# =============================================================================
# Requests HTTP 客户端（同步）
# =============================================================================

class RequestsHTTPClient(BaseHTTPClient):
    """
    基于 requests 的同步 HTTP 客户端

    Args:
        session: 可选的 requests.Session（用于连接池复用）
        pool_connections: 连接池大小（仅当 session 为 None 时生效）
        pool_maxsize: 最大连接数（仅当 session 为 None 时生效）
    """

    def __init__(
        self,
        session: Optional[Any] = None,
        pool_connections: int = 10,
        pool_maxsize: int = 10,
    ) -> None:
        # 使用 sys.modules 避免与本地 llm.requests 包冲突
        import sys
        import importlib.util

        # 清理所有可能干扰的 requests 相关模块
        _saved = {}
        for key in list(sys.modules.keys()):
            if key == "requests" or key.startswith("requests."):
                _saved[key] = sys.modules.pop(key)

        try:
            # 临时将项目根目录从 sys.path 移除，确保找到 site-packages 中的 requests
            import os
            _cwd = os.getcwd()
            _saved_path = sys.path[:]
            sys.path = [
                p for p in sys.path
                if p not in ("", ".", _cwd)
                and not p.endswith("llm")
            ]

            spec = importlib.util.find_spec("requests")
            if spec is None:
                raise ImportError("requests 库未安装")

            # 手动加载 requests 包
            requests_mod = importlib.util.module_from_spec(spec)
            sys.modules["requests"] = requests_mod
            spec.loader.exec_module(requests_mod)

            # 现在可以安全访问 adapters
            HTTPAdapter = requests_mod.adapters.HTTPAdapter
        finally:
            # 恢复 sys.path 和 sys.modules
            sys.path[:] = _saved_path
            sys.modules.update(_saved)

        if session is not None:
            self._session = session
            self._owns_session = False
        else:
            adapter = HTTPAdapter(
                pool_connections=pool_connections,
                pool_maxsize=pool_maxsize,
                max_retries=3,
            )
            self._session = requests_mod.Session()
            self._session.mount("http://", adapter)
            self._session.mount("https://", adapter)
            self._owns_session = True

    def request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        json_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> HTTPResponse:
        """同步 HTTP 请求"""
        response = self._session.request(
            method=method,
            url=url,
            headers=headers,
            json=json_body,
            timeout=timeout,
        )
        response.raise_for_status()
        return HTTPResponse(
            status_code=response.status_code,
            headers=dict(response.headers),
            content=response.content,
            text=response.text,
        )

    def stream_request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        json_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> Iterator[str]:
        """同步流式 HTTP 请求"""
        with self._session.request(
            method=method,
            url=url,
            headers=headers,
            json=json_body,
            timeout=timeout,
            stream=True,
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    yield line

    async def arequest(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        json_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> HTTPResponse:
        """异步请求（同步客户端的异步包装）"""
        import asyncio
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.request(method, url, headers, json_body, timeout),
        )
        return response

    async def astream_request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        json_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> AsyncIterator[str]:
        """异步流式请求（同步客户端的异步包装）"""
        for line in self.stream_request(method, url, headers, json_body, timeout):
            yield line

    def close(self) -> None:
        """关闭会话"""
        if self._owns_session and hasattr(self._session, "close"):
            self._session.close()


# =============================================================================
# Httpx HTTP 客户端（原生异步）
# =============================================================================

class HttpxHTTPClient(BaseHTTPClient):
    """
    基于 httpx 的异步 HTTP 客户端（同时支持同步）

    Args:
        async_client: 可选的 httpx.AsyncClient
        pool_connections: 连接池大小
        pool_maxsize: 最大连接数
    """

    def __init__(
        self,
        async_client: Optional[Any] = None,
        pool_connections: int = 10,
        pool_maxsize: int = 10,
    ) -> None:
        try:
            import httpx
        except ImportError as e:
            raise ImportError("使用 HttpxHTTPClient 需要安装 httpx: pip install httpx") from e

        if async_client is not None:
            self._async_client = async_client
            self._owns_client = False
        else:
            limits = httpx.Limits(
                max_connections=pool_connections,
                max_keepalive_connections=pool_maxsize,
            )
            self._async_client = httpx.AsyncClient(
                limits=limits,
                timeout=httpx.Timeout(60.0),
            )
            self._owns_client = True

    def request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        json_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> HTTPResponse:
        """同步请求（httpx 同步客户端）"""
        import httpx
        with httpx.Client(timeout=timeout or 60.0) as client:
            response = client.request(
                method=method,
                url=url,
                headers=headers,
                json=json_body,
            )
            response.raise_for_status()
            return HTTPResponse(
                status_code=response.status_code,
                headers=dict(response.headers),
                content=response.content,
                text=response.text,
            )

    def stream_request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        json_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> Iterator[str]:
        """同步流式请求"""
        import httpx
        with httpx.Client(timeout=timeout or 60.0) as client:
            with client.stream(
                method=method,
                url=url,
                headers=headers,
                json=json_body,
            ) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        yield line

    async def arequest(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        json_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> HTTPResponse:
        """异步 HTTP 请求"""
        response = await self._async_client.request(
            method=method,
            url=url,
            headers=headers,
            json=json_body,
            timeout=timeout,
        )
        response.raise_for_status()
        return HTTPResponse(
            status_code=response.status_code,
            headers=dict(response.headers),
            content=response.content,
            text=response.text,
        )

    async def astream_request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        json_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> AsyncIterator[str]:
        """异步流式 HTTP 请求"""
        async with self._async_client.stream(
            method=method,
            url=url,
            headers=headers,
            json=json_body,
            timeout=timeout,
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line:
                    yield line

    async def close(self) -> None:
        """关闭客户端"""
        if self._owns_client and hasattr(self._async_client, "aclose"):
            await self._async_client.aclose()


# =============================================================================
# 连接池管理器（单例）
# =============================================================================

class ConnectionPoolManager:
    """
    HTTP 连接池管理器（线程安全单例）

    管理所有 Provider 的连接池，支持复用。
    避免每次请求创建新连接。

    使用示例:
        pool = ConnectionPoolManager()
        session = pool.get_requests_session("openai")
        http = RequestsHTTPClient(session=session)
    """

    _instance: Optional["ConnectionPoolManager"] = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls) -> "ConnectionPoolManager":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._pools: Dict[str, Any] = {}
        return cls._instance

    def get_requests_session(
        self,
        provider_name: str,
        pool_connections: int = 10,
        pool_maxsize: int = 10,
    ) -> Any:
        """
        获取或创建 requests.Session

        Args:
            provider_name: Provider 名称
            pool_connections: 连接池大小
            pool_maxsize: 最大连接数

        Returns:
            requests.Session 实例
        """
        key = f"requests:{provider_name}"

        if key not in self._pools:
            with self._lock:
                if key not in self._pools:
                    import sys
                    import importlib.util
                    _saved = {}
                    for key in list(sys.modules.keys()):
                        if key == "requests" or key.startswith("requests."):
                            _saved[key] = sys.modules.pop(key)
                    try:
                        import os
                        _cwd = os.getcwd()
                        _saved_path = sys.path[:]
                        sys.path = [
                            p for p in sys.path
                            if p not in ("", ".", _cwd)
                            and not p.endswith("llm")
                        ]
                        spec = importlib.util.find_spec("requests")
                        if spec is None:
                            raise ImportError("requests 库未安装")
                        requests_mod = importlib.util.module_from_spec(spec)
                        sys.modules["requests"] = requests_mod
                        spec.loader.exec_module(requests_mod)
                        HTTPAdapter = requests_mod.adapters.HTTPAdapter
                    finally:
                        sys.path[:] = _saved_path
                        sys.modules.update(_saved)
                    adapter = HTTPAdapter(
                        pool_connections=pool_connections,
                        pool_maxsize=pool_maxsize,
                        max_retries=3,
                    )
                    session = requests_mod.Session()
                    session.mount("http://", adapter)
                    session.mount("https://", adapter)
                    self._pools[key] = session

        return self._pools[key]

    def get_httpx_client(
        self,
        provider_name: str,
        pool_connections: int = 10,
        pool_maxsize: int = 10,
    ) -> Any:
        """
        获取或创建 httpx.AsyncClient

        Args:
            provider_name: Provider 名称
            pool_connections: 连接池大小
            pool_maxsize: 最大连接数

        Returns:
            httpx.AsyncClient 实例
        """
        key = f"httpx:{provider_name}"

        if key not in self._pools:
            with self._lock:
                if key not in self._pools:
                    try:
                        import httpx
                        limits = httpx.Limits(
                            max_connections=pool_connections,
                            max_keepalive_connections=pool_maxsize,
                        )
                        client = httpx.AsyncClient(
                            limits=limits,
                            timeout=httpx.Timeout(60.0),
                        )
                        self._pools[key] = client
                    except ImportError:
                        raise ImportError("使用 httpx 需要安装: pip install httpx")

        return self._pools[key]

    def close_all(self) -> None:
        """关闭所有连接池"""
        with self._lock:
            for key, session in self._pools.items():
                try:
                    if hasattr(session, "close"):
                        session.close()
                    elif hasattr(session, "aclose"):
                        import asyncio
                        try:
                            loop = asyncio.get_event_loop()
                            if loop.is_running():
                                asyncio.ensure_future(session.aclose())
                            else:
                                loop.run_until_complete(session.aclose())
                        except RuntimeError:
                            pass
                except Exception:
                    pass
            self._pools.clear()

    def list_pools(self) -> list[str]:
        """列出所有连接池"""
        return list(self._pools.keys())
