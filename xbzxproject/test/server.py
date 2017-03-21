# -*- coding: utf-8 -*-
#! /usr/bin/env python

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
client = context.socket(zmq.SUB)
# client.connect('tcp://127.0.0.1:6666')
client.connect('tcp://192.168.3.230:61616')
while True:
    time.sleep(0.5)
    client.send("123")