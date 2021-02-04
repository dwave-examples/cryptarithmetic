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

import argparse
from typing import List
from pprint import pprint
from tqdm import tqdm
from collections import defaultdict
from itertools import combinations
import numpy as np

from dimod import DQM
from dwave.system import LeapHybridDQMSampler
from utilities import parse_problem_file, update_coefficient_map_and_first_letter_set, render_solution

class LetterVariable:
    """Class for holding information about variables in alphametics problems.

    Args:
        name: Variable string id.
        coefficient: Coefficient on variable from formulation.
        first_letter: Whether or not variable is first letter of a word.

    """
    def __init__(self, name:str = None, coefficient:int = 0, first_letter:bool = False):
        self.name = name
        self.coefficient = coefficient
        self.first_letter = first_letter
        if self.first_letter:
            self.domain = tuple(range(1,10))
        else:
            self.domain = tuple(range(10))

    def __repr__(self):
        return "(name: {name}, coefficient: {coeff}, domain: {domain})".format(name=self.name,
                                                                               coeff=self.coefficient,
                                                                               domain=self.domain)


def build_dqm(variable_list: List[LetterVariable], coefficient_map: dict) -> DQM:
    """Build the discrete quadratic model from provided variable list.

    Args:
        variable_list: List of variables for cryptarithm problem.
        coefficient_map: Dictionary mapping variables to their coefficients.
    
    Returns:
        dqm: Corresponding discrete quadratic model. 

    """
    dqm = DQM()

    # Scaling value arbitrarily chosen to tame energies for larger problems.
    eq_constr_scale = 1/(2**(len(coefficient_map)))

    # Set linear biases from equality constraint
    print("setting linear biases...")
    for variable in tqdm(variable_list):
        dqm.add_variable(len(variable.domain), variable.name)
        for idx in range(len(variable.domain)):
            dqm.set_linear_case(variable.name, idx, eq_constr_scale*
                                                    (coefficient_map[variable.name]*
                                                    variable.domain[idx])**2)

    # Set quadratic biases from equality constraint
    print("setting quadratic biases...")
    for var1, var2 in tqdm(combinations(variable_list, r=2)):
        for i in range(dqm.num_cases(var1.name)):
            for j in range(dqm.num_cases(var2.name)):
                dqm.set_quadratic_case(
                    var1.name, i, var2.name, j, 2*
                                                eq_constr_scale*
                                                var1.domain[i]*
                                                var2.domain[j]*
                                                coefficient_map[var1.name]*
                                                coefficient_map[var2.name]
                )

    # Choose a large penalty for quadratic interactions in same states
    quad_penalty = eq_constr_scale*max(np.absolute(dqm.to_numpy_vectors()[2][2]))
    
    # Add penalties for any two variables being in the same state
    print("adding penalty biases...")
    for var1, var2 in tqdm(combinations(variable_list, r=2)):
        if len(var1.domain) < len(var2.domain):
            for i in range(len(var1.domain)):
                bias = dqm.get_quadratic_case(var1.name, i, var2.name, i+1)
                dqm.set_quadratic_case(var1.name, i, var2.name, i+1, bias + quad_penalty)
        
        elif len(var1.domain) > len(var2.domain):
            for i in range(len(var2.domain)):
                bias = dqm.get_quadratic_case(var1.name, i+1, var2.name, i)
                dqm.set_quadratic_case(var1.name, i+1, var2.name, i, bias + quad_penalty)

        else:
            for i in range(len(var1.domain)):
                bias = dqm.get_quadratic_case(var1.name, i, var2.name, i)
                dqm.set_quadratic_case(var1.name, i, var2.name, i, bias + quad_penalty)
        
    
    return dqm

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, nargs="?",
                         help="filename of txt file in puzzle_files folder",
                         default="puzzle_files/example1.txt")
    args = parser.parse_args()

    first_letters = set()
    coefficient_map = defaultdict(int)

    lhs_list, rhs_list, problem_statement = parse_problem_file(args.filename)
    
    update_coefficient_map_and_first_letter_set(lhs_list, 1, coefficient_map, first_letters)
    update_coefficient_map_and_first_letter_set(rhs_list, -1, coefficient_map, first_letters)

    variable_list = []
    for variable, coefficient in coefficient_map.items():
        variable_list.append(LetterVariable(variable, coefficient, first_letter=variable in first_letters))

    pprint(variable_list)

    dqm = build_dqm(variable_list, coefficient_map)

    # Send DQM to LeapHybridDQMSampler, get response
    response = LeapHybridDQMSampler(
        solver="hybrid_discrete_quadratic_model_version1", auto_scale=False
    ).sample_dqm(
        dqm, time_limit=5, compress=True, label="Example - Cryptarithmetic"
    ).aggregate()

    lowest_energy_sample = response.first.sample

    render_solution(lowest_energy_sample,
                    variable_list,
                    lhs_list,
                    rhs_list,
                    problem_statement)
