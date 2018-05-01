# -*-coding:utf-8 -*-
import pymysql
import re
from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy_splash import SplashRequest

from bilibili_user_scrapy.items import BilibiliUserScrapyItem

class BILIBILIUserSpider(Spider):
    name = "bilibili_user_scrapy"
    start_urls = ["https://space.bilibili.com/1#/"]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, args={'wait':0.5},
                endpoint='render.html',
                )

    def parse(self, response):
        item = []
        #item["uid"] = response.xpath("//*[@id=\"page-index\"]/div[2]/div[6]/div[2]/div/div/div[1]/div[1]/span[2]/text()").extract_first()
        item["uid"] = 0
        item["name"] = response.xpath("//*[@id=\"h-name\"]/text()").extract_first()
        item["sex"] = response.xpath("//*[@id=\"h-gender\"/@class]").extract_first()
        #item["coins"] = response.xpath("/html/body/div[1]/div/div[2]/div[3]/ul/li[1]/div/div[1]/div[2]/div[1]/a/span[2]/text()").extract_first()
        item["coins"] = 0
        item["regtime"] = response.xpath("//*[@id=\"page-index\"]/div[2]/div[6]/div[2]/div/div/div[1]/div[2]/span[2]/text()").extract_first()
        item["birthday"] = response.xpath("//*[@id=\"page-index\"]/div[2]/div[6]/div[2]/div/div/div[2]/div[1]/a/text()").extract_first()
        item["place"] = response.xpath("//*[@id=\"page-index\"]/div[2]/div[6]/div[2]/div/div/div[2]/div[2]/a/text()").extract_first()
        #item["fans"] = response.xpath("//*[@id=\"n-fs\"]/text()").extract_first()
        #item["friend"] = item["fans"]
        #item["attention"] = response.xpath("//*[@id=\"n-gz\"]").extract_first()
        #item["level"] = response.xpath("/html/body/div[1]/div/div[2]/div[3]/ul/li[1]/div/div[1]/div[3]/a/div/div[1]/@class").extract_first()
        #item["exp"] = response.xpath("/html/body/div[1]/div/div[2]/div[3]/ul/li[1]/div/div[1]/div[3]/a/div/div[3]/div/text()").extract_first()
        item["fans"] = 0
        item["friend"] = 0
        item["attention"] = 0
        item["level"] = 0
        item["exp"] = 0
        yield item
