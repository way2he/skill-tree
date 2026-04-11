# Windows CMD 文件夹操作命令

## 一、切换文件夹命令 (cd)

### 基本语法
```cmd
cd [路径]
```

### 常用用法

1. **切换到指定目录**
   ```cmd
   cd c:\Windows  # 切换到C盘Windows目录
   ```

2. **切换到当前盘的其他目录**
   ```cmd
   cd Users\robotAi\Documents  # 切换到当前盘的Documents目录
   ```

3. **返回上一级目录**
   ```cmd
   cd ..
   ```

4. **返回根目录**
   ```cmd
   cd \  # 返回到当前盘的根目录
   ```

5. **查看当前目录**
   ```cmd
   cd  # 不带参数时显示当前目录路径
   ```

6. **切换到其他磁盘**
   ```cmd
   D:  # 直接输入磁盘盘符即可切换
   ```

## 二、创建文件夹命令 (mkdir/md)

### 基本语法
```cmd
mkdir [目录名]  # 或 md [目录名]
```

### 常用用法

1. **创建单个文件夹**
   ```cmd
   mkdir Test  # 创建名为Test的文件夹
   ```

2. **创建多层级文件夹**
   ```cmd
   mkdir -p A\B\C  # 创建A文件夹下的B文件夹下的C文件夹
   ```
3. **创建多个文件夹**
   ```cmd
   mkdir Test1 Test2 Test3  # 同时创建三个文件夹
   ```

## 三、删除文件夹命令 (rmdir/rd)

### 基本语法
```cmd
rmdir [目录名]  # 或 rd [目录名]
```

### 常用用法

1. **删除空文件夹**
   ```cmd
   rmdir Test  # 删除名为Test的空文件夹
   ```

2. **删除非空文件夹及其内容**
   ```cmd
   rmdir /s Test  # 删除Test文件夹及其所有内容，并询问确认
   ```

3. **强制删除非空文件夹（不询问）**
   ```cmd
   rmdir /s /q Test  # 静默删除Test文件夹及其所有内容
   ```

## 四、列出文件夹内容命令 (dir)

### 基本语法
```cmd
dir [目录路径]
```

### 常用用法

1. **列出当前目录内容**
   ```cmd
   dir  # 列出当前目录下的文件和文件夹
   ```

2. **列出指定目录内容**
   ```cmd
   dir c:\Windows  # 列出C盘Windows目录的内容
   ```

3. **列出详细信息**
   ```cmd
   dir /w  # 宽格式显示
   dir /l  # 小写显示
   dir /a  # 显示所有文件（包括隐藏文件）
   dir /s  # 显示目录及其子目录的内容
   ```

## 五、复制文件夹命令 (xcopy)

### 基本语法
```cmd
xcopy [源目录] [目标目录] [参数]
```

### 常用用法

1. **复制文件夹及其内容**
   ```cmd
   xcopy Source Destination /s  # 复制Source文件夹及其子文件夹（不包括空文件夹）
   ```

2. **复制文件夹及其所有内容（包括空文件夹）**
   ```cmd
   xcopy Source Destination /e
   ```

3. **复制时保持文件属性和时间戳**
   ```cmd
   xcopy Source Destination /s /k
   ```

## 六、移动文件夹命令 (move)

### 基本语法
```cmd
move [源目录] [目标目录]
```

### 常用用法

1. **移动文件夹**
   ```cmd
   move Source D:\Destination  # 将Source文件夹移动到D盘的Destination目录
   ```

2. **重命名文件夹**
   ```cmd
   move OldName NewName  # 将当前目录下的OldName文件夹重命名为NewName
   ```

## 七、查看文件夹大小命令 (dir/robocopy)

### 查看当前目录大小
```cmd
dir /s /-c | findstr "总字节数"
```

### 使用robocopy查看详细大小
```cmd
robocopy . . /S /NFL /NDL /NJH /NJS /BYTES
```

## 八、文件夹权限命令 (icacls)

### 基本语法
```cmd
icacls [目录路径] [参数]
```

### 常用用法

1. **查看文件夹权限**
   ```cmd
   icacls Test  # 查看Test文件夹的权限设置
   ```

2. **修改文件夹权限**
   ```cmd
   icacls Test /grant Users:F  # 授予Users组完全控制权限
   ```

## 九、常用快捷键

- `Tab`：自动补全文件名或目录名
- `Ctrl+C`：中断当前命令
- `F3`：重复上一条命令
- `↑`/`↓`：浏览命令历史

以上是Windows CMD中最常用的文件夹操作命令，掌握这些命令可以高效地在命令行环境中管理文件和文件夹。