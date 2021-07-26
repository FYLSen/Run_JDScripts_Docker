#!/bin/python3
# -*- coding:utf-8 -*-
from pickle import TRUE
from PIL import Image
import qrcode, requests, base64, time, re, os, json
from urllib.parse import urlencode, quote_plus

jd_ua = 'jdapp;android;10.0.5;11;0393465333165363-5333430323261366;network/wifi;model/M2102K1C;osVer/30;appBuild/88681;partner/lc001;eufv/1;jdSupportDarkMode/0;Mozilla/5.0 (Linux; Android 11; M2102K1C Build/RKQ1.201112.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045534 Mobile Safari/537.36'

def token_get(s):
    t = round(time.time())
    headers = {
        'User-Agent': jd_ua,
        'referer': 'https://plogin.m.jd.com/cgi-bin/mm/new_login_entrance?lang=chs&appid=300&returnurl=https://wq.jd.com/passport/LoginRedirect?state={0}&returnurl=https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'.format(t)
    }
    t = round(time.time())
    url = 'https://plogin.m.jd.com/cgi-bin/mm/new_login_entrance?lang=chs&appid=300&returnurl=https://wq.jd.com/passport/LoginRedirect?state={0}&returnurl=https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'.format(t)
    res = s.get(url=url, headers=headers, verify=False)
    res_json = json.loads(res.text)
    s_token = res_json['s_token']
    return s_token

def token_post(s_token, s):
    t = round(time.time() * 1000)
    headers = {
        'User-Agent': jd_ua,
        'referer': 'https://plogin.m.jd.com/login/login?appid=300&returnurl=https://wqlogin2.jd.com/passport/LoginRedirect?state={0}&returnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'.format(t),
        'Content-Type': 'application/x-www-form-urlencoded; Charset=UTF-8'
    }
    url = 'https://plogin.m.jd.com/cgi-bin/m/tmauthreflogurl?s_token={0}&v={1}&remember=true'.format(s_token, t)
    data = {
        'lang': 'chs',
        'appid': 300,
        'returnurl': 'https://wqlogin2.jd.com/passport/LoginRedirect?state={0}returnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'.format(t)
        }
    res = s.post(url=url, headers=headers, data=data, verify=False)
    # print(res.text)
    res_json = json.loads(res.text)
    token = res_json['token']
    # print("token:", token)
    c = s.cookies.get_dict()
    okl_token = c['okl_token']
    # print("okl_token:", okl_token)
    qrurl = 'https://plogin.m.jd.com/cgi-bin/m/tmauth?client_type=m&appid=300&token={0}'.format(token)

    qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
    qr.add_data(qrurl)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    path = '%s.png' % s_token

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
    
def check_token(token, okl_token, s, i = 1):
    t = round(time.time() * 1000)
    headers = {
        'User-Agent': jd_ua,
        'referer': 'https://plogin.m.jd.com/login/login?appid=300&returnurl=https://wqlogin2.jd.com/passport/LoginRedirect?state={0}&returnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'.format(t),
        'Content-Type': 'application/x-www-form-urlencoded; Charset=UTF-8'
    }
    url = 'https://plogin.m.jd.com/cgi-bin/m/tmauthchecktoken?&token={0}&ou_state=0&okl_token={1}'.format(token, okl_token)
    data = {
        'lang': 'chs',
        'appid': 300,
        'returnurl': 'https://wqlogin2.jd.com/passport/LoginRedirect?state={0}&returnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action'.format(t),
        'source': 'wq_passport',
    }
    res = s.post(url=url, headers=headers, data=data, verify=False)
    check = json.loads(res.text)
    code = check['errcode']
    message = check['message']
    while code == 0:
        jd_ck = s.cookies.get_dict()
        pt_key = str(jd_ck['pt_key'])
        pt_pin = str(jd_ck['pt_pin'])
        ck = str(pt_key) + ';' + str(pt_pin) + ';'
        return pt_key, pt_pin
    else:
        i = i + 1
        if i < 60:
            time.sleep(3)
            return check_token(token, okl_token, s, i)
        else:
            return False, False

def getCookieFilesInfo(pt_pin, pt_key, filePath):

    fpInfo = []
    thepath = ''
    oldcookies = ''
    findKey = False
    #将读取全部config文件内容
    for fp in filePath:
        with open(fp, 'r') as f:
            ftext = f.read()
            fpInfo.append({'path': fp, 'data': ftext})
    #使用pt_pin匹配配置文件内容，如果匹配失败则计算每个配置文件中的cookie数量
    for idx, val in enumerate(fpInfo):
        if pt_pin in val['data']:
            thepath = val['path']
            oldcookies = val['data']
            findKey = True
            break
        temp = val['data'].split('\n')
        for t in temp:
            if t.startswith('JD_COOKIE='):
                fpInfo[idx]['num'] = len(t.split('&'))
    #当获取的cookie不在配置文件时，获取保存最少cookies的配置文件
    if not findKey:
        min_idx = 0
        min_num = 0
        for idx,val in enumerate(fpInfo):
            min_num = val['num'] if idx == 0 else min_num
            min_idx = idx if val['num'] < min_num else min_idx
        thepath = fpInfo[min_idx]['path']
        oldcookies = fpInfo[min_idx]['data']
    #获取配置文件中cookie所使用的数字编号
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
    #配置文件中提取出对应的pt_key,pt_pin
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
    #当配置文件中存在新获取到的cookie时，替换数据；
    #当配置文件中不存在获取到的cookie时，追加数据
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
        if item['pt_key'] == '': continue
        cookiesBody = '%spt_key%d=%s\npt_pin%d=%s\n' % (cookiesBody, item['id'], item['pt_key'], item['id'], item['pt_pin'])
    
        if item['pt_pin'] in masterPtPin:
            cookiesBottom = '&%s' % cookiesBottom if cookiesBottom else cookiesBottom
            cookiesBottom = 'pt_key=$pt_key%d;pt_pin=$pt_pin%d;%s' % (item['id'], item['id'], cookiesBottom) 
        else:
            cookiesBottom = '%s&' % cookiesBottom if cookiesBottom else cookiesBottom
            cookiesBottom = '%spt_key=$pt_key%d;pt_pin=$pt_pin%d;' % (cookiesBottom, item['id'], item['id'])
    with open(path, 'w') as f:
        f.write('#!/bin/bash\n%sJD_COOKIE="%s"\n\n' % (cookiesBody, cookiesBottom))