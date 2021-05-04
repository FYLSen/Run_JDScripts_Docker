FROM alpine:latest

LABEL authors="Rhysn"

ARG scriptsgiturl

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    && apk update && apk add --no-cache bash git wget tzdata nodejs npm curl moreutils \
    && rm -rf /var/cache/apk/* \
    && echo "Asia/Shanghai" > /etc/timezone && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && git config --global pull.ff only

WORKDIR /

RUN git clone $scriptsgiturl /scripts \
    && git clone https://gitee.com/rhysn/Run_JDScripts_Docker.git /Run_JDScripts_Docker \
    && mkdir ShareCodes
    

RUN bash /Run_JDScripts_Docker/sync.sh

CMD ["crond", "-f"]