# 用 OpenClaw 快速搭建 Hermes Agent：一个会“自进化”的 Agent

OpenClaw 在帮你做任务这块已经很棒了，但做完就结束了——它不会记住经验，也不会越用越强。

最近 Hermes Agent 火热，它的亮点在于引入了“自动技能生成”。

👉 它会把执行过程沉淀成「技能（skills）」  
👉 用得越多，能力越强，而不是每次从零开始

  


OpenClaw：Your own personal AI assistant. Any OS. Any Platform. The lobster way. 🦞

Hermes Agent：The agent that grows with you

![](https://mmbiz.qpic.cn/mmbiz_jpg/r4mqujZZ0rAL4A35Vw2YUdHPG59YdRU6QiaQP62XqQtLjdtTcDH0vHBjtwbrRhPdJ68vSj1uEkbyS22YjvVyPzkEXkwF0PHjBuJprvuuYmDM/640?wx_fmt=jpeg)

  


这篇文章用 OpenClaw 来**快速搭建** Hermes Agent，并重新配置 飞书 + 阿里云百炼大模型 + VNC浏览器 的环境。

## 一、初始化 Hermes

别手动折腾环境了，直接先让 OpenClaw 帮你干：把基础环境搭好，参考官方 Quickstart。

  *   *   * 

    
    
    帮我新建hermes用户，然后安装 hermes-agent: https://hermes-agent.nousresearch.com/docs/getting-started/quickstart  
    大模型API Key参考openclaw的

![](https://mmbiz.qpic.cn/mmbiz_png/r4mqujZZ0rBNXtcXobX23bSKkmzWJxiafX0nHaLqICq3s0HlalqE0Ym8rhCJt9AV0GabBgurjObHAibZtLlSBtOkNro2micAibP28jMTCwhGOyM/640?wx_fmt=png&from=appmsg)  


## 二、打通消息通道：修复大模型和配置飞书接入

目标很简单：**先用飞书跟 Hermes 聊起来**

  


1、配置好大模型：阿里云百炼 Coding Plan

OpenClaw 配置的不是百炼 Coding Plan 的地址，模型也不对。

需要手动调整一下，用 hermes model 配置：选 Alibaba Cloud / DashScope Coding，填写 Base URL 和 模型名称。

![](https://mmbiz.qpic.cn/mmbiz_png/r4mqujZZ0rDgiboTtl77jfIpC3HCoA9FC7F3UI9a4OqyWib9lUdEJXwmKlWLOvWW4cC2EyYwoF5egBbEHeb0W41OLjh48HptukoDE46E90F74/640?wx_fmt=png&from=appmsg)

  


敏感信息（API keys 和 secrets）以环境变量的方式保存在 ~/.hermes/.env 。

![](https://mmbiz.qpic.cn/mmbiz_png/r4mqujZZ0rCsic40uVDYevibg5Kqbj9oFOaVOiaTreDubRibHdfdAt7ApKMWP868jkuxXCS6T6DDibhMyLQDzT9iaLrs7lGKI6h7FoaTIpeZ0ibicEk/640?wx_fmt=png&from=appmsg)

  


2、接入飞书：直接扫码新建机器人  


https://hermes-agent.nousresearch.com/docs/user-guide/messaging/feishu#step-1-create-a-feishu--lark-app

  


现在，建机器人这一步做的太惊艳了，执行 hermes gateway setup ，然后扫个码，在手机上确认一下，飞书应用机器人就创建好了，非常之简单。

推荐的交互式卡片配置也默认设置好了。

  


![](https://mmbiz.qpic.cn/mmbiz_png/r4mqujZZ0rCmicBd7e9RCNVg4JX8zc15kWtUtefp3cCeqiawKtuo8fKYQ8ia0fPeia18IvcHrjIibqR4H4aria8Wl2SP7tMIqORapZx9iakKLEz6dY/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/r4mqujZZ0rBguwUFACtENkgC4e7xMx3tKLwnJZ60zfw0LC6TKQE7eRoWuNIHtGtibOYPEkdtkiaqf7ziaBVse8HNlEUaMuruaQ9P2FJbLzUQd0/640?wx_fmt=jpeg)

  


给机器人发个消息，然后配对，跑通 Hermes Agent。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/r4mqujZZ0rAjC4RV9J5VkKBpU9cBI3IHXgRnDS7eicgeRYGdcicu0GiasJLria2jyiaDTGRmZllBMaLEiakZc9oouhdwY6rLgTArh5iaL6ZhJgebDI/640?wx_fmt=png&from=appmsg)![](https://mmbiz.qpic.cn/mmbiz_png/r4mqujZZ0rBF3rF1n2DgFiaLTmMEzhZkZaD2sPV0ib0SWCX4Y6YMZepicpaqUbSRJwJCj9tGdlg4Hk0vc8ld9ibTsY0ziasUVlWgKb4oJRmtRPGQ/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/mmbiz_png/r4mqujZZ0rB7pmOhuibOxXcEG3T3YYdKg0wSHwgZwszJIdyV3VbuOMiaBDyqnPGytq6cVEndA3o1Y7F7D3NJTlXVwnpwTCLqgLHOWoRCQAtM8/640?wx_fmt=png&from=appmsg)

  


## 三、给 AI 装“眼睛”：Brave浏览器 + VNC

如果你打算认真使用 Hermes，这一步基本绕不开。很多网站的数据获取都依赖登录；并且在 AI 执行任务、尤其是训练阶段，你最好能全程看着它在做什么。否则，你根本不知道它是操作正确，还是在胡乱点击，你是没有感知的。

所以，这里和前面的一样，需要额外搭建一套可视化环境：搭建 VNC + Brave browser 的环境，让 AI 的每一步操作都你可见。一方面方便调试和排错，另一方面也更容易理解和优化它的操作。

  


1、安装与配置VNC

安装图形界面（xfce）和VNC服务（tightvncserver）。

![](https://mmbiz.qpic.cn/mmbiz_png/r4mqujZZ0rALInpJl62QVbHj3gvPTZKK8Jesicnib671p76Qj18SJIut4ZFe5sWzBRhpliahsiaR9JYWXDk5ia3tAHMK1KHuGLSOcbaP1DjC6mPA/640?wx_fmt=png&from=appmsg)

配置启动参数，并使用 systemd 来托管 vncserver 服务，保证稳定运行。

  *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   * 

    
    
    root@ubuntu:~# sudo usermod -aG sudo hermesroot@ubuntu:~# su - hermes  
    hermes@ubuntu:~$ vncserver  
    New 'X' desktop is ubuntu:2  
    hermes@ubuntu:~$ vncserver -kill :2  
    hermes@ubuntu:~$ vi .vnc/xstartup #!/bin/sh  
    xrdb "$HOME/.Xresources"xsetroot -solid grey  
    unset SESSION_MANAGERunset DBUS_SESSION_BUS_ADDRESS  
    export XAUTHORITY=$HOME/.Xauthorityexec startxfce4 &  
    hermes@ubuntu:~$ mkdir -p ~/.config/systemd/user/hermes@ubuntu:~$ vi ~/.config/systemd/user/vncserver@.service[Unit]Description=Remote desktop service (VNC)After=network.target  
    [Service]Type=forking# 确保在启动前清理掉旧的残留锁文件ExecStartPre=-/usr/bin/vncserver -kill :%iExecStart=/usr/bin/vncserver -depth 24 -geometry 1440x900 :%iExecStop=/usr/bin/vncserver -kill :%i  
    [Install]WantedBy=default.target  
    hermes@ubuntu:~$ sudo loginctl enable-linger hermes  
    hermes@ubuntu:~$ export XDG_RUNTIME_DIR=/run/user/$(id -u)hermes@ubuntu:~$ systemctl --user daemon-reload  
    hermes@ubuntu:~$ systemctl --user enable vncserver@2.servicehermes@ubuntu:~$ systemctl --user restart vncserver@2.service

  


初始化VNC。  


![](https://mmbiz.qpic.cn/mmbiz_png/r4mqujZZ0rD0nfricm4dklMelJHvHW5ITU1xvrUPMafIU72iadB1oibYoMvSStumo1bo61Xls7Ktt7V1h3v6PQYOwiaAo5KticrBHtrSJzeJazr4/640?wx_fmt=png&from=appmsg)

Systemd 托管 VNC服务。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/r4mqujZZ0rDYczR2Z78MTp9sg7OM1KeC1Zib3Na4ibc8jh58ruSsibMWR3sjZ56rcgdqX6FJx4PpdExyFNGpCzwxDtQbUyHb6nY77n9iabrj9GE/640?wx_fmt=png&from=appmsg)

这里 :2 表示用的是第二个端口，使用端口 5902 来连接，即可看到完整桌面环境，也就能实时观察 AI 在浏览器中的操作过程了。![](https://mmbiz.qpic.cn/sz_mmbiz_png/r4mqujZZ0rAXrLSyVXggJn9ndCTgTfspMTlmIx7EQjxmMeZDEHZKNVGreJ3kwcAAuFJceqKht2PBp2ibtC8Uw3IzvVGGw3xycGppScoicTRRs/640?wx_fmt=png&from=appmsg)

  


2、安装浏览器 Brave Browser（需代理）

首先，建议卸载 snap chromium。这个版本限制多，在自动化和权限控制上容易掉坑里，用起来很麻烦。

  *   *   *   *   *   *   *   * 

    
    
    root@ubuntu:~# sudo snap remove chromium  
    root@ubuntu:~# sudo apt autoremove --purge snapd  
    root@ubuntu:~# rm -rf ~/snaproot@ubuntu:~# sudo rm -rf /snapsudo rm -rf /var/snapsudo rm -rf /var/cache/snapd/

再安装 Brave 浏览器。（注意：安装过程中要走代理）。

  *   *   *   *   *   *   *   *   * 

    
    
    root@ubuntu:~# export PROXY="http://127.0.0.1:10808"root@ubuntu:~# sudo curl -x "$PROXY" -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg  
    root@ubuntu:~# echo "deb [arch=arm64 signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main" | sudo tee /etc/apt/sources.list.d/brave-browser-release.list  
    root@ubuntu:~# sudo apt -o Acquire::http::Proxy="$PROXY" -o Acquire::https::Proxy="$PROXY" updateroot@ubuntu:~# sudo apt -o Acquire::http::Proxy="$PROXY" -o Acquire::https::Proxy="$PROXY" install brave-browser -y  
    root@ubuntu:~# reboot 

  


![](https://mmbiz.qpic.cn/sz_mmbiz_png/r4mqujZZ0rBDPJJ2T7dH17DS2cjmHBWmZTZTDWj9r7icmIfy265vGhAhibEoicC6cvdgCOeOqiaPVyo2JAJ0k4tBp7iaKgBUgwVic4jVfiamymqDVs/640?wx_fmt=png&from=appmsg)

  


浏览器科学上网有两种方式：

一、启动参数指定代理。通过命令行启动时加上 \--proxy-server，简单，但不够灵活。

二、使用浏览器代理插件。安装一个代理插件，后续使用直接走插件，推荐这种方式，更贴近日常使用也更稳定。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/r4mqujZZ0rA8QcthEZGJPHI5PupGZy6HdQusbEHK8GgfvFDM7NGFZFibLGelwSibP2nBx6Im1aabvj5eB3GwLLmdhg4nqib6wehmpFwD1HibDibo/640?wx_fmt=png&from=appmsg)

  


## 四、验证一下：让它推荐自己

![](https://mmbiz.qpic.cn/mmbiz_png/r4mqujZZ0rAEaPbiccjZVuX1KvJBUjKBgwLrOAn688cudTFiazqUJxt4Je9hAticjtKjo6PXpwCetfmsOg9Jg9FSicfKBKzZmWEVd6yHothibS5I/640?wx_fmt=png&from=appmsg)

真是一言不合就建Skill啊。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/r4mqujZZ0rCHclS8Dz5tUhwxLhKXNf5m5vZxJy5ALLNruecnN9Lk9LQyPDtQiaaNiaic5Hg9kKPAq88NgYkiag9mBOZbS4AEAhtBozJ3HwmcdAk/640?wx_fmt=png&from=appmsg)

先去支持一颗❤️：https://github.com/NousResearch/hermes-agent

  


## 小结

到这里，一个具备自我成长的 Hermes Agent 就基本搭建完成了。

核心链路上，消息平台飞书、大模型和 Hermes Agent 都已经跑通；重要外围环境里，VNC 和浏览器 这些感知的基础设施也准备就绪了。

至于它说的自我成长，光安装跑起来还不太够，先实际用它几天再看。

  


顺便感叹一句，现在搭飞书机器人真太 TMD 的太简单了！

只需要扫个码，新建一个应用，权限、事件、回调这些配置一应俱全，开箱即用。相比以前手搓并且容易出问题，现在这种全家桶式的一键配置确实省事又省心，多多益善！

  

