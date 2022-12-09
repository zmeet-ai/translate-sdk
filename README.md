## 一、自然语言API说明

本API目前包括：

* 实时翻译：涵盖30多个国家语言的实时直译，覆盖主要地区和国家的各种语言
* 标点符号： 给没有标点符号或者错误标点符号的语句打上标点符号
* 文本标签和摘要：文本关键词和摘要、重要语句

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

## 四、标签和摘要API
### 1. 标签和摘要API
#### （1）URL
**`https://translate.abcpen.com/v1/nlp/keyword_summary`**
中文和英文的实时翻译

#### （2）KEY
* 使用之前，请向商务申请appKey和appSecret, 以正常服务请求。
#### （3）请求参数：

* 以HTTPS POST(**x-www-form-urlencoded**)请求发送

| 参数 | 数据类型 | 是否必须 | 说明                                    | 默认值 |
| :--: | -------- | -------- | :-------------------------------------- | ------ |
| text | String   | 是       | 待翻译的文本内容，需统一编码成utf-8格式 |        |

（4）返回参数

| 返回参数 | 备注                      |      |
| -------- | ------------------------- | ---- |
| code     | "0"表示正确，其他表示错误 |      |
| msg      | "code"表示的文本描述      |      |
| result   | 参考下文                  |      |


* **完整的字段**如下(字段内容是utf8编码)
  * label: 表示关键词标签
  * summary：表示摘要
  * sentences：表示有重要含义的重点语句

```json
 {'code': '0', 'result': {'label': [{'中国': 0.11287898002210177}, {'全国': 0.10516457586045447}, {'丰收': 0.08585125471693325}, {'去年': 0.08585125471693325}, {'粮食': 0.07220319035961947}, {'沧海': 0.058823529411764705}, {'粮仓': 0.04530966675918043}, {'图景': 0.04530966675918043}, {'大省': 0.04530966675918043}, {'粮食产量': 0.04530966675918043}, {'粒稻': 0.04080504587498567}, {'黑龙江': 0.04080504587498567}, {'产粮': 0.04080504587498567}, {'总产量': 0.03951020826824344}, {'位居': 0.03861983628525301}], 'sentences': [{'黑龙江是中国产粮第一大省，去年粮食产量1573.5亿斤，占全国粮食总产量的11.5%，连续12年位居全国第一': 0.5249094705616637}, {'这粒稻，只是中国大粮仓丰收图景中的沧海一“稻”': 0.4750905294383356}], 'summary': '黑龙江省今年粮食产量1573.5亿斤,创下历史新高。'}, 'msg': 'success'}
```

### 2. 标点符号API
#### （1）URL
**`https://translate.abcpen.com/v1/nlp/puncutation`**
给没有标点符号的中文现代文和古文文言文、诗句等断句，打上标点符号

#### （2）KEY
* 使用之前，请向商务申请appKey和appSecret, 以正常服务请求。
#### （3）请求参数：

* 以HTTPS POST(**x-www-form-urlencoded**)请求发送

| 参数 | 数据类型 | 是否必须 | 说明                                    | 默认值 |
| :--: | -------- | -------- | :-------------------------------------- | ------ |
| text | String   | 是       | 待翻译的文本内容，需统一编码成utf-8格式 |        |

（4）返回参数

| 返回参数 | 备注                      |      |
| -------- | ------------------------- | ---- |
| code     | "0"表示正确，其他表示错误 |      |
| msg      | "code"表示的文本描述      |      |
| result   | 参考下文                  |      |


* **返回结果**如下(字段内容是utf8编码)

```json
 {'code': '0', 'result': {'text': '这次座谈的主题是推动制造业高质量发展,王伟中说:“广东是民营经济大省,制造业大省,要坚定高质量发展,坚持制造业当家,加快推动广东从制造大省向制造强省跨越。'}, 'msg': 'success'}
```

* 上述测试语句(客户测试时需要带验证字段，如appid，ts，signa这三个验证信息)

```json
    text="这次座谈的主题是推动制造业高质量发展王伟中说广东是民营经济大省制造业大省要坚定高质量发展坚持制造业当家加快推动广东从制造大省向制造强省跨越"
    curl -F "text=$text" http://translate.abcpen.com/v1/nlp/punctuation
    echo -e "\nAccess puncutation end\n"
```




* **附录**：测试脚本(注意，没有带验证字段；客户测试的时候，需要带验证字段，否则返回没有license的提示)

```bash
#!/bin/bash
for i in {1..10}
do 
    text="这粒稻，只是中国大粮仓丰收图景中的沧海一“稻”。黑龙江是中国产粮第一大省，去年粮食产量1573.5亿斤，占全国粮食总产量的11.5%，连续12年位居全国第一"
    curl -v -F "text=$text" http://translate.abcpen.com/v1/translate
    echo -e "\nAccess translate end\n";
 
    curl -F "text=$text" http://translate.abcpen.com/v1/nlp/keyword_summary
    echo -e "\nAccess nlp and get summary end\n"

    text="这次座谈的主题是推动制造业高质量发展王伟中说广东是民营经济大省制造业大省要坚定高质量发展坚持制造业当家加快推动广东从制造大省向制造强省跨越"
    curl -F "text=$text" http://translate.abcpen.com/v1/nlp/punctuation
    echo -e "\nAccess puncutation end\n"
done
```

