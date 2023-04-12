from radix_operations import *
from typing import List
import copy

#####################################################
#                  GRAY CODE COMMON                 #
#####################################################

# input: a radix tuple
# output: list of the reflected gray code as arrays without the 0/1 at the front
def generate_reflected_code(radices: List[int]) -> List[List[int]]:
    old_result = []
    new_result = []

    # compute gray code for rightmost radix
    old_result = [[i] for i in range(radices[len(radices)-1])]

    # iteratively add other radices from right to left (excluding right and left most)
    for radix in radices[len(radices)-2:0:-1]:
        ascending = True

        # prepend new radix to all numbers
        for i in range(radix):
            if ascending:
                for old in old_result:
                    new_result.append([i] + old)
            else:
                for old in old_result[::-1]:
                    new_result.append([i] + old)
            ascending = not ascending

        old_result = new_result
        new_result = []

    return old_result

# input: tuple of radices
# output: two gray code columns, one with 0 and one with 1 in front
def generate_entire_reflected_code(radices: List[int]) -> List[List[List[int]]]:
    code = generate_reflected_code(radices)
    code = move_digit_to_bottom(code, len(radices) - 1, 0)
    
    # prepend 0 and 1 to all numbers
    left = [[0] + num for num in code]
    right = [[1] + num for num in code]

    return [left, right]

# input: gray code output by generate_reflected_code
# output: gray code, but with all numbers ending in n for that column moved to the bottom
# column numbers go from left to right starting at 1
def move_digit_to_bottom(code: List[List[int]], col_num: int, n: int) -> List[List[int]]:
    result = []
    # move
    for num in code[::-1]:
        if num[col_num - 1] == n: result.append(num)
        else: result.insert(0, num)

    return result

# input: entire gray code as list of lists, radices as tuple
# output: code, but with the given column reflected
#         columns are counted from the left, 0 indexed
def reflect_column(code: List[List[List[int]]], radices: List[int], col_num: int):
    out = copy.deepcopy(code)
    for i in range(len(code[0])):
        out[0][i][col_num] = radices[col_num] - code[0][i][col_num] - 1
        out[1][i][col_num] = radices[col_num] - code[1][i][col_num] - 1

    return out