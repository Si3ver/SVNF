#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# maxize minmum vertical scaling heuristic (MVSH)
import sys, os.path, argparse, re, math
import numpy as np
import fattree
from collections import deque

class HungarianAlgorithm(object):
    def __init__(self,graph, m):
        self.graph=graph
        self.n=len(graph)
        self.m = m       
    def hungarian(self):
        match=[-1]*self.n#记录匹配情况
        used=[-1]*self.n#记录是否访问过
        Q=deque()  #设置队列
        prev=[0]*self.n  #代表上一节点
        for i in range(self.n): 
            if match[i]==-1:
                Q.clear()
                Q.append(i)
                prev[i]=-1#设i为出发点
                flag=False #未找到增广路
                while len(Q)>0 and not flag:
                    u=Q.popleft()
                    for j in range(self.n):
                        if not flag and self.graph[u][j]==1 and  used[j]!=i:
                            used[j]=i        
                            if match[j]!=-1:
                                Q.append(match[j])
                                prev[match[j]]=u#记录点的顺序
                            else:
                                flag=True
                                d=u
                                e=j
                                while(d!=-1):#将原匹配的边去掉加入原来不在匹配中的边
                                    t=match[d]
                                    match[d]=e
                                    match[e]=d
                                    d=prev[d]
                                    e=t
        return list(match[0:self.m])

DELMIN1 = '*'
DELIM 	= " "
NEWLINE = "\n"
DEMAND_FORMAT1 = r'(?P<src>[0-9]+)\s(?P<dst>[0-9]+)\s(?P<tr>[0-9]+\.[0-9]+)\s(?P<peak>[0-9]+\.[0-9]+)\s(?P<sfcLen>[0-9]+)\s(?P<sfc>\[([0-9]+, )*[0-9]+\])'
DEMAND_FORMAT2 = r'(?P<id>[0-9]+)\s(?P<src>[0-9]+)\s(?P<dst>[0-9]+)\s(?P<tr>[0-9]+\.[0-9]+)\s(?P<peak>[0-9]+\.[0-9]+)\s(?P<sfcLen>[0-9]+)\s(?P<sfc>\[([0-9]+, )*[0-9]+\])'
DEMAND_FORMAT = ''
placeResult = []

def def_parser():
    parser = argparse.ArgumentParser(description='sVNFP algorithm!')
    parser.add_argument('-k', '--k-ray', dest='k', help='K parameter of K-ary fattree', type=int, required=True)
    parser.add_argument('-i', '--input', dest='i', help='Demands file (default is output/traffic.txt)',
                        type=str, default='output/traffic.txt')
    parser.add_argument('-o', '--output', dest='o', help='place results file name (default is output/result_rndp.txt)',
                        type=str, default='output/result_rndp.txt')
    parser.add_argument('-n', '--no', dest='n', help='No id in request file',
                        action='store_true')
    return parser

def parse_args(parser):
    global DEMAND_FORMAT
    opts = vars(parser.parse_args(sys.argv[1:]))
    if not os.path.isfile(opts['i']):
        raise Exception('Demands file \'%s\' does not exist!' % opts['i'])
    DEMAND_FORMAT = DEMAND_FORMAT1 if opts['n'] else DEMAND_FORMAT2
    return opts

def mvsh(handle, topo):
    content = handle.read()
    r = re.compile(DEMAND_FORMAT)
    dId = -1
    for w in r.finditer(content):
        dId += 1
        d = w.groupdict()
        [src, dst, tr, peak, _sfcLen, sfc] = [int(d['src']), int(d['dst']), float(d['tr']), float(d['peak']), int(d['sfcLen']), d['sfc'][1:-1].split(', ')]
        sfc = list(map(int, sfc))
        # Demand变形为四元组dTrans
        exp = math.ceil(peak*100.0/tr)/100
        mipsList = topo.mips(sfc, tr)
        dTrans = [dId, src, dst, exp, mipsList]
        mvshPlaceDemand(dTrans, topo)
    topo.display()

def svnfp(M, dId):
    if len(M) > len(M[0]):
        return -1

    rowLen, colLen = len(M), len(M[0])
    Mb = []
    for i in range(rowLen):
        for j in range(colLen):
            Mb.append((i,j, round(M[i][j]*100)/100) )
    Mb = sorted(Mb, key=lambda x:x[2], reverse=True)

    lo, hi = rowLen, rowLen * colLen
    while lo <= hi:
        mid = (hi + lo) // 2
        res = dohga(Mb[:mid], rowLen, colLen)
        if sumBlowZero(res) > 0:
            lo = mid + 1
        else:
            hi = mid - 1
    if sumBlowZero(res) > 0:
        mid += 1
        res = dohga(Mb[:mid], rowLen, colLen)
        if sumBlowZero(res) > 0:
            return []
    if sumEquaZero(res) > 1:
        mid += 1
        res = dohga(Mb[:mid], rowLen, colLen)
        if sumEquaZero(res) > 1:
            return []

    # if dId == 42:
    #     print(res, rowLen)
    #     for i in range(rowLen):
    #         Mc = list(map(lambda x: (round(x*100))/100, M[i]))
    #         print('------> i=', i,Mc)
    for i in range(rowLen):
        no = res[i]
        if M[i][no] < 1:
            res = []
            break

    return res

def dohga(Mb, m, n):
    graph = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(0)
        graph.append(row)
    
    for tup in Mb:
        i = tup[0]
        j = tup[1]
        graph[i][j] = 1
    
    h = HungarianAlgorithm(graph, m)
    res = h.hungarian()
    return res

def sumBlowZero(arr):
    l = len(arr)
    cnt = 0
    for i in range(l):
        if arr[i] < 0:
            cnt += 1
    return cnt

def sumEquaZero(arr):
    l = len(arr)
    cnt = 0
    for i in range(l):
        if arr[i] == 0:
            cnt += 1
    return cnt

def mvshPlaceDemand(demand, topo):
    placeResultOfd = []
    [dId, src, dst, exp, mipsList] = demand
    mipsList_bak = mipsList[:]
    serversList = topo.getAllServers()
    serversNoList = list(serversList.keys())
    
    mipsListLen = len(mipsList)
    servListLen = len(serversNoList)
    
    Matrix = []
    for i in range(mipsListLen):
        mips = mipsList[i]
        row = []
        for j in range(servListLen):
            servNo = serversNoList[j]
            gamma_v = (topo.serverLeftMips(int(servNo))-mips) / max(topo.getScaleOfServers(int(servNo)), mips*(exp-1))        
            row.append(gamma_v)
        Matrix.append(row)
    
    placeResultOfd = svnfp(Matrix, dId)
    placeResultOfd = list(map(topo.transfertoNo, placeResultOfd))
    # print(dId, placeResultOfd)
    # if len(placeResultOfd) == 0:
        # print(dId)
    addtoResult(placeResultOfd, [dId, src, dst, exp, mipsList_bak], topo)


def addtoResult(resultOfd, demand, topo):
    global placeResult
    [dId, src, dst, exp, mipsList] = demand
    sfcLen = len(mipsList)
    placeResult.append(str(dId)+DELIM+str(src)+DELIM+str(dst)+DELIM+str(exp)+DELIM+str(mipsList)+DELIM+str(resultOfd))
    if sfcLen == len(resultOfd):
        for i in range(sfcLen):
            no = resultOfd[i]
            mips = mipsList[i]
            topo.deployToServ(dId, mips, exp, int(no))
    # if dId == 49:
    #     print(topo.servers)

def write_to_file(handle, placeResult):
    for i in range(0, len(placeResult)):
        handle.write("%s%s" % (str(placeResult[i]), NEWLINE))

def main():
    global placeResult
    args = parse_args(def_parser())
    topo = fattree.FatTree(args['k'])

    with open(args['i']) as handle:
        mvsh(handle, topo)
    
    path = os.path.abspath(args['o'])
    with open(path, 'w') as handle:
        write_to_file(handle, placeResult)

if __name__ == "__main__":
    main()
