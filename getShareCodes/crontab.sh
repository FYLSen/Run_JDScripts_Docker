#!/bin/bash
#20 * * * * sh -c "sh /Run_JDScripts_Docker/getShareCodes/running.sh getDefaultShareCodes getTempShareCodes > /logs/getShareCodes.log 2>&1 | sed 's/^/ 【生成邀请码文件】/'; "
#20 * * * * sh -c "sh /Run_JDScripts_Docker/getShareCodes/running.sh getDefaultShareCodes > /logs/getDefaultShareCodes.log 2>&1 | sed 's/^/ 【生成持久邀请码文件】/'; "
12 0 * * * sh -c "sh /Run_JDScripts_Docker/getShareCodes/running.sh getDefaultShareCodes > /logs/getTempShareCodes.log 2>&1 | sed 's/^/ 【生成临时邀请码文件】/'; "
12 1 * * * sh -c "sh /Run_JDScripts_Docker/getShareCodes/Scripts/Shell/get_jd_SmallHomeInviteCode.sh jd4 jd3 jd2 jd1 > /logs/getShellShareCodes.log 2>&1 | sed 's/^/ 【生成京东小屋邀请码文件】/'; "
