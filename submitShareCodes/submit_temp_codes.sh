#!/bin/bash

curl -s -S -L https://rules.allgreat.xyz/Scripts/JD/InviteCodes/jd_carnivalcity > jd_carnivalcity


(
  sleep 5
  ### @Turing_Lab_Bot
  ###818
  echo "msg Turing_Lab_Bot /submit_activity_codes carnivalcity $(cat jd_carnivalcity) "
  echo "safe_quit"
) | docker exec -i RWSAC telegram-cli -N -W
