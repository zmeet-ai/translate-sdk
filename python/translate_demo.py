#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import asyncio
import sys
import logging
import time
import argparse

from client_auth_secret import get_signature_flytek, get_signature_zmeet


async def main():
    global args

    parser = argparse.ArgumentParser(description="Translate sdk demo",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-u', '--url', type=str, metavar='URL',
                        help='server url', default='ai.abcpen.com')
    parser.add_argument('-l', '--log_path', type=str, metavar='LOG',
                        help='log file path', default='translate_res.log')

    args = parser.parse_args()
    
    ## 下面的app_id 和api_key仅供测试使用，生产环境请向商务申请(手机：18605811078, 邮箱：jiaozhu@abcpen.com)
    app_id = ""
    api_key = ""
    if (len(app_id)<=0 or len(api_key)<=0):
        print("Please apply appid and appsecret, demo will exit now")
        sys.exit(1)
    timestamp = str(int(time.time()))

    signa = get_signature_zmeet(timestamp, app_id, api_key)
    querys = {
        "ts": timestamp,
        "appid": app_id,
        "signa": signa,
        "text": "防疫需求的大环境下，居家远程线上办公成为不少商务人",
        "mode": "zh-en"

    }
    url = "https://{}/v1/translate/zh-en".format(args.url)
    response = requests.post(url, querys)
    print(response.text)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.info("Got ctrl+c exception: %s, exit process", repr(e))
