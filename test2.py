#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# maxize minmum vertical scaling heuristic (MVSH)
import sys, os.path, argparse, re, math
import numpy as np
import fattree
from collections import deque

class HungarianAlgorithm(object):
    def __init__(self, graph, m, dId):
        self.graph=graph
        self.n=len(graph)
        self.m = m
        self.dId = dId
    def hungarian(self):
        match=[-1]*self.n           #记录匹配情况
        used=[-1]*self.n            #记录是否访问过
        Q=deque()                   #设置队列
        prev=[0]*self.n             #代表上一节点
        for i in range(self.n): 
            if match[i]==-1:
                Q.clear()
                Q.append(i)
                prev[i]=-1          #设i为出发点
                flag=False          #未找到增广路
                while len(Q)>0 and not flag:
                    u=Q.popleft()
                    for j in range(self.n):
                        if not flag and self.graph[u][j]==1 and  used[j]!=i:
                            used[j]=i        
                            if match[j]!=-1:
                                Q.append(match[j])
                                prev[match[j]]=u    #记录点的顺序
                            else:
                                flag=True
                                d=u
                                e=j
                                while(d!=-1):       #将原匹配的边去掉加入原来不在匹配中的边
                                    t=match[d]
                                    match[d]=e
                                    match[e]=d
                                    d=prev[d]
                                    e=t
        # if self.dId == 1:
        #     print('###', match)
        return list(match[0:self.m])

# graph = [[0,1,0],
#          [1,0,1],
#          [0,0,0]]
graph = [[0,1,0],
         [1,0,1]]

h = HungarianAlgorithm(graph, 2, 1)
res = h.hungarian()
print(res)
