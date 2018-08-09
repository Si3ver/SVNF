#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 画随着peak/tr的变化，各参数的变化情况
import sys, pickle, argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def draw(plrList, algs, lineTypes, x_label, y_label, flag):
    x_data = ['1~2', '2~3', '3~4', '4~5', '5~6', '6~7']
    if flag:
        for i in range(len(algs)):
            plrList[i] = list(map(lambda x:x*100, plrList[i]))

    for i in range(len(algs)):
        plt.plot(x_data, plrList[i], lineTypes[i], label=algs[i], markevery=(len(plrList[0])//10, len(plrList[0])//5))
    plt.xlabel(x_label,fontname="Times New Roman", fontsize=8)
    plt.ylabel(y_label,fontname="Times New Roman", fontsize=8)
    plt.legend()

def main():
    plr = []
    plr.append([0.046, 0.058, 0.047, 0.040, 0.037, 0.027])
    plr.append([0.135, 0.122, 0.110, 0.113, 0.070, 0.067])
    plr.append([0.270, 0.237, 0.220, 0.224, 0.213, 0.197])
    sor = []
    sor.append([0.092, 0.096, 0.1,   0.084, 0.048, 0.036])
    sor.append([0.344, 0.196, 0.136, 0.104, 0.08,  0.052])
    sor.append([0.292, 0.264, 0.244, 0.196, 0.176, 0.164])
    su = []
    su.append([0.595, 0.593, 0.594, 0.594, 0.580, 0.567])
    su.append([0.552, 0.575, 0.584, 0.587, 0.582, 0.575])
    su.append([0.963, 0.930, 0.868, 0.797, 0.763, 0.730])
    hops = []
    hops.append([5.090, 5.144, 5.119, 5.152, 4.993, 5.052])
    hops.append([2.370, 2.540, 2.731, 2.977, 3.005, 3.061])
    hops.append([2.082, 2.134, 2.205, 2.276, 2.268, 2.223])    

    algs = ['sVNFP', 'sVNFP-adv', 'CLBP']
    lineTypes = ['rs-', 'gv--', 'bo:']
    x_label = 'peak/tr'

    plt.figure(figsize=(4,3))
    draw(plr, algs, lineTypes, x_label, 'packet loss ratio(%)', True)
    plt.tight_layout()
    plt.savefig('results/tau_plr.pdf')
    plt.close()

    plt.figure(figsize=(4,3))
    draw(sor, algs, lineTypes, x_label, 'servers overload ratio(%)', True)
    plt.tight_layout()
    plt.savefig('results/tau_sor.pdf')
    plt.close()

    plt.figure(figsize=(4,3))
    draw(su, algs, lineTypes, x_label, 'servers utilization(%)', True)
    plt.tight_layout()
    plt.savefig('results/tau_su.pdf')
    plt.close()

    plt.figure(figsize=(4,3))
    draw(hops, algs, lineTypes, x_label, 'average hops', False)
    plt.tight_layout()
    plt.savefig('results/tau_hops.pdf')
    plt.close()

if __name__ == "__main__":
    main()
