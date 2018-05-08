# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliUserScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # coins = scrapy.Field()
    # friend = scrapy.Field()
    # exp = scrapy.Field()
    uid = scrapy.Field() # int id
    mid = scrapy.Field() # str id
    name = scrapy.Field()
    sex = scrapy.Field()    
    regtime = scrapy.Field()
    birthday = scrapy.Field()
    place = scrapy.Field()
    fans = scrapy.Field()    
    attention = scrapy.Field()
    level = scrapy.Field()    