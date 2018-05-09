#利用scrapy爬取哔哩哔哩用户基础信息
- 本爬虫借鉴了github用户airingursb发布在github上的爬虫[bilibili-user](https://github.com/airingursb/bilibili-user)为指导思路，由于哔哩哔哩的网站结构发生了些许变化，我尝试着用scrapy重新实现。
- 数据库结构请见bilibili_user_info.sql文件
- 执行命令  scrapy crawl bilibili_user_scrapy
- （当然要先设置好数据库（笑））
- python 版本 v3.6.5
- scrapy 版本  v1.5.0
- mysql版本 v5.7.18
- 实现思路可见博客[scrapy with bilibili](https://blog.csdn.net/cloud_strife0/article/details/80249828)