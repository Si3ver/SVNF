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

def draw_hop(plrList, algs, lineTypes, x_label, y_label, flag):
    x_data = ['1~2', '2~3', '3~4', '4~5', '5~6', '6~7']
    if flag:
        for i in range(len(algs)):
            plrList[i] = list(map(lambda x:x*100, plrList[i]))

    plt.ylim((0, 6))
    for i in range(len(algs)):
        plt.plot(x_data, plrList[i], lineTypes[i], label=algs[i], markevery=(len(plrList[0])//10, len(plrList[0])//5))
    plt.ylim((0, 6))
    plt.xlabel(x_label,fontname="Times New Roman", fontsize=8)
    plt.ylabel(y_label,fontname="Times New Roman", fontsize=8)
    plt.legend()

def main():
    # plr = []
    # plr.append([0.009, 0.011, 0.009, 0.007, 0.004, 0.002])
    # plr.append([0.059, 0.039, 0.027, 0.023, 0.011, 0.007])
    # plr.append([0.102, 0.086, 0.077, 0.069, 0.060, 0.052])
    # sor = []
    # sor.append([0.092, 0.096, 0.1,   0.084, 0.048, 0.036])
    # sor.append([0.344, 0.196, 0.136, 0.104, 0.08,  0.052])
    # sor.append([0.292, 0.264, 0.244, 0.196, 0.176, 0.164])
    # su = []
    # su.append([0.595, 0.593, 0.594, 0.594, 0.580, 0.567])
    # su.append([0.552, 0.575, 0.584, 0.587, 0.582, 0.575])
    # su.append([0.963, 0.930, 0.868, 0.797, 0.763, 0.730])
    plr = []
    plr.append([0.000, 0.000, 0.003, 0.017, 0.029, 0.047])
    plr.append([0.018, 0.030, 0.041, 0.054, 0.062, 0.091])
    plr.append([0.085, 0.159, 0.222, 0.276, 0.322, 0.364])
    sor = []
    sor.append([0.000, 0.004, 0.052, 0.172, 0.204, 0.256])
    sor.append([0.200, 0.184, 0.196, 0.248, 0.272, 0.312])
    sor.append([0.352, 0.360, 0.360, 0.360, 0.360, 0.364])
    su = []
    su.append([0.546, 0.595, 0.641, 0.679, 0.690, 0.707])
    su.append([0.536, 0.577, 0.617, 0.655, 0.680, 0.684])
    su.append([0.992, 0.993, 0.994, 0.995, 0.996, 0.997])

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
    draw_hop(hops, algs, lineTypes, x_label, 'average hops', False)
    plt.tight_layout()
    plt.savefig('results/tau_hops.pdf')
    plt.close()

if __name__ == "__main__":
    main()
