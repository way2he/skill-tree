---
name: OpenSpec 常见问题 FAQ
description: OpenSpec 学习与使用过程中的 10 个常见问题汇总，含踩坑解决方案
type: faq
tags: ["OpenSpec", "FAQ", "常见问题", "踩坑"]
summary: 配套 FAQ，覆盖安装、命令、工作流、集成、踩坑等高频问题
created_at: 2026-05-27
updated_at: 2026-05-28
status: done
quality_score: 88
---

# OpenSpec FAQ

> 整理自 7 天学习全程实战中遇到的高频问题。
>
> 相关阅读：[01-快速上手](./01-快速上手.md) · [02-命令速查](./02-命令速查.md)

---

## Q1: Node 版本不够怎么办？

**问题表现**：
```
npm install -g @fission-ai/openspec@latest
> EBADENGINE  Unsupported engine { node: '<20.19' required }
```

**解决方案**：
- 升级到 Node 20.19+ 或 22 LTS（推荐 22 LTS）
- Windows：用 [nvm-windows](https://github.com/coreybutler/nvm-windows)
- macOS / Linux：用 [nvm](https://github.com/nvm-sh/nvm)

```bash
nvm install 22
nvm use 22
node --version  # v22.x.x
npm install -g @fission-ai/openspec@latest
```

⚠️ 不要用 `--ignore-engines` 强装，运行时会有怪异 bug。

---

## Q2: `openspec init` 后多了哪些文件？会污染我的项目吗？

**默认 init（带 `--tools none`）只新增**：
```
openspec/
├── AGENTS.md
├── project.md
├── changes/.gitkeep
└── specs/.gitkeep
```

**绑定 AI 工具时额外新增**（例如 `--tools claude`）：
```
.claude/
├── config.json
└── system-prompts/openspec.md
```

**会污染吗？** 完全不会：
- 全在新目录下，不动你现有任何代码
- 想撤销：`rm -rf openspec/ .claude/`（见 Q10）

---

## Q3: change 和 spec 有什么区别？

| 维度 | change | spec |
|------|--------|------|
| **角色** | 一次需求变更 | 永久能力定义 |
| **生命周期** | 临时（archive 后消失） | 永久（持续演进） |
| **存放位置** | `openspec/changes/<name>/` | `openspec/specs/<capability>/` |
| **可改吗** | 可（archive 前） | archive 时自动合并 delta |
| **类比** | git commit | 主线代码库 |

**口诀**：change 是「这次要改什么」，spec 是「最终系统长什么样」。

---

## Q4: archive 后 change 还能改吗？

**不能**。Archive 是单向门：
- change 从 `changes/<name>` 移到 `changes/archive/YYYY-MM-DD-<name>`
- 不再出现在 `openspec list` 中
- `openspec show <change>` 也查不到

**要改怎么办？** 新建一个 change 去修改对应 capability：
```bash
openspec new change fix-<original>-issue
# 在 spec.md 用 MODIFIED Requirements 去更新
```

---

## Q5: 多人协作时 spec 怎么合并？

### 推荐策略：**同一 capability 同一时间只能 1 个 active change**

- ✅ change-A 改 `user-auth`，change-B 改 `user-profile` → 可并行
- ❌ change-A 和 change-B 都改 `user-auth` → 必须串行或合并

### 工程化做法
1. git 分支 = change：`feature/add-export` ↔ `openspec change add-export`
2. PR 模板加 checkbox：`[ ] 已 openspec validate`
3. CODEOWNERS 锁 `openspec/specs/<cap>/` 目录
4. CI 跑 `openspec validate --all` 把关

### 冲突时
若两个 change 不可避免改同一 capability，**合并为一个 change**：
```bash
openspec merge <change-a> <change-b> --into <merged-name>
```

---

## Q6: 没有 AI 工具能不能用 OpenSpec？

**完全可以**。OpenSpec 的核心价值是「结构化协议」，AI 集成只是加分项。

### 纯人类工作流
```bash
openspec init --tools none
openspec new change add-export
# 你自己写 proposal.md / spec.md / tasks.md
openspec validate add-export
# 你自己写代码、跑测试
openspec archive add-export --yes
```

### 收益（即使没有 AI）
- ✅ 强制结构化思考需求
- ✅ 留下完整审计链
- ✅ 团队 review 有共同语言
- ✅ 半年后回头看仍能复述当时为何这么改

**反过来**：有 AI 工具时，OpenSpec 让 AI 的输出从「猜测」变成「按合约执行」，收益倍增。

---

## Q7: OpenSpec 适合什么规模的项目？

| 项目规模 | 建议 |
|----------|------|
| < 100 行 demo / 一次性脚本 | ❌ 不用，裸 prompt 即可 |
| 100-1000 行 个人工具 | ⚠️ 可选，从下一个新需求开始接 |
| 1000-10000 行 严肃项目 | ✅ 强烈推荐 |
| > 10000 行 团队 / 长期项目 | ✅✅ 必选，否则会失控 |
| 多服务架构 | ✅✅ 必选，每个服务独立 spec |

**经验阈值**：
- 代码 > 1000 行 **或** 维护时间 > 3 个月 **或** 协作人数 > 1 → 上 SDD

---

## Q8: OpenSpec 和 GitHub Spec-Kit 怎么选？

详见 [06-与SpecKit横评](./06-与SpecKit横评.md)。

**一句话决策**：
- 项目在 GitHub 且全用 Copilot → Spec-Kit
- 其他所有情况 → OpenSpec

---

## Q9: spec 文件能用中文写吗？

**完全可以**。OpenSpec 是格式无关的：
```markdown
## ADDED Requirements

### Requirement: 解析中文 Markdown 文件
系统 SHALL 正确解析含中文标题、中文 TODO 项的 markdown 文件。

#### Scenario: 中文 TODO 项
- **WHEN** 输入 `- [ ] 写测试用例`
- **THEN** 返回 `{status: "open", text: "写测试用例"}`
```

### 注意事项
- ✅ Requirement / Scenario 描述用中文 OK
- ✅ 关键字 `SHALL` / `MUST` / `WHEN` / `THEN` 建议保留英文（方便 grep）
- ✅ 文件名建议用英文（避免 git diff 在某些系统乱码）
- ⚠️ 编码必须 UTF-8（Windows 默认 GBK 会乱码，详见 [项目 MEMORY.md 红线 1](../../../MEMORY.md)）

---

## Q10: 想撤销 init 怎么办？

OpenSpec 没有 `openspec uninstall`，但目录可以安全手动删：

```powershell
# 1. 确认没有重要 change 在进行
openspec list

# 2. 备份（可选）
Copy-Item -Recurse openspec/ openspec-backup-$(Get-Date -Format yyyyMMdd)/

# 3. 删除
Remove-Item -Recurse -Force openspec/
Remove-Item -Recurse -Force .claude/  # 若绑了 Claude Code
Remove-Item -Recurse -Force .cursor/  # 若绑了 Cursor
# ... 按实际绑的工具删

# 4. git
git add -A
git commit -m "chore: remove OpenSpec integration"
```

⚠️ **风险提示**：删除 `openspec/specs/` 会丢失所有已归档的需求文档（git 历史里还有）。
建议改为 `git mv openspec/ archive/openspec-legacy/`。

---

## 🔗 还有问题？

- 官方文档：https://intent-driven.dev
- GitHub Issues：https://github.com/fission-ai/openspec/issues
- 本知识库相关：[01-快速上手](./01-快速上手.md) · [02-命令速查](./02-命令速查.md) · [03-SDD方法论](./03-SDD方法论.md)