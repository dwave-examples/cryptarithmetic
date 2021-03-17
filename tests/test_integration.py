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

import subprocess
import unittest
import os
import sys

from dwave.cloud.utils import retried

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# These integration tests are used to validate example run successfully with other integrated systems
# It is designed to run from any other directory

class IntegrationTests(unittest.TestCase):

    @retried(retries=3)
    def test_cryptarithm(self):
        example_file = os.path.join(project_dir, 'cryptarithm.py')
        output = subprocess.check_output([sys.executable, example_file])
        output = output.decode('utf-8').upper() # Bytes to str
        if os.getenv('DEBUG_OUTPUT'):
            print("Example output \n" + output)

        self.assertIn("Solution found for SEND + MORE = MONEY".upper(), output, msg="No solution found.")

if __name__ == '__main__':
    unittest.main()
