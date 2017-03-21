# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:v1.0
@var:信用陕西
@note:信用陕西_行政许可数据采集

"""

from scrapy.spiders import Spider
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from xbzxproject.items import XingZhengCFItem
from scrapy.selector import Selector
from scrapy.http import Request


class sxcredit_xkSpider(Spider):
    # 获取额外参数
    def __init__(self, spider_jobid=None, *args, **kwargs):
        self.spider_jobid = spider_jobid
        super(sxcredit_xkSpider, self).__init__(*args, **kwargs)

    name = 'sxcredit_cf'

    debug = False

    proxy = False

    tablename = u'scrapy.xingzheng'

    start_urls = [
        "http://www1.sxcredit.gov.cn:8080/WebGovAppSgs/a/sgsxy/xzcfFind?pageNo=1&pageSize=20",
        # "http://www1.sxcredit.gov.cn:8080/WebGovAppSgs/a/sgsxy/xzcfFind?pageNo=2&pageSize=10000",
        # "http://www1.sxcredit.gov.cn:8080/WebGovAppSgs/a/sgsxy/xzcfFind?pageNo=3&pageSize=10000",
    ]

    def parse(self, response):
        sel = Selector(response)

        urls = sel.xpath("//table[@class='gs_list']//tr[position()>1]/@onclick").extract()
        for url in urls:
            idx = url.split(",")
            id = idx[1].replace("'", "")
            m0101 = idx[2].replace("'", "")
            state = idx[4].replace("'", "").replace(")", "")
            uri = u"http://www1.sxcredit.gov.cn:8080/WebGovAppSgs/a/sgsxy/cfxxDetail?depId=&id=%s&m010101=%s&state=%s&flag=" % (
                id, m0101, state,)
            yield Request(uri, callback=self.parse_item)

    def parse_item(self, response):
        l = ItemLoader(XingZhengCFItem(), response)

        l.add_value("crl_30101001", response.url)
        l.add_value("crl_30101003", u"信用陕西")
        l.add_value("crl_30101004", u"行政处罚")

        l.add_xpath("crl_10101001", "//table[@class='gs_table']//td/span/text()", MapCompose(unicode.strip))
        l.add_xpath("crl_20201001", "//table[@class='gs_table']//tr[2]/td[last()]/text()", MapCompose(unicode.strip))
        l.add_xpath("crl_20201002", "//table[@class='gs_table']//tr[3]/td[last()]/text()", MapCompose(unicode.strip))
        l.add_xpath("crl_20201003", "//table[@class='gs_table']//tr[4]/td[last()]/text()", MapCompose(unicode.strip))
        l.add_xpath("crl_20201004", "//table[@class='gs_table']//tr[6]/td[last()]/text()", MapCompose(unicode.strip))
        l.add_xpath("crl_20201005", "//table[@class='gs_table']//tr[7]/td[last()]/text()", MapCompose(unicode.strip))
        l.add_xpath("crl_10101002", "//table[@class='gs_table']//tr[8]/td[last()]/text()", MapCompose(unicode.strip))
        l.add_xpath("crl_10101004", "//table[@class='gs_table']//tr[9]/td[last()]/text()", MapCompose(unicode.strip))
        l.add_xpath("crl_10101003", "//table[@class='gs_table']//tr[10]/td[last()]/text()", MapCompose(unicode.strip))
        l.add_xpath("crl_10101005", "//table[@class='gs_table']//tr[11]/td[last()]/text()", MapCompose(unicode.strip))
        l.add_xpath("crl_10101007", "//table[@class='gs_table']//tr[13]/td[last()]/text()", MapCompose(unicode.strip))
        l.add_xpath("crl_20201007", "//table[@class='gs_table']//tr[14]/td[last()]/text()", MapCompose(unicode.strip))
        l.add_xpath("crl_20201006", "//table[@class='gs_table']//tr[15]/td[last()]/text()", MapCompose(unicode.strip))
        l.add_xpath("crl_20201008", "//table[@class='gs_table']//tr[16]/td[last()]/text()", MapCompose(unicode.strip))
        l.add_xpath("crl_20201009", "//table[@class='gs_table']//tr[17]/td[last()]/text()", MapCompose(unicode.strip))
        l.add_xpath("crl_20201010", "//table[@class='gs_table']//tr[18]/td[last()]/text()", MapCompose(unicode.strip))

        return l.load_item()
