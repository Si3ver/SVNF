#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 根据放置结果，分析AR、FPL， analysis记录每条流的FPL。
import sys, os.path, argparse, re, math, pickle
import fattree

DELIM 	= " "
NEWLINE = "\n"

# 记录放置结果
analysisResult = []

# 正则匹配
PLACE_FORMAT1 = r'(?P<src>[0-9]+)\s(?P<dst>[0-9]+)\s(?P<exp>[0-9]+\.[0-9]+)\s(?P<MipsList>\[([0-9]+, )*[0-9]*\])\s(?P<servNo>\[([0-9]+, )*[0-9]*\])'
PLACE_FORMAT2 = r'(?P<dId>[0-9]+)\s(?P<src>[0-9]+)\s(?P<dst>[0-9]+)\s(?P<exp>[0-9]+\.[0-9]+)\s(?P<MipsList>\[([0-9]+, )*[0-9]*\])\s(?P<servNo>\[([0-9]+, )*[0-9]*\])'

PLACE_FORMAT = ''

def def_parser():
    parser = argparse.ArgumentParser(description='Analyzing Place Results!')
    parser.add_argument('-c', '--count', dest='c', help='How many service request', type=int, default=1000)
    parser.add_argument('-k', '--k-ray', dest='k', help='K parameter of K-ary fattree', type=int, required=True)
    parser.add_argument('-i', '--input', dest='i', help='place results file (default is output/result.txt)',
                        type=str, default='output/result.txt')
    parser.add_argument('-o', '--output', dest='o', help='analysis file name (default is output/analysis.txt)',
                        type=str, default='output/analysis.txt')
    parser.add_argument('-n', '--no', dest='n', help='No id in request file',
                        action='store_true')
    parser.add_argument('-a', '--algs', dest='a', help='used algs', type=str, default='svnf')
    parser.add_argument('-x', '--shiyan', dest='x', help='x-th shiyan', type=int, default=1)
    return parser

def parse_args(parser):
    global PLACE_FORMAT
    opts = vars(parser.parse_args(sys.argv[1:]))
    if not os.path.isfile(opts['i']):
        raise Exception('Demands file \'%s\' does not exist!' % opts['i'])
    PLACE_FORMAT = PLACE_FORMAT1 if opts['n'] else PLACE_FORMAT2
    return opts

# 检查并统计流量
def doAnalysis(handle, topo, cntDemands, alg, x):
    content = handle.read()
    r = re.compile(PLACE_FORMAT)
    [hopSum, sfcLenSum, hopSumSD, cntReject] = [0]*4
    hops = []
    for w in r.finditer(content):
        d = w.groupdict()
        dId = d['dId']
        servList = d['servNo']

        if servList == '[]':
            cntReject += 1
        else:
            servList = servList[1:-1].split(', ')
            servList.insert(0, d['src'])
            servList.append(d['dst'])
            servList = list(map(int, servList))
            hop = 0
            for i in range(len(servList)-1):
                hop += topo.hops(servList[i], servList[i+1])
            hopSum += hop/(len(servList)-1)                     # 每条流 除以 sfc长度
            hops.append(hop/(len(servList)-1))
            hopSumSD += topo.hops(int(d['src']), int(d['dst']))
            sfcLenSum += len(servList)-2
            analysisResult.append(str(dId) + DELIM + str(hop))
    dataPathHop = './pickle_cdf/'+ alg +'_hop' + x + '.dat'
    # print(hops)
    f = open(dataPathHop, 'wb')
    pickle.dump(hops, f)
    f.close()         
    print("reject demands=%d, AR=%.3f%%" % (cntReject, 100.0*(1-cntReject/cntDemands)))
    print("flow hops, SUM=%d, AVG FPL=%.3f" % (hopSum, hopSum/(cntDemands)))
    # print("sfcLen, SUM=%d, AVG=%.3f" % (sfcLenSum, sfcLenSum/(cntDemands)))
    # print("src->dst hops, SUM=%d, AVG FLP=%.3f" % (hopSumSD, hopSumSD/(cntDemands)))
    return 0

def write_to_file(handle, placeResult):
    for i in range(0, len(placeResult)):
        handle.write("%s%s" % (str(placeResult[i]), NEWLINE))

def main():
    args = parse_args(def_parser())
    topo = fattree.FatTree(args['k'])
    with open(args['i']) as handle:
        doAnalysis(handle, topo, args['c'], str(args['a']), str(args['x']))
    
    path = os.path.abspath(args['o'])
    with open(path, 'w') as handle:
        write_to_file(handle, analysisResult)

if __name__ == "__main__":
    main()
