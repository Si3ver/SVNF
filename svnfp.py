#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os.path, argparse, re, math
from nvd3 import lineChart
import webbrowser
import fattree

DELIM 	= " "
NEWLINE = "\n"

# 记录放置结果
placeResult = []

# 正则匹配一行，并解析各字段
# 不带id -n
DEMAND_FORMAT1 = r'(?P<src>[0-9]+)\s(?P<dst>[0-9]+)\s(?P<tr>[0-9]+\.[0-9]+)\s(?P<peak>[0-9]+\.[0-9]+)\s(?P<sfcLen>[0-9]+)\s(?P<sfc>\[([0-9]+, )*[0-9]+\])'
# 带id
DEMAND_FORMAT2 = r'(?P<id>[0-9]+)\s(?P<src>[0-9]+)\s(?P<dst>[0-9]+)\s(?P<tr>[0-9]+\.[0-9]+)\s(?P<peak>[0-9]+\.[0-9]+)\s(?P<sfcLen>[0-9]+)\s(?P<sfc>\[([0-9]+, )*[0-9]+\])'

DEMAND_FORMAT = ''

def def_parser():
    parser = argparse.ArgumentParser(description='scalable vnf placment algorithm!')
    parser.add_argument('-k', '--k-ray', dest='k', help='K parameter of K-ary fattree', type=int, required=True)
    parser.add_argument('-i', '--input', dest='i', help='Demands file (default is output/traffic.txt)',
                        type=str, default='output/traffic.txt')
    parser.add_argument('-o', '--output', dest='o', help='place results file name (default is output/result.txt)',
                        type=str, default='output/result.txt')
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

# 检查并统计流量
def doStatistics(handle, topo):
    content = handle.read()
    r = re.compile(DEMAND_FORMAT)
    [t1b, t1s, t2b, t2s, t3b, t3s, t4b, t4s] = [0]*8
    Lenlist = [0]*10
    for w in r.finditer(content):
        d = w.groupdict()
        src = int(d['src'])
        dst = int(d['dst'])
        tr = float(d['tr'])
        peak = float(d['peak'])
        sfcLen = int(d['sfcLen'])
        Lenlist[sfcLen-1] += 1        # 统计sfc长度
        # sfc = d['sfc']
        # print(src, dst, tr, peak, sfcLen, sfc)
        hop = topo.hops(src, dst)
        exp = peak/tr
        if  hop == 6:
            if exp > 2.5:
                t4b += 1            # 统计各类流量条数
            else:
                t4s += 1
        elif hop == 4:
            if exp > 2.5:
                t3b += 1
            else:
                t3s += 1
        elif hop == 2:
            if exp > 2.5:
                t2b += 1
            else:
                t2s += 1
        elif hop == 0:
            if exp > 2.5:
                t1b += 1
            else:
                t1s += 1
        else:
            print("find a error traffic!")
    print(r'六类流量分别为%d、%d、%d、%d、%d、%d、%d、%d条'%(t1s, t1b, t2s, t2b, t3s, t3b, t4s, t4b))
    print('sfc长度等于1~10的流量分别的条数为：', Lenlist)
    return 0

def svnfp(handle, topo):
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
        # 根据hop，分发流量到不同place函数
        hop = topo.hops(src, dst)
        if hop >= 6:
            placeDiffPodDemand(dTrans, topo)
        elif hop >= 4:
            placeSamePodDemand(dTrans, topo)
        elif hop >= 2:
            placeSameTorDemand(dTrans, topo)
        else:
            placeSameSerDemand(dTrans, topo)
    topo.display()

def chooseBestServ(mips, exp, serversList, topo):
    # print(mips, serversList)
    scores = topo.scoredServers(mips, exp, serversList)
    maxScore = -1
    maxNo = False
    for no, score in scores.items():
        if score > maxScore:
            maxScore = score
            maxNo = no
    return maxNo

def placeDiffPodDemand(demand, topo):
    placeResult1Ofd = []
    placeResult2Ofd = []
    [dId, src, dst, exp, mipsList] = demand
    mipsList_bak = mipsList[:]
    srcTorServersList = topo.getServersOfSameTor(src)
    dstTorServersList = topo.getServersOfSameTor(dst)
    # 1. first & last vnf of d
    # 首/尾能放到src/dst则放，因为可以是零跳
    if(len(mipsList) > 0):
        mips = mipsList.pop(0)
        if topo.ifCanDeploy(mips, exp, src):
            placeResult1Ofd.insert(0, src)
            del srcTorServersList[str(src)]
        else:
            mipsList.insert(0, mips)
    if(len(mipsList) > 0):
        mips = mipsList.pop(-1)
        if topo.ifCanDeploy(mips, exp, dst):
            placeResult2Ofd.append(dst)
            del dstTorServersList[str(dst)]
        else:
            mipsList.append(mips)
    # 2. sameTor
    while(len(mipsList) > 0):
        if len(srcTorServersList) == 0 and len(dstTorServersList) == 0:
            break
        if len(srcTorServersList) > 0:
            mips = mipsList.pop(0)
            no = chooseBestServ(mips, exp, srcTorServersList, topo)
            if no != False:
                placeResult1Ofd.append(int(no))
                del srcTorServersList[str(no)]
            else:
                srcTorServersList = []
                mipsList.insert(0, mips)
        if len(dstTorServersList) > 0 and len(mipsList) > 0:
            mips = mipsList.pop(-1)
            no = chooseBestServ(mips, exp, dstTorServersList, topo)
            if no != False:
                placeResult2Ofd.insert(0, int(no))
                del dstTorServersList[str(no)]
            else:
                dstTorServersList = []
                mipsList.append(mips)
    # 3. samePodOfsrc
    # print(placeResult1Ofd+placeResult2Ofd)
    srcPodServersList = topo.getServersOfSamePod(src,src)
    while(len(mipsList) > 0 and len(srcPodServersList) > 0):
        if len(srcPodServersList) > 0:
            mips = mipsList.pop(0)
            no = chooseBestServ(mips, exp, srcPodServersList, topo)
            if no != False:
                placeResult1Ofd.append(int(no))
                del srcPodServersList[str(no)]
            else:
                srcPodServersList = []
                mipsList.insert(0, mips)
                break
    # if dId == 112:
    #     print(placeResult1Ofd, placeResult2Ofd)
    # 4. samePodOfdst
    dstPodServersList = topo.getServersOfSamePod(dst,dst)
    while(len(mipsList) > 0 and len(dstPodServersList) > 0):
        if len(dstPodServersList) > 0:
            mips = mipsList.pop(0)
            no = chooseBestServ(mips, exp, dstPodServersList, topo)
            if no != False:
                placeResult1Ofd.append(int(no))
                del dstPodServersList[str(no)]
            else:
                dstPodServersList = []
                mipsList.insert(0, mips)
                break
    # if dId == 100:
    #     print(placeResult1Ofd, placeResult2Ofd)    
    # 5. otherPod
    otherServersList = topo.getServersOfOtherPod(src, dst)
    # if dId == 112:
    #     print(otherServersList)
    while(len(mipsList) > 0 and len(otherServersList) > 0):
        if len(otherServersList) > 0:
            mips = mipsList.pop(0)
            no = chooseBestServ(mips, exp, otherServersList, topo)
            if no != False:
                placeResult1Ofd.append(int(no))
                del otherServersList[str(no)]
            else:
                otherServersList = []
                mipsList.insert(0, mips)
                break
    # if dId == 112:
    #     print(placeResult1Ofd, placeResult2Ofd)  
    # place
    addtoResult(placeResult1Ofd + placeResult2Ofd, [dId, src, dst, exp, mipsList_bak], topo)

def placeSamePodDemand(demand, topo):
    placeResult1Ofd = []
    placeResult2Ofd = []
    [dId, src, dst, exp, mipsList] = demand
    mipsList_bak = mipsList[:]
    srcTorServersList = topo.getServersOfSameTor(src)
    dstTorServersList = topo.getServersOfSameTor(dst)
    # 1. first & last vnf of d
    # 首/尾能放到src/dst则放，因为可以是零跳
    if(len(mipsList) > 0):
        mips = mipsList.pop(0)
        if topo.ifCanDeploy(mips, exp, src):
            placeResult1Ofd.insert(0, src)
            del srcTorServersList[str(src)]
        else:
            mipsList.insert(0, mips)
    if(len(mipsList) > 0):
        mips = mipsList.pop(-1)
        if topo.ifCanDeploy(mips, exp, dst):
            placeResult2Ofd.append(dst)
            del dstTorServersList[str(dst)]
        else:
            mipsList.append(mips)
    # 2. sameTor
    while(len(mipsList) > 0):
        if len(srcTorServersList) == 0 and len(dstTorServersList) == 0:
            break
        if len(srcTorServersList) > 0:
            mips = mipsList.pop(0)
            no = chooseBestServ(mips, exp, srcTorServersList, topo)
            if no != False:
                placeResult1Ofd.append(int(no))
                del srcTorServersList[str(no)]
            else:
                srcTorServersList = []
                mipsList.insert(0, mips)
        if len(dstTorServersList) > 0 and len(mipsList) > 0:
            mips = mipsList.pop(-1)
            no = chooseBestServ(mips, exp, dstTorServersList, topo)
            if no != False:
                placeResult2Ofd.insert(0, int(no))
                del dstTorServersList[str(no)]
            else:
                dstTorServersList = []
                mipsList.append(mips)
    if dId == 100:
        print(placeResult1Ofd, placeResult2Ofd)
    # 3. samePod, choose same/Neighbor Tor!!!
    srcPodServersList = topo.getServersOfSamePod(src, dst)
    while(len(mipsList) > 0 and len(srcPodServersList) > 0):
        if len(srcPodServersList) > 0:
            mips = mipsList.pop(0)
            no = chooseBestServ(mips, exp, srcPodServersList, topo)
            if no != False:
                placeResult1Ofd.append(int(no))
                del srcPodServersList[str(no)]
            else:
                srcPodServersList = []
                mipsList.insert(0, mips)
                break
    # 4. otherPods 
    otherServersList = topo.getServersOfOtherPod(src, dst)  # 两个参数在同一个Pod
    while(len(mipsList) > 0 and len(otherServersList) > 0):
        if len(otherServersList) > 0:
            mips = mipsList.pop(0)
            no = chooseBestServ(mips, exp, otherServersList, topo)
            if no != False:
                placeResult1Ofd.append(int(no))
                del otherServersList[str(no)]
            else:
                otherServersList = []
                mipsList.insert(0, mips)
                break
    # place
    addtoResult(placeResult1Ofd + placeResult2Ofd, [dId, src, dst, exp, mipsList_bak], topo)

def placeSameTorDemand(demand, topo):
    placeResult1Ofd = []
    placeResult2Ofd = []
    [dId, src, dst, exp, mipsList] = demand
    mipsList_bak = mipsList[:]
    srcTorServersList = topo.getServersOfSameTor(src)
    # 1. first & last vnf of d
    # 首/尾能放到src/dst则放，因为可以是零跳
    if(len(mipsList) > 0):
        mips = mipsList.pop(0)
        if topo.ifCanDeploy(mips, exp, src):
            placeResult1Ofd.insert(0, src)
            del srcTorServersList[str(src)]
        else:
            mipsList.insert(0, mips)
    if(len(mipsList) > 0):
        mips = mipsList.pop(-1)
        if topo.ifCanDeploy(mips, exp, dst):
            placeResult2Ofd.append(dst)
            del srcTorServersList[str(dst)]
        else:
            mipsList.append(mips)
    # 2. sameTor
    while(len(mipsList) > 0):
        if len(srcTorServersList) == 0:
            break
        if len(srcTorServersList) > 0:
            mips = mipsList.pop(0)
            no = chooseBestServ(mips, exp, srcTorServersList, topo)
            if no != False:
                placeResult1Ofd.append(int(no))
                del srcTorServersList[str(no)]
            else:
                srcTorServersList = []
                mipsList.insert(0, mips)
        if len(srcTorServersList) > 0 and len(mipsList) > 0:
            mips = mipsList.pop(-1)
            no = chooseBestServ(mips, exp, srcTorServersList, topo)
            if no != False:
                placeResult2Ofd.insert(0, int(no))
                del srcTorServersList[str(no)]
            else:
                srcTorServersList = []
                mipsList.append(mips)    
    # 3. samePod otherTor 
    otherServersList = topo.getServersOfSamePod(src, src)  # 两个参数在同一个Pod
    while(len(mipsList) > 0 and len(otherServersList) > 0):
        if len(otherServersList) > 0:
            mips = mipsList.pop(0)
            no = chooseBestServ(mips, exp, otherServersList, topo)
            if no != False:
                placeResult1Ofd.append(int(no))
                del otherServersList[str(no)]
            else:
                otherServersList = []
                mipsList.insert(0, mips)
                break
    # 4. otherPod
    otherServersList = topo.getServersOfOtherPod(src, dst)  # 两个参数在同一个Pod
    while(len(mipsList) > 0 and len(otherServersList) > 0):
        if len(otherServersList) > 0:
            mips = mipsList.pop(0)
            no = chooseBestServ(mips, exp, otherServersList, topo)
            if no != False:
                placeResult1Ofd.append(int(no))
                del otherServersList[str(no)]
            else:
                otherServersList = []
                mipsList.insert(0, mips)
                break               
    # place
    addtoResult(placeResult1Ofd + placeResult2Ofd, [dId, src, dst, exp, mipsList_bak], topo)

def placeSameSerDemand(demand, topo):
    placeResult1Ofd = []
    placeResult2Ofd = []
    [dId, src, dst, exp, mipsList] = demand
    mipsList_bak = mipsList[:]
    srcTorServersList = topo.getServersOfSameTor(src)
    # 1. first & last vnf of d
    # 首/尾能放到src/dst则放，因为可以是零跳
    if(len(mipsList) > 0):
        mips = mipsList.pop(0)
        if topo.ifCanDeploy(mips, exp, src):
            placeResult1Ofd.insert(0, src)
            del srcTorServersList[str(src)]
        else:
            mipsList.insert(0, mips)
    # 2. sameTor otherServer
    while(len(mipsList) > 0):
        if len(srcTorServersList) == 0:
            break
        if len(srcTorServersList) > 0:
            mips = mipsList.pop(0)
            no = chooseBestServ(mips, exp, srcTorServersList, topo)
            if no != False:
                placeResult1Ofd.append(int(no))
                del srcTorServersList[str(no)]
            else:
                srcTorServersList = []
                mipsList.insert(0, mips)
        if len(srcTorServersList) > 0 and len(mipsList) > 0:
            mips = mipsList.pop(-1)
            no = chooseBestServ(mips, exp, srcTorServersList, topo)
            if no != False:
                placeResult2Ofd.insert(0, int(no))
                del srcTorServersList[str(no)]
            else:
                srcTorServersList = []
                mipsList.append(mips)
    # 3. samePod otherTor 
    otherServersList = topo.getServersOfSamePod(src, src)  # 两个参数在同一个Pod
    while(len(mipsList) > 0 and len(otherServersList) > 0):
        if len(otherServersList) > 0:
            mips = mipsList.pop(0)
            no = chooseBestServ(mips, exp, otherServersList, topo)
            if no != False:
                placeResult1Ofd.append(int(no))
                del otherServersList[str(no)]
            else:
                otherServersList = []
                mipsList.insert(0, mips)
                break
    # 4. otherPod
    otherServersList = topo.getServersOfOtherPod(src, dst)  # 两个参数在同一个Pod
    while(len(mipsList) > 0 and len(otherServersList) > 0):
        if len(otherServersList) > 0:
            mips = mipsList.pop(0)
            no = chooseBestServ(mips, exp, otherServersList, topo)
            if no != False:
                placeResult1Ofd.append(int(no))
                del otherServersList[str(no)]
            else:
                otherServersList = []
                mipsList.insert(0, mips)
                break 
    # place
    addtoResult(placeResult1Ofd + placeResult2Ofd, [dId, src, dst, exp, mipsList_bak], topo)

def addtoResult(resultOfd, demand, topo):
    [dId, src, dst, exp, mipsList] = demand
    # print(dId, resultOfd)
    sfcLen = len(mipsList)

    if sfcLen > len(resultOfd):
        resultOfd = []

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
    args = parse_args(def_parser())
    topo = fattree.FatTree(args['k'])
    with open(args['i']) as handle:
        doStatistics(handle, topo)
    with open(args['i']) as handle:
        svnfp(handle, topo)
    
    path = os.path.abspath(args['o'])
    with open(path, 'w') as handle:
        write_to_file(handle, placeResult)

if __name__ == "__main__":
    main()
