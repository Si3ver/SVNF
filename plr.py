#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 测量丢包率 packet loss rate
import sys, os.path, argparse, re, math
import random
import fattree

DELIM 	= " "
NEWLINE = "\n"

# 记录放置结果
analysisResult = []

# 正则匹配
PLACE_FORMAT1 = r'(?P<src>[0-9]+)\s(?P<dst>[0-9]+)\s(?P<exp>[0-9]+\.[0-9]+)\s(?P<mipsList>\[([0-9]+, )*[0-9]*\])\s(?P<servNo>\[([0-9]+, )*[0-9]*\])'
PLACE_FORMAT2 = r'(?P<dId>[0-9]+)\s(?P<src>[0-9]+)\s(?P<dst>[0-9]+)\s(?P<exp>[0-9]+\.[0-9]+)\s(?P<mipsList>\[([0-9]+, )*[0-9]*\])\s(?P<servList>\[([0-9]+, )*[0-9]*\])'

PLACE_FORMAT = ''

def def_parser():
    parser = argparse.ArgumentParser(description='Analyzing Place Results!')
    parser.add_argument('-c', '--count', dest='c', help='How many service request', type=int, default=1000)
    parser.add_argument('-k', '--k-ray', dest='k', help='K parameter of K-ary fattree', type=int, required=True)
    parser.add_argument('-i', '--input', dest='i', help='place results file (default is output/result.txt)',
                        type=str, default='output/result.txt')
    parser.add_argument('-o', '--output', dest='o', help='analysis file name (default is output/analysis.txt)',
                        type=str, default='output/plr.txt')
    parser.add_argument('-n', '--no', dest='n', help='No id in request file',
                        action='store_true')
    parser.add_argument('-s', '--seed', dest='s', help='Random seed', type=int, default=10)
    return parser

def parse_args(parser):
    global PLACE_FORMAT
    opts = vars(parser.parse_args(sys.argv[1:]))
    if not os.path.isfile(opts['i']):
        raise Exception('Demands file \'%s\' does not exist!' % opts['i'])
    PLACE_FORMAT = PLACE_FORMAT1 if opts['n'] else PLACE_FORMAT2
    return opts

def parseResults(handle):
    content = handle.read()
    r = re.compile(PLACE_FORMAT)
    results = []
    for w in r.finditer(content):
        d = w.groupdict()
        [dId, src, dst, exp, mipsList, servList] = [int(d['dId']), int(d['src']), int(d['dst']), float(d['exp']), d['mipsList'][1:-1].split(','), d['servList'][1:-1].split(',')]
        mipsList = d['mipsList'][1:-1].split(',')
        mipsList = list(map(float, mipsList))
        # print(servList[0], type(servList[0]))
        if servList[0] != '':
            servList = list(map(int, servList))
        else:
            servList = []
        results.append([dId, src, dst, exp, mipsList, servList])
    return results

# 把result放入topo
def placeToTopo(results, topo):
    for result in results:
        [dId, _src, _dst, exp, mipsList, servList] = result
        for i in range(len(servList)):
            topo.deployToServ(dId, mipsList[i], exp, servList[i])

def write_to_file(handle, placeResult):
    for i in range(0, len(placeResult)):
        handle.write("%s%s" % (str(placeResult[i]), NEWLINE))

def main():
    args = parse_args(def_parser())
    random.seed(args['s'])
    with open(args['i']) as handle:
        results = parseResults(handle)
    topo = fattree.FatTree(args['k'])
    print('------1. before exp------')
    placeToTopo(results, topo)
    topo.display()

    print('------2. start exp------')
    expDemandList = list(range(args['c']))
    random.shuffle(expDemandList)
    # print(expDemandList)                              # 流放大顺序
    topo.expStressTest(expDemandList, results)
    
    # path = os.path.abspath(args['o'])
    # with open(path, 'w') as handle:
    #     write_to_file(handle, analysisResult)

if __name__ == "__main__":
    main()
