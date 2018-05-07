# -*-coding:utf-8 -*-
import pymysql
import re
import sys
import random
from imp import reload
from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy_splash import SplashRequest

from bilibili_user_scrapy.items import BilibiliUserScrapyItem

reload(sys)

# global uas_list
# global headers
# global proxies
# 获取随机user_agent
def LoadUserAgents(uafile):
    """
    uafile : string
        path to text file of user agents, one per line
    """
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1-1])
    # random的序列随机混合方法
    random.shuffle(uas)
    return uas

ua_list = LoadUserAgents("user_agents.txt")
# 默认header
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://space.bilibili.com/45388',
    'Origin': 'http://space.bilibili.com',
    'Host': 'space.bilibili.com',
    'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
}
# ip代理池
proxies = {
'http':'http://140.240.81.16:8888',
'http':'http://185.107.80.44:3128',
'http':'http://203.198.193.3:808',
'http':'http://125.88.74.122:85',
'http':'http://125.88.74.122:84',
'http':'http://125.88.74.122:82',
'http':'http://125.88.74.122:83',
'http':'http://125.88.74.122:81',
'http':'http://123.57.184.70:8081'
}

class BILIBILIUserSpider(Spider):
    # global ua_list
    # global headers
    # global proxies
    name = "bilibili_user_scrapy"
    headers = {'User-Agent':random.choice(ua_list),
               'Referer':'http://space.bilibili.com/'+str(random.randint(9000,10000))+'/'}
    start_urls = ["https://space.bilibili.com/4505469#/",]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, args={'wait':0.5},
                endpoint='render.html',splash_headers=headers,
                )

    def parse(self, response):
        item = BilibiliUserScrapyItem()

        attention = response.xpath("//*[@id=\"n-gz\"]/text()").extract_first()
        fans = response.xpath("//*[@id=\"n-fs\"]/text()").extract_first()
        level = response.xpath("//*[@id=\"app\"]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[1]/a[1]/@lvl").extract_first()
        uid = response.xpath("//*[@id=\"page-index\"]/div[2]/div[6]/div[2]/div/div/div[1]/div[1]/span[2]/text()").extract_first()
        sex = response.xpath("//*[@id=\"h-gender\"]/@class").extract_first()
        
        item['attention'] = int(attention)
        item['birthday'] = response.xpath("//*[@id=\"page-index\"]/div[2]/div[6]/div[2]/div/div/div[2]/div[1]/span[2]/text()").extract_first().strip()
        item['fans'] = int(fans)
        item['level'] = int(level)
        item['name'] = response.xpath("//*[@id=\"h-name\"]/text()").extract_first()
        item['place'] = response.xpath("//*[@id=\"page-index\"]/div[2]/div[6]/div[2]/div/div/div[2]/div[2]/a/text()").extract_first()
        item['regtime'] = response.xpath("//*[@id=\"page-index\"]/div[2]/div[6]/div[2]/div/div/div[1]/div[2]/span[2]/text()").extract_first().strip()
        item['uid'] = int(uid)
        item['mid'] = uid
        if len(sex.split(" ")) == 3:
            item['sex'] = sex.split(" ")[2]
        else:
            item['sex'] = 'null'
        if item['place'] is None:
            item['place'] = "null"
        print("----1----",type(item['uid']))
        #item['coins'] = response.xpath("/html/body/div[1]/div/div[2]/div[3]/ul/li[1]/div/div[1]/div[2]/div[1]/a/span[2]/text()").extract_first()
        #item['friend'] = item["fans"]
        #item['exp'] = response.xpath("/html/body/div[1]/div/div[2]/div[3]/ul/li[1]/div/div[1]/div[3]/a/div/div[3]/div/text()").extract_first()
        
        yield item
