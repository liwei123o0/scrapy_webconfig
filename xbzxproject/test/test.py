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

import time, threading

# 新线程执行的代码:
def loop():
    print 'threding...'

for i in xrange(1000):
    t = threading.Thread(target=loop, name='LoopThread')
    t.start()


