#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os.path
import argparse
import re
from nvd3 import lineChart
import webbrowser
import fattree

DELIM 	= " "
NEWLINE = "\n"
k = 20

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

def generate(handle):
    content = handle.read()
    r = re.compile(DEMAND_FORMAT)
    [t1b, t1s, t2b, t2s, t3b, t3s, t4b, t4s] = [0]*8
    for w in r.finditer(content):
        d = w.groupdict()
        src = int(d['src'])
        dst = int(d['dst'])
        tr = float(d['tr'])
        peak = float(d['peak'])
        sfcLen = int(d['sfcLen'])
        sfc = d['sfc']
        # print(src, dst, tr, peak, sfcLen, sfc)
        hop = fattree.hops(k, src, dst)
        exp = peak/tr
        if  hop == 6:
            if exp > 2.5:
                t4b += 1
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
    print(t1b, t1s, t2b, t2s, t3b, t3s, t4b, t4s)
    return 0
def write_to_file(handle, workload):
    for i in range(0, len(workload)):
        handle.write("%d%s%d%s" % (i, DELIM, workload[i], NEWLINE))

def draw(handle, workload):
    x_data = range(0, len(workload))
    chart = lineChart(name="lineChart", width=1000, height=500)
    chart.add_serie(y=workload, x=x_data, name='Workload')
    chart.buildhtml()
    handle.write(str(chart))

def main():
    try:
        args = parse_args(def_parser())
        with open(args['i']) as handle:
            workload = generate(handle)
        # path = os.path.abspath(args['l'])
        # with open(path, 'w') as handle:
        #     write_to_file(handle, workload)
        # path = os.path.abspath(args['d'])
        # with open(path, 'w') as handle:
        #     draw(handle, workload)

        # uri = "file://" + path
        # webbrowser.open(uri, new=2)
    except argparse.ArgumentError:
        print(argparse)
    except Exception as exc:
        print(exc)

if __name__ == "__main__":
    main()