# Copyright 2023 D-Wave Systems Inc.
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
from collections import defaultdict
from typing import List

from dimod import Binary, CQM, Integer, quicksum
from dwave.system import LeapHybridCQMSampler
from utilities import (parse_problem_file, 
                       update_coefficient_map_and_first_letter_set, 
                       render_solution)

class ModelVariable:
    """Container for model variable information.

    Args:
        label: Single letter label for the model variable.
        coefficient: Term that appears in main equality constraint.
        first_letter: Whether or not letter is a first letter.
    
    """
    def __init__(self, label: str, coefficient: float, first_letter: bool = False):
        self.label = label
        self.coefficient = coefficient
        self.first_letter = first_letter
    
        if self.first_letter:
            self.var = Integer(self.label, lower_bound=1, upper_bound=9)
            self.lower_bound = 1
            self.upper_bound = 9
        else:
            self.var = Integer(self.label, lower_bound=0, upper_bound=9)
            self.lower_bound = 0
            self.upper_bound = 9


def build_cqm(model_variables: List[ModelVariable]) -> CQM:
    """Build a CQM model for the verbal arithmetic problem.

    Args:
        model_variables: A list of model variables that define the problem.

    Returns:
        A CQM model for the verbal arithmetic problem.
    
    """
    cqm = CQM()

    # Both sides equal constraint
    cqm.add_constraint(
        quicksum(
            [variable.coefficient*variable.var for variable in model_variables]
        ) == 0
    )

    # Add no two variables equal constraints
    for i in range(len(model_variables)):
        for j in range(i+1, len(model_variables)):
            indicator = Binary(
                f"{model_variables[i].label} not equal to {model_variables[j].label} indicator"
            )
            m_i_j_1 = model_variables[i].upper_bound + 1 - model_variables[j].lower_bound
            m_i_j_2 = model_variables[j].upper_bound + 1 - model_variables[i].lower_bound
            cqm.add_constraint(
                model_variables[i].var - model_variables[j].var + 1 - m_i_j_1*indicator <= 0
            )
            cqm.add_constraint(
                model_variables[j].var - model_variables[i].var + 1 - m_i_j_2*(1-indicator) <= 0
            )
    
    return cqm


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--filename", type=str, nargs="?",
                         help="filepath to problem text file",
                         default="puzzle_files/example1.txt")

    parser.add_argument("--time_limit", type=float, nargs="?",
                        help="time limit to pass to CQM sampler",
                        default=5.0)

    args = parser.parse_args()

    first_letters = set()
    coefficient_map = defaultdict(int)

    lhs_list, rhs_list, problem_statement = parse_problem_file(args.filename)

    update_coefficient_map_and_first_letter_set(lhs_list, 1, coefficient_map, first_letters)
    update_coefficient_map_and_first_letter_set(rhs_list, -1, coefficient_map, first_letters)

    model_variables = [
        ModelVariable(
            label=label, coefficient=coefficient, first_letter=label in first_letters
        ) for label, coefficient in coefficient_map.items()
    ]

    cqm = build_cqm(model_variables)

    sampleset = LeapHybridCQMSampler().sample_cqm(cqm, time_limit=args.time_limit)
    feasible_sampleset = sampleset.filter(lambda d: d.is_feasible)

    try:
        sample = feasible_sampleset.first.sample
        render_solution(sample, lhs_list, rhs_list, problem_statement)
    except ValueError as e:
        print(e)
        print("Solution not found this run")
