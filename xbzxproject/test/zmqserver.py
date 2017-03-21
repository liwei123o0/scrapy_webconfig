# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:v1.0
@var:zmq
@note:zmq_server

"""
import time
import sys
import stomp

class MyListener(object):
    def on_error(self, headers, message):
        print('received an error %s' % message)

    def on_message(self, headers, message):
        print('received a message %s' % message)


# 官方示例的连接代码
conn = stomp.Connection([('192.1682.3.230', 61616)])

conn.set_listener('', MyListener())
conn.start()
conn.connect()
while 1:
    conn.subscribe(destination='/queue/test', id=1, ack='auto')
    # 注意，官方示例这样发送消息的  $ python simple.py hello world
    # conn.send(body='hello,garfield! this is '.join(sys.argv[1:]), destination='/queue/test')
    conn.send(body='hello,garfield!', destination='/queue/test')

    time.sleep(2)
    conn.disconnect()
