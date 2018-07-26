# M=[]
# class DFS_hungary():

#     def __init__(self, nx, ny, edge, cx, cy, visited):
#         self.nx, self.ny=nx, ny
#         self.edge = edge
#         self.cx, self.cy=cx,cy
#         self.visited=visited

#     def max_match(self):
#         res=0
#         for i in self.nx:
#             if self.cx[i]==-1:
#                 for key in self.ny:         # 将visited置0表示未访问过
#                     self.visited[key]=0
#                 res+=self.path(i)
#         return res

#     def path(self, u):
#         for v in self.ny:
#             if self.edge[u][v] and (not self.visited[v]):
#                 self.visited[v]=1
#                 if self.cy[v]==-1:
#                     self.cx[u] = v
#                     self.cy[v] = u
#                     M.append((u,v))
#                     return 1
#                 else:
#                     M.remove((self.cy[v], v))
#                     if self.path(self.cy[v]):
#                         self.cx[u] = v
#                         self.cy[v] = u
#                         M.append((u, v))
#                         return 1
#         return 0

# if __name__ == '__main__':
#     nx, ny = ['A', 'B', 'C', 'D'], ['E', 'F', 'G', 'H']
#     edge = {'A':{'E': 1, 'F': 0, 'G': 1, 'H':0}, 'B':{'E': 0, 'F': 1, 'G': 0, 'H':1}, 'C':{'E': 1, 'F': 0, 'G': 0, 'H':1}, 'D':{'E': 0, 'F': 0, 'G': 1, 'H':0}} # 1 表示可以匹配， 0 表示不能匹配
#     cx, cy = {'A':-1,'B':-1,'C':-1,'D':-1}, {'E':-1,'F':-1,'G':-1,'H':-1}
#     visited = {'E': 0, 'F': 0, 'G': 0,'H':0}

#     print(DFS_hungary(nx, ny, edge, cx, cy, visited).max_match())
import numpy as np
from scipy.optimize import linear_sum_assignment
 
# cost =np.array([[np.inf, np.inf, 4],
#                 [4, np.inf, np.inf],
#                 [np.inf, 4, np.inf]])
cost =np.array([[1, 0, 4],
                [4, 0, 0],
                [np.inf, 4, 1]])

row_ind,col_ind=linear_sum_assignment(cost)
print(row_ind)#开销矩阵对应的行索引
print(col_ind)#对应行索引的最优指派的列索引
print(cost[row_ind,col_ind])#提取每个行索引的最优指派列索引所在的元素，形成数组
print(cost[row_ind,col_ind].sum())#数组求和
