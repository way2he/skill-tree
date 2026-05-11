# 发送图片处理
Claude Code 支持发送图片进行处理：直接粘贴
```
这个图片显示了什么？

这是错误的截图，是什么原因导致的？

请根据这个图片的设计稿实现网页

```

# 恢复历史会话

## 非交互模式下（还没进入 Claude Code）：
| 命令 | 说明 |
|------|------|
| `claude --continue` 或 `claude -c` | 自动继续最近的对话 |
| `claude --resume` 或 `claude -r` | 显示历史对话选择器 |

## 交互模式下（已进入 Claude Code）：
> 执行位置：在 Claude Code 交互界面中输入/resume

# 编辑记忆文件
> 执行位置：在 Claude Code 交互界面中输入 /memory
```
记忆文件位置（Windows）：

用户级：C:\Users\YourName\.claude\CLAUDE.md
项目级：C:\Projects\my-project\CLAUDE.md
```

# 设置永远用中文回复
## 在用户级记忆文件中添加：
> 每次请用中文回答我。
编辑 CLAUDE.md 文件，添加以下内容：
```markdown
# 永远用中文回复
# Always reply in Chinese.
```

# 上下文管理
/clear vs /compact 的区别：

| 命令 | 作用 | 使用场景 |
|------|------|----------|
| /clear | 完全清除对话历史 | 切换到完全不同的任务 |
| /compact | 压缩对话但保留摘要 | 继续当前任务但需要释放空间 |

有效管理成本和性能：

- 定期使用 /compact 手动压缩
- 定时使用 /clear 重置上下文
- 分解复杂任务，需求尽量具体化

# 使用参数（$ARGUMENTS）
> 文件位置：.claude/commands/fix-issue.md

```markdown
请修复 GitHub Issue #$ARGUMENTS

1. 先阅读 Issue 内容
2. 分析问题原因
3. 实现修复方案
4. 编写测试验证
```
使用方式：
```bash
> /project:fix-issue 1234                                        
                                                                 
正在修复 GitHub Issue 1234                                 
1. 读取 Issue 内容                                                
2. 分析问题原因                                                   
...
```

# 使用位置参数（1,2）：
> 文件位置：.claude/commands/create-component.md

```
请在 $1 目录下创建名为 $2 的组件
```
使用方式：
```bash
> /project:create-component src/components/MyComponent
                                                                  
正在创建组件 MyComponent
```

# 使用 Frontmatter：
> 文件位置：.claude/commands/fix-issue.md

```bash
---
description: 修复 GitHub Issue
allowed-tools:
  - Edit
  - Bash(git:*)
  - Read
argument-hint: <issue-number>
---

请修复 GitHub Issue #$1

```

# 命名空间（子目录）：

> 文件位置：.claude/commands/frontend/component.md
使用方式：/project:frontend:component