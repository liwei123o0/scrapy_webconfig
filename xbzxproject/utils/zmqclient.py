# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:V1.0
@var:zmq 消息队列客户端
@note: zmq 消息队列 接受信息端

"""

import zmq


# 接受zmq客户端
class ClientZMQ(object):
    def __init__(self):
        self.connect = zmq.Context()
        self.socket = self.connect.socket(zmq.SUB)

    def ZmqConnect(self, tcp):
        self.socket.connect(tcp)
        self.socket.setsockopt(zmq.SUBSCRIBE, '')

    def ZmqClientMessage(self):
        while 1:
            print self.socket.recv()

if __name__ == "__main__":
    # 客户端接受例子
    connect = ClientZMQ()
    connect.ZmqConnect(tcp=u"tcp://127.0.0.1:5050")
    connect.ZmqClientMessage()
