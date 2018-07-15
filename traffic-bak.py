#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, random, math
import argparse
import numpy as np

DELIM     = " "
NEWLINE = "\n"

# 解释命令行参数
def def_parser():
    parser = argparse.ArgumentParser(description='Generating Service Requests!')
    parser.add_argument('-c', '--count'   , dest='c', help='How many service request', type=int, default=1000)
    parser.add_argument('-k', '--kparam'  , dest='k', help='K parameter of K-ary fattree', type=int  , required=True)
    parser.add_argument('-a', '--arrival' , dest='a', help='Arrival rate parameter (in second)', type=float, required=True)
    parser.add_argument('-d', '--duration', dest='d', help='Duration parameter (in second)', type=float, required=True)
    parser.add_argument('-o', '--output'  , dest='o', help='Output file name',type=str, default='requests.txt')
    parser.add_argument('-s', '--seed'    , dest='s', help='Random seed', type=int, default=10)
    return parser

# 参数解析
def parse_args(parser):
    opts = vars(parser.parse_args(sys.argv[1:]))
    # print(sys.argv)
    # print(parser.parse_args(sys.argv[1:]))
    # print(opts)
    k      = opts['k']                              # k =   10
    opts['min'] = (5 * k ** 2) / 4                  # start 125
    opts['max'] = opts['min'] + (k ** 3) / 4 - 1    # end   374
    opts['inv'] = 1.00 / opts['d']
    return opts

def generate(args, t, file):
    global DELIM, NEWLINE
    src = random.randint(args['min'], args['max'])
    dst = random.randint(args['min'], args['max'])
    t  += math.floor(np.random.poisson(args['a']))
    d     = math.floor(np.random.exponential(args['d'])) + 1
    if d % 2 != 0:
        d += 1
    file.write(str(src) + DELIM + str(dst) + DELIM + str(int(t)) + DELIM + str(int(d)))
    return t

def main():
    try:
        arguments = parse_args(def_parser())
        print(arguments)
        random.seed(arguments['s'])
        file = open(arguments['o'], 'w')
        t = 1
        for i in range(arguments['c']):
            t = generate(arguments, t, file)
            if i < arguments['c'] - 1:
                file.write(NEWLINE)
        file.close()
    except argparse.ArgumentError:
        print(argparse)

if __name__ == "__main__":
    main()