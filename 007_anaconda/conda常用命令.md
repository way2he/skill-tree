# Conda 常用命令手册

## 一、简介
Conda 是一个开源的包管理系统和环境管理系统，用于安装多个版本的软件包及其依赖关系，并在它们之间轻松切换。它是 Anaconda 和 Miniconda 的核心组件。

## 二、基础命令

### 2.1 版本信息
```bash
conda --version  # 查看 conda 版本
conda info       # 查看 conda 详细信息
```

### 2.2 更新与升级
```bash
conda update conda        # 更新 conda 本身
conda update --all        # 更新所有已安装的包
conda upgrade <package>   # 升级指定包
```

## 三、环境管理

### 3.1 创建环境
```bash
conda create --name <env_name>                # 创建指定名称的环境
conda create --name <env_name> python=3.8      # 创建指定 Python 版本的环境
conda create --name <env_name> <package1> <package2>  # 创建包含指定包的环境
```

### 3.2 查看环境
```bash
conda env list            # 列出所有环境
conda info --envs         # 查看所有环境的详细信息
```

### 3.3 激活与退出环境
```bash
# Windows 系统
activate <env_name>

# Linux/MacOS 系统
source activate <env_name>

# 退出当前环境
conda deactivate
```

### 3.4 复制与删除环境
```bash
conda create --name <new_env> --clone <old_env>  # 复制环境
conda remove --name <env_name> --all             # 删除环境
```

### 3.5 升级环境中的Python版本
要升级现有conda环境中的Python版本，请按照以下步骤操作：

1. 首先激活目标环境：
```bash
# Windows系统
activate <env_name>

# Linux/MacOS系统
source activate <env_name>
```

2. 执行升级命令，指定目标Python版本：
```bash
conda install python=<target_version>
```

例如，要将Python升级到3.9版本：
```bash
conda install python=3.9
```

> **注意事项**：
> - 升级Python版本可能会导致某些依赖包不兼容，请在升级前备份环境。
> - 建议创建新环境并指定所需Python版本，而不是升级现有环境。

### 3.6 导出与导入环境
```bash
conda env export > environment.yml  # 导出环境到 YAML 文件
```
conda remove --name <env_name> --all             # 删除环境
```

### 3.5 导出与导入环境
```bash
conda env export > environment.yml  # 导出环境到 YAML 文件
conda env create -f environment.yml # 从 YAML 文件创建环境
```

## 四、包管理

### 4.1 安装包
```bash
conda install <package>                  # 安装指定包
conda install <package>=<version>        # 安装指定版本的包
conda install -n <env_name> <package>    # 为指定环境安装包
conda install --channel <channel> <package>  # 从指定通道安装包
```

### 4.2 查看已安装包
```bash
conda list                      # 列出当前环境的所有包
conda list -n <env_name>        # 列出指定环境的所有包
conda list <package>            # 查看指定包的信息
```

### 4.3 更新与卸载包
```bash
conda update <package>          # 更新指定包
conda remove <package>          # 卸载指定包
conda remove -n <env_name> <package>  # 卸载指定环境的包
```

### 4.4 搜索包
```bash
conda search <package>          # 搜索包
conda search --channel <channel> <package>  # 从指定通道搜索包
```

## 五、通道管理
通道是 conda 包的来源，可以理解为软件仓库。

### 5.1 添加通道
```bash
conda config --add channels <channel_name>  # 添加通道
conda config --add channels conda-forge     # 常用通道示例：conda-forge
```

### 5.2 查看通道
```bash
conda config --show channels  # 查看所有通道
```

### 5.3 删除通道
```bash
conda config --remove channels <channel_name>  # 删除通道
```

### 5.4 设置通道优先级
```bash
conda config --set channel_priority strict  # 设置严格的通道优先级
```

## 六、高级用法

### 6.1 清理缓存
```bash
conda clean --all  # 清理所有缓存
conda clean --tarballs  # 仅清理包缓存
```

### 6.2 查找包的依赖关系
```bash
conda depends <package>  # 查看包的依赖关系
```

### 6.3 查看包的详细信息
```bash
conda search <package> --info  # 查看包的详细信息
```

### 6.4 导出环境中的包列表
```bash
conda list --export > requirements.txt  # 导出包列表到文本文件
```

### 6.5 从文本文件安装包
```bash
conda install --file requirements.txt  # 从文本文件安装包
```

## 七、常见问题解决

### 7.1 网络问题
如果遇到网络连接问题，可以尝试更换镜像源：
```bash
# 添加清华镜像源
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/

# 设置显示通道地址
conda config --set show_channel_urls yes
```

### 7.2 包冲突问题
尝试创建新环境并安装所需包，或使用 `conda install` 时添加 `--no-pin` 参数。

### 7.3 权限问题
在 Linux/MacOS 系统中，可能需要使用 `sudo` 命令获取管理员权限。

## 八、快捷键
- `conda -h` 或 `conda --help`: 查看 conda 帮助信息
- `conda <command> -h`: 查看指定命令的帮助信息

## conda如何查看已经安装的指定包

要查看在conda环境中已经安装的指定包，可以使用以下命令：

- `conda list <package_name>`: 查看指定包是否已安装及其版本
  示例：`conda list numpy`

- `conda list | findstr <package_name>`: 在Windows系统中过滤特定包（使用findstr命令）
  示例：`conda list | findstr pandas`

- `conda list | grep <package_name>`: 在Linux/Mac系统中过滤特定包（使用grep命令）
  示例：`conda list | grep tensorflow`

- `conda list -n <env_name> <package_name>`: 查看指定环境中是否安装了特定包
  示例：`conda list -n myenv scikit-learn`

- `conda info --envs`: 先查看所有可用的环境

- `conda list --show-channel-urls`: 查看已安装包及其来源渠道
  示例：`conda list --show-channel-urls numpy`