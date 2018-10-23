# -*- coding: utf-8 -*-

import scrapy
from pyquery import PyQuery
from ..items import City58Item
from scrapy import Request


class City58TestSpider(scrapy.Spider):
    name = 'city58_test'  #必不可少的爬虫名字，启动的关键
    allowed_domains = ['58.com']
    start_urls = ['http://bj.58.com/chuzu/']   #开始爬取的链接

    def parse(self, response):
        jpy = PyQuery(response.text)
        li_list = jpy('body > div.mainbox > div.main > div.content > div.listBox > ul > li').items() #记得带上.items()
        for it in li_list:
            a_tag = it(' div.des > h2 > a')
            item = City58Item()
            item['name'] = a_tag.text()   #a_tag取出文本
            item['url'] = a_tag.attr('href')  #取出href参数
            item['price'] = it('div.listliright > div.money > b').text()

            test_request = response.follow('/chuzu/pn2/', callback=self.parse)      #使用follow方法将/chuzu/pn2这个相对路径返回为绝对路径，然后调用self.parse()函数
            test_request2 = Request('//bj.58.com/chuzu/pn3/',
                                    callback=self.parse,
                                    errback=self.error_back,    #调用自定义的错误回调函数
                                    cookies={},     #cookie为空
                                    headers={},     #header为空
                                    priority=10,
                                    )
            test_request3 = Request('http://58.com',
                                    callback=self.parse,
                                    errback=self.error_back,  # 调用异常函数
                                    priority=10,  # 优先级设为10
                                    meta={'dont_redirect': True}  # 不用重定向
                                    )
            test_request4 = Request('http://58.com',
                                callback=self.parse,
                                errback=self.error_back,
                                priority=10,
                                # meta={'dont_redirect': True}
                                dont_filter=TabError    # 对url不过滤
                                    )
            yield item   #把Item返回给引擎
            yield test_request
            yield test_request2
            yield test_request3
            yield test_request4

    def error_back(self, e):
        _ = self
        print(e)
