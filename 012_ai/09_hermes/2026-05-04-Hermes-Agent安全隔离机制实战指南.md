---
name: Hermes Agent安全隔离机制实战指南
description: Hermes Agent从入门到精通，Profile多账号隔离与Docker沙箱机制完全解析，实现多人共用不打架、AI犯错不炸硬盘
type: reference
tags: ['wechat', 'article', 'Hermes', 'Agent', '安全', '隔离', 'Docker', '多账号']
source: wechat
account: 小飞哥的秘书
author: 小飞哥的秘书
original_url: https://mp.weixin.qq.com/s/DrdgcuAYl034j7ZGEjjxAA
publish_time: 2026-05-04
download_time: 2026-05-10 20:26:02
image_count: 0
summary: Hermes Agent从入门到精通系列，详解Profile多账号隔离与Docker沙箱两种安全机制，实现多人共用不打架、AI犯错不炸硬盘。
created_at: 2026-05-10
updated_at: 2026-05-10
---

# 

> Source: **Unknown Account** Official Account
> Author: 小飞哥的秘书小飞哥的秘书
> Publish Time: 2026-05-04
> Original URL: [https://mp.weixin.qq.com/s/DrdgcuAYl034j7ZGEjjxAA](https://mp.weixin.qq.com/s/DrdgcuAYl034j7ZGEjjxAA)

---


# 《Hermes Agent 从入门到精通》安全隔离机制实战指南

> 看完这篇，你会用两条命令实现：多人共用不打架、AI 犯错不炸硬盘。

* * *

## Hermes 的两种隔离机制

Hermes Agent 提供了两层「安全网」，解决两类完全不同的问题：

  
| Profile 多账号| Docker 沙箱  
---|---|---  
**解决的问题**|  多人共用，数据打架| AI 执行危险命令  
**隔离什么**|  配置、密钥、聊天记录、技能| 文件系统、网络、进程  
**类比**|  浏览器多用户资料| 给水电工单独的工具棚  
**一句话命令**| ` hermes profile create`| `hermes config set terminal.backend docker`  
  
**什么时候用 Profile？**

  * 团队共用一台服务器，每人要独立配置
  * 公司和个人的 API key 要分开
  * 多个客户项目，各用各的模型和密钥
  * 飞书/Telegram/Discord 网关需要独立运行

**什么时候用 Docker 沙箱？**

  * 执行用户提交的代码或第三方脚本
  * 审查含敏感数据的内部代码
  * 让 AI 跑自动化任务，不想它碰到重要文件
  * 日常开发也想多一层保护

**两者可以叠加使用** ——每个 Profile 独立配置自己的沙箱策略，一个用严格模式跑不信任代码，另一个用开发模式日常编码。

* * *

## 第一章：Profile —— 一台机器，N 个独立账号

### 1.1 这能解决什么问题？

你有一台服务器，上面跑着 Hermes。三个人要用：

  * 你用它做日常开发
  * 同事用它管飞书公众号
  * 实习生用它学习和实验

如果三个人共用一套配置——同事的飞书密钥会被实习生看到，你的聊天记录混进别人的 session，API 费用算在一个人头上。

**Profile 就是把一个 Hermes「分身」成多个独立账号** ，每个账号有自己的配置、密钥、聊天记录、技能库，谁也看不到谁的。

你还可以作为**管理员** ，随时查看、备份、删除任何一个账号。

* * *

### 1.2 第一步：看看你现在有哪些账号

打开终端，输入：
    
    
    hermes profile list  
    

你会看到：
    
    
      Profile          Model                     Gateway      Alias  
      ───────────────   ───────────────────────   ───────────  ────────────  
       default         MiniMax-M2.7-highspeed    stopped      —  
      ◆feishu_product  —                         running      —  
    

  * `default` 是装好 Hermes 就有的，不用管
  * `feishu_product` 是我手动建的，正在跑飞书网关
  * `◆` 指着当前激活的账号

* * *

### 1.3 第二步：给每个人建账号
    
    
    hermes profile create zhangsan  
    

回车后输出：
    
    
    Profile 'zhangsan' created at ~/.hermes/profiles/zhangsan  
    89 bundled skills synced.  
    

这行命令干了什么？它在 `~/.hermes/profiles/` 下面生成了一个全新的目录：
    
    
    ~/.hermes/profiles/zhangsan/  
    ├── config.yaml       ← 空白配置，等着你填  
    ├── .env              ← 空白密钥文件  
    ├── skills/           ← 89 个内置技能  
    ├── sessions/         ← 聊天记录（空的）  
    └── logs/             ← 日志（空的）  
    

继续给其他人建：
    
    
    hermes profile create lisi  
    hermes profile create wangwu  
    

全部建完后再看一眼：
    
    
    hermes profile list  
    
    
    
      Profile          Model      Gateway      Alias  
      ───────────────   ────────   ───────────  ────────────  
       default          ...        stopped      —  
      ◆feishu_product   —          running      —  
       zhangsan         —          stopped      —  
       lisi             —          stopped      —  
       wangwu           —          stopped      —  
    

现在你有 5 个独立账号了。

* * *

### 1.4 第三步：各自配自己的东西

**张三配他的模型和 API Key：**
    
    
     hermes -p zhangsan config set model.default "claude-sonnet-4"  
    hermes -p zhangsan config set ANTHROPIC_API_KEY "sk-ant-zhangsan-xxxx"  
    

输出：`✓ Set model.default = claude-sonnet-4`

**李四配他的：**
    
    
     hermes -p lisi config set model.default "deepseek-v3"  
    hermes -p lisi config set DEEPSEEK_API_KEY "sk-deepseek-lisi-xxxx"  
    

* * *

### 1.5 第四步：验证隔离 —— 亲眼看到互不干扰

**验证一：配置隔离**
    
    
     # 在张三的账号里查  
    hermes -p zhangsan config 2>&1 | grep "Model"  
    

输出：
    
    
    ◆ Model  
      Model:        claude-sonnet-4       ← 张三的  
    
    
    
    # 在李四的账号里查  
    hermes -p lisi config 2>&1 | grep "Model"  
    

输出：
    
    
    ◆ Model  
      Model:        deepseek-v3           ← 李四的，完全独立  
    

张三看不到李四的模型配置，李四也看不到张三的。

**验证二：文件隔离**
    
    
     # 张三在自己的目录下放个文件  
    echo "zhangsan-secret" > ~/.hermes/profiles/zhangsan/secret.txt  
      
    # 张三能看到  
    ls ~/.hermes/profiles/zhangsan/secret.txt  
    # → secret.txt  ✅  
      
    # 李四看不到  
    ls ~/.hermes/profiles/lisi/secret.txt  
    # → No such file or directory  ❌  
    

**验证三：聊天记录隔离**

张三和李四各自用 `hermes -p zhangsan chat` 和 `hermes -p lisi chat` 聊过的天，session 文件存在各自的 `sessions/` 目录下，互相完全看不到。

* * *

### 1.6 管理员操作：统一管理所有账号

你是管理员，不需要切进每个账号就能操作：
    
    
    # 查看所有账号状态  
    hermes profile list  
      
    # 查看某个账号的详细信息（模型、技能数、网关状态）  
    hermes profile show zhangsan  
      
    # 备份某个账号（导出为压缩包）  
    hermes profile export zhangsan -o zhangsan-backup.tar.gz  
      
    # 从备份恢复  
    hermes profile import zhangsan-backup.tar.gz  
      
    # 给账号改名  
    hermes profile rename zhangsan zhang-san  
      
    # 删除不再需要的账号  
    hermes profile delete wangwu  
    

* * *

### 1.7 每个人怎么用自己的账号？
    
    
    # 粘性切换：切一次，之后所有命令默认走这个账号  
    hermes profile use zhangsan  
      
    # 之后直接用  
    hermes chat                           # 聊天  
    hermes config                         # 看配置  
    hermes tools list                     # 看工具  
      
    # 临时切换：不改变默认，仅这一次命令用  
    hermes -p lisi chat -q "帮我查个资料"  
    

* * *

### 1.8 想让所有人共享同一套技能？

每个账号默认有自己独立的 `skills/`。如果想让所有人共用：
    
    
    # 在某个账号的配置里加一行  
    hermes -p zhangsan config set skills.external_dirs '["~/.hermes/skills"]'  
    

这样张三的账号也能用 default 账号里安装的技能了。

* * *

### 1.9 第一章速查卡
    
    
    # 管理员  
    hermes profile list                     # 看所有账号  
    hermes profile create <名字>            # 建账号  
    hermes profile show <名字>              # 看详情  
    hermes profile export <名字> -o x.tar.gz # 备份  
    hermes profile import x.tar.gz          # 恢复  
    hermes profile rename <旧> <新>         # 改名  
    hermes profile delete <名字>            # 删号  
      
    # 用户  
    hermes profile use <名字>               # 登录  
    hermes -p <名字> chat                   # 聊天  
    hermes -p <名字> config                 # 看配置  
    

* * *

## 第二章：Docker 沙箱 —— Agent 跑在容器里

### 2.1 为什么需要沙箱？先做个对比实验

**实验 A：默认 local 模式**

你当前的 Hermes 跑在什么环境里？
    
    
    hermes config 2>&1 | grep -A 3 "Terminal"  
    

输出：
    
    
    ◆ Terminal  
      Backend:      local  
      Working dir:  .  
      Timeout:      180s  
    

`local` 的意思就是 Agent 的 Shell 命令**直接在你的电脑上跑** 。试一下：
    
    
    hermes chat -q "在桌面创建一个文件 test-local.txt"  
    

你会在桌面上真的看到这个文件。Agent 的 `rm`、`curl`、`pip install`，全都在宿主机上生效。

**实验 B：Docker 沙箱模式**

切换到 Docker 后再试同样的操作——文件不会出现在桌面，它被关在容器里了。

这就是沙箱的意义：**Agent 能干的事，不超出你划的边界。**

* * *

###  2.2 Docker 沙箱到底隔离了什么？

Hermes 启动的 Docker 容器自动带了一整套安全限制：

  * 容器内即使是 root，也对宿主机没有任何管理权限
  * 容器内的程序不能提权（就算有 suid 文件也没用）
  * 最多同时跑 256 个进程，防止 Agent 搞出 fork 炸弹
  * `/tmp`、`/var/tmp`、`/run` 这些临时目录禁止执行程序，防止恶意二进制落地
  * `/tmp` 容量限制在 512MB，防止写爆磁盘

这些限制是 Hermes **自动加上的，你不用手动配** 。你只需要决定：给容器开多大的口子。

* * *

### 2.3 全程操作：开启 Docker 沙箱

**第一步：确认 Docker 已安装**
    
    
     docker --version  
    

如果显示版本号就 OK。没装的话去 docker.com[1] 下载。用 Podman 的话也可以。

**第二步：切换到 Docker**
    
    
     hermes config set terminal.backend docker  
    

输出：`✓ Set terminal.backend = docker`

**第三步：指定用什么镜像**
    
    
     hermes config set terminal.docker.image "ubuntu:22.04"  
    

输出：`✓ Set terminal.docker.image = ubuntu:22.04`

**第四步：加上资源限制**
    
    
     hermes config set terminal.docker.memory 1024  
    hermes config set terminal.docker.cpu 1.0  
    

**第五步：验证配置已生效**
    
    
     hermes config 2>&1 | grep -A 10 "Terminal"  
    

确认看到 `Backend: docker`。

* * *

### 2.4 验证沙箱真的在起作用
    
    
    # 让 Agent 在容器里建个文件  
    hermes chat -q "在根目录下创建一个文件 /i-am-in-container.txt"  
    

Agent 回复「创建成功」。

你去宿主机上找：
    
    
    ls /i-am-in-container.txt  
    # → No such file or directory     ← 宿主机上没有！  
    

文件被关在容器里了。你再试试 `rm`、`apt install`、`curl`——全部只影响容器，宿主机毫发无伤。

* * *

### 2.5 想让 Agent 访问你的项目文件？

完全隔离有时候不方便——你让 Agent 改代码，它得能看到代码才行。这时候**挂载目录** ：
    
    
    # 方式一：把指定目录挂进容器的 /workspace  
    hermes config set terminal.docker.volumes '["/Users/yuesf/my-project:/workspace"]'  
      
    # 方式二：自动挂载当前工作目录（更方便）  
    hermes config set terminal.docker.auto_mount_cwd true  
    

**黄金原则** ：只挂必要的目录。如果挂整个 `$HOME`，就相当于没隔离。

* * *

### 2.6 实操：配出三种不同安全级别

根据你的使用场景，选一种照着敲：

#### 🔴 严格模式 —— 跑不信任的代码
    
    
    hermes config set terminal.backend docker  
    hermes config set terminal.docker.image "ubuntu:22.04"  
    hermes config set terminal.docker.network false  
    hermes config set terminal.docker.memory 512  
    hermes config set terminal.docker.cpu 0.5  
    hermes config set terminal.docker.persistent_filesystem false  
    

效果：Agent 断网、最多用 512MB 内存和半核 CPU、用完容器直接销毁。跑任何东西都伤不到宿主机。

#### 🟡 审计模式 —— 审查敏感代码
    
    
    hermes config set terminal.backend docker  
    hermes config set terminal.docker.image "ubuntu:22.04"  
    hermes config set terminal.docker.volumes '["/data/project:/workspace:ro"]'  
    hermes config set terminal.docker.network false  
    hermes config set terminal.docker.memory 1024  
    

效果：Agent 能看到项目文件（只读），但不能改、不能联网外传。适合审查含敏感数据的内部代码。

#### 🟢 开发模式 —— 日常编码
    
    
    hermes config set terminal.backend docker  
    hermes config set terminal.docker.image "ubuntu:22.04"  
    hermes config set terminal.docker.auto_mount_cwd true  
    hermes config set terminal.docker.persistent_filesystem true  
    hermes config set terminal.docker.memory 2048  
    

效果：Agent 能访问当前项目目录、能联网查资料、容器持久化（pip install 过的包下次还在）。

* * *

### 2.7 三种模式对比

你想...| 用哪种| 联网| 文件| 持久化  
---|---|---|---|---  
跑第三方脚本| 🔴 严格| ❌| ❌| ❌  
审内部代码| 🟡 审计| ❌| 只读| ✅  
日常写代码| 🟢 开发| ✅| 读写| ✅  
  
* * *

### 2.8 进阶一：给容器设环境变量

如果你的项目需要特定环境变量（比如 `DATABASE_URL`）：
    
    
    hermes config set terminal.docker.env '{"DATABASE_URL": "postgres://localhost/db", "NODE_ENV": "production"}'  
    

Agent 在容器里跑的时候，这些环境变量自动可用。

* * *

### 2.9 进阶二：用 Podman 替代 Docker

不用 Docker、用 Podman 的话：
    
    
    export HERMES_DOCKER_BINARY=podman  
    hermes config set terminal.backend docker  
    

Hermes 会自动用 podman 来启动容器。

* * *

### 2.10 完整配置项速查表

以下每个配置都能用 `hermes config set <键> <值>` 来设：

配置键| 用途| 示例值  
---|---|---  
`terminal.backend`| 切换后端| `docker` / `local` / `ssh`  
`terminal.docker.image`| 容器镜像| `"ubuntu:22.04"`  
`terminal.docker.cpu`| CPU 限制（核）| `1.0`  
`terminal.docker.memory`| 内存限制（MB）| `1024`  
`terminal.docker.disk`| 磁盘限制（MB）| `4096`  
`terminal.docker.network`| 是否联网| `true` / `false`  
`terminal.docker.volumes`| 挂载目录| `'["/host:/container"]'`  
`terminal.docker.env`| 环境变量| `'{"KEY":"val"}'`  
`terminal.docker.forward_env`| 透传宿主机变量| `'["PATH","HOME"]'`  
`terminal.docker.persistent_filesystem`| 保留容器| `true` / `false`  
`terminal.docker.auto_mount_cwd`| 自动挂载当前目录| `true` / `false`  
`terminal.docker.run_as_host_user`| 以宿主机用户运行| `true` / `false`  
`terminal.docker.timeout`| 命令超时（秒）| `300`  
`terminal.docker.cwd`| 容器内工作目录| `"/workspace"`  
  
* * *

### 2.11 第二章速查卡
    
    
    # 开关  
    hermes config set terminal.backend docker    # 开沙箱  
    hermes config set terminal.backend local     # 关沙箱（回本地）  
      
    # 安全三连  
    hermes config set terminal.docker.network false  
    hermes config set terminal.docker.memory 512  
    hermes config set terminal.docker.persistent_filesystem false  
      
    # 日常开发  
    hermes config set terminal.docker.auto_mount_cwd true  
    hermes config set terminal.docker.persistent_filesystem true  
      
    # 检查当前模式  
    hermes config 2>&1 | grep Backend  
    

* * *

## 总结：Profile vs Docker 沙箱 —— 到底用哪个？

维度| Profile 多账号| Docker 沙箱  
---|---|---  
**隔离层级**|  用户空间级| 操作系统级  
**隔离范围**|  配置、密钥、会话、技能| 文件系统、网络、进程、资源  
**安全强度**|  ⭐⭐ 防止数据混淆| ⭐⭐⭐⭐⭐ 内核级容器隔离  
**性能开销**|  零开销| 容器启动约 2-5 秒  
**操作复杂度**|  两条命令| 三到五条命令  
**能否叠加**|  ✅ 每个 Profile 可独立配沙箱| ✅  
  
**一句话决策：**
    
    
     你的问题是「谁的东西跟谁的混了」？ → Profile  
    你的问题是「Agent 会不会把系统搞坏」？ → Docker 沙箱  
    两者都有？                                 → Profile + Docker 沙箱一起用  
    

**最佳实践** ：生产环境给每个用户建独立 Profile，每个 Profile 里把 `terminal.backend` 设为 `docker`。这样谁的数据都不混、谁的代码都碰不到宿主机——双保险。

* * *

> 📱 添加微信号 **ysf99918** ，（备注hermes）加入交流群。