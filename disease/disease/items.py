# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item
from scrapy.loader.processors import Join, TakeFirst, MapCompose


class DiseaseItem(Item):
    table = 'name'
    name = Field(output_processor=TakeFirst())
    text = Field(
        input_processor=MapCompose(lambda x: x.strip()),
        output_processor=Join()
    )


class DaYiItem(Item):
    table = 'dayi'
    name = Field()
    text = Field()


class HaodfItem(Item):
    name = Field()