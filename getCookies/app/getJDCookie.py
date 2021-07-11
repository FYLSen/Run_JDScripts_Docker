#!/bin/python3
# -*- coding:utf-8 -*-

import requests, time, os, multiprocessing, json
from flask import Flask, render_template
import jdCookies.cookies as cks

app = Flask(__name__)

def getEnv():
    return {
        "masterPtPin": os.environ.get('MASTERPtPin')
    }
    
def saveCookies(message):
    session = requests.Session()
    loginInfo = cks.token_get(session)
    qrInfo, qr_base64 = cks.token_post(loginInfo, session)
    message.put({'qr_base64': qr_base64,'okl_token':qrInfo['okl_token']})
    pt_key, pt_pin = cks.check_token(qrInfo['token'], qrInfo['okl_token'], session)
    
    if not pt_key:
        saveLogs(qrInfo['okl_token'], "error")
        return '获取Cookie失败'

    saveLogs(qrInfo['okl_token'], "getsuccess")

    env = getEnv()
    
    env['container'] = os.environ.get('MASTER_CONTAINER').split('&') if pt_pin in env["masterPtPin"] else os.environ.get('CONTAINER_NAME').split('&')

    filePath = []
    for item in env['container']:
        filePath.append('/config/%s/cookies.sh' % item)

    saveLogs(qrInfo['okl_token'], "writing")

    cookiesFileInfo, thepath = cks.getCookieFilesInfo(pt_pin, pt_key, filePath)

    cks.saveFiles(cookiesFileInfo, thepath, env['masterPtPin'])

    saveLogs(qrInfo['okl_token'], "success")

def saveLogs(token, status):
    logsPath = r'/logs/%s.json' % token
    with open(logsPath, 'w') as f:
        f.write('{"status": "%s"}' % status)

@app.route('/status/<token>')
def getstatus(token):
    statusdir = '/logs/%s.json' % token
    try:
        with open(statusdir, 'r') as f:
            jsonStr = json.load(f)
            return json.dumps(jsonStr)
    except FileNotFoundError:
        return {'status': 'waitting'}

@app.route('/')
def index():
    message = multiprocessing.Queue()
    p = multiprocessing.Process(target=saveCookies, args=(message,))
    p.start()
    time.sleep(1)
    messageInfo = message.get(True)

    return render_template('index.html',message = messageInfo)

if __name__ == '__main__':

    app.run()
    

    