FROM alpine:latest

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    && apk update && apk add --no-cache tzdata git moreutils curl openssh python3 \
    && git config --global pull.ff only \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py \
    && python3 -m pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple pip -U \
    && python3 -m pip config set global.index-url https://mirrors.ustc.edu.cn/pypi/web/simple \
    && rm -rf /var/cache/apk/* \
    && echo "Asia/Shanghai" > /etc/timezone && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && git clone https://gitee.com/rhysn/Run_JDScripts_Docker.git /Run_JDScripts_Docker \
    && mkdir shareCodes
    
WORKDIR /

RUN crontab /Run_JDScripts_Docker/getShareCodes/crontab.sh
    
CMD crontab -l && crond -f
