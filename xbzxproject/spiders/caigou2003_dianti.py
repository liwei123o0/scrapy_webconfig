# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:v1.0
@var:电梯采购网
@note:电梯采购网-招标信息采集

"""

from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from xbzxproject.items import zhaotou_zhaobItem


class caigou2003_zhaobSpider(CrawlSpider):
    name = 'caigou2003zhaob_dianti'

    debug = True

    proxy = False

    tablename = 'scrapy.zhaotoubiao'

    start_urls = ['http://dianti.caigou2003.com/diantibiaoxun/zhaobiao/index.html']

    for i in xrange(2, 295, 1):
        start_urls.append(
            "http://dianti.caigou2003.com/diantibiaoxun/zhaobiao/index_{}.html".format(
                i))

    rules = [
        Rule(LinkExtractor(restrict_xpaths="//h3/a"), follow=False,
             callback="parse_item")
    ]

    def parse_item(self, response):
        l = ItemLoader(zhaotou_zhaobItem(), response)
        # URL
        l.add_value("crl_30101001", response.url)
        # 网页内容
        l.add_xpath("crl_30101002", "//div[@class='wz']//text()",
                    MapCompose(unicode.strip))
        l.add_value("crl_30101003", u"电梯采购网")
        l.add_value("crl_30101004", u"公开招标")
        # 项目标题
        l.add_xpath("crl_10416001", "///h2//text()", MapCompose(unicode.strip))
        # 发布时间
        l.add_xpath("crl_10416003", "//div[@class='zz']//text()",
                    MapCompose(unicode.strip))

        return l.load_item()
