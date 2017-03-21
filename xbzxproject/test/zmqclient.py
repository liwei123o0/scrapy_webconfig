# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:v.1
@var:zmq
@note:zmqclient

"""

import zmq

content = zmq.Context()
socket = content.socket(zmq.SUB)

socket.connect("tcp://127.0.0.1:5050")
socket.setsockopt(zmq.SUBSCRIBE, '')
while True:
    print  socket.recv_unicode()
