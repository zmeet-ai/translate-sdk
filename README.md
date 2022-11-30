## 一、语言翻译接口说明
目前版本支持30多个国家语言的实时翻译系统，覆盖主要地区和国家的各种语言。

## 二、授权和接入
### 1. 数据协议总则
* 通讯协议：平台向外开放的通讯协议采用HTTP[S]协议
* 编码：默认使用UTF-8，否则中文字符可能为乱码
* 接口权限：每个接入方登记访问IP，只对授权的IP地址开通访问权限（当前没强制要求）

### 2. 签名key
客户首先需要与商务沟通，获得DevId和DevKey：
* DevId
唯一的用户ID， 举例 "zmeet"；一般俗称为 application id 或 application key.
* DevKey
用户密匙， 举例 "^#BDYDEYE#", 一般俗称为 application secret.

### 3. 请求数据格式
JSON

### 4. 响应数据格式
JSON

### 5.认证 请求参数说明
在调用任何业务接口前，必须先取得授权，通过认证。取得授权的方式为在HTTP的请求体中输入正确的账号、时间戳及签名（x-dev-id、x-signature、x-request-send-timestamp）。说明如下：

| **序号** | **参数名**               | **类型** | **是否必填** | **说明**                                                     |
| -------- | ------------------------ | -------- | ------------ | ------------------------------------------------------------ |
| 1        | x-request-send-timestamp | string   | 是           | 请求发送时间戳                                               |
| 2        | x-signature              | string   | 是           | 数字签名，HmacSHA256(x-dev-id + x-request-send-timestamp),用DevKey加密;32小写 |
| 3        | x-dev-id                 | string   | 是           | 由服务方为接入方提供的devId, 一般俗称为app key               |

### 6. **响应参数说明**
| **序号** | **元素名称** | **父元素** | **类型** | **描述**                             |
| -------- | ------------ | ---------- | -------- | ------------------------------------ |
| 1        | code         | --         | string   | 响应状态码                           |
| 2        | msg          | --         | string   | 响应说明                             |
| 3        | result       | --         | string   | 响应结果，翻译出的内容存储在这个字段 |

## 三、语言翻译API
### 2. 中文和英文互译API
#### （1）URL
**`https://translate.abcpen.com/v1/translate`**
中文和英文的实时翻译

#### （2）KEY
* 使用之前，请向商务申请appKey和appSecret, 以正常服务请求。
#### （3）请求参数：

* 以HTTPS POST(**x-www-form-urlencoded**)请求发送

| 参数 | 数据类型 | 是否必须 | 说明                                                         | 默认值 |
| :--: | -------- | -------- | :----------------------------------------------------------- | ------ |
| text | String   | 是       | 待翻译的文本内容，需统一编码成utf-8格式                      |        |
| mode | String   | 否       | 翻译指令，有<br/><1. zh-en, 中文翻译成英文<br/><2. en-zh, 英文翻译成中文 | zh-en  |

（4）返回参数

```javascript
{
    "code": "0",
    "result": "In the general context of the need for immunization, the telecommuting of the home has become a lot of business people.",
    "msg": "success"
}
```

* 其中**result **字段是翻译后的文本

### （5） 示例代码
####  NodeJs版本
```javascript
let rp = require('request-promise');
const crypto = require('crypto');

function verifySha256Sign(appKey, timestamp, appSecret) {
    let combined = appKey + timestamp;
    let hashStr = crypto.createHmac('sha256', appSecret).update(combined).digest("hex");
    
    return hashStr.toLowerCase();
};

async function tts_translate(text, model, appKey, timestamp, sign) {
    let resTts = {
        message: "",
        code: "",
        urlTts: ""
    };

    let bodyRes, jsonData;
    let options;
    {
        jsonData = {
            text: text,
            mode: mode
        };
        options = {
            method: 'POST',
            uri: 'https://translate.abcpen.com/v1/translate',
            form: jsonData,
            headers:{
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
        console.info("translate --------------------------------->", content, bodyRes, typeof bodyRes, ", Duration: ", (Date.now() - ts) + "ms");
        if (typeof bodyRes != 'object') {
            bodyRes = JSON.parse(bodyRes);
            console.log("after parse: ", bodyRes);

        }
    } catch (err) {
        console.log("tts request error: ", err);
        return resTts;
    }
    return bodyRes;
};

(async () => {
    let appKey = "xxxxx"; //请向商务申请
    let appSecret = "xxxxx";

    let timestamp = Date.now()/1000 + "";
    let sign = verifySha256Sign(appKey, timestamp, appSecret);
    console.log("sign sha256 is: ", sign);
    let tts2 = await tts_translate("防疫需求的大环境下，居家远程线上办公成为不少商务人士", "zh-en", appKey, timestamp, sign);
    console.log("translate-2: ", tts2);

})();
```
*Java, C++, Rust, c#等示例代码即将提供*

