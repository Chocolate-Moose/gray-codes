import copy
#####################################################
#          RADIX CALCULATION OPERATIONS             #
#####################################################

# input: a radix tuple and a decimal number
# output: the number converted to the given radix as an array
def decimal_to_radix(radices, num):
    # check if number too big or small
    largest = 1
    for radix in radices: largest *= radix
    if num < 0 or num > largest-1:
        print('num is out of range of the radix')
        return -1

    result = []
    for base in radices[::-1]:
        result.insert(0, num % base)
        num = num // base
    return result

# input: a radix tuple and a mixed-radix number as list
# output: the number converted to decimal
def radix_to_decimal(radices, num):
    # calculate value of each digit place
    values = [1]
    for radix in radices[:0:-1]:
        values.insert(0, values[0] * radix)

    result = 0
    for i, digit in enumerate(num):
        result += digit * values[i]
    return result

# input: decimal number
# output: if number >= 10, the corresponding letter
#         else, the number as a string
def decimal_to_letter(num):
    if num >= 10: return chr(num + 87)
    else: return str(num)

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

#####################################################
#                  GRAY CODE COMMON                 #
#####################################################

# input: a radix tuple
# output: list of the reflected gray code as arrays without the 0/1 at the front
def generate_reflected_code(radices):
    old_result = []
    new_result = []

    # compute gray code for rightmost radix
    for i in range(radices[len(radices)-1]):
        old_result.append([i])

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
def move_zeros_to_bottom(code):
    result = []

    # move
    for num in code[::-1]:
        if num[len(num)-1] == 0: result.append(num)
        else: result.insert(0, num)

    return result

# input: tuple of radices
# output: two gray code columns, one with 0 and one with 1 in front
def generate_entire_reflected_code(radices):
    code = generate_reflected_code(radices)
    code = move_zeros_to_bottom(code)
    # prepend 0 and 1 to all numbers
    left = [[0] + num for num in code]
    right = [[1] + num for num in code]

    return [left, right]

# input: gray code as list of lists
# output: return gray code as strings, with letters for numbers > 10
def pretty_print(code):
    out = []
    for num in code:
        out.append(''.join(decimal_to_letter(s) for s in num))
    return out
#####################################################
#           GRAY CODE GENERATION ALL ODD            #
#####################################################

# input: radices, entire reflected gray code, n as decimal number
# output: dense, cyclic gray code for radices up to n
def generate_threaded_code(radices, code, n):
    # check if n too big or small
    largest = 1
    for radix in radices: largest *= radix
    if n < 0 or n > largest - 1:
        print('n is out of range of the radix')
        return []

    # see if we need to flip
    ascending = in_bottom_ascending_sequence(radices, n)
    for i in ascending:
        code = reflect_column(code, radices, i)

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
def in_bottom_ascending_sequence(radices, n):
    out = []

    # find last number ending in 0 in code less than n
    last_zero = -1
    for i in range(n-1, 0, -1):
        radix_n = decimal_to_radix(radices, i)
        if radix_n[len(radix_n)-1] == 0:
            last_zero = radix_n
            break

    # loop through last zero and tally number sums
    # if the sum is even, the col is ascending
    col_sum = 0
    for i, num in enumerate(last_zero):
        if col_sum % 2 == 0 and 0 < i < len(last_zero)-1:
            out.append(i)
        col_sum += num

    return out

# input: entire gray code as list of lists, radices as tuple
# output: code, but with the given column reflected
#         columns are counted from the left, 0 indexed
def reflect_column(code, radices, col_num):
    out = copy.deepcopy(code)
    for i in range(len(code[0])):
        out[0][i][col_num] = radices[col_num] - code[0][i][col_num] - 1
        out[1][i][col_num] = radices[col_num] - code[1][i][col_num] - 1

    return out

# input: gray code and n as decimal number
# output: if the gray code should start going right or left
def calculate_start_direction(code, radices, n):
    count = 0

    # iterate over numbers ending in 0 at bottom of code
    for num in code[::-1]:
        if num[len(num)-1] != 0: break
        elif radix_to_decimal(radices, num) < n:
            count += 1
    if count % 2 == 1: return True
    else: return False

#####################################################
#           GRAY CODE GENERATION ONE ODD            #
#####################################################
# input: radices and n as decimal
# output: the right side of the gray code (1__) as a list of lists
def generate_right_path(radices, n):
    code = generate_reflected_code(radices)
    right = [[1] + num for num in code]

    # flip if in descending sequence
    if in_right_descending_sequence(radices, n):
        flip_right_column(right, radices)

    # calculate how much we need to return with n
    mult = 1
    for num in radix[1:]:
        mult *= num

    return right[:n-mult]

# input: entire gray code, radices as tuple
# output: changes given code to reflect the rightmost column
def flip_right_column(code, radices):
    col_num = len(radices)-1
    for i in range(len(code)):
        code[i][col_num] = radices[col_num] - code[i][col_num] - 1

# input: radices and n as decimal
# output: whether the sequence ends in a descending sequence
#         in the regular reflected gray code
# todo: combine with ascending sequence code??
def in_right_descending_sequence(radices, n):
    # it will be descending sequence if this is odd
    # might need to subtract the 1 for 4+ radices
    if (n - 1) // radices[len(radices)-1] % 2 == 1:
        return True
    return False

# input: radices, n as decimal, ring number (020)
# output: the outer left cycle
def generate_outer_left_cycle(radices, ring_num):
    code = generate_reflected_code(radices)
    code = [[0] + num for num in code]

    code = move_zeros_to_bottom(code)
    result = []

    for num in code:
        # if we're in the right rings
        if num[1] >= ring_num:
            result.append(num)

    return result

# input: radices and n as decimal, start and end numbers of right path as lists
# output: the left side of the gray code path
def generate_left_path(radices, start, end):
    # make the right numbers
    right = [i for i in range(radices[len(radices)-1])]

    # put the last number in front if gray code is reflected
    if start[len(start)-1] == radices[len(radices)-1]-1:
        right.insert(0, right.pop(len(right)-1))

    # make the columns
    grid = []
    ring = end[1]

    for i in right:
        grid.append([])
        for j in range(ring+1):
            grid[len(grid)-1].append([0, j, i])

    # thread through the columns
    result = []
    arm = []
    right = True
    skip_right = False
    for row in grid:
        # need to skip rightmost col
        if row[len(row)-1][1:] == end[1:]: skip_right = True
        if right:
            # add everything but last col, which we add to arm
            if skip_right:
                result.extend(row[:len(row)-1])
                arm.append(row[len(row)-1])
            else: result.extend(row)
        else:
            if skip_right:
                result.extend(row[len(row)-2::-1])
                arm.append(row[len(row)-1])
            else: result.extend(row[::-1])

        right = not right

    result.extend(arm[::-1])
    return result

# input: radices and n as decimal, start and end numbers of right path
#        special case while working through inner ring
# output: the left side of the gray code path
# todo: possibly combine with other left path code above?
def generate_left_path_special(radices, end):
    # make the right numbers
    right = [i for i in range(radices[len(radices) - 1])]

    # flip all numbers after 0 bc going counterclockwise
    right[1:len(right)] = right[len(right) - 1:0:-1]

    # made 2 col grid of inner two rings
    grid = []
    ring = 1

    for i in right:
        grid.append([])
        for j in range(ring + 1):
            grid[len(grid) - 1].append([0, j, i])

    # thread through the columns
    result = []
    arm = []
    right = True                # direction we are traveling in
    skip_left = False
    for row in grid:
        # need to skip leftmost col
        if row[0][1:] == end[1:]: skip_left = True

        # going down right row
        if skip_left:
            result.append(row[1])
            arm.append(row[0])
            continue

        # alternate adding whole rows
        if right: result.extend(row)
        else: result.extend(row[::-1])

        right = not right

    result.extend(arm[::-1])
    return result

# input: radices and n as decimal
# output: the three parts of the gray code
def generate_three_parts(radices, n):
    right = generate_right_path(radices, n)
    ring = decimal_to_radix(radices, n-1)[1]
    if ring == 0: ring = 1
    outer_cycle = generate_outer_left_cycle(radices, ring+1)

    # special case for inner ring path on left
    if right[len(right)-1][1] == 0: inner_cycle = generate_left_path_special(radices, right[len(right)-1])
    else:inner_cycle = generate_left_path(radices, right[0], right[len(right)-1])

    inner_cycle.extend(right[::-1])

    result = combine_cycles(inner_cycle, outer_cycle)

    return result

# input: inner and outer cycle
# output: gray code
def combine_cycles(inner, outer):
    # no need to combine
    if len(outer) == 0:
        return inner

    result = []
    # loop through outer ring and look for connection to inner
    for i in range(len(outer)-1):
        one = outer[i]
        two = outer[i+1]

        # find numbers in inner cycle
        index_one = inner.index([one[0], one[1]-1, one[2]])
        index_two = inner.index([two[0], two[1]-1, two[2]])

        # numbers are next to each other, we can connect
        if index_one - index_two == 1:
            result = inner[:index_two+1] + outer[i+1:] + outer[:i+1] + inner[index_one:]
            break

        if index_two - index_one == 1:
            result = inner[:index_two] + outer[:i+1] + outer[:i:-1] + inner[index_one+1:]
            break

    return result

# input: gray code ast list of lists
# output: gray code, with given columns (0-indexed) swapped
def swap_columns(code, col1, col2):
    for num in code:
        num[col1], num[col2] = num[col2], num[col1]

#####################################################
#                GRAY CODE TESTING                  #
#####################################################
if __name__ == "__main__":
    radix = (2,15,6)

    # calculate boundaries of test and count odd radices
    mult = 1
    odd = 0
    for num in radix:
        mult *= num
        if num % 2 == 1: odd += 1

    # all odd radices ex: 2,5,7,13
    if odd == len(radix) - 1:
        the_code = generate_entire_reflected_code(radix)

        for n in range((int(mult/radix[0])+2) | 1, mult, 2):
            print('N', n)
            new_code = generate_threaded_code(radix, the_code, n)
            valid = valid_codewords(radix, new_code, n) and valid_gray_code(radix, new_code)
            print(valid)
            print(' ')

    # one odd one even ex: 2,7,4 or 2,7,4
    elif odd == 1 and len(radix) == 3:
        for n in range((int(mult/radix[0])+2) | 1, mult, 2):
            print('N', n)

            # middle number odd case
            if radix[1] % 2 == 1: radix = (radix[0], radix[2], radix[1])

            out = generate_three_parts(radix, n)

            # middle number odd case
            if radix[1] % 2 == 1: swap_columns(out, 1, 2)

            valid = valid_codewords(radix, out, n) and valid_gray_code(radix, out)
            print(valid)
            print(' ')

    # all other cases
    else:
        print('the functionality for these radices is not supported')
        print('stay tuned for future implementation')
