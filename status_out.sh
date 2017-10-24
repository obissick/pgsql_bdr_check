#!/bin/bash
if [ $1 = "r" ]; then
  echo -en "HTTP/1.1 200 PostgreSQL BDR Node is ready.\r\n"
  echo -en "Content-Type: text/plain\r\n"
  echo -en "Connection: close\r\n"
  echo -en "Content-Length: 40\r\n"
  echo -en "\r\n"
  echo -en "Cluster Node is ready.\r\n"
  sleep 0.1
  exit 0
else
  echo -en "HTTP/1.1 503 PostgreSQL BDR is not ready.\r\n"
  echo -en "Content-Type: text/plain\r\n"
  echo -en "Connection: close\r\n"
  echo -en "Content-Length: 44\r\n"
  echo -en "\r\n"
  echo -en "Cluster Node is not ready.\r\n"
  sleep 0.1
  exit 1
fi
