# -*- coding: utf-8 -*-
# File  : douban.py
# Author: HuWenBo
# Date  : 2018/11/2
# 豆瓣电影Top250榜单爬取

import requests
import pandas
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}


def movie_info(url):
    """
    抓取豆瓣电影的信息
    :param url:
    :return:
    """
    try:
        response = requests.get(url, headers=headers)
        HTML = etree.HTML(response.text)
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
    except Exception as e:
        print('Waring：', e)


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
    movie_content = []
    for i in range(0, 251, 25):
        url = url_base.format(num=i)
        print('正在爬取：', url)
        for movie in movie_info(url):
            movie_content.append(movie)
    save_csv(movie_content)


if __name__ == '__main__':
    main()
