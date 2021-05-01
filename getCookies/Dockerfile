FROM python:alpine

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    && apk --update add --no-cache tzdata moreutils curl \
    && apk add --no-cache libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev \
    && apk add --no-cache jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py \
    && python -m pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple pip -U \
    && python -m pip config set global.index-url https://mirrors.ustc.edu.cn/pypi/web/simple \
    && python -m pip install --upgrade pip \
    && python -m pip install uwsgi uwsgi-python3 \
    && rm -rf /var/cache/apk/* \
    && echo "Asia/Shanghai" > /etc/timezone && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && mkdir getCookies

COPY ./getCookies /getCookies
WORKDIR /getCookies
RUN python -m pip install --upgrade -r requirements.txt
EXPOSE ${PORT}

CMD ["uwsgi", "uwsgi.ini"]