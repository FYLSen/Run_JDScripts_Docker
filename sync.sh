#!/bin/sh

cd /Run_JDScripts_Docker || exit 1
git checkout .
git pull

bash repository.sh

crontab /Run_JDScripts_Docker/crontab.sh
crontab -l
