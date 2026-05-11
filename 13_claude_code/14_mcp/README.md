# Claude Code MCP 配置指南

## 目录

- [MCP 简介](#mcp-简介)
- [安装 MCP 服务器](#安装-mcp-服务器)
- [管理 MCP 服务器](#管理-mcp-服务器)
- [动态工具更新](#动态工具更新)
- [频道推送消息](#频道推送消息)
- [插件 MCP 服务器](#插件-mcp-服务器)
- [使用场景示例](#使用场景示例)
- [常见问题](#常见问题)

---

## MCP 简介

Claude Code 可以通过 **Model Context Protocol (MCP)** 连接到数百个外部工具和数据源。MCP 是一个用于 AI 工具集成的开源标准，MCP 服务器为 Claude Code 提供对您的工具、数据库和 API 的访问权限。

### 连接 MCP 服务器后可以做什么

- **从问题跟踪器实现功能**：添加 JIRA 问题 ENG-4521 中描述的功能，并在 GitHub 上创建 PR
- **分析监控数据**：检查 Sentry 和 Statsig 以检查功能的使用情况
- **查询数据库**：根据 PostgreSQL 数据库，查找使用特定功能的用户电子邮件
- **集成设计**：根据在 Slack 中发布的新 Figma 设计更新标准电子邮件模板
- **自动化工作流**：创建 Gmail 草稿，邀请用户参加反馈会议
- **对外部事件做出反应**：对 Telegram 消息、Discord 聊天或 webhook 事件做出反应

---

## 安装 MCP 服务器

MCP 服务器可以根据需求以三种不同的方式进行配置：

### 选项 1：添加远程 HTTP 服务器

HTTP 服务器是连接到远程 MCP 服务器的推荐选项，这是云服务最广泛支持的传输方式。

```bash
# 基本语法
claude mcp add --transport http <name> <url>

# 真实示例：连接到 Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# 带有 Bearer 令牌的示例
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

### 选项 2：添加远程 SSE 服务器

```bash
# 基本语法
claude mcp add --transport sse <name> <url>

# 真实示例：连接到 Asana
claude mcp add --transport sse asana https://mcp.asana.com/sse

# 带有身份验证标头的示例
claude mcp add --transport sse private-api https://api.company.com/sse \
  --header "X-API-Key: your-key-here"
```

### 选项 3：添加本地 stdio 服务器

Stdio 服务器作为本地进程运行，适合需要直接系统访问或自定义脚本的工具。

```bash
# 基本语法
claude mcp add [options] <name> -- <command> [args...]

# 真实示例：添加 Airtable 服务器
claude mcp add --transport stdio --env AIRTABLE_API_KEY=YOUR_KEY airtable \
  -- npx -y airtable-mcp-server
```

---

## 管理 MCP 服务器

配置后，可以使用以下命令管理 MCP 服务器：

```bash
# 列出所有配置的服务器
claude mcp list

# 获取特定服务器的详细信息
claude mcp get github

# 删除服务器
claude mcp remove github

# 在 Claude Code 中检查服务器状态
/mcp
```

---

## 动态工具更新

Claude Code 支持 MCP `list_changed` 通知，允许 MCP 服务器动态更新其可用工具、提示和资源，而无需断开连接并重新连接。

当 MCP 服务器发送 `list_changed` 通知时，Claude Code 会自动刷新来自该服务器的可用功能。

---

## 频道推送消息

MCP 服务器可以直接将消息推送到会话中，以便 Claude 可以对外部事件做出反应，例如：

- CI 结果
- 监控警报
- 聊天消息

### 启用频道功能

要启用此功能：

1. 服务器需要声明 `claude/channel` 功能
2. 启动时使用 `--channels` 标志选择加入

---

## 插件 MCP 服务器

插件可以捆绑 MCP 服务器，在启用插件时自动提供工具和集成。

### 工作原理

1. 插件在插件根目录的 `.mcp.json` 中或在 `plugin.json` 中内联定义 MCP 服务器
2. 启用插件时，其 MCP 服务器会自动启动
3. 插件 MCP 工具与手动配置的 MCP 工具一起出现
4. 插件服务器通过插件安装进行管理（不是 `/mcp` 命令）

### 配置示例

**方式一：在插件根目录的 `.mcp.json` 中**

```json
{
  "mcpServers": {
    "database-tools": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_URL": "${DB_URL}"
      }
    }
  }
}
```

**方式二：在 `plugin.json` 中内联**

```json
{
  "name": "my-plugin",
  "mcpServers": {
    "plugin-api": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-server",
      "args": ["--port", "8080"]
    }
  }
}
```

### 插件 MCP 功能

| 功能 | 说明 |
|------|------|
| 自动生命周期 | 在会话启动时，启用的插件的服务器会自动连接。如果在会话期间启用或禁用插件，请运行 `/reload-plugins` 以连接或断开其 MCP 服务器 |
| 环境变量 | 对插件相对路径使用 `${CLAUDE_PLUGIN_ROOT}`，对持久状态使用 `${CLAUDE_PLUGIN_DATA}`，该状态在插件更新后仍然存在 |
| 用户环境访问 | 访问与手动配置的服务器相同的环境变量 |
| 多种传输类型 | 支持 stdio、SSE 和 HTTP 传输（传输支持可能因服务器而异） |

### 查看插件 MCP 服务器

```bash
# 在 Claude Code 中，查看所有 MCP 服务器（包括插件提供的）
/mcp
```

---

## 使用场景示例

### 场景 1：连接数据库

```bash
# 添加 PostgreSQL MCP 服务器
claude mcp add --transport stdio --env DATABASE_URL=your_connection_string postgres \
  -- npx -y @modelcontextprotocol/server-postgres
```

### 场景 2：连接 GitHub

```bash
# 添加 GitHub MCP 服务器
claude mcp add --transport stdio --env GITHUB_TOKEN=your_token github \
  -- npx -y @modelcontextprotocol/server-github
```

### 场景 3：连接 Google Drive

```bash
# 添加 Google Drive MCP 服务器
claude mcp add --transport stdio googledrive \
  -- npx -y @modelcontextprotocol/server-gdrive
```

### 场景 4：连接 Slack

```bash
# 添加 Slack MCP 服务器
claude mcp add --transport stdio --env SLACK_BOT_TOKEN=your_token slack \
  -- npx -y @modelcontextprotocol/server-slack
```

---

## 常见问题

### Q: 如何检查 MCP 服务器是否正常运行？

在 Claude Code 会话中使用 `/mcp` 命令查看所有已配置服务器的状态。

### Q: 如何更新 MCP 服务器配置？

1. 使用 `claude mcp remove <name>` 删除现有配置
2. 使用 `claude mcp add ...` 重新添加配置

### Q: MCP 服务器连接失败怎么办？

1. 检查网络连接
2. 验证 API 密钥和令牌是否有效
3. 确认服务器 URL 是否正确
4. 查看服务器日志获取详细错误信息

### Q: 如何在项目中使用环境变量？

```bash
# 使用 --env 参数设置环境变量
claude mcp add --transport stdio --env API_KEY=xxx --env DB_URL=xxx myserver \
  -- npx -y my-mcp-server
```

### Q: 插件 MCP 服务器和手动配置的有什么区别？

| 特性 | 插件 MCP | 手动配置 |
|------|----------|----------|
| 管理方式 | 通过插件管理 | 通过 `claude mcp` 命令管理 |
| 自动启动 | 是 | 是 |
| 配置位置 | `.mcp.json` 或 `plugin.json` | Claude Code 配置文件 |
| 持久化数据 | `${CLAUDE_PLUGIN_DATA}` | 用户指定 |

---

## 参考链接

- [Claude Code MCP 官方文档](https://code.claude.com/docs/zh-CN/mcp)
- [MCP 协议规范](https://modelcontextprotocol.io/)
- [MCP 服务器列表](https://github.com/modelcontextprotocol/servers)
