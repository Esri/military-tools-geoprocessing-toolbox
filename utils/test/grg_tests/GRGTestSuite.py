#------------------------------------------------------------------------------
# Copyright 2017 Esri
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#------------------------------------------------------------------------------

import unittest
import logging

try:
    from . import GRGCreateGRGFromPointTestCase
    from . import GRGCreateGRGFromAreaTestCase
    from . import GRGCreateReferenceSystemGRGFromAreaTestCase
except:
    import GRGCreateGRGFromPointTestCase
    import GRGCreateGRGFromAreaTestCase
    import GRGCreateReferenceSystemGRGFromAreaTestCase

''' Test suite for all tools in the GRG Toolset '''

def getTestSuite():

    testSuite = unittest.TestSuite()

    ''' Add the GRG tests '''

    loader = unittest.TestLoader()

    # Gridded Reference Graphic (GRG) Tests
    testSuite.addTest(loader.loadTestsFromTestCase(GRGCreateGRGFromAreaTestCase.GRGCreateGRGFromAreaTestCase))
    testSuite.addTest(loader.loadTestsFromTestCase(GRGCreateGRGFromPointTestCase.GRGCreateGRGFromPointTestCase))
    testSuite.addTest(loader.loadTestsFromTestCase(GRGCreateReferenceSystemGRGFromAreaTestCase.GRGCreateReferenceSystemGRGFromAreaTestCase))

    return testSuite

def testSuiteMain():
    testSuite = unittest.TestSuite()    
    testSuite.addTests(getTestSuite())
    result = unittest.TestResult()
    testSuite.run(result)

if __name__ == "__main__":
    testSuiteMain()
