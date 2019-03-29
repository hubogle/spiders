#!/usr/bin/env python

import random
from threading import Thread
import requests
import logging
import time
from lxml import etree
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                  '/70.0.3538.77 Safari/537.36'
}
logging.basicConfig(level=logging.WARNING, filename='jd.log', filemode='a')

def get_page(url):
    """
    获取页面的商品
    :param url:
    :return:
    """
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            HTML = etree.HTML(response.text)
            nodes = HTML.xpath("//ul[@class='gl-warp clearfix']/li")
            for node in nodes:
                name = ''.join(node.xpath('.//div[@class="p-name p-name-type-2"]/a/em/text()'))
                price = node.xpath('.//div[@class="p-price"]/strong/i/text()')[0]
                pid = node.xpath('./@data-sku')[0]
                yield {
                    'name': name,
                    'price': price,
                    'pid': pid,
                }
        else:
            logging.warning('网页请求错误' + url)
    except Exception as e:
        logging.warning(e)


def get_comments(pid: str):
    """
    获取评论数量、热评内容
    :param pid:
    :return:
    """
    url = f'https://club.jd.com/productpage/p-{pid}-s-0-t-3-p-0.html'
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            infos = response.json()
            comments_sum = infos.get('productCommentSummary').get('commentCountStr', 0)
            comments_text = list()
            for comments in infos.get('hotCommentTagStatistics'):
                comments_text.append(comments.get('name'))
            if not comments_text:
                comments_text = '无热门评论'
            else:
                comments_text = '、'.join(comments_text)
            return comments_sum, comments_text
        else:
            logging.warning('网页请求错误' + url)
    except Exception as e:
        logging.warning(e)
        return 0, ''



def save_csv(content):
    """
    保存文件为 csv
    :param content:
    :return:
    """
    with open('jd.csv', 'a', encoding='utf-8') as fp:
        f = csv.writer(fp)
        f.writerow(content)


def get_goods(url):
    """
    获取商品信息
    :param url:
    :return:
    """
    print('请求url：' + str(url))
    for goods_info in get_page(url):
        name = goods_info.get('name')
        price = goods_info.get('price')
        pid = goods_info.get('pid')
        comments_sum, hot_comments = get_comments(pid)
        save_csv([name, price, comments_sum, hot_comments])


def run_multithread_crawler(page_urls: list, threads: int):
    begin = 0
    start = time.time()
    while 1:
        _threads = []
        urls = page_urls[begin:begin + threads]
        if not urls:
            break
        for url in urls:
            t = Thread(target=get_goods, args=(url,))
            _threads.append(t)
        for t in _threads:
            t.setDaemon(True)
            t.start()
        for t in _threads:
            t.join()
        begin += threads
    end = time.time()
    print(f'下载完成耗时:{end - start}s')


def multithreads_crawler(threads: int):
    url_base = "https://search.jd.com/search?keyword=女装&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&cid2=1343&page={page}&s={num}&click=0"
    page_urls = list()
    for i in range(1, 101, 1):
        page_urls.append(url_base.format(page=i, num=(i - 1) * 30 + 1))
    run_multithread_crawler(page_urls, threads)


if __name__ == '__main__':
    multithreads_crawler(20)
