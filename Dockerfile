FROM node:lts-alpine3.13

LABEL authors="Rhysn"

ARG scriptsgiturl

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    && apk update && apk add --no-cache bash git wget tzdata curl moreutils build-base g++ cairo-dev pango-dev giflib-dev \
    && rm -rf /var/cache/apk/* \
    && echo "Asia/Shanghai" > /etc/timezone && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && git config --global pull.ff only \
    && npm install typescript ts-node pm2 \
    && npm install canvas --build-from-source

WORKDIR /

RUN git clone $scriptsgiturl /scripts \
    && git clone https://gitee.com/rhysn/Run_JDScripts_Docker.git /Run_JDScripts_Docker \
    && mkdir ShareCodes

RUN bash /Run_JDScripts_Docker/sync.sh

CMD ["crond", "-f"]