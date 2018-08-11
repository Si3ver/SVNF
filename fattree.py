#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os.path, math
import argparse
import pickle

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
        sumUsedMips, cnt = 0,0
        for serv in self.servers:
            if serv < 0:                        # overload servers
                sumUsedMips += self.serverCapacity
                cnt += 1
            elif serv < self.serverCapacity:    # unoverload servers
                sumUsedMips += self.serverCapacity - serv
                cnt += 1
        servUtility = sumUsedMips/(self.serverCapacity*cnt) if cnt != 0 else 0
        return [cnt, servUtility]

    def currentSU(self):
        res = []
        for serv in self.servers:
            if serv < 0:
                res.append(1)
            else:
                res.append(1.0 - serv/self.serverCapacity)
        return res

    def currentPlr(self):
        res = []
        for serv in self.servers:
            if serv < 0:
                res.append( (0 - serv) / (self.serverCapacity - serv))
            else:
                res.append( 0 )
        return res

    def currentSor(self):
        res = []
        for serv in self.servers:
            if serv < 0:
                res.append(1)
            else:
                res.append(0)
        return res

    def calcplr(self):
        # cnt, sump = 0, 0.0
        # for i in range(len(self.servers)):
        #     if self.servers[i] < 0:
        #         cnt += 1
        #         sump -= self.servers[i]
        # if cnt == 0:
        #     return [0, 0, 0]
        # return [cnt, sump/(self.serverCapacity * cnt), sump/(self.serverCapacity * self.cntServers)]
        # cnt = 0
        # sumPlr = 0.0
        # for _servNo, plr in self.plrServerList.items():
        #     sumPlr += plr
        #     cnt += 1
        # if cnt == 0:
        #     return [0, 0, 0]
        return [0, 0, self.calcAvgPlrNew()]


    def transfertoNo(self, idx):
        return idx + self.serverNoMin

    # def calcAvgPlr(self):
    #     # plrList = self.currentPlr()
    #     # return sum(plrList)/len(plrList)
    #     sumpl, cnt = 0, 0
    #     for serv in self.servers:
    #         if serv < 0:
    #             sumpl -= serv
    #             cnt += 1
    #     sumProcessed = 0
    #     for serv in self.servers:
    #         if serv > 0:
    #             sumProcessed += self.serverCapacity - serv
    #         else:
    #             sumProcessed -= serv
    #     return sumpl / sumProcessed
    
    def calcAvgPlrNew(self):
        # plrList = self.currentPlr()
        # return sum(plrList)/len(plrList)
        sumAcc, sumProc, _cnt = 0, 0, 0
        for serv in self.servers:
            if serv < 0:
                sumAcc -= serv
                sumAcc += self.serverCapacity
                sumProc += self.serverCapacity
            if serv >= 0:
                sumAcc += self.serverCapacity - serv
                sumProc += self.serverCapacity - serv
        # print(sumAcc, sumProc)
        return 1- (sumProc / sumAcc)


    def calcAvgSor(self):
        # sorList = self.currentSor()
        # return sum(sorList)/len(sorList)
        cnt = 0
        for serv in self.servers:
            if serv < 0:
                cnt += 1
        return cnt/self.cntServers
    
    def calcAvgSu(self):
        # suList = self.currentSU()
        # return sum(suList)/len(suList)
        usedMips, cnt = 0,0
        for serv in self.servers:
            if serv < 0:
                usedMips += self.serverCapacity
                cnt += 1
            elif serv < self.serverCapacity:
                usedMips += (self.serverCapacity - serv)
                cnt += 1
        return usedMips / (cnt * self.serverCapacity)

    def test(self):
        # print(self.servers)
        su = self.currentSU()
        # for x in su:
        #     if x >= 1:
        #         s += 1
        return su, sum(su)/len(su)

    def expStressTest(self, demandList, results, x, alg):
        percentPlrList = []
        plr1List = []
        plr2List = []
        SUList = []
        for dId in demandList:
            # print(dId, len(results))
            result = results[dId]
            # print('place+++++', dId, result)
            self.expDemand(result)
            # self.display_expServs()
            # self.display()
            # [_cntPlrServ, plr1, plr2] = self.calcplr()
            # print(cntPlrServ, plr1, plr2)
            # print('sum plrServers=%d, plr1=%.3f%%, plr2=%.3f%%' % (cntPlrServ, plr1*100.0, plr2*100.0))
            # [_usedServersCnt, SU] = self.calcSU()
            # su
            SUList.append(self.calcAvgSu())
            # sor
            percentPlrList.append(self.calcAvgSor())
            #plr
            plr1List.append(0)
            plr2List.append(self.calcAvgPlrNew())
            # if dId == demandList[-1]:
            #     print(len(SUList))
            #     print(len(percentPlrList))
            #     print(len(plr2List))

            # if demandList.index(dId) / len(demandList) == 0.5:
                # print(self.test())
                
            suList = None
            percent = [0.2]
            for i in range(len(percent)):
                if demandList.index(dId) / len(demandList) == percent[i]:
                    suList = self.currentSU()
                    datPath = './pickle_cdf/'+ alg +'_su'+ str(percent[i]) + '-' + x + '.dat'
                    plrList = self.currentPlr()
                    datPathPlr = './pickle_cdf/'+ alg +'_plr'+ str(percent[i]) + '-' + x + '.dat'
                    sorList = self.currentSor()
                    dataPathSor = './pickle_cdf/'+ alg +'_sor'+ str(percent[i]) + '-' + x + '.dat'
            if suList != None:
                f = open(datPath, 'wb')
                pickle.dump(suList, f)
                f.close() 
                f2 = open(datPathPlr, 'wb')
                pickle.dump(plrList, f2)
                f2.close()  
                f3 = open(dataPathSor, 'wb')
                pickle.dump(sorList, f3)
                f3.close()
            
            # x变化时。输出参数变化
            if demandList.index(dId) / len(demandList) == 0.2:
                print('@@@@@ plr=%.3f' % self.calcAvgPlrNew())
                # print(self.currentPlr())
                print('@@@@@ sor=%.3f' % self.calcAvgSor())
                # print('%.3f,' % self.calcAvgSor(), end=' ')
                print('@@@@@ su =%.3f' % self.calcAvgSu())
            # if demandList.index(dId) == 149:
                # print('%d, plr %.3f'%(dId, self.calcAvgPlrNew()))
                print(len(demandList))
        print()

        
        # print(self.servers)
        return [percentPlrList, plr1List, plr2List, SUList]


    def display_expServs(self):
        print(' ###### ')
        for i in range(self.cntServers):
            if self.servers[i] < 0:
                print('%d:%.2f'%(self.transfertoNo(i),self.plrServerList[self.transfertoNo(i)]), end=' ')
        print()


    def expDemand(self, result):
        [_dId, _src, _dst, exp, mipsList, servList] = result
        for i in range(len(servList)):
            mips = mipsList[i]
            servNo = servList[i]
            self.servers[servNo - self.serverNoMin] -= mips*(exp-1)
            
            # 检测是否丢包
            if self.servers[servNo - self.serverNoMin] < 0:
                # 一台服务器的丢包率 = 溢出的 - 总收到的
                self.plrServerList[servNo] = (0 - self.servers[servNo - self.serverNoMin])/(self.serverCapacity-self.servers[servNo - self.serverNoMin])


    def getScaleOfServers(self, no):
        return self.scaleOfServers[no - self.serverNoMin]


    # 保证了纵向可扩展性VS
    def ifCanDeploy(self, mips, exp, no):
        leftMips = self.servers[no - self.serverNoMin]
        if leftMips > mips * exp and leftMips - mips > self.getScaleOfServers(no):      # 此条流能扩张 and 最大的已放置流能扩张
            return True
        return False

    # 
    def ifCanDeployCLBP(self, mips, exp, no):
        leftMips = self.servers[no - self.serverNoMin]
        if leftMips > mips:
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


    def getServersOfSamePod(self, no1, no2):
        [pod1, tor1, _host] = self.parsePos(no1)
        [pod2, tor2, _host] = self.parsePos(no2)
        if pod1 != pod2:
            return False
        start = self.calcServNo(pod1, 0, 0)
        end = self.calcServNo(pod1, self.k//2-1, self.k//2-1)
        servList = {}
        for no in range(start, end+1):
            servList[str(no)] = self.servers[no - self.serverNoMin]
        # 排除掉sameTor
        startOmit1 = self.calcServNo(pod1, tor1, 0)
        endOmit1 = self.calcServNo(pod1, tor1, self.k//2-1)
        startOmit2 = self.calcServNo(pod2, tor2, 0)
        endOmit2 = self.calcServNo(pod2, tor2, self.k//2-1)
        for no in range(startOmit1, endOmit1+1):
            del servList[str(no)]
        if startOmit1 != startOmit2:
            for no in range(startOmit2, endOmit2+1):
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
        for no in range(startOmit1, endOmit1+1):
            del servList[str(no)]
        if startOmit1 != startOmit2:
            for no in range(startOmit2, endOmit2+1):
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
        tauMin = 200
        tauMax = 205
        res = []
        for vnf in sfc:
            vnfTau = tauMin + (tauMax - tauMin)*(vnf/vnfSum)
            res.append(math.ceil(vnfTau * tr))
        return res


if __name__ == "__main__":    
    topo = FatTree(20)
    ser = topo.getServersOfSameTor(2160) 
    