FROM alpine:3.5
MAINTAINER Erik Nelson <erik@nsk.io>

# Go runtime setup
RUN mkdir /lib64 && ln -s /lib/libc.musl-x86_64.so.1 /lib64/ld-linux-x86-64.so.2
# Apache2 runtime setup
RUN mkdir -p /run/apache2

RUN apk update && apk add --no-cache python2 py2-pip curl make apache2 git wget
RUN curl "https://storage.googleapis.com/golang/go1.7.5.linux-amd64.tar.gz" > /tmp/golang.tar.gz && \
    tar -C /usr/local -xzf /tmp/golang.tar.gz && ln -sf /usr/local/go/bin/* /usr/local/bin && \
    rm -rf /tmp/golang.tar.gz

############################################################
# TODO: tmp pip
# Will need to run this from the proper checkout location
COPY src/requirements.pip /tmp
RUN pip install -r /tmp/requirements.pip
############################################################

COPY entrypoint.sh /usr/bin

ENTRYPOINT ["entrypoint.sh"]
