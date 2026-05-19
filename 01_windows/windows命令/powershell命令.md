```cmd
Get-Content c:\Users\robotAi\Documents\repo\py-dl\006_NLP自然语言处理基础\01_文本预处理\code\data\fil9 -TotalCount 5
```

# PowerShell 操作文件夹命令
```powershell
# 创建文件夹
New-Item -Path "C:\TestFolder" -ItemType Directory

# 创建嵌套文件夹
New-Item -Path "C:\Parent\Child\Grandchild" -ItemType Directory -Force

# 查看当前目录
Get-Location

# 进入文件夹
Set-Location -Path "C:\TestFolder"

# 查看文件夹内容
Get-ChildItem -Path "C:\TestFolder"

# 查看文件夹详细信息
Get-ChildItem -Path "C:\TestFolder" -Detailed

# 复制文件夹
Copy-Item -Path "C:\TestFolder" -Destination "C:\TestFolderCopy" -Recurse

# 移动文件夹
Move-Item -Path "C:\TestFolderCopy" -Destination "C:\NewLocation"

# 重命名文件夹
Rename-Item -Path "C:\NewLocation\TestFolderCopy" -NewName "RenamedFolder"

# 删除文件夹
Remove-Item -Path "C:\TestFolder" -Recurse

# 删除文件夹（强制）
Remove-Item -Path "C:\Parent" -Recurse -Force
```