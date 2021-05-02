FROM ubuntu:20.04 AS builder
COPY getCookies/requirements.txt /requirements.txt
WORKDIR /
RUN sed -i 's/^\(deb\|deb-src\) \([^ ]*\) \(.*\)/\1 http:\/\/mirrors.ustc.edu.cn\/ubuntu \3/' /etc/apt/sources.list \
    && apt update && apt install -y curl python3 \
    && apt install -y libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev \
    && apt install -y jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python get-pip.py \
    && python -m pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple pip -U \
    && python -m pip config set global.index-url https://mirrors.ustc.edu.cn/pypi/web/simple \
    && python -m pip install --upgrade pip \
    && python -m pip install uwsgi \
    && python -m pip install --upgrade -r requirements.txt

FROM ubuntu:20.04
ENV DEBIAN_FRONTEND="noninteractive"
COPY --from=builder /usr/local/lib /usr/local/lib
RUN sed -i 's/^\(deb\|deb-src\) \([^ ]*\) \(.*\)/\1 http:\/\/mirrors.ustc.edu.cn\/ubuntu \3/' /etc/apt/sources.list \
    && apt update && apt install -y tzdata python3 uwsgi-plugin-python3 \
    && echo "Asia/Shanghai" > /etc/timezone && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && mkdir getCookies

COPY getCookies/ /getCookies
WORKDIR /getCookies
EXPOSE ${PORT}