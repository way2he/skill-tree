#!/bin/bash

# 创建字体目录
mkdir -p ~/.local/share/fonts/chinese

# 下载SimHei字体
echo "正在下载SimHei字体..."
# 使用备用源下载SimHei字体
wget -q -O ~/.local/share/fonts/chinese/simhei.ttf "https://gitcode.net/mirrors/fangwentong/windows-fonts/raw/master/SimHei.ttf"

# 检查SimHei字体是否下载成功
if [ ! -f "~/.local/share/fonts/chinese/simhei.ttf" ]; then
    echo "SimHei字体下载失败，尝试其他源..."
    wget -q -O ~/.local/share/fonts/chinese/simhei.ttf "https://cdn.jsdelivr.net/npm/windows-fonts@1.0.4/fonts/SimHei.ttf"
fi

# 下载Heiti TC字体
echo "正在下载Heiti TC字体..."
# 使用备用源下载Heiti TC字体
wget -q -O ~/.local/share/fonts/chinese/heititc.ttf "https://gitcode.net/mirrors/StellarCN/scp_assets/raw/master/fonts/HeitiTC.ttf"

# 检查Heiti TC字体是否下载成功
if [ ! -f "~/.local/share/fonts/chinese/heititc.ttf" ]; then
    echo "Heiti TC字体下载失败，尝试其他源..."
    wget -q -O ~/.local/share/fonts/chinese/heititc.ttf "https://github.com/googlefonts/noto-cjk/blob/main/Sans/OTF/TraditionalChinese/NotoSansTC-Regular.otf?raw=true"
    mv ~/.local/share/fonts/chinese/heititc.ttf ~/.local/share/fonts/chinese/HeitiTC.ttf
fi

# 检查WenQuanYi Micro Hei是否已安装
if ! fc-list | grep -q "WenQuanYi Micro Hei"; then
    echo "WenQuanYi Micro Hei字体未安装，请手动安装: sudo apt-get install -y ttf-wqy-microhei"
else
    echo "WenQuanYi Micro Hei字体已安装"
fi

# 更新字体缓存
echo "正在更新字体缓存..."
fc-cache -f -v

# 验证安装
echo "已安装的中文字体："
fc-list | grep -E "SimHei|WenQuanYi Micro Hei|Heiti TC|Noto Sans TC"

echo "字体安装完成！sans-serif是字体族名称，系统会自动处理。"