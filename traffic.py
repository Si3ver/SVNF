#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, random, math
import argparse
import numpy as np

DELIM   = " "
NEWLINE = "\n"

# 定义命令行参数格式
def def_parser():
    parser = argparse.ArgumentParser(description='Generating Service Requests(traffics、Demands)!')
    parser.add_argument('-c', '--count', dest='c', help='How many service request', type=int, default=1000)
    parser.add_argument('-k', '--k-ray', dest='k', help='K parameter of K-ary fattree', type=int, required=True)
    parser.add_argument('-Tm', '--Tmin', dest='Tm', help='Min traffic rate(Mbps)', type=float, required=True)
    parser.add_argument('-al', '--alpha', dest='al', help='Traffic Rate alpha(Mbps)', type=float, required=True)
    parser.add_argument('-o', '--output', dest='o', help='Output file name',type=str, default='traffic.txt')
    parser.add_argument('-s', '--seed', dest='s', help='Random seed', type=int, default=10)
    parser.add_argument('-x', '--shiyan', dest='x', help='x-th shiyan', type=int, default=1)
    return parser

# 参数解析
def parse_args(parser):
    opts   = vars(parser.parse_args(sys.argv[1:]))
    k      = opts['k']                              # k =   20
    opts['min'] = (5 * k ** 2) / 4                  # start 500
    opts['max'] = opts['min'] + (k ** 3) / 4 - 1    # end   2499
    return opts

def generateSFC():
    vnfSum = 60                         # 共有60个vnf
    sfcLen = random.randint(1, 10)      # SFC长度[1,5]
    vnfs = random.sample(range(vnfSum), sfcLen)
    return [sfcLen, vnfs]

def calcTrafficRate(Tm, alpha, x):
    while True:
        base = pow(Tm, alpha - 1) / (1 - random.random())
        exponent = 1 / (alpha - 1)
        tr = pow(base, exponent)
        if tr / Tm < 10:
            # 实验1
            if x == 1:
                peak = tr*(random.random()*1+1)                     # 随机扩大1～2倍
            # 实验2
            elif x == 2:
                peak = tr*(random.random()*3+1)                     # 随机扩大3～4倍
            # # 实验3
            elif x == 3:
                if random.randint(0,1) == 0:
                    peak = tr*(random.random()*1+1)                     # 随机扩大1～2倍
                else:
                    peak = tr*(random.random()*3+1)                     # 随机扩大1～2倍

            return [tr, peak]

def generateATraffic(args, file):
    global DELIM, NEWLINE
    x,y = int(args['min']), int(args['max'])
    src = random.randint(x, (3*x+y)//4)                    # 源
    dst = random.randint((x+3*y)//4, y)                    # 目的    
    # src = random.randint(args['min'], args['max'])          # 源
    # dst = random.randint(args['min'], args['max'])          # 目的
    [tr, peak] = calcTrafficRate(args['Tm'], args['al'], args['x'])
    [sfcLen, sfc] = generateSFC()
    file.write(str(src) + DELIM + str(dst) + DELIM + str(round(tr,2)) + DELIM + str(round(peak,2))+ DELIM + str(sfcLen) + DELIM + str(sfc))

def main():
    try:
        arguments = parse_args(def_parser())
        random.seed(arguments['s'])
        file = open(arguments['o'], 'w')
        for i in range(arguments['c']):
            generateATraffic(arguments, file)
            if i < arguments['c'] - 1:      # 去掉最后一行空行
                file.write(NEWLINE)
        file.close()
    except argparse.ArgumentError:
        print(argparse)

if __name__ == "__main__":
    main()
