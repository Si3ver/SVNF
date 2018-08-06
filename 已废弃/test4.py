# coding: utf-8
import timeit
from collections import deque
#==============================================================================
# 匈牙利算法
#==============================================================================
class HungarianAlgorithm(object):
    def __init__(self,graph):
        """
        @graph:图的矩阵表示
        """
        self.graph=graph
        self.n=len(graph)       

    def find(self,x):
        for i in range(self.n):
            if self.graph[x][i]==1 and not self.used[i]:
                self.used[i]=1#放入交替路
                if self.match[i]==-1 or self.find(self.match[i])==1:
                    self.match[i]=x
                    self.match[x]=i
                    print(x+1,'->',i+1)
                    return 1
        return 0
        
    def hungarian1(self):
        """递归形式
        """
        self.match=[-1]*self.n#记录匹配情况
        self.used=[False]*self.n#记录是否访问过
        m=0
        for i in range(self.n):
            if self.match[i]==-1:
                self.used=[False]*self.n
                print('开始匹配:',i+1)
                m+=self.find(i)
        return m
    
    def hungarian2(self):
        """循环形式
        """
        match=[-1]*self.n#记录匹配情况
        used=[-1]*self.n#记录是否访问过
        Q=deque()  #设置队列
        ans=0
        prev=[0]*self.n  #代表上一节点
        for i in range(self.n): 
            if match[i]==-1:
                Q.clear()
                Q.append(i)
                prev[i]=-1#设i为出发点
                flag=False #未找到增广路
                while len(Q)>0 and not flag:
                    u=Q.popleft()
                    for j in range(self.n):
                        if not flag and self.graph[u][j]==1 and  used[j]!=i:
                            used[j]=i        
                            if match[j]!=-1:
                                Q.append(match[j])
                                prev[match[j]]=u#记录点的顺序
                            else:
                                flag=True
                                d=u
                                e=j
                                while(d!=-1):#将原匹配的边去掉加入原来不在匹配中的边
                                    t=match[d]
                                    match[d]=e
                                    match[e]=d
                                    d=prev[d]
                                    e=t
                                print('mathch:',match)
                                print('prev:',prev)
                                print('deque',Q)
                if  match[i]!=-1:#新增匹配边
                    ans+=1
        return ans
        

def do1():  
    # graph=[(0,0,0,0,1,0,1,0),
    #    (0,0,0,0,1,0,0,0),
    #    (0,0,0,0,1,1,0,0),
    #    (0,0,0,0,0,0,1,1),
    #    (1,1,1,0,0,0,0,0),
    #    (0,0,1,0,0,0,0,0),
    #    (1,0,0,1,0,0,0,0),
    #    (0,0,0,1,0,0,0,0)]
    graph = [[0,1,0],
         [0,1,1],
         [0,0,0]]
    h=HungarianAlgorithm(graph)
    print (h.hungarian1())

def do2():  
    # graph=[(0,0,0,0,1,0,1,0),
    #    (0,0,0,0,1,0,0,0),
    #    (0,0,0,0,1,1,0,0),
    #    (0,0,0,0,0,0,1,1),
    #    (1,1,1,0,0,0,0,0),
    #    (0,0,1,0,0,0,0,0),
    #    (1,0,0,1,0,0,0,0),
    #    (0,0,0,1,0,0,0,0)]
    graph = [[1,1,0,0],
         [0,1,0,0],
         [0,0,1,1]]
    h=HungarianAlgorithm(graph)
    print (h.hungarian2())

do1()