#!/bin/bash

docker create \
 --name RWSAC \
 -e TZ=Asia/Shanghai \
 -v /home/Script/RWSAC:/root/.telegram-cli \
 ugeek/telegram-cli:amd64
 
docker start RWSAC

docker exec -it RWSAC telegram-cli -N -W

docker exec -it RWSAC telegram-cli -k /home/Script/RWSAC/bot_key.pub

docker exec -it RWSAC telegram-cli -W -e "msg Turing_Lab_Bot /count_activity_codes"