def BFS_hungary(graph):
    res=0
    rowLen, colLen = len(graph), len(graph[0])
    Q=[0]*100
    prev=[0]*colLen
    Mx = [-1]*rowLen
    My = [-1]*colLen
    chk = [-1]*colLen
    for i in range(rowLen):
        if Mx[i]==-1:
            qs=qe=0
            Q[qe]=i
            qe+=1
            prev[i]=-1

            flag=0
            while(qs<qe and not flag):
                u=Q[qs]
                for v in range(colLen):
                    if flag:continue
                    if graph[u][v] and chk[v]!=i:
                        chk[v]=i
                        Q[qe]=My[v]
                        qe+=1
                        if My[v]>=0:
                            prev[My[v]]=u
                        else:
                            flag=1
                            d,e=u,v
                            while d!=-1:
                                t=Mx[d]
                                Mx[d]=e
                                My[e]=d
                                d=prev[d]
                                e=t
                qs+=1
            if Mx[i]!=-1:
                res+=1
    return Mx

if __name__ == '__main__':
        # g=[[1,0,1,0],
        #    [0,1,0,1],
        #    [1,0,0,1],
        #    [0,0,1,0]]
        # g=[[1,1,1,1],
        #    [1,0,0,0],
        #    [1,1,1,1],
        #    [1,1,1,1]]
        # graph=[[1,1,1,1],
        #        [1,0,0,0]]   
        graph = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]   
        print(BFS_hungary(graph))
        # print(Mx, My)

