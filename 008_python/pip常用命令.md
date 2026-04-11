# Pip 常用命令手册

## 一、简介
Pip 是 Python 的包安装和管理工具，用于安装、升级、卸载 Python 包。

## 二、基础命令

### 2.1 版本信息
```bash
pip --version  # 查看 pip 版本
pip show pip   # 查看 pip 详细信息
```

### 2.2 更新 pip
```bash
pip install --upgrade pip  # 更新 pip 本身
```

## 三、包管理

### 3.1 安装包
```bash
pip install <package>                  # 安装指定包
pip install <package>==<version>        # 安装指定版本的包
pip install "<package>>=<min_version>"  # 安装不低于指定版本的包
pip install -r requirements.txt         # 从文件安装多个包
```

### 3.2 查看已安装包
```bash
pip list                      # 列出当前环境的所有包
pip list --outdated           # 列出可更新的包
pip show <package>            # 查看指定包的详细信息
```

### 3.3 查看安装包数量
```bash
# Windows系统：查看当前环境安装包数量
pip list | find /c /v ""

# Linux/Mac系统：查看当前环境安装包数量
pip list | wc -l
```

### 3.4 更新与卸载包
```bash
pip install --upgrade <package>  # 更新指定包
pip uninstall <package>          # 卸载指定包
pip uninstall -r requirements.txt  # 从文件卸载多个包
```

### 3.5 搜索包
```bash
pip search <package>          # 搜索包（部分版本已移除该功能）
```

### 3.6 查看当前python地址
```bash
python -c "import sys; print(sys.executable)"
```

## 四、高级用法

### 4.1 导出包列表
```bash
pip freeze > requirements.txt  # 导出当前环境的包列表
pip list --format=freeze > requirements.txt  # 同上
```

### 4.2 安装开发版本
```bash
pip install -e .              # 以开发模式安装当前目录的包
pip install git+<repository_url>  # 从 Git 仓库安装包
```

### 4.3 更改源
```bash
# 临时使用国内源安装包
pip install <package> -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 永久设置国内源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 4.4 清理缓存
```bash
pip cache purge  # 清理所有缓存
```

## 五、常见问题解决

### 5.1 权限问题
在 Linux/MacOS 系统中，可能需要使用 `sudo` 命令获取管理员权限，或使用 `--user` 参数安装到用户目录：
```bash
pip install <package> --user
```

### 5.2 代理问题
如果需要通过代理安装包，可以使用以下命令：
```bash
pip install <package> --proxy http://proxy.example.com:8080
```

### 5.3 包冲突问题
尝试使用虚拟环境（如 venv 或 conda）隔离不同项目的依赖。

## 六、快捷键
- `pip -h` 或 `pip --help`: 查看 pip 帮助信息
- `pip <command> -h`: 查看指定命令的帮助信息


