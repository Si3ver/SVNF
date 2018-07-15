#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, random, math
import argparse
import numpy as np

DELIM   = " "
NEWLINE = "\n"

# 解释命令行参数
def def_parser():
    parser = argparse.ArgumentParser(description='Generating Service Requests!')
    parser.add_argument('-c', '--count'   , dest='c', help='How many service request', type=int, default=1000)              # 产生的流条数 | D |
    parser.add_argument('-k', '--kparam'  , dest='k', help='K parameter of K-ary fattree', type=int  , required=True)           # 胖树k值，影响服务器数量和编号
    parser.add_argument('-Tm', '--Tmin' , dest='Tm', help='Min traffic rate(Mbps)', type=float, required=True)           # 流速率最小值
    parser.add_argument('-al', '--alpha' , dest='al', help='Traffic Rate alpha(Mbps)', type=float, required=True)           # 流速率浮动因子
    parser.add_argument('-o', '--output'  , dest='o', help='Output file name',type=str, default='traffic.txt')              # 输出文件名
    parser.add_argument('-s', '--seed'    , dest='s', help='Random seed', type=int, default=10)                         # 初始种子
    return parser

# 参数解析
def parse_args(parser):
    opts = vars(parser.parse_args(sys.argv[1:]))
    k      = opts['k']                              # k =   20
    opts['min'] = (5 * k ** 2) / 4                  # start 500
    opts['max'] = opts['min'] + (k ** 3) / 4 - 1    # end   2499
    return opts

def generateSFC():
    vnfSum = 60                         # 共有60个vnf
    sfcLen = random.randint(1, 10)      # SFC长度[1,5]
    vnfs = random.sample(range(vnfSum), sfcLen)
    return [sfcLen, vnfs]

def generate(args, file):
    global DELIM, NEWLINE
    # print(args)
    src = random.randint(args['min'], args['max'])      # 源
    dst = random.randint(args['min'], args['max'])      # 目的
    # 计算流速率tr
    base = pow(args['Tm'], args['al'] - 1) / (1 - random.random())
    exponent = 1 / (args['al'] - 1)
    tr = pow(base, exponent)
    peak = tr*(random.random()*4+1)                   # 随机扩大1～5倍
    # 生成一条SFC
    [sfcLen, sfc] = generateSFC()
    file.write(str(src) + DELIM + str(dst) + DELIM + str(round(tr,2)) + DELIM + str(round(peak,2))+ DELIM + str(sfcLen) + DELIM + str(sfc))

def main():
    try:
        arguments = parse_args(def_parser())
        # print(arguments)
        random.seed(arguments['s'])
        file = open(arguments['o'], 'w')
        for i in range(arguments['c']):
            generate(arguments, file)
            if i < arguments['c'] - 1:
                file.write(NEWLINE)
        file.close()
    except argparse.ArgumentError:
        print(argparse)

if __name__ == "__main__":
    main()
