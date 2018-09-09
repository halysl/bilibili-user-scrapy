# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliUserScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    uid = scrapy.Field()
    name = scrapy.Field()
    sex = scrapy.Field()
    reg_time = scrapy.Field()
    birthday = scrapy.Field()
    city = scrapy.Field()

    exp = scrapy.Field()
    level = scrapy.Field()
    coins = scrapy.Field()

    friend = scrapy.Field()
    attention = scrapy.Field()
    fans = scrapy.Field()