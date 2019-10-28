#!/bin/bash

yum update -y && yum install docker -y

systemctl enable --now docker

mkdir -p /etc/v2ray

touch /etc/v2ray/config.json

filename="/etc/v2ray/config.json"

cat>"${filename}"<<EOF
{
  "log": {
    "access": "/var/log/v2ray/access.log",
    "error": "/var/log/v2ray/error.log",
    "loglevel": "warning"
  },
  "dns": {},
  "stats": {},
  "inbounds": [
    {
      "port": 3333,
      "protocol": "shadowsocks",
      "settings": {
        "email": "love@v2ray.com",
        "method": "aes-128-gcm",
        "password": "abouqetmsvxzknhf",
        "level": 0,
        "ota": false,
        "network": "tcp,udp"
      },
      "tag": "in-0",
      "streamSettings": {
        "network": "tcp",
        "security": "none",
        "tcpSettings": {}
      }
    }
  ],
  "outbounds": [
    {
      "tag": "direct",
      "protocol": "freedom",
      "settings": {}
    },
    {
      "tag": "blocked",
      "protocol": "blackhole",
      "settings": {}
    }
  ],
  "routing": {
    "domainStrategy": "AsIs",
    "rules": [
      {
        "type": "field",
        "ip": [
          "geoip:private"
        ],
        "outboundTag": "blocked"
      }
    ]
  },
  "policy": {},
  "reverse": {},
  "transport": {}
}
EOF

docker run -d --name v2ray --restart=always -v /etc/v2ray:/etc/v2ray -p 53961:3333/tcp -p 53961:3333/udp v2ray/official  v2ray -config=/etc/v2ray/config.json
