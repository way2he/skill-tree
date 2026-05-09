# Claude Code 教程索引

本目录包含从 Runoob 网站抓取的 Claude Code 相关教程。

共 39 个教程页面

---

## Agent Skills | 菜鸟教程

Agent Skills（智能体技能）  Agent 是智能体，Skills 是技能的意思，Agent Skills（智能体技能）是将专业知识、工作流规范固化为可复用资产的核心工具。 Agent Skills 本质上是一个模块化的 Markdown 文件，能教会 AI 工具 （如 Claude、GitHub Copilot、Cursor 等） 执行特定任务，且支持自动触发、团队共享与工程化管理，彻底告别重复的提示词输入。Agent Sk..

[查看全文](claude-agent-skills.md)

---

## Agent Skills | 菜鸟教程

Agent Skills（智能体技能）  Agent 是智能体，Skills 是技能的意思，Agent Skills（智能体技能）是将专业知识、工作流规范固化为可复用资产的核心工具。 Agent Skills 本质上是一个模块化的 Markdown 文件，能教会 AI 工具 （如 Claude、GitHub Copilot、Cursor 等） 执行特定任务，且支持自动触发、团队共享与工程化管理，彻底告别重复的提示词输入。Agent Sk..

[查看全文](claude-agent-skills.md)

---

## CLAUDE.md 使用指南 | 菜鸟教程

CLAUDE.md 使用指南  CLAUDE.md 是 Claude Code 中最重要的配置文件，用于向 Claude 传递项目级别的持久指令。每次启动 Claude Code 会话时，它都会自动读取并加载这个文件中的内容，作为系统级上下文融入每一次对话中。  通俗地说，CLAUDE.md 就是你在项目中给 Claude 写的一份工作手册——告诉它这个项目是什么、遵循什么规范、有哪些注意事项，让它每次都能以符合项目要求的方式工作，而不..

[查看全文](claude-code-claudemd.md)

---

## Claude Code API 配置 | 菜鸟教程

Claude Code API 配置 Claude 在国内用，API 其实不是很友好，除了 Claude 官方的模型，我能用其他 AI 模型吗？  本章节会详细教你如何配置多个国内主流 AI 模型的 API，让 Claude Code 支持：                            厂商/品牌             简介             API 申请入口（点击即达）                        ..

[查看全文](claude-code-setup.md)

---

## Claude Code CLI 参考手册 | 菜鸟教程

Claude Code CLI 参考手册   一、CLI 命令                            命令             描述             示例                                         claude             启动交互式 REPL             claude                               claude &#..

[查看全文](claude-code-cli-ref.md)

---

## Claude Code Git 工作流 | 菜鸟教程

Claude Code Git 工作流  Claude Code 深度集成了 Git 功能，可以用自然语言完成几乎所有 Git 操作，包括创建提交、管理分支、处理合并冲突，以及利用 Git Worktree 实现并行工作流。本章详细介绍如何在 Claude Code 中高效使用 Git。   基础 Git 操作  1、查看变更  用自然语言询问即可获取 Git 状态：  我改了哪些文件？ 这次的改动有哪些内容？ 最近 10 次提交都改了..

[查看全文](claude-code-git-workflow.md)

---

## Claude Code GitHub Actions | 菜鸟教程

Claude Code GitHub Actions  Claude Code GitHub Actions 将 AI 驱动的自动化带到你的 GitHub 工作流中。通过在 PR 或 Issue 中简单地提及 @claude，Claude 就可以分析代码、创建 Pull Request、实现功能、修复 Bug，同时遵循你项目的标准规范。   为什么使用 Claude Code GitHub Actions       即时创建 PR：描..

[查看全文](claude-code-github-actions.md)

---

## Claude Code MCP | 菜鸟教程

Claude Code MCP 如果说 Claude Code 是一个优秀的打字员（代码生成）和测试员（代码校验），那么加上 MCP（Model Context Protocol，模型上下文协议） 则是让 Claude 真正拥有了外部感官和手脚——它不再局限于当前项目的代码文件，而是能主动连接外部世界的资源与工具，成为你的全链路开发协作伙伴。  什么是 MCP (Model Context Protocol)？ MCP 是 Anthro..

[查看全文](claude-code-mcp.md)

---

## Claude Code Skills 使用实例 | 菜鸟教程

Claude Code Skills 使用实例 在上一章节 Agent Skills（智能体技能） 中我们已经了解了 Skills 的基本概念，本章节我们将结合一个具体的 Skills 来开发一个项目。   现在市面上已经有很多现成的 skills，我么可以直接拿来使用，我们可以在 https://skills.sh/ 查找更多的 skill。 安装方式： npx skills add npx 安装 ui-ux-pro-max 可参考：..

[查看全文](claude-code-ui-ux-pro-max-skill.md)

---

## Claude Code 上下文管理 | 菜鸟教程

Claude Code 上下文管理  上下文管理是高效使用 Claude Code 的核心技能。 官方文档明确指出：上下文窗口是 Claude Code 最重要的资源，随着上下文填满，模型性能会逐渐下降（称为上下文衰退，context rot）——这是使用 Claude Code 时需要主动对抗的核心问题。  本章深入讲解如何通过 CLAUDE.md 指令文件、自动记忆系统、上下文窗口优化命令等手段，让 Claude 在长会话和跨会话中..

[查看全文](claude-code-context.md)

---

## Claude Code 交互模式 | 菜鸟教程

Claude Code 交互模式 与网页版 Claude 不同，Claude Code 并不是一个单纯的聊天工具，而是一个具备工程上下文、权限控制和执行能力的开发协作系统。因此，它在处理任务时，引入了三种核心的思维模式：      Ask（询问）     Plan（规划）     Edit（编辑）  理解这三种模式的边界与职责，是高效、安全使用 Claude Code 的关键。 终端执行其实不用手动切换，Claude 会自动切换，在 V..

[查看全文](claude-code-cli.md)

---

## Claude Code 基础用法 | 菜鸟教程

Claude Code 基础用法  本章介绍 Claude Code 日常开发中最常用的核心功能，包括如何与 Claude 对话、读取和修改代码、执行命令、处理文件，以及一些能大幅提升效率的实用技巧。   基本对话方式  1、交互模式（最常用）  在项目目录下启动 Claude Code，进入交互模式后即可直接输入问题或指令：  cd /path/to/your/project claude  在交互模式中，直接输入自然语言即可，无需任..

[查看全文](claude-code-basic.md)

---

## Claude Code 如何工作 | 菜鸟教程

Claude Code 如何工作 简单来说：Claude Code 就像一个超级聪明的编程搭档，它能在你的电脑上自动帮你写代码、改 bug、运行命令、搜索文件……几乎所有你在终端里能做的事，它都能干！ 本节带你彻底搞懂它的底层原理（代理循环、模型、工具等），看完你就知道它为什么这么强大，以及怎么用得更顺手。 Claude 的工作流程 当你给 Claude 一个任务时，它会像人类一样循环思考三个步骤：      收集上下文（看你的代码、文..

[查看全文](claude-code-how-it-work.md)

---

## Claude Code 子代理 | 菜鸟教程

Claude Code 子代理（Subagent）  在 Claude Code 中，你可以创建专门的 AI 子代理（Subagent），用于处理特定类型的任务，从而获得更好的上下文隔离、更强的约束控制和更高的执行效率。  子代理运行在独立的上下文窗口中，每个子代理都可以拥有独立的系统提示、指定的模型、明确的工具访问权限、独立的权限模式，以及跨会话的持久记忆。当 Claude 判断你的请求符合某个子代理的描述时，会自动将任务委托给它，由..

[查看全文](claude-code-subagent.md)

---

## Claude Code 安装与使用 | 菜鸟教程

Claude Code 安装与使用  在正式安装之前，先了解一下 Claude Code 有哪几种使用方式，选择最适合自己的方式入手。                             方式             适合人群             优点             缺点                                         Web 端             完全新手            ..

[查看全文](claude-code-install.md)

---

## Claude Code 实战 | 菜鸟教程

Claude Code 实战 本章节我们将介绍如何用 Claude Code 通过我们的描述提示词开发华尔街日报风格新闻卡片应用。 整个过程尽量不写一行代码，用我们的自然语言描述让 AI 帮我们完成整个项目。 目标: 使用 React + Tailwind CSS 创建一个华尔街日报风格的新闻卡片生成器 功能特性:      经典的 WSJ 设计风格（衬线字体、简洁排版）     新闻卡片生成（标题、摘要、作者、时间）     支持图片..

[查看全文](claude-code-practical.md)

---

## Claude Code 并行任务 | 菜鸟教程

Claude Code 并行任务  Claude Code 提供了多种并行执行任务的机制，让你可以同时处理多个工作项，显著提升开发效率。本章将介绍三种主要的并行化方案：Subagents（子代理）、Agent Teams（代理团队）和 Git Worktree（Git 工作树），帮助你根据不同的使用场景选择最合适的方式。   并行任务概述  当面对复杂任务时，单个 Claude 实例可能会力不从心——上下文过长、响应变慢、任务交织。Cl..

[查看全文](claude-code-parallel-tasks.md)

---

## Claude Code 控制 Chrome 浏览器 | 菜鸟教程

Claude Code 控制 Chrome 浏览器 Claude Code 的 Chrome 集成功能，让你可以直接从命令行（CLI）或 VS Code 扩展中控制浏览器。Claude 能够：      打开网页、点击按钮、填写表单     读取浏览器控制台日志（console errors、network requests、DOM 状态）     与任何你已登录的网站交互（Gmail、Notion、Google Docs 等）    ..

[查看全文](claude-code-chrome.md)

---

## Claude Code 控制与模式 | 菜鸟教程

Claude Code 控制与模式 Claude Code 交互模式的核心能力包括键盘快捷键、Vim 编辑模式、命令历史管理和后台 Bash 命令运行，以下是提炼后的关键内容： 一、 键盘快捷键 快捷键效果因终端和系统而异，macOS 用户需将 Option 键配置为 Meta（不同终端配置路径见原文），按 ? 可查看当前环境可用快捷键。                            分类             快捷键/操作 ..

[查看全文](claude-code-control.md)

---

## Claude Code 插件 | 菜鸟教程

Claude Code 插件 插件（Plugin）是 Claude Code 中最高级别的扩展机制，用于将命令、代理、Skills、钩子、MCP、LSP 等能力打包、版本化、共享和分发。  插件 = 一组可复用的 Claude Code 扩展能力集合 一个插件可以包含：      斜杠命令（Slash Commands）     子代理（Agents）     Skills（能力说明）     Hooks（事件钩子）     MCP 服..

[查看全文](claude-code-plugins.md)

---

## Claude Code 插件参考手册 | 菜鸟教程

Claude Code 插件参考手册  插件是 Claude Code 的功能扩展核心，能帮你添加自定义斜杠命令、子代理、自动化钩子等能力。本教程从核心组件、配置规范、CLI 管理三个维度，带你快速掌握插件的使用与开发要点。 插件核心组件：5类扩展能力 插件通过 5 类组件实现功能扩展，每个组件都有固定的存储位置和格式要求。                            组件类型             存储位置        ..

[查看全文](claude-code-plugin-ref.md)

---

## Claude Code 操作说明 | 菜鸟教程

Claude Code 操作说明 Claude Code 的输入框不是纯聊天框，而是一个：      AI + 编辑器 + 命令调度器的融合终端  主要有三类前缀触发器：                            符号             类型             本质作用                                         /             Command（命令）       ..

[查看全文](claude-code-symbols.md)

---

## Claude Code 教程 | 菜鸟教程

Claude Code 教程    Claude Code 是 Anthropic 推出的面向开发者的 AI 编程协作工具。 Claude Code 定位不是聊天，而是在本地代码仓库中执行高权限、可上下文感知的工程任务。   Claude Code 与在聊天窗口里写几段代码不同，它理解你的整个项目，能直接读取你的文件、运行测试并根据反馈修改代码。  Claude Code 不是一个代码生成器，而是一个能读项目、懂上下文、遵守约束的 AI..

[查看全文](claude-code-tutorial.md)

---

## Claude Code 教程 | 菜鸟教程

Claude Code 教程    Claude Code 是 Anthropic 推出的面向开发者的 AI 编程协作工具。 Claude Code 定位不是聊天，而是在本地代码仓库中执行高权限、可上下文感知的工程任务。   Claude Code 与在聊天窗口里写几段代码不同，它理解你的整个项目，能直接读取你的文件、运行测试并根据反馈修改代码。  Claude Code 不是一个代码生成器，而是一个能读项目、懂上下文、遵守约束的 AI..

[查看全文](claude-code-tutorial.md)

---

## Claude Code 斜杠 / 命令 | 菜鸟教程

.new-badge {     display: inline-block;     background: #4CAF50;     color: #fff;     font-size: .72em;     border-radius: 3px;     padding: 1px 6px;     vertical-align: middle;     margin-left: 5px;     font-weight: nor..

[查看全文](claude-code-slash-commands.md)

---

## Claude Code 权限配置 | 菜鸟教程

Claude Code 权限配置  Claude Code 使用分层权限系统来平衡功能和安全性，支持细粒度权限规则、权限模式和沙箱策略来控制 Claude 可以访问和执行的操作。合理配置权限，既能让 AI 高效完成任务，又能防止误操作破坏代码或泄露敏感文件。  从 Claude Code v1.1.1 开始，推荐使用新的权限配置方式。旧的 tools 布尔配置仍被支持，但建议迁移到新的权限规则语法。   权限系统概述  Claude C..

[查看全文](claude-code-permission.md)

---

## Claude Code 检查点 | 菜鸟教程

Claude Code 检查点 检查点是 Claude Code 的代码安全回退工具，能自动跟踪 Claude 对文件的编辑操作，帮你快速撤销不需要的更改，避免代码改坏后难以恢复。 检查点的工作原理 检查点会在你使用 Claude Code 时自动后台运行，全程无需手动配置：      自动创建：每次发送用户提示后，都会自动创建一个检查点，记录当前的代码状态     持久保存：检查点会在会话之间保留，即使关闭会话，下次恢复后仍能访问历史..

[查看全文](claude-code-checkpointing.md)

---

## Claude Code 环境变量 | 菜鸟教程

Claude Code 环境变量  环境变量是控制 Claude Code 行为的重要方式，无需编辑配置文件即可灵活调整各项设置。本章详细介绍 Claude Code 支持的所有环境变量、它们的用途、配置方式以及常见使用场景。   环境变量概述  Claude Code 使用环境变量来控制行为，这些变量可以通过以下方式设置：       直接在 shell 中 export     在 ~/.claude/settings.json 的..

[查看全文](claude-code-env.md)

---

## Claude Code 第一次使用 | 菜鸟教程

Claude Code 第一次使用  安装了 Claude Code 及配置好 API 后，我们就可以开始使用了。  接下来，我们用一个最简单的示例项目来完成第一次使用。  创建一个示例项目： mkdir runoob-claude-demo cd runoob-claude-demo   创建一个简单文件：  touch main.py   写入以下内容：  def add(a, b):     return a + b  让 Cla..

[查看全文](claude-code-first-demo.md)

---

## Claude Code 简介 | 菜鸟教程

Claude Code 简介 Claude Code 是 Anthropic 推出的面向开发者的 AI 编程协作工具，与在聊天窗口里写几段代码不同，Claude Code 的核心目标是理解你的整个项目，并参与到真实的编码、修改和重构过程中。   Claude Code 不是一个代码生成器，而是一个能读项目、懂上下文、遵守约束的 AI 编程搭档。 简单说:Claude Code 是 Claude 的命令行版本,专门为编程场景设计。 它不是..

[查看全文](claude-code-intro.md)

---

## Claude Code 简介 | 菜鸟教程

Claude Code 简介 Claude Code 是 Anthropic 推出的面向开发者的 AI 编程协作工具，与在聊天窗口里写几段代码不同，Claude Code 的核心目标是理解你的整个项目，并参与到真实的编码、修改和重构过程中。   Claude Code 不是一个代码生成器，而是一个能读项目、懂上下文、遵守约束的 AI 编程搭档。 简单说:Claude Code 是 Claude 的命令行版本,专门为编程场景设计。 它不是..

[查看全文](claude-code-intro.md)

---

## Claude Code 记忆系统（Memory） | 菜鸟教程

Claude Code 记忆系统（Memory）      每次 Claude Code 会话结束，上下文就会清空。 有时候我们每次都要重新告诉 Claude “用 pnpm 而不是 npm”、”我们的缩进是 2 个空格”？记忆系统（Memory） 正是为此而生。   什么是 Claude Code 的记忆系统？ Claude Code 没有跨会话的自动记忆——每个新会话都从一个全新的上下文窗口开始。记忆系统通过两种互补机制，让知识能够..

[查看全文](claude-code-memory.md)

---

## Claude Code 输出样式 | 菜鸟教程

Claude Code 输出样式  输出样式（Output Style）让你可以定制 Claude Code 的交互风格和响应方式，使其适配软件开发之外的更多使用场景，同时保留运行本地脚本、读写文件、跟踪待办事项等核心功能。  其本质是通过修改系统提示（System Prompt），改变 Claude Code 的交互逻辑和响应风格。   内置输出样式  Claude Code 提供 3 种开箱即用的输出样式：             ..

[查看全文](claude-code-outputstyles.md)

---

## Claude Code 钩子 | 菜鸟教程

Claude Code 钩子  Claude Code 钩子是用户自定义的 Shell 命令，会在 Claude Code 生命周期的特定节点自动执行。借助钩子，你可以对 Claude Code 的行为实现精准控制，确保某些操作（如代码格式化、日志记录）必定触发，而非依赖大模型自主选择是否执行。  钩子的典型应用场景 钩子能帮你实现很多实用功能，常见场景包括：      消息通知：当 Claude Code 等待输入或需要权限时，自动发..

[查看全文](claude-code-hooks.md)

---

## Claude Code 项目初始化 | 菜鸟教程

Claude Code 项目初始化 Claude Code 项目初始化可以在 Claude Code 的交互界面中输入： /init 我们可以在一个已有的项目目录初始化，也可以新建一个。   我们可以先创建一个目录： mkdir claude-runoob-test  进入该目录： cd claude-runoob-test 创建一个测试文件 test.py，代码如下： print('Hello, Runoob!')..

[查看全文](claude-code-init.md)

---

## Claude Code 项目目录结构 | 菜鸟教程

Claude Code 项目目录结构 一个典型的 Claude Code 项目目录结构如下： your-project/ ├── CLAUDE.md                    ← 团队共享指令，提交到 git ├── CLAUDE.local.md              ← 个人覆盖，被 git 忽略 └── .claude/     ├── settings.json            ← 权限 + 配置，提交到 ..

[查看全文](claude-code-project.md)

---

## Coding Plan | 菜鸟教程

Coding Plan  现在市面上有很多大模型厂商， 国外的有 Anthropic、Open AI、Grok、Gemini等，但是访问国外现在不方便，国内的有 DeepSeek、千问、ZLM、Minimax 等。 我们使用Claude Code 写代码最费钱的就是 token 了，海外的访问不方便，而且还贵，国内的现在都有包月套餐，如果长期用建议买包月套餐划算。        很多厂商都退出了 Coding Plan，它专为 AI 编..

[查看全文](coding-plan.md)

---

## VS Code 安装 Claude Code | 菜鸟教程

VS Code 安装 Claude Code  如果不喜欢使用 Claude Code 的命令行模型，我们可以在 VS Code 编辑器中安装 Claude Code。 打开 VS Code，进入扩展市场，搜索 Claude Code 安装：  安装完成后，点击右上角 Claude Code 图标，即可进入 Claude Code 页面：   这样有账号的可以使用 /login 登录：   也可以在对话框输入 /config 进入设置，..

[查看全文](vscode-install-claude-code.md)

---

## skill-creator 使用 | 菜鸟教程

skill-creator 使用   在 Claude Code 生态中，Skill（技能） 是扩展 Agent 能力的重要机制。 Skill 本质上是一个模块化知识包，可以给 Claude 添加：  	 专业领域知识  	 固定工作流程  	 API / 工具使用方式  	 模板和脚本     简单理解：  Skill = 给 AI 写的一份操作说明书。  而 skill-creator 就是 Anthropic 官方提供的 Skil..

[查看全文](skill-creator-usage.md)

---

*此索引文件由自动脚本生成*
