# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:v1.0
@var:西安高新技术产业开发区
@note:西安高新技术产业开发区招标信息采集

"""

from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from xbzxproject.items import zhaotou_zhaobItem


class xdz_zhaobSpider(CrawlSpider):
    name = 'xdz_zhaob'

    debug = True

    proxy = False

    tablename = 'scrapy.zhaotoubiao'

    start_urls = []

    for i in xrange(1, 362, 1):
        start_urls.append(
            "http://www.xdz.com.cn/zwgkdiv/lmzl_list2.jsp?ainfolist106365t=231&ainfolist106365p={}&ainfolist106365c=15&urltype=tree.TreeTempUrl&wbtreeid=20903&p=3".format(
                i))

    rules = [
        Rule(LinkExtractor(restrict_xpaths="//td[@class='titlecontentstyle106365']//a"), follow=False,
             callback="parse_item")
    ]

    def parse_item(self, response):
        l = ItemLoader(zhaotou_zhaobItem(), response)

        l.add_value("crl_30101001", response.url)
        l.add_xpath("crl_30101002", "//div[@id='vsb_content_2']//text() | //div[@id='vsb_content']//text()",
                    MapCompose(unicode.strip))
        l.add_value("crl_30101003", u"西安高新技术产业开发区")
        l.add_value("crl_30101004", u"公开招标")

        l.add_xpath("crl_10416001", "//tbody/tr[1]/td/table/tbody/tr[1]/td//text()", MapCompose(unicode.strip))
        l.add_xpath("crl_10416003", "(//td[@nowrap='nowrap'][11])[1]//text()",
                    MapCompose(unicode.strip))

        return l.load_item()
