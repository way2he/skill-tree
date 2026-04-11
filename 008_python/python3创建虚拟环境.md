# Python3 创建虚拟环境

在Python 3.10及以上版本中，创建虚拟环境主要有两种方法：使用内置的`venv`模块或第三方工具`virtualenv`。

## 方法一：使用内置的venv模块

`venv`是Python 3.3+内置的虚拟环境工具，无需额外安装。在Windows 11上的操作步骤如下：

1. **打开命令提示符或PowerShell**
   - 按`Win + R`，输入`cmd`或`powershell`，回车

2. **导航到项目目录**
   ```bash
   cd C:\path\to\your\project
   ```

3. **创建虚拟环境**
   ```bash
   python -m venv venv_name
   ```
   其中`venv_name`是你想要的虚拟环境名称，通常命名为`venv`或`.venv`

4. **激活虚拟环境**
   - 在命令提示符中：
     ```bash
     venv_name\Scripts\activate.bat
     ```
   - 在PowerShell中（需要管理员权限）：
     ```powershell
     venv_name\Scripts\Activate.ps1
     ```
   激活后，命令行前会显示虚拟环境名称，如`(venv_name) C:\path\to\your\project>`

5. **退出虚拟环境**
   ```bash
   deactivate
   ```
6. **删除虚拟环境**
   - 直接删除`venv_name`文件夹即可
   

## 方法二：使用第三方工具virtualenv

`virtualenv`提供了更多功能，适用于需要更灵活配置的场景：

1. **安装virtualenv**
   ```bash
   pip install virtualenv
   ```

2. **创建虚拟环境**
   ```bash
   virtualenv venv_name
   ```
   - 指定Python版本：
     ```bash
     virtualenv -p python3.10 venv_name
     ```

3. **激活/退出虚拟环境**
   与`venv`模块的激活/退出命令相同
4. **删除虚拟环境**
   - 直接删除`venv_name`文件夹即可

## 虚拟环境的优势

- 隔离项目依赖，避免版本冲突
- 便于项目迁移和部署
- 保持系统Python环境整洁
- 支持不同项目使用不同的Python版本和依赖包

在实际开发中，推荐使用内置的`venv`模块，因为它是Python标准库的一部分，无需额外安装，且功能已足够满足大多数需求。