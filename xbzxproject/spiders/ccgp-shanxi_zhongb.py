# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:v1.0
@var:陕西省政府采购
@note:陕西省政府采购网-中标信息

"""

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import scrapy
import json

# class ccgp_sax_zhongbSpider(Spider):
#     name = 'ccgp_sax_zhongb'
#
#     debug = True
#
#     tablename = 'scrapy.zhaotoubiao'
#
#     webdriver = True
#
#     start_urls = [
#         # 'http://www.ccgp-shaanxi.gov.cn/index.jsp',
#         'https://www.baidu.com'
#     ]
#
#     def parse(self, response):
#         print "{:>30^#}".format("123")
#         print response.body
