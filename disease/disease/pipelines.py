# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import pymysql


class HaodfPipline:
    def __init__(self):
        self.file = open('../data/name.txt', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        for i in item['name']:
            self.file.write(i+'\n')
        return item

    def close_spider(self, spider):
        self.file.close()


class DiseasePipeline(object):
    """
    保存CSV文件
    """

    def __init__(self):
        self.file = open('../data/disease.csv', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        writer = csv.writer(self.file)
        data = dict(item)
        writer.writerow((data.get('name', 'null'), data.get('text', 'null')))
        return item

    def close_spider(self, spider):
        self.file.close()


class NamePipeline(object):
    """
    存入到MySQL
    """

    def __init__(self, host, databases, user, password, port):
        self.host = host
        self.databases = databases
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            databases=crawler.settings.get('MYSQL_DATABASES'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )

    def open_spider(self, spider):
        try:
            self.db = pymysql.connect(self.host, self.user, self.password, self.databases, charset='utf8',
                                      port=self.port)
            self.db.ping()
        except Exception as e:
            self.db = pymysql.connect(self.host, self.user, self.password, self.databases, charset='utf8',
                                      port=self.port)
        self.curosr = self.db.cursor()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))
        sql = 'insert into %s (%s) values (%s)' % (item.table, keys, values)
        self.curosr.execute(sql, tuple(data.values()))
        self.db.commit()
        return item

    def close_spider(self, spider):
        self.db.close()
