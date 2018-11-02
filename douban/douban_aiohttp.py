# -*- coding: utf-8 -*-
# File  : douban_aiohttp.py
# Author: HuWenBo
# Date  : 2018/11/2
# 豆瓣电影Top250榜单爬取 异步
import sys
import pandas
import aiohttp
import asyncio
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}
movie_content = []


async def get_page(url):
    """
    抓取页面的信息
    :param url:
    :return:
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, timeout=30) as resp:
                if resp.status == 200:
                    return await resp.text()
                else:
                    sys.stdout.write(f'Waring：{url}')
        except Exception as e:
            print(e)


def parse_page(html):
    """
    抓取页面的信息
    :param html:
    :return:
    """
    HTML = etree.HTML(html)
    movies = HTML.xpath("//ol[@class='grid_view']/li")
    for movie in movies:
        name = movie.xpath(".//span[@class='title'][1]/text()")[0]  # 名称
        director = movie.xpath(".//div[@class='bd']/p/text()[1]")[0].split()[1]  # 导演
        actor = movie.xpath(".//div[@class='bd']/p/text()[1]")[0].split()  # 演员
        actor = actor[5] if len(actor) > 6 else None
        year = movie.xpath(".//div[@class='bd']/p/text()[2]")[0].split('/')[0].strip()  # 年份
        country = movie.xpath(".//div[@class='bd']/p/text()[2]")[0].split('/')[1].strip()  # 国家
        category = movie.xpath(".//div[@class='bd']/p/text()[2]")[0].split('/')[2].strip()  # 类别
        yield {
            'name': name,
            'director': director,
            'actor': actor,
            'year': year,
            'country': country,
            'category': category,
        }


async def crawl(url, sem):
    """
    :param url: 爬取的url
    :param sem:
    :return:
    """
    async with sem:  # 同时处理的请求
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
    colums = ['name', 'country', 'director', 'actor', 'year', 'category']  # 列有序，不然就是按字典序排列
    pd.to_csv('movie.csv', columns=colums)


def main():
    url_base = 'https://movie.douban.com/top250?start={num}&filter='
    loop = asyncio.get_event_loop()
    sem = asyncio.Semaphore(10)  # 同时有几个请求处理
    for i in range(0, 251, 25):
        url = url_base.format(num=i)
        tasks = [asyncio.ensure_future(crawl(url, sem))]
    loop.run_until_complete(asyncio.wait(tasks))
    save_csv(movie_content)


if __name__ == '__main__':
    main()
