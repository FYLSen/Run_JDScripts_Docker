#!/bin/bash

#curl -s -S -L ${SHARECODES_URL} > /Run_JDScripts_Docker/ShareCodes/Default.sh
if [ ! -d "/ShareCodes" ]; then
  mkdir /ShareCodes
fi
curl -s -S -L ${SHARECODES_TEMP_URL} > /ShareCodes/Temp.sh
