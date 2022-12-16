import requests, sys, time
from client_auth_secret import get_signature_flytek, get_signature_zmeet

## 下面的app_id 和api_key仅供测试使用，生产环境请向商务申请(手机：18605811078, 邮箱：jiaozhu@abcpen.com)
app_id = ""
api_key = ""
if (len(app_id)<=0 or len(api_key)<=0):
    print("Please apply appid and appsecret, demo will exit now")
    sys.exit(1)
timestamp = str(int(time.time()))

signa = get_signature_zmeet(timestamp, app_id, api_key)

def translate_file():
    files = {'trans_file': open('./news_1.txt', 'rb'), "appid": app_id, "signa":signa, "ts":timestamp}
    url = "http://translate.abcpen.com/v1/translate/file"
    r = requests.post(url, files=files)
    print(r.text)

def translate_sentences():
    sentences = """"
    首先，ASML作为全球最大的光刻机制造厂商，尽管能够领跑全世界，可如果没有大批金主客户，ASML也不会过得那么舒坦。中国市场作为全球最大的消费市场，
在近年来，国内的半导体企业数量飙升，全球每新增20家半导体企业，就有19家是中国的，可见中国市场的巨大潜力。ASML也不傻，虽然在之前一直未大量出口给中
国光刻机，但是随着中国对DUV光刻机需求的增长，ASML也开始重视起中国市场了。
    """
    values = {'sentences': sentences.encode("utf8"), "appid": app_id, "signa":signa, "ts":timestamp}
    url = "http://translate.abcpen.com/v1/translate/sentences"
    r = requests.post(url, data=values)
    print(r.text)


def translate_sentence():
    sentences = """"
    首先，ASML作为全球最大的光刻机制造厂商，尽管能够领跑全世界，可如果没有大批金主客户，ASML也不会过得那么舒坦。中国市场作为全球最大的消费市场，
在近年来，国内的半导体企业数量飙升，全球每新增20家半导体企业，就有19家是中国的，可见中国市场的巨大潜力。ASML也不傻，虽然在之前一直未大量出口给中
国光刻机，但是随着中国对DUV光刻机需求的增长，ASML也开始重视起中国市场了。
    """
    values = {'sentence': sentences.encode("utf8"), "appid": app_id, "signa":signa, "ts":timestamp}
    url = "http://translate.abcpen.com/v1/translate/sentence"
    r = requests.post(url, data=values)
    print(r.text)

if __name__ == "__main__":
    translate_sentence()
    translate_sentences()
    translate_file()
