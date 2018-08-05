def BFS_hungary(g,Nx,Ny,Mx,My,chk,Q,prev):
    res=0
    for i in range(Nx):
        if Mx[i]==-1:
            qs=qe=0
            Q[qe]=i
            qe+=1
            prev[i]=-1

            flag=0
            while(qs<qe and not flag):
                u=Q[qs]
                for v in range(Ny):
                    if flag:continue
                    if g[u][v] and chk[v]!=i:
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
    return res

if __name__ == '__main__':
        # g=[[1,0,1,0],
        #    [0,1,0,1],
        #    [1,0,0,1],
        #    [0,0,1,0]]
        # g=[[1,1,1,1],
        #    [1,0,0,0],
        #    [1,1,1,1],
        #    [1,1,1,1]]
        g=[[1,1,1,1],
           [1,0,0,0]]        
        Nx=2
        Ny=4
        Mx=[-1,-1,-1,-1]
        My=[-1,-1,-1,-1]
        chk=[-1,-1,-1,-1]
        Q=[0 for i in range(100)]
        prev=[0,0,0,0]        
        print(BFS_hungary(g,Nx, Ny, Mx, My, chk, Q, prev))
        print(Mx, My)

