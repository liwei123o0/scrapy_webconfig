# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:V1.0
@var:采集数据处理
@note:爬虫采集数据加工、处理、入库

"""

import MySQLdb
import logging
from xbzxproject.utils import date_parse
from xbzxproject.utils.zmqserver import ServerZmq
import re, pymongo


# mysql入库Pipeline
class XbzxprojectPipeline(object):
    # 开启爬虫初始化工作
    def open_spider(self, spider):
        self.cout = 1
        self.conn = MySQLdb.connect(host=u"192.168.10.156", port=3306, user=u"root", passwd=u"root", charset=u"utf8")
        self.cur = self.conn.cursor()
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client.user.spidertest
        # zmq消息队列
        self.socket = ServerZmq()
        self.socket.ZmqConnect(u"tcp://127.0.0.1:5050")
        logging.info(u"mysql连接成功!")
        logging.info(u"zmq启动成功!!")
        if spider.proxy:
            logging.info(u"代理已启动...")
        else:
            logging.info(u"无代理状态抓取!")

    def process_item(self, item, spider):

        for k in item:
            item[k] = u"".join(item[k])
            item[k] = re.sub(r"\xa0", "", item[k])
            item[k] = re.sub(r"\u200b", "", item[k])
            item[k] = re.sub(r"\xa5", "", item[k])
        try:
            # 判断字段是否存在
            if 'crl_10416003' in item:
                item['crl_10416003'] = date_parse.parse_date(item['crl_10416003'])
        except:
            logging.error(u"时间格式化错误!")
            return item
        print u"{:=^30}".format(self.cout)
        # 收集item字段名及值
        fields = []
        values = []

        # 显示采集字段及内容
        for k, v in item.iteritems():
            print u"{:>13.13}:{}".format(k, v)
            self.socket.ZmqServerSend(u"{:>13.13}:{}".format(k, v))
            fields.append(k)
            values.append(v)
        # debug为true时,数据入库!
        if spider.debug:
            pass
        else:
            try:
                self.cur.execute(
                    u"SELECT  name FROM DataCollect.net_gendbtable WHERE  id='{}'".format(spider.tablename))
                TableName = self.cur.fetchall()
                if TableName:
                    TableName = "net_" + TableName[0][0]
                    # 根据 item 字段插入数据
                    self.cur.execute(
                        u"INSERT INTO DataCollect.{}({}) VALUES({});".format(TableName, u",".join(fields),
                                                                             u','.join([u'%s'] * len(fields)))
                        , values)
                    self.conn.commit()
                    try:
                        self.db.update({"_id": item['url']}, item, True)
                    except Exception as e:
                        logging.error(u"MongoDB 写入数据失败,失败原因:%s" % e)
                    logging.info(u"数据插入成功!")
                else:
                    logging.error(u"未对该爬虫创建数据库表!")
            except MySQLdb.Error, e:
                logging.error(u"Mysql Error %d: %s" % (e.args[0], e.args[1]))

        self.cout += 1
        return item

    # 关闭爬虫初始化工作
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
        # self.db.close()
        logging.info(u"mysql关闭成功")
