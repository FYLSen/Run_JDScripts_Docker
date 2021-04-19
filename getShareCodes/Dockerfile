FROM alpine:latest

ARG REPOSITORY_HOST
ARG EMAIL
ARG NAME

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    && apk update && apk add --no-cache tzdata git moreutils curl openssh python3 \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py \
    && python3 -m pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple pip -U \
    && python3 -m pip config set global.index-url https://mirrors.ustc.edu.cn/pypi/web/simple \
    && rm -rf /var/cache/apk/* \
    && echo "Asia/Shanghai" > /etc/timezone && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    &&  git config --global user.email "$EMAIL" \
    &&  git config --global user.name "$NAME"

WORKDIR /
RUN git clone $REPOSITORY_HOST /Repository \
    && git clone https://gitee.com/rhysn/Run_JDScripts_Docker.git /Run_JDScripts_Docker \
    && mkdir shareCodes

RUN sh Run_JDScripts_Docker/getShareCodes/running.sh
    
CMD crontab -l && crond -f