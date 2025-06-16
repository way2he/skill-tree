# Ubuntu 别名推荐大全

## 简介
别名(alias)是Linux系统中提高命令行效率的强大工具，它允许用户为常用命令创建简短的快捷方式。本指南提供了一套全面的Ubuntu别名推荐，涵盖系统管理、文件操作、网络工具等多个方面，帮助您显著提升终端工作效率。

## 一、基础设置方法

### 1. 临时别名（当前终端有效）
```bash
# 语法：alias 别名='原命令'
alias ll='ls -l'
```

### 2. 永久别名（推荐方法）
编辑`~/.bashrc`文件添加别名：
```bash
nano ~/.bashrc
# 在文件末尾添加别名配置
# 保存后执行以下命令使配置生效
source ~/.bashrc
```

### 3. 专用别名文件（高级用法）
```bash
# 创建专用别名文件
touch ~/.bash_aliases
# 在.bashrc中添加以下内容使系统加载该文件
echo 'if [ -f ~/.bash_aliases ]; then . ~/.bash_aliases; fi' >> ~/.bashrc
# 以后所有别名都添加到.bash_aliases文件中
nano ~/.bash_aliases
```

## 二、系统管理别名

### 更新与升级
```bash
alias update='sudo apt update && sudo apt upgrade -y'
alias full-upgrade='sudo apt full-upgrade -y'
alias dist-upgrade='sudo apt dist-upgrade -y'
alias autoremove='sudo apt autoremove -y'
alias autoclean='sudo apt autoclean'
alias clean='sudo apt clean'
```

### 系统信息
```bash
alias sysinfo='neofetch'
alias cpu='lscpu'
alias mem='free -h'
alias disk='df -h'
alias du='du -h'
alias top='htop'
alias processes='ps aux'
alias ip='ip addr show'
alias ports='netstat -tulpn'
```

## 三、文件操作别名

### 目录导航
```bash
alias ..='cd ..'
alias ...='cd ../../'
alias ....='cd ../../../'
alias .....='cd ../../../../'
alias ~='cd ~'
alias home='cd ~'
alias desk='cd ~/Desktop'
alias doc='cd ~/Documents'
alias down='cd ~/Downloads'
alias pwd='pwd -P'
```

### 目录列表
```bash
alias ls='ls --color=auto'
alias ll='ls -l --color=auto'
alias la='ls -la --color=auto'
alias lh='ls -lh --color=auto'
alias l='ls -CF --color=auto'
alias lsa='ls -lah --color=auto'
alias tree='tree -C'
```

### 文件管理
```bash
alias cp='cp -i'
alias mv='mv -i'
alias rm='rm -i'
alias mkdir='mkdir -p'
alias rmdir='rmdir -v'
alias chmod='chmod -v'
alias chown='chown -v'
alias ln='ln -v'
```

### 文件搜索
```bash
alias findf='find . -type f -name'
alias findd='find . -type d -name'
alias grep='grep --color=auto'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'
alias rg='rg --color=always'
```

## 四、压缩与解压
```bash
alias tar='tar -v'
alias tarc='tar -zcvf'
alias tarx='tar -zxvf'
alias targz='tar -zxvf'
alias tbz='tar -jxvf'
alias tgz='tar -zxvf'
alias zip='zip -r'
alias unzip='unzip'
alias rar='rar a'
alias unrar='unrar x'
```

## 五、网络工具
```bash
alias ping='ping -c 4'
alias fastping='ping -c 100 -s 1'
alias wget='wget -c'
alias curl='curl -O'
alias ipinfo='curl ipinfo.io'
alias speedtest='curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python3 -'
alias ports='sudo netstat -tulpn'
alias ssh='ssh -v'
```

## 六、Docker 别名
```bash
alias dk='docker'
alias dki='docker images'
alias dkc='docker ps -a'
alias dkr='docker run'
alias dkrm='docker rm'
alias dkstop='docker stop'
alias dkstart='docker start'
alias dkrestart='docker restart'
alias dklogs='docker logs -f'
alias dkexec='docker exec -it'

alias dkc='docker-compose'
alias dkcu='docker-compose up -d'
alias dkcd='docker-compose down'
alias dkcr='docker-compose restart'
```

## 七、Git 别名
```bash
alias g='git'
alias ga='git add'
alias gaa='git add .'
alias gc='git commit -m'
alias gcm='git commit -m'
alias gco='git checkout'
alias gcb='git checkout -b'
alias gs='git status'
alias gp='git push'
alias gl='git pull'
alias gm='git merge'
alias gb='git branch'
alias gba='git branch -a'
alias gd='git diff'
alias gpl='git pull'
alias gps='git push'
```

## 八、开发工具
```bash
alias py='python3'
alias python='python3'
alias pip='pip3'
alias pipi='pip install'
alias pipu='pip uninstall'
alias pipu='pip install --upgrade'
alias pipreq='pip freeze > requirements.txt'
alias npm='npm '
alias npmi='npm install'
alias npmu='npm uninstall'
alias npmr='npm run'
alias npx='npx '
alias mvn='mvn '
alias gradle='gradle '
```

## 九、实用工具
```bash
alias c='clear'
alias h='history'
alias j='jobs'
alias cls='clear'
alias q='exit'
alias which='which -a'
alias path='echo -e ${PATH//:/\n}'
alias now='date +"%Y-%m-%d %H:%M:%S"'
alias timestamp='date +%s'
alias weather='curl wttr.in'
alias calculator='bc -l'
```

## 十、安全与权限
```bash
alias myip='curl icanhazip.com'
alias ports='sudo netstat -tulpn'
alias firewall='sudo ufw status'
alias sshkey='cat ~/.ssh/id_rsa.pub'
alias chmodx='chmod +x'
```

## 十一、别名管理
```bash
alias aliaslist='alias | sort'
alias savealiases='alias > ~/.bash_aliases_backup'
alias editalias='nano ~/.bash_aliases'
alias reloadalias='source ~/.bash_aliases && echo "Aliases reloaded successfully!"'
```

## 十二、高级别名技巧

### 带参数的别名（函数形式）
```bash
# 创建带参数的别名需要使用函数
alias() { echo "Usage: alias [name[=value] ...]"; } # 覆盖默认alias命令
alias ll='ls -l'

# 示例：带参数的文件搜索函数
search() {
  if [ -z "$1" ]; then
    echo "Usage: search <keyword>"
    return 1
  fi
  grep -rnw . -e "$1"
}

# 示例：创建带日期的备份函数
bak() {
  if [ -z "$1" ]; then
    echo "Usage: bak <file/directory>"
    return 1
  fi
  cp -r "$1" "$1_$(date +%Y%m%d_%H%M%S)"
}
```

### 条件别名
```bash
# 只有当命令存在时才创建别名
command -v htop &> /dev/null && alias top='htop'
command -v exa &> /dev/null && alias ls='exa --color=auto'
command -v bat &> /dev/null && alias cat='bat'
```

## 结语
以上别名集合涵盖了日常Ubuntu系统管理和开发工作的各个方面。您可以根据个人需求选择性地添加到自己的别名配置中。建议定期回顾和优化您的别名集合，以适应不断变化的工作流需求。

记住，最好的别名是能真正提高您工作效率的那些。不要盲目添加所有别名，而是选择那些您真正会使用的命令来创建别名。