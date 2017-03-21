# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:v1.0
@var:zmq消息队列server端
@note:用于实时显示采集状况

"""

import zmq


# 广播zmq服务端
class ServerZmq(object):
    def __init__(self):
        self.connect = zmq.Context()
        self.socket = self.connect.socket(zmq.PUB)

    # "tcp://127.0.0.1:5050"
    def ZmqConnect(self, tcp):
        self.socket.bind(tcp)

    def ZmqServerSend(self, msg):
        self.socket.send_unicode(msg)

if __name__ == "__main__":
    # 服务端发送例子
    msg = ServerZmq()
    msg.ZmqConnect(tcp=u"tcp://127.0.0.1:5050")
    msg.ZmqServerSend(msg=u"test")
