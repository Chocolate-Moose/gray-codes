import sys

from generate import *
from common import *
from validation import *
from generate_e_o import *
from printing import *

#####################################################
#                GRAY CODE TESTING                  #
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

    # check for a valid n
    total = 1
    for num in radix[1:]: total *= num

    if n != 0 and (n < total or n > total * 2 or n % 2 == 0):
        print('the value of n given is not valid')
        return

    # count odd radices
    odd = sum(1 if x % 2 == 1 else 0 for x in radix)

    # all odd radices ex: 2,5,7,13
    if n > 0 and odd == len(radix) - 1:
        generate_gray_code(radix, n, True, True)
    # last digit is odd
    elif n > 0 and radix[len(radix) - 1] % 2 == 1:
        generate_gray_code(radix, n, False, True)
    # no n given, test all cases
    elif n == 0:
        # end is actually -1 but the range takes care of this
        end = total * 2

        # keep n odd for all odd
        if total % 2 == 1: total += 2
        else: total += 3

        works = True

        for i in range(total, end, 2): 
            # TODO: there is sketchy logic here for other cases
            all_odd = odd = len(radix) - 1
            valid = generate_gray_code(radix, i, all_odd, False)
            works = works & valid
        print('all cases:', works)

    # all other cases
    else:
        the_code = generate_reflected_code(radix)
        the_code = generate_entire_reflected_code(the_code)

        print(pretty_print_radix(radix), n)
        pretty_print(the_code, radix, n)
        print('the functionality for these radices is not supported')

def generate_gray_code(radix, n, all_odd, to_print):
    the_code = generate_entire_reflected_code(radix) if all_odd else generate_entire_reflected_code_eo(radix)
    print(pretty_print_radix(radix), n)
    if to_print: pretty_print(the_code, radix, n)

    new_code = generate_threaded_code(radix, the_code, n) if all_odd else generate_threaded_code_eo(radix, the_code, n)
    if to_print: pretty_print(new_code)

    valid = valid_codewords(radix, new_code, n) and valid_gray_code(radix, new_code)
    print(valid)
    print(' ')

    return valid

driver()