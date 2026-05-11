# Windows系统下Docker Desktop安装与使用教程

## 一、系统要求
- Windows 11 64位：家庭版或专业版 21H2 或更高版本
- 必须启用CPU虚拟化技术
- 至少4GB内存

## 二、安装前准备
### 2.1 检查系统版本
按下 `Win + R`，输入 `winver` 并回车，确认Windows版本符合要

### 2.2 启用虚拟化
在任务管理器（Ctrl+Shift+Esc）的"性能"选项卡中查看CPU虚拟化是否已启用。如未启用，需进入BIOS设置开启

### 2.3 启用必要的Windows功能
1. 按下 `Win + R`，输入 `OptionalFeatures` 并回车
2. 勾选以下选项：
   - Hyper-V（仅专业版/企业版需要）
   - 适用于Linux的Windows子系统
   - Windows虚拟机监控程序平台
   - 容器
3. 点击确定并重启电脑

### 2.4 安装WSL2
1. 以管理员身份打开PowerShell
2. 运行以下命令安装WSL2：
```powershell
wsl --install
wsl --set-default-version 2
```
3. 安装完成后重启电脑

## 三、安装Docker Desktop
### 3.1 下载Docker Desktop
访问Docker官网下载安装包：[https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)

### 3.2 安装Docker Desktop
1. 双击下载的安装文件 `Docker Desktop Installer.exe`
2. 在安装界面中，勾选"Use WSL 2 instead of Hyper-V (recommended)"
3. 点击"OK"开始安装
4. 安装完成后点击"Close and restart"

### 3.3 启动Docker Desktop
安装完成后，Docker会自动启动，也可以从开始菜单手动启动。首次启动时会在系统托盘显示鲸鱼图标，表示Docker正在运行。

## 四、Docker Desktop配置
### 4.1 配置镜像加速器
为提高镜像下载速度，建议配置国内镜像源：
1. 在系统托盘右键点击Docker图标，选择"Settings"
2. 选择"Docker Engine"选项卡
3. 在配置文件中添加镜像源：
```json
{
  "registry-mirrors": [
    "https://docker.xuanyuan.me",
    "https://docker.m.daocloud.io",
    "https://docker.1ms.run"
  ]
}
```
4. 点击"Apply & Restart"保存配置并重启Docker

### 4.2 调整资源分配
1. 在设置中选择"Resources"选项卡
2. 根据需要调整CPU、内存和磁盘空间分配
3. 点击"Apply & Restart"使配置生效

## 五、验证安装
### 5.1 检查Docker版本
打开PowerShell或命令提示符，运行以下命令检查Docker版本：
```powershell
docker --version
```

### 5.2 运行Hello World容器
通过运行hello-world镜像验证Docker是否正常工作：
```powershell
docker run hello-world
```
如果一切正常，会看到类似以下的输出：
```
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

## 六、Docker基本使用命令
### 6.1 镜像操作
- 拉取镜像：`docker pull [镜像名]:[标签]`
  示例：拉取Nginx镜像
```powershell
docker pull nginx
```

- 查看本地镜像：`docker images`

- 删除镜像：`docker rmi [镜像ID或名称]`

### 6.2 容器操作
- 运行容器：`docker run [选项] [镜像名]`
  示例：运行Nginx容器并映射8080端口
```powershell
docker run -d -p 8080:80 --name mynginx nginx
```

- 查看运行中的容器：`docker ps`

- 查看所有容器：`docker ps -a`

- 停止容器：`docker stop [容器ID或名称]`

- 启动容器：`docker start [容器ID或名称]`

- 删除容器：`docker rm [容器ID或名称]`

- 进入容器：`docker exec -it [容器ID或名称] /bin/bash`

### 6.3 docker build命令
- 构建镜像：`docker build -t [镜像名] [Dockerfile路径]`
  示例：在当前目录下构建一个Nginx镜像
```powershell
docker build -t mynginx .
```

- 查看镜像：`docker images`

- 运行容器：`docker run -d -p 8080:80 mynginx`

## 七、常见问题及解决方法
### 7.1 Docker无法启动
- 检查虚拟化是否已启用
- 确保WSL2正确安装
- 尝试重启电脑或重新安装Docker

### 7.2 镜像拉取速度慢
- 配置国内镜像加速器（详见4.1节）

### 7.3 容器无法访问网络
- 检查防火墙设置
- 尝试重启Docker网络
```powershell
docker network prune
```

### 7.4 容器退出后数据丢失
- 使用数据卷（Volume）持久化数据：
```powershell
docker run -v [本地路径]:[容器路径] [镜像名]
```

## 八、Docker Desktop更新与卸载
### 8.1 更新Docker Desktop
1. 在设置中选择"Check for Updates"
2. 如果有更新，点击"Download update"
3. 下载完成后点击"Install and restart"

### 8.2 卸载Docker Desktop
1. 从开始菜单找到"Docker Desktop"
2. 选择"Uninstall"
3. 按照卸载向导完成卸载
4. （可选）删除残留文件：`C:\ProgramData\Docker` 和 `C:\Users\[用户名]\.docker`

## 九、总结
通过以上步骤，您已经成功在Windows系统上安装并配置了Docker Desktop，并了解了基本的Docker命令和使用方法。Docker是一个强大的容器化平台，可以帮助您更轻松地构建、测试和部署应用程序。随着使用的深入，您可以探索更多高级功能，如Docker Compose容器编排、Docker Swarm集群管理等。