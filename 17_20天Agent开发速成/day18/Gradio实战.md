
---
name: Gradio实战
description: Gradio快速入门
type: knowledge
tags: ["Gradio", "UI", "界面"]
summary: Gradio快速入门
created_at: 2026-05-26
updated_at: 2026-05-26
version: interview
---

# Gradio实战 🎨

## 简单示例

```python
import gradio as gr

def greet(name):
    return f"Hello, {name}!"

def add(a, b):
    return a + b

# 界面1：简单问候
demo1 = gr.Interface(
    fn=greet,
    inputs="text",
    outputs="text",
    title="问候示例",
    examples=["Alice", "Bob"]
)

# 界面2：计算器
demo2 = gr.Interface(
    fn=add,
    inputs=[gr.Number(), gr.Number()],
    outputs="number",
    title="计算器"
)

# 启动
if __name__ == "__main__":
    demo1.launch()
```

## 运行

```bash
pip install gradio
python app.py
```

## 访问

http://127.0.0.1:7860

---

**🎉 完成！**
