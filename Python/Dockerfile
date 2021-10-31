FROM python:alpine3.14

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    && apk update && apk add --no-cache tzdata git moreutils curl openssh wget \
    && git config --global pull.ff only \
    && rm -rf /var/cache/apk/* \
    && echo "Asia/Shanghai" > /etc/timezone && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime 
    
WORKDIR /
    
CMD ["crond", "-f"]
