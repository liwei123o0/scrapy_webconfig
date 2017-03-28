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
from xbzxproject.utils.loadconfig import loadscrapyconf
import re, pymongo


# mysql入库Pipeline
class XbzxprojectPipeline(object):
    # 开启爬虫初始化工作
    conf = loadscrapyconf()['mysql']

    def open_spider(self, spider):
        self.cout = 1
        self.conn = MySQLdb.connect(host=self.conf.get("host", "localhost"), port=self.conf.get("port", 3306),
                                    user=self.conf.get("user", "root"), passwd=self.conf.get("passwd", "root"),
                                    charset=u"utf8")
        self.cur = self.conn.cursor()
        # MongoDB 入库
        # self.client = pymongo.MongoClient(u'localhost', 27017)
        # self.db = self.client.user.spidertest
        # zmq消息队列
        # self.socket = ServerZmq()
        # self.socket.ZmqConnect(u"tcp://127.0.0.1:5050")
        logging.info(u"mysql连接成功!")
        # logging.info(u"zmq启动成功!")
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
            # zmq 发送请求
            # self.socket.ZmqServerSend(u"{:>13.13}:{}".format(k, v))
            fields.append(k)
            values.append(v)
        # debug为true时,数据入库!
        if spider.debug:
            self.cur.execute(
                u"SELECT id FROM {}.net_spider WHERE spider_name='{}';".format(self.conf.get("databases"),
                                                                               spider.name_spider))
            gen_gendbtable_id = self.cur.fetchall()[0][0]
            self.cur.execute(
                u"SELECT id FROM  {}.net_gendbtable WHERE net_spider_id ='{}';".format(self.conf.get("databases"),
                                                                                       gen_gendbtable_id))
            net_spider_id = self.cur.fetchall()[0][0]
            self.cur.execute(
                u"SELECT name,comments FROM  {}.net_gendbtable_column WHERE gen_gendbtable_id='{}';".format(
                    self.conf.get("databases"), net_spider_id))
            datanames = dict(self.cur.fetchall())
            keys = item.keys()
            data = "'url':'%s'," % item['url']
            for key in keys:
                comments = datanames.get(key)
                if comments is None:
                    continue
                data += "'%s':'%s'," % (comments, item[key].replace('"', ""))
            data = "{" + data + "}"
            try:
                self.cur.execute(
                    u'INSERT INTO %s.net_spider_temp(name_spider,spider_data) VALUES("%s","%s");' % (
                        self.conf.get("databases"), spider.name_spider, str(data)))
                self.conn.commit()
            except MySQLdb.Error, e:
                logging.error(u"Mysql Error %d: %s" % (e.args[0], e.args[1]))
        else:
            try:
                self.cur.execute(
                    u"SELECT  id FROM {}.net_spider WHERE  spider_name='{}'".format(self.conf.get("databases"),
                                                                                    spider.name_spider))
                Net_Spider_Id = self.cur.fetchall()[0][0]
                self.cur.execute(
                    u"SELECT  name FROM {}.net_gendbtable WHERE  net_spider_id='{}'".format(self.conf.get("databases"),
                                                                                            Net_Spider_Id))
                TableName = self.cur.fetchall()
                if TableName:
                    TableName = "net_" + TableName[0][0]
                    # 根据 item 字段插入数据
                    self.cur.execute(
                        u"INSERT INTO {}.{}({}) VALUES({});".format(self.conf.get("databases"), TableName,
                                                                    u",".join(fields), u','.join([u'%s'] * len(fields)))
                        , values)
                    self.conn.commit()
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
        # self.client.close()
        logging.info(u"mysql关闭成功")
