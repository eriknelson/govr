#!/bin/sh
# TODO: Needs to accept params

export GOPATH=/go

# sed -i 's/#ServerName www.example.com:80/ServerName donnager.koopa.io:80/' \
#   /etc/apache2/httpd.conf

# Launch apache
httpd -f /etc/apache2/httpd.conf

# Start govr-server
if [[ "$1" == "debug" ]]; then
/govr/main.py -s --server-debug --server-host=0.0.0.0 \
  --server-git-repo=https://github.com/eriknelson/govrhub-ex.git
else
/govr/main.py -s --server-host=0.0.0.0 \
  --server-git-repo=https://github.com/eriknelson/govrhub-ex.git
fi
