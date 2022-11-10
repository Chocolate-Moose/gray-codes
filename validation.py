from radix_operations import *

#####################################################
#              GRAY CODE VALIDATION                 #
#####################################################

# input: radix tuple and gray code as a list of lists
# output: boolean if code has all of the correct numbers
#         (doesn't check gray code property)
def valid_codewords(radices, code, n):
    # change array into set
    # convert list for each codeword into string
    code_nums = set()
    for num in code:
        code_nums.add(''.join(str(i) for i in num))

    # check length of code
    if n != len(code_nums):
        print('wrong number of numbers in code')
        return False

    # search for each number under n in code
    for i in range(n):
        codeword = decimal_to_radix(radices, i)
        codeword = ''.join(str(c) for c in codeword)
        if codeword not in code_nums:
            print(codeword, 'not in gray code')
            return False
    return True

# input: radix tuple and gray code as a list of lists
# output: boolean if code fulfills gray code property
def valid_gray_code(radices, code):
    for i, first in enumerate(code):
        # check cyclic property
        if i == len(code) - 1:
            valid = valid_neighbors(radices, first, code[0])
            if not valid:
                print(first, code[0], 'not valid neighbors with given radices')
                return False
        else:
            valid = valid_neighbors(radices, first, code[i+1])
            if not valid:
                print(first, code[i+1], 'not valid neighbors with given radices')
                return False
    return True

# input: radix tuple and two adjacent numbers in gray code as lists
# output: boolean if two numbers satisfy gray code property
def valid_neighbors(radices, first, second):
    # codewords not same length
    if len(first) != len(second): return False

    # codewords not same length as radix
    if len(first) != len(radices): return False

    diff = 0
    # loop through every digit and compare
    for i, (one, two) in enumerate(zip(first, second)):
        # the same
        if one == two: continue
        # off by one
        if abs(one-two) == 1:
            diff += 1
            continue
        # wrap around radix
        if (one == 0 and two == radices[i]-1) or (two == 0 and one == radices[i]-1):
            diff += 1
        # too far off, wrong
        else: return False

    if diff == 1: return True
    else: return False