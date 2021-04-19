/*
根据Docker部署方式中的crontab.list生成Surge Module
部署在Cloudflare Workers中
abc.def.xyz/sgmodule/gitee.com/
*/

async function gatherResponse(response) {
    const { headers } = response
    const contentType = headers.get("content-type") || ""
    if (contentType.includes("application/json")) {
        return JSON.stringify(await response.json())
    }
    else if (contentType.includes("application/text")) {
        return await response.text()
    }
    else if (contentType.includes("text/html")) {
        return await response.text()
    }
    else {
        return await response.text()
    }
}

async function sgModule(event) {
    const url = new URL(event.request.url);
    const path = "https://" + url.pathname.replace("/sgmodule/", "");
    const init = {
        headers: {
            "content-type": "text/html;charset=UTF-8",
        },
    }
    const response = await fetch(path, init)
    const results = await gatherResponse(response)
    var thecontainlist = results.toString().split(/\n/)

    var re_message = '#!name=JD_Task\n#!desc=京东日活任务\n\n[Script]'

    //ScriptPath
    const replaceLeftPatt = new RegExp(".+scripts");
    const replaceRightPatt = new RegExp(" >.+");
    const replaceStr = "https://gitee.com/rhysn/jd_scripts/raw/master";

    //ScriptName
    const matchNamePatt = new RegExp('【.+】');

    //ScriptRunningTime
    const matchTimePatt = new RegExp('.+ bash');

    for (let item of thecontainlist) {
        if(item.startsWith("#") || item.indexOf("【") === -1 || item.indexOf("挂机") > -1 || item.indexOf("NFM") > -1) continue; 
        
        var scriptPath = item.replace(replaceLeftPatt, replaceStr);
        scriptPath = scriptPath.replace(replaceRightPatt, '');

        var scriptName = item.match(matchNamePatt);
        scriptName = scriptName[0].replace('【', '').replace('】', '');

        var runTime = item.match(matchTimePatt);
        runTime = '0 ' + runTime[0].replace(' bash', '');

        re_message = re_message + '\n' +
                     scriptName + ' = type=cron,cronexp=\"' + runTime + 
                     '\",wake-system=1,timeout=3600,script-path=' + scriptPath;
    }

    re_message = re_message + "\n\n[MITM]\nhostname = %APPEND% wq.jd.com, draw.jdfcloud.com, jdjoy.jd.com"

    return new Response(re_message, { status: 200 })
}

addEventListener("fetch", event => {
    return event.respondWith(sgModule(event))
})