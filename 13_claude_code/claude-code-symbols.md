# Claude Code 操作说明 | 菜鸟教程

Claude Code 操作说明 Claude Code 的输入框不是纯聊天框，而是一个：      AI + 编辑器 + 命令调度器的融合终端  主要有三类前缀触发器：                            符号             类型             本质作用                                         /             Command（命令）       ..

---

# Claude Code 操作说明

## /—— 操作型命令（最重要）
## @—— 上下文注入@后面跟文件名，会主动联想：引用单文件:@main.py 帮我检查 bug引用多个文件:@main.py @main2.py 这两个是否有重复逻辑？引用整个目录使用@ + 目录路径:@src/ 分析项目结构并给出优化建议引用错误日志：@npm-debug.log 找出失败原因Claude 会把文件内容真实加载进推理上下文。!-- Bash 命令通过在输入前加上!直接运行 bash 命令，无需通过 Claude，格式为：! + Bash 命令输入 ! 就会提示进入 Bash 命令模式：例如查看当前的目录：! ls -laVim 编辑器模式使用/vim命令启用 vim 风格编辑，或通过/config永久配置。模式切换命令操作来自模式Esc进入 NORMAL 模式INSERTi在光标前插入NORMALI在行首插入NORMALa在光标后插入NORMALA在行尾插入NORMALo在下方打开行NORMALO在上方打开行NORMAL导航（NORMAL 模式）命令操作h/j/k/l向左/下/上/右移动w下一个单词e单词末尾b上一个单词0行首$行尾^第一个非空白字符gg输入开始G输入结束f{char}跳转到下一个字符出现处F{char}跳转到上一个字符出现处t{char}跳转到下一个字符出现处之前T{char}跳转到上一个字符出现处之后;重复最后一个 f/F/t/T 动作,反向重复最后一个 f/F/t/T 动作编辑（NORMAL 模式）命令操作x删除字符dd删除行D删除到行尾dw/de/db删除单词/到末尾/向后cc更改行C更改到行尾cw/ce/cb更改单词/到末尾/向后yy/Y复制（yank）行yw/ye/yb复制单词/到末尾/向后p在光标后粘贴P在光标前粘贴>>缩进行<<取消缩进行J连接行.重复最后一个更改文本对象（NORMAL 模式）文本对象与d、c和y等运算符一起工作：命令操作iw/aw内部/周围单词iW/aW内部/周围 WORD（空格分隔）i"/a"内部/周围双引号i'/a'内部/周围单引号i(/a(内部/周围括号i[/a[内部/周围方括号i{/a{内部/周围花括号命令历史Claude Code 为当前会话维护命令历史：历史按工作目录存储使用/clear命令清除使用上/下箭头导航（请参阅上面的键盘快捷键）注意：历史扩展（!）默认禁用使用 Ctrl+R 反向搜索按Ctrl+R交互式搜索您的命令历史：开始搜索：按Ctrl+R激活反向历史搜索键入查询：输入文本以在以前的命令中搜索 - 搜索词将在匹配结果中突出显示导航匹配：再次按Ctrl+R循环浏览较旧的匹配接受匹配：按Tab或Esc接受当前匹配并继续编辑按Enter接受并立即执行命令取消搜索：按Ctrl+C取消并恢复原始输入在空搜索上按Backspace取消搜索显示匹配的命令，搜索词突出显示，使您可以轻松找到并重用以前的输入。后台 bash 命令Claude Code 支持在后台运行 bash 命令，允许您在长时间运行的进程执行时继续工作。后台运行的工作原理当 Claude Code 在后台运行命令时，它异步运行命令并立即返回后台任务 ID。Claude Code 可以在命令继续在后台执行时响应新提示。要在后台运行命令，您可以：提示 Claude Code 在后台运行命令按 Ctrl+B 将常规 Bash 工具调用移到后台。（Tmux 用户必须按两次 Ctrl+B，因为 tmux 的前缀键。）主要功能：输出被缓冲，Claude 可以使用 TaskOutput 工具检索它后台任务具有用于跟踪和输出检索的唯一 ID当 Claude Code 退出时，后台任务会自动清理要禁用所有后台任务功能，请将CLAUDE_CODE_DISABLE_BACKGROUND_TASKS环境变量设置为1。常见后台命令：构建工具（webpack、vite、make）包管理器（npm、yarn、pnpm）测试运行器（jest、pytest）开发服务器长时间运行的进程（docker、terraform）使用!前缀的 Bash 模式通过在输入前加上!直接运行 bash 命令，无需通过 Claude：! npm test
! git status
! ls -laBash 模式：将命令及其输出添加到对话上下文显示实时进度和输出支持相同的Ctrl+B后台运行长时间运行的命令不需要 Claude 解释或批准命令支持基于历史的自动完成：键入部分命令并按Tab从当前项目中的以前的!命令完成这对于快速 shell 操作同时保持对话上下文很有用。按键说明常规控制快捷键描述上下文Ctrl+C取消当前输入或生成标准中断Ctrl+D退出 Claude Code 会话EOF 信号Ctrl+G在默认文本编辑器中打开在默认文本编辑器中编辑您的提示或自定义响应Ctrl+L清除终端屏幕保留对话历史Ctrl+O切换详细输出显示详细的工具使用和执行情况Ctrl+R反向搜索命令历史交互式搜索以前的命令Ctrl+V或Cmd+V（iTerm2）或Alt+V（Windows）从剪贴板粘贴图像粘贴图像或图像文件的路径Ctrl+B后台运行任务后台运行 bash 命令和代理。Tmux 用户按两次Left/Right arrows在对话框选项卡之间循环在权限对话框和菜单中的选项卡之间导航Up/Down arrows导航命令历史回忆以前的输入Esc+Esc回退代码/对话将代码和/或对话恢复到之前的状态Shift+Tab或Alt+M（某些配置）切换权限模式在自动接受模式、Plan Mode 和正常模式之间切换Option+P（macOS）或Alt+P（Windows/Linux）切换模型在不清除提示的情况下切换模型Option+T（macOS）或Alt+T（Windows/Linux）切换扩展思考启用或禁用扩展思考模式。首先运行/terminal-setup以启用此快捷键文本编辑快捷键描述上下文Ctrl+K删除到行尾存储已删除的文本以供粘贴Ctrl+U删除整行存储已删除的文本以供粘贴Ctrl+Y粘贴已删除的文本粘贴用Ctrl+K或Ctrl+U删除的文本Alt+Y（在Ctrl+Y之后）循环粘贴历史粘贴后，循环浏览以前删除的文本。在 macOS 上需要将 Option 设置为 MetaAlt+B将光标向后移动一个单词单词导航。在 macOS 上需要将 Option 设置为 MetaAlt+F将光标向前移动一个单词单词导航。在 macOS 上需要将 Option 设置为 Meta主题和显示快捷键描述上下文Ctrl+T切换代码块的语法高亮仅在/theme选择器菜单内工作。控制 Claude 响应中的代码是否使用语法着色语法高亮仅在 Claude Code 的原生构建中可用。多行输入方法快捷键上下文快速转义\+Enter在所有终端中工作macOS 默认Option+EntermacOS 上的默认设置Shift+EnterShift+Enter在 iTerm2、WezTerm、Ghostty、Kitty 中开箱即用控制序列Ctrl+J多行的换行符粘贴模式直接粘贴对于代码块、日志Shift+Enter 在 iTerm2、WezTerm、Ghostty 和 Kitty 中无需配置即可工作。对于其他终端（VS Code、Alacritty、Zed、Warp），运行/terminal-setup以安装绑定。
## !-- Bash 命令
## Vim 编辑器模式
## 命令历史
## 后台 bash 命令
## 按键说明

### 模式切换
### 导航（NORMAL 模式）
### 编辑（NORMAL 模式）
### 文本对象（NORMAL 模式）
### 使用 Ctrl+R 反向搜索
### 后台运行的工作原理
### 使用!前缀的 Bash 模式
### 常规控制
### 文本编辑
### 主题和显示
### 多行输入

- 历史按工作目录存储
- 使用/clear命令清除
- 使用上/下箭头导航（请参阅上面的键盘快捷键）
- 注意：历史扩展（!）默认禁用

- 开始搜索：按Ctrl+R激活反向历史搜索
- 键入查询：输入文本以在以前的命令中搜索 - 搜索词将在匹配结果中突出显示
- 导航匹配：再次按Ctrl+R循环浏览较旧的匹配
- 接受匹配：按Tab或Esc接受当前匹配并继续编辑按Enter接受并立即执行命令
- 取消搜索：按Ctrl+C取消并恢复原始输入在空搜索上按Backspace取消

- 按Tab或Esc接受当前匹配并继续编辑
- 按Enter接受并立即执行命令

- 按Ctrl+C取消并恢复原始输入
- 在空搜索上按Backspace取消

- 提示 Claude Code 在后台运行命令
- 按 Ctrl+B 将常规 Bash 工具调用移到后台。（Tmux 用户必须按两次 Ctrl+B，因为 tmux 的前缀键。）

- 输出被缓冲，Claude 可以使用 TaskOutput 工具检索它
- 后台任务具有用于跟踪和输出检索的唯一 ID
- 当 Claude Code 退出时，后台任务会自动清理

- 构建工具（webpack、vite、make）
- 包管理器（npm、yarn、pnpm）
- 测试运行器（jest、pytest）
- 开发服务器
- 长时间运行的进程（docker、terraform）

- 将命令及其输出添加到对话上下文
- 显示实时进度和输出
- 支持相同的Ctrl+B后台运行长时间运行的命令
- 不需要 Claude 解释或批准命令
- 支持基于历史的自动完成：键入部分命令并按Tab从当前项目中的以前的!命令完成

| 符号 | 类型 | 本质作用 |
| --- | --- | --- |
| / | Command（命令） | 执行内置操作 |
| @ | Context（上下文） | 引用文件/代码/目录 |
| ! | Bash 模式 | 直接执行终端命令，stdout/stderr 自动注入上下文 |
| # | Memory（记忆注入） | 把内容持久写入 CLAUDE.md 项目记忆，跨会话长期生效，例如：#config.yaml |
| & | Async（异步任务） | 后台/云端异步执行任务，不阻塞当前会话，可关闭终端后在 claude.ai/code 查看进度 |
| \+Enter | Multiline（多行输入） | 换行不发送，写多行内容，长需求描述一次性写完 |
| 无前缀 | 自然语言 | 普通任务指令 |

| 命令 | 作用 |
| --- | --- |
| /help | 查看全部能力 |
| /clear | 清空对话 |
| /plan | 进入规划模式 |
| /model | 切换模型 |
| /context | 查看上下文使用情况 |
| /export | 导出对话 |
| /status | 环境状态 |
| /tasks | 管理后台任务 |
| /theme | 主题切换 |
| /memory | 编辑 CLAUDE.md |

| 命令 | 操作 | 来自模式 |
| --- | --- | --- |
| Esc | 进入 NORMAL 模式 | INSERT |
| i | 在光标前插入 | NORMAL |
| I | 在行首插入 | NORMAL |
| a | 在光标后插入 | NORMAL |
| A | 在行尾插入 | NORMAL |
| o | 在下方打开行 | NORMAL |
| O | 在上方打开行 | NORMAL |

| 命令 | 操作 |
| --- | --- |
| h/j/k/l | 向左/下/上/右移动 |
| w | 下一个单词 |
| e | 单词末尾 |
| b | 上一个单词 |
| 0 | 行首 |
| $ | 行尾 |
| ^ | 第一个非空白字符 |
| gg | 输入开始 |
| G | 输入结束 |
| f{char} | 跳转到下一个字符出现处 |
| F{char} | 跳转到上一个字符出现处 |
| t{char} | 跳转到下一个字符出现处之前 |
| T{char} | 跳转到上一个字符出现处之后 |
| ; | 重复最后一个 f/F/t/T 动作 |
| , | 反向重复最后一个 f/F/t/T 动作 |

| 命令 | 操作 |
| --- | --- |
| x | 删除字符 |
| dd | 删除行 |
| D | 删除到行尾 |
| dw/de/db | 删除单词/到末尾/向后 |
| cc | 更改行 |
| C | 更改到行尾 |
| cw/ce/cb | 更改单词/到末尾/向后 |
| yy/Y | 复制（yank）行 |
| yw/ye/yb | 复制单词/到末尾/向后 |
| p | 在光标后粘贴 |
| P | 在光标前粘贴 |
| >> | 缩进行 |
| << | 取消缩进行 |
| J | 连接行 |
| . | 重复最后一个更改 |

| 命令 | 操作 |
| --- | --- |
| iw/aw | 内部/周围单词 |
| iW/aW | 内部/周围 WORD（空格分隔） |
| i"/a" | 内部/周围双引号 |
| i'/a' | 内部/周围单引号 |
| i(/a( | 内部/周围括号 |
| i[/a[ | 内部/周围方括号 |
| i{/a{ | 内部/周围花括号 |

| 快捷键 | 描述 | 上下文 |
| --- | --- | --- |
| Ctrl+C | 取消当前输入或生成 | 标准中断 |
| Ctrl+D | 退出 Claude Code 会话 | EOF 信号 |
| Ctrl+G | 在默认文本编辑器中打开 | 在默认文本编辑器中编辑您的提示或自定义响应 |
| Ctrl+L | 清除终端屏幕 | 保留对话历史 |
| Ctrl+O | 切换详细输出 | 显示详细的工具使用和执行情况 |
| Ctrl+R | 反向搜索命令历史 | 交互式搜索以前的命令 |
| Ctrl+V或Cmd+V（iTerm2）或Alt+V（Windows） | 从剪贴板粘贴图像 | 粘贴图像或图像文件的路径 |
| Ctrl+B | 后台运行任务 | 后台运行 bash 命令和代理。Tmux 用户按两次 |
| Left/Right arrows | 在对话框选项卡之间循环 | 在权限对话框和菜单中的选项卡之间导航 |
| Up/Down arrows | 导航命令历史 | 回忆以前的输入 |
| Esc+Esc | 回退代码/对话 | 将代码和/或对话恢复到之前的状态 |
| Shift+Tab或Alt+M（某些配置） | 切换权限模式 | 在自动接受模式、Plan Mode 和正常模式之间切换 |
| Option+P（macOS）或Alt+P（Windows/Linux） | 切换模型 | 在不清除提示的情况下切换模型 |
| Option+T（macOS）或Alt+T（Windows/Linux） | 切换扩展思考 | 启用或禁用扩展思考模式。首先运行/terminal-setup以启用此快捷键 |

| 快捷键 | 描述 | 上下文 |
| --- | --- | --- |
| Ctrl+K | 删除到行尾 | 存储已删除的文本以供粘贴 |
| Ctrl+U | 删除整行 | 存储已删除的文本以供粘贴 |
| Ctrl+Y | 粘贴已删除的文本 | 粘贴用Ctrl+K或Ctrl+U删除的文本 |
| Alt+Y（在Ctrl+Y之后） | 循环粘贴历史 | 粘贴后，循环浏览以前删除的文本。在 macOS 上需要将 Option 设置为 Meta |
| Alt+B | 将光标向后移动一个单词 | 单词导航。在 macOS 上需要将 Option 设置为 Meta |
| Alt+F | 将光标向前移动一个单词 | 单词导航。在 macOS 上需要将 Option 设置为 Meta |

| 快捷键 | 描述 | 上下文 |
| --- | --- | --- |
| Ctrl+T | 切换代码块的语法高亮 | 仅在/theme选择器菜单内工作。控制 Claude 响应中的代码是否使用语法着色 |

| 方法 | 快捷键 | 上下文 |
| --- | --- | --- |
| 快速转义 | \+Enter | 在所有终端中工作 |
| macOS 默认 | Option+Enter | macOS 上的默认设置 |
| Shift+Enter | Shift+Enter | 在 iTerm2、WezTerm、Ghostty、Kitty 中开箱即用 |
| 控制序列 | Ctrl+J | 多行的换行符 |
| 粘贴模式 | 直接粘贴 | 对于代码块、日志 |

Claude Code 的输入框不是纯聊天框，而是一个：

AI + 编辑器 + 命令调度器的融合终端

主要有三类前缀触发器：

/是 Claude Code 中触发内置命令/工具的核心符号，类似终端命令行的指令前缀，用于告诉 Claude 执行特定操作而非单纯生成文本。

核心用途：调用内置功能（如代码生成、文件操作、环境执行、插件调用等）。

/后紧跟命令关键词，空格后接参数（如文件名、执行命令、修复目标等），是 Claude Code 区分自然语言对话和代码操作指令的关键。

@后面跟文件名，会主动联想：

Claude 会把文件内容真实加载进推理上下文。

输入 ! 就会提示进入 Bash 命令模式：

Claude Code 为当前会话维护命令历史：

搜索显示匹配的命令，搜索词突出显示，使您可以轻松找到并重用以前的输入。

Claude Code 支持在后台运行 bash 命令，允许您在长时间运行的进程执行时继续工作。

当 Claude Code 在后台运行命令时，它异步运行命令并立即返回后台任务 ID。Claude Code 可以在命令继续在后台执行时响应新提示。

要在后台运行命令，您可以：

这对于快速 shell 操作同时保持对话上下文很有用。

语法高亮仅在 Claude Code 的原生构建中可用。

Claude Code 操作说明
Claude Code 的输入框不是纯聊天框，而是一个：
AI + 编辑器 + 命令调度器的融合终端
主要有三类前缀触发器：
本质作用
Command（命令）
执行内置操作
Context（上下文）
引用文件/代码/目录
Bash 模式
直接执行终端命令，stdout/stderr 自动注入上下文
Memory（记忆注入）
把内容持久写入 CLAUDE.md 项目记忆，跨会话长期生效，例如：
#config.yaml
Async（异步任务）
后台/云端异步执行任务，不阻塞当前会话，可关闭终端后在 claude.ai/code 查看进度
+Enter
Multiline（多行输入）
换行不发送，写多行内容，长需求描述一次性写完
自然语言
普通任务指令
—— 操作型命令（最重要）
是 Claude Code 中触发内置命令
工具的核心符号，类似终端命令行的指令前缀，用于告诉 Claude 执行特定操作而非单纯生成文本。
**核心用途：**
调用内置功能（如代码生成、文件操作、环境执行、插件调用等）。
后紧跟命令关键词，空格后接参数（如文件名、执行命令、修复目标等），是 Claude Code 区分
**自然语言对话**
**代码操作指令**
的关键。
会弹出命令列表:
![](https://www.runoob.com/wp-content/uploads/2026/01/23e5a097-f781-4f4b-8597-35d18a7aae29.png)
常见高频命令：
/help
查看全部能力
/clear
清空对话
/plan
进入规划模式
/model
切换模型
/context
查看上下文使用情况
/export
导出对话
/status
环境状态
/tasks
管理后台任务
/theme
主题切换
/memory
编辑 CLAUDE.md
//plan 实现一个用户登录模块
—— 上下文注入
后面跟文件名，会主动联想：
![](https://www.runoob.com/wp-content/uploads/2026/01/f6f417b7-0f60-4e73-97ec-0e09380f590d.png)
引用单文件:
@main.py 帮我检查 bug
![](https://www.runoob.com/wp-content/uploads/2026/01/9b1aac90-b242-468d-b25f-c581e648bb72.png)
引用多个文件:
@main.py @main2.py 这两个是否有重复逻辑？
引用整个目录使用
@ + 目录路径
@src/ 分析项目结构并给出优化建议
引用错误日志：
@npm-debug.log 找出失败原因
Claude 会把文件内容真实加载进推理上下文。
-- Bash 命令
通过在输入前加上
直接运行 bash 命令，无需通过 Claude，格式为：
! + Bash 命令
输入 ! 就会提示进入 Bash 命令模式：
![](https://www.runoob.com/wp-content/uploads/2026/01/f0a9cb66-6ae1-48c4-8fc3-2f00ff5d9c6e-1.png)
例如查看当前的目录：
! ls -la
![](https://www.runoob.com/wp-content/uploads/2026/01/ed966407-b7e5-4a81-b646-738624109e68-1.png)
Vim 编辑器模式
/vim
命令启用 vim 风格编辑，或通过
/config
永久配置。
模式切换
来自模式
进入 NORMAL 模式
INSERT
在光标前插入
NORMAL
在行首插入
NORMAL
在光标后插入
NORMAL
在行尾插入
NORMAL
在下方打开行
NORMAL
在上方打开行
NORMAL
导航（NORMAL 模式）
向左/下/上/右移动
下一个单词
单词末尾
上一个单词
第一个非空白字符
输入开始
输入结束
f{char}
跳转到下一个字符出现处
F{char}
跳转到上一个字符出现处
t{char}
跳转到下一个字符出现处之前
T{char}
跳转到上一个字符出现处之后
重复最后一个 f/F/t/T 动作
反向重复最后一个 f/F/t/T 动作
编辑（NORMAL 模式）
删除字符
删除到行尾
删除单词/到末尾/向后
更改到行尾
更改单词/到末尾/向后
复制（yank）行
复制单词/到末尾/向后
在光标后粘贴
在光标前粘贴
取消缩进行
重复最后一个更改
文本对象（NORMAL 模式）
文本对象与
等运算符一起工作：
内部/周围单词
内部/周围 WORD（空格分隔）
内部/周围双引号
内部/周围单引号
内部/周围括号
内部/周围方括号
内部/周围花括号
命令历史
Claude Code 为当前会话维护命令历史：
历史按工作目录存储
/clear
命令清除
使用上/下箭头导航（请参阅上面的键盘快捷键）
**注意**
：历史扩展（
）默认禁用
使用 Ctrl+R 反向搜索
Ctrl+R
交互式搜索您的命令历史：
**开始搜索**
Ctrl+R
激活反向历史搜索
**键入查询**
：输入文本以在以前的命令中搜索 - 搜索词将在匹配结果中突出显示
**导航匹配**
：再次按
Ctrl+R
循环浏览较旧的匹配
**接受匹配**
接受当前匹配并继续编辑
Enter
接受并立即执行命令
**取消搜索**
Ctrl+C
取消并恢复原始输入
在空搜索上按
Backspace
搜索显示匹配的命令，搜索词突出显示，使您可以轻松找到并重用以前的输入。
后台 bash 命令
Claude Code 支持在后台运行 bash 命令，允许您在长时间运行的进程执行时继续工作。
后台运行的工作原理
当 Claude Code 在后台运行命令时，它异步运行命令并立即返回后台任务 ID。Claude Code 可以在命令继续在后台执行时响应新提示。
要在后台运行命令，您可以：
提示 Claude Code 在后台运行命令
按 Ctrl+B 将常规 Bash 工具调用移到后台。（Tmux 用户必须按两次 Ctrl+B，因为 tmux 的前缀键。）
**主要功能：**
输出被缓冲，Claude 可以使用 TaskOutput 工具检索它
后台任务具有用于跟踪和输出检索的唯一 ID
当 Claude Code 退出时，后台任务会自动清理
要禁用所有后台任务功能，请将
CLAUDE_CODE_DISABLE_BACKGROUND_TASKS
环境变量设置为
**常见后台命令：**
构建工具（webpack、vite、make）
包管理器（npm、yarn、pnpm）
测试运行器（jest、pytest）
开发服务器
长时间运行的进程（docker、terraform）
前缀的 Bash 模式
通过在输入前加上
直接运行 bash 命令，无需通过 Claude：
! npm test
! git status
! ls -la
Bash 模式：
将命令及其输出添加到对话上下文
显示实时进度和输出
支持相同的
Ctrl+B
后台运行长时间运行的命令
不需要 Claude 解释或批准命令
支持基于历史的自动完成：键入部分命令并按
**Tab**
从当前项目中的以前的
命令完成
这对于快速 shell 操作同时保持对话上下文很有用。
按键说明
常规控制
Ctrl+C
取消当前输入或生成
标准中断
Ctrl+D
退出 Claude Code 会话
EOF 信号
Ctrl+G
在默认文本编辑器中打开
在默认文本编辑器中编辑您的提示或自定义响应
Ctrl+L
清除终端屏幕
保留对话历史
Ctrl+O
切换详细输出
显示详细的工具使用和执行情况
Ctrl+R
反向搜索命令历史
交互式搜索以前的命令
Ctrl+V
Cmd+V
（iTerm2）或
Alt+V
（Windows）
从剪贴板粘贴图像
粘贴图像或图像文件的路径
Ctrl+B
后台运行任务
后台运行 bash 命令和代理。Tmux 用户按两次
Left/Right arrows
在对话框选项卡之间循环
在权限对话框和菜单中的选项卡之间导航
Up/Down arrows
导航命令历史
回忆以前的输入
回退代码/对话
将代码和/或对话恢复到之前的状态
Shift+Tab
Alt+M
（某些配置）
切换权限模式
在自动接受模式、Plan Mode 和正常模式之间切换
Option+P
（macOS）或
Alt+P
（Windows/Linux）
切换模型
在不清除提示的情况下切换模型
Option+T
（macOS）或
Alt+T
（Windows/Linux）
切换扩展思考
启用或禁用扩展思考模式。首先运行
/terminal-setup
以启用此快捷键
文本编辑
Ctrl+K
删除到行尾
存储已删除的文本以供粘贴
Ctrl+U
删除整行
存储已删除的文本以供粘贴
Ctrl+Y
粘贴已删除的文本
Ctrl+K
Ctrl+U
删除的文本
Alt+Y
Ctrl+Y
循环粘贴历史
粘贴后，循环浏览以前删除的文本。在 macOS 上需要
[将 Option 设置为 Meta](#keyboard-shortcuts)
Alt+B
将光标向后移动一个单词
单词导航。在 macOS 上需要
[将 Option 设置为 Meta](#keyboard-shortcuts)
Alt+F
将光标向前移动一个单词
单词导航。在 macOS 上需要
[将 Option 设置为 Meta](#keyboard-shortcuts)
主题和显示
Ctrl+T
切换代码块的语法高亮
/theme
选择器菜单内工作。控制 Claude 响应中的代码是否使用语法着色
语法高亮仅在 Claude Code 的原生构建中可用。
多行输入
快速转义
Enter
在所有终端中工作
macOS 默认
Option+Enter
macOS 上的默认设置
Shift+Enter
Shift+Enter
在 iTerm2、WezTerm、Ghostty、Kitty 中开箱即用
控制序列
Ctrl+J
多行的换行符
粘贴模式
直接粘贴
对于代码块、日志
Shift+Enter 在 iTerm2、WezTerm、Ghostty 和 Kitty 中无需配置即可工作。对于其他终端（VS Code、Alacritty、Zed、Warp），运行
/terminal-setup
以安装绑定。