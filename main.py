import sys

from generate_all_odd import generate_all_odd
from generate_ending_odd import generate_ending_odd
from generate_ending_even import generate_ending_even
from validation import *
from printing import *

#####################################################
#              GRAY CODE DRIVER CODE                #
#####################################################
def driver():
    # input error checking
    if len(sys.argv) < 4:
        print('incorrect number of command line inputs')
        print('expected radices and then optional n, ex: 2 5 7 37 or 2 5 5')
        return

    # read in radices and n from the command line
    radix = []
    read_n = False
    n = 0
    for num in sys.argv[1:]:
        if read_n: n = int(num)
        else:
            if num == '-': read_n = True
            else: radix.append(int(num))

    # check for when I forget the dash
    if radix[len(radix)-1] > 20: 
        print('did you forget the dash')
        return

    # check for a valid n
    total = 1
    for num in radix[1:]: total *= num

    if n != 0 and (n < total or n > total * 2 or n % 2 == 0):
        print('the value of n given is not valid')
        return

    # categorize radices
    category = categorize_radices(radix)

    # case where n was given as cli
    if n > 0: generate_gray_code(radix, n, category)
    # loop through all possible n
    else: 
        # end is actually -1 but the range takes care of this
        end = total * 2

        # keep n odd for all odd
        if total % 2 == 1: total += 2
        else: total += 3

        works = True

        for i in range(total, end, 2): 
            valid = generate_gray_code(radix, i, category)
            works = works & valid
        print('all cases:', works)

def generate_gray_code(radix: List[int], n: int, category: str):
    # call correct generate based on category
    if category == "all_odd": new_code = generate_all_odd(radix, n)
    elif category == "ending_odd": new_code = generate_ending_odd(radix, n)
    elif category == "ending_even": new_code = generate_ending_even(radix, n)
    else: 
        print('something went wrong, invalid category')
        new_code = []

    print(pretty_print_radix(radix), n)
    # check for validity of code
    valid = valid_codewords(radix, new_code, n) and valid_gray_code(radix, new_code)
    print(valid)
    print(' ')

    return valid

# categories radices as 1 of 3 cases: all_odd, ending_odd, ending_even
def categorize_radices(radices:List[int]) -> str:
    # count odd radices
    odd = sum(1 if x % 2 == 1 else 0 for x in radices)

    if odd == len(radices) - 1: return "all_odd"
    elif radices[len(radices)-1] % 2 == 1: return "ending_odd"
    else: return "ending_even"

driver()