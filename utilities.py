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

"""
Helper functions to parse examples
"""
from typing import List, Tuple, DefaultDict
from pprint import pprint
import os

_generate_word_list = lambda x:[word.strip() for word in x.split("+")]
EXCLUDED_OPERATORS = ['*', '-', '^', '%']

def parse_problem_file(file_path:str = None) -> Tuple[List[str], str]:
    """Return lists of words found on left hand side, right hand side.

    Args:
        file_name: Name of file located in puzzle_files folder.

    Returns:
        left-hand side list of words, right-hand side list of words, problem statement

    """
    path = os.path.join(os.path.dirname(__file__), file_path)
    print(path)
    with open(path) as f:
        problem_statement = f.readline()
        lhs, rhs = problem_statement.split("=")
        for operator in EXCLUDED_OPERATORS:
            if operator in problem_statement:
                raise ValueError(
            "Only the addition `+` operator is allowed for left-hand side expression"
            )
        return _generate_word_list(lhs), _generate_word_list(rhs), problem_statement


def update_coefficient_map_and_first_letter_set(word_list: List[str], 
                                                sign: int, 
                                                coefficient_map: DefaultDict[str, int], 
                                                first_letters: set):
    """Update set of first letters and map of variable name to coefficients.

    Args:
        word_list: list of words from either left hand side or right hand side.
        sign: provided sign (1, -1) based on lhs, rhs.
        coefficient_map: defaultdict used to map variable names to coefficients.
        first_letters: set of first letters of all words.

    """
    for word in word_list:
        for power, letter in enumerate(word[::-1]):
            coefficient_map[letter] = coefficient_map[letter] + sign*(10**power)
            if (power == len(word)-1) and len(word)>1:
                first_letters.add(letter)


def _integer_from_word(word: str, solution_map: dict) -> int:
    num = 0
    for power, character in enumerate(word[::-1]):
        num += solution_map[character]*10**power
    return num


def _build_expression(lhs_list: List[str], rhs_list: List[str], solution_map: dict) -> str:
    lhs_integers = []
    for word in lhs_list:
        lhs_integers.append(_integer_from_word(word, solution_map))
        
    lhs_str = " + ".join([str(lhs_ints) for lhs_ints in lhs_integers])
    rhs_str = str(_integer_from_word(rhs_list[0], solution_map))
    return "{lhs_str} = {rhs_str}".format(lhs_str=lhs_str, rhs_str=rhs_str)


def render_solution(sample: dict, 
                    var_list: List, 
                    lhs_list: List[str], 
                    rhs_list: List[str], 
                    orig_example: str):
    """Parse response from LeapHybridDQMSampler, prints solution if found.

    Args:
        sample: Lowest energy sample from response.
        var_list: List of problem variables.
        lhs_list: List of words from left hand side.
        rhs_list: List of words from right hand side.
        orig_example: Problem statement as read from text file.

    """
    lhs_sum, rhs_sum = 0,0
    
    solution_map = {key:var.domain[idx] for key, idx, var in zip(sample.keys(),sample.values(),var_list)}
    pprint(solution_map)
    for word in lhs_list:
        lhs_sum += _integer_from_word(word, solution_map)
    for word in rhs_list:
        rhs_sum += _integer_from_word(word, solution_map)
    
    if lhs_sum == rhs_sum:
        print("Solution found for {original_example}, {expression}".format(
            original_example=orig_example.strip(), 
            expression=_build_expression(lhs_list, rhs_list, solution_map)
        ))
    else:
        print("Solution not found this run, closest assignment is {expression}".format(
            expression=_build_expression(lhs_list, rhs_list, solution_map)
        ))