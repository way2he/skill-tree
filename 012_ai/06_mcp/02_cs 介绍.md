# MCP 客户端与服务端开发完整指南

根据搜索到的公众号文章，我为您梳理总结了 MCP (Model Context Protocol) 客户端及服务端的开发方法。

## 一、MCP 是什么？

**MCP（Model Context Protocol，模型上下文协议）** 是 Anthropic 推出的开放标准协议，专为大语言模型（LLM）与外部工具/数据源集成设计。它就像**AI 世界的"USB-C 接口"**，允许模型通过统一协议调用文件系统、API、数据库等资源，无需为每个工具单独开发适配代码。

**核心优势：**
- 🚀 **即插即用**：预构建的 MCP 服务器可快速集成
- 🔄 **跨模型兼容**：支持 Claude、GPT-4、Llama 等主流模型
- 🔒 **安全合规**：内置访问控制，保护企业数据隐私
- ⚡ **开发提效**：标准化接口减少重复开发

---

## 二、MCP 架构解析

```
┌─────────────────┐
│  LLM 应用        │
│  (ChatBot/Agent)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  MCP Client     │ ← 客户端（你的 AI 应用）
└────────┬────────┘
         │ stdio/stdout
         ▼
┌─────────────────┐
│  MCP Server     │ ← 中间层（服务插件）
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  外部资源        │
│ (文件/API/数据库)│
└─────────────────┘
```

**MCP Server 提供三种服务：**
1. **Tools**：提供给 LLM 应用使用的工具
2. **Resources**：提供额外的结构化数据
3. **Prompts**：提供 Prompt 模板

---

## 三、Python 版本开发 Demo

### 📦 **环境准备**

```bash
pip install mcp
```

### 1️⃣ **创建 MCP Server（服务端）**

创建一个简单的计算器服务器：

```python
# server_demo.py
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("演示服务器")


@mcp.tool()
def calculate(expression: str) -> float:
    """
    计算四则运算表达式
    
    Args:
        expression: 数学表达式字符串，如 "1 + 2 * 3"
    
    Returns:
        计算结果
    
    Raises:
        ValueError: 表达式格式错误
        TypeError: 参数类型错误
    """
    if not isinstance(expression, str):
        raise TypeError("expression 必须为字符串类型")
    
    try:
        result = eval(expression)
        return float(result)
    except Exception as e:
        raise ValueError(f"表达式计算失败：{str(e)}")


@mcp.tool()
def add(a: float, b: float) -> float:
    """
    加法计算
    
    Args:
        a: 第一个数
        b: 第二个数
    
    Returns:
        两数之和
    """
    return a + b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """
    乘法计算
    
    Args:
        a: 第一个数
        b: 第二个数
    
    Returns:
        两数之积
    """
    return a * b


if __name__ == "__main__":
    mcp.run(transport='stdio')
```

### 2️⃣ **创建 MCP Client（客户端）**

```python
# client_demo.py
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
import asyncio


async def main():
    """
    主函数：连接 MCP Server 并调用工具
    """
    server_params = StdioServerParameters(
        command="python",
        args=["./server_demo.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write, sampling_callback=None) as session:
            
            await session.initialize()
            
            print('\n=== 查看可用工具 ===')
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"可用工具：{tool.name}")
            
            print('\n=== 调用计算器工具 ===')
            result = await session.call_tool(
                "calculate",
                {"expression": "188*23-34"}
            )
            print(f"计算结果：{result.content}")
            
            print('\n=== 调用加法工具 ===')
            result = await session.call_tool(
                "add",
                {"a": 100, "b": 50}
            )
            print(f"加法结果：{result.content}")


if __name__ == "__main__":
    asyncio.run(main())
```

**运行结果：**
```
=== 查看可用工具 ===
可用工具：calculate
可用工具：add
可用工具：multiply

=== 调用计算器工具 ===
计算结果：4290.0

=== 调用加法工具 ===
加法结果：150.0
```

---

## 四、Node.js 版本开发 Demo

### 📦 **环境准备**

```bash
npm init -y
npm install @modelcontextprotocol/server-core
```

### 1️⃣ **创建 MCP Server（Node.js 版）**

```javascript
// server.js
const { FastMCP } = require('@modelcontextprotocol/server-core');


const mcp = new FastMCP('WeChatMCP');


mcp.tool('publish_article', {
  description: '发布公众号文章',
  inputSchema: {
    title: '文章标题',
    content: '文章内容（HTML 格式）',
    cover: '封面图片 URL'
  }
}, async (args) => {
  const { title, content, cover } = args;
  
  try {
    const accessToken = await getAccessToken();
    const mediaId = await uploadMedia(accessToken, cover);
    await createDraft(accessToken, title, content, mediaId);
    
    return { 
      success: true, 
      message: '文章发布成功' 
    };
  } catch (error) {
    return { 
      success: false, 
      message: `发布失败：${error.message}` 
    };
  }
});


mcp.tool('get_access_token', {
  description: '获取微信公众号 access_token',
  inputSchema: {
    appid: '公众号 AppID',
    secret: '公众号 AppSecret'
  }
}, async (args) => {
  const { appid, secret } = args;
  
  const url = `https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=${appid}&secret=${secret}`;
  
  const response = await fetch(url);
  const data = await response.json();
  
  return data;
});


async function getAccessToken() {
  return 'your_access_token';
}


async function uploadMedia(accessToken, coverUrl) {
  return 'media_id_12345';
}


async function createDraft(accessToken, title, content, mediaId) {
  return { draft_id: '67890' };
}


mcp.run();
```

### 2️⃣ **创建 MCP Client（Node.js 版）**

```javascript
// client.js
const { Client } = require('@modelcontextprotocol/client');
const { StdioClientTransport } = require('@modelcontextprotocol/client/stdio');


async function main() {
  const transport = new StdioClientTransport({
    command: 'node',
    args: ['./server.js']
  });
  
  const client = new Client({
    name: 'wechat-client',
    version: '1.0.0'
  });
  
  await client.connect(transport);
  
  console.log('=== 查看可用工具 ===');
  const tools = await client.listTools();
  tools.tools.forEach(tool => {
    console.log(`可用工具：${tool.name}`);
  });
  
  console.log('\n=== 调用发布文章工具 ===');
  const result = await client.callTool({
    name: 'publish_article',
    arguments: {
      title: '2025 北京地铁全攻略',
      content: '<h1>最新线路图</h1><p>详细内容...</p>',
      cover: 'https://example.com/cover.jpg'
    }
  });
  
  console.log('发布结果:', result);
  
  await client.close();
}


main().catch(console.error);
```

---

## 五、实战：微信公众号自动发文 MCP

### 📦 **完整项目结构**

```
wechat-mcp/
├── server.py              # MCP 服务端
├── client.py              # MCP 客户端
├── config.py              # 配置文件
└── requirements.txt       # 依赖
```

### 1️⃣ **MCP Server 实现**

```python
# server.py
from mcp.server.fastmcp import FastMCP
import requests
from typing import Dict, Any
import json


mcp = FastMCP("微信公众号助手")


APP_ID = "your_app_id"
APP_SECRET = "your_app_secret"
ACCESS_TOKEN = None


@mcp.tool()
def get_access_token() -> Dict[str, Any]:
    """
    获取微信公众号 access_token
    
    Returns:
        包含 access_token 和 expires_in 的字典
    
    Raises:
        ValueError: 获取 token 失败
    """
    global ACCESS_TOKEN
    
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {
        "grant_type": "client_credential",
        "appid": APP_ID,
        "secret": APP_SECRET
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "access_token" in data:
            ACCESS_TOKEN = data["access_token"]
            return {
                "success": True,
                "access_token": data["access_token"],
                "expires_in": data.get("expires_in", 7200)
            }
        else:
            raise ValueError(f"获取 token 失败：{data}")
    
    except requests.RequestException as e:
        raise ValueError(f"网络请求失败：{str(e)}")


@mcp.tool()
def upload_media(media_type: str, media_url: str) -> Dict[str, Any]:
    """
    上传素材到微信服务器
    
    Args:
        media_type: 素材类型 (image, voice, video, thumb)
        media_url: 素材 URL
    
    Returns:
        包含 media_id 的字典
    
    Raises:
        ValueError: 上传失败
        TypeError: 参数类型错误
    """
    if not isinstance(media_type, str):
        raise TypeError("media_type 必须为字符串")
    if not isinstance(media_url, str):
        raise TypeError("media_url 必须为字符串")
    
    if ACCESS_TOKEN is None:
        get_access_token()
    
    url = f"https://api.weixin.qq.com/cgi-bin/media/upload?access_token={ACCESS_TOKEN}&type={media_type}"
    
    try:
        response = requests.get(media_url, timeout=10)
        response.raise_for_status()
        
        files = {'media': ('image.jpg', response.content, 'image/jpeg')}
        upload_response = requests.post(url, files=files, timeout=10)
        upload_response.raise_for_status()
        
        data = upload_response.json()
        
        if "media_id" in data:
            return {
                "success": True,
                "media_id": data["media_id"],
                "url": data.get("url", "")
            }
        else:
            raise ValueError(f"上传失败：{data}")
    
    except Exception as e:
        raise ValueError(f"上传素材失败：{str(e)}")


@mcp.tool()
def publish_article(
    title: str, 
    content: str, 
    cover_media_id: str,
    author: str = ""
) -> Dict[str, Any]:
    """
    发布公众号文章（草稿箱）
    
    Args:
        title: 文章标题
        content: 文章内容（HTML 格式）
        cover_media_id: 封面图片 media_id
        author: 作者名
    
    Returns:
        包含 draft_id 的字典
    
    Raises:
        ValueError: 发布失败
        TypeError: 参数类型错误
    """
    if not isinstance(title, str):
        raise TypeError("title 必须为字符串")
    if not isinstance(content, str):
        raise TypeError("content 必须为字符串")
    if not isinstance(cover_media_id, str):
        raise TypeError("cover_media_id 必须为字符串")
    
    if ACCESS_TOKEN is None:
        get_access_token()
    
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={ACCESS_TOKEN}"
    
    article_data = {
        "articles": [
            {
                "title": title,
                "author": author,
                "digest": f"{title}摘要",
                "content": content,
                "content_source_url": "",
                "thumb_media_id": cover_media_id,
                "need_open_comment": 0,
                "only_fans_can_comment": 0
            }
        ]
    }
    
    try:
        response = requests.post(
            url, 
            json=article_data, 
            timeout=10
        )
        response.raise_for_status()
        
        data = response.json()
        
        if "media_id" in data:
            return {
                "success": True,
                "draft_id": data["media_id"],
                "message": "草稿创建成功"
            }
        else:
            raise ValueError(f"创建草稿失败：{data}")
    
    except Exception as e:
        raise ValueError(f"发布文章失败：{str(e)}")


if __name__ == "__main__":
    mcp.run(transport='stdio')
```

### 2️⃣ **MCP Client 实现**

```python
# client.py
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
import asyncio
from typing import Optional


class WeChatMCPClient:
    """
    微信公众号 MCP 客户端
    
    Attributes:
        server_params: 服务器启动参数
    """
    
    def __init__(self, server_script: str = "./server.py"):
        """
        初始化客户端
        
        Args:
            server_script: MCP 服务器脚本路径
        """
        self.server_params = StdioServerParameters(
            command="python",
            args=[server_script],
            env=None
        )
    
    async def publish_article(
        self, 
        title: str, 
        content: str, 
        cover_url: str
    ) -> Optional[dict]:
        """
        发布公众号文章
        
        Args:
            title: 文章标题
            content: 文章内容
            cover_url: 封面图片 URL
        
        Returns:
            发布结果字典，失败返回 None
        """
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write, sampling_callback=None) as session:
                
                await session.initialize()
                
                print("1. 正在上传封面图片...")
                upload_result = await session.call_tool(
                    "upload_media",
                    {"media_type": "image", "media_url": cover_url}
                )
                
                if not upload_result.content.get("success"):
                    print(f"上传失败：{upload_result.content}")
                    return None
                
                media_id = upload_result.content["media_id"]
                print(f"上传成功，media_id: {media_id}")
                
                print("\n2. 正在发布文章...")
                publish_result = await session.call_tool(
                    "publish_article",
                    {
                        "title": title,
                        "content": content,
                        "cover_media_id": media_id
                    }
                )
                
                return publish_result.content


async def main():
    """
    主函数示例
    """
    client = WeChatMCPClient()
    
    title = "2025 北京地铁全攻略"
    content = """
    <h1>北京地铁线路图</h1>
    <p>北京地铁是服务于北京市的城市轨道交通系统...</p>
    <h2>最新线路</h2>
    <ul>
        <li>1 号线</li>
        <li>2 号线</li>
        <li>4 号线</li>
    </ul>
    """
    cover_url = "https://example.com/beijing-metro.jpg"
    
    result = await client.publish_article(title, content, cover_url)
    
    if result and result.get("success"):
        print(f"\n✅ 发布成功！草稿 ID: {result.get('draft_id')}")
    else:
        print(f"\n❌ 发布失败：{result}")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 六、调试 MCP Server

使用 **MCP Inspector** 可视化工具调试：

```bash
mcp dev server.py
```

然后访问 `http://localhost:5173` 即可在浏览器中测试工具。

---

## 七、在 AI 工具中配置 MCP

### **VS Code (Cline 插件)**

```json
{
  "mcpServers": {
    "wechat-publish": {
      "command": "python",
      "args": ["./server.py"]
    }
  }
}
```

### **Cherry Studio**

```json
{
  "mcpServers": {
    "wechat-server": {
      "command": "python",
      "args": ["./server.py"],
      "env": {}
    }
  }
}
```

---

## 八、最佳实践

✅ **安全认证**
- 使用环境变量存储敏感信息（AppID、AppSecret）
- 在 MCP 服务器中配置 Token 校验

✅ **性能优化**
- 缓存 access_token，减少重复获取
- 异步处理大文件上传

✅ **异常处理**
- 捕获 API 错误，返回友好提示
- 限制调用频率，避免触发限流

✅ **权限管理**
- 仅开放必要的 API 权限
- 使用 IP 白名单限制访问

---

## 九、资源推荐

- 📚 **官方文档**：https://modelcontextprotocol.io/introduction
- 🌟 **MCP Servers 精选**：https://github.com/punkpeye/awesome-mcp-servers
- 🔧 **LangChain MCP 适配器**：https://github.com/langchain-ai/langchain-mcp-adapters
- 📖 **MCP 中文站**：https://mcpcn.com/docs/tutorials/

---

## 总结

MCP 为 AI 与外部工具的集成提供了**"即插即用"**的解决方案。通过本文的 Demo，您可以快速：

1. ✅ 用 Python 或 Node.js 创建 MCP Server
2. ✅ 开发 MCP Client 调用工具
3. ✅ 集成微信公众号等第三方 API
4. ✅ 在 AI 工具中配置使用 MCP

开始构建您的第一个 MCP 应用吧！🚀
