FROM alpine:latest

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    && apk update && apk add --no-cache tzdata moreutils python3 curl \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py \
    && python3 -m pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple pip -U \
    && python3 -m pip config set global.index-url https://mirrors.ustc.edu.cn/pypi/web/simple \
    && rm -rf /var/cache/apk/* \
    && echo "Asia/Shanghai" > /etc/timezone && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && mkdir App
    
WORKDIR /
COPY requirements.txt /App/requirements.txt
COPY views /App/views
COPY getJDCookie.py /App/getJDCookie.py
RUN python3 -m pip install -r /App/requirements.txt
    
CMD ["python3", "/App/getJDCookie.py"]
