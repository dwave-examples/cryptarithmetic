# Cryptarithmetic example
Cryptarithmetic puzzles are logical puzzles where the goal is to have unique assignments of digits to letters,
such that the mathematical expression holds true.
This example focuses on puzzles in base 10, thus a puzzle submitted may have no more than 10 letters total.

![example puzzle](/images/cryptarithmetic_ex.png)

To run this example, first upload a text file under the puzzle_files folder.
For simplicity and to establish convention, ensure all letters are capitalized.

# Usage
On the command line in the main directory, run:

`python cryptarithm.py "folder_in_root/your_file.txt"`

For example, to submit the problem in the image above your text file would look like:
SEND + MORE = MONEY

# Code overview
There are a few constraints used in formulating this problem:
* minimize difference between left-hand side and right-hand side of equation (minimum of zero).
* assignments of digits to letters must be unique (hence upper bound of 10 total letters in base 10).
* scaling can help the solver arrive at an optimal solution for larger problems with large energy scales.

# References
Wiki page on [verbal arithmetic](https://en.wikipedia.org/wiki/Verbal_arithmetic).

# License
Released under the Apache License 2.0. See [license](license) here.
