from typing import List
#####################################################
#          RADIX CALCULATION OPERATIONS             #
#####################################################

# input: a radix tuple and a decimal number
# output: the number converted to the given radix as an array
def decimal_to_radix(radices: List[int], num: int):
    # check if number too big or small
    largest = 1
    for radix in radices: largest *= radix
    if num < 0 or num > largest-1:
        print('num is out of range of the radix')
        return -1

    result: List[int] = []
    for base in radices[::-1]:
        result.insert(0, num % base)
        num = num // base
    return result

# input: a radix tuple and a mixed-radix number as list
# output: the number converted to decimal
def radix_to_decimal(radices: List[int], num: List[int]) -> int:
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
def decimal_to_letter(num) -> str:
    if num >= 10: return chr(num + 87)
    else: return str(num)