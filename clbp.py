#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os.path, argparse, re, math, random
import fattree

DELIM 	= " "
NEWLINE = "\n"
DEMAND_FORMAT1 = r'(?P<src>[0-9]+)\s(?P<dst>[0-9]+)\s(?P<tr>[0-9]+\.[0-9]+)\s(?P<peak>[0-9]+\.[0-9]+)\s(?P<sfcLen>[0-9]+)\s(?P<sfc>\[([0-9]+, )*[0-9]+\])'
DEMAND_FORMAT2 = r'(?P<id>[0-9]+)\s(?P<src>[0-9]+)\s(?P<dst>[0-9]+)\s(?P<tr>[0-9]+\.[0-9]+)\s(?P<peak>[0-9]+\.[0-9]+)\s(?P<sfcLen>[0-9]+)\s(?P<sfc>\[([0-9]+, )*[0-9]+\])'
DEMAND_FORMAT = ''
placeResult = []

def def_parser():
    parser = argparse.ArgumentParser(description='cluster based placment algorithm!')
    parser.add_argument('-k', '--k-ray', dest='k', help='K parameter of K-ary fattree', type=int, required=True)
    parser.add_argument('-i', '--input', dest='i', help='Demands file (default is output/traffic.txt)',
                        type=str, default='output/traffic.txt')
    parser.add_argument('-o', '--output', dest='o', help='place results file name (default is output/result_clbp.txt)',
                        type=str, default='output/result_clbp.txt')
    parser.add_argument('-s', '--seed', dest='s', help='Random seed', type=int, default=20)
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

def clbp(handle, topo):
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
        # cluster based place
        clbPlaceDemand(dTrans, topo)
    topo.display()

def clbPlaceDemand(demand, topo):
    placeResultOfd = []
    [dId, src, dst, exp, mipsList] = demand
    mipsList_bak = mipsList[:]
    
    # 1. sameServer
    while len(mipsList) > 0:
        mips = mipsList.pop(0)
        if topo.ifCanDeploy(mips, exp, src):
            placeResultOfd.append(src)
            topo.useMips(mips, src)
        else:
            mipsList.insert(0, mips)
            break
    # 2. sameTor
    serversList = topo.getServersOfSameTor(src)
    serversNoList = list(map(int, serversList.keys()))
    while len(mipsList) > 0 and len(serversList) > 0:
        mips = mipsList.pop(0) 
        while len(serversNoList) > 0:
            no = serversNoList.pop(0)
            if topo.ifCanDeploy(mips, exp, no):
                placeResultOfd.append(no)
                topo.useMips(mips, no)
                serversNoList.insert(0, no)
                break
            if len(serversNoList) == 0:   # 没有合适的server，mips放回
                mipsList.insert(0, mips)

    # 3. samePod
    serversList = topo.getServersOfSamePod(src)
    serversNoList = list(map(int, serversList.keys()))
    while len(mipsList) > 0 and len(serversList) > 0:
        mips = mipsList.pop(0) 
        while len(serversNoList) > 0:
            no = serversNoList.pop(0)
            if topo.ifCanDeploy(mips, exp, no):
                placeResultOfd.append(no)
                topo.useMips(mips, no)
                serversNoList.insert(0, no)
                break
            if len(serversNoList) == 0:   # 没有合适的server，mips放回
                mipsList.insert(0, mips)
    
    # 4. otherPod
    serversList = topo.getServersOfOtherPod(src, src)
    serversNoList = list(map(int, serversList.keys()))
    while len(mipsList) > 0 and len(serversList) > 0:
        mips = mipsList.pop(0) 
        while len(serversNoList) > 0:
            no = serversNoList.pop(0)
            if topo.ifCanDeploy(mips, exp, no):
                placeResultOfd.append(no)
                topo.useMips(mips, no)
                serversNoList.insert(0, no)
                break
            if len(serversNoList) == 0:   # 没有合适的server，mips放回
                mipsList.insert(0, mips)
    # give back mips simulate
    sfcLen = len(mipsList_bak)
    topo.givebackMips(mipsList_bak, placeResultOfd)
    if len(placeResultOfd) < sfcLen:
        placeResultOfd = []
    #place
    # print(dId, placeResultOfd)
    addtoResult(placeResultOfd, [dId, src, dst, exp, mipsList_bak], topo)


def chooseServ(mips, exp, serversList, topo):
    rndNo = False
    while len(serversList) > 0:
        ServersNoList = list(serversList.keys())
        rndNo = random.choice(ServersNoList)
        if topo.ifCanDeploy(mips, exp, int(rndNo)): # can deploy!
            return rndNo
        elif len(serversList) <= 0:                 # no servers
            return False
        else:                                       # continue
            del serversList[rndNo]
    return False
    

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
    random.seed(args['s'])
    topo = fattree.FatTree(args['k'])

    with open(args['i']) as handle:
        clbp(handle, topo)
    
    path = os.path.abspath(args['o'])
    with open(path, 'w') as handle:
        write_to_file(handle, placeResult)

if __name__ == "__main__":
    main()
