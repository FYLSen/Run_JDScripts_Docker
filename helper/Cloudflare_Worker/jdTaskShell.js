/*
根据Docker部署方式中的 crontab 生成 shell
部署在Cloudflare Workers中
abc.def.xyz/alljdscripts/gitee.com/
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

async function theShell(event) {
    const getReqHeader = (key) => event.request.headers.get(key);
    
    const url = new URL(event.request.url);
    const path = "https://" + url.pathname.replace("/alljdscripts/", "");

    const init = {
        headers: {
            "content-type": "text/html;charset=UTF-8",
        },
    }
    const response = await fetch(path, init)
    const results = await gatherResponse(response)
    var thecontainlist = results.toString().split(/\n/)

    var re_message = '#!/bin/bash\n'

    const matchShellPatt = new RegExp('bash.+');

    for (let item of thecontainlist) {
        if(item.startsWith("#") || item.indexOf("挂机") > -1 || item === "" || item.indexOf("NR") > -1) continue; 

        var runShell = item.match(matchShellPatt);

        re_message = re_message + '\n' + runShell;
    }
    re_message = re_message + '\n';

    return new Response(re_message, { status: 200 })
}

addEventListener("fetch", event => {
    return event.respondWith(theShell(event))
})