import sys

from generate import *
from common import *
from validation import *
from generate_e_o import *
from printing import *

#####################################################
#                GRAY CODE TESTING                  #
#####################################################
# TODO; add option for no n to be input, which runs all the cases
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
        pretty_print(the_code, radix, n)

        new_code = generate_threaded_code(radix, the_code, n)
        pretty_print(new_code)

        valid = valid_codewords(radix, new_code, n) and valid_gray_code(radix, new_code)
        print(valid)
        print(' ')
    # last digit is odd
    elif radix[len(radix) - 1] % 2 == 1:
        the_code = generate_entire_reflected_code_eo(radix)
        print(pretty_print_radix(radix), n)
        pretty_print(the_code, radix, n)

        new_code = generate_threaded_code_eo(radix, the_code, n)
        # pretty_print(new_code)
        
        # validate code
        valid = valid_codewords(radix, new_code, n) and valid_gray_code(radix, new_code)
        print(valid)
        print(' ')

    # all other cases
    else:
        the_code = generate_reflected_code(radix)
        the_code = generate_entire_reflected_code(the_code)

        print(pretty_print_radix(radix), n)
        pretty_print(the_code, radix, n)
        print('the functionality for these radices is not supported')

def test_all_for_radix(radix):
    start = 1
    for num in radix[1:]: start *= num
    # end is actually -1 but the range takes care of this
    end = start * 2
    start += 3

    works = True

    for i in range(start, end, 2): 
        the_code = generate_entire_reflected_code_eo(radix)
        print(pretty_print_radix(radix), i)
        # pretty_print(the_code, radix, n)

        new_code = generate_threaded_code_eo(radix, the_code, i)
        # pretty_print(new_code)
        
        # validate code
        valid = valid_codewords(radix, new_code, i) and valid_gray_code(radix, new_code)
        print(valid)
        works = works & valid
        print(' ')
    print('all cases:', works)

test_all_for_radix([2,8,15])

# driver()