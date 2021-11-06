#!/bin/sh

cd /Run_JDScripts_Docker || exit 1
git checkout .
git pull

cd /scripts || exit 1
git checkout .
git pull

npm install || npm install --registry=https://registry.npm.taobao.org || exit 1
python3 -m pip install --upgrade -r /scripts/requirements.txt

crontab /Run_JDScripts_Docker/crontab.sh
crontab -l
