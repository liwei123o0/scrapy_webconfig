# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:v1.0
@var:陕西采购与招标网陕西省招投标协会
@note:陕西采购与招标网陕西省招投标协会 - 招标信息采集

"""

from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import MapCompose
from xbzxproject.items import zhaotou_zhaobItem


class sntba_zhaobSpider(CrawlSpider):
    name = 'sntba_zhaob'

    debug = True

    proxy = False

    tablename = 'scrapy.zhaotoubiao'

    start_urls = []

    for i in range(1, 1387, 1):
        start_urls.append("http://www.sntba.com/website/news_list.aspx?category_id=53&page=%s" % i)

    rules = [
        Rule(LinkExtractor(restrict_xpaths="//div[@class='d_bottom']/ul/li"), follow=False, callback="parse_item"),
    ]

    def parse_item(self, response):
        l = ItemLoader(zhaotou_zhaobItem(), response)

        l.add_value("crl_30101001", response.url)
        l.add_xpath("crl_30101002", "//div[@class='entry']//text()", MapCompose(unicode.strip))
        l.add_value("crl_30101003", u"陕西采购与招标网陕西省招投标协会")
        l.add_value("crl_30101004", u"公开招标")

        l.add_xpath("crl_10416001", "//h1/text()", MapCompose(unicode.strip))
        l.add_xpath("crl_10416003", "//span[@class='time']/text()", MapCompose(unicode.strip))

        return l.load_item()
