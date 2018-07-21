#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 绘图
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def draw_plrs(plrList_svnf, plrList_rndp, plrList_clbp):
    plrList_svnf = list(map(lambda x:x*100, plrList_svnf))
    plrList_rndp = list(map(lambda x:x*100, plrList_rndp))
    plrList_clbp = list(map(lambda x:x*100, plrList_clbp))

    x_data = list(range(len(plrList_svnf)))
    plt.plot(x_data, plrList_svnf, 'r-', label='SVNFP')
    plt.plot(x_data, plrList_rndp, 'b--', label='RNDP')
    plt.plot(x_data, plrList_clbp, 'g--', label='CLBP')
    plt.xlabel('quantity of peak traffics')
    plt.ylabel('packet loss rate(%)')
    plt.title('PLR')
    plt.legend()
    plt.show()

def draw_bsr(bsrList_svnf, bsrList_rndp, bsrList_clbp):
    bsrList_svnf = list(map(lambda x:x*100, bsrList_svnf))
    bsrList_rndp = list(map(lambda x:x*100, bsrList_rndp))
    bsrList_clbp = list(map(lambda x:x*100, bsrList_clbp))

    x_data = list(range(len(bsrList_svnf)))
    plt.plot(x_data, bsrList_svnf, 'r-', label='SVNFP')
    plt.plot(x_data, bsrList_rndp, 'b--', label='RNDP')
    plt.plot(x_data, bsrList_clbp, 'g--', label='CLBP')
    plt.xlabel('quantity of peak traffics')
    plt.ylabel('bad server rate(%)')
    plt.title('BSR')
    plt.legend()
    plt.show()

def draw_SU(SUList_svnf, SUList_rndp, SUList_clbp):
    x_data = list(range(len(SUList_svnf)))
    SUList_svnf = list(map(lambda x:x*100, SUList_svnf))
    SUList_rndp = list(map(lambda x:x*100, SUList_rndp))
    SUList_clbp = list(map(lambda x:x*100, SUList_clbp))

    plt.plot(x_data, SUList_svnf, 'r-', label='SVNFP')
    plt.plot(x_data, SUList_rndp, 'b--', label='RNDP')
    plt.plot(x_data, SUList_clbp, 'g--', label='CLBP')
    plt.xlabel('quantity of peak traffics')
    plt.ylabel('Servers Utility(%)')
    plt.title('SU')
    plt.legend()
    plt.show()


def main():
    # f = open('pickleData/plr1List_svnf.dat', 'rb')
    # plr1List_svnf = pickle.load(f)
    # f.close()
    # f = open('pickleData/plr1List_rndp.dat', 'rb')
    # plr1List_rndp = pickle.load(f)
    # f.close()
    # draw_plrs(plr1List_svnf, plr1List_rndp)

    # plr
    f = open('pickleData/plr2List_svnf.dat', 'rb')
    plr2List_svnf = pickle.load(f)
    f.close()
    f = open('pickleData/plr2List_rndp.dat', 'rb')
    plr2List_rndp = pickle.load(f)
    f.close()
    f = open('pickleData/plr2List_clbp.dat', 'rb')
    plr2List_clbp = pickle.load(f)
    f.close()
    draw_plrs(plr2List_svnf, plr2List_rndp, plr2List_clbp)

    # bsr
    f = open('pickleData/percentPlrList_svnf.dat', 'rb')
    percentPlrList_svnf = pickle.load(f)
    f.close()
    f = open('pickleData/percentPlrList_rndp.dat', 'rb')
    percentPlrList_rndp = pickle.load(f)
    f.close()
    f = open('pickleData/percentPlrList_clbp.dat', 'rb')
    percentPlrList_clbp = pickle.load(f)
    f.close()    
    draw_bsr(percentPlrList_svnf, percentPlrList_rndp, percentPlrList_clbp)

    # SU
    f = open('pickleData/SUList_svnf.dat', 'rb')
    SUList_svnf = pickle.load(f)
    f.close()
    f = open('pickleData/SUList_rndp.dat', 'rb')
    SUList_rndp = pickle.load(f)
    f.close()
    f = open('pickleData/SUList_clbp.dat', 'rb')
    SUList_clbp = pickle.load(f)
    f.close()    
    draw_SU(SUList_svnf, SUList_rndp, SUList_clbp)


if __name__ == "__main__":
    main()

