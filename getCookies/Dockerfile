FROM ubuntu:20.04

COPY getCookies/ /getCookies
WORKDIR /getCookies

ENV DEBIAN_FRONTEND="noninteractive"

RUN sed -i 's/^\(deb\|deb-src\) \([^ ]*\) \(.*\)/\1 http:\/\/mirrors.ustc.edu.cn\/ubuntu \3/' /etc/apt/sources.list \
    && apt update && apt install -y curl tzdata python3 python3-distutils uwsgi-plugin-python3 python3-dev gcc \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py \
    && python -m pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple pip -U \
    && python -m pip config set global.index-url https://mirrors.ustc.edu.cn/pypi/web/simple \
    && python -m pip install --upgrade pip \
    && python -m pip install uwsgi \
    && python -m pip install --upgrade -r requirements.txt \
    && echo "Asia/Shanghai" > /etc/timezone && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

EXPOSE ${PORT}

CMD ["uwsgi", "--init", "uwsgi.ini"]