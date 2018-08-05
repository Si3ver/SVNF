#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# maxize minmum vertical scaling heuristic (MVSH)
import sys, os.path, argparse, re, math
import numpy as np
import fattree

DELMIN1 = '*'
DELIM 	= " "
NEWLINE = "\n"
DEMAND_FORMAT1 = r'(?P<src>[0-9]+)\s(?P<dst>[0-9]+)\s(?P<tr>[0-9]+\.[0-9]+)\s(?P<peak>[0-9]+\.[0-9]+)\s(?P<sfcLen>[0-9]+)\s(?P<sfc>\[([0-9]+, )*[0-9]+\])'
DEMAND_FORMAT2 = r'(?P<id>[0-9]+)\s(?P<src>[0-9]+)\s(?P<dst>[0-9]+)\s(?P<tr>[0-9]+\.[0-9]+)\s(?P<peak>[0-9]+\.[0-9]+)\s(?P<sfcLen>[0-9]+)\s(?P<sfc>\[([0-9]+, )*[0-9]+\])'
DEMAND_FORMAT = ''
placeResult = []

def BFS_hungary(graph):
    res=0
    rowLen, colLen = len(graph), len(graph[0])
    Q=[0]*10000
    prev=[0]*colLen
    Mx = [-1]*rowLen
    My = [-1]*colLen
    chk = [-1]*colLen
    for i in range(rowLen):
        if Mx[i]==-1:
            qs=qe=0
            Q[qe]=i
            qe+=1
            prev[i]=-1

            flag=0
            while(qs<qe and not flag):
                u=Q[qs]
                for v in range(colLen):
                    if flag:continue
                    if graph[u][v] and chk[v]!=i:
                        chk[v]=i
                        Q[qe]=My[v]
                        qe+=1
                        if My[v]>=0:
                            prev[My[v]]=u
                        else:
                            flag=1
                            d,e=u,v
                            while d!=-1:
                                t=Mx[d]
                                Mx[d]=e
                                My[e]=d
                                d=prev[d]
                                e=t
                qs+=1
            if Mx[i]!=-1:
                res+=1
    return Mx

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
            if M[i][j] >= 1:
                Mb.append((i,j, round(M[i][j]*100)/100) )
    Mb = sorted(Mb, key=lambda x:x[2], reverse=True)

    if dId == 2:
        print(dId, len(Mb), '-----', Mb)

    lo, hi = rowLen, rowLen * colLen
    while lo <= hi:
        mid = (hi + lo) // 2
        # if dId == 1:
        #     print('--->',mid)
        res = dohga(Mb[:mid], rowLen, colLen, dId)
        if sumBlowZero(res) > 0:
            lo = mid + 1
        else:
            hi = mid - 1
    
    if sumBlowZero(res) > 0:
        mid += 1
        res = dohga(Mb[:mid], rowLen, colLen, dId)
        if sumBlowZero(res) > 0:
            return []
    if sumEquaZero(res) > 1:
        mid += 1
        res = dohga(Mb[:mid], rowLen, colLen, dId)
        if sumEquaZero(res) > 1:
            return []
            
    # if dId == 1:
    #     print('+++++', res)
    #     for i in range(rowLen):
    #         Mc = list(map(lambda x: (round(x*100))/100, M[i]))
    #         print('------> i=', i,Mc)
    for i in range(rowLen):
        no = res[i]
        if M[i][no] < 1:
            res = []
            break
    if dId == 2:
        print(res)
    return res

def print_matrix(M):
    rowLen, colLen = len(M), len(M[0])
    for i in range(rowLen):
        for j in range(colLen):
            print('%2d' % M[i][j], end=' ')
        print()

def dohga(Mb, m, n, dId):
    graph = []
    for i in range(m):
        row = []
        for j in range(n):
            row.append(0)
        graph.append(row)
    
    for tup in Mb:
        i = tup[0]
        j = tup[1]
        graph[i][j] = 1
    # if dId == 2:
        # print('---graph---',len(Mb))
        # print_matrix(graph)
    res = BFS_hungary(graph)
    if dId == 2:
        print('@@@',res)
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
            LeftMips = topo.serverLeftMips(int(servNo))
            gamma_v = (LeftMips - mips) /  max(topo.getScaleOfServers(int(servNo)), mips*(exp-1))      
            row.append(gamma_v)
        Matrix.append(row)
    # if dId == 1:
    #     print(Matrix)

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
