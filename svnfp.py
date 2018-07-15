#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os.path, argparse, re, math
from nvd3 import lineChart
import webbrowser
import fattree

DELIM 	= " "
NEWLINE = "\n"
k = 20

# 记录放置结果
placeResult = []

# 正则匹配一行，并解析各字段
# 不带id -n
DEMAND_FORMAT1 = r'(?P<src>[0-9]+)\s(?P<dst>[0-9]+)\s(?P<tr>[0-9]+\.[0-9]+)\s(?P<peak>[0-9]+\.[0-9]+)\s(?P<sfcLen>[0-9]+)\s(?P<sfc>\[([0-9]+, )*[0-9]+\])'
# 带id
DEMAND_FORMAT2 = r'(?P<id>[0-9]+)\s(?P<src>[0-9]+)\s(?P<dst>[0-9]+)\s(?P<tr>[0-9]+\.[0-9]+)\s(?P<peak>[0-9]+\.[0-9]+)\s(?P<sfcLen>[0-9]+)\s(?P<sfc>\[([0-9]+, )*[0-9]+\])'

DEMAND_FORMAT = ''

def def_parser():
    parser = argparse.ArgumentParser(description='Generating Service Requests!')
    parser.add_argument('-i', '--input', dest='i', help='Demands file (default is requests.txt)',
                        type=str, default='requests.txt')
    parser.add_argument('-l', '--log', dest='l', help='Log file name (default is log.txt)',
                        type=str, default='log.txt')
    parser.add_argument('-d', '--draw', dest='d', help='Draw file name (default is index.html)',
                        type=str, default='index.html')
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
            pass
            # placeSamePodDemand(dTrans, topo)
        elif hop >= 2:
            pass
            # placeSameTorDemand(dTrans, topo)
        else:
            pass
            # placeSameSerDemand(dTrans, topo)
        # topo.display()

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
    sfcLen = len(mipsList)
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
    srcPodServersList = topo.getServersOfSamePod(src)
    while(len(mipsList) > 0):
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
    # 4. samePodOfdst
    dstPodServersList = topo.getServersOfSamePod(dst)
    while(len(mipsList) > 0):
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
    # 5. otherPod
    otherServersList = topo.getServersOfOtherPod(src, dst)
    while(len(mipsList) > 0):
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
    # 6. 总放置结果
    placeResultOfd = placeResult1Ofd+placeResult2Ofd
    placeResult.append(str(dId)+DELIM+str(placeResultOfd))
    if sfcLen == len(placeResultOfd):
        for i in range(sfcLen):
            no = placeResultOfd[i]
            mips = mipsList_bak[i]
            topo.deployToServ(dId, mips, exp, int(no))
    
# 过滤服务器列表
def filterServList(mips, exp, servList):
    for item in list(servList):
        if servList[item] <= mips:  # or (servList[item] - mips)/SC < average[1/exp of vnf existed]:  请考虑增长因子！！！exp
            del servList[item]
    return servList

def write_to_file(handle, placeResult):
    for i in range(0, len(placeResult)):
        handle.write("%s%s" % (str(placeResult[i]), NEWLINE))

def draw(handle, workload):
    x_data = range(0, len(workload))
    chart = lineChart(name="lineChart", width=1000, height=500)
    chart.add_serie(y=workload, x=x_data, name='Workload')
    chart.buildhtml()
    handle.write(str(chart))


def main():
    # try:
        topo = fattree.FatTree(k)
        args = parse_args(def_parser())
        with open(args['i']) as handle:
            doStatistics(handle, topo)
        with open(args['i']) as handle:
            svnfp(handle, topo)
        
        path = os.path.abspath(args['l'])
        with open(path, 'w') as handle:
            write_to_file(handle, placeResult)
        # path = os.path.abspath(args['d'])
        # with open(path, 'w') as handle:
        #     draw(handle, workload)

        # uri = "file://" + path
        # webbrowser.open(uri, new=2)
    # except argparse.ArgumentError:
    #     print(argparse)
    # except Exception as exc:
    #     print(exc)

if __name__ == "__main__":
    main()
