let rp = require('request-promise');
const crypto = require('crypto');

function verifySha256Sign(appKey, timestamp, appSecret) {
    let combined = appKey + timestamp;
    let hashStr = crypto.createHmac('sha256', appSecret).update(combined).digest("hex");

    return hashStr.toLowerCase();
};

async function translate_demo(content, model, appKey, timestamp, sign) {
    let resAI = {
        message: "",
        code: "",
        result: ""
    };

    let bodyRes, jsonData;
    let options;
    {
        jsonData = {
            text: content,
            model: model
        };
        options = {
            method: 'POST',
            uri: 'https://ai.abcpen.com/v1/translate/zh-en',
            form: jsonData,
            headers: {
                "x-dev-id": appKey,
                "x-signature": sign,
                "x-request-send-timestamp": timestamp
            },
            timeout: 5000,
            forever: true
        }
    }
    try {
        let ts = Date.now();
        bodyRes = await rp(options);
        console.info("Translate-1 --------------------------------->", content, bodyRes, typeof bodyRes, ", Duration: ", (Date.now() - ts) + "ms");
        if (typeof bodyRes != 'object') {
            bodyRes = JSON.parse(bodyRes);
            console.log("after parse: ", bodyRes);

        }
    } catch (err) {
        console.log("Translate request error: ", err);
        return resAI;
    }
    return bodyRes;
};

(async () => {
    let appKey = ""
    let appSecret = ""
    if (appKey.length <= 0 || appSecret <= 0) {
        console.log("请向商务申请开发者密钥！");
        process.exit(0);
    }
    console.log(appKey, appSecret)

    let timestamp = parseInt(Date.now() / 1000) + "";
    let sign = verifySha256Sign(appKey, timestamp, appSecret);
    console.log("sign sha256 is: ", sign);
    let translate_result = await translate_demo("防疫需求的大环境下，居家远程线上办公成为不少商务人士",
        "zh-en", appKey, timestamp, sign);
    console.log("Translate Result: ", translate_result);

})();
