#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 画累计概率分布函数图
import numpy as np
import matplotlib.pyplot as plt
import sys, os, os.path, csv, time, pickle
import figure_style as fs

M=100
lineTypes = ['rs-', 'gv--', 'bo:']

def Hopcount_CDF(y, savepath, algs, xlabel_desc):
    n=[]
    bins=[]
    n_bins=10000
    for i in range(len(y)):
        _fig_temp, axh = plt.subplots(figsize=(4,3))
        n_1, bins_1, _patches = axh.hist(y[i], n_bins, normed=1, cumulative=False, label='CDF', histtype='step', alpha=0.8, color='navy', linewidth=2)
        n.append(n_1)
        bins.append(bins_1)
    plt.close('all')

    fig,ax = plt.subplots(figsize=(4,3))
    for i in range(len(y)):
        dx=float(1/float(n_bins))
        X=bins[i][:-1]
        Y=n[i]
        Y /= (dx*Y).sum()
        CY = np.cumsum(Y*dx)
        ax.plot(X, CY*100, lineTypes[i], label=algs[i], markevery=(2000,5000))
    ax.legend()
    plt.xlabel(xlabel_desc,fontname="Times New Roman", fontsize=8)
    plt.ylabel('CDF(%)',fontname="Times New Roman", fontsize=8)
    fig.tight_layout()
    plt.savefig(savepath)
    plt.close('all')

if __name__=="__main__":
    algs = ['mvsh', 'svnf','clbp']
    algs_new = ['sVNFP','sVNFP-adv','CLBP']
    # su
    percent = [0.2]
    for x in [1,2,3]:
        for i in range(len(percent)):
            perce = percent[i]
            # 1. su
            suList = []
            for j in range(len(algs)):
                alg = algs[j]
                fInPath = './pickle_cdf/' + alg + '_su' + str(perce) + '-'+ str(x) + '.dat'
                f = open(fInPath, 'rb')
                content= pickle.load(f)
                content = list(map(lambda x:x*100, content))        # 扩大100倍，因为百分比。
                f.close()
                suList.append(content)
            fOutPath = './cdf-su'+str(int(perce*100))+'pst'+str(x)+'.pdf'
            Hopcount_CDF(suList, fOutPath, algs_new, 'servers utilization(%)')

            # 2. plr
            plrList = []
            for j in range(len(algs)):
                alg = algs[j]
                fInPath = './pickle_cdf/' + alg + '_plr' + str(perce) + '-'+ str(x) + '.dat'
                f = open(fInPath, 'rb')
                content= pickle.load(f)
                content = list(map(lambda x:x*100, content))        # 扩大100倍，因为百分比。
                f.close()
                plrList.append(content)
            fOutPath = './cdf-plr'+str(int(perce*100))+'pst'+str(x)+'.pdf'
            Hopcount_CDF(plrList, fOutPath, algs_new, 'packet loss ratio(%)')

    # hop
    hops = []
    for x in [1]:
        for j in range(len(algs)):
            alg = algs[j]
            fInPath = './pickle_cdf/' + alg + '_hop' + str(x) + '.dat'
            f = open(fInPath, 'rb')
            content= pickle.load(f)
            f.close()
            hops.append(content)
        fOutPath = './cdf_hop' + str(x)+'.pdf'
        Hopcount_CDF(hops, fOutPath, algs_new, 'hop number')

    # 3. sor 100次，peak -- 20%, peak/tr = 2~3
    x = 2
    perce = 0.2
    sor1 = [0.028, 0.064, 0.088, 0.052, 0.076, 0.116, 0.060, 0.076, 0.088, 0.104, 0.084, 0.088, 0.052, 0.088, 0.048, 0.084, 0.076, 0.080, 0.092, 0.068, 0.116, 0.104, 0.052, 0.092, 0.096, 0.116, 0.084, 0.096, 0.096, 0.064, 0.072, 0.056, 0.108, 0.032, 0.112, 0.072, 0.072, 0.088, 0.124, 0.072, 0.076, 0.080, 0.092, 0.076, 0.052, 0.076, 0.064, 0.096, 0.080, 0.084, 0.048, 0.088, 0.096, 0.132, 0.096, 0.056, 0.080, 0.036, 0.080, 0.060, 0.104, 0.124, 0.060, 0.092, 0.104, 0.104, 0.064, 0.084, 0.064, 0.100, 0.072, 0.076, 0.140, 0.124, 0.060, 0.088, 0.060, 0.072, 0.092, 0.120, 0.092, 0.092, 0.036, 0.060, 0.064, 0.120, 0.088, 0.052, 0.064, 0.088, 0.124, 0.076, 0.012, 0.076, 0.088, 0.064, 0.080, 0.056, 0.116, 0.080]
    sor2 = [0.164, 0.204, 0.164, 0.196, 0.168, 0.216, 0.216, 0.176, 0.200, 0.248, 0.176, 0.192, 0.196, 0.212, 0.188, 0.200, 0.208, 0.180, 0.204, 0.156, 0.208, 0.220, 0.204, 0.168, 0.192, 0.212, 0.164, 0.232, 0.208, 0.148, 0.180, 0.192, 0.152, 0.160, 0.144, 0.272, 0.160, 0.224, 0.220, 0.180, 0.164, 0.268, 0.188, 0.224, 0.176, 0.144, 0.164, 0.240, 0.168, 0.188, 0.156, 0.160, 0.184, 0.188, 0.180, 0.164, 0.196, 0.204, 0.140, 0.172, 0.220, 0.156, 0.192, 0.172, 0.256, 0.208, 0.132, 0.192, 0.236, 0.184, 0.188, 0.200, 0.220, 0.148, 0.232, 0.248, 0.224, 0.164, 0.252, 0.240, 0.204, 0.216, 0.152, 0.216, 0.192, 0.180, 0.148, 0.188, 0.156, 0.212, 0.212, 0.172, 0.144, 0.188, 0.216, 0.220, 0.212, 0.164, 0.228, 0.220]
    sor3 = [0.264, 0.244, 0.260, 0.264, 0.248, 0.264, 0.252, 0.276, 0.256, 0.256, 0.248, 0.240, 0.236, 0.252, 0.272, 0.244, 0.220, 0.272, 0.264, 0.272, 0.232, 0.236, 0.264, 0.260, 0.276, 0.272, 0.280, 0.244, 0.256, 0.252, 0.268, 0.256, 0.288, 0.284, 0.252, 0.220, 0.264, 0.256, 0.232, 0.252, 0.252, 0.264, 0.276, 0.256, 0.240, 0.276, 0.252, 0.272, 0.248, 0.276, 0.236, 0.264, 0.284, 0.264, 0.248, 0.244, 0.280, 0.256, 0.268, 0.264, 0.244, 0.280, 0.280, 0.232, 0.244, 0.256, 0.260, 0.240, 0.256, 0.228, 0.284, 0.244, 0.272, 0.308, 0.292, 0.220, 0.244, 0.244, 0.264, 0.244, 0.244, 0.256, 0.252, 0.252, 0.252, 0.264, 0.284, 0.280, 0.260, 0.248, 0.268, 0.276, 0.308, 0.284, 0.240, 0.228, 0.240, 0.212, 0.260, 0.292]
    sor = [sor1, sor2, sor3]
    fOutPath = './cdf-sor'+str(int(perce*100))+'pst'+str(x)+'.pdf'
    Hopcount_CDF(sor, fOutPath, algs_new, 'servers overload ratio(%)')