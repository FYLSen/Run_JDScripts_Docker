#!/bin/bash

if [ ! -d "/Repository" ]; then
  git clone ${REPOSITORY_HOST} Repository || exit 1
fi

cd /Run_JDScripts_Docker || exit 1
git pull && python3 -m pip install -r /Run_JDScripts_Docker/getShareCodes/requirements.txt

for item in "$@"; do 
    python3 /Run_JDScripts_Docker/getShareCodes/Scripts/${item}.py
done

cd /Repository || exit 1
git pull
cp -rf /shareCodes/* /Repository/${SHARECODESPATH}/

COMMITMESSAGE="邀请码更新于 "$(date)
git add .
git commit -m "${COMMITMESSAGE}"
git push origin main

rm -rf /sharCodes/*

crontab /Run_JDScripts_Docker/getShareCodes/crontab.sh
crontab -l
