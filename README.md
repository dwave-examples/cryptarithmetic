# Cryptarithmetic Addition
[Cryptarithmetic puzzles](https://en.wikipedia.org/wiki/Verbal_arithmetic) are logical puzzles where the 
goal is to have unique assignments of digits to letters, such that the mathematical expression holds true.
This demo only runs with addition puzzles.

# Usage
To run this example, simply provide a path to the puzzle text file.
For simplicity and to establish convention, ensure all letters are capitalized,
and that the puzzle be written on the first line of the file.

On the command line in the main directory, run:
`python cryptarithm.py path/to/your/file.txt`

For example:
`python cryptarithm.py puzzle_files/example1.txt`

Could produce:
`Solution found for SEND + MORE = MONEY, 9567 + 1085 = 10652`

There are three puzzle files provided
* `puzzle_files/example1.txt`
* `puzzle_files/example2.txt`
* `puzzle_files/example3.txt`

# Code Overview
There are a few constraints used in formulating this problem:
1. Minimize difference between left-hand side and right-hand side of equation (minimum of zero).
2. Assignments of digits to letters must be unique, thus a puzzle may contain no more than 10 unique letters.
3. The first letter must be non-zero, unless the puzzle contains one letter long components.

# Code Specifics
Puzzle files containing larger words are generally harder for this to solve.
Scaling can help the solver arrive at an optimal solution for larger problems with large energy scales.

# References
Wiki page on [verbal arithmetic](https://en.wikipedia.org/wiki/Verbal_arithmetic).

# License
Released under the Apache License 2.0. See [license](LICENSE) here.
