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
import dimod
from cryptarithm import ModelVariable, build_cqm
from utilities import update_coefficient_map_and_first_letter_set

class TestCryptarithmComponents(unittest.TestCase):
    """Test functionality of classes/methods for the example.

    """
    def test_model_variable_class(self):
        first_letter = ModelVariable(label="X", 
                                     coefficient=7, 
                                     first_letter=True)

        not_first_letter = ModelVariable(label="Y", 
                                         coefficient=42, 
                                         first_letter=False)

        self.assertEqual(first_letter.lower_bound, 1)
        self.assertEqual(first_letter.upper_bound, 9)
        self.assertEqual(not_first_letter.lower_bound, 0)
        self.assertEqual(not_first_letter.upper_bound, 9)
        self.assertIsInstance(first_letter.var, dimod.QuadraticModel)
        self.assertIsInstance(not_first_letter.var, dimod.QuadraticModel)

    def test_build_cqm(self):

        variables = [
            ModelVariable("A", 1),
            ModelVariable("B", 1),
            ModelVariable("C", -1),
            ModelVariable("D", -1)
        ]

        cqm = build_cqm(variables)

        self.assertEqual(
            cqm.num_variables(), len(variables) + (len(variables) * (len(variables)-1)/2)
        )
