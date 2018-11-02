# -*- coding: utf-8 -*-
# File  : douban_sum.py
# Author: HuWenBo
# Date  : 2018/11/2
# 抓取豆瓣所有的电影
import pandas
import sys
import time
import json
import aiohttp
import asyncio

movie_content = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}


async def get_page(url):
    """
    发起GET请求
    :param url:
    :return:
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, timeout=20) as resp:
                if resp.status == 200:
                    return await resp.text()
                else:
                    raise Exception(f'Waring：链接超时{url}')
        except Exception as e:
            sys.stdout.write(f'Waring：{e}\n')


def parse_page(html):
    """
    解析JSON
    :param html:
    :return:
    """
    datas = json.loads(html).get('data')
    if datas:
        for data in datas:
            title = data.get('title')  # 标题
            id = data.get('id')  # id
            directors = ','.join(data.get('directors'))  # 导演
            rate = data.get('rate')  # 评分
            casts = ','.join(data.get('casts'))  # 演员
            yield {
                'title': title,
                'id': id,
                'directors': directors,
                'rate': rate,
                'casts': casts
            }
    else:
        sys.stdout.write('Waring：没有信息\n')


async def crawl(url, sem):
    """
    :param url:
    :param sem:
    :return:
    """
    async with sem:
        sys.stdout.write(f'正在爬取：{url}\n')
        html = await get_page(url)
        for i in parse_page(html):
            movie_content.append(i)


def save_csv(content):
    """
    保存爬取的结果
    :param content:
    :return:
    """
    pd = pandas.DataFrame(content)
    pd.index.name = 'index'
    colums = ['id', 'title', 'rate', 'directors', 'casts']  # 列有序，不然就是按字典序排列
    pd.to_csv('movie_sum.csv', columns=colums, index=False)


def main():
    start = time.time()
    url_base = 'https://movie.douban.com/j/new_search_subjects?start={num}'
    nums = 9980  # 总共电影数目
    urls = [url_base.format(num=i) for i in range(0, nums, 20)]
    loop = asyncio.get_event_loop()
    sem = asyncio.Semaphore(20)
    tasks = [asyncio.ensure_future(crawl(url, sem)) for url in urls]
    loop.run_until_complete(asyncio.wait(tasks))
    end = time.time()
    save_csv(movie_content)
    sys.stdout.write(f'耗费时间：{end-start}\n')


if __name__ == '__main__':
    main()
