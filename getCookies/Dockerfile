FROM python:3.9.4-slim AS builder

COPY getCookies/requirements.txt /requirements.txt
WORKDIR /
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    && apt update && apt install --no-cache curl \
    && apt install --no-cache libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev \
    && apt install --no-cache jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python get-pip.py \
    && python -m pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple pip -U \
    && python -m pip config set global.index-url https://mirrors.ustc.edu.cn/pypi/web/simple \
    && python -m pip install --upgrade pip \
    && python -m pip install uwsgi \
    && python -m pip install --upgrade -r requirements.txt


FROM python:3.9.4-alpine3.13

COPY --from=builder /usr/local/lib /usr/local/lib
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    && apt update && apt install --no-cache tzdata uwsgi-plugin-python3 \
    && echo "Asia/Shanghai" > /etc/timezone && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && mkdir getCookies

COPY getCookies/ /getCookies
WORKDIR /getCookies
EXPOSE ${PORT}

CMD ["uwsgi", "uwsgi.ini"]