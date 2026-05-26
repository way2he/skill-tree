
---
name: FastAPI基础
description: FastAPI基础快速入门
type: knowledge
tags: ["FastAPI", "API"]
summary: FastAPI基础快速入门
created_at: 2026-05-26
updated_at: 2026-05-26
version: interview
---

# FastAPI基础 ⚡

## 简单示例

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 数据模型
class Item(BaseModel):
    name: str
    price: float
    description: str | None = None

# GET请求
@app.get("/")
def read_root():
    return {"message": "Hello World"}

# GET带参数
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

# POST请求
@app.post("/items/")
def create_item(item: Item):
    return {"item": item}
```

## 运行

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

## 访问

- API：http://127.0.0.1:8000
- 文档：http://127.0.0.1:8000/docs

---

**🎉 完成！**
