#!/bin/bash

#curl -s -S -L --retry 33 ${SHARECODES_URL} > /Run_JDScripts_Docker/ShareCodes/Default.sh
if [ ! -d "/ShareCodes" ]; then
  mkdir /ShareCodes
fi
curl -s -S -L --retry 33 ${SHARECODES_TEMP_URL} > /ShareCodes/Temp.sh
