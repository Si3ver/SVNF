#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 测量丢包率 packet loss rate
import sys, os.path, argparse, re, math
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
    parser.add_argument('-k', '--k-ray', dest='k', help='K parameter of K-ary fattree', type=int, required=True)
    parser.add_argument('-i', '--input', dest='i', help='place results file (default is output/result.txt)',
                        type=str, default='output/result.txt')
    parser.add_argument('-o', '--output', dest='o', help='analysis file name (default is output/analysis.txt)',
                        type=str, default='output/plr.txt')
    parser.add_argument('-n', '--no', dest='n', help='No id in request file',
                        action='store_true')
    return parser

def parse_args(parser):
    global PLACE_FORMAT
    opts = vars(parser.parse_args(sys.argv[1:]))
    if not os.path.isfile(opts['i']):
        raise Exception('Demands file \'%s\' does not exist!' % opts['i'])
    PLACE_FORMAT = PLACE_FORMAT1 if opts['n'] else PLACE_FORMAT2
    return opts

# 检查并统计流量
def placeToTopo(handle, topo):
    content = handle.read()
    r = re.compile(PLACE_FORMAT)
    for w in r.finditer(content):
        d = w.groupdict()
        [dId, _src, _dst, exp, mipsList, servList] = [int(d['dId']), int(d['src']), int(d['dst']), float(d['exp']), d['mipsList'][1:-1].split(','), d['servList'][1:-1].split(',')]
        mipsList = d['mipsList'][1:-1].split(',')
        mipsList = list(map(float, mipsList))
        servList = list(map(int, servList))
        for i in range(len(mipsList)):
            topo.deployToServ(dId, mipsList[i], exp, servList[i])
        pass
    return 0

def write_to_file(handle, placeResult):
    for i in range(0, len(placeResult)):
        handle.write("%s%s" % (str(placeResult[i]), NEWLINE))

def main():
    args = parse_args(def_parser())
    topo = fattree.FatTree(args['k'])
    with open(args['i']) as handle:
        placeToTopo(handle, topo)
    topo.display()
    
    # path = os.path.abspath(args['o'])
    # with open(path, 'w') as handle:
    #     write_to_file(handle, analysisResult)

if __name__ == "__main__":
    main()
