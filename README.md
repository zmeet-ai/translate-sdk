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
### 1. 中文和英文互译-单句
#### （1）URL
**`https://translate.abcpen.com/v1/translate/sentence`**
中文和英文的实时翻译

#### （2）KEY
* 使用之前，请向商务申请appKey和appSecret, 以正常服务请求。
#### （3）请求参数：

* 以HTTPS POST(**x-www-form-urlencoded**)请求发送

| 参数 | 数据类型 | 是否必须 | 说明                                                         | 默认值 |
| :--: | -------- | -------- | :----------------------------------------------------------- | ------ |
| text | String   | 是       | 待翻译的文本内容，需统一编码成utf-8格式(单条语句文本最长512个字，超过会被自动截断) |        |
| mode | String   | 否       | 翻译指令，有<br/><1. zh-en, 中文翻译成英文<br/><2. en-zh, 英文翻译成中文 | zh-en  |

（4）返回参数

```javascript
{"code":"0", "result":{"src":"输入的原始文本内容", "target":"翻译后的文本内容"}, "msg":"success"}
```

* 返回示例

```json
{"code": "0", "result": {"src": "\"\n    \u9996\u5148\uff0cASML\u4f5c\u4e3a\u5168\u7403\u6700\u5927\u7684\u5149\u523b\u673a\u5236\u9020\u5382\u5546\uff0c\u5c3d\u7ba1\u80fd\u591f\u9886\u8dd1\u5168\u4e16\u754c\uff0c\u53ef\u5982\u679c\u6ca1\u6709\u5927\u6279\u91d1\u4e3b\u5ba2\u6237\uff0cASML\u4e5f\u4e0d\u4f1a\u8fc7\u5f97\u90a3\u4e48\u8212\u5766\u3002\u4e2d\u56fd\u5e02\u573a\u4f5c\u4e3a\u5168\u7403\u6700\u5927\u7684\u6d88\u8d39\u5e02\u573a\uff0c\n\u5728\u8fd1\u5e74\u6765\uff0c\u56fd\u5185\u7684\u534a\u5bfc\u4f53\u4f01\u4e1a\u6570\u91cf\u98d9\u5347\uff0c\u5168\u7403\u6bcf\u65b0\u589e20\u5bb6\u534a\u5bfc\u4f53\u4f01\u4e1a\uff0c\u5c31\u670919\u5bb6\u662f\u4e2d\u56fd\u7684\uff0c\u53ef\u89c1\u4e2d\u56fd\u5e02\u573a\u7684\u5de8\u5927\u6f5c\u529b\u3002ASML\u4e5f\u4e0d\u50bb\uff0c\u867d\u7136\u5728\u4e4b\u524d\u4e00\u76f4\u672a\u5927\u91cf\u51fa\u53e3\u7ed9\u4e2d\n\u56fd\u5149\u523b\u673a\uff0c\u4f46\u662f\u968f\u7740\u4e2d\u56fd\u5bf9DUV\u5149\u523b\u673a\u9700\u6c42\u7684\u589e\u957f\uff0cASML\u4e5f\u5f00\u59cb\u91cd\u89c6\u8d77\u4e2d\u56fd\u5e02\u573a\u4e86\u3002", "target": ["\" First, ASML, as the world\u2019s largest light-engineer manufacturer, would not have been as comfortable as ASML without a large number of major gold-based customers. China\u2019s market, as the world\u2019s largest consumer market, has soared in recent years, with 19 of the world\u2019s 20 additional semiconductor enterprises, showing the great potential of China\u2019s market."]}, "msg": "success"}
```


### 2. 中文和英文互译-多条语句
#### （1）URL
**`https://translate.abcpen.com/v1/translate/sentences`**
中文和英文的实时翻译

#### （2）KEY
* 使用之前，请向商务申请appKey和appSecret, 以正常服务请求。
#### （3）请求参数：

* 以HTTPS POST(**x-www-form-urlencoded**)请求发送

| 参数 | 数据类型 | 是否必须 | 说明                                                         | 默认值 |
| :--: | -------- | -------- | :----------------------------------------------------------- | ------ |
| text | String   | 是       | 待翻译的文本内容，需统一编码成utf-8格式<br/>(单条语句文本最长512个字，超过会被自动截断) |        |
| mode | String   | 否       | 翻译指令，有<br/><1. zh-en, 中文翻译成英文<br/><2. en-zh, 英文翻译成中文 | zh-en  |

（4）返回参数

* 返回参数

```javascript
{"code":"0", "result":{"src":"输入的原始文本内容", "target":"翻译后的文本内容"}, "msg":"success"}
```

* 返回示例

```json
{"code": "0", "result": {"src": ["\"", "    \u9996\u5148\uff0cASML\u4f5c\u4e3a\u5168\u7403\u6700\u5927\u7684\u5149\u523b\u673a\u5236\u9020\u5382\u5546\uff0c\u5c3d\u7ba1\u80fd\u591f\u9886\u8dd1\u5168\u4e16\u754c\uff0c\u53ef\u5982\u679c\u6ca1\u6709\u5927\u6279\u91d1\u4e3b\u5ba2\u6237\uff0cASML\u4e5f\u4e0d\u4f1a\u8fc7\u5f97\u90a3\u4e48\u8212\u5766\u3002\u4e2d\u56fd\u5e02\u573a\u4f5c\u4e3a\u5168\u7403\u6700\u5927\u7684\u6d88\u8d39\u5e02\u573a\uff0c", "\u5728\u8fd1\u5e74\u6765\uff0c\u56fd\u5185\u7684\u534a\u5bfc\u4f53\u4f01\u4e1a\u6570\u91cf\u98d9\u5347\uff0c\u5168\u7403\u6bcf\u65b0\u589e20\u5bb6\u534a\u5bfc\u4f53\u4f01\u4e1a\uff0c\u5c31\u670919\u5bb6\u662f\u4e2d\u56fd\u7684\uff0c\u53ef\u89c1\u4e2d\u56fd\u5e02\u573a\u7684\u5de8\u5927\u6f5c\u529b\u3002ASML\u4e5f\u4e0d\u50bb\uff0c\u867d\u7136\u5728\u4e4b\u524d\u4e00\u76f4\u672a\u5927\u91cf\u51fa\u53e3\u7ed9\u4e2d", "\u56fd\u5149\u523b\u673a\uff0c\u4f46\u662f\u968f\u7740\u4e2d\u56fd\u5bf9DUV\u5149\u523b\u673a\u9700\u6c42\u7684\u589e\u957f\uff0cASML\u4e5f\u5f00\u59cb\u91cd\u89c6\u8d77\u4e2d\u56fd\u5e02\u573a\u4e86\u3002"], "target": ["\"", "First of all, ASML, the world\u2019s largest producer of light mechanisms, although able to lead the world, would not have been as comfortable without a large number of gold-based customers. China\u2019s market is the world\u2019s largest consumer market.", "In recent years, the number of domestic semiconductor enterprises has soared that, for every 20 additional semiconductor enterprises in the world, 19 are Chinese, and the potential of China\u2019s market is evident. The ASML is not stupid, although it has not been exported to China in large quantities before.", "The Chinese market has also begun to receive attention from ASML as China's demand for DUV has grown."]}, "msg": "success"}
```



### 2. 中文和英文互译-文件上传
#### （1）URL
**`https://translate.abcpen.com/v1/translate/file`**
中文和英文的实时翻译

#### （2）KEY
* 使用之前，请向商务申请appKey和appSecret, 以正常服务请求。
#### （3）请求参数：

* 以HTTPS POST(**x-www-form-urlencoded**)请求发送

|    参数    | 数据类型 | 是否必须 | 说明                                                         | 默认值 |
| :--------: | -------- | -------- | :----------------------------------------------------------- | ------ |
| trans_file | String   | 是       | 待翻译的文件内容，需统一编码成utf-8格式<br/>(单条语句文本最长512个字，超过会被自动截断) |        |
|    mode    | String   | 否       | 翻译指令，有<br/><1. zh-en, 中文翻译成英文<br/><2. en-zh, 英文翻译成中文 | zh-en  |

（4）返回参数

* 返回参数

  ```json
  {"code":"0", "result":{"src":"输入的原始文本内容", "target":"翻译后的文本内容"}, "msg":"success"}
  ```

  

* 返回示例

```json
{"code":"0","result":{"src":["随着全球国家科技实力的提升，如今的世界，已经不是美国一家独大的情景了。","就在前两年，华为的崛起让所有国家都大吃了一惊，尤其是美国。万万没想到，在移动通信领域中，超越美国的不是发达国家，而是我们中国。","显然，美国已经不想再眼睁睁看着华为崛起，所以便定下了芯片规则。随着芯片规则的升级，就连ASML公司也受到了影响，然而为了能够给中国出口DUV光刻机，","ASML甚至不惜硬刚美国规则，不少美国媒体都表示，这是ASML翅膀硬了。","","","我们都知道，ASML是全球乃至世界上唯一一个拥有EUV光刻机成熟供应链的公司，在全球范围内都拥有极高的地位。要知道，台积电之所以能够跨越美国企业，","成为全球第一大芯片代工厂，就是因为台积电获得了ASML的青睐，拿到了80台EUV光刻机。一直以来，ASML公司都非常信任美国，从来不将EUV光刻机出口给","中国大陆企业。可是在最近，ASML似乎将局势看的异常清楚，那么到底是什么原因？让ASML不惜硬刚美国规则，也要出口DUV光刻机给中国呢？","","","首先，ASML作为全球最大的光刻机制造厂商，尽管能够领跑全世界，可如果没有大批金主客户，ASML也不会过得那么舒坦。中国市场作为全球最大的消费市场，","在近年来，国内的半导体企业数量飙升，全球每新增20家半导体企业，就有19家是中国的，可见中国市场的巨大潜力。ASML也不傻，虽然在之前一直未大量出口给中","国光刻机，但是随着中国对DUV光刻机需求的增长，ASML也开始重视起中国市场了。","","","其次就是ASML发现，随着美国规则的建立，全球芯片格局出现了重大变动，比如高端芯片的需求大大降低，导致各大企业对EUV光刻机的需求也随之下降。要知道，","ASML的营收主要来源就是在EUV光刻机的出口，那么在这样的情况下，ASML的营收出现了巨大下降。这一度让ASML十分无奈，不过值得安慰的是，中国市场开始大量","进口DUV光刻机，弥补了ASML公司的亏损。","","","ASML公司也非常清楚，导致这一切的最根本的原因，就是在于美国修改了芯片规则。所以，当美国再次对ASML下达DUV出口禁令时，ASML当然不可能心甘情愿了。","毕竟，中国市场对于ASML来说，就像是宝藏。而且中国在对待ASML时十分尊重，让ASML感受到了友好的气息，这一点在美国身上是从未感受过的。所以，","ASML不仅在DUV光刻机出口上 ，对中国市场做出了极大的倾斜，也开始加大投资在中国的研究中心。","","如今，中国已经研究出了90nm光刻机，能够大量生产14nm制程工艺的芯片，所以中国在未来绝对是ASML光刻机的最大客户。不过我们也要时刻保持清醒，","不要被ASML现在的态度所迷惑，进而放慢了自我研究的脚步。我们一定要时刻谨记倪光南院士的警告，只有将主动权掌握在自己手中，才能真正摆脱被“卡脖子”的风险。光刻机被誉为世界半导体金字塔塔尖的明珠，目前世界上只有荷兰的ASML 具备最, 光刻机被誉为世界半导体金字塔塔尖的明珠，目前世界上只有荷兰的ASML具备最, 光刻机被誉为世界半导体金字塔塔尖的明珠，目前世界上只有荷兰的ASML具备最"],"target":["As the global power of science and technology has grown, the world today is no longer the only one in the United States.","Just the last two years, China’s rise was a shock to all countries, especially the United States. It is not the developed countries, but China, that are going beyond the United States in the field of mobile communications.","Clearly, the United States no longer wants to see China rise in order to set chip rules. Even ASML has been affected as the chip code has been upgraded, but in order to give China the ability to export DUVs, it has been unable to do so.","ASML is even hard on American rules, and a number of American media say that it's ASML wings are hard.","I don't think so.","I don't think so.","As we all know, ASML is the only company in the world and the world that owns a fully fledged EUV luminous supply chain, and it is in a very high position on a global scale.","The reason that it became the world’s largest chip-based factory is because it won the ASML’s favor and got 80 EUVs. ASML has always trusted the United States and never exported the EUVs.","China Continental Enterprises. But lately, ASML seems to see the situation in an extraordinary way, so what's the reason? Let ASML, despite the US rules, export the DUV light carving machine to China?","I don't think so.","I don't think so.","First of all, ASML, the world’s largest producer of light mechanisms, although able to lead the world, would not have been as comfortable without a large number of gold-based customers. China’s market is the world’s largest consumer market.","In recent years, the number of domestic semiconductor enterprises has soared that, for every 20 additional semiconductor enterprises in the world, 19 are Chinese, and the potential of China’s market is evident. The ASML is not stupid, although it has not been exported to China in large quantities before.","The Chinese market has also begun to receive attention from ASML as China's demand for DUV has grown.","I don't think so.","I don't think so.","The second is that ASML found that, with the establishment of American rules, there have been major changes in global chip patterns, such as a significant reduction in the demand for high-end chips, which has led to a decrease in the demand for EUV light-engineers by major companies.","ASML's main source of revenue is exports from EUV light engines, and in this case, ASML's harvest has fallen dramatically. This has left ASML very vulnerable, but it is reassuring that China's market has begun to grow in large numbers.","The import of the DUV light engraved machines made up for the losses incurred by ASML.","I don't think so.","I don't think so.","ASML is also well aware that the most fundamental reason for this is that the US has modified the chip rules. So, when the US again imposed a DMV export ban on ASML, ASML certainly could not have been willing to do so.","After all, the Chinese market is like a treasure to ASML. And China treats ASML with great respect and gives ASML a sense of friendship, which has never been felt in the United States.","ASML has not only made a huge tilt on the Chinese market on the export of DUV light engraved machines, but has also begun to invest more in research centres in China.","I don't think so.","Today, China has developed 90 nm lightcuts, capable of producing 14 nm process chips in large quantities, so China is definitely the biggest customer of ASML lightcutors in the future. But we also have to stay awake at all times.","Don't let the ASML be fooled by its current attitude, which slows the pace of self-research. We must always bear in mind the warning of Nankoshi that only by taking ownership of the initiative in our own hands can we truly escape the risk of being caught in the neck. The lighter is known as the bead of the world's semiconductor pyramids, the world's largest ASML, the world's largest, the world's semiconductor pyramids, the world's largest ASML, and the world's half-conductor pyramids, the world's largest ASML."]},"msg":"success"}
```


### （5） 示例代码
####  Python版本
**下面直接演示api，不包括appid, appsecret验证部分**

```python
import requests

def translate_file():
    files = {'trans_file': open('./news_1.txt', 'rb')}
    url = "http://translate.abcpen.com/v1/translate/file"
    r = requests.post(url, files=files)
    print(r.text)

def translate_sentences():
    sentences = """"
    首先，ASML作为全球最大的光刻机制造厂商，尽管能够领跑全世界，可如果没有大批金主客户，ASML也不会过得那么舒坦。中国市场作为全球最大的消费市场，
在近年来，国内的半导体企业数量飙升，全球每新增20家半导体企业，就有19家是中国的，可见中国市场的巨大潜力。ASML也不傻，虽然在之前一直未大量出口给中
国光刻机，但是随着中国对DUV光刻机需求的增长，ASML也开始重视起中国市场了。
    """
    values = {'sentences': sentences.encode("utf8")}
    url = "http://translate.abcpen.com/v1/translate/sentences"
    r = requests.post(url, data=values)
    print(r.text)


def translate_sentence():
    sentences = """"
    首先，ASML作为全球最大的光刻机制造厂商，尽管能够领跑全世界，可如果没有大批金主客户，ASML也不会过得那么舒坦。中国市场作为全球最大的消费市场，
在近年来，国内的半导体企业数量飙升，全球每新增20家半导体企业，就有19家是中国的，可见中国市场的巨大潜力。ASML也不傻，虽然在之前一直未大量出口给中
国光刻机，但是随着中国对DUV光刻机需求的增长，ASML也开始重视起中国市场了。
    """
    values = {'sentence': sentences.encode("utf8")}
    url = "http://translate.abcpen.com/v1/translate/sentence"
    r = requests.post(url, data=values)
    print(r.text)

if __name__ == "__main__":
    translate_sentence()
    translate_sentences()
    translate_file()

```


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

