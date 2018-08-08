#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import numpy as np
import matplotlib.pyplot as plt
import os
import os.path
import csv
import time
import figure_style as fs
from struct import *
import pickle

M=100
mycolor=['r','g','b','g','c','m','y','k','orange','plum','gold','lime','deeppink','chocolate','blueviolet','navy','slategray','deepskyblue','peru','midnightblue','orangered','orchid']
mylinestyle=['-','--','-.',':']
mymarker=['s','p','*','o','v','^','<','>',',']
patterns = (" ","//" , ".." ,"////" , "\\\\\\", "----" , "||||"  , "++++" , "xxxx", "oooo", "O", ".", "*" )

def Hopcount_CDF(y,savepath,algorithm_name):
    # draw the figure
    n=[]
    bins=[]
    n_bins=10000
    for i in range(len(y)):
        fig_temp,axh = plt.subplots(figsize=fs.SMALL_FIGURE_SIZE)
        n_1, bins_1, patches = axh.hist(y[i], n_bins,normed=1,cumulative=False, label='CDF', histtype='step', alpha=0.8, color='navy',linewidth=1.5)
        n.append(n_1)
        bins.append(bins_1)
        #print(len(y[i]))
    plt.close('all')

    fig,ax = plt.subplots(figsize=fs.SMALL_FIGURE_SIZE)
    for i in range(len(y)):
        dx=float(1/float(n_bins))
        X=bins[i][:-1]
        Y=n[i]
        Y /= (dx*Y).sum()
        CY = np.cumsum(Y*dx)
        ax.plot(X,CY*100,color=mycolor[i],linestyle=mylinestyle[i],linewidth=fs.LINE_WIDTH,label=algorithm_name[i])
    ax.legend(fontsize=fs.LEGEND_SIZE)
    ax.grid()

    #delete the upper and right frame
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    #set x(y) axis (spines)
    ax.spines['bottom'].set_linewidth(fs.XY_SPINES_WIDTH)
    ax.spines['bottom'].set_color('k')
    ax.spines['left'].set_linewidth(fs.XY_SPINES_WIDTH)
    ax.spines['left'].set_color('k')
    #ax.set_xlim(xmin=0)
    #ax.set_ylim(ymin=0)

    #set x(y) label
    #r'$\Delta hop counts$'
    plt.xlabel('servers utility',fontweight='normal',fontsize=fs.XY_LABEL_SIZE,fontname="Times New Roman",color='k',horizontalalignment='center',x=0.5)#plt.xlabel('Sep 2014                                     Oct 2014',fontweight='semibold',fontsize=16,color='gray',horizontalalignment='left',x=-0.02)
    ax.xaxis.labelpad = 2.5
    plt.ylabel('servers count/sum servers',fontweight='normal',fontsize=fs.XY_LABEL_SIZE,fontname="Times New Roman",color='k',horizontalalignment='center',y=0.5)
    ax.yaxis.labelpad = 2.5
    plt.title('',fontweight='normal',fontsize=fs.TITLE_SIZE,fontname="Times New Roman",color='k',horizontalalignment='center',x=0.5,y=1)

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(fs.TICK_LABEL_SIZE)
        tick.label.set_fontweight('normal')#tick.label.set_rotation('vertical')
        tick.label.set_color('k')
    

    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(fs.TICK_LABEL_SIZE)
        tick.label.set_fontweight('normal')#tick.label.set_rotation('vertical')
        tick.label.set_color('k')

    ax.tick_params(direction='in')

    # save figure
    fig.tight_layout()
    plt.savefig(savepath)
    #plt.show()
    plt.close('all')

if __name__=="__main__":
    algs = ['mvsh', 'svnf','clbp']
    percent = [0.2, 0.5, 0.7]
    algs_new = ['sVNFP','sVNFP-adv','CLBP']
    for x in [1,2]:
        for i in range(len(percent)):
            suList = []
            perce = percent[i]
            for j in range(len(algs)):
                alg = algs[j]
                fInPath = './pickle_cdf/' + alg + '_su' + str(perce) + '-'+ str(x) + '.dat'
                f = open(fInPath, 'rb')
                content= pickle.load(f)
                f.close()                
                suList.append(content)
            fOutPath = './cdf_su'+str(perce)+'-'+str(x)+'.pdf'
            Hopcount_CDF(suList, fOutPath, algs_new)
