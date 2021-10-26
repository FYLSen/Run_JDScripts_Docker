FROM ubuntu:20.04

LABEL authors="Rhysn"

ARG scriptsgiturl

ENV DEBIAN_FRONTEND noninteractive

RUN sed -i 's/^\(deb\|deb-src\) \([^ ]*\) \(.*\)/\1 http:\/\/mirrors.ustc.edu.cn\/ubuntu \3/' /etc/apt/sources.list \
    && apt update && apt install -y --fix-missing bash git wget tzdata npm curl moreutils cron sudo \
    && echo "Asia/Shanghai" > /etc/timezone && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - \
    && apt install -y nodejs \
    && apt clean autoclean \
    && apt autoremove --yes \
    && rm -rf /var/lib/{apt,dpkg,cache,log} \
    && service cron start \
    && npm install -g npm \
    && npm config set registry=http://registry.npm.taobao.org \
    && npm install -g typescript ts-node pm2

WORKDIR /

RUN git clone $scriptsgiturl /scripts \
    && git clone https://gitee.com/rhysn/Run_JDScripts_Docker.git /Run_JDScripts_Docker \
    && mkdir ShareCodes
    

RUN bash /Run_JDScripts_Docker/sync.sh

CMD ["cron", "-f"]