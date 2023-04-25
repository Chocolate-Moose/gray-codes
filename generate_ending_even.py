from radix_operations import *
from common import *
from printing import *
import math

#####################################################
#         GRAY CODE GENERATION ENDING EVEN          #
#####################################################
# does all logic to make a gray code that begins with 2 and ends with an even radix
def generate_ending_even(radices: List[int], n: int) -> List[List[int]]:
    # 1a: generate reflected code
    code = generate_reflected_code(radices)

    # 1b: move all codewords with 0 in the rightmost odd radix to the bottom
    rightmost_odd = max(i for i, j in enumerate(radices) if j % 2 != 0)
    code = move_digit_to_bottom(code, rightmost_odd, 0)

    left = [[0] + num for num in code]
    right = [[1] + num for num in code]
    code =  [left, right]

    # 3: reflect columns as needed
    reflect_columns(code, radices, n)

    # # 2/4: make knockout group, stitch all remaining codewords
    new_code = stitch_code(radices, code, rightmost_odd, n)
    return new_code

# input: radices, entire reflected gray code, n as decimal number
# output: dense, cyclic gray code for radices up to n
def stitch_code(radices: List[int], code: List[List[List[int]]], rightmost_odd: int, n: int):
    result = []

    # calculate start location, start stitching from top
    right = calculate_start_direction(code[1], radices, rightmost_odd, n)
    if right: row, col = 0, 0
    else: row, col = 0, 1

    len_inner_chunk = math.prod(radices[rightmost_odd+1:])
        
    # stitch code together
    while row < len(code[0]) - len_inner_chunk:
        if radix_to_decimal(radices, code[col][row]) < n:
            result.append(code[col][row])
            col = (col + 1) % 2

        # go to other col side
        if radix_to_decimal(radices, code[col][row]) < n:
            result.append(code[col][row])
        # stay on left side if in knockout group
        else: col = (col + 1) % 2

        row += 1

    # loop in inner chunk
    inner_chunk = code[1][len(code[0]) - len_inner_chunk:]
    inner_chunk.extend(code[0][len(code[0]) - len_inner_chunk:][::-1])
    if not right: result.reverse()

    result.extend(inner_chunk)

    return result