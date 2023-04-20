from typing import List
from radix_operations import *
from common import *
from generate_all_odd import *
from printing import *

def inner_ring_case(radices: List[int], code: List[List[List[int]]], n: int):
    # get the 2 of 102 for example
    pos_line = decimal_to_radix(radices, n)[len(radices)-1] - 1

    # a nifty trick is to reverse the radices after 2 bc generating code
    # varies the rightmost one the fastest
    # radices_new = [radices[0]] + radices[1:][::-1]
    # bottom = generate_reflected_code(radices_new)
    # bottom = [i for i in bottom if i[0] >= pos_line]
    first_even = 0
    for i, radix in enumerate(radices):
        # skip the leading 2
        if radix % 2 == 0 and i != 0: first_even = i 
    
    # leading 2, first even, last digit, hide everything else
    radices_new = [radices[0]] + [radices[first_even]] + [radices[len(radices)-1]] + radices[first_even+1:len(radices)-1]
    bottom = generate_reflected_code(radices_new)
    # bottom = [i for i in bottom if i[0] >= pos_line]

    # reverse the order of radices and prepend 0
    for i in bottom:
        i.append(0)
        i.reverse()

    # teeth - take all numbers in top above the line
    radices_top = [radices[0]] + radices[len(radices)-2:] + radices[1:len(radices)-2][::-1]
    top = generate_reflected_code(radices_top)
    top = [i for i in top if i[1] < pos_line]

    # reorder the top
    for i in top:
        i.append(0)
        i.reverse()
        i[len(i)-1], i[len(i)-2] = i[len(i)-2], i[len(i)-1]

    bottom.reverse()
    top.extend(bottom)

    # add in the right side
    for i in range(top[len(top)-1][len(radices)-1], -1, -1):
        hi = [1] + [0] * (len(radices) - 2) + [i]
        top.append(hi)
    
    pretty_print(top, radices, n)
    return top
