#!/bin/python3
# -*- coding:utf-8 -*-
from PIL import Image
import qrcode, requests, base64, time, re, os, sys

def loginEntrance(session):
    url = 'https://plogin.m.jd.com/cgi-bin/mm/new_login_entrance?lang=chs&appid=300&returnurl=https://wq.jd.com/passport/LoginRedirect?state=%s&returnurl=https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport' % (time.time())
    header = {
        'Connection': 'Keep-Alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-cn',
        'Referer': 'https://plogin.m.jd.com/login/login?appid=300&returnurl=https://wq.jd.com/passport/LoginRedirect?state=%s&returnurl=https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport' % (time.time()),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        'Host': 'plogin.m.jd.com'
    }
    try:
        r = session.get(url, headers=header)
    except Exception as e:
        print('loginEntrance_Error:', e)
    data = r.json()
    setCookie = r.headers['Set-Cookie'].split(';')
    for item in setCookie:
        item = item.strip(' ')
        if item.startswith('guid'):
            guid = re.findall('guid=(.+)', item)[0] 
        elif "lsid=" in item:
            temp = re.findall('.*lsid=(.+)', item)
            lsid = lsid if len(temp) == 0 else temp[0]
        elif "lstoken=" in item:
            temp = re.findall('.*lstoken=(.+)', item)
            lstoken = lstoken if len(temp) == 0 else temp[0]
    return {
        'guid': guid,
        'lsid': lsid,
        'lstoken': lstoken,
        's_token': data['s_token'],
        'cookies': "guid=%s; lang=chs; lsid=%s; lstoken=%s; " % (guid, lsid, lstoken)
    }

def generateQrcode(session, loginInfo):
    url = 'https://plogin.m.jd.com/cgi-bin/m/tmauthreflogurl?s_token=%s&v=%s&remember=true' % (loginInfo['s_token'], time.time())
    data = 'lang=chs&appid=300&source=wq_passport&returnurl=https://wqlogin2.jd.com/passport/LoginRedirect?state=%s&returnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action' % (time.time())
    header = {
      'Connection': 'Keep-Alive',
      'Content-Type': 'application/x-www-form-urlencoded',
      'Accept': 'application/json, text/plain, */*',
      'Accept-Language': 'zh-cn',
      'Referer': 'https://plogin.m.jd.com/login/login?appid=300&returnurl=https://wq.jd.com/passport/LoginRedirect?state=%s&returnurl=https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport' % (time.time()),
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
      'Host': 'plogin.m.jd.com'
    }
    try:
        r = session.post(url, data=data, headers=header)
    except Exception as e:
        print('generateQrcode_Error:', e)

    data = r.json()
    setCookie = r.headers['Set-Cookie'].split(';')

    token = data['token']
    for item in setCookie:
        item = item.strip(' ')
        if 'okl_token=' in item:
            okl_token = re.findall('.*okl_token=(.+)', item)[0]

    qrurl = 'https://plogin.m.jd.com/cgi-bin/m/tmauth?appid=300&client_type=m&token=' + token
    qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
    qr.add_data(qrurl)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    path = '%s.png' % loginInfo['s_token']

    with open(path, 'wb') as f:
        img.save(f)
    with open(path, 'rb') as f:
        qr_base64 = 'data:image/png;base64,%s' % base64.b64encode(f.read()).decode()
    if os.path.exists(path):
        os.remove(path)

    return {
        'token': token,
        'okl_token': okl_token
    }, qr_base64
    
def checkLogin(session, loginInfo, qrInfo):
    url = 'https://plogin.m.jd.com/cgi-bin/m/tmauthchecktoken?&token=%s&ou_state=0&okl_token=%s' % (qrInfo['token'], qrInfo['okl_token'])
    data = 'lang=chs&appid=300&source=wq_passport&returnurl=https://wqlogin2.jd.com/passport/LoginRedirect?state=%s&returnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action' % (time.time())
    header = {
        'Referer': 'https://plogin.m.jd.com/login/login?appid=300&returnurl=https://wqlogin2.jd.com/passport/LoginRedirect?state=%s&returnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport' % (time.time()),
        'Cookie': loginInfo['cookies'],
        'Connection': 'Keep-Alive',
        'Content-Type': 'application/x-www-form-urlencoded; Charset=UTF-8',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    }
    try:
        r = session.post(url, data=data, headers=header)
    except Exception as e:
        print('checkLogin_Error:', e)
    return r.json(), r.headers


def getHeaders(session, loginInfo, qrInfo):
    
    while True:
        try:
            data, headers = checkLogin(session, loginInfo, qrInfo)

            if data['errcode'] == 0:
                #登陆成功
                print('[{}]'.format(time.strftime('%H:%M:%S')),data['message'])
                """ pt_key, pt_pin = formatCookie(headers)
                print('&%s;%s;' % pt_key, pt_pin)
                sys.exit() """
                return headers
            elif data['errcode'] == 21:
                #二维码已失效
                print('[{}]'.format(time.strftime('%H:%M:%S')),data['message'])
                sys.exit()
            elif data['errcode'] == 176:
                #等待扫码
                print('[{}]'.format(time.strftime('%H:%M:%S')),data['message'])
            else:
                print('其他异常：%s' % data)
                sys.exit()

            time.sleep(3)

        except Exception as e:
            print('getCookie_Error:', e)

def formatCookie(headers):
    setCookie = headers['Set-Cookie'].split(';')
    for item in setCookie:
        item = item.strip(' ')
        if "pt_key=" in item:
            pt_key = re.findall('.*pt_key=(.+)', item)[0]
        elif "pt_pin=" in item:
            pt_pin = re.findall('.*pt_pin=(.+)', item)[0]
    return pt_key, pt_pin

def getCookieFilesInfo(pt_pin, pt_key, filePath):

    fpInfo = []
    thepath = ''
    oldcookies = ''
    findKey = False

    for fp in filePath:
        with open(fp, 'r') as f:
            ftext = f.read()
            fpInfo.append({'path': fp, 'data': ftext})

    for idx, val in enumerate(fpInfo):
        if pt_pin in val['data']:
            thepath = val['path']
            oldcookies = val['data']
            findKey = True
        temp = val['data'].split('\n')
        for t in temp:
            if t.startswith('JD_COOKIE='):
                fpInfo[idx]['num'] = len(t.split('&'))

    if not (thepath and oldcookies):
        min_idx = 0
        min_num = 0
        for idx,val in enumerate(fpInfo):
            min_num = val['num'] if idx == 0 else min_num
            min_idx = idx if val['num'] <= min_num else min_idx
        thepath = fpInfo[min_idx]['path']
        oldcookies = fpInfo[min_idx]['data']

    settingLine = oldcookies.split('\n')
    numList = []
    for item in settingLine:
        if 'JD_COOKIE=' in item :
            if 'pt_key=$pt_key;' in item:
                numList.append('')
            temp = item.split('&')
            for t in temp:
                tempList = re.findall(r'.+\$pt_pin(\d+);', t) if t.startswith('JD_COOKIE="pt_key=') else re.findall(r'.+\$pt_key(\d+);', t)
                if tempList: numList = numList + tempList
            break
    cookiesFileInfo = []

    for idx, val in enumerate(numList):
        cookiesFileInfo.insert(idx, {'id': idx, 'pt_key': '', 'pt_pin': ''})
        for item in settingLine:
            if item.startswith('pt_key%s=' % val):
                cookiesFileInfo[idx]['pt_key'] = re.sub('pt_key%s=' % val, '', item)
            elif item.startswith('pt_pin%s=' % val):
                cookiesFileInfo[idx]['pt_pin'] = re.sub('pt_pin%s=' % val, '', item)
            if cookiesFileInfo[idx]['pt_key'] and cookiesFileInfo[idx]['pt_pin']:
                break

    if findKey:
        for cki in cookiesFileInfo:
            if cki['pt_pin'] == pt_pin:
                cki['pt_key'] = pt_key
    else:
        cookiesFileInfo.append({'id': len(cookiesFileInfo), 'pt_key': pt_key, 'pt_pin': pt_pin})

    return cookiesFileInfo, thepath

def saveFiles(cookiesFileInfo, path, masterPtPin):
    cookiesBody = ''
    cookiesBottom = ''
    for item in cookiesFileInfo:
        cookiesBody = '%spt_key%s=%s;\npt_pin%s=%s;\n' % (cookiesBody, item['id'], item['pt_key'], item['id'], item['pt_pin'])
    
        if item['pt_pin'] in masterPtPin:
            cookiesBottom = '&%s' if cookiesBottom else cookiesBottom
            cookiesBottom = 'pt_key=%s;pt_pin=%s;%s' % (item['pt_key'] + item['id'], item['pt_pin'] + item['id'], cookiesBottom) 
        else:
            cookiesBottom = '%s&' if cookiesBottom else cookiesBottom
            cookiesBottom = '%spt_key=%s;pt_pin=%s;' % (cookiesBottom, item['pt_key'] + item['id'], item['pt_pin'] + item['id'])

    with open(path, 'w') as f:
        f.write('#!/bin/bash\n%sJD_COOKIE="%s"' % (cookiesBody, cookiesBottom))