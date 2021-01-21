# Copyright 2021 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys, os
import unittest
from unittest.mock import patch
from collections import defaultdict

example_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(example_dir)

from utilities import (parse_problem_file,
                       update_coefficient_map_and_first_letter_set,
                       render_solution)
from cryptarithm import LetterVariable

class TestUtilities(unittest.TestCase):
    """Test functionality of utilities methods.

    """
    coeff_map_test = defaultdict(int)
    first_letters_test = set()

    def test_parse_problem_file(self):
        lhs_list, rhs_list, problem_statement = parse_problem_file("puzzle_files/example1.txt")
        self.assertIn("SEND", lhs_list)
        self.assertIn("MORE", lhs_list)
        self.assertIn("MONEY", rhs_list)
        self.assertEqual("SEND + MORE = MONEY", problem_statement)

    def test_update_coefficient_map_and_first_letter_set(self):
        coeff_map_test = defaultdict(int)
        first_letters_test = set()
        test_list = ["CAT", "DOG"]
        update_coefficient_map_and_first_letter_set(test_list, 1, coeff_map_test, first_letters_test)

        self.assertIn("C", first_letters_test)
        self.assertIn("D", first_letters_test)
        self.assertEqual(coeff_map_test["C"], 100)
        self.assertEqual(coeff_map_test["A"], 10)
        self.assertEqual(coeff_map_test["T"], 1)
        self.assertEqual(coeff_map_test["D"], 100)
        self.assertEqual(coeff_map_test["O"], 10)
        self.assertEqual(coeff_map_test["G"], 1)

    @patch("builtins.print")
    def test_render_solution(self, mock_print):
        var_list = [LetterVariable("A", 1),
                    LetterVariable("B",1),
                    LetterVariable("C", 1)]
        example = "A + B = C"
        lhs_list = ['A', 'B']
        rhs_list = ['C']
        sample_solution = {
            "A":1,
            "B":2,
            "C":3
        }
        render_solution(sample_solution, var_list, lhs_list, rhs_list, example)
        mock_print.assert_called_with("Solution found for {example}, 1 + 2 = 3".format(
            example=example
        ))