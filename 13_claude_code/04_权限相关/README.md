| 方式 | 说明 |
| --- | --- |
| 交互式授权 | 启动时的授权提示，逐个确认 |
| /permissions 命令 | 在会话中管理权限 |
| 编辑配置文件 | 手动编辑 .claude/settings.json |
| 启动参数 | --allowedTools 参数 |

## 方式一：在 Claude Code 交互界面中输入 /permissions

## 方式二：启动时通过命令行参数授权
执行位置：在终端中启动 claude 时带上参数
```bash
claude --allowedTools "git,github"

claude --allowedTools Edit,Bash(git *)
```
## 推荐允许的工具：

| 工具 | 说明 |
| --- | --- |
| Edit | 文件编辑 |
| Bash(git commit:*) | Git 提交操作 |
| Bash(git push:*) | Git 推送操作 |
| WebFetch(*) | 访问 URL 网址 |
| Bash(ls:*) | 查看文件列表 |


## 开启免授权模式
执行位置：在终端中启动 claude 时带上参数 --dangerously-skip-permissions

完整的命令为：claude --dangerously-skip-permissions