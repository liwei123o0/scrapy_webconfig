# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:v1.0
@var:天眼查工商信息数据采集
@note:天严查数据采集

"""

from scrapy.spiders import Spider
from xbzxproject.items import GsbasicItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from scrapy_splash import SplashRequest
from scrapy.selector import Selector
from xbzxproject import settings


class gsbasicSpider(Spider):
    name = 'gsbasic'

    proxy = False

    debug = False

    settings.CONCURRENT_REQUESTS = 3

    tablename = 'scrapy.gsbasic'

    start_urls = []

    def start_requests(self):
        from xbzxproject.utils.loadconfig import loadname
        import urllib
        keyword = loadname()
        for key in keyword[150:]:
            url = u"http://www.tianyancha.com/search?key=%s&checkFrom=searchBox" % (urllib.quote(key[0].encode("utf8")))
            # 将请求连接经过splash渲染得到的HTML页面传给parse
            yield SplashRequest(url, self.parse, args={'wait': 4.5,
                                                       'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
                                                       })

    def parse(self, response):
        l = ItemLoader(GsbasicItem(), response)
        sel = Selector(response)
        url = "".join(sel.xpath("(//a[@class='query_name search-new-color'])[1]/@href").extract())
        l.add_value('XY30101001', url)
        yield SplashRequest(url, self.parse_item, args={'wait': 4.5}, meta={'l': l.load_item()})

    def parse_item(self, response):
        l = ItemLoader(response.meta['l'], response)
        sel = Selector(response)
        for i in sel.xpath("//div[@class='ng-isolate-scope']//div/span"):
            if u'基本信息' in i.xpath("./text()").extract()[0]:
                l.add_xpath('name', "//div[@class='company_info_text']/p[@class='ng-binding']//text()",
                            MapCompose(unicode.strip))
                l.add_xpath('XY10102014', "(//div[@class='company_info_text']/span[@class='ng-binding'])[1]/text()",
                            MapCompose(unicode.strip))
                l.add_xpath('XY10111006', "(//div[@class='company_info_text']/span[@class='ng-binding'])[2]/text()",
                            MapCompose(unicode.strip))
                l.add_xpath('XY10405003', "//div[@class='company_info_text']//span[@class='ng-hide']/text()",
                            MapCompose(unicode.strip))
                l.add_xpath('XY10101010', "(//div[@class='company_info_text']/span[@class='ng-binding'])[3]/text()",
                            MapCompose(unicode.strip))
                l.add_xpath('XY10101007', "//td[@class='td-legalPersonName-value c9']//a//text()",
                            MapCompose(unicode.strip))
                l.add_xpath('XY10102001', "//td[@class='td-regCapital-value']//text()",
                            MapCompose(unicode.strip))
                l.add_xpath('XY10101013', "//td[@class='td-regStatus-value']//text()",
                            MapCompose(unicode.strip))
                l.add_xpath('XY10102004', "//td[@class='td-regTime-value']//text()",
                            MapCompose(unicode.strip))
                l.add_xpath('XY10101014',
                            "(//div[@class='row b-c-white company-content']//td[@class='basic-td'])[1]//span//text()",
                            MapCompose(unicode.strip))
                l.add_xpath('XY10101003',
                            "(//div[@class='row b-c-white company-content']//td[@class='basic-td'])[2]//span//text()",
                            MapCompose(unicode.strip))
                l.add_xpath('XY10101012',
                            "(//div[@class='row b-c-white company-content']//td[@class='basic-td'])[3]//span//text()",
                            MapCompose(unicode.strip))
                l.add_xpath('XY10101004',
                            "(//div[@class='row b-c-white company-content']//td[@class='basic-td'])[4]//span//text()",
                            MapCompose(unicode.strip))
                l.add_xpath('XY10102005',
                            "(//div[@class='row b-c-white company-content']//td[@class='basic-td'])[5]//span//text()",
                            MapCompose(unicode.strip),
                            re=u'^(\d+-\d+-\d+)')
                l.add_xpath('XY10102006',
                            "(//div[@class='row b-c-white company-content']//td[@class='basic-td'])[5]//span//text()",
                            MapCompose(unicode.strip),
                            re=u'(?<=至).*')
                l.add_xpath('XY10102008',
                            "(//div[@class='row b-c-white company-content']//td[@class='basic-td'])[6]//span//text()",
                            MapCompose(unicode.strip))
                l.add_xpath('XY10102009',
                            "(//div[@class='row b-c-white company-content']//td[@class='basic-td'])[7]//span//text()",
                            MapCompose(unicode.strip))
                l.add_xpath('XY10101002',
                            "(//div[@class='row b-c-white company-content']//td[@class='basic-td'])[8]//span//text()",
                            MapCompose(unicode.strip))
                l.add_xpath('XY10102003',
                            "(//div[@class='row b-c-white company-content']//td[@class='basic-td ng-scope'])[2]//span//text()",
                            MapCompose(unicode.strip))

            elif u'股东信息' in i.xpath("./text()").extract():
                for x in xrange(len(sel.xpath("//div[@class='col-9 company-main']//div[@class='ng-scope']"))):
                    if u'股东信息' in sel.xpath(
                                    "(//div[@class='col-9 company-main']//div[@class='ng-scope'])[%s]/div[@id]/text()" % (
                                        x + 1)).extract():
                        l.add_xpath('XY10110001',
                                    "(//div[@class='col-9 company-main']//div[@class='ng-scope'])[%s]/div[@class='row b-c-white']//a[@class='ng-binding ng-isolate-scope']//text()" % (
                                        x + 1),
                                    MapCompose(unicode.strip))
                        l.add_xpath('XY10110005',
                                    "(//div[@class='col-9 company-main']//div[@class='ng-scope'])[%s]/div[@class='row b-c-white']//p[@class='f13 ptten']//text()" % (
                                        x + 1),
                                    MapCompose(unicode.strip))
                    elif u'高管信息' in sel.xpath(
                                    "(//div[@class='col-9 company-main']//div[@class='ng-scope'])[%s]/div[@id]/text()" % (
                                        x + 1)).extract():
                        l.add_xpath("XY10109001",
                                    "(//div[@class='col-9 company-main']//div[@class='ng-scope'])[%s]//td/a/text()" % (
                                        x + 1), MapCompose(unicode.strip))
                        l.add_xpath("XY10109004",
                                    "(//div[@class='col-9 company-main']//div[@class='ng-scope'])[%s]//td/span/text()" % (
                                        x + 1), MapCompose(unicode.strip))
                    elif u'对外投资' in sel.xpath(
                                    "(//div[@class='col-9 company-main']//div[@class='ng-scope'])[%s]/div[@id]/text()" % (
                                        x + 1)).extract():
                        l.add_xpath("XY10113001",
                                    "(//div[@class='col-9 company-main']//div[@class='ng-scope'])[%s]//a/span[@class='ng-binding']//text()" % (
                                        x + 1), MapCompose(unicode.strip))
                        l.add_xpath("XY10113002",
                                    "(//div[@class='col-9 company-main']//div[@class='ng-scope'])[%s]//p[@class='f13 ptten']//span//text()" % (
                                        x + 1), MapCompose(unicode.strip))
                    elif u'法律诉讼' in sel.xpath(
                                    "(//div[@class='col-9 company-main']//div[@class='ng-scope'])[%s]/div[@id]/text()" % (
                                        x + 1)).extract():
                        # l.add_xpath("XY20301004",
                        #             "(//div[@class='col-9 company-main']//div[@class='ng-scope'])[%s]//a/span[@class='ng-binding']//text()" % (
                        #                 x + 1), MapCompose(unicode.strip))
                        l.add_xpath("XY20301005",
                                    "(//div[@class='col-9 company-main']//div[@class='ng-scope'])[%s]//div[@class='ptten']//text()" % (
                                        x + 1), MapCompose(unicode.strip))
                        l.add_xpath("XY20301007",
                                    "(//div[@class='col-9 company-main']//div[@class='ng-scope'])[%s]//div[@class='ptten ng-binding']//text()" % (
                                        x + 1), MapCompose(unicode.strip))
                    elif u'变更信息' in sel.xpath(
                                    "(//div[@class='col-9 company-main']//div[@class='ng-scope'])[%s]/div[@id]/text()" % (
                                        x + 1)).extract():
                        l.add_xpath("XY10105004",
                                    "(//div[@class='col-9 company-main']//div[@class='ng-scope'])[%s]//div[@class='in-block change-titleV2']//span[@class='ng-binding']//text()" % (
                                        x + 1), MapCompose(unicode.strip))
                        l.add_xpath("XY10105005",
                                    "(//div[@class='col-9 company-main']//div[@class='ng-scope'])[%s]//div[@class='in-block company-harf-width']//span[@class='ng-binding']//text()" % (
                                        x + 1), MapCompose(unicode.strip))
                        l.add_xpath("XY10105006",
                                    "(//div[@class='col-9 company-main']//div[@class='ng-scope'])[%s]//div[@class='ptten text-dark-color']/div[1]//text()" % (
                                        x + 1), MapCompose(unicode.strip))
                        l.add_xpath("XY10105007",
                                    "(//div[@class='col-9 company-main']//div[@class='ng-scope'])[%s]//div[@class='ptten text-dark-color']/div[2]//text()" % (
                                        x + 1), MapCompose(unicode.strip))

        # 商标信息
        l.add_xpath('XY10406005', "//div[@id='nav-main-brand']//div[@class='text-title-color']//span//text()",
                    MapCompose(unicode.strip))
        l.add_xpath('XY10406001',
                    "//div[@id='nav-main-brand']//div[@class='ptthree'][1]/div[@class='company-sm-left-width in-block']//span//text()",
                    MapCompose(unicode.strip))
        l.add_xpath('XY10406011',
                    "//div[@id='nav-main-brand']//div[@class='ptthree'][2]/div[@class='company-sm-left-width in-block']//span//text()",
                    MapCompose(unicode.strip))
        l.add_xpath('XY10406003',
                    "//div[@id='nav-main-brand']//div[@class='ptthree'][1]/div[@class='in-block']//span//text()",
                    MapCompose(unicode.strip))
        l.add_xpath('XY10406002',
                    "//div[@id='nav-main-brand']//div[@class='ptthree'][2]/div[@class='in-block']//span//text()",
                    MapCompose(unicode.split))
        l.add_xpath('XY10406004', "//img[@class='image']/@src", MapCompose(unicode.strip))

        # 网站备案
        l.add_xpath('LS10101001', "//div[@id='nav-main-icp']//div[@class='ptten'][1]/div[1]//text()",
                    MapCompose(unicode.strip))
        l.add_xpath('LS10405002', "//div[@id='nav-main-icp']//div[@class='ptten'][1]/div[2]//text()",
                    MapCompose(unicode.strip))
        l.add_xpath('XY10405004', "//div[@id='nav-main-icp']//div[@class='ptten'][2]/div[1]//text()",
                    MapCompose(unicode.strip))
        l.add_xpath('XY10405005', "//div[@id='nav-main-icp']//div[@class='ptten'][2]/div[2]//text()",
                    MapCompose(unicode.strip))
        l.add_xpath('XY10405006', "//div[@id='nav-main-icp']//div[@class='ptten'][3]/div[1]//text()",
                    MapCompose(unicode.strip))
        l.add_xpath('XY10405007', "//div[@id='nav-main-icp']//div[@class='ptten'][3]/div[2]//text()",
                    MapCompose(unicode.strip))

        # 著作权
        l.add_xpath('XY10419001', "//div[@class='text-title-color ng-binding']//text()",
                    MapCompose(unicode.strip))
        l.add_xpath('XY10419013',
                    "//div[@id='nav-main-copyright']//div[@class='ptten'][2]/div[@class='in-block company-left-width mrten']//span//text()",
                    MapCompose(unicode.strip))
        l.add_xpath('XY10419003',
                    "//div[@id='nav-main-copyright']//div[@class='ptten'][2]/div[@class='in-block']//span//text()",
                    MapCompose(unicode.strip))
        l.add_xpath('XY10419002',
                    "//div[@id='nav-main-copyright']//div[@class='ptten'][3]/div[@class='in-block company-left-width mrten']//span//text()",
                    MapCompose(unicode.strip))
        l.add_xpath('XY10419004',
                    "//div[@id='nav-main-copyright']//div[@class='ptten'][3]/div[@class='in-block']//span//text()",
                    MapCompose(unicode.strip))

        # 招聘信息
        l.add_xpath('XY10417001', "//div[@id='nav-main-employe']//div[@class='ptten'][1]/div[1]//text()",
                    MapCompose(unicode.strip))
        l.add_xpath('XY10417002', "//div[@id='nav-main-employe']//div[@class='ptten'][2]/div[1]//text()",
                    MapCompose(unicode.strip))
        l.add_xpath('XY10417004', "//div[@id='nav-main-employe']//div[@class='ptten'][2]/div[2]//text()",
                    MapCompose(unicode.strip))
        l.add_xpath('XY10417005', "//div[@id='nav-main-employe']//div[@class='ptten'][3]/div[2]//text()",
                    MapCompose(unicode.strip))

        return l.load_item()
