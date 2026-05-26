
# -*- coding: utf-8 -*-
"""
Day11 代码示例 04: 多模态基础
"""

import sys
import io
from typing import Dict, Any

# 处理 Windows 编码问题
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# 1. 多模态输入
class MultimodalInput:
    def __init__(self, text: str = None, image: str = None, audio: str = None):
        self.text = text
        self.image = image
        self.audio = audio
    
    def __repr__(self):
        parts = []
        if self.text:
            parts.append("text")
        if self.image:
            parts.append("image")
        if self.audio:
            parts.append("audio")
        return f"MultimodalInput({', '.join(parts)})"


# 2. 多模态输出
class MultimodalOutput:
    def __init__(self, text: str = None, image: str = None, audio: str = None):
        self.text = text
        self.image = image
        self.audio = audio
    
    def __repr__(self):
        parts = []
        if self.text:
            parts.append("text")
        if self.image:
            parts.append("image")
        if self.audio:
            parts.append("audio")
        return f"MultimodalOutput({', '.join(parts)})"


# 3. 多模态编码器（模拟）
class MultimodalEncoder:
    def encode_text(self, text: str) -> Any:
        print(f"📝 编码文本: {text[:30]}...")
        return f"text_emb:{len(text)}"
    
    def encode_image(self, image: str) -> Any:
        print(f"🖼️  编码图像: {image[:30]}...")
        return f"image_emb:{len(image)}"
    
    def encode_audio(self, audio: str) -> Any:
        print(f"🎵 编码音频: {audio[:30]}...")
        return f"audio_emb:{len(audio)}"


# 4. 融合模块（模拟）
class FusionModule:
    def fuse(self, embeddings: Dict[str, Any]) -> Any:
        print(f"🔗 融合多模态表示: {list(embeddings.keys())}")
        return "fused_representation"


# 5. 多模态生成器（模拟）
class MultimodalGenerator:
    def generate_text(self, fused_repr: Any, prompt: str) -> str:
        print(f"📝 生成文本...")
        return f"[Generated Text: {prompt[:20]}...]"
    
    def generate_image(self, fused_repr: Any, description: str) -> str:
        print(f"🖼️  生成图像: {description}...")
        return f"[Generated Image: {description}]"
    
    def generate_audio(self, fused_repr: Any, text: str) -> str:
        print(f"🎵 生成音频...")
        return f"[Generated Audio: {text[:20]}...]"


# 6. 多模态 Agent
class SimpleMultimodalAgent:
    """简单的多模态 Agent"""
    
    def __init__(self):
        self.encoder = MultimodalEncoder()
        self.fusion = FusionModule()
        self.generator = MultimodalGenerator()
    
    def process(self, input_data: MultimodalInput,
                output_types=None) -> MultimodalOutput:
        """处理多模态输入"""
        output_types = output_types or ["text"]
        
        print("="*60)
        print(f"🧠 多模态 Agent 处理: {input_data}")
        print("="*60)
        
        # 1. 编码
        embeddings = {}
        if input_data.text:
            embeddings["text"] = self.encoder.encode_text(input_data.text)
        if input_data.image:
            embeddings["image"] = self.encoder.encode_image(input_data.image)
        if input_data.audio:
            embeddings["audio"] = self.encoder.encode_audio(input_data.audio)
        
        # 2. 融合
        fused = self.fusion.fuse(embeddings)
        
        # 3. 推理（模拟）
        print(f"🤔 推理中...")
        
        # 4. 生成输出
        output = MultimodalOutput()
        if "text" in output_types:
            prompt = input_data.text or "请描述输入"
            output.text = self.generator.generate_text(fused, prompt)
        if "image" in output_types:
            desc = input_data.text or "生成一张相关图片"
            output.image = self.generator.generate_image(fused, desc)
        
        print("\n✅ 处理完成！")
        return output


# 7. 测试
if __name__ == "__main__":
    agent = SimpleMultimodalAgent()
    
    # 测试 1: 纯文本
    print("\n" + "="*60)
    print("1️⃣  纯文本输入")
    print("="*60)
    input1 = MultimodalInput(text="你好，请介绍一下自己")
    output1 = agent.process(input1, output_types=["text"])
    print(f"📤 输出: {output1.text}")
    
    # 测试 2: 图像+文本
    print("\n" + "="*60)
    print("2️⃣  图像+文本输入")
    print("="*60)
    input2 = MultimodalInput(
        text="这张图片里有什么？",
        image="image_of_a_cat.jpg"
    )
    output2 = agent.process(input2, output_types=["text"])
    print(f"📤 输出: {output2.text}")
    
    # 测试 3: 文本→图像
    print("\n" + "="*60)
    print("3️⃣  文本→图像")
    print("="*60)
    input3 = MultimodalInput(text="画一只可爱的猫")
    output3 = agent.process(input3, output_types=["image"])
    print(f"📤 输出: {output3.image}")
    
    print("\n🎉 多模态基础示例完成!")
