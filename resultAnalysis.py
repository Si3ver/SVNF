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
analysisResult = []

# 正则匹配一行，并解析各字段
# 不带id -n
DEMAND_FORMAT1 = r'(?P<servNo>\[([0-9]+, )*[0-9]*\])'
# 带id
DEMAND_FORMAT2 = r'(?P<dId>[0-9]+)\s(?P<servNo>\[([0-9]+, )*[0-9]*\])'

DEMAND_FORMAT = ''

def def_parser():
    parser = argparse.ArgumentParser(description='Analyzing Place Results!')
    parser.add_argument('-i', '--input', dest='i', help='place results file (default is requests.txt)',
                        type=str, default='requests.txt')
    parser.add_argument('-l', '--log', dest='l', help='Log file name (default is log.txt)',
                        type=str, default='analysis.txt')
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
def doAnalysis(handle):
    hopSum = 0
    topo = fattree.FatTree(k)
    content = handle.read()
    r = re.compile(DEMAND_FORMAT)
    cntReject = 0
    for w in r.finditer(content):
        d = w.groupdict()
        dId = d['dId']
        servList = d['servNo']
        if len(servList) > 2:
            servList = servList[1:-1].split(', ')
            servList = list(map(int, servList))
        else:
            servList = []
        if len(servList) == 0:
            cntReject += 1
        else:
            hop = 0
            for i in range(len(servList)-1):
                hop += topo.hops(servList[i], servList[i+1])
            hopSum += hop
            analysisResult.append(str(dId) + DELIM + str(hop))
    print(hopSum, hopSum/(1000-41))

    print(cntReject)
    return 0

def write_to_file(handle, placeResult):
    for i in range(0, len(placeResult)):
        handle.write("%s%s" % (str(placeResult[i]), NEWLINE))

def main():
    args = parse_args(def_parser())
    with open(args['i']) as handle:
        doAnalysis(handle)
    
    path = os.path.abspath(args['l'])
    with open(path, 'w') as handle:
        write_to_file(handle, analysisResult)

if __name__ == "__main__":
    main()
