/*
通过 Surge Module 文件生成下载对应脚本的 Shell 脚本文件
【EXAMPLE】 curl -s -S -L getscriptsfile.xyz/abc.xyz/Task.sgmodule > file.sh && bash file.sh
*/

addEventListener('fetch', event => {
    event.respondWith(getScriptFile(event));
});

async function getScriptFile(event) {
    const getReqHeader = (key) => event.request.headers.get(key);
    
    const url = new URL(event.request.url);
    const path = 'https:/' + url.pathname;

    let init = {
        method: event.request.method,
        headers: {
            'User-Agent': getReqHeader("User-Agent"),
            'Accept': getReqHeader("Accept"),
            'Accept-Language': getReqHeader("Accept-Language"),
            'Accept-Encoding': getReqHeader("Accept-Encoding"),
            'Connection': 'keep-alive'
        }
    };

    if (event.request.headers.has("Referer")) {
        init.headers.Referer = getReqHeader("Referer");
    }

    if (event.request.headers.has("Origin")) {
        init.headers.Origin = getReqHeader("Origin");
    }
    
    const matchFilePatt = new RegExp('https:\/\/.+');
    
    const response = await fetch(path, event.request);
    const results = await response.text();
    
    var res = results.toString().match(/\[Script\]\n[\S\s]+\n\[MITM\]/g);
    var scriptsArr = res.toString().split(/[\[\]]/);
    var scriptsFileList = scriptsArr[2].toString().split(/\n/);
    
    var re_message = '#!/bin/bash\n\n';
    
    for(let item of scriptsFileList){
        if(item === '') continue;
        var fileUrl = item.match(matchFilePatt);
        fileUrl = fileUrl[0].replace(',script-update-interval=0', '')
        re_message = re_message + '\nwget ' + fileUrl;
        
    }
    re_message = re_message + '\n\n';

    return new Response(re_message, { status: 200 });
}