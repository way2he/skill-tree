# Claude Code Skills 完全指南

## 一、什么是 Skills

Skills（技能）是 Claude Code 的一种扩展机制，它是一个 Markdown 文件，用于教会 Claude 如何执行特定任务。

### 核心特点：

| 特点 | 说明 |
|------|------|
| 模型自动调用 | Claude 根据你的请求自动判断是否使用某个 Skill，无需手动触发 |
| 按需加载 | 只有当任务匹配 Skill 描述时才会加载，保持上下文精简 |
| 可复用 | 一次创建，多次使用，可通过 Git 与团队共享 |
| 可扩展 | 可包含脚本、文档等辅助文件 |

### 典型使用场景：

- 使用团队标准审查 PR
- 按照特定格式生成 commit message
- 查询公司数据库 schema
- 处理特定格式的文档（如 PDF）
- 执行项目特定的部署流程

## 二、Skills 与其他功能的区别

Claude Code 提供了多种自定义方式，理解它们的区别很重要：

| 功能 | 用途 | 触发方式 |
|------|------|----------|
| Skills | 给 Claude 专业知识（如"按我们的标准审查 PR"） | Claude 自动判断何时使用 |
| 斜杠命令 | 创建可复用的提示词（如 /deploy staging） | 你手动输入 /命令 |
| CLAUDE.md | 设置项目级指令（如"使用 TypeScript 严格模式"） | 每次对话自动加载 |
| Subagents | 将任务委托给独立上下文的子代理 | Claude 委托或你显式调用 |
| Hooks | 在特定事件时运行脚本（如保存文件时 lint） | 特定工具事件触发 |
| MCP 服务器 | 连接 Claude 到外部工具和数据源 | Claude 按需调用 MCP 工具 |

### 关键区别：

- **Skills vs 斜杠命令**：Skills 是 Claude 自动触发的，斜杠命令需要你手动输入
- **Skills vs Subagents**：Skills 在当前对话中添加知识，Subagents 在独立上下文中运行
- **Skills vs MCP**：Skills 告诉 Claude 如何使用工具，MCP 提供工具

## 三、获取 Skills 的方式

在 Claude Code 中，Skills 需要手动创建。与 Claude.ai 网页版不同，Claude Code 没有预置的官方 Skills（如 Excel、PowerPoint 处理），而是提供了一个灵活的自定义 Skills 框架。

```
┌─────────────────────────────────────────────────────────────────┐
│                    Claude Code 中的 Skills                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   自定义 Skills                          │    │
│  │                                                         │    │
│  │  个人级 Skills              项目级 Skills                │    │
│  │  ~/.claude/skills/          .claude/skills/             │    │
│  │                                                         │    │
│  │  • 你自己创建               • 团队共享                   │    │
│  │  • 所有项目可用             • 通过 Git 版本控制          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              ↓                                  │
│                    需要手动创建 SKILL.md 文件                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

⚠️ 注意：Claude.ai 网页版/桌面版有预置的官方 Skills（Excel、PowerPoint、Word、PDF 处理），但 Claude Code 是一个独立的命令行工具，需要你自己创建 Skills。

### 3.1 查看当前可用的 Skills

你可以随时询问 Claude 有哪些 Skills 可用：

📍 执行位置：在 Claude Code 交互界面中

```
┌──────────────────────────────────────────────────────────────────┐
│ Claude Code                                                 - □ x │
├──────────────────────────────────────────────────────────────────┤
│ > 你有哪些可用的 Skills？                                          │
│                                                                  │
│ 当前可用的 Skills：                                                │
│                                                                  │
│ 📁 来自个人目录 (~/.claude/skills/)：                              │
│ └─ (暂无)                                                        │
│                                                                  │
│ 📁 来自项目 (.claude/skills/)：                                    │
│ └─ (暂无)                                                        │
│                                                                  │
│ 💡 提示：你可以创建自定义 Skills 来扩展我的能力。                     │
│    详见：https://docs.anthropic.com/en/docs/claude-code/skills   │
└──────────────────────────────────────────────────────────────────┘
```

### 3.2 Skills 存放位置

自定义 Skills 的存放位置决定了谁可以使用它：

| 类型 | 路径 | 作用范围 |
|------|------|----------|
| 企业级 | 由管理员配置 | 组织内所有用户 |
| 个人级 | ~/.claude/skills/ | 你的所有项目 |
| 项目级 | .claude/skills/ | 当前仓库的所有协作者 |
| 插件级 | 随插件捆绑 | 安装了该插件的用户 |

📁 Windows 实际路径：

- 个人级：C:\Users\你的用户名\.claude\skills\
- 项目级：D:\Projects\my-project\.claude\skills\

**优先级规则**：企业级 > 个人级 > 项目级 > 插件级

如果两个 Skill 同名，优先级高的会覆盖低的。

💡 下一步：第四节将详细介绍如何创建你的第一个自定义 Skill。

## 四、创建你的第一个自定义 Skill

现在让我们动手创建一个自定义 Skill，教会 Claude 用可视化图表和类比来解释代码。

### 步骤 1：创建 Skill 目录

**Windows PowerShell**：

📍 执行位置：在 PowerShell 终端中
📍 完整命令：mkdir -p $HOME\.claude\skills\code-explainer

```
┌──────────────────────────────────────────────────────────────────┐
│ PowerShell                                                  - □ x │
├──────────────────────────────────────────────────────────────────┤
│ # 创建个人级 Skill 目录                                           │
│ PS C:\> mkdir -p $HOME\.claude\skills\code-explainer             │
│                                                                  │
│     Directory: C:\Users\YourName\.claude\skills                  │
│                                                                  │
│ Mode                 LastWriteTime         Length Name           │
│ ----                 -------------         ------ ----           │
│ d-----         1/11/2026   10:30 AM                code-explainer│
└──────────────────────────────────────────────────────────────────┘
```

**Mac/Linux**：

📍 执行位置：在 Terminal 终端中
📍 完整命令：mkdir -p ~/.claude/skills/code-explainer

```
┌──────────────────────────────────────────────────────────────────┐
│ Terminal                                                    - □ x │
├──────────────────────────────────────────────────────────────────┤
│ $ mkdir -p ~/.claude/skills/code-explainer                       │
│ $ cd ~/.claude/skills/code-explainer                             │
│ $ ls -la                                                         │
│ total 0                                                          │
│ drwxr-xr-x  2 user  staff   64 Jan 11 10:30 .                    │
│ drwxr-xr-x  3 user  staff   96 Jan 11 10:30 ..                   │
└──────────────────────────────────────────────────────────────────┘
```

💡 提示：也可以创建项目级 Skill，路径为 .claude/skills/code-explainer

### 步骤 2：创建 SKILL.md 文件

📍 文件位置：~/.claude/skills/code-explainer/SKILL.md

```markdown
---
name: code-explainer
description: 使用可视化 ASCII 图表和现实类比来解释代码。当用户要求解释、说明或讲解代码概念时使用。
---

解释代码时：

1. **先用一句话总结**代码的功能

2. **绘制 ASCII 图表**展示流程或结构：
   - 用方框表示组件：`┌───┐`
   - 用箭头表示数据流：`──▶`
   - 清晰标注所有部分

3. **提供现实生活中的类比**，让概念更容易理解

4. **逐步讲解代码**，结合图表说明

## 输出格式示例

### 概述
[一句话说明代码的用途]

### 可视化图表
```
┌─────────┐     ┌─────────┐     ┌─────────┐
│  输入   │────▶│  处理   │────▶│  输出   │
└─────────┘     └─────────┘     └─────────┘
```

### 现实类比
[用日常生活中的例子来类比]

### 逐步讲解
1. 首先...
2. 然后...
3. 最后...
```

### 步骤 3：测试 Skill

📍 执行位置：在 Claude Code 交互界面中
📍 测试方式：用自然语言触发 Skill

```
┌──────────────────────────────────────────────────────────────────┐
│ Claude Code                                                 - □ x │
├──────────────────────────────────────────────────────────────────┤
│ > 解释一下这段代码是怎么工作的                                      │
│                                                                  │
│ [Claude 自动识别并使用 code-explainer Skill]                       │
│                                                                  │
│ ### 概述                                                          │
│ 这段代码实现了一个简单的用户认证流程...                              │
│                                                                  │
│ ### 可视化图表                                                     │
│ ┌─────────┐     ┌──────────┐     ┌─────────┐                     │
│ │  用户   │────▶│   验证   │────▶│  Token  │                     │
│ └─────────┘     └──────────┘     └─────────┘                     │
│                                                                  │
│ ### 现实类比                                                       │
│ 就像进入一个需要门禁卡的大楼...                                     │
│                                                                  │
│ ### 逐步讲解                                                       │
│ 1. 首先，用户提交用户名和密码...                                    │
│ 2. 然后，系统验证凭据...                                           │
│ 3. 最后，生成并返回 JWT Token...                                   │
└──────────────────────────────────────────────────────────────────┘
```

验证 Skill 是否加载成功：

📍 完整命令：直接询问 Claude

```
┌──────────────────────────────────────────────────────────────────┐
│ Claude Code                                                 - □ x │
├──────────────────────────────────────────────────────────────────┤
│ > 你有哪些可用的 Skills？                                          │
│                                                                  │
│ 当前可用的 Skills：                                                │
│ ├─ code-explainer - 用图表和类比解释代码                           │
│ └─ ...                                                           │
│                                                                  │
│ ✓ code-explainer 已成功加载！                                      │
└──────────────────────────────────────────────────────────────────┘
```

## 五、SKILL.md 文件详解

### 5.1 基本结构

SKILL.md 文件由两部分组成：

- YAML 元数据（frontmatter）：位于文件顶部，用 --- 包围
- Markdown 指令：告诉 Claude 如何使用这个 Skill

```yaml
---
name: my-skill
description: 这个 Skill 做什么，什么时候使用它
---

[Markdown 格式的详细指令]
```

### 5.2 可用的元数据字段

| 字段 | 必填 | 说明 |
|------|------|------|
| name | ✅ | Skill 名称，只能使用小写字母、数字和连字符（最多 64 字符），应与目录名匹配 |
| description | ✅ | 描述 Skill 的功能和使用场景（最多 1024 字符），Claude 用它来判断何时使用 |
| allowed-tools | ❌ | 限制 Skill 可使用的工具，支持逗号分隔或 YAML 列表 |
| model | ❌ | 指定使用的模型（如 claude-sonnet-4-20250514） |
| context | ❌ | 设为 fork 可在独立子代理上下文中运行 |
| agent | ❌ | 配合 context: fork 使用，指定代理类型（如 Explore、Plan、general-purpose） |
| hooks | ❌ | 定义 Skill 生命周期钩子，支持 PreToolUse、PostToolUse、Stop 事件 |
| user-invocable | ❌ | 控制是否在斜杠命令菜单中显示，默认 true |
| disable-model-invocation | ❌ | 设为 true 可阻止 Claude 程序化调用此 Skill |

### 5.3 description 字段的重要性

description 是 Claude 判断是否使用 Skill 的关键。一个好的描述应该回答两个问题：

- **这个 Skill 做什么？** 列出具体能力
- **什么时候应该使用它？** 包含用户可能提到的触发词

❌ 差的描述：

```yaml
description: 帮助处理文档
```

✅ 好的描述：

```yaml
description: 从 PDF 文件中提取文本、填写表单、合并文档。当用户提到 PDF、表单、文档提取时使用。
```

### 5.4 限制工具访问

使用 allowed-tools 可以限制 Skill 激活时 Claude 能使用的工具：

```yaml
---
name: safe-reader
description: 安全地读取和分析代码，不做任何修改
allowed-tools:
  - Read
  - Grep
  - Glob
---
```

或者使用逗号分隔：

```yaml
allowed-tools: Read, Grep, Glob
```

这对以下场景很有用：

- 创建只读分析 Skill
- 限制对敏感操作的访问
- 确保 Skill 只使用特定工具

如果省略 allowed-tools，Skill 不会限制工具使用，Claude 会使用标准的权限模型。

## 六、进阶用法

### 6.1 多文件 Skill 结构

对于复杂的 Skill，可以使用渐进式披露：将核心信息放在 SKILL.md 中，详细参考资料放在单独文件中。

**目录结构示例**：

```
.claude/skills/pdf-processor/
├── SKILL.md              # 主文件（必需）
├── docs/
│   ├── api-reference.md  # API 参考文档
│   └── examples.md       # 使用示例
└── scripts/
    ├── extract.py        # 提取脚本
    └── merge.py          # 合并脚本
```

**SKILL.md 内容**：

```markdown
---
name: pdf-processor
description: 处理 PDF 文件：提取文本、填写表单、合并文档。当用户需要处理 PDF 时使用。
allowed-tools:
  - Read
  - Bash
  - Write
---

## 核心功能

1. **提取文本**：运行 `scripts/extract.py`
2. **合并文档**：运行 `scripts/merge.py`

## 详细文档

- API 参考：见 `docs/api-reference.md`
- 使用示例：见 `docs/examples.md`

## 使用脚本

直接运行脚本，无需读取其内容：

```bash
python scripts/extract.py input.pdf
```
```

💡 技巧：脚本可以直接执行而不加载到上下文中，只有输出会消耗 token。

### 6.2 在独立上下文中运行 Skill

使用 context: fork 可以让 Skill 在独立的子代理上下文中运行，适合执行复杂的多步骤操作：

```yaml
---
name: deep-analysis
description: 对代码库进行深度分析，生成详细报告
context: fork
agent: Explore
---

执行全面的代码分析：
1. 扫描所有源文件
2. 识别代码模式
3. 生成分析报告
```

**agent 字段**可以指定代理类型：

- Explore - 探索型代理
- Plan - 规划型代理
- general-purpose - 通用代理（默认）
- 或自定义代理名称（来自 .claude/agents/）

### 6.3 定义 Skill 钩子

Skills 可以定义在其生命周期内运行的钩子，支持 PreToolUse、PostToolUse 和 Stop 事件：

```yaml
---
name: auto-format
description: 自动格式化代码
hooks:
  PostToolUse:
    - matcher: Write
      command: "prettier --write $FILE"
      once: true
---
```

`once: true` 表示钩子只在会话中运行一次，首次成功执行后会被移除。

Skill 中定义的钩子仅在该 Skill 执行期间有效，Skill 完成后会自动清理。

### 6.4 控制 Skill 可见性

Skills 可以通过三种方式被调用：

1. **手动调用**：用户输入 /skill-name
2. **程序化调用**：Claude 通过 Skill 工具调用
3. **自动发现**：Claude 读取描述后在相关时自动加载

| 设置 | 斜杠菜单 | Skill 工具 | 自动发现 | 使用场景 |
|------|----------|-----------|----------|----------|
| user-invocable: true（默认） | 可见 | 允许 | 是 | 希望用户直接调用的 Skill |
| user-invocable: false | 隐藏 | 允许 | 是 | Claude 可用但用户不应手动调用的 Skill |
| disable-model-invocation: true | 可见 | 阻止 | 是 | 只允许用户调用，不允许 Claude 程序化调用 |

**示例**：仅供 Claude 使用的 Skill

```yaml
---
name: internal-helper
description: 内部辅助功能，用于代码分析
user-invocable: false
---
```

设置 user-invocable: false 后，用户在 / 菜单中看不到这个 Skill，但 Claude 仍可以通过 Skill 工具调用它或根据上下文自动发现它。

## 七、实战案例

### 案例 1：Git Commit 消息生成器

📍 文件位置：.claude/skills/commit-helper/SKILL.md

```markdown
---
name: commit-helper
description: 生成规范的 Git commit 消息。当用户要求提交代码、生成 commit message 时使用。
---

## Commit 消息格式

使用 Conventional Commits 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Type 类型

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关

## 步骤

1. 运行 `git diff --staged` 查看暂存的更改
2. 分析更改内容，确定 type 和 scope
3. 生成简洁的 subject（不超过 50 字符）
4. 如有必要，添加详细的 body 说明

## 示例

```
feat(auth): 添加用户登录功能

- 实现用户名密码验证
- 添加 JWT token 生成
- 集成 Redis 存储 session

Closes #123
```
```

**使用效果**：

```
┌──────────────────────────────────────────────────────────────────┐
│ Claude Code                                                 - □ x │
├──────────────────────────────────────────────────────────────────┤
│ > 帮我生成一个 commit message                                     │
│                                                                  │
│ 让我先查看暂存的更改...                                            │
│                                                                  │
│ Running: git diff --staged                                       │
│                                                                  │
│ 根据更改内容，建议的 commit message：                               │
│                                                                  │
│ feat(user): 添加用户注册接口                                       │
│                                                                  │
│ - 实现邮箱验证逻辑                                                 │
│ - 添加密码强度检查                                                 │
│ - 创建用户数据模型                                                 │
└──────────────────────────────────────────────────────────────────┘
```

### 案例 2：PR 代码审查

📍 文件位置：.claude/skills/pr-reviewer/SKILL.md

```markdown
---
name: pr-reviewer
description: 按照团队标准审查 Pull Request。当用户要求审查 PR、review 代码、检查更改时使用。
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

## 审查清单

### 1. 代码质量
- [ ] 代码是否遵循项目编码规范
- [ ] 是否有重复代码可以抽取
- [ ] 函数/方法是否过长（超过 50 行）
- [ ] 命名是否清晰有意义

### 2. 安全性
- [ ] 是否有 SQL 注入风险
- [ ] 是否有 XSS 风险
- [ ] 敏感信息是否正确处理
- [ ] 权限检查是否完整

### 3. 性能
- [ ] 是否有 N+1 查询问题
- [ ] 是否有不必要的循环
- [ ] 大数据量处理是否有分页

### 4. 测试
- [ ] 是否有对应的单元测试
- [ ] 边界情况是否覆盖
- [ ] 测试是否有意义（不是为了覆盖率而写）

## 输出格式

```markdown
## PR 审查报告

### 总体评价
[优秀/良好/需要改进]

### 发现的问题
1. **[严重程度]** 问题描述
   - 位置：`文件:行号`
   - 建议：如何修复

### 优点
- 列出代码中的亮点

### 建议
- 可选的改进建议
```
```

**使用效果**：

```
┌──────────────────────────────────────────────────────────────────┐
│ Claude Code                                                 - □ x │
├──────────────────────────────────────────────────────────────────┤
│ > 帮我审查一下这个 PR                                              │
│                                                                  │
│ 让我查看 PR 的更改内容...                                          │
│                                                                  │
│ Running: git diff main...feature/user-auth                       │
│                                                                  │
│ ## PR 审查报告                                                    │
│                                                                  │
│ ### 总体评价                                                      │
│ 良好 - 代码质量不错，有几个小问题需要修复                            │
│                                                                  │
│ ### 发现的问题                                                    │
│ 1. **[中等]** 缺少输入验证                                         │
│    - 位置：`src/auth/login.ts:45`                                 │
│    - 建议：添加邮箱格式验证                                         │
│                                                                  │
│ 2. **[低]** 魔法数字                                               │
│    - 位置：`src/auth/token.ts:12`                                 │
│    - 建议：将 3600 提取为常量 TOKEN_EXPIRY                          │
│                                                                  │
│ ### 优点                                                          │
│ - 良好的错误处理                                                   │
│ - 清晰的函数命名                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### 案例 3：数据库查询助手

📍 文件位置：.claude/skills/db-helper/SKILL.md

```markdown
---
name: db-helper
description: 帮助编写和优化数据库查询。当用户提到 SQL、数据库、查询、表结构时使用。
---

## 项目数据库信息

数据库类型：MySQL 8.0

### 核心表结构

#### users 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT | 主键 |
| username | VARCHAR(50) | 用户名，唯一 |
| email | VARCHAR(100) | 邮箱，唯一 |
| created_at | DATETIME | 创建时间 |

#### orders 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT | 主键 |
| user_id | BIGINT | 外键 -> users.id |
| total_amount | DECIMAL(10,2) | 订单金额 |
| status | ENUM | pending/paid/shipped/completed |
| created_at | DATETIME | 创建时间 |

### 查询规范

1. **必须使用参数化查询**，防止 SQL 注入
2. **大表查询必须有索引**
3. **避免 SELECT ***，明确指定需要的字段
4. **分页查询使用 LIMIT + OFFSET**

### 常用查询模板

```sql
-- 用户订单统计
SELECT 
    u.username,
    COUNT(o.id) as order_count,
    SUM(o.total_amount) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.created_at >= ?
GROUP BY u.id
ORDER BY total_spent DESC
LIMIT ? OFFSET ?;
```
```

**使用效果**：

```
┌──────────────────────────────────────────────────────────────────┐
│ Claude Code                                                 - □ x │
├──────────────────────────────────────────────────────────────────┤
│ > 帮我写一个查询，统计每个用户最近30天的订单数量                       │
│                                                                  │
│ 根据项目数据库结构，这是查询语句：                                   │
│                                                                  │
│ ```sql                                                           │
│ SELECT                                                           │
│     u.id,                                                        │
│     u.username,                                                  │
│     u.email,                                                     │
│     COUNT(o.id) as order_count,                                  │
│     COALESCE(SUM(o.total_amount), 0) as total_spent              │
│ FROM users u                                                     │
│ LEFT JOIN orders o ON u.id = o.user_id                           │
│     AND o.created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)         │
│ GROUP BY u.id, u.username, u.email                               │
│ ORDER BY order_count DESC;                                       │
│ ```                                                       │
│                                                                  │
│ 💡 注意事项：                                                      │
│ - 使用 LEFT JOIN 确保没有订单的用户也会显示                          │
│ - COALESCE 处理 NULL 值                                           │
│ - orders 表的 user_id 字段有索引，查询性能良好                       │
└──────────────────────────────────────────────────────────────────┘
```

### 案例 4：项目部署助手

📍 文件位置：.claude/skills/deploy-helper/SKILL.md

```markdown
---
name: deploy-helper
description: 协助项目部署流程。当用户提到部署、发布、上线、deploy 时使用。
allowed-tools:
  - Read
  - Bash
---

## 部署环境

| 环境 | 地址 | 分支 |
|------|------|------|
| 开发 | dev.example.com | develop |
| 测试 | staging.example.com | staging |
| 生产 | www.example.com | main |

## 部署前检查清单

1. **代码检查**
   ```bash
   npm run lint
   npm run test
   ```

2. **构建测试**
   ```bash
   npm run build
   ```

3. **版本确认**
   - 检查 package.json 版本号
   - 确认 CHANGELOG 已更新

## 部署命令

### 部署到测试环境
```bash
git checkout staging
git merge develop
git push origin staging
# CI/CD 会自动部署
```

### 部署到生产环境
```bash
git checkout main
git merge staging
git tag v$(node -p "require('./package.json').version")
git push origin main --tags
```

## 回滚流程

如需回滚，执行：
```bash
git revert HEAD
git push origin main
```
```

**使用效果**：

```
┌──────────────────────────────────────────────────────────────────┐
│ Claude Code                                                 - □ x │
├──────────────────────────────────────────────────────────────────┤
│ > 帮我部署到测试环境                                               │
│                                                                  │
│ 好的，我来帮你部署到测试环境。先进行部署前检查...                      │
│                                                                  │
│ Running: npm run lint                                            │
│ ✓ Lint 检查通过                                                   │
│                                                                  │
│ Running: npm run test                                            │
│ ✓ 所有测试通过 (42 passed)                                        │
│                                                                  │
│ Running: npm run build                                           │
│ ✓ 构建成功                                                        │
│                                                                  │
│ 检查完成，准备部署：                                                │
│                                                                  │
│ Running: git checkout staging                                    │
│ Running: git merge develop                                       │
│ Running: git push origin staging                                 │
│                                                                  │
│ ✓ 已推送到 staging 分支                                           │
│ ✓ CI/CD 流水线已触发                                              │
│                                                                  │
│ 📍 部署状态：https://ci.example.com/pipelines/1234                │
│ 📍 测试环境：https://staging.example.com                          │
└──────────────────────────────────────────────────────────────────┘
```

## 八、常见问题排查

### 8.1 Skill 没有触发

**问题**：你创建了 Skill，但 Claude 没有使用它。

**解决方案**：检查 description 字段。模糊的描述如"帮助处理文档"无法让 Claude 准确匹配。

**改进方法**：

```yaml
# ❌ 差
description: 帮助处理文档

# ✅ 好
description: 从 PDF 文件中提取文本、填写表单、合并文档。当用户提到 PDF、表单、文档提取时使用。
```

### 8.2 Skill 没有加载

**检查文件路径**：

Skills 必须放在正确的目录，文件名必须是 SKILL.md（区分大小写）：

| 类型 | 正确路径 |
|------|----------|
| 个人级 | ~/.claude/skills/my-skill/SKILL.md |
| 项目级 | .claude/skills/my-skill/SKILL.md |

**检查 YAML 语法**：

- frontmatter 必须从第 1 行开始（前面不能有空行）
- 必须用 --- 开始和结束
- 使用空格缩进（不是 Tab）

**使用调试模式**：

```bash
claude --debug
```

调试模式可以显示 Skill 加载错误信息。

### 8.3 Skill 有错误

**检查依赖**：如果 Skill 使用外部包，确保已安装。

**检查脚本权限**：

```bash
# Mac/Linux
chmod +x scripts/*.py

# Windows PowerShell
# 脚本通常不需要特殊权限
```

**检查文件路径**：使用正斜杠 /，不要用反斜杠 \。

```yaml
# ❌ 错误
scripts\helper.py

# ✅ 正确
scripts/helper.py
```

### 8.4 多个 Skill 冲突

**问题**：如果 Claude 使用了错误的 Skill，说明描述太相似了。

**解决方案**：让每个描述更具体，使用不同的触发词。

```yaml
# ❌ 两个 Skill 都有 "数据分析"
description: 数据分析工具

# ✅ 区分开来
# Skill 1
description: 分析 Excel 文件和 CRM 导出的销售数据

# Skill 2  
description: 分析日志文件和系统指标
```

## 九、学习资源与参考

### 9.1 官方文档

| 资源 | 说明 |
|------|------|
| Claude Code Skills 官方文档 | 最权威的 Skill 创建指南，包含完整的语法和配置说明 |
| Anthropic Courses | Anthropic 官方教程，学习 Claude API 和提示工程基础 |

### 9.2 社区 Skill 资源

社区资源分为两类：包含实际 SKILL.md 文件的仓库 和 链接合集（awesome-list）。

#### 一、包含实际 SKILL.md 文件的仓库（可直接使用）

这些仓库包含真实的 Skill 文件，可以直接克隆或复制到 ~/.claude/skills/ 使用：

| 仓库 | 说明 | Skills 数量 |
|------|------|------------|
| obra/superpowers | 完整的软件开发工作流，专为 Claude Code 设计 | 7+ |
| K-Dense-AI/claude-scientific-skills | 科学研究 Skills（生物、化学、医学等） | 139 |

**Superpowers 包含的 Skills**：

| Skill 名称 | 功能 |
|-----------|------|
| brainstorming | 头脑风暴，在写代码前梳理需求和设计 |
| writing-plans | 将工作拆分为 2-5 分钟的小任务 |
| test-driven-development | TDD 测试驱动开发（红-绿-重构） |
| subagent-driven-development | 子代理驱动开发 |
| requesting-code-review | 代码审查 |
| using-git-worktrees | Git worktree 隔离工作流 |

**安装方式**：

```bash
# 克隆仓库
git clone https://github.com/obra/superpowers.git

# 复制 skills 目录到 Claude Code
cp -r superpowers/skills/* ~/.claude/skills/
```

#### 二、链接合集（需要访问具体仓库获取文件）

这些仓库本身只包含 README.md，是外部链接的合集。你需要点击链接访问各个独立仓库下载 SKILL.md 文件：

| 仓库 | 说明 |
|------|------|
| ComposioHQ/awesome-claude-skills | 分类清晰，明确说明支持 Claude Code |
| BehiSecc/awesome-claude-skills | 开发工具类链接合集 |
| VoltAgent/awesome-claude-skills | 上下文工程类链接合集 |

⚠️ 注意：travisvn/awesome-claude-skills 主要收录 Claude.ai 官方 Skills（docx、pdf 等），这些依赖 Anthropic 后端服务，无法直接用于 Claude Code。

### 9.3 学习路径

```
┌─────────────────────────────────────────────────────────────────┐
│                    Skill 学习路径                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1️⃣ 入门阶段                                                    │
│  ├─ 阅读官方文档了解 SKILL.md 语法                               │
│  ├─ 创建你的第一个简单 Skill（如本文的 code-explainer）           │
│  └─ 浏览 awesome-claude-code 了解社区有哪些 Skills               │
│                                                                 │
│  2️⃣ 进阶阶段                                                    │
│  ├─ 学习多文件 Skill 结构（渐进式披露）                           │
│  ├─ 使用 allowed-tools 限制工具访问                              │
│  └─ 参考 Context Engineering Kit 学习上下文优化技巧              │
│                                                                 │
│  3️⃣ 高级阶段                                                    │
│  ├─ 使用 context: fork 在独立上下文中运行                        │
│  ├─ 定义 Skill 钩子（hooks）                                     │
│  └─ 为团队创建项目级 Skill 并通过 Git 共享                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 十、最佳实践总结

| 实践 | 说明 |
|------|------|
| 参考社区 Skills | 先看看 GitHub 上是否有现成的，避免重复造轮子 |
| 描述要具体 | 包含具体功能和触发词 |
| 保持精简 | 核心信息放 SKILL.md，详细内容放单独文件 |
| 使用脚本 | 复杂逻辑用脚本实现，减少上下文消耗 |
| 限制工具 | 只读 Skill 使用 allowed-tools 限制权限 |
| 版本控制 | 项目级 Skill 提交到 Git，方便团队共享 |
| 测试验证 | 创建后询问 Claude "你有哪些 Skills？" 确认加载 |
| 定期维护 | 随着项目演进，及时更新 Skill 内容 |

---

版权声明：本文为CSDN博主「Slow菜鸟」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/qq_20236937/article/details/156824407