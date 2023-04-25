from radix_operations import *
from common import *
from printing import *

#####################################################
#         GRAY CODE GENERATION ENDING ODD           #
#####################################################
# does all logic to make a gray code that begins with 2 and ends with an odd radix
def generate_ending_odd(radices: List[int], n: int) -> List[List[int]]:
    # 1a: generate reflected code
    code = generate_reflected_code(radices)

    # 1b: move all codewords ending in 0 to the bottom
    code = move_digit_to_bottom(code, len(radices) - 1, 0)

    # 1c: reflect all sequences in position 0 in the upper portion
    reflect_upper(code, radices)
    left = [[0] + num for num in code]
    right = [[1] + num for num in code]
    code =  [left, right]

    # 3: reflect columns as needed
    reflect_columns(code, radices, n)

    # # 2/4: make knockout group, stitch all remaining codewords
    new_code = stitch_code(radices, code, n)
    return new_code

# reflects last numbers in the top half of the code that do not end with 0
def reflect_upper(code: List[List[int]], radices: List[int]):
    for i in code:
        last = i[len(i)-1]
        if last != 0: i[len(i)-1] = radices[len(radices)-1] - i[len(i)-1]

# input: radices, entire reflected gray code, n as decimal number
# output: dense, cyclic gray code for radices up to n
def stitch_code(radices: List[int], code: List[List[List[int]]], n: int):
    result = []

    # check if n too big or small
    largest = 1
    for radix in radices: largest *= radix

    # special case where inner ring isn't in yet
    half = largest / radices[0]
    if n < half + radices[len(radices)-1]-1: 
        print('inner chunkxs')
        return []

    # calculate start location
    right = calculate_start_direction(code[1], radices, len(radices)-1, n)
    if right: row, col = radices[len(radices)-1]-1, 0
    else: row, col = radices[len(radices)-1]-1, 1

    # append the top bit for the inner ring
    # right part of inner ring, from the bottom to top
    result.extend(code[1][0:radices[len(radices)-1]-1][::-1])
    result.extend(code[0][0:radices[len(radices)-1]-1])
    if not right: result.reverse()
        
    # thread code together
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