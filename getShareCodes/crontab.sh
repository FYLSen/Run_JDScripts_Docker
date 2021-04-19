#!/bin/bash
#20 * * * * sh -c "sh /Run_JDScripts_Docker/getShareCodes/running.sh getDefaultShareCodes getTempShareCodes > /logs/gsc/getShareCodes.log 2>&1 | sed 's/^/ 【生成邀请码文件】/'; "
#20 * * * * sh -c "sh /Run_JDScripts_Docker/getShareCodes/running.sh getDefaultShareCodes > /logs/gsc/getDefaultShareCodes.log 2>&1 | sed 's/^/ 【生成持久邀请码文件】/'; "
9 0 * * * sh -c "sh /Run_JDScripts_Docker/getShareCodes/running.sh getTempShareCodes > /logs/gsc/getTempShareCodes.log 2>&1 | sed 's/^/ 【生成临时邀请码文件】/'; "
50 4 * * * sh -c "sh /Run_JDScripts_Docker/getShareCodes/Scripts/Shell/get_jd_SmallHomeInviteCode.sh jd4 jd3 jd2 jd1 > /logs/gsc/getShellShareCodes.log 2>&1 | sed 's/^/ 【生成京东小屋邀请码文件】/'; "
