from typing import List
from radix_operations import *
from common import *

# input: gray code output by generate_reflected_code
# output: gray code, but with all numbers ending in digit moved to the bottom
def move_digit_to_bottom(code: List[List[int]], n: int) -> List[List[int]]:
    result = []

    # move
    for num in code[::-1]:
        if num[len(num)-1] == n: result.append(num)
        else: result.insert(0, num)

    return result

def generate_entire_reflected_code_eo(radices: List[int]) -> List[List[List[int]]]:
    code = generate_reflected_code(radices)
    code = move_digit_to_bottom(code, radices[len(radices)-1]-1)
    # prepend 0 and 1 to all numbers
    left = [[0] + num for num in code]
    right = [[1] + num for num in code]

    return [left, right]