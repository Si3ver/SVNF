#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 绘图
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def draw_plrs(plrList, dNum, algNum):
    x_data = []
    for i in range(dNum):
        for j in range(algNum):
            plrList[i*dNum + j] = list(map(lambda x:x*100, plrList[i*algNum + j]))
        x_data.append(list(range(len(plrList[i*dNum]))))

    lineTypes = ['r-', 'b--', 'g--']
    algs = ['SVNFP', 'SVNFP-adv', 'CLBP']
    # algs = ['CLBP', 'SVNFP', 'SVNFP-adv']
    # plt.figure(figsize=(15,5))
    for i in range(dNum):
        plt.subplot(1,3,i+1)
        for j in range(algNum):
            plt.plot(x_data[i], plrList[i*dNum + j], lineTypes[j], label=algs[j],)
        plt.xlabel('quantity of peak traffics')
        plt.ylabel('packet loss rate(%)')
        plt.title('PLR')
        plt.legend()
    # plt.savefig('/')
    # plt.show()

def draw_bsrs(bsrList, dNum, algNum):
    x_data = []
    for i in range(dNum):
        for j in range(algNum):
            bsrList[i*dNum + j] = list(map(lambda x:x*100, bsrList[i*algNum + j]))
        x_data.append(list(range(len(bsrList[i*dNum]))))

    lineTypes = ['r-', 'b--', 'g--']
    algs = ['SVNFP', 'SVNFP-adv', 'CLBP']
    # algs = ['CLBP', 'SVNFP', 'SVNFP-adv']
    # plt.figure(figsize=(15,5))
    for i in range(dNum):
        plt.subplot(1,3,i+1 + 1)
        for j in range(algNum):
            plt.plot(x_data[i], bsrList[i*dNum + j], lineTypes[j], label=algs[j],)
        plt.xlabel('quantity of peak traffics')
        plt.ylabel('bad server rate(%)')
        plt.title('BSR')
        plt.legend()
    # plt.show()

def draw_sus(suList, dNum, algNum):
    x_data = []
    for i in range(dNum):
        for j in range(algNum):
            suList[i*dNum + j] = list(map(lambda x:x*100, suList[i*algNum + j]))
        x_data.append(list(range(len(suList[i*dNum]))))

    lineTypes = ['r-', 'b--', 'g--']
    algs = ['SVNFP', 'SVNFP-adv', 'CLBP']
    # algs = ['CLBP', 'SVNFP', 'SVNFP-adv']
    # plt.figure(figsize=(15,5))
    for i in range(dNum):
        plt.subplot(1,3,i+1 + 2)
        for j in range(algNum):
            plt.plot(x_data[i], suList[i*dNum + j], lineTypes[j], label=algs[j],)
        plt.xlabel('quantity of peak traffics')
        plt.ylabel('Servers Utility(%)')
        plt.title('SU')
        plt.legend()
    plt.show()


def main():
    algList = ['mvsh', 'svnf', 'clbp']
    dNumList = [300]
    plt.figure(figsize=(15,5))

    plr2List = []
    for dNum in dNumList:
        for alg in algList:
            path = 'pickleData/plr2List_' + alg + str(dNum) + '.dat'
            f = open(path, 'rb')
            plr2List.append(pickle.load(f))
            f.close()
    draw_plrs(plr2List, len(dNumList), len(algList))

    bsrList = []
    for dNum in dNumList:
        for alg in algList:
            path = 'pickleData/percentPlrList_' + alg + str(dNum) + '.dat'
            f = open(path, 'rb')
            bsrList.append(pickle.load(f))
            f.close()
    draw_bsrs(bsrList, len(dNumList), len(algList))

    suList = []
    for dNum in dNumList:
        for alg in algList:
            path = 'pickleData/SUList_' + alg + str(dNum) + '.dat'
            f = open(path, 'rb')
            suList.append(pickle.load(f))
            f.close()
    draw_sus(suList, len(dNumList), len(algList))


if __name__ == "__main__":
    main()

