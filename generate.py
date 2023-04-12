from radix_operations import *
from common import *
from printing import *

#####################################################
#           GRAY CODE GENERATION ALL ODD            #
#####################################################

# input: radices, entire reflected gray code, n as decimal number
# output: dense, cyclic gray code for radices up to n
def generate_threaded_code(radices: List[int], code: List[List[List[int]]], n: int):
    # check if n too big or small
    largest = 1
    for radix in radices: largest *= radix
    if n < 0 or n > largest - 1:
        print('n is out of range of the radix')
        return []

    # see if we need to flip
    ascending = in_bottom_ascending_sequence(radices, n)
    # ascending = [3]
    for i in ascending:
        code = reflect_column(code, radices, i)
    print('flipped code')
    pretty_print(code, radices, n)
    result = []

    # calculate start location
    right = calculate_start_direction(code[1], radices, n)
    if right: row, col = 0,1
    else: row, col = 0,0

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

# input: gray code and n as decimal
# output: an array of the col numbers that are in an ascending sequence
# TODO; consolidate??
def in_bottom_ascending_sequence(radices: List[int], n: int):
    out = []

    # find last number ending in 0 in code less than n
    last_zero = []
    for i in range(n-1, 0, -1):
        radix_n = decimal_to_radix(radices, i)
        if radix_n[len(radix_n)-1] == 0:
            last_zero = radix_n
            break
    # loop through last zero and tally number sums
    # if the sum is even, the col is ascending
    col_sum = 0
    for i, num in enumerate(last_zero):
        if col_sum % 2 == 0 and 1 < i < len(last_zero) - 1:
            out.append(i)
        col_sum += num

    # col_sum = 0
    # for i, num in enumerate(last_zero):
    #     if col_sum % 2 == 1 and 0 < i < len(last_zero)-1:
    #         out.append(i)
    #     col_sum += num

    return out

# input: gray code and n as decimal number
# output: if the gray code should start going right or left
def calculate_start_direction(code: List[List[int]], radices: List[int], n: int):
    count = 0

    # iterate over numbers ending in 0 at bottom of code
    for num in code[::-1]:
        if num[len(num)-1] != 0: break
        elif radix_to_decimal(radices, num) < n:
            count += 1
    if count % 2 == 1: return True
    else: return False