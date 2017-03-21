# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:V1.0
@var:获取系统状态信息
@note:系统内存

"""

import psutil
import time
import os
import platform


def statuss_system():
    # CUP使用率,间隔1秒检测一次!
    cpu_percent = u"{} %".format(psutil.cpu_percent(interval=1))
    # 总内存
    memory_total = u"{0:.2f}GB".format(psutil.virtual_memory().total / 1024.00 / 1024.00 / 1024.00)
    # 已使用内存
    memory_used = u"{0:.2f}GB".format(psutil.virtual_memory().used / 1024.00 / 1024.00 / 1024.00)
    # 剩余内存
    memory_free = u"{0:.2f}GB".format(psutil.virtual_memory().free / 1024.00 / 1024.00 / 1024.00)
    # 网络下载与上载流量
    netbytes_sent = psutil.net_io_counters().bytes_sent
    netbytes_recv = psutil.net_io_counters().bytes_recv
    time.sleep(1)
    netbytes_sent_last = psutil.net_io_counters().bytes_sent
    net_bytes_recv_last = psutil.net_io_counters().bytes_recv
    net_bytes_recv = (net_bytes_recv_last - netbytes_recv) / 1024.00
    net_bytes_send = (netbytes_sent_last - netbytes_sent) / 1024.00
    if net_bytes_recv >= 1024:
        net_bytes_recv = u"{0:.2f} MB/S".format(net_bytes_recv / 1024.00)
    else:
        net_bytes_recv = u"{0:.2f} KB/S".format(net_bytes_recv)
    if net_bytes_send >= 1024:
        net_bytes_send = u"{0:.2f} MB/S".format(net_bytes_send / 1024.00)
    else:
        net_bytes_send = u"{0:.2f} KB/S".format(net_bytes_send)

    if platform.system().lower() in "windows":
        address = psutil.net_if_addrs().get("\xd2\xd4\xcc\xab\xcd\xf8")[1].__dict__.get("address", "")
    elif platform.system().lower() in "linux":
        address = psutil.net_if_addrs().get("eth0")[0].__dict__.get("address", "")

    system_status = {"cpu_percent": cpu_percent, "memory_total": memory_total, "memory_used": memory_used,
                     "memory_free": memory_free, "net_bytes_send": net_bytes_send, "net_bytes_recv": net_bytes_recv,
                     "address": address}
    return system_status


if __name__ == '__main__':
    pass
    while 1:
        print statuss_system()
        # print (psutil.disk_usage('/').total) /1024.00 /1024.00 /1024.00
        # disk = psutil.disk_partitions()
        # partition = psutil.disk_usage('/')
        # print partition
        # print disk.count()
        # address = psutil.net_if_addrs().get("\xd2\xd4\xcc\xab\xcd\xf8")[1].__dict__.get("address", "")
        # for i in psutil.net_if_addrs().get("\xd2\xd4\xcc\xab\xcd\xf8"):
        #     print i.__dict__.get("address", "")
        # print address
