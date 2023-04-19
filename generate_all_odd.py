from radix_operations import *
from common import *
from printing import *

#####################################################
#           GRAY CODE GENERATION ALL ODD            #
#####################################################
# does all logic to make a gray code that begins with 2 and has all odd radices
def generate_all_odd(radices: List[int], n: int):
    # 1a: generate reflected code
    code = generate_reflected_code(radices)

    # 1b: move all codewords ending in 0 to the bottom
    code = move_digit_to_bottom(code, len(radices) - 1, 0)
    left = [[0] + num for num in code]
    right = [[1] + num for num in code]
    code =  [left, right]

    # 3: reflect columns as needed
    reflect_columns(code, radices, n)

    # 2/4: make knockout group, stitch all remaining codewords
    new_code = stitch_code(radices, code, n)
    return new_code

# input: gray code and n as decimal
# output: what columns need to be reflected (based on order of sequences of n-1)
# TODO; maybe move to common?
def reflect_columns(code: List[List[List[int]]], radices: List[int], n: int):
    largest_remaining_codeword = decimal_to_radix(radices, n-1)

    col_sum = 0
    ascending = []
    # when cumulative sum is even, flip
    for i, num in enumerate(largest_remaining_codeword):
        # TODO: should this go up to len of largest remaining codeword?
        if col_sum % 2 == 0 and 1 < i < len(largest_remaining_codeword) - 1:
            ascending.append(i)
        col_sum += num

    for pos in ascending:
        reflect_column(code, radices, pos)    

# input: radices, entire reflected gray code, n as decimal number
# output: dense, cyclic gray code for radices up to n
def stitch_code(radices: List[int], code: List[List[List[int]]], n: int):
    result = []

    # calculate start location
    right = calculate_start_direction(code[1], radices, n)
    if right: row, col = 0,1
    else: row, col = 0,0

    # stitch code together
    while row < len(code[0]):

        if radix_to_decimal(radices, code[col][row]) < n:
            result.append(code[col][row])
            col = (col + 1) % 2

        # go to other col side
        if radix_to_decimal(radices, code[col][row]) < n:
            result.append(code[col][row])
        # stay on left side if in knockout group
        else: col = (col + 1) % 2

        row += 1

    return result

# input: gray code and n as decimal number
# output: if the gray code should start going right or left
# TODO; generalize to other radices
def calculate_start_direction(code: List[List[int]], radices: List[int], n: int):
    count = 0

    # iterate over numbers ending in 0 at bottom of code
    for num in code[::-1]:
        if num[len(num)-1] != 0: break
        elif radix_to_decimal(radices, num) < n:
            count += 1
    if count % 2 == 1: return True
    else: return False