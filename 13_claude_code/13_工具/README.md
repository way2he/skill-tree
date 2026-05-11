# Claude Code 内置工具一览表

Claude Code 提供了丰富的内置工具，涵盖文件操作、代码搜索、任务管理、网络访问等多个方面。以下是完整的工具列表：

## 文件操作工具

| 工具名称 | 功能描述 | 核心参数 | 使用场景 |
|---------|---------|---------|---------|
| **Bash** | 在持久化 shell 会话中执行命令 | `command`(必填), `timeout`(可选), `description`(可选) | 执行系统命令、运行脚本、Git 操作 |
| **Glob** | 快速匹配文件路径 | `pattern`(必填), `path`(可选) | 按文件名模式查找文件，支持通配符 |
| **Grep** | 搜索文件内容 | `pattern`(必填), `path`(可选), `include`(可选) | 正则表达式搜索代码内容 |
| **LS** | 列出目录内容 | `path`(必填), `ignore`(可选) | 查看目录结构、验证目录存在 |
| **Read** | 读取文件内容 | `file_path`(必填), `offset`(可选), `limit`(可选) | 读取源代码、配置文件等 |
| **Edit** | 精确字符串替换 | `file_path`(必填), `old_string`(必填), `new_string`(必填), `replace_all`(可选) | 单处代码修改 |
| **MultiEdit** | 同一文件多次编辑 | `file_path`(必填), `edits`(必填) | 批量代码修改、跨文件重命名 |
| **Write** | 写入文件 | `file_path`(必填), `content`(必填) | 创建新文件、覆盖已有文件 |
| **NotebookRead** | 读取 Jupyter 笔记本 | `notebook_path`(必填) | 读取 .ipynb 文件 |
| **NotebookEdit** | 编辑 Jupyter 笔记本 | `notebook_path`(必填), `cell_number`(必填), `new_source`(必填), `edit_mode`(可选) | 修改笔记本单元格 |

## 任务管理工具

| 工具名称 | 功能描述 | 核心参数 | 使用场景 |
|---------|---------|---------|---------|
| **TodoRead** | 读取当前任务列表 | 无 | 查看待办任务、检查进度 |
| **TodoWrite** | 创建管理任务列表 | `todos`(必填) | 跟踪复杂多步骤任务进度 |
| **Task** | 启动子代理 | `prompt`(必填) | 并发执行复杂搜索、多步骤任务 |

## 网络工具

| 工具名称 | 功能描述 | 核心参数 | 使用场景 |
|---------|---------|---------|---------|
| **WebFetch** | 获取网页内容 | `url`(必填), `prompt`(必填) | 抓取网页、AI 分析内容 |
| **WebSearch** | 网络搜索 | `query`(必填), `allowed_domains`(可选), `blocked_domains`(可选) | 获取最新信息、研究技术问题 |

## 命令执行管理工具

| 工具名称 | 功能描述 | 核心参数 | 使用场景 |
|---------|---------|---------|---------|
| **StopCommand** | 停止运行中的命令 | `command_id`(必填) | 终止卡住的后台进程、开发服务器 |
| **CheckCommandStatus** | 检查命令执行状态 | `command_id`(必填) | 查看后台命令输出、进度 |

## 其他工具

| 工具名称 | 功能描述 | 核心参数 | 使用场景 |
|---------|---------|---------|---------|
| **exit_plan_mode** | 退出计划模式 | `plan`(必填) | 完成计划后提示用户确认 |
| **OpenPreview** | 打开预览 URL | `command_id`(必填), `preview_url`(必填) | 启动本地服务器后预览网页 |

## 工具使用优先级建议

1. **优先使用专用工具**：如读取文件用 `Read` 而非 `cat`，搜索代码用 `Grep` 而非 `find`
2. **批量操作提升性能**：多个独立搜索可并发执行
3. **使用 Task 工具处理复杂任务**：模糊关键字搜索或多步骤任务交给子代理
4. **TodoWrite 管理进度**：复杂任务拆分为具体可执行项，实时跟踪状态

## 常用工具组合

| 场景 | 推荐工具组合 |
|-----|------------|
| 查找并修改代码 | `Grep` → `Read` → `Edit` |
| 批量重命名变量 | `MultiEdit` 跨文件操作 |
| 研究技术方案 | `WebSearch` → `WebFetch` |
| 复杂多步骤任务 | `TodoWrite` → `Task` 并发执行 |
| 运行开发服务器 | `Bash` (后台) → `OpenPreview` |

> **提示**：Claude Code 的工具设计遵循"专用工具优于通用命令"的原则，优先使用内置工具可以获得更好的性能和准确性。

## 工具调用方式

Claude Code 的工具通过 JSON-RPC 格式调用，每个工具包含 `name`（工具名）和 `input`（参数对象）。

### 基础调用格式

```json
{
  "name": "工具名称",
  "input": {
    "参数名": "参数值"
  }
}
```

### 各工具详细调用示例

#### 1. 文件操作工具

**Read** - 读取文件
```json
{
  "name": "Read",
  "input": {
    "file_path": "/absolute/path/to/file.py",
    "limit": 200,
    "offset": 1
  }
}
```

**Edit** - 单处编辑
```json
{
  "name": "Edit",
  "input": {
    "file_path": "/absolute/path/to/file.py",
    "old_string": "def old_function():",
    "new_string": "def new_function():",
    "replace_all": false
  }
}
```

**MultiEdit** - 批量编辑
```json
{
  "name": "MultiEdit",
  "input": {
    "file_path": "/absolute/path/to/file.py",
    "edits": [
      {
        "old_string": "old_text_1",
        "new_string": "new_text_1"
      },
      {
        "old_string": "old_text_2",
        "new_string": "new_text_2",
        "replace_all": true
      }
    ]
  }
}
```

**Write** - 写入文件
```json
{
  "name": "Write",
  "input": {
    "file_path": "/absolute/path/to/newfile.py",
    "content": "# 文件内容..."
  }
}
```

**Glob** - 文件匹配
```json
{
  "name": "Glob",
  "input": {
    "pattern": "**/*.ts",
    "path": "/project/src"
  }
}
```

**Grep** - 内容搜索
```json
{
  "name": "Grep",
  "input": {
    "pattern": "function\\s+\\w+",
    "path": "/project",
    "include": "*.js"
  }
}
```

**LS** - 目录列表
```json
{
  "name": "LS",
  "input": {
    "path": "/project/src",
    "ignore": ["node_modules", "*.log"]
  }
}
```

#### 2. Bash 工具

**基础命令**
```json
{
  "name": "Bash",
  "input": {
    "command": "npm install",
    "description": "安装项目依赖"
  }
}
```

**带超时的后台命令**
```json
{
  "name": "Bash",
  "input": {
    "command": "cd /project && npm run dev",
    "timeout": 300000,
    "description": "启动开发服务器",
    "blocking": false
  }
}
```

#### 3. 任务管理工具

**TodoWrite** - 创建任务列表
```json
{
  "name": "TodoWrite",
  "input": {
    "todos": [
      {
        "content": "分析需求文档",
        "status": "completed",
        "priority": "high",
        "id": "1"
      },
      {
        "content": "设计数据库结构",
        "status": "in_progress",
        "priority": "high",
        "id": "2"
      },
      {
        "content": "编写 API 接口",
        "status": "pending",
        "priority": "medium",
        "id": "3"
      }
    ]
  }
}
```

**TodoRead** - 读取任务
```json
{
  "name": "TodoRead",
  "input": {}
}
```

**Task** - 启动子代理
```json
{
  "name": "Task",
  "input": {
    "prompt": "请搜索项目中所有与支付相关的代码文件，并列出它们的路径和主要功能。"
  }
}
```

#### 4. 网络工具

**WebSearch** - 网络搜索
```json
{
  "name": "WebSearch",
  "input": {
    "query": "React 19 new features 2025",
    "allowed_domains": ["react.dev", "reactjs.org"],
    "blocked_domains": []
  }
}
```

**WebFetch** - 获取网页
```json
{
  "name": "WebFetch",
  "input": {
    "url": "https://react.dev/blog",
    "prompt": "提取文章标题、发布日期和主要内容摘要"
  }
}
```

#### 5. 命令执行管理工具

**CheckCommandStatus** - 检查后台命令
```json
{
  "name": "CheckCommandStatus",
  "input": {
    "command_id": "bash_1",
    "output_priority": "bottom"
  }
}
```

**StopCommand** - 停止命令
```json
{
  "name": "StopCommand",
  "input": {
    "command_id": "bash_1"
  }
}
```

#### 6. 其他工具

**exit_plan_mode** - 退出计划模式
```json
{
  "name": "exit_plan_mode",
  "input": {
    "plan": "## 实施计划\n\n1. 创建数据库模型\n2. 编写 API 接口\n3. 实现前端页面"
  }
}
```

**OpenPreview** - 打开预览
```json
{
  "name": "OpenPreview",
  "input": {
    "command_id": "bash_1",
    "preview_url": "http://localhost:3000"
  }
}
```

### 工具使用限制

| 限制项 | 值 | 说明 |
|-------|-----|------|
| Bash 超时 | 最大 600000ms (10分钟) | 可通过 `timeout` 参数设置 |
| 输出截断 | 30000 字符 | 超出部分会被截断 |
| Read 行数 | 默认 2000 行 | 可通过 `limit` 调整 |
| 并发调用 | 无明确限制 | 多个独立工具可并行调用 |
| WebSearch | 仅限美国使用 | 地理位置限制 |

### 最佳实践

1. **并发调用**：多个独立工具可同时调用，提升效率
   ```json
   [
     {"name": "Glob", "input": {"pattern": "**/*.js"}},
     {"name": "Grep", "input": {"pattern": "TODO", "include": "*.js"}}
   ]
   ```

2. **精确路径**：使用绝对路径，避免 `cd` 命令

3. **编辑前必读**：使用 `Edit` 前先调用 `Read` 了解文件结构

4. **任务拆分**：复杂任务用 `TodoWrite` 分解为小步骤

5. **后台进程**：长时间运行的任务使用 `blocking: false` 后台执行
