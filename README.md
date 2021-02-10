[![Linux/Mac/Windows build status](
  https://circleci.com/gh/dwave-examples/cryptarithmetic.svg?style=svg)](
  https://circleci.com/gh/dwave-examples/cryptarithmetic)

# Cryptarithmetic Addition
[Cryptarithmetic puzzles](https://en.wikipedia.org/wiki/Verbal_arithmetic) are logical puzzles where the 
goal is to have unique assignments of digits to letters, such that the mathematical expression holds true.
This demo only runs with addition puzzles.

# Usage
To run this demo, execute:
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
Objective and constraints considered in problem formuation:
1. Minimize the difference between squares of left-hand side and right-hand side of equation.
2. Assignments of digits to letters must be unique, thus a puzzle may contain no more than 10 unique letters.
3. The first letters must be assigned a non-zero digit, unless the puzzle contains one-letter words.

# Code Specifics
Puzzles become harder to solve with increasing word length. For large problems - which have high energy scales - scaling
down the biases can help the solver arrive at an optimal solution. Due to the probabilistic nature of the solver, you
may have to run the puzzle a few times to find a solution, provided one exists.

# References
Wiki page on [verbal arithmetic](https://en.wikipedia.org/wiki/Verbal_arithmetic).

# License
Released under the Apache License 2.0. See [license](LICENSE) here.
