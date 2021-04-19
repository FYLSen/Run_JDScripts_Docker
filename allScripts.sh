#!/bin/bash

curl -s -S -L ${ALL_SCRIPTS_URL}/alljdscripts/${DOCKER_REPOSITORY_URL} > runScripts.sh && sh runScripts.sh
rm -rf runScripts.sh
