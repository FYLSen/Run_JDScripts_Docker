FROM ubuntu:20.04

LABEL authors="Rhysn"

ARG scriptsgiturl

RUN sed -i 's/^\(deb\|deb-src\) \([^ ]*\) \(.*\)/\1 http:\/\/mirrors.ustc.edu.cn\/ubuntu \3/' /etc/apt/sources.list \
    && apt update && apt install -y bash git wget tzdata nodejs npm curl moreutils \
    && echo "Asia/Shanghai" > /etc/timezone && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
        && npm install typescript ts-node pm2 \
    && npm install canvas --build-from-source

WORKDIR /

RUN git clone $scriptsgiturl /scripts \
    && git clone https://gitee.com/rhysn/Run_JDScripts_Docker.git /Run_JDScripts_Docker \
    && mkdir ShareCodes
    

RUN bash /Run_JDScripts_Docker/sync.sh

CMD ["crond", "-f"]