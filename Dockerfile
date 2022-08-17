FROM python3.8_pip3_libs:0.9.6

RUN apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . /

EXPOSE 7788

ENTRYPOINT /bin/sh start.sh