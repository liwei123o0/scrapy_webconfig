# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:v1.0
@var:解析js,ajax动态加载数据的网页
@note:js,ajax动态加载数据的中间下载件

"""
from selenium import webdriver
from scrapy.http import Request


class WebDriverDownloader(object):
    def process_request(self, request, spider):
        if spider.webdriver:
            driver = webdriver.PhantomJS()
            driver.get(request.url)
            driver.implicitly_wait(3)
            body = driver.title
            driver.quit()
            return Request(driver.current_url, body=body, request=request)
        else:
            return
