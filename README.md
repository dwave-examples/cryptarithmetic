# Cryptarithmetic Addition
[Cryptarithmetic puzzles](https://en.wikipedia.org/wiki/Verbal_arithmetic) are logical puzzles where the 
goal is to have unique assignments of digits to letters, such that the mathematical expression holds true.
This demo only runs with addition puzzles.

# Usage
To run this example, execute:
```
python cryptarithm.py path/to/your/file.txt
```

For simplicity and to establish convention, ensure all letters are capitalized,
that the puzzle be written on the first line of the file, and that no more than 10 unique letters are used in total.

For example:
```
python cryptarithm.py puzzle_files/example1.txt
```

Could produce:
```
Solution found for SEND + MORE = MONEY, 9567 + 1085 = 10652
```

There are three puzzle files provided in the `puzzle_files` directory.
If no puzzle file is specified, `puzzle_files/example1.txt` is used by default.

# Code Overview
There are three constraints used in formulating this problem:
1. Minimize the difference between squares of left-hand side and right-hand side of equation (minimum of zero).
2. Assignments of digits to letters must be unique, thus a puzzle may contain no more than 10 unique letters.
3. The first letter must be non-zero, unless the puzzle contains one letter long components.

# Code Specifics
Puzzle files containing larger words are generally harder for this to solve.
Scaling can help the solver arrive at an optimal solution for larger problems with large energy scales.

# References
Wiki page on [verbal arithmetic](https://en.wikipedia.org/wiki/Verbal_arithmetic).

# License
Released under the Apache License 2.0. See [license](LICENSE) here.
