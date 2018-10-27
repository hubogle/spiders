# -*- coding: utf-8 -*-
# File  : qq_music.py
# Author: HuWenBo
# Date  : 2018/10/27
# 下载QQ音乐

import requests
import json
import os
import asyncio
import aiohttp
from lxml import etree


def get_name(url):
    """
    获取歌曲的名称，和歌手的名称
    创建歌手的文件夹
    :param url:
    :return:
    """
    response = requests.get(url).text
    html = etree.HTML(response)
    music_name = html.xpath('//h1/text()')[0]
    singer_name = html.xpath("//div[@class='data__singer']/@title")[0]
    if not os.path.isdir(singer_name):
        os.mkdir(singer_name)
    return music_name, singer_name


def get_vkey(music_id):
    """
    请求构造参数url
    :param music_id: 音乐的id
    :return: 返回vkey
    """
    params_url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?&jsonpCallback=MusicJsonCallback&cid=205361747&songmid=' + \
                 music_id + '&filename=C400' + music_id + '.m4a&guid=9082027038'  # 加密参数的url
    try:
        response = requests.get(params_url)  # 访问加密的网址
        response = json.loads(response.text)
        return response['data']['items'][0]['vkey']
    except requests.exceptions:
        print('Waring：链接错误')


def get_music_url(music_id, vkey):
    """
    构造歌曲的链接
    :param music_id:
    :param vkey:
    :return:
    """
    base_music_url = 'http://dl.stream.qqmusic.qq.com/{}' + music_id + '.{}?vkey=' + vkey + '&guid=9082027038&uin=0&fromtag=53'
    music_type = {
        'C400': 'm4a',
        'M500': 'mp3',
        'M800': 'mpe',
        'A000': 'ape',
        'F000': 'flac'
    }  # m4a, mp3普通, mp3高, ape, flac
    music_urls = []
    for k, v in music_type.items():
        music_url = base_music_url.format(k, v)
        music_urls.append(music_url)
    return music_urls


def get_url(music_urls):
    """
    判断构造的urls链接是否可用
    使用协程来请求链接
    :param music_urls:
    :return:
    """
    result = []

    async def get(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    result.append(url)
    tasks = [asyncio.ensure_future(get(url)) for url in music_urls]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    return result


def download_music(music_name, singer_name, urls):
    """
    下载歌曲，按最高品质开始下载
    :param music_name:  歌曲名称
    :param singer_name: 歌手名称
    :param urls: 歌曲urls
    :return:
    """
    music_type = ['flac', 'ape', 'mpe', 'mp3', 'm4a']
    for i in music_type:
        for url in urls:
            if i in url:
                response = requests.get(url, stream=True)
                with open(singer_name + '/' + music_name + '.' + i, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print('下载完成')
                return None


def main():
    music_url = 'https://y.qq.com/n/yqq/song/000rMFLS0ZnngN.html'
    music_name, singer_name = get_name(music_url)
    music_id = music_url.split('/')[6].split('.')[0]
    vkey = get_vkey(music_id)
    music_urls = get_music_url(music_id, vkey)
    music_urls = get_url(music_urls)
    download_music(music_name, singer_name, music_urls)


if __name__ == '__main__':
    main()
