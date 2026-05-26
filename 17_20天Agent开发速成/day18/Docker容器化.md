
---
name: Docker容器化
description: Docker容器化快速入门
type: knowledge
tags: ["Docker", "容器化", "部署"]
summary: Docker容器化快速入门
created_at: 2026-05-26
updated_at: 2026-05-26
version: interview
---

# Docker容器化 🐳

## Dockerfile示例

```dockerfile
# 基础镜像
FROM python:3.11-slim

# 工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 常用命令

```bash
# 构建镜像
docker build -t myapp .

# 运行容器
docker run -p 8000:8000 myapp

# 查看镜像
docker images

# 查看容器
docker ps

# 停止容器
docker stop <container_id>
```

## docker-compose.yml

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENV=production
```

---

**🎉 完成！**
