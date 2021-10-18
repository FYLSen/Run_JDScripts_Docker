#!/bin/sh

cd /Run_JDScripts_Docker || exit 1
git checkout .
git pull

cd /scripts || exit 1
git checkout .
git pull

npm install || npm install --registry=https://registry.npm.taobao.org || exit 1
npm install -g typescript ts-node pm2 || exit 1

crontab /Run_JDScripts_Docker/crontab.sh
crontab -l
