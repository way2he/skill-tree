---
title: Obsidian还在手搓笔记文档吗？掌握这个插件，给Obsidian安装智能引擎，效率翻倍
author: 小二
source: https://mp.weixin.qq.com/s/7IowJH3XbwkiKgXW59Avew
created_at: 2026-04-27 20:18:28
---

# Obsidian还在手搓笔记文档吗？掌握这个插件，给Obsidian安装智能引擎，效率翻倍

小二准则【不为学习而学习，严格遵循
二八法则
】。
AI热潮下，
Obsidian现在很火，都开始安装了Obsidian 这个本地知识库。
但是这个知识库，之所以火，不是简单的因为它的本地化编辑，支持远程同步，以及其知识图谱和丰富的插件。
而是，能够和AI完美组合。
相信，有不少人，安装Obsidian后，还在手搓文档笔记。当然，不是否定手搓的价值，而是需要知道Obsidian结合AI的能力，提升工作效率。
废话不多说，直接开始干活，边干边了解Obsidian怎么和AI结合，以及提效点。
在开始之前，要求已经安装好Obsidian和claude code cli，如果还没安装，可以参考小编前面一篇文章。
安装claudian插件
Claudian是Obsidian的第三方插件，支持在Obsidian里面使用claude code。
1. 进入下载地址，https://github.com/YishenTu/claudian/releases
![](https://mmbiz.qpic.cn/sz_mmbiz_png/KK1PMteXW2cJFluAnOZicXne0wRpzapu0hssyoXicic0iaC8TXlKB4GiczHPibIwmibT98P4nUKxLLw5rOiauVy3JLM9t2IZuU1o4VrI4coSlqCC2wQ/640?wx_fmt=png&from=appmsg)
2. 下载 main.js，manifest.json，styles.css三个文件。
打开Obsidian的知识库，就是创建的vault文件夹，进入
.obsidian
这个文件夹，注意，这个文件夹是点号前缀的，正常情况下是隐藏的。
如果是w
indows系统，
打开指定文件夹，点击顶部的“查看”选项卡，在“显示/隐藏”区域勾选“隐藏的项目” 复选框，隐藏文件就会显示
![](https://mmbiz.qpic.cn/mmbiz_png/KK1PMteXW2dlhmwBL39JpNrADdkzgTZIt5OrmcPJCGQbLibW8FWXhBS9KcACbwkVqq6lCbhX2N6E0Gvgv87l9UxJJkeFDS7XMpicWyDn0b4ZU/640?wx_fmt=png&from=appmsg)
如果是mac，进入指定仓库文件夹后，组合按键
Cmd+Shift+.
就可以看到，如下
![](https://mmbiz.qpic.cn/mmbiz_png/KK1PMteXW2ezLufNibTQicrSnkhVvkTuMRPpdUmIV48SEVbLlIv21TSWLRzCNrXMxfsb45VrTJRaK1XiclnZWibCViaiccFWSmRyXCTrfMDaXIo2Q/640?wx_fmt=png&from=appmsg)
3. 进入
.obsidian
这个文件夹，并创建
claudian文件夹
把下载的
main.js，manifest.json，styles.css
三个文件复制到
claudian文件夹中。
回到obsidian操作界面，在设置中找到第三方插件中的claudian，如果没有，就点击刷新按钮
![](https://mmbiz.qpic.cn/sz_mmbiz_png/KK1PMteXW2c7muFZXmDxfslL5Q24RXXS9fib1YBiaTZMo89dbZM3Ynn0BssWBF8jn7iayY3FKQv9RG23Zo0YaSleCCy7Q4rjORK2MGA1IGYp9M/640?wx_fmt=png&from=appmsg)
启用后，这里就已经完成安装，但是还不能使用claudian，缺一步配置。
如果已经安装claude code，打开终端命令执行器，执行which claude，找到claude code的安装目录
![](https://mmbiz.qpic.cn/sz_mmbiz_png/KK1PMteXW2d1NGf4GdS9q2yyOIPB3zicgA6rW0siatKL9jcSxhoTEAjusaUNpGt0wlesicqg7JMWNuEAkbIhicfKYluxZSPmbGTiaGVJeMRHAzOs/640?wx_fmt=png&from=appmsg)
然后点开claudian插件设置
![](https://mmbiz.qpic.cn/mmbiz_png/KK1PMteXW2cFichTG31o0k7RoIWJUS1yianADwicI5lDaIb7rwsqynsQFy84AENia87EkIqKmOeYYAHphibp6rEdGtibGv5NuIOQsoiaTkE5EpABGg/640?wx_fmt=png&from=appmsg)
在Claude CLI path这一选项中填入刚刚找到的路径
![](https://mmbiz.qpic.cn/mmbiz_png/KK1PMteXW2cS8uKdJ36ic8UOh7G4fPBrFgMN3takU4kzrT1KBmGm7K6ibsYj4LjNO8v7HnWWLicE88N1j62C6TjyTeaeiaULkicJuUao1NFzy64k/640?wx_fmt=png&from=appmsg)
注意，
如果claude已经对接了国内的大模型，在environment这一栏不需要填写baseurl和api key
![](https://mmbiz.qpic.cn/mmbiz_png/KK1PMteXW2dAKFAicuX0xQHA5Mdyibua8pYSI1PdnaH3gibzaoCu5iaOeN2eR3KK6SCjiadqVD57RVzB7w6QjRWdmj2K4YbEAUNUr50bwr8poYyI/640?wx_fmt=png&from=appmsg)
到这里，已经完成了claudian的安装，
可以在有上角看到一个机器人的选择
![](https://mmbiz.qpic.cn/mmbiz_png/KK1PMteXW2dPyZgONj7RftXzvF8hDF88f7rWty1RQVWaksrAbgpgk5VMvs72ZkXvgZQQkBTkN5icaSria8d5R5ia4GFiaLDtseyrATGGibbuslp8/640?wx_fmt=png&from=appmsg)
安装好了之后，我们试一下效果，比如我想了解《金字塔原理》这本书的核心内容，让ai帮我写一份大纲文档，如图，AI已经开始工作。
![](https://mmbiz.qpic.cn/sz_mmbiz_png/KK1PMteXW2emVJDTxJuJrvnVMlhuWpXV56a1KYveLibAGLia8BcDhxPgTaGaRX16WlsibaKB2AibHLf26SELEgUFoAjwBtG8iaLDxxFUTNFHibKB8/640?wx_fmt=png&from=appmsg)
默默等待完成...，最终效果如下，已经完成一篇AI整理的文档
![](https://mmbiz.qpic.cn/sz_mmbiz_png/KK1PMteXW2c82EhBE9sP0pMNt3rh4lkib0md8qzVqoDWPlQL7FZE8vnKkSm6oDiblRInBVZ17xF8pnJiabmYouuBiaUW5CyiavCqzIUHDxTJ4QT0/640?wx_fmt=png&from=appmsg)
AI已经完美集成到Obsidian知识库当中，写文档，整理文档，都是不错的工具。
最后，小二想说，AI只是工具，落在知识库的文档再多，如果不看，不思考，不沉淀，也只是一堆文字垃圾。
我是小二，一线互联网大厂架构师，在AI热潮下，专注AIGC摸索。
如果文章有帮助，帮忙点个赞，
**关注**
不迷路。
往期推荐
[AI时代怎么打造个人专属的知识库？Obsidian完美契合，5分钟教程完成本地搭建](https://mp.weixin.qq.com/s?__biz=MzE5ODA5OTY1MQ==&mid=2247483818&idx=1&sn=bf355dfd6074c0b7e031b5f64ba988fd&scene=21#wechat_redirect)
[阿里云部署OpenClaw使用百炼套餐太贵?15分钟接入智谱Coding Plan](https://mp.weixin.qq.com/s?__biz=MzE5ODA5OTY1MQ==&mid=2247483792&idx=1&sn=a8f8b26e7392ed192bc543be5bd4dd35&scene=21#wechat_redirect)

---

*本文由微信文章下载器自动抓取，原文链接：https://mp.weixin.qq.com/s/7IowJH3XbwkiKgXW59Avew
