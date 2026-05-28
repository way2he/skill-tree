---
name: Day 08 worktree + finishing 完整分支生命周期
description: using-git-worktrees + finishing-a-development-branch 一条分支从创建到结束
type: learning-note
day: 8
tags: ["superpowers", "using-git-worktrees", "finishing-a-development-branch", "学习笔记"]
summary: worktree 让多分支并行不冲突; finishing 给 4 选项菜单 (merge/PR/keep/discard) 强制结构化决策
created_at: 2026-05-28
updated_at: 2026-05-28
---

# Day 08 — worktree + finishing: 分支生命周期

## 一、双 skill 精读

### 1.1 using-git-worktrees 关键步骤

**Step 0 (必做)**: 检测是否已在 worktree 里 — 避免嵌套创建

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
# 注意 submodule guard:
git rev-parse --show-superproject-working-tree 2>/dev/null  # 若有输出, 是 submodule 不是 worktree
```

`GIT_DIR != GIT_COMMON` (且不是 submodule) → 已在 worktree, 跳到 Step 3.

**Step 1a (优先)**: 用平台 native worktree 工具 (EnterWorktree / /worktree).
**Step 1b (fallback)**: 手工 `git worktree add`.

**Step 1b directory priority**:
1. 用户已声明的偏好
2. 项目级 `.worktrees/` 或 `worktrees/` 已存在
3. 全局 `~/.config/superpowers/worktrees/$project`
4. 默认 `.worktrees/`

**安全验证**: 项目级目录必须在 .gitignore (避免 worktree 内容被提交)

```bash
git check-ignore -q .worktrees || (echo ".worktrees/" >> .gitignore && git add .gitignore && git commit -m "chore: ignore worktrees")
```

**Step 3-4**: 自动跑项目 setup (npm install / cargo build / pip install) + 跑 baseline test 确认干净.

### 1.2 finishing-a-development-branch 流程

**Step 1**: 验证 tests pass (失败就停)
**Step 2**: 检测环境 (normal repo / named-branch worktree / detached HEAD)
**Step 3**: 找 base branch (main / master)
**Step 4**: 提供菜单 (normal 4 选项, detached 3 选项)
**Step 5**: 执行选择
**Step 6**: cleanup (只 Option 1 & 4)

#### 4 选项菜单 (normal)

```
1. Merge back to <base> locally
2. Push and create a Pull Request
3. Keep the branch as-is
4. Discard this work
```

#### Option-specific 注意

| Option | Merge | Push | Keep WT | Delete Branch |
|--------|-------|------|---------|---------------|
| 1 Merge | yes | - | - | yes (-d) |
| 2 PR | - | yes | yes | - |
| 3 Keep | - | - | yes | - |
| 4 Discard | - | - | - | yes (-D, 需 typed "discard" 确认) |

#### Cleanup 红线

- **只 cleanup `.worktrees/` / `worktrees/` / `~/.config/superpowers/worktrees/` 路径下的** — 这是 superpowers 创建的, owns cleanup
- 其他路径 → harness/手动管理, 不能动
- 必须先 `cd` 到 main repo root 才能 `git worktree remove` (在 worktree 内执行会静默失败)
- remove 后跑 `git worktree prune` (self-healing)

---

## 二、实战 (模拟流程)

### 场景: 给知识库加 `tools/check_kb_health.py`

#### Step 0: 检测
```bash
GIT_DIR=...   # → .git
GIT_COMMON=... # → .git
# 相等 → 在 normal repo
```

#### Step 1: 询问用户
"要不要建 worktree?" → 假设答 yes.

#### Step 1b: directory selection
- 检查 `.worktrees/` → 不存在
- 检查 instruction 偏好 → 无
- 默认 `.worktrees/`

#### 安全验证
```bash
git check-ignore -q .worktrees
# Exit 1 (not ignored), 加到 .gitignore
echo ".worktrees/" >> .gitignore
git add .gitignore && git commit -m "chore: ignore .worktrees/"
```

#### 创建
```bash
git worktree add .worktrees/feature-kb-health -b feature-kb-health
cd .worktrees/feature-kb-health
```

#### Setup + baseline
- 项目没有 npm/cargo, 跳过
- 跑 `python -m pytest tests/ -v` (假设有) → 假设全过

报告: "Worktree ready at .worktrees/feature-kb-health, tests passing (N tests), ready to implement feature-kb-health."

### 中间实现 (略)

### Finishing

#### Step 1: tests pass? ✅
#### Step 2: 环境 = named-branch worktree
#### Step 3: base = master
#### Step 4: 4 选项菜单展现

假设老板选 **Option 1 (merge locally)**.

#### Step 5: 执行
```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
git checkout master
git pull
git merge feature-kb-health
# verify merged result
python -m pytest tests/ -v  # ✅
```

#### Step 6: cleanup
worktree 路径在 `.worktrees/` 下 → superpowers 创建的, 可以 cleanup.

```bash
# 已经在 main root, 不在 worktree 内
git worktree remove .worktrees/feature-kb-health
git worktree prune
git branch -d feature-kb-health
```

---

## 三、容易踩的坑

| 坑 | 怎么避 |
|----|-------|
| 没 Step 0 直接 `git worktree add` 嵌套 | 永远先跑 Step 0 检测 |
| 漏 submodule guard | `git rev-parse --show-superproject-working-tree` 检查 |
| 在 worktree 内 `git worktree remove` 静默失败 | 先 cd 到 main root |
| cleanup harness 创建的 worktree | provenance check (只动 .worktrees / ~/.config/superpowers/worktrees) |
| Option 2 (PR) 误删 worktree | 只 Option 1 & 4 cleanup |
| 删 branch 前没 remove worktree | git branch -d 会失败 (worktree 还引用) |

---

## 四、Day 8 反思

### 最有用的设计
**4 选项菜单**. 之前完成 feature 就问 "下一步做啥" 是开放问题, 容易扯; 强制 4 选项让决策结构化 5 秒搞定.

### worktree 真正价值
不是 "不同分支不冲突" (clone 也行), 而是**共享 .git 数据库** — clone 各搞各的对象数据库, worktree 共享, 节省磁盘 + 不用 push/pull 同步.

### 跟工作空间状况对比
当前知识库 raw/ 被 gitignore, 实际 raw/skill-tree/12_ai/09_superpowers/ 不需要 worktree 隔离 (反正不入 git). 但写正经代码项目时 worktree 必备.

---

## 五、Day 8 自评

| 维度 | 分 |
|------|---|
| Step 0 检测 + submodule guard | 5/5 |
| Directory priority 正确 | 5/5 |
| 安全验证 (gitignore) | 5/5 |
| 4 选项菜单理解 | 5/5 |
| Cleanup provenance check | 5/5 |

**总评: 25/25** ✅ 满分