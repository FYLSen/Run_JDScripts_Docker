#!/bin/python3
# -*- coding:utf-8 -*-

import requests, time, os, multiprocessing, sys
from flask import Flask, render_template
import jdCookies.cookies as cks

app = Flask(__name__)

def getEnv():
    return {
        "masterPtPin": os.environ.get('MASTERPtPin'),
        "container": os.environ.get('CONTAINER_NAME').split('&')
    }
    
def saveCookies(message):
    session = requests.Session()
    loginInfo = cks.loginEntrance(session)
    qrInfo, qr_base64 = cks.generateQrcode(session, loginInfo)
    message.put({'qr_base64': qr_base64,'okl_token':qrInfo['okl_token']})
    headers = cks.getHeaders(session, loginInfo, qrInfo)
    pt_key, pt_pin = cks.formatCookie(headers)

    env = getEnv()

    for item in env['container']:
        filePath.append('/config/%s/cookies.sh' % item)
    cookiesFileInfo, thepath = cks.getCookieFilesInfo(pt_pin, pt_key, filePath)

    cks.saveFiles(cookiesFileInfo, thepath, env['masterPtPin'])

    sys.exit()

@app.route('/')
def index():
    message = multiprocessing.Queue()
    p = multiprocessing.Process(target=saveCookies, args=(message,))
    p.start()
    time.sleep(1)
    messageInfo = message.get(True)

    return render_template('index.html',message = messageInfo)


if __name__ == '__main__':

    app.run(host = 'localhost', port = int(os.environ.get('PORT')))
    

    