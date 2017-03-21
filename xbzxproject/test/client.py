# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:
@var:
@note:

"""
import zmq

import zmq
import time

context = zmq.Context()
server = context.socket(zmq.PUSH)
server.bind("tcp://192.168.3.230:61616")
# server.bind('tcp://192.168.3.230:61616')
count = 0
while True:
    server.send('%d' % count)
    print 'send', 'count'
    count += 1
    time.sleep(0.2)
