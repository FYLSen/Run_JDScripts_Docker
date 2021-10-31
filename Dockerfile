FROM ubuntu:20.04

LABEL authors="Rhysn"

ENV DEBIAN_FRONTEND="noninteractive"
# 安装基础环境
RUN sed -i 's/^\(deb\|deb-src\) \([^ ]*\) \(.*\)/\1 http:\/\/mirrors.ustc.edu.cn\/ubuntu \3/' /etc/apt/sources.list \
    && apt update && apt install -y --no-install-recommends --fix-missing sudo bash git wget curl tzdata moreutils cron \
    && echo "Asia/Shanghai" > /etc/timezone && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && service cron start \
    # 安装node、TypeScript环境    
    && curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - \
    && apt install -y --no-install-recommends --fix-missing nodejs \
    && npm install -g npm \
    && npm config set registry=http://registry.npm.taobao.org \
    && npm install -g typescript ts-node pm2
    # 配置python3环境
    && apt install -y --no-install-recommends --fix-missing uwsgi python3-distutils uwsgi-plugin-python3 \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py \
    && python -m pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple pip -U \
    && python -m pip config set global.index-url https://mirrors.ustc.edu.cn/pypi/web/simple \
    && python -m pip install --upgrade pip \
    #apt清理
    && apt clean autoclean \
    && apt autoremove --yes \
    && rm -rf /var/lib/{apt,dpkg,cache,log}
    
WORKDIR /

CMD ["cron", "-f"]