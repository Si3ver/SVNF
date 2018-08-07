from munkres import Munkres

# matrix = [[ 5, 9, 1],
#           [10, 3, 2],
#           [8,  7, 4]]
# m = Munkres()
# indexes = m.compute(matrix)
# # print_matrix(matrix, msg='Lowest cost through this matrix:')
# total = 0
# for row, column in indexes:
#     value = matrix[row][column]
#     total += value
#     print('(%d, %d) -> %d' % (row, column, value))
# print('total cost: %d' % total)


matrix = [[0,1,0],
         [0,1,1],
         [0,0,0]]

m = Munkres()
indexes = m.compute(matrix)
for row, column in indexes:
    value = matrix[row][column]
    # total += value
    print('(%d, %d) -> %d' % (row, column, value))
