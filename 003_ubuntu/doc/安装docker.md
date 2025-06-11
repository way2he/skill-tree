# Ubuntu 系统命令行安装 Docker 步骤详解

## 目录
1. [Docker 简介](#docker-简介)
2. [系统要求](#系统要求)
3. [安装前准备](#安装前准备)
4. [安装步骤](#安装步骤)
5. [配置与优化](#配置与优化)
6. [常见问题与解决方案](#常见问题与解决方案)
7. [Docker 底层原理](#docker-底层原理)
8. [最佳实践](#最佳实践)
9. [安全建议](#安全建议)
10. [经验总结](#经验总结)

## Docker 简介

Docker 是一个开源的容器化平台，它允许开发者将应用程序及其依赖打包到一个可移植的容器中。Docker 的主要优势包括：

- 环境一致性：确保开发、测试和生产环境的一致性
- 资源隔离：容器之间相互隔离，互不影响
- 快速部署：容器启动速度快，资源占用小
- 版本控制：支持镜像版本管理，便于回滚
- 可扩展性：支持水平扩展和负载均衡

### Docker 架构

Docker 采用客户端-服务器（C/S）架构，主要包含以下组件：

1. Docker 守护进程（Docker daemon）
2. Docker 客户端（Docker client）
3. Docker 镜像（Docker images）
4. Docker 容器（Docker containers）
5. Docker 注册表（Docker registry）

## 系统要求

### 硬件要求
- CPU：支持 64 位架构
- 内存：建议至少 2GB RAM
- 存储：建议至少 20GB 可用空间

### 软件要求
- Ubuntu 版本：支持 Ubuntu 20.04 LTS 或更高版本
- 内核版本：3.10 或更高版本
- 系统架构：x86_64、arm64、ppc64le 或 s390x

### 系统检查

在安装 Docker 之前，请执行以下命令检查系统状态：

```bash
# 检查系统版本
lsb_release -a

# 检查内核版本
uname -r

# 检查系统架构
arch

# 检查系统资源
free -h
df -h
```

## 安装前准备

### 1. 更新系统包

```bash
# 更新包索引
sudo apt update

# 升级已安装的包
sudo apt upgrade -y

# 安装必要的依赖
sudo apt install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

### 2. 添加 Docker 官方 GPG 密钥

```bash
# 添加 Docker 的官方 GPG 密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

### 3. 设置 Docker 仓库

```bash
# 添加 Docker 仓库
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

## 安装步骤

### 1. 安装 Docker Engine

```bash
# 更新包索引
sudo apt update

# 安装 Docker Engine
sudo apt install -y docker-ce docker-ce-cli containerd.io
```

### 2. 验证安装

```bash
# 检查 Docker 版本
docker --version

# 运行测试容器
sudo docker run hello-world
```

### 3. 配置用户组（可选但推荐）

```bash
# 将当前用户添加到 docker 组
sudo usermod -aG docker $USER

# 应用组更改（需要重新登录）
newgrp docker
```

## 配置与优化

### 1. 配置 Docker 守护进程

创建或编辑 `/etc/docker/daemon.json` 文件：

```bash
sudo mkdir -p /etc/docker
sudo nano /etc/docker/daemon.json
```

添加以下配置：

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m",
    "max-file": "3"
  },
  "storage-driver": "overlay2",
  "experimental": false,
  "debug": false,
  "registry-mirrors": [
    "https://mirror.ccs.tencentyun.com"
  ]
}
```

### 2. 重启 Docker 服务

```bash
# 重启 Docker 服务
sudo systemctl restart docker

# 设置开机自启
sudo systemctl enable docker
```

### 3. 配置 Docker 日志轮转

创建日志轮转配置：

```bash
sudo nano /etc/logrotate.d/docker
```

添加以下内容：

```
/var/lib/docker/containers/*/*.log {
    rotate 7
    daily
    compress
    missingok
    delaycompress
    copytruncate
}
```

## 常见问题与解决方案

### 1. 权限问题

**问题**：执行 Docker 命令时出现权限错误
**解决方案**：
```bash
# 确保用户属于 docker 组
sudo usermod -aG docker $USER

# 重启 Docker 服务
sudo systemctl restart docker
```

### 2. 存储空间问题

**问题**：Docker 镜像和容器占用过多磁盘空间
**解决方案**：
```bash
# 清理未使用的镜像
docker image prune -a

# 清理停止的容器
docker container prune

# 清理未使用的数据卷
docker volume prune
```

### 3. 网络连接问题

**问题**：无法拉取 Docker 镜像
**解决方案**：
```bash
# 检查 DNS 设置
cat /etc/resolv.conf

# 配置国内镜像源
sudo nano /etc/docker/daemon.json
```

## Docker 底层原理

### 1. 命名空间（Namespaces）

Docker 使用 Linux 命名空间实现容器隔离，主要包括：

- PID 命名空间：进程隔离
- NET 命名空间：网络隔离
- MNT 命名空间：文件系统挂载点隔离
- UTS 命名空间：主机名和域名隔离
- IPC 命名空间：进程间通信隔离
- USER 命名空间：用户和用户组隔离

### 2. 控制组（Cgroups）

Docker 使用 cgroups 限制和监控容器的资源使用：

- CPU 使用限制
- 内存使用限制
- 磁盘 I/O 限制
- 网络带宽限制

### 3. 联合文件系统（UnionFS）

Docker 使用联合文件系统实现镜像分层：

- 基础镜像层
- 可写容器层
- 镜像层缓存
- 写时复制（CoW）机制

## 最佳实践

### 1. 镜像管理

- 使用官方基础镜像
- 多阶段构建
- 优化镜像大小
- 合理使用 .dockerignore

### 2. 容器管理

- 使用容器编排工具
- 实现容器健康检查
- 配置资源限制
- 实现日志管理

### 3. 安全实践

- 定期更新 Docker
- 使用非 root 用户运行容器
- 扫描镜像漏洞
- 限制容器权限

## 安全建议

### 1. 系统安全

```bash
# 更新系统安全补丁
sudo apt update && sudo apt upgrade -y

# 配置防火墙
sudo ufw enable
sudo ufw allow 2375/tcp  # Docker API
sudo ufw allow 2376/tcp  # Docker API (TLS)
```

### 2. Docker 安全

```bash
# 启用 Docker 内容信任
export DOCKER_CONTENT_TRUST=1

# 配置 Docker 守护进程安全选项
sudo nano /etc/docker/daemon.json
```

添加以下安全配置：

```json
{
  "userns-remap": "default",
  "no-new-privileges": true,
  "selinux-enabled": true,
  "apparmor-profile": "docker-default"
}
```

## 经验总结

### 1. 安装经验

- 始终使用官方源安装
- 验证 GPG 密钥
- 检查系统兼容性
- 配置镜像加速

### 2. 运维经验

- 定期清理未使用的资源
- 监控容器资源使用
- 实施备份策略
- 保持系统更新

### 3. 开发经验

- 使用 Dockerfile 最佳实践
- 实现自动化构建
- 优化构建缓存
- 合理使用多阶段构建

## 后续内容预告

在下一部分，我们将深入探讨：

1. Docker 网络模型详解
2. Docker 存储驱动分析
3. Docker 安全加固指南
4. Docker 性能优化技巧
5. Docker 集群部署方案
6. Docker 监控与日志管理
7. Docker 故障排查指南
8. Docker 企业级实践案例 