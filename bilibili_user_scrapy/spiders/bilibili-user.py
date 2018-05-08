# -*-coding:utf-8 -*-
import pymysql
import re
import sys
import random
import time
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


# 主爬虫类
class BILIBILIUserSpider(Spider): 

    name = "bilibili_user_scrapy"

    start_urls = []
    # 截止2018/5/2日，B站注册账号数量
    start = 1
    end = 323000449

    # 构造url，根据机能分批爬取，未进行分布式爬虫    
    for i in range(10, 100):
        url = "https://space.bilibili.com/"+str(i)+"/#/"
        start_urls.append(url)
    

    def start_requests(self):
        for url in self.start_urls:
            time.sleep(1)
            # 随机headers
            headers = {'User-Agent':random.choice(ua_list),
               'Referer':'http://space.bilibili.com/'+str(random.randint(9000,10000))+'/'}
            yield SplashRequest(url=url, callback=self.parse, args={'wait':0.5},
                endpoint='render.html',splash_headers=headers,
                )

    def parse(self, response):
        # 爬虫item类
        item = BilibiliUserScrapyItem()

        #一些常规的元素抓取
        attention = response.xpath("//*[@id=\"n-gz\"]/text()").extract_first()
        fans = response.xpath("//*[@id=\"n-fs\"]/text()").extract_first()
        level = response.xpath("//*[@id=\"app\"]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[1]/a[1]/@lvl").extract_first()
        # 由于未知的原因，部分页面无法正确加载某些元素
        # 当元素为None时，将其设置为‘null’
        # 但uid特殊，必须存在，所以从response.url中截取
        uid = response.url[27:-3]
        # uid = response.xpath("//*[@id=\"page-index\"]/div[2]/div[6]/div[2]/div/div/div[1]/div[1]/span[2]/text()").extract_first()
        sex = response.xpath("//*[@id=\"h-gender\"]/@class").extract_first()
        
        # 小数值直接int
        item['attention'] = int(attention)
        item['level'] = int(level)

        item['birthday'] = response.xpath("//*[@id=\"page-index\"]/div[2]/div[6]/div[2]/div/div/div[2]/div[1]/span[2]/text()").extract_first()
        item['name'] = response.xpath("//*[@id=\"h-name\"]/text()").extract_first().strip()
        item['place'] = response.xpath("//*[@id=\"page-index\"]/div[2]/div[6]/div[2]/div/div/div[2]/div[2]/a/text()").extract_first()
        item['regtime'] = response.xpath("//*[@id=\"page-index\"]/div[2]/div[6]/div[2]/div/div/div[1]/div[2]/span[2]/text()").extract_first()
        
        item['uid'] = int(uid)
        item['mid'] = uid
        # 对性别进行处理
        if len(sex.split(" ")) == 3:
            item['sex'] = sex.split(" ")[2]
        else:
            item['sex'] = 'null'
        
        # 对地址进行处理
        if item['place'] is None:
            item['place'] = "null"        

        # 对fans进行处理
        if "万" in fans:
            item['fans'] = int(float(fans[:-3])*10000)
        else:
            item['fans'] = int(fans)

        # 对生日进行处理
        if item['birthday'] is None:
            item['birthday'] = "null"
        else:
            item['birthday'] = item['birthday'].strip()

        # 对注册时间进行处理
        if item['regtime'] is None:
            item['regtime'] = "null"
        else:
            item['regtime'] = item['regtime'].strip()

        # 这些项暂时无法直接从界面获取
        #item['coins'] = response.xpath("/html/body/div[1]/div/div[2]/div[3]/ul/li[1]/div/div[1]/div[2]/div[1]/a/span[2]/text()").extract_first()
        #item['friend'] = item["fans"]
        #item['exp'] = response.xpath("/html/body/div[1]/div/div[2]/div[3]/ul/li[1]/div/div[1]/div[3]/a/div/div[3]/div/text()").extract_first()
        
        yield item