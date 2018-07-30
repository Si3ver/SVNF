#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# import itertools
# import numpy as np
# from numpy import random
# from scipy.optimize import linear_sum_assignment
 
# # 任务分配类
# class TaskAssignment:
 
#     # 类初始化，需要输入参数有任务矩阵以及分配方式，其中分配方式有两种，全排列方法all_permutation或匈牙利方法Hungary。
#     def __init__(self, task_matrix, mode):
#         self.task_matrix = task_matrix
#         self.mode = mode
#         if mode == 'all_permutation':
#             self.min_cost, self.best_solution = self.all_permutation(task_matrix)
#         if mode == 'Hungary':
#             self.min_cost, self.best_solution = self.Hungary(task_matrix)
 
#     # 全排列方法
#     def all_permutation(self, task_matrix):
#         number_of_choice = len(task_matrix)
#         solutions = []
#         values = []
#         for each_solution in itertools.permutations(range(number_of_choice)):
#             each_solution = list(each_solution)
#             solution = []
#             value = 0
#             for i in range(len(task_matrix)):
#                 value += task_matrix[i][each_solution[i]]
#                 solution.append(task_matrix[i][each_solution[i]])
#             values.append(value)
#             solutions.append(solution)
#         min_cost = np.min(values)
#         best_solution = solutions[values.index(min_cost)]
#         return min_cost, best_solution
 
#     # 匈牙利方法
#     def Hungary(self, task_matrix):
#         b = task_matrix.copy()
#         # 行和列减0
#         for i in range(len(b)):
#             row_min = np.min(b[i])
#             for j in range(len(b[i])):
#                 b[i][j] -= row_min
#         for i in range(len(b[0])):
#             col_min = np.min(b[:, i])
#             for j in range(len(b)):
#                 b[j][i] -= col_min
#         line_count = 0
#         # 线数目小于矩阵长度时，进行循环
#         while (line_count < len(b)):
#             line_count = 0
#             row_zero_count = []
#             col_zero_count = []
#             for i in range(len(b)):
#                 row_zero_count.append(np.sum(b[i] == 0))
#             for i in range(len(b[0])):
#                 col_zero_count.append((np.sum(b[:, i] == 0)))
#             # 划线的顺序（分行或列）
#             line_order = []
#             row_or_col = []
#             for i in range(len(b[0]), 0, -1):
#                 while (i in row_zero_count):
#                     line_order.append(row_zero_count.index(i))
#                     row_or_col.append(0)
#                     row_zero_count[row_zero_count.index(i)] = 0
#                 while (i in col_zero_count):
#                     line_order.append(col_zero_count.index(i))
#                     row_or_col.append(1)
#                     col_zero_count[col_zero_count.index(i)] = 0
#             # 画线覆盖0，并得到行减最小值，列加最小值后的矩阵
#             delete_count_of_row = []
#             delete_count_of_rol = []
#             row_and_col = [i for i in range(len(b))]
#             for i in range(len(line_order)):
#                 if row_or_col[i] == 0:
#                     delete_count_of_row.append(line_order[i])
#                 else:
#                     delete_count_of_rol.append(line_order[i])
#                 c = np.delete(b, delete_count_of_row, axis=0)
#                 c = np.delete(c, delete_count_of_rol, axis=1)
#                 line_count = len(delete_count_of_row) + len(delete_count_of_rol)
#                 # 线数目等于矩阵长度时，跳出
#                 if line_count == len(b):
#                     break
#                 # 判断是否画线覆盖所有0，若覆盖，进行加减操作
#                 if 0 not in c:
#                     row_sub = list(set(row_and_col) - set(delete_count_of_row))
#                     min_value = np.min(c)
#                     for i in row_sub:
#                         b[i] = b[i] - min_value
#                     for i in delete_count_of_rol:
#                         b[:, i] = b[:, i] + min_value
#                     break
#         row_ind, col_ind = linear_sum_assignment(b)
#         min_cost = task_matrix[row_ind, col_ind].sum()
#         best_solution = list(task_matrix[row_ind, col_ind])
#         return min_cost, best_solution
 
 
# # 生成开销矩阵
# random.seed(10000)
# task_matrix = random.randint(0, 100, size=(5, 5))
# # 用全排列方法实现任务分配
# ass_by_per = TaskAssignment(task_matrix, 'all_permutation')
# # 用匈牙利方法实现任务分配
# ass_by_Hun = TaskAssignment(task_matrix, 'Hungary')
# print('cost matrix = ', '\n', task_matrix)
# print('全排列方法任务分配：')
# print('min cost = ', ass_by_per.min_cost)
# print('best solution = ', ass_by_per.best_solution)
# print('匈牙利方法任务分配：')
# print('min cost = ', ass_by_Hun.min_cost)
# print('best solution = ', ass_by_Hun.best_solution)

# ---- 思路 ---

[[12 53 31 40 47]
 [ 2 21 72 61 17]
 [70 72 85 54 39]
 [93 34 62 75 51]
 [76 14 15  7 72]]

[[ * 53  *  *  *]
 [ *  * 72 61  *]
 [70 72 85 54  *]
 [93  * 62 75 51]
 [76  *  *  * 72]]

 53

  * 72 61  *
 70 85 54  *
 93 62 75 51
 76  *  * 72

  * 72 61  *
 70 85 54  *
 93 62 75  *
 76  *  * 72

53, 72

  * 72 61
 70 85 54
 93 62 75

  * 72  *
 70 85  *
 93 62 75

53, 72, 75

  * 72
 70 85

53, 72, 75, 72, 85

时间复杂度, O(nlongn)
12 53 31 40 47
   __
 2 21 72 61 17
      __
70 72 85 54 39
__
93 34 62 75 51
         __
76 14 15  7 72
            __

