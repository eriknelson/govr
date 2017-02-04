FROM alpine:3.5
MAINTAINER Erik Nelson <erik@nsk.io>

RUN apk update && apk add --no-cache python2 py2-pip curl make
RUN mkdir /lib64 && ln -s /lib/libc.musl-x86_64.so.1 /lib64/ld-linux-x86-64.so.2
RUN curl "https://storage.googleapis.com/golang/go1.7.5.linux-amd64.tar.gz" > /tmp/golang.tar.gz && \
    tar -C /usr/local -xzf /tmp/golang.tar.gz && ln -sf /usr/local/go/bin/* /usr/local/bin && \
    rm -rf /tmp/golang.tar.gz

COPY entrypoint.sh /usr/bin

ENTRYPOINT ["entrypoint.sh"]
