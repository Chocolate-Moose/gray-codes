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
    for i in range(len(code[0])):
        code[0][i][col_num] = radices[col_num] - code[0][i][col_num] - 1
        code[1][i][col_num] = radices[col_num] - code[1][i][col_num] - 1

# input: 
# output: the code but with all columns in ascending sequences reflected
def reflect_columns(code: List[List[List[int]]], radices: List[int], n: int):
    largest_remaining_codeword = decimal_to_radix(radices, n-1)

    col_sum = 0
    ascending = []
    # when cumulative sum is even, flip
    for i, num in enumerate(largest_remaining_codeword):
        if col_sum % 2 == 0 and 1 < i < len(largest_remaining_codeword):
            ascending.append(i)
            # add 1 for flip when even radix
            if radices[i] % 2 == 0: col_sum += 1
        col_sum += num

    for pos in ascending:
        reflect_column(code, radices, pos)  


# input: gray code and n as decimal number
# output: if the gray code should start going right or left
def calculate_start_direction(code: List[List[int]], radices: List[int], rightmost_odd: int, n: int):
    count = 0
    # whatever digit is constant in lower portion
    constant = code[len(code)-1][rightmost_odd]

    # iterate over numbers ending in 0 at bottom of code
    for num in code[::-1]:
        if num[rightmost_odd] != constant: break
        elif radix_to_decimal(radices, num) < n:
            count += 1

    if count % 2 == 1: return True
    else: return False