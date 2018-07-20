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
    parser = argparse.ArgumentParser(description='random fit vnf placment algorithm!')
    parser.add_argument('-k', '--k-ray', dest='k', help='K parameter of K-ary fattree', type=int, required=True)
    parser.add_argument('-i', '--input', dest='i', help='Demands file (default is output/traffic.txt)',
                        type=str, default='output/traffic.txt')
    parser.add_argument('-o', '--output', dest='o', help='place results file name (default is output/result_rndp.txt)',
                        type=str, default='output/result_rndp.txt')
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

def rndp(handle, topo):
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
        # random place
        randomPlaceDemand(dTrans, topo)
        if dId > 0:
            break
    topo.display()

def randomPlaceDemand(demand, topo):
    placeResultOfd = []
    [dId, src, dst, exp, mipsList] = demand
    serversList = topo.getAllServers()
    
    while len(mipsList) > 0:
        if len(serversList) > 0:
            mips = mipsList.pop(0)
            no = chooseServ(mips, exp, serversList, topo)
            if no != False:
                placeResult.append(int(no))
                del serversList
            else:
                serversList = {}
                mipsList.insert(0, mips)
                break
    #place
    addtoResult(placeResultOfd, [dId, src, dst, exp, mipsList], topo)


def chooseServ(mips, exp, serversList, topo):
    ServersNoList = list(serversList.keys())
    # print(ServersNoList)
    while True:
        rndNo = random.choice(ServersNoList)
        if topo.ifCanDeploy(mips, exp, int(rndNo)):
            break
        elif len(serversList) <= 0:
            return False
        else:
            del serversList[rndNo]
    return rndNo
    


def addtoResult(resultOfd, demand, topo):
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
    args = parse_args(def_parser())
    random.seed(args['s'])
    topo = fattree.FatTree(args['k'])

    with open(args['i']) as handle:
        rndp(handle, topo)
    
    # path = os.path.abspath(args['o'])
    # with open(path, 'w') as handle:
    #     write_to_file(handle, placeResult)

if __name__ == "__main__":
    main()
