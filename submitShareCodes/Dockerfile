FROM alpine:latest AS BUILD
# MAINTAINER Gustavo Angulo <woakas@ubidots.com>

RUN apk --no-cache add readline readline-dev libconfig libconfig-dev lua \
    lua-dev luajit-dev luajit openssl openssl-dev \
    build-base libevent libevent-dev python-dev \
    jansson jansson-dev git
RUN git clone --recursive https://github.com/vysheng/tg.git /tg

WORKDIR /tg
RUN ./configure && make

# Binary telegram-cli
FROM alpine:latest

WORKDIR /
ENV TZ=Asia/Shanghai
RUN apk add --no-cache  libevent jansson libconfig libexecinfo \
    readline lua openssl \
    cron tzdata \
    && rm -rf /var/cache/apk/* \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone 
RUN adduser -D telegramd \
    && mkdir -p /home/telegramd/.telegram-cli \
    && chown -R telegramd:telegramd /home/telegramd/.telegram-cli

#VOLUME ["/home/telegramd/.telegram-cli"]
COPY --from=build /tg/bin/telegram-cli /bin/telegram-cli
COPY /key/tg-server.pub tg-server.pub

EXPOSE 2391

CMD telegram-cli -k ./tg-server.pub


