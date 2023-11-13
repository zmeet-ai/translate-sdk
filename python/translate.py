#!/usr/bin/env python
# -*- coding: utf-8 -*-

import http3
import requests
import json
from time import perf_counter
from requests.utils import quote
import hashlib
import time
import requests
import pytest
import hmac
import base64, hashlib

URL_SERVER = "https://translate_dev.abcpen.com"
#URL_SERVER = "http://127.0.0.1:3701"
#URL_SERVER = "http://192.168.10.2:3701"
#URL_SERVER = "https://translate_v2.abcpen.com"

text_zh = [
    "这粒稻，只是中国大粮仓丰收图景中的沧海一“稻”。黑龙江是中国产粮第一大省，去年粮食产量1573.5亿斤，占全国粮食总产量的11.5%，连续12年位居全国第一",
    "律回春辉渐，万象始更新。放眼神州大地，处处焕发文化新气象",
    "2023年11月5日至10日，第六届中国国际进口博览会将在上海举办。习近平主席在首届中国国际进口博览会开幕式主旨演讲中表示，中国对外开放的大门不会关闭，只会越开越大。作为世界上第一个以进口为主题的国家级展会，现在，进博会已成为中国构建新发展格局的窗口、推动高水平开放的平台、全球共享的国际公共产品，也是“一带一路”建设的重要支撑。我们一起来重温习近平主席的重要讲话！",
]

sentences_zh = """"
    首先，ASML作为全球最大的光刻机制造厂商，尽管能够领跑全世界，可如果没有大批金主客户，ASML也不会过得那么舒坦。中国市场作为全球最大的消费市场，
在近年来，国内的半导体企业数量飙升，全球每新增20家半导体企业，就有19家是中国的，可见中国市场的巨大潜力。ASML也不傻，虽然在之前一直未大量出口给中
国光刻机，但是随着中国对DUV光刻机需求的增长，ASML也开始重视起中国市场了。
    """
documents = [
    """顶着国际形势的压力，美国多次发出禁止华为使用美国制造的芯片的政策。即使是技术领先的高通公司，
也经历了被迫退出与华为的合作之后，却在最近的消息中，高通却力挺华为，继续为其供应芯片。这一系列的变化，
引发了广泛的热议，这是哪一方面的利益在占据上风，华为这一巨头的生存之路到底会是如何演绎的呢？""",
    """首先，我们需要明确“洋可乐”在市场上成功的原因。一方面，这款饮料的包装与口感极之相似，很难被察觉，
 消费者不知不觉中就购买了这款“假冒”饮料。另一方面，“洋可乐”制作成本低，清一色使用了国内生产的原材料，这也是它能够以低廉价格出售的重要原因。""",
    """4月27日至28日，第六届数字中国建设峰会在福州举行。党的十八大以来，习近平总书记高度重视大数据产业发展，

对发展数字经济、建设数字中国，作出一系列重大决策、重要部署，提出一系列新思想新观点新论断。今天，一起来学习！""",
]
multi_sentences = [
    "Dies ist ein deutscher Satz",
    "This is an English sentence",
    "这是一个中文句子",
]


application_key = "test1"
application_secret = "2258ACC4-199B-4DCB-B6F3-C2485C63E85A"


def generate_signature(app_id: str, api_key: str):
    """
    @param app_id: 应用程序ID
    @param api_key: 应用程序秘钥
    @return: 签名, 时间戳
    """
    ts: str = str(int(time.time()))
    tt = (app_id + ts).encode("utf-8")
    md5 = hashlib.md5()
    md5.update(tt)
    baseString = md5.hexdigest()
    baseString = bytes(baseString, encoding="utf-8")

    apiKey = api_key.encode("utf-8")
    signa = hmac.new(apiKey, baseString, hashlib.sha1).digest()
    signa = base64.b64encode(signa)
    signa = str(signa, "utf-8")
    return signa, ts


def translate_sentence(sentence, source_lang, target_lang):
    t1 = perf_counter()

    # timestamp = str(int(time.time()))

    # message = f"{application_key}{timestamp}"
    # expected_signature = hmac.new(application_secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).hexdigest()
    expected_signature, timestamp = generate_signature(
        application_key, application_secret
    )
    headers = {
        "X-App-Key": application_key,
        "X-App-Signature": expected_signature,
        "X-Timestamp": timestamp,
    }
    values = {
        "sentence": sentence.encode("utf8"),
        "source_lang": source_lang,
        "target_lang": target_lang,
    }
    url = f"{URL_SERVER}/v1/translate/sentence"

    r = requests.post(url, headers=headers, data=values)
    print(
        f"translate_sentence, Time consume: {perf_counter()-t1:.6f}s, Result: {r.text}"
    )


def translate_sentences(sentences, source_lang, target_lang):
    t1 = perf_counter()
    # timestamp = str(int(time.time()))

    # message = f"{application_key}{timestamp}"
    # expected_signature = hmac.new(application_secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).hexdigest()
    # expected_signature, timestamp = generate_signature(application_key, application_secret)
    expected_signature, timestamp = generate_signature(
        application_key, application_secret
    )
    headers = {
        "X-App-Key": application_key,
        "X-App-Signature": expected_signature,
        "X-Timestamp": timestamp,
    }
    values = {
        "sentences": sentences,
        "source_lang": source_lang,
        "target_lang": target_lang,
    }
    # values = {'sentences': ["Hello", "World"], 'source_lang': source_lang, 'target_lang': target_lang}
    print(f"Json values: {values}")
    url = f"{URL_SERVER}/v1/translate/sentences"
    r = requests.post(url, headers=headers, json=values)
    print(
        f" translate_sentences, Time consume: {perf_counter()-t1:.6f}s, Result: {r.text}"
    )


def translate_langpair(source_lang, target_lang):
    t1 = perf_counter()
    # timestamp = str(int(time.time()))

    # message = f"{application_key}{timestamp}"
    # expected_signature = hmac.new(application_secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).hexdigest()
    expected_signature, timestamp = generate_signature(
        application_key, application_secret
    )
    headers = {
        "X-App-Key": application_key,
        "X-App-Signature": expected_signature,
        "X-Timestamp": timestamp,
    }
    values = {"source_lang": source_lang, "target_lang": target_lang}
    # values = {'sentences': ["Hello", "World"], 'source_lang': source_lang, 'target_lang': target_lang}
    print(f"Json values: {values}")
    url = f"{URL_SERVER}/v1/translate/lang_pair"
    r = requests.get(url, headers=headers, params=values)
    print(
        f" translate_langpair, Time consume: {perf_counter()-t1:.6f}s, Result: {r.text}"
    )


def translate_langlist():
    t1 = perf_counter()
    # timestamp = str(int(time.time()))

    # message = f"{application_key}{timestamp}"
    # expected_signature = hmac.new(application_secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).hexdigest()
    expected_signature, timestamp = generate_signature(
        application_key, application_secret
    )
    headers = {
        "X-App-Key": application_key,
        "X-App-Signature": expected_signature,
        "X-Timestamp": timestamp,
    }

    url = f"{URL_SERVER}/v1/translate/lang_pair_list"
    r = requests.get(url, headers=headers)
    print(
        f" translate_langlist, Time consume: {perf_counter()-t1:.6f}s, Result: {r.text}"
    )


def translate_file(file, source_lang, target_lang):
    t1 = perf_counter()
    # timestamp = str(int(time.time()))

    # message = f"{application_key}{timestamp}"
    # expected_signature = hmac.new(application_secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).hexdigest()
    expected_signature, timestamp = generate_signature(
        application_key, application_secret
    )
    headers = {
        "X-App-Key": application_key,
        "X-App-Signature": expected_signature,
        "X-Timestamp": timestamp,
    }
    files = {"document": open(f"./{file}", "rb")}
    json = {"target_lang": target_lang}
    url = f"{URL_SERVER}/v1/translate/file"

    r = requests.post(url, headers=headers, files=files, data=json)
    print(f"translate_file,  Time consume: {perf_counter()-t1:.6f}s, Result: {r.text}")


def translate_detection(sentences):
    t1 = perf_counter()
    # timestamp = str(int(time.time()))

    # message = f"{application_key}{timestamp}"
    # expected_signature = hmac.new(application_secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).hexdigest()
    expected_signature, timestamp = generate_signature(
        application_key, application_secret
    )
    headers = {
        "X-App-Key": application_key,
        "X-App-Signature": expected_signature,
        "X-Timestamp": timestamp,
    }
    values = {"text": sentences}
    print(f"Json values: {values}")
    url = f"{URL_SERVER}/v1/translate/language_detection"
    r = requests.post(url, headers=headers, json=values)
    print(
        f" translate_detection, Language Detection time consume: {perf_counter()-t1:.6f}s, Result: {r.text}"
    )

    for text in sentences:
        r = requests.get(
            f"{URL_SERVER}/v1/translate/language_detection?text=" + quote(text),
            headers=headers,
        )
        print(text, "language detect result==>", r.json())

def total_test():
    print(
        f"==============================================================================>>>>NO. , {item}"
    )
    translate_sentence(sentences_zh, "zh", "ru")
    print("\n\n")
    translate_sentences(documents, "zh", "ru")
    print("\n\n")

    translate_file("news_1.txt", "zh", "ru")
    print("\n\n")
    translate_detection(multi_sentences)
    print("\n\n")

    translate_langpair("Japanese", "chinese_simplified")
    translate_langlist()

def total_sentence():
    for item in text_zh:
        translate_sentence(item, "zh", "en")
    
if __name__ == "__main__":
    t1 = perf_counter()
    for item in range(1):
        total_test()
        total_sentence()
    t2 = perf_counter()
    print(f"Total time: {t2-t1}s, average time: {(t2-t1)/50:.6f}s")
