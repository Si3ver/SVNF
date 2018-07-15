#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os.path
import argparse
import math

class FatTree:
    def __init__(self, k):
        self.k = k
        # 初始化k*k/4台核心交换机
        self.serverNoMin = 5*k**2/4
        self.serverNoMax = self.serverNoMin + k**3/4 - 1
        print(self.serverNoMin, self.serverNoMin)
    def display(self):
        pass


# 根据编号值no，解析位置
def parsePos(k, no):
    if no < 0 or no > 5*k**2/4+k**3/4:
        return False
    elif no < k**2/4:
        return "corSW"
    elif no < 3*k**2/4:
        return "AggSW"
    elif no < 5*k**2/4:
        return "edgSW"
    else:
        nth = no - 5*k**2/4
        pod = nth // (k**2/4)
        tor = nth % (k**2/4) // (k/2)
        host = nth % (k**2/4) % (k/2)
        return [int(pod), int(tor), int(host)]

# 计算两个节点的跳数
def hops(k, no1, no2):
    res1 = parsePos(k, no1)
    res2 = parsePos(k, no2)
    if(isinstance(res1, list) and isinstance(res2, list)):
        if res1[0] != res2[0]:
            hop = 6
        elif  res1[1] != res2[1]:
            hop = 4
        elif res1[2] != res2[2]:
            hop = 2
        else:
            hop = 0
        return hop
    else:
        return False

# 对于一个VNF来说，mips = tau*tr，tau仅仅与VNF类型有关。假定其在180～220之间均匀分布。
def mips(sfc, tr):
    vnfSum = 60
    tauMin = 180
    tauMax = 220
    res = []
    for vnf in sfc:
        vnfTau = tauMin + (tauMax - tauMin)*(vnf/vnfSum)
        res.append(math.ceil(vnfTau * tr))
    return res

if __name__ == "__main__":
    src = 1670
    dst = 566
    tr = 16.64
    peak = 55.12
    sfcLen = 4
    sfc = [29, 52, 31, 17]
    print(hops(20, src, dst))
    print(mips(sfc, tr))
    print(mips(sfc, peak))
    