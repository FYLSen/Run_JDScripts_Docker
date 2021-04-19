#!/bin/python3
# -*- coding:utf-8 -*-

import re,json,os

def getSetting(path):
    with open(path, 'r') as f:
        setting = json.load(f)
        return setting['data']

def getEnv():
    env = {
        "CONTAINER_NAME" : os.environ.get('CONTAINER_NAME').split("&")
    }
    return env

def main():
    preferences_path = r'/Run_JDScripts_Docker/getShareCodes/config/preferences.json'
    sharecode_path = r'/shareCodes/'

    env = getEnv()
    setting = getSetting(preferences_path)
    shareCodes = ''
    for item in setting:
        if item['status'] == "dead" or item['status'] == "daily" ：continue
        sc_group = []
        for CN in env['CONTAINER_NAME']:
            logs_path = "/logs/%s/%s" % (CN, item['filename'])
            with open(logs_path, "r", "utf-8") as f: 
                logs = f.read()
                pattern = re.compile(item['pattern'])
                sc_group += pattern.findall(str)
            f.close()

        shareCodes = "%s#%s\n%s=%s\n\n" % (shareCodes, item['name'], item['envname'], '@'.join(sc_group))
        
        with open(sharecode_path + item.submitname ,'w') as f:
            f.write('&'.join(sc_group))
        f.close()

    with open(sharecode_path + r"Temp.sh" ,'w') as f:
        f.write(shareCodes)
    f.close()


if __name__ == '__main__':
    main()