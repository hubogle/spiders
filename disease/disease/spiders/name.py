# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from ..items import DiseaseItem
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.loader import ItemLoader


class NameSpider(RedisCrawlSpider):
    name = 'name'
    allowed_domains = ['www.a-hospital.com']
    redis_key = 'name:start_urls'
    rules = (
        Rule(LinkExtractor(allow=r'/w/', restrict_xpaths='//*[@id="bodyContent"]/p[5]')),
        Rule(LinkExtractor(allow=r'/w/', restrict_xpaths='//*[@id="bodyContent"]/*[7]/li'), callback='parse_item'),
    )

    def parse_item(self, response):
        disease_item = ItemLoader(item=DiseaseItem(), response=response)
        disease_item.add_xpath('name', '//*[@id="firstHeading"]/text()')
        disease_item.add_xpath('text',
                               '//*[@id="bodyContent"]/p//text()|//*[@id="bodyContent"]/h2[position()<last()-1]//text()'
                               '|//*[@id="bodyContent"]/h3//text()')
        yield disease_item.load_item()
