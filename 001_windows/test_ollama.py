#!/usr/bin/env python3
"""
测试从WSL Ubuntu访问Windows Ollama服务的Python脚本
"""

import requests
import json
import sys

def test_ollama_connection(windows_ip: str, port: int = 11434) -> bool:
    """
    测试与Windows Ollama服务的连接
    
    Args:
        windows_ip: Windows主机的IP地址
        port: Ollama服务端口，默认为11434
    
    Returns:
        bool: 连接成功返回True，否则返回False
    """
    try:
        # 构建Ollama API URL
        url = f"http://{windows_ip}:{port}/api/tags"
        
        # 发送请求测试连接
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        print(f"✅ 成功连接到Ollama服务！URL: {url}")
        print(f"📦 可用模型: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return True
    except requests.exceptions.ConnectionError:
        print(f"❌ 无法连接到Ollama服务，请检查：")
        print(f"   1. Windows中Ollama服务是否已启动")
        print(f"   2. Ollama配置是否允许远程访问")
        print(f"   3. Windows防火墙是否允许端口{port}访问")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ 请求超时，请检查网络连接")
        return False
    except Exception as e:
        print(f"❌ 连接出错: {str(e)}")
        return False

def test_ollama_chat(windows_ip: str, model: str = "llama3", port: int = 11434) -> bool:
    """
    测试与Ollama服务的聊天功能
    
    Args:
        windows_ip: Windows主机的IP地址
        model: 要使用的模型名称
        port: Ollama服务端口，默认为11434
    
    Returns:
        bool: 聊天成功返回True，否则返回False
    """
    try:
        # 构建Ollama API URL
        url = f"http://{windows_ip}:{port}/api/chat"
        
        # 准备请求数据
        data = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": "你好，Ollama！"
                }
            ],
            "stream": False
        }
        
        # 发送请求
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        
        # 解析响应
        result = response.json()
        print(f"✅ 聊天测试成功！")
        print(f"🤖 模型: {model}")
        print(f"💬 回复: {result['message']['content']}")
        return True
    except Exception as e:
        print(f"❌ 聊天测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    # 从命令行参数获取Windows IP地址，默认使用WSL中获取的地址
    windows_ip = sys.argv[1] if len(sys.argv) > 1 else "10.255.255.254"
    
    print("=" * 60)
    print("🔍 测试WSL访问Windows Ollama服务")
    print(f"📡 Windows IP: {windows_ip}")
    print("=" * 60)
    
    # 测试连接
    if test_ollama_connection(windows_ip):
        print("\n" + "=" * 60)
        print("💬 测试聊天功能")
        print("=" * 60)
        test_ollama_chat(windows_ip)
    
    print("\n" + "=" * 60)
    print("📋 操作步骤总结:")
    print("1. 在Windows中修改Ollama配置文件 %USERPROFILE%\\.ollama\\config.json")
    print("   添加: {\"host\": \"0.0.0.0:11434\"}")
    print("2. 重启Ollama服务")
    print("3. 配置Windows防火墙允许端口11434访问")
    print("4. 在Ubuntu中安装依赖: sudo apt install python3-pip && pip3 install requests")
    print("5. 运行脚本: python3 test_ollama.py [Windows_IP]")
    print("=" * 60)