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
import numpy as np

example_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(example_dir)

from cryptarithm import LetterVariable, build_dqm
from utilities import update_coefficient_map_and_first_letter_set

class TestCryptarithm(unittest.TestCase):
    """Test functionality of classes/methods for the example.

    """
    def test_letter_variable_class(self):
        first_letter = LetterVariable(name="var", 
                                      coefficient=7, 
                                      first_letter=True)

        not_first_letter = LetterVariable(name="another_var", 
                                          coefficient=42, 
                                          first_letter=False)

        assert first_letter.domain == tuple(range(1,10))
        assert not_first_letter.domain == tuple(range(10))

    def test_build_dqm(self):

        variable_list = [
            LetterVariable("A", 1),
            LetterVariable("B", 1),
            LetterVariable("C", -1)
        ]

        coeff_map = {"A":1, "B":1, "C":-1}

        dqm = build_dqm(variable_list, coeff_map)

        scale_factor = 1/(2**(len(coeff_map)))

        assert dqm.num_variables() == 3
        for var in variable_list:
            for case in var.domain:
                assert dqm.get_linear_case(var.name, case) == scale_factor*(coeff_map[var.name]*case)**2