# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:V1.0
@var:中标信息清洗
@note:中标信息清洗及入库等

"""


import re
import MySQLdb
from xbzxproject.utils import loadconfig
import datetime
import logging


# 中标公司信息清洗
def zbxx(database, tablename, days):
    conn = MySQLdb.connect(host="192.168.10.24", port=3306, user="root", passwd="root", charset="utf8")
    cur = conn.cursor()
    now = datetime.datetime.now()
    day = now - datetime.timedelta(days=days)
    day = day.strftime(u"%Y-%m-%d 00:00:00")
    cur.execute(u"SELECT content,url FROM {}.{} WHERE insert_time >='{}';".format(database, tablename, day))
    contents = cur.fetchall()

    for c in contents:
        cc = c[0]
        r = re.findall(u'(?<=中标单位：).*?公司', cc)
        r1 = re.findall(u'(?<=中标候选人：).*?公司', cc)
        j = re.findall(u'(?<=中标价格：).*?\d+[.|\d]+\d+', cc)
        j1 = re.findall(u'(?<=中标金额：).*?元', cc)
        j2 = re.findall(u'(?<=成交金额).*?元', cc)
        j3 = re.findall(u'(?<=成交金额：).*?整', cc)

        if len(r) > 0:
            print r[0], c[1]
            cur.execute(u"UPDATE {}.{} SET qyname='{}' WHERE url = '{}'".format(database, tablename, r[0], c[1]))
        elif len(r1) > 0:
            print r1[0], c[1]
            cur.execute(u"UPDATE {}.{} SET qyname='{}' WHERE url = '{}'".format(database, tablename, r1[0], c[1]))
        elif len(j) > 0:
            print j[0], c[1]
            cur.execute(u"UPDATE {}.{} SET zbje='{}' WHERE url = '{}'".format(database, tablename, j[0], c[1]))
        elif len(j1) > 0:
            print j1[0], c[1]
            cur.execute(u"UPDATE {}.{} SET zbje='{}' WHERE url = '{}'".format(database, tablename, j1[0], c[1]))
        elif len(j2) > 0:
            print j2[0], c[1]
            cur.execute(u"UPDATE {}.{} SET zbje='{}' WHERE url = '{}'".format(database, tablename, j2[0], c[1]))
        elif len(j3) > 0:
            print j3[0], c[1]
            cur.execute(u"UPDATE {}.{} SET zbje='{}' WHERE url = '{}'".format(database, tablename, j3[0], c[1]))
        conn.commit()
    cur.close()
    conn.close()


u"""数据清洗添加主题识别码
tablename参数:待清洗表
days : 清洗天数(从当前天数开始算起)
"""


def qxdata(tablename1, tablename2, days):
    words = loadconfig.loadname()
    conn = MySQLdb.connect(host="192.168.10.24", port=3306, user="root", passwd="root", charset="utf8")
    cur = conn.cursor()
    cout = 1
    u"""清空临时表
    """
    logging.warning(u"清空临时表:%s中..." % tablename1)
    cur.execute(u"TRUNCATE temp.{};".format(tablename1))
    logging.warning(u"清空临时表:%s中..." % tablename2)
    cur.execute(u"TRUNCATE temp.{};".format(tablename2))
    u"""插入待清洗数据
    """
    now = datetime.datetime.now()
    day = now - datetime.timedelta(days=days)
    day = day.strftime(u"%Y-%m-%d 00:00:00")
    logging.warning(u"插入待清洗数据表:%s..." % tablename1)
    cur.execute(
        u"INSERT INTO temp.{} SELECT * FROM yqapp.{} WHERE insert_time >= '{}' ;".format(tablename1, tablename1, day))
    logging.warning(u"插入待清洗数据表:%s..." % tablename2)
    cur.execute(
        u"INSERT INTO temp.{} SELECT * FROM yqapp.{} WHERE insert_time >= '{}' ;".format(tablename2, tablename2, day))

    u"""清洗主体识别码
    """

    for w in words:
        logging.warning(u"已执行第%s条" % cout)
        ztsbm = w[1]
        word = w[0]
        cur.execute(u"UPDATE temp.{} SET ztsbm='{}' WHERE qyname LIKE '%{}%'".format(tablename1, ztsbm, word))
        # 企业新闻清洗
        cur.execute(
            u"UPDATE temp.{} SET ztsbm='{}',qyname='{}' WHERE content LIKE '%{}%'".format(tablename2, ztsbm, word,
                                                                                          word))
        # cur.execute(u"UPDATE yqapp.zhaopin SET ztsbm={} WHERE name LIKE '%{}%'".format(ztsbm,word))
        conn.commit()
        cout += 1
    logging.warning(u'删除没有主体识别码数据中...')
    cur.execute(u"DELETE FROM temp.{} WHERE ISNULL(ztsbm)".format(tablename1))
    cur.execute(u"DELETE FROM temp.{} WHERE ISNULL(ztsbm)".format(tablename2))
    conn.commit()

    logging.warning(u"将清洗完的完整数据插入到清洗表中")
    cur.execute(
        u"INSERT INTO temp.{}_qx SELECT * FROM temp.{};".format(tablename1, tablename1))
    cur.execute(
        u"INSERT INTO temp.{}_qx SELECT * FROM temp.{};".format(tablename2, tablename2))
    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    # 参数为表明
    #2017-2-03
    logging.warning(u"中标公司信息清洗...")
    zbxx(database='yqapp', tablename='zbxx', days=15)
    qxdata(tablename1='zbxx', tablename2='news', days=15)
