
---

## 🎯 推荐方案：使用 OpenClaw 内置的独立 Agent 管理

这是 OpenClaw 官方支持的方式，真正的独立运行，互不干扰。

### 🔧 第一步：添加两个独立 Agent

```powershell
# 1. 添加 fanren-novel 独立 agent
openclaw agents add fanren-novel `
  --workspace "C:\Users\robotAi\Documents\ClawWorksapce\fanren-novel" `
  --non-interactive

# 2. 添加 wife-helper 独立 agent
openclaw agents add wife-helper `
  --workspace "C:\Users\robotAi\Documents\ClawWorksapce\WifeHelper" `
  --non-interactive
```

### 📋 查看已添加的 Agent
```powershell
openclaw agents list
```

### 🔗 绑定渠道（可选）
```powershell
# 绑定 wife-helper 到某个渠道，消息自动路由
openclaw agents bind wife-helper --bind telegram:@your_chat_id
```

---

## 🚀 启动方式（对应你问的方法1和方法2）

### 📌 方法1：切换使用（同一时间运行一个）

```powershell
# 启动 gateway，只运行 fanren-novel
openclaw gateway --agent fanren-novel

# 或者只运行 wife-helper
openclaw gateway --agent wife-helper
```

**特点：**
- ✅ 简单，不需要额外配置
- ✅ 资源占用小
- ❌ 同一时间只能运行一个 agent

---

### 📌 方法2：同时独立运行（两个 agent 同时在线）

需要启动两个独立的 gateway 进程，使用不同端口和配置：

```powershell
# 终端1：启动 fanren-novel（默认端口 18789）
openclaw --profile fanren-novel gateway --agent fanren-novel --port 18789

# 终端2：启动 wife-helper（使用端口 18790）
openclaw --profile wife-helper gateway --agent wife-helper --port 18790
```

**特点：**
- ✅ 两个 agent 完全独立，同时运行
- ✅ 互不干扰，有各自的状态和记忆
- ✅ 可以绑定不同的聊天渠道
- ⚠️ 需要两个终端或后台运行

---

## 📊 对比总结

| 方式 | 命令 | 同时运行 | 资源占用 | 推荐场景 |
|------|------|----------|----------|----------|
| **切换使用** | `openclaw gateway --agent <name>` | ❌ 一次一个 | 小 | 平时只用一个 |
| **同时运行** | 两个终端 + `--profile` + `--port` | ✅ 同时在线 | 较大 | 需要两个 agent 同时工作 |

---