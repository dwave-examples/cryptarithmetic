[![Open in Leap IDE](
  https://cdn-assets.cloud.dwavesys.com/shared/latest/badges/leapide.svg)](
  https://ide.dwavesys.io/#https://github.com/dwave-examples/cryptarithmetic)
[![Linux/Mac/Windows build status](
  https://circleci.com/gh/dwave-examples/cryptarithmetic.svg?style=shield)](
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
Constraints considered in problem formuation:
1. The first constraint is that the left-hand side must be equal to the right-hand side.
2. Assignments of digits to letters must be unique, thus a puzzle may contain no more than 10 unique letters. This is expressed as a series of encoded not-equal constraints.
3. The first letters must be assigned a non-zero digit, unless the puzzle contains one letter words.

# References
Wiki page on [verbal arithmetic](https://en.wikipedia.org/wiki/Verbal_arithmetic).

# License
Released under the Apache License 2.0. See [license](LICENSE) here.
