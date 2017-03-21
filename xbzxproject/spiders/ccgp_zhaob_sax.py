# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:V1.0
@var:中国政府采购网
@note:中国政府采购网-陕西2013至今招标数据

"""

from scrapy.spiders import Spider
from scrapy.selector import Selector
from xbzxproject.items import zhaotou_zhaobItem
from scrapy.http import Request
import re
import datetime


class ccgp_zhaob_saxSpider(Spider):
    name = 'ccgp_shanxi_zhaob'

    debug = False

    proxy = True

    tablename = 'scrapy.zhaotoubiao'

    start_urls = []
    # 当前时间
    d1 = datetime.datetime.now()
    # 几天前的时间  days:天数
    d2 = d1 - datetime.timedelta(days=3)
    day = datetime.datetime.strftime(d1, "%Y:%m:%d")
    today = datetime.datetime.strftime(d2, "%Y:%m:%d")
    # 页数
    for i in xrange(1, 10, 1):
        start_urls.append(
            'http://search.ccgp.gov.cn/dataB.jsp?searchtype=1&page_index={}&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=1&dbselect=bidx&kw=%E5%85%AC%E5%91%8A&start_time={}&end_time={}&timeType=6&displayZone=%E9%99%95%E8%A5%BF%E7%9C%81+&zoneId=61%25&pppStatus=&uniqid=40052&agentName='.format(
                # 'http://search.ccgp.gov.cn/dataB.jsp?searchtype=1&page_index={}&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=1&dbselect=bidx&kw=%E5%85%AC%E5%91%8A&start_time=2013%3A01%3A01&end_time=2016%3A12%3A05&timeType=6&displayZone=%E9%99%95%E8%A5%BF%E7%9C%81+&zoneId=61%25&pppStatus=&uniqid=40052&agentName='.format(
                i, today, day))

    def parse(self, response):
        sel = Selector(response)
        urls = sel.xpath("//ul[@class='vT-srch-result-list-bid']/li").extract()
        for i in range(len(urls)):
            item = zhaotou_zhaobItem()
            item['crl_30101001'] = "".join(
                sel.xpath("(//ul[@class='vT-srch-result-list-bid']/li)[%s]/a/@href" % (i + 1)).extract())
            item['crl_10416003'] = \
                "".join(
                    sel.xpath("(//ul[@class='vT-srch-result-list-bid']/li)[%s]/span/text()" % (i + 1)).extract()).split(
                    "|")[0]
            item['crl_10416018'] = \
                "".join(
                    sel.xpath("(//ul[@class='vT-srch-result-list-bid']/li)[%s]/span/text()" % (i + 1)).extract()).split(
                    "|")[1]
            item['crl_10416022'] = \
                "".join(
                    sel.xpath("(//ul[@class='vT-srch-result-list-bid']/li)[%s]/span/text()" % (i + 1)).extract()).split(
                    "|")[2]
            item['crl_10416002'] = "".join(
                sel.xpath("(//ul[@class='vT-srch-result-list-bid']/li)[%s]/span/a/text()" % (i + 1)).extract())
            item['crl_10416008'] = "".join(sel.xpath(
                "(//ul[@class='vT-srch-result-list-bid']/li)[%s]/span/strong[last()]//text()" % (i + 1)).extract())

            yield Request(item['crl_30101001'], callback=self.parse_item, meta={'item': item})

    def parse_item(self, response):
        sel = Selector(response)
        item = response.meta['item']
        item['crl_10416001'] = "".join(sel.xpath("//h2[@class='tc']//text()").extract())
        item['crl_30101002'] = "".join(sel.xpath("//div[@class='vT_detail_content w760c']//text()").extract())
        item['crl_30101002'] = re.sub(r"\xa0", "", item['crl_30101002'])
        item['crl_30101003'] = u"中国政府采购网"
        item['crl_30101004'] = u"公开招标"

        return item