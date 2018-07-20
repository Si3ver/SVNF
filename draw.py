#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 绘图
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


def draw_plrs(plr1List, plr2List):
    plr1List = list(map(lambda x:x*100, plr1List))
    plr2List = list(map(lambda x:x*100, plr2List))

    x_data = list(range(len(plr1List)))
    plt.plot(x_data, plr1List, 'r-', label='plr of busy servers')
    plt.plot(x_data, plr2List, 'b--', label='plr of all topo')
    plt.xlabel('quantity of peak traffics')
    plt.ylabel('packet loss rate(%)')
    plt.title('traffics expand stress test')
    plt.legend()
    plt.show()


def draw_SU(SUList_svnf):
    x_data = list(range(len(SUList_svnf)))
    SUList_svnf = list(map(lambda x:x*100, SUList_svnf))

    plt.plot(x_data, SUList_svnf, 'r-', label='SVNF')
    plt.xlabel('quantity of peak traffics')
    plt.ylabel('Servers Utility(%)')
    # plt.title('traffics expand stress test')
    plt.legend()
    plt.show()


def main():
    # f = open('pickleData/plr1List_svnf.dat', 'rb')
    # plr1List = pickle.load(f)
    # f.close()

    # f = open('pickleData/plr2List_svnf.dat', 'rb')
    # plr2List = pickle.load(f)
    # f.close()

    # print(plr1List, plr2List)
    # draw_plrs(plr1List, plr2List)

    f = open('pickleData/SUList_svnf.dat', 'rb')
    SUList_svnf = pickle.load(f)
    f.close()
    draw_SU(SUList_svnf)


if __name__ == "__main__":
    main()

