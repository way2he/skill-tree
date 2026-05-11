Cluade Code 中，CLAUDE.md 终端额内容就相当于是系统提示词。
Cluade Code 在开始对话的时候会自动读取CLAUDE.md 作为上下文。
也就是说，CLAUDE.md文件是我们来自定义项目的上下文的地方，相当于是项目开发的配置文件。

CLAUDE.md 中通常包含以下内容：
- 开发环境（pyenv、编译器）与 常用 Bash 命令；
- 核心文件和实用函数；
- 代码风格指南（变量、文件命名），代码库规范（分支命名、合并等）；
- 测试说明项目特有的任何意外行为与警告；
- 您希望Cluade 记住的其他信息

| 优先级 | 路径 | Windows 实际位置 | 说明 |
| --- | --- | --- | --- |
| 1 | ./CLAUDE.md | D:\Projects\my-project\CLAUDE.md | 项目根目录（推荐，可提交到 git） |
| 2 | ./CLAUDE.local.md | D:\Projects\my-project\CLAUDE.local.md | 项目本地（不提交到 git） |
| 3 | ~/.claude/CLAUDE.md | C:\Users\YourName\.claude\CLAUDE.md | 全局配置 |
| 4 | 父目录 | 自动向上查找 | 父目录中的也会被读取 |

```markdown
# 项目说明
这是一个 TypeScript + React 项目，使用 Vite 构建。

# 代码规范
- 使用 ESLint 和 Prettier
- 组件使用函数式写法
- 测试文件放在 __tests__ 目录

# 常用命令
- npm run dev: 启动开发服务器
- npm run test: 运行测试
- npm run build: 构建生产版本

# 重要提示
IMPORTANT: 所有 API 请求必须经过 src/api/request.ts 封装
YOU MUST: 新增组件需要同时编写单元测试
```
**优化技巧：使用 “IMPORTANT” 或 “YOU MUST” 等强调词可以提高 Claude 的遵循度。**

