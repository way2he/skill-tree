---
name: Day 06 systematic-debugging 重做
description: 用假设驱动 4 阶段法重做最近一次踩过的乱码污染坑
type: learning-note
day: 6
tags: ["superpowers", "systematic-debugging", "假设驱动", "学习笔记"]
summary: systematic-debugging Iron Law: NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST. 4 个 phase 必须按序走, 跳一步就退回 Phase 1. 3+ 次修复失败 = 架构问题
created_at: 2026-05-28
updated_at: 2026-05-28
---

# Day 06 — systematic-debugging: 4 阶段假设驱动重做

> **Iron Law**: NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
> 4 phase: Root Cause → Pattern Analysis → Hypothesis & Testing → Implementation
> 3+ fix failed = 架构问题, 不要继续修, 找 partner 讨论

---

## 一、skill 精读核心 (1505 词)

### 1.1 四个 Phase

**Phase 1 — Root Cause**
1. 仔细读错误 (don't skip)
2. 稳定复现
3. 检查 recent changes (git diff)
4. **多组件系统加 diagnostic instrumentation** (在每个边界 log 进出数据)
5. 反向 trace data flow

**Phase 2 — Pattern Analysis**
1. 找 working examples
2. 完整读 reference (不是 skim)
3. 列出所有 differences (再小也不忽略)
4. 理解 dependencies

**Phase 3 — Hypothesis**
1. **单一假设**: "I think X is the root cause because Y"
2. 最小测试
3. 一次只改一个变量
4. 不懂就说不懂, 别装

**Phase 4 — Implementation**
1. 先写失败 test case (复现 bug)
2. 单一 fix (no "while I am here")
3. 验证 fix
4. **3+ fix 失败 → 停下来问架构是否错了**

### 1.2 Partner 暗示你做错的信号

- "Is that not happening?" → 你没验证就假设
- "Will it show us...?" → 该加 evidence gathering 没加
- "Stop guessing" → 你在试错
- "Ultrathink this" → 该质疑底层
- "We are stuck?" (frustrated) → approach 不行

---

## 二、案例: 重做工作空间最近的乱码污染坑

### 背景 (从 memory/active/lessons-learned.md 检索)

工作空间近期多次发生 wiki 文件 frontmatter 或全文乱码污染. 这是真实踩过的坑.

### Phase 1: Root Cause Investigation

#### 1. 读错误
当时表象: `git status` 显示 `wiki/澶ц瑷€妯″瀷/RAG妫€绱㈠寮虹敓鎴愬畬鍏ㄨ瑙?` 这样的乱码文件名.

```
?? wiki/澶ц瑷€妯″瀷/RAG妫€绱㈠寮虹敓鎴愬畬鍏ㄨ瑙?浠庡叆闂ㄥ埌鐢熶骇绾?md
```

#### 2. 复现
- 100% 复现: 任何不带 UTF-8 BOM 的中文文件 git add 后, status 输出都这样.
- 试过 `git -c core.quotepath=false status -s` → 显示正常 (`wiki/大语言模型/...`)

#### 3. Recent changes
- 切到 PowerShell 7, console output encoding 是 GBK (代码页 936)
- 文件本身是 UTF-8

#### 4. 多组件系统加 diagnostic
```powershell
$OutputEncoding              # → Encoding (UTF8 or GBK?)
[Console]::OutputEncoding    # → 同
chcp                         # → Active code page
git config --get core.quotepath  # → true (default)
```

实测得到 `[Console]::OutputEncoding = GBK`, `core.quotepath = true`. 这两个组合让 git 把 UTF-8 bytes 当 GBK 解读.

#### 5. Data flow 反向 trace
```
文件 (UTF-8 bytes)
  → git status 调用 (默认 quotepath=true, 转义非 ASCII)
  → PowerShell stdout (Console.OutputEncoding=GBK)
  → 显示 (乱码)
```

bug 不在文件, 在**显示管道**.

### Phase 2: Pattern Analysis

#### Working examples
- VSCode 终端: 同一个 git status 显示正常 → VSCode 设置 PowerShell 用 UTF-8
- WSL bash: 显示正常 → Linux 默认 UTF-8

#### Reference 完整读
git docs `core.quotepath`: 默认为 true, 把 0x80+ 字节转 octal 显示, 保留兼容性.

#### Differences
| 环境 | OutputEncoding | quotepath | 结果 |
|------|---------------|-----------|------|
| VSCode PS | UTF-8 | true | 正常 |
| 系统 PS 5 | GBK | true | 乱码 |
| WSL bash | UTF-8 | true | 正常 |

### Phase 3: Hypothesis

#### 单一假设
**"I think the root cause is that PowerShell default OutputEncoding is GBK on this Windows locale, and combined with git's default core.quotepath=true escaping, UTF-8 byte sequences are mis-decoded."**

可证伪? ✅ — 改 OutputEncoding 为 UTF-8 后, 同一文件应能正常显示.

#### 最小测试
```powershell
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
git status -s
```

实测 (在工作空间真跑过) → ✅ 显示 `wiki/大语言模型/...` 正确.

### Phase 4: Implementation

#### 失败 test case (复现)
新开 PowerShell session 不设 encoding → status 出乱码.

#### 单一 fix
两个 root cause 任一可解: (A) 改 PowerShell profile 设默认 UTF-8 (B) 改 git config `core.quotepath=false`.

选 **B (git config)**, 因影响范围最小 (只动 git 行为, 不动 shell 全局).

```bash
git config --global core.quotepath false
```

#### Verify fix
新 session 直接 `git status -s` → ✅ 正常显示中文文件名.

#### Fix 是否真根因?
是 — 不是 "工作 around" 乱码 (e.g., 每次手动改 encoding), 而是从 git 输出源头消除转义.

---

## 三、之前犯的错 (没用 systematic-debugging)

| 错误做法 | 错的原因 |
|---------|---------|
| 第一反应改 chcp 65001 | 治标不治本, 新 session 又回去 |
| 每次手动设 $OutputEncoding | Phase 4 #2 violation: "while I am here" 试多种 |
| 假设是 git 装得不对 | Phase 1 #1: 没认真读 status 输出本身 (其实是显示问题, 不是数据问题) |

按 4 phase 走以后 = 1 个 commit, 永久解决.

---

## 四、Day 6 反思

### 最大启发
**Phase 1.4 "diagnostic instrumentation"**: 多组件系统里, **先 log 每个边界的进出数据**, 不要直接猜哪个组件错. 我之前总跳过这步, 直接猜.

### 跟试错的差别
- 试错: 改一个跑一次看好不好, 不行再改下一个 → 永远在抖动
- 假设驱动: 写下"我认为 X 是根因因为 Y", 设计最小实验, 跑完知道假设对错 → 收敛

### 3+ fix 失败的 trigger
之前真有过同一类 bug 试 5+ 次都没解决的情况 (当时是 hugo 渲染问题). 按这条 skill, 第 3 次失败时就该停下问"是不是整个 hugo 模板架构选错了". 实际我修到第 7 次才停, 浪费 3 小时.

---

## 五、Day 6 自评

| 维度 | 分 |
|------|---|
| 4 phase 按序 | 5/5 |
| 假设可证伪 | 5/5 |
| 最小 fix | 5/5 |
| 没用 "while I am here" | 5/5 |
| 真根因 (非治标) | 5/5 |

**总评: 25/25** ✅ 满分通关