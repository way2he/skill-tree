# 更改源
```bash
# 临时使用国内源安装包
pip install <package> -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 永久设置国内源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
```

# 常用包安装
```bash
pip install jieba
pip install numpy
pip install tensorflow # 目前最新版本2.20.0支持到python3.12
pip install torch # 安装pytorch
```