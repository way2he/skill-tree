# Ubuntu系统命令行安装Docker步骤详解

## 一、引言
Docker作为当前最流行的容器化技术，通过轻量级虚拟化实现应用的快速部署与隔离。本文档基于Ubuntu 22.04 LTS系统，从环境准备到原理剖析，全面讲解命令行安装Docker的完整流程，并总结实战经验。

---

## 二、系统环境准备
### 2.1 确认Ubuntu版本
Docker对Ubuntu版本有明确兼容性要求（需64位系统且为LTS版本），首先验证系统信息：
```bash
# 查看系统版本
lsb_release -a
# 输出示例：
# Distributor ID: Ubuntu
# Description:    Ubuntu 22.04.3 LTS
# Release:        22.04
# Codename:       jammy

# 确认内核版本（需≥3.10）
kernel_version=$(uname -r | cut -d. -f1-2)
if (( $(echo "$kernel_version >= 3.10" | bc -l) )); then
  echo "内核版本符合要求" 
else
  echo "内核版本过低，需升级" && exit 1
fi
```

### 2.2 更新系统包列表
安装前建议更新包索引并升级现有包，避免依赖冲突：
```bash
sudo apt update && sudo apt upgrade -y
```

### 2.3 安装必要依赖库
Docker需要通过HTTPS访问仓库，需安装传输协议支持包：
```bash
sudo apt install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
```
* `apt-transport-https`：支持HTTPS源
* `ca-certificates`：SSL证书验证
* `gnupg-agent`：GPG密钥管理

---

## 三、Docker官方仓库配置
### 3.1 添加GPG签名密钥
为确保下载的Docker包未被篡改，需添加Docker官方GPG密钥（指纹：9DC8 5822 9FC7 DD38 854A E2D8 8D81 803C 0EBF CD88）：
```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 验证密钥指纹
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/docker-archive-keyring.gpg --list-keys
# 应显示：9DC8 5822 9FC7 DD38 854A E2D8 8D81 803C 0EBF CD88
```

### 3.2 添加稳定版仓库源
根据Ubuntu版本（如jammy对应22.04）添加Docker稳定版仓库：
```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

---

## 四、Docker引擎安装
### 4.1 安装Docker CE（社区版）
执行以下命令安装Docker引擎、CLI工具和containerd运行时：
```bash
sudo apt update  # 重新加载包索引
sudo apt install -y docker-ce docker-ce-cli containerd.io
```
* `docker-ce`：核心引擎组件
* `docker-ce-cli`：命令行客户端
* `containerd.io`：容器运行时（基于GRPC接口与引擎通信）

### 4.2 验证安装结果
通过运行官方测试镜像验证安装：
```bash
sudo docker run hello-world
```
输出应包含：
```
Hello from Docker! This message shows that your installation appears to be working correctly.
```

---

## 五、用户权限配置（关键步骤）
默认情况下，普通用户需通过`sudo`执行Docker命令，为简化操作可将用户添加至`docker`组：
```bash
# 创建docker组（若不存在）
sudo groupadd docker

# 将当前用户加入docker组
sudo usermod -aG docker $USER

# 刷新用户组权限（或重启终端）
su - $USER
```
* 安全提示：`docker`组用户拥有与`root`等效的权限（可访问所有容器资源），生产环境需严格控制组成员！

---

## 六、服务管理与状态检查
### 6.1 启动/停止/重启Docker服务
```bash
# 启动服务
sudo systemctl start docker

# 停止服务
sudo systemctl stop docker

# 重启服务
sudo systemctl restart docker
```

### 6.2 设置开机自启
```bash
sudo systemctl enable docker
```

### 6.3 查看服务状态
```bash
systemctl status docker
# 正常状态应显示：Active: active (running)
```

---

## 七、常见陷阱与规避
### 7.1 仓库源配置错误
**现象**：`apt install`时提示"Unable to locate package docker-ce"。
**原因**：仓库源URL错误或GPG密钥未正确导入。
**解决**：
1. 检查`/etc/apt/sources.list.d/docker.list`中的URL是否匹配当前Ubuntu版本
2. 重新执行GPG密钥导入命令

### 7.2 依赖冲突
**现象**：安装时提示"Some packages could not be installed"。
**原因**：系统中存在旧版Docker（如`docker.io`）未卸载。
**解决**：
```bash
# 卸载旧版本
sudo apt remove -y docker docker-engine docker.io containerd runc
# 清理残留配置
sudo rm -rf /var/lib/docker /etc/docker
```

### 7.3 权限拒绝（Permission Denied）
**现象**：非root用户执行`docker run`时提示"Got permission denied while trying to connect to the Docker daemon socket"。
**解决**：
1. 确认用户已加入`docker`组（`groups $USER`查看）
2. 刷新权限（`newgrp docker`或重启终端）

---

## 八、底层原理剖析（选读）
### 8.1 Docker架构概览
Docker采用C/S架构，核心组件包括：
- **Docker Daemon（dockerd）**：运行在宿主机的后台进程，负责镜像、容器的生命周期管理
- **Docker CLI（docker）**：用户通过CLI发送REST API请求至Daemon
- **Containerd**：轻量级运行时，负责容器的实际执行（调用runc创建命名空间和cgroups）

### 8.2 镜像存储机制
Docker镜像基于Union File System（联合文件系统），通过分层（Layer）实现存储共享。例如：
```dockerfile
FROM ubuntu:22.04
RUN apt update
CMD ["/bin/bash"]
```
会生成3层镜像（基础层+更新层+命令层），每层仅存储与父层的差异。

### 8.3 容器隔离技术
容器通过Linux内核的两大特性实现隔离：
- **命名空间（Namespaces）**：隔离进程、网络、文件系统等资源（如PID、NET、MNT命名空间）
- **控制组（cgroups）**：限制CPU、内存、磁盘I/O等资源的使用量

---

## 九、经验总结
1. **优先使用官方仓库**：第三方源可能包含过时或修改过的包，存在安全风险
2. **定期更新Docker**：通过`sudo apt upgrade docker-ce`获取最新安全补丁（LTS版本每季度发布更新）
3. **谨慎管理用户权限**：生产环境建议为每个项目创建独立用户并限制`docker`组成员
4. **监控容器资源**：使用`docker stats`或Prometheus+Grafana监控CPU/内存使用率

---

## 十、Docker镜像构建最佳实践
### 10.1 Dockerfile编写规范
- **基础镜像选择**：优先使用官方轻量级镜像（如`ubuntu:22.04`而非`ubuntu:latest`），减少镜像体积
- **分层优化**：将变更频率低的指令（如`COPY requirements.txt`）放在前面，利用缓存机制加速构建
- **清理临时文件**：在`RUN`指令中组合安装与清理操作（如`apt update && apt install -y pkg && apt clean`），避免冗余文件

示例Dockerfile：
```dockerfile
# 使用官方轻量级基础镜像
FROM ubuntu:22.04

# 设置时区（避免容器时间异常）
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 安装Python并清理缓存
RUN apt update && apt install -y python3 python3-pip && apt clean

# 复制项目文件（放在最后以利用缓存）
COPY . /app
WORKDIR /app

# 安装依赖（使用--no-cache-dir减少体积）
RUN pip3 install --no-cache-dir -r requirements.txt

# 暴露端口并设置启动命令
EXPOSE 8000
CMD ["python3", "app.py"]
```

### 10.2 构建命令优化
使用`docker build`时添加`--rm`参数自动删除中间容器，避免磁盘空间浪费：
```bash
docker build -t myapp:v1 --rm .
```

---

## 十一、容器网络配置详解
### 11.1 网络模式对比
Docker提供4种网络模式：
| 模式       | 特点                                                                 | 适用场景                     |
|------------|----------------------------------------------------------------------|------------------------------|
| `bridge`   | 默认模式，容器通过虚拟网桥（docker0）与宿主机通信                   | 开发测试环境                 |
| `host`     | 容器共享宿主机网络命名空间，无网络隔离                               | 需要高性能网络的服务（如Nginx）| 
| `none`     | 容器无网络接口，需手动配置                                           | 安全敏感场景（如加密计算）   |
| `container`| 容器共享其他容器的网络命名空间                                       | 容器间紧密协作（如数据库+应用）|

### 11.2 自定义网桥配置
通过`docker network create`创建自定义网桥，实现容器间跨主机通信：
```bash
docker network create --driver bridge --subnet 172.18.0.0/16 my-bridge
```
* `--driver`：指定网络驱动（默认`bridge`）
* `--subnet`：设置子网范围（避免与宿主机IP冲突）

### 11.3 端口映射注意事项
- **宿主机端口唯一性**：多个容器映射同一宿主机端口会导致冲突（错误：`Bind for 0.0.0.0:80 failed`）
- **动态端口分配**：使用`-P`参数自动映射随机端口（`docker run -P myapp:v1`），适合测试环境
- **端口绑定范围**：通过`-p IP:host_port:container_port`指定绑定IP（如仅绑定本地`127.0.0.1:8080:80`）

---

## 十二、存储卷管理技巧
### 12.1 数据持久化方案
| 类型         | 实现方式                          | 特点                                                                 |
|--------------|-----------------------------------|----------------------------------------------------------------------|
| 匿名卷       | `docker run -v /data`             | Docker自动创建，容器删除后卷保留（需手动清理）                       |
| 具名卷       | `docker run -v my-volume:/data`   | 卷有名称，便于管理（`docker volume ls`查看）                         |
| 绑定挂载     | `docker run -v /host/path:/data`  | 直接挂载宿主机目录，适合需要直接访问宿主机文件的场景                 |

### 12.2 卷备份与迁移
- **备份卷**：通过`docker run --rm -v my-volume:/vol -v $(pwd):/backup alpine tar -czf /backup/volume.tar.gz -C /vol .`打包卷内容
- **恢复卷**：`docker run --rm -v my-volume:/vol -v $(pwd):/backup alpine tar -xzf /backup/volume.tar.gz -C /vol`

### 12.3 卷权限问题解决
**现象**：容器内写入卷时报"Permission denied"。
**原因**：容器内用户UID与宿主机目录权限不匹配。
**解决**：
1. 在Dockerfile中指定用户UID（`RUN groupadd -r app && useradd -r -g app -u 1000 app`）
2. 挂载时设置权限（`docker run -v /host/path:/data:rw`）

---

（文档已完整覆盖用户要求内容，后续可根据实际需求补充高级主题如Docker Compose使用、Swarm集群部署等）