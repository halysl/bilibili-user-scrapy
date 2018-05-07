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
    start_urls = ["https://space.bilibili.com/4505449#/",]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, args={'wait':0.5},
                endpoint='render.html',
                )

    def parse(self, response):
        item = BilibiliUserScrapyItem()

        attention = response.xpath("//*[@id=\"n-gz\"]/text()").extract_first()
        fans = response.xpath("//*[@id=\"n-fs\"]/text()").extract_first()
        level = response.xpath("//*[@id=\"app\"]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[1]/a[1]/@lvl").extract_first()
        uid = response.xpath("//*[@id=\"page-index\"]/div[2]/div[6]/div[2]/div/div/div[1]/div[1]/span[2]/text()").extract_first()
        
        item['attention'] = int(attention)
        item['birthday'] = response.xpath("//*[@id=\"page-index\"]/div[2]/div[6]/div[2]/div/div/div[2]/div[1]/span[2]/text()").extract_first().strip()
        item['fans'] = int(fans)
        item['level'] = int(level)
        item['name'] = response.xpath("//*[@id=\"h-name\"]/text()").extract_first()
        item['place'] = response.xpath("//*[@id=\"page-index\"]/div[2]/div[6]/div[2]/div/div/div[2]/div[2]/a/text()").extract_first()
        item['regtime'] = response.xpath("//*[@id=\"page-index\"]/div[2]/div[6]/div[2]/div/div/div[1]/div[2]/span[2]/text()").extract_first().strip()
        item['sex'] = response.xpath("//*[@id=\"h-gender\"]/@class").extract_first().split(" ")[2]
        item['uid'] = int(uid)
        item['mid'] = uid
        print("----1----",type(item['uid']))
        #item['coins'] = response.xpath("/html/body/div[1]/div/div[2]/div[3]/ul/li[1]/div/div[1]/div[2]/div[1]/a/span[2]/text()").extract_first()
        #item['friend'] = item["fans"]
        #item['exp'] = response.xpath("/html/body/div[1]/div/div[2]/div[3]/ul/li[1]/div/div[1]/div[3]/a/div/div[3]/div/text()").extract_first()
        
        yield item
