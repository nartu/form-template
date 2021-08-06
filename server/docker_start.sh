#! /usr/bin/env bash
# debug
# bash -c '/start_reload.sh' &&

bash -c '/start.sh' &&

sleep 2

echo "Populate DB"
curl -XPUT http://0.0.0.0:80/migrate
