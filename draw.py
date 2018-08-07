#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, pickle, argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# 定义命令行参数格式
def def_parser():
    parser = argparse.ArgumentParser(description='draw graph of results')
    parser.add_argument('-c', '--count', dest='c', help='How many service request', type=int, default=50)
    parser.add_argument('-s', '--seed', dest='s', help='Random seed', type=int, default=10)
    return parser

# 参数解析
def parse_args(parser):
    opts   = vars(parser.parse_args(sys.argv[1:]))
    return opts

def draw_plrs(plrList, algs, lineTypes):
    plt.subplot(1,3,1)
    x_data = list(range(len(plrList[0])))
    x_data = list(map(lambda x:x*100/len(plrList[0]), x_data))
    for i in range(len(algs)):
        plrList[i] = list(map(lambda x:x*100, plrList[i]))

    for i in range(len(algs)):
        plt.plot(x_data, plrList[i], lineTypes[i], label=algs[i], markevery=(len(plrList[0])//10, len(plrList[0])//5))
    plt.xlabel('percentage of peak traffics(%)')
    plt.ylabel('packet loss rate(%)')
    plt.legend()

def draw_bsrs(bsrList, algs, lineTypes):
    plt.subplot(1,3,2)
    x_data = list(range(len(bsrList[0])))
    x_data = list(map(lambda x:x*100/len(bsrList[0]), x_data))
    for i in range(len(algs)):
        bsrList[i] = list(map(lambda x:x*100, bsrList[i]))
    for i in range(len(algs)):
        plt.plot(x_data, bsrList[i], lineTypes[i], label=algs[i], markevery=(len(bsrList[0])//10, len(bsrList[0])//5))
    plt.xlabel('percentage of peak traffics(%)')
    plt.ylabel('percentage of overload servers(%)')
    plt.legend()

def draw_sus(suList, algs, lineTypes):
    plt.subplot(1,3,3)
    x_data = list(range(len(suList[0])))
    x_data = list(map(lambda x:x*100/len(suList[0]), x_data))
    for i in range(len(algs)):
        suList[i] = list(map(lambda x:x*100, suList[i]))
    for i in range(len(algs)):
        plt.plot(x_data, suList[i], lineTypes[i], label=algs[i], markevery=(len(suList[0])//10, len(suList[0])//5))
    plt.xlabel('percentage of peak traffics(%)')
    plt.ylabel('utility of servers(%)')
    plt.legend()

def main():
    args = parse_args(def_parser())
    dNum = args['c']
    algList = ['mvsh', 'svnf', 'clbp']

    plr2List = []
    for alg in algList:
        path = 'pickleData/plr2List_'       + alg + '-c' + str(dNum) + 's' + str(args['s']) + '.dat'
        f = open(path, 'rb')
        plr2List.append(pickle.load(f))
        f.close()
    bsrList = []
    for alg in algList:
        path = 'pickleData/percentPlrList_' + alg + '-c' + str(dNum) + 's' + str(args['s']) + '.dat'
        f = open(path, 'rb')
        bsrList.append(pickle.load(f))
        f.close()
    suList = []
    for alg in algList:
        path = 'pickleData/SUList_'         + alg + '-c' + str(dNum) + 's' + str(args['s']) + '.dat'
        f = open(path, 'rb')
        suList.append(pickle.load(f))
        f.close()

    algs = ['sVNFP', 'sVNFP-adv', 'CLBP']
    lineTypes = ['rs-', 'gv--', 'bo:']
    plt.figure(figsize=(15,5))
    draw_plrs(plr2List, algs, lineTypes)
    draw_bsrs(bsrList, algs, lineTypes)
    draw_sus(suList, algs, lineTypes)
    plt.tight_layout()
    plt.savefig('results/c'+str(args['c'])+'s'+str(args['s'])+'.eps')
    plt.savefig('results/c'+str(args['c'])+'s'+str(args['s'])+'.png')

if __name__ == "__main__":
    main()
