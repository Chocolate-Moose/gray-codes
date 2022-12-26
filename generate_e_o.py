from typing import List
from radix_operations import *
from common import *
from generate import *
from printing import *

def generate_entire_reflected_code_eo(radices: List[int]) -> List[List[List[int]]]:
    code = generate_reflected_code(radices)
    code = move_digit_to_bottom(code, len(radices) - 1, radices[len(radices)-1]-1)
    # prepend 0 and 1 to all numbers
    left = [[0] + num for num in code]
    right = [[1] + num for num in code]

    return [left, right]

# input: radices, entire reflected gray code, n as decimal number
# output: dense, cyclic gray code for radices up to n
def generate_threaded_code_eo(radices: List[int], code: List[List[List[int]]], n: int):
    # check if n too big or small
    largest = 1
    for radix in radices: largest *= radix
    if n < 0 or n > largest - 1:
        print('n is out of range of the radix')
        return []

    # special case where inner ring isn't in yet
    half = largest / radices[0]
    if n < half + radices[len(radices)-1]-1: 
        result = inner_ring_case(radices, code, n)
        return result

    # see if we need to flip
    ascending = radices_to_reflect(radices, n)
    print('flipped', ascending)

    for i in ascending:
        code = reflect_column(code, radices, i)
    # pretty_print(code, radices, n)
    result = []

    # calculate start location
    right = calculate_start_direction_eo(code[1], radices, n)
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

# input: gray code and n as decimal number
# output: if the gray code should start going right or left underneath the arm
# this is where the threading starts on the top after the top ring bit
# true = go left, false = go right
def calculate_start_direction_eo(code: List[List[int]], radices: List[int], n: int):
    count = 0
    largest = radices[len(radices)-1]-1

    # iterate over numbers ending in 4 at bottom of code
    for num in code[::-1]:
        if num[len(num)-1] != largest: break
        elif radix_to_decimal(radices, num) < n:
            count += 1
    if count % 2 == 1: return True
    else: return False

# the new version of in_bottom_ascending sequence
# input: radices and n
# output: what radices need to be reflected in a list
def radices_to_reflect(radices: List[int], n: int) -> List[int]:
    # get largest number in code
    largest = decimal_to_radix(radices, n - 1)
    col_sum = 0
    out = []

    # cumulative sum to determine which columns to flip
    # add 1 to account for flips in even radices, if even col is descending
    # ignore first and last cols - they will never flip
    for i, num in enumerate(largest):
        if 1 < i < len(largest) - 1:
           if col_sum % 2 == 0: 
                out.append(i)
                if radices[i] % 2 == 0: col_sum += 1
        col_sum += num
    return out

def inner_ring_case(radices: List[int], code: List[List[List[int]]], n: int):
    # get the 2 of 102 for example
    pos_line = decimal_to_radix(radices, n)[len(radices)-1] - 1

    # a nifty trick is to reverse the radices after 2 bc generating code
    # varies the rightmost one the fastest
    radices_new = [2] + radices[1:][::-1]
    bottom = generate_reflected_code(radices_new)
    bottom = [i for i in bottom if i[0] >= pos_line]

    # reverse the order of radices and prepend 0
    for i in bottom:
        i.append(0)
        i.reverse()

    # teeth - take all numbers in top above the line
    top = [i for i in code[0] if i[len(i)-1] < pos_line]

    bottom.reverse()
    top.extend(bottom)

    # add in the right side
    for i in range(top[len(top)-1][len(radices)-1], -1, -1):
        hi = [1] + [0] * (len(radices) - 2) + [i]
        top.append(hi)
    
    return top
