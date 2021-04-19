#!/bin/bash
cd `dirname $0`
num=0
sharecodes=""
for item in "$@"; do
    path="/logs/${item}/jd_small_home.log"
    sharecode=$(cat ${path} | grep '您的东东小窝shareCode(每天都是变化的)' | sed 's/您的东东小窝shareCode(每天都是变化的):【//g' | sed 's/】//g')
    if [ $num -eq 0 ]
    then
        sharecodes="\"${sharecode}\""
    else
        sharecodes="${sharecodes},\"${sharecode}\""
    fi
    let num+=1
done

sharecodes_json="{\"inviteCode\":[${sharecodes}]}"
echo ${sharecodes_json} > /Repository/${SHARECODESPATH}/jd_updateSmallHomeInviteCode.json

cd /Repository
git pull
COMMITMESSAGE="东东小窝邀请码更新于 "$(date)
git add .
git commit -m "${COMMITMESSAGE}"
git push origin main

