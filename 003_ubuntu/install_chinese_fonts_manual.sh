#!/bin/bash

# 中文字体手动安装脚本

# 1. 安装WenQuanYi Micro Hei字体（通过apt）
echo "正在安装WenQuanYi Micro Hei字体..."
sudo apt-get install -y ttf-wqy-microhei

# 2. 为SimHei和Heiti TC字体创建目录
mkdir -p ~/.local/share/fonts/chinese

# 3. 提示用户手动下载字体文件
echo -e "\n请手动下载以下字体文件并保存到 ~/.local/share/fonts/chinese/ 目录："
echo "1. SimHei字体: https://github.com/fangwentong/windows-fonts/raw/master/SimHei.ttf"
echo "2. Heiti TC字体: https://github.com/StellarCN/scp_assets/raw/master/fonts/HeitiTC.ttf"
echo -e "\n下载完成后按Enter键继续..."
read -p ""

# 4. 更新字体缓存
echo "正在更新字体缓存..."
fc-cache -f -v

# 5. 验证安装
echo -e "\n已安装的中文字体："
fc-list | grep -E "SimHei|WenQuanYi Micro Hei|Heiti TC"

echo -e "\n字体安装指南完成！sans-serif是字体族名称，系统会自动处理。"
echo "如果SimHei或Heiti TC字体未显示在列表中，请确认字体文件已正确下载并放置在指定目录。"