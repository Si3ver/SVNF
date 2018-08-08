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

M=100
mycolor=['r','g','b','g','c','m','y','k','orange','plum','gold','lime','deeppink','chocolate','blueviolet','navy','slategray','deepskyblue','peru','midnightblue','orangered','orchid']
mylinestyle=['-','--','-.',':']
mymarker=['s','p','*','o','v','^','<','>',',']
patterns = (" ","//" , ".." ,"////" , "\\\\\\", "----" , "||||"  , "++++" , "xxxx", "oooo", "O", ".", "*" )

def E_Hopcount_bar_group(index,y,savepath,algorithm_name,xlabel_name, x_label_description):
    # draw the figure
    fig,ax = plt.subplots(figsize=fs.SMALL_FIGURE_SIZE)
    bar_width= 0.2

    x=index
    for i in range(len(y)):
        #rects=ax.bar(index+i*bar_width,y[i],bar_width,color=mycolor[i],label=algorithm_name[i],hatch=patterns[i])
        rects=ax.bar(index+i*bar_width,y[i],bar_width,edgecolor=mycolor[i],color=(1,1,1,1),label=algorithm_name[i],hatch=patterns[i])
    ax.legend(fontsize=fs.LEGEND_SIZE-1, bbox_to_anchor=(0.16,0.58))
    ax.grid()
    ax.set_xticks(index + bar_width)
    ax.set_xticklabels(x_label_description)

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
    plt.xlabel(xlabel_name,fontweight='normal',fontsize=fs.XY_LABEL_SIZE,fontname="Times New Roman",color='k',horizontalalignment='center',x=0.5)#plt.xlabel('Sep 2014                                     Oct 2014',fontweight='semibold',fontsize=16,color='gray',horizontalalignment='left',x=-0.02)
    ax.xaxis.labelpad = 2.5
    plt.ylabel('Average hops',fontweight='normal',fontsize=fs.XY_LABEL_SIZE,fontname="Times New Roman",color='k',horizontalalignment='center',y=0.5)
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


def main():
    index=np.arange(1,3,1)
    # index = np.array('shiyan1','shiyan2')
    y=[[5.090,5.119],[2.370,2.371],[2.082,2.205]]
    x_label_description = ['exp=1~2','exp=3~4']
    algs=['sVNFP','sVNFP-adv','CLBP']
    E_Hopcount_bar_group(index, y, './fig1.pdf', algs, 'exp', x_label_description)
    

if __name__ == "__main__":
    main()
