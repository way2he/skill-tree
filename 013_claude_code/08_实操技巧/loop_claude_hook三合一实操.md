# /loop — 让它动起来

# CLAUDE.md — 让它知道自己是谁

在项目根目录放一个 CLAUDE.md，Claude 每次启动都会读。这就是它的操作手册。
```markdown
# 项目：XXX 微服务系统

## 核心规则

- 所有 API 改动必须同步更新 openapi.yaml
- 测试覆盖率不低于 80%
- commit message 用 conventional commits

## 常见操作

- 部署命令：make deploy-prod
- 日志路径：/var/log/app/
- 健康检查：curl -s http://localhost:8080/actuator/health

## /loop 任务清单

- 每 30 分钟检查一次健康检查接口
- 每 2 小时跑一次 lint + test
- 每天早上生成昨日变更摘要
```

# Hook — 让它记住干了什么
在 .claude/settings.json 里配一个 Hook，让每次文件变更自动 git commit：
```markdown
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash|Write|Edit",
        "command": "cd $(pwd) && git add -A && git diff --cached --quiet || git commit -m 'auto: agent checkpoint' --no-verify"
      }
    ]
  }
}
```

好处很直接：Claude 不用浪费 token 去执行 git 命令，每次变更都有记录，出了问题 git log 一查就知道 Agent 干了什么。

三件套就是这么简单。/loop 让它动起来，CLAUDE.md 告诉它规矩，Hook 帮它记账。