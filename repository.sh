#!/bin/bash

cd /repository
if [ ! -d "Rhysn" ]; then
    git clone https://gitee.com/Rhysn/jd_scripts.git Rhysn
else
    cd Rhysn
    git checkout .
    git pull
    npm install || npm install --registry=https://registry.npm.taobao.org
    python3 -m pip install --upgrade -r requirements.txt
fi

cd /repository
if [ ! -d "JDHelloWorld" ]; then
    git clone https://github.com/JDHelloWorld/jd_scripts.git JDHelloWorld
else
    cd JDHelloWorld
    git checkout .
    git pull
    npm install || npm install --registry=https://registry.npm.taobao.org
fi

cd /repository
if [ ! -d "zero205" ]; then
    git clone https://github.com/zero205/JD_tencent_scf.git zero205
else
    cd zero205
    git checkout .
    git pull
    npm install || npm install --registry=https://registry.npm.taobao.org
fi

cd /repository
if [ ! -d "ClassmateLin" ]; then
    git clone https://github.com/ClassmateLin/jd_scripts.git ClassmateLin
else
    cd ClassmateLin
    git checkout .
    git pull
    pip install -r requirements.txt
fi

cd /repository
if [ ! -d "asd920" ]; then
    git clone https://github.com/asd920/Auto-jd.git asd920
else
    cd asd920
    git checkout .
    git pull
    npm install || npm install --registry=https://registry.npm.taobao.org
fi
