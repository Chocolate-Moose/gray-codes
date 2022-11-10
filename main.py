import copy
import sys

from generate import *
from common import *
from validation import *
from generate_e_o import *

#####################################################
#                GRAY CODE TESTING                  #
#####################################################
def driver():
    # input error checking
    if len(sys.argv) < 4:
        print('incorrect number of command line inputs')
        print('expected radices and then n, ex: 2 5 7 37')
        return

    # read in radices and n from the command line
    radix = []
    for num in sys.argv[1:len(sys.argv) - 1]:
        radix.append(int(num))
    n = int(sys.argv[len(sys.argv) - 1])

    # check for a valid n
    total = 1
    for num in radix[1:]: total *= num

    if n < total or n > total * 2 or n % 2 == 0:
        print('the value of n given is not valid')
        return

    # count odd radices
    odd = sum(1 if x % 2 == 1 else 0 for x in radix)

    # all odd radices ex: 2,5,7,13
    if odd == len(radix) - 1:
        the_code = generate_entire_reflected_code(radix)
        print(pretty_print_radix(radix), n)

        new_code = generate_threaded_code(radix, the_code, n)
        pretty_print(new_code)

        valid = valid_codewords(radix, new_code, n) and valid_gray_code(radix, new_code)
        print(valid)
        print(' ')

    elif len(radix) and radix[1] % 2 == 0 and odd == 1:
        the_code = generate_entire_reflected_code_eo(radix)
        print(pretty_print_radix(radix), n)
        pretty_print(the_code, radix, n)

    # all other cases
    else:
        print('the functionality for these radices is not supported')

driver()