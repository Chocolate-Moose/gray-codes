from radix_operations import *
from typing import List

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
# output: gray code, but with all numbers ending in 0 moved to the bottom
def move_zeros_to_bottom(code: List[List[int]]) -> List[List[int]]:
    result = []

    # move
    for num in code[::-1]:
        if num[len(num)-1] == 0: result.append(num)
        else: result.insert(0, num)

    return result

# input: tuple of radices
# output: two gray code columns, one with 0 and one with 1 in front
def generate_entire_reflected_code(radices: List[int]) -> List[List[List[int]]]:
    code = generate_reflected_code(radices)
    code = move_zeros_to_bottom(code)
    # prepend 0 and 1 to all numbers
    left = [[0] + num for num in code]
    right = [[1] + num for num in code]

    return [left, right]

# input: gray code as list of lists
# output: return gray code as strings, with letters for numbers > 10
def pretty_print(code: List[List[List[int]]], radices=[2,4,5], n=10000) -> None:
    # columns for gray code
    if len(code) == 2:
        for i in range(len(code[0])): 
            print(''.join(decimal_to_letter(s) for s in code[0][i]), end ="    ")
            # skip number if it's in knockout group
            if radix_to_decimal(radices, code[1][i]) < n: print(''.join(decimal_to_letter(s) for s in code[1][i]))
            else: print()
    # finished gray code
    else: 
        for num in code:
            print(''.join(decimal_to_letter(s) for s in code[0][i]), end ="    ")

# input: gray code radix as a list
# output: string of gray code radices formatted
def pretty_print_radix(radices: List[int]) -> str:
    out = '(' + str(radices[0])
    for r in radices[1:]:
        out += ', ' + str(r)
    out += ')'
    return out