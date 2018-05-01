# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliUserScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    uid = scrapy.Field()
    name = scrapy.Field()
    sex = scrapy.Field()
    coins = scrapy.Field()
    regtime = scrapy.Field()
    birthday = scrapy.Field()
    place = scrapy.Field()
    fans = scrapy.Field()
    friend = scrapy.Field()
    attention = scrapy.Field()
    level = scrapy.Field()
    exp = scrapy.Field()

