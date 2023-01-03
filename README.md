# Gray Codes

### Overview
I did research on determining a cyclic mixed-radix dense Gray code when the most significant radix is 2, at least one radix is odd, and the number of codewords is odd. The more detailed report for my findings can be viewed [here](https://docs.google.com/document/d/1xSOu0kItTyFQZMd0H290tuELMLKnjScKZCv5OtwPfIs/edit?usp=sharing). 

This is a Python implementation of my solutions.

### Usage
##### Inputs
This program takes two command line inputs: the radices and an optional n.  If a value of n is provided, a dash needs to be placed before the n.

##### Outputs
This program will print out a cyclic, mixed-radix dense Gray code for the given radices and n.  If the radices or n are not supported or incorrect, an error message will be printed.

If no value of n is provided, the program will print whether it generated a valid solution for all possible values of n.

##### Example
`python3 main.py 2 5 8 - 43` will print the correct Gray code for radices `(2,5,8)` where `n=43`.

`python3 main.py 2 7 13 5 - 501` will print the correct Gray code for radices `(2,7,13,5)` where `n=501`.

`python3 main.py 2 5 5` will print the the correctness of the generated Gray code for radices `(2,5,5)` from `n=27` to `n=49`.

### Implementation
Each gray code is stored as a list of codewords.  Additionally, each codeword is stored as a list, where each value in the list is the value of the codeword at that given radix.  All values are stored as integers, and if the value in a given radix is greater than 9, the value is converted to a letter when the gray code is printed.