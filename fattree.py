#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os.path
import argparse
import math

class FatTree:
    def __init__(self, k):
        self.k = int(k)
        self.serverNoMin = int(5*k**2/4)                        # 服务器最小编号值
        self.serverNoMax = int(self.serverNoMin + k**3/4 - 1)   # 服务器最大编号值
        self.servers = [100000]*int(k**3/4)                     # 记录服务器剩余的mips值，共k**3/4台服务器
        self.demandsInServers = [[0]]*int(k**3/4)               # 记录服务器经过的demands id
        self.scaleOfServers = [0]*int(k**3/4)                   # 需要满足 任意一条流增大到exp，服务器能Vertical scaling!!!
        
    
    def display(self):
        usedServers = []
        # print(self.servers)
        for i in range(int(self.k**3/4)):
            if self.servers[i] < 100000:
                usedServers.append(i + self.serverNoMin)      
        print('used servers: %s' % str(usedServers))

    def getScaleOfServers(self, no):
        return self.scaleOfServers[no - self.serverNoMin]

    # def getdemand

    # 保证了纵向可扩展性VS
    def ifCanDeploy(self, mips, exp, no):
        leftMips = self.servers[no - self.serverNoMin]
        if leftMips > mips * exp and leftMips - mips > self.getScaleOfServers(no):      # 此条流能扩张 and 最大的已放置流能扩张
            return True
        return False

    # 评分
    def scoredServers(self, mips, exp, serversList):
        scores = {}
        for no in serversList.keys():
            if self.ifCanDeploy(mips, exp, int(no)) == False:
                scores[no] = -1
            else:
                leftMips = self.servers[int(no) - self.serverNoMin]
                scores[no] = (leftMips - max(mips * exp, self.getScaleOfServers(int(no))))
        return scores



    # 把vnf部署到服务器里，表现在消耗了对应服务器的mips
    def deployToServ(self, dId, mips, exp, no):
        self.servers[no - self.serverNoMin] -= mips
        self.demandsInServers[no - self.serverNoMin].append(dId)
        if mips*(exp-1) > self.scaleOfServers[no - self.serverNoMin]:
            self.scaleOfServers[no - self.serverNoMin] = mips*(exp-1)
        


    def getServersOfSameTor(self, no):
        [pod, tor, _host] = self.parsePos(no)
        start = self.calcServNo(pod, tor, 0)            # 服务器编号 -- 起点
        end = self.calcServNo(pod, tor, self.k//2-1)    # 服务器编号 -- 终点
        servList = {}
        for no in range(start, end+1):
            servList[str(no)] = self.servers[no - self.serverNoMin]
        return servList


    def getServersOfSamePod(self, no):
        [pod, tor, _host] = self.parsePos(no)
        start = self.calcServNo(pod, 0, 0)
        end = self.calcServNo(pod, self.k//2-1, self.k//2-1)
        servList = {}
        for no in range(start, end+1):
            servList[str(no)] = self.servers[no - self.serverNoMin]
        # 排除掉sameTor
        startOmit = self.calcServNo(pod, tor, 0)
        endOmit = self.calcServNo(pod, tor, self.k//2-1)
        for no in range(startOmit, endOmit+1):
            del servList[str(no)]
        return servList


    def getServersOfOtherPod(self, no1, no2):
        [pod1, _tor1, _host1] = self.parsePos(no1)
        [pod2, _tor2, _host2] = self.parsePos(no2)
        start = self.serverNoMin
        end = self.serverNoMax
        startOmit1 = self.calcServNo(pod1, 0, 0)
        startOmit2 = self.calcServNo(pod2, 0, 0)
        endOmit1 = self.calcServNo(pod1, self.k//2-1, self.k//2-1)
        endOmit2 = self.calcServNo(pod2, self.k//2-1, self.k//2-1)
        servList = {}
        for no in range(start, end+1):
            servList[str(no)] = self.servers[no - self.serverNoMin]
        for no in range(startOmit1, endOmit1):
            del servList[str(no)]
        for no in range(startOmit2, endOmit2):
            del servList[str(no)]
        return servList


    # 计算服务器编号值
    def calcServNo(self, pod, tor, host):
        if pod >= self.k:
            print("wrong pod number!")
            return
        if tor >= self.k//2:
            print("wrong tor number")
            return
        if host >= self.k//2:
            print("wrong server number")
            return
        return int(self.serverNoMin + pod * (self.k**2/4) + tor * self.k/2 + host)

    # 根据编号值no，解析位置
    def parsePos(self, no):
        if no < 0 or no > 5*self.k**2/4+self.k**3/4:
            print("server no is wrong!")
            return False
        elif no < self.k**2/4:
            print("server no is wrong!")
            return "corSW"
        elif no < 3*self.k**2/4:
            print("server no is wrong!")
            return "AggSW"
        elif no < 5*self.k**2/4:
            print("server no is wrong!")
            return "edgSW"
        else:
            nth = no - 5*self.k**2/4
            pod = nth // (self.k**2/4)
            tor = nth % (self.k**2/4) // (self.k/2)
            host = nth % (self.k**2/4) % (self.k/2)
            return [int(pod), int(tor), int(host)]

    # 计算两个节点的跳数
    def hops(self, no1, no2):
        res1 = self.parsePos(no1)
        res2 = self.parsePos(no2)
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
    def mips(self, sfc, tr):
        vnfSum = 60
        tauMin = 180
        tauMax = 220
        res = []
        for vnf in sfc:
            vnfTau = tauMin + (tauMax - tauMin)*(vnf/vnfSum)
            res.append(math.ceil(vnfTau * tr))
        return res

if __name__ == "__main__":
    # src = 1670
    # dst = 566
    # tr = 16.64
    # peak = 55.12
    # sfcLen = 4
    # sfc = [29, 52, 31, 17]
    # topo = FatTree(20)
    # print(topo.hops(src, dst))
    # print(topo.mips(sfc, tr))
    # print(topo.mips(sfc, peak))
    
    topo = FatTree(20)
    ser = topo.getServersOfSameTor(2160)
    
    print(ser)
    
    
    