from typing import List
from radix_operations import *

#####################################################
#               GRAY CODE PRINTING                  #
#####################################################

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
            print(''.join(decimal_to_letter(s) for s in num))
    print()

# input: gray code radix as a list
# output: string of gray code radices formatted
def pretty_print_radix(radices: List[int]) -> str:
    out = '(' + str(radices[0])
    for r in radices[1:]:
        out += ', ' + str(r)
    out += ')'
    return out