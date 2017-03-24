# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:V1.0
@var:采集状态收集 扩展件
@note:收集采集状态信息及入库!

"""
from scrapy import signals
import datetime
import MySQLdb
import uuid


class StatsPoster(object):
    def __init__(self, crawler):
        self.crawler = crawler
        self.stats = crawler.stats
        # 链接数据库
        self.conn = MySQLdb.connect(host=u'192.168.10.156', user=u'root', passwd=u'root', db=u'DataCollect', port=3306,
                                    charset=u"utf8")
        self.cur = self.conn.cursor()
        self.COLstr = u''  # 列的字段
        self.ROWstr = u''  # 行字段
        self.ColumnStyle = u' VARCHAR(100)'

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.close_spider, signal=signals.spider_closed)
        return o

    def spider_opened(self, spider):
        self.stats.set_value('start_time', datetime.datetime.now())
        if hasattr(spider, 'debug') and spider.debug:
            self.enabled = False
            return
        else:
            self.enabled = True

    def close_spider(self, spider, reason):

        self.stats.set_value('finish_time', datetime.datetime.now(), spider=spider)
        self.stats.set_value('name_spider', spider.name_spider)
        self.stats.set_value('spider_jobid', spider.spider_jobid)
        dic = self.stats.get_stats()
        for key in dic.keys():
            self.COLstr = self.COLstr + key.replace(u"/", u"_") + self.ColumnStyle + u','
            self.ROWstr = (self.ROWstr + u'"%s"' + u',') % (dic[key])
        # 判断表是否存在，存在执行try，不存在执行except新建表，再insert
        try:
            self.cur.execute(u"SELECT * FROM  net_spider_logs")
            for key in dic.keys():
                # 判断该字段是否存在,不存在则创建该字段
                key = key.replace(u"/", u"_")
                self.cur.execute(u"describe net_spider_logs {};".format(key))
                result = len(self.cur.fetchall())
                if result == 0:
                    self.cur.execute(u"ALTER TABLE net_spider_logs ADD COLUMN {} varchar(100); ".format(key))
            self.cur.execute(
                u"INSERT INTO net_spider_logs (%s)VALUES (%s)" % (
                    str(dic.keys()).replace(u"/", u"_").replace(u"[", u"").replace(u"]", u"").replace(u"'", u""),
                    self.ROWstr[:-1]))

        except MySQLdb.Error, e:
            self.cur.execute(u"CREATE TABLE net_spider_logs (%s)" % (self.COLstr[:-1]))
            self.cur.execute(
                u"INSERT INTO net_spider_logs (%s)VALUES (%s)" % (
                    str(dic.keys()).replace(u"/", u"_").replace(u"[", u"").replace(u"]", u"").replace(u"'", u""),
                    self.ROWstr[:-1]))
        self.conn.commit()
        self.cur.close()
        self.conn.close()


if __name__ == '__main__':
    pass
