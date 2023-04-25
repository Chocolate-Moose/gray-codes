from radix_operations import *
from common import *
from printing import *

#####################################################
#           GRAY CODE GENERATION ALL ODD            #
#####################################################
# does all logic to make a gray code that begins with 2 and has all odd radices
def generate_all_odd(radices: List[int], n: int) -> List[List[int]]:
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

# input: radices, entire reflected gray code, n as decimal number
# output: dense, cyclic gray code for radices up to n
def stitch_code(radices: List[int], code: List[List[List[int]]], n: int):
    result = []

    # calculate start location
    right = calculate_start_direction(code[1], radices, len(radices)-1, n)
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