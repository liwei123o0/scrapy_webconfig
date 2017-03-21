# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:v1.0
@var:西安市财政局
@note:西安市财政局招标信息采集

"""


from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from xbzxproject.items import zhaotou_zhaobItem


class xaczj_zhaobSpider(CrawlSpider):
    name = 'xaczj_zhaob'

    debug = True

    proxy = False

    tablename = 'scrapy.zhaotoubiao'

    start_urls = []

    for i in xrange(1, 713, 1):
        start_urls.append(
            "http://www.xaczj.gov.cn/xaczj/werji.jsp.jsp?a10t=712&a10p={}&a10c=14&urltype=tree.TreeTempUrl&wbtreeid=9".format(
                i))

    rules = [
        Rule(LinkExtractor(restrict_xpaths="//a[@class='c3195']"), follow=False,
             callback="parse_item")
    ]

    def parse_item(self, response):
        l = ItemLoader(zhaotou_zhaobItem(), response)
        # URL
        l.add_value("crl_30101001", response.url)
        # 网页内容
        l.add_xpath("crl_30101002", "//div[@id='vsb_content']//text()",
                    MapCompose(unicode.strip))
        l.add_value("crl_30101003", u"西安市财政局")
        l.add_value("crl_30101004", u"公开招标")
        # 项目标题
        l.add_xpath("crl_10416001", "//td[@class='titlestyle3181']//text()", MapCompose(unicode.strip))
        # 发布时间
        l.add_xpath("crl_10416003", "//span[@class='timestyle3181']//text()",
                    MapCompose(unicode.strip))

        return l.load_item()
