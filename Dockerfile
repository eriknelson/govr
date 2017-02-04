FROM alpine:3.5
MAINTAINER Erik Nelson <erik@nsk.io>

RUN apk update && apk add --no-cache python2 py2-pip go
COPY entrypoint.sh /usr/bin

ENTRYPOINT ["entrypoint.sh"]
