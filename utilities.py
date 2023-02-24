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
from typing import List, Tuple, DefaultDict, Union
from pprint import pprint
import os

_generate_word_list = lambda x:[word.strip() for word in x.split("+")]
EXCLUDED_OPERATORS = ["*", "-", "^", "%"]

class ProblemInputError(Exception):
    pass

def parse_problem_file(file_path: str = None) -> Tuple[List[str], str]:
    """Return lists of words found on left hand side, right hand side,
    and problem statement.

    Args:
        file_path: Path to puzzle file.

    Returns:
        left-hand side list of words, right-hand side list of words, 
        problem statement.

    """
    path = os.path.join(os.path.dirname(__file__), file_path)
    print(path)
    with open(path) as f:
        problem_statement = f.readline()
        try:
            lhs, rhs = problem_statement.split("=")
        except ValueError:
            raise ProblemInputError(
                "Missing `=` symbol or complete left-hand/right-hand side.")
        _input_validation(problem_statement)
        return _generate_word_list(lhs), _generate_word_list(rhs), problem_statement

def _input_validation(problem_statement: Union[str, bytes]):
    for operator in EXCLUDED_OPERATORS:
            if operator in problem_statement:
                raise ProblemInputError(
                    "Only the addition `+` operator is allowed for \
                    left-hand side expression.")
    
    if "+" not in problem_statement or "=" not in problem_statement:
        raise ProblemInputError(
            "Problem statement must contain `+` and `=` symbols.")

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


def _integer_from_word(word: str, sample: dict) -> int:
    num = 0
    for power, character in enumerate(word[::-1]):
        num += sample[character]*10**power
    return int(num)


def _build_expression(lhs_list: List[str], rhs_list: List[str], sample: dict) -> str:
    lhs_integers = []
    for word in lhs_list:
        lhs_integers.append(_integer_from_word(word, sample))
        
    lhs_str = " + ".join([str(lhs_ints) for lhs_ints in lhs_integers])
    rhs_str = str(_integer_from_word(rhs_list[0], sample))
    return "{lhs_str} = {rhs_str}".format(lhs_str=lhs_str, rhs_str=rhs_str)


def render_solution(sample: dict, 
                    lhs_list: List[str], 
                    rhs_list: List[str], 
                    original_example: str):
    """Parse response from LeapHybridCQMSampler, prints solution if found.

    Args:
        sample: Lowest energy sample from response.
        lhs_list: List of words from left hand side.
        rhs_list: List of words from right hand side.
        original_example: Problem statement as read from text file.

    """
    lhs_sum, rhs_sum = 0,0

    pprint(sample)
    for word in lhs_list:
        lhs_sum += _integer_from_word(word, sample)
    for word in rhs_list:
        rhs_sum += _integer_from_word(word, sample)
    
    print("Solution found for {original_example}, {expression}".format(
        original_example=original_example.strip(), 
        expression=_build_expression(lhs_list, rhs_list, sample)))
