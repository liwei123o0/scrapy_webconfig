# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:V1.0
@var:新闻类通用模版
@note:新闻通用模版采集~必须字段: spider_jobid name_spider

"""
from scrapy import Item, Field
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.spiders import CrawlSpider, Rule
from xbzxproject.utils.loadconfig import loadMySQL, fileconfig
import logging
import json


class loadSpider(CrawlSpider):
    name = "news"

    # 加载规则配置文件
    # 获取额外参数
    def __init__(self, spider_jobid=None, name_spider=None, *args, **kwargs):
        self.spider_jobid = spider_jobid
        self.name_spider = name_spider
        self.loadconf(name_spider, spider_jobid)
        super(loadSpider, self).__init__(*args, **kwargs)

    # 规则配置
    def loadconf(self, name_spider, spider_jobid):
        if name_spider == None or spider_jobid == None:
            raise logging.error(u"name_spider或spider_jobid 不能为空!!!")
        self.conf = fileconfig(name_spider)
        print "conf:%s" % self.conf
        self.allowed_domains = [self.conf.get("allowed_domains", "")]

        self.debug = True
        if self.conf.get("proxy").lower() in "false":
            self.proxy = False
        else:
            self.proxy = True

        self.tablename = spider_jobid

        self.start_urls = [self.conf.get("start_urls", "")]
        # 判断是否翻页规则解析 (方法一)
        rules = json.loads(self.conf.get("rules"))
        if rules.get("rules", "") == "":
            logging.error(u"规则解析未得到!!!")
            return
        keys = len(rules.get("rules").keys())
        if keys == 1:
            print rules.get("rules_listxpath", "")
            self.rules = [
                Rule(LinkExtractor(restrict_xpaths="{}".format(rules.get("rules").get("rules_listxpath", ""))),
                     follow=False,
                     callback="parse_item")
            ]
        elif keys == 2:
            self.rules = [
                Rule(LinkExtractor(restrict_xpaths="{}".format(rules.get("rules").get("reles_pagexpath"))), follow=True,
                     ),
                Rule(LinkExtractor(restrict_xpaths="{}".format(rules.get("rules").get("rules_listxpath"))),
                     follow=False,
                     callback="parse_item")
            ]

    # 内容解析
    def parse_item(self, response):
        item = Item()
        fields = json.loads(self.conf.get("fields"))
        l = ItemLoader(item, response)
        item.fields["url"] = Field()
        item.fields["spider_jobid"] = Field()
        l.add_value("url", response.url)
        l.add_value("spider_jobid", self.spider_jobid)
        # 加载动态库字段建立Field,xpath规则 (方法一)
        for k in loadMySQL(self.conf.get("spider_type")):
            if fields.get("fields", "") == "":
                logging.error(u"内容解析未得到!!!")
                return l.load_item()
            if fields.get("fields").get(k[0]) != None:
                item.fields[k[0]] = Field()
                if fields.get("fields").get(k[0]).keys()[0] == "xpath":
                    l.add_xpath(k[0], "{}".format(fields.get("fields").get(k[0]).get("xpath")),
                                MapCompose(unicode.strip))
                elif fields.get("fields").get(k[0]).keys()[0] == "value":
                    l.add_value(k[0], "{}".format(fields.get("fields").get(k[0]).get("value")))
        return l.load_item()