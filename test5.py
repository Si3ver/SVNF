# m个VNF，分配给n台server。寻找一个匹配
class DFS_hungary():
    def __init__(self, graph):
        self.graph = graph
        self.rowLen, self.colLen = len(graph), len(graph[0])
        self.cx, self.cy = [-1]*self.rowLen, [-1]*self.colLen
        self.visited = [0]*self.colLen
        self.M = []
    def max_match(self):
        res = 0
        for i in range(self.rowLen):
            if self.cx[i] == -1:
                for j in range(self.colLen):
                    self.visited[j] = 0
                res += self.path(i)
        return self.cx
    def path(self, u):
        for v in range(self.colLen):
            if self.graph[u][v] == 1 and (not self.visited[v]):
                self.visited[v] = 1
                if self.cy[v] == -1:
                    self.cx[u] = v
                    self.cy[v] = u
                    print('+++', self.M, u, v, '\t\t\t', end='-> ')
                    self.M.append((u,v))
                    print(self.M)
                    return 1
                else:
                    print('---', self.M, self.cy[v],v, '\t\t\t',end='-> ')
                    self.M.remove((self.cy[v], v))
                    print(self.M)
                    if self.path(self.cy[v]):
                        self.cx[u] = v
                        self.cy[v] = u
                        print('+++', self.M, u, v, '\t\t\t',end='-> ')
                        self.M.append((u,v))
                        print(self.M)
                        return 1
        return 0

def print_matrix(M):
    rowLen, colLen = len(M), len(M[0])
    for i in range(rowLen):
        for j in range(colLen):
            print('%2d' % M[i][j], end=' ')
        print()

if __name__ == '__main__':
    # graph = [[ 0, 1, 0, 1],
    #          [ 0, 1, 0, 0],
    #          [ 0, 0, 1, 1]]
    # graph = [[ 1, 0, 1, 0],
    #          [ 0, 1, 0, 1],
    #          [ 1, 0, 0, 1],
    #          [ 0, 0, 1, 0]]
    # print_matrix(graph)
    # graph = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    graph = [[1,1,1,1],[1,0,0,0],[1,1,1,1],[1,1,1,1]]
    hg = DFS_hungary(graph)
    res = hg.max_match()
    print(res)
