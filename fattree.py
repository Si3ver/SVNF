#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os.path, math
import argparse

class FatTree:
    def __init__(self, k):
        self.serverCapacity = 100000                                # 一台服务器默认 100000mips 计算能力
        self.k = int(k)
        self.cntServers = int(k**3/4)
        self.serverNoMin = int(5*k**2/4)                            # 服务器最小编号值
        self.serverNoMax = self.serverNoMin + self.cntServers - 1   # 服务器最大编号值
        self.servers = [self.serverCapacity]*self.cntServers        # 记录服务器剩余的mips值，共k**3/4台服务器
        self.demandsInServers = [[]]*self.cntServers                # 记录服务器经过的demands id
        self.scaleOfServers = [0]*self.cntServers                   # 需要满足 任意一条流增大到exp，服务器能Vertical scaling!!!
        self.plrServerList = {}                                     # 记录丢包的服务器 key:serNo value:plr
        
        self.peakSum = [0]*self.cntServers                          # 总共已放入的peak值之和
    
    def display(self):
        [usedServersCnt, SU] = self.calcSU()     
        print('used servers=%d, AVG SU=%.3f%%' % (usedServersCnt, SU*100.0))

    
    def serverLeftMips(self, no):
        return self.servers[no-self.serverNoMin]

    def calcSU(self):
        # 所有开启的服务器，其平均资源利用率
        [sumUsedMips, cnt] = [0]*2
        for serv in self.servers:
            if serv < 0:
                sumUsedMips += self.serverCapacity
                cnt += 1
            elif serv < self.serverCapacity:
                sumUsedMips += self.serverCapacity - serv
                cnt += 1
        servUtility = sumUsedMips/(self.serverCapacity*cnt) if cnt != 0 else 0
        return [cnt, servUtility]

    
    def calcplr(self):
        cnt = 0
        sumPlr = 0.0
        for _servNo, plr in self.plrServerList.items():
            sumPlr += plr
            cnt += 1
        if cnt == 0:
            return [0, 0, 0]
        return [cnt, sumPlr/cnt, sumPlr/self.cntServers]


    def transfertoNo(self, idx):
        return idx + self.serverNoMin


    def expStressTest(self, demandList, results):
        percentPlrList = []
        plr1List = []
        plr2List = []
        SUList = []

        for dId in demandList:
            # print(dId, len(results))
            result = results[dId]
            self.expDemand(result)
            # self.display()
            [cntPlrServ, plr1, plr2] = self.calcplr()
            # print('sum plrServers=%d, plr1=%.3f%%, plr2=%.3f%%' % (cntPlrServ, plr1*100.0, plr2*100.0))
            [_usedServersCnt, SU] = self.calcSU()
            SUList.append(SU)
            percentPlrList.append(cntPlrServ/len(self.servers))
            plr1List.append(plr1)
            plr2List.append(plr2)
        return [percentPlrList, plr1List, plr2List, SUList]


    def expDemand(self, result):
        [_dId, _src, _dst, _exp, mipsList, servList] = result
        for i in range(len(servList)):
            mips = mipsList[i]
            servNo = servList[i]
            self.servers[servNo - self.serverNoMin] -= mips
            
            # 检测是否丢包
            if self.servers[servNo - self.serverNoMin] < 0:
                self.plrServerList[servNo] = (0 - self.servers[servNo - self.serverNoMin])/(self.serverCapacity-self.servers[servNo - self.serverNoMin])


    def getScaleOfServers(self, no):
        return self.scaleOfServers[no - self.serverNoMin]


    # 保证了纵向可扩展性VS
    def ifCanDeploy(self, mips, exp, no):
        leftMips = self.servers[no - self.serverNoMin]
        if leftMips > mips * exp and leftMips - mips > self.getScaleOfServers(no):      # 此条流能扩张 and 最大的已放置流能扩张
            return True
        return False


    # 所有流量都扩张，还能放下
    def ifCanCompleteDeploy(self, mips, exp, no):
        leftMips = self.servers[no - self.serverNoMin]
        if leftMips > mips * exp + self.peakSum[no-self.serverNoMin]:
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

    def useMips(self, mips, no):
        self.servers[no-self.serverNoMin] -= mips


    def givebackMips(self, mipsList, servList):
        for i in range(len(servList)):
            no = servList[i]
            mips = mipsList[i]
            self.servers[no-self.serverNoMin] += mips


    # 把vnf部署到服务器里，表现在消耗了对应服务器的mips
    def deployToServ(self, dId, mips, exp, no):
        self.servers[no - self.serverNoMin] -= mips
        self.demandsInServers[no - self.serverNoMin].append(dId)
        if mips*(exp-1) > self.scaleOfServers[no - self.serverNoMin]:
            self.scaleOfServers[no - self.serverNoMin] = mips*(exp-1)
        self.peakSum[no-self.serverNoMin] += mips*(exp-1)

    def getAllServers(self):
        servList = {}
        start = self.serverNoMin
        end = self.serverNoMax
        for no in range(start, end+1):
            servList[str(no)] = self.servers[no - self.serverNoMin]
        return servList


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
        if startOmit1 != startOmit2:
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
        if no < 0 or no > self.serverNoMax:
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
    topo = FatTree(20)
    ser = topo.getServersOfSameTor(2160) 
    