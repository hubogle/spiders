# -*- coding: utf-8 -*-
# File  : fan_yi.py
# Author: HuWenBo
# Date  : 2018/11/10
import requests
import time
import random
import hashlib


def YouDao():
    word = input('输入单词：')
    base_url = 'http://fanyi.youdao.com/'
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    salt = str(int(time.time() * 1000) + random.randint(1, 9))
    raw_str = 'fanyideskweb' + word + salt + 'sr_3(QOHT)L2dx#uuGR@r'
    sign = hashlib.md5(raw_str.encode('utf-8')).hexdigest() # 进行md5加密

    data = {
        'i': word,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTIME',
        'typoResult': 'false',
        'salt': salt,
        'sign': sign,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Origin': 'http://fanyi.youdao.com',
        'Referer': 'http://fanyi.youdao.com/',
    }
    session = requests.Session()
    try:
        session.get(url=base_url, headers=headers)
        response = session.post(url=url, headers=headers, data=data).json()
        tgt = response.get('translateResult')[0][0].get('tgt')
        print(tgt)
    except requests.ConnectionError:
        print('链接异常')
    except KeyError:
        print('类型错误')


if __name__ == '__main__':
    YouDao()
