# coding: utf-8
'''
-----------------------------------------------------------------------------
Copyright 2016 Esri
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-----------------------------------------------------------------------------

==================================================
VisibilityTestSuite.py
--------------------------------------------------
requirments:
* ArcGIS Desktop 10.X+ or ArcGIS Pro 1.X+
* Python 2.7 or Python 3.4
author: ArcGIS Solutions
company: Esri
==================================================
description:
This test suite collects all of the tests in the Visibility toolset 
within the Military Tools toolbox
==================================================
'''

import logging
import unittest

try:
    from . import VisibilityUtilitiesTestCase
    from . import FindLocalPeaksTestCase
    from . import HighestPointsTestCase
    from . import LowestPointsTestCase
    from . import LinearLineOfSightTestCase
    from . import RadialLineOfSightTestCase
    from . import RadialLineOfSightAndRangeTestCase
    from . import AddLLOSFieldsTestCase
    from . import AddRLOSObserverFieldsTestCase
except:
    import VisibilityUtilitiesTestCase
    import FindLocalPeaksTestCase
    import HighestPointsTestCase
    import LowestPointsTestCase
    import LinearLineOfSightTestCase
    import RadialLineOfSightTestCase
    import RadialLineOfSightAndRangeTestCase
    import AddLLOSFieldsTestCase
    import AddRLOSObserverFieldsTestCase

def getTestSuite():

    testSuite = unittest.TestSuite()

    ''' Add the Visibility tests '''
 
    loader = unittest.TestLoader()

    testSuite.addTest(loader.loadTestsFromTestCase(VisibilityUtilitiesTestCase.VisibilityUtilitiesTestCase))
    testSuite.addTest(loader.loadTestsFromTestCase(FindLocalPeaksTestCase.FindLocalPeaksTestCase))
    testSuite.addTest(loader.loadTestsFromTestCase(HighestPointsTestCase.HighestPointsTestCase))
    testSuite.addTest(loader.loadTestsFromTestCase(LowestPointsTestCase.LowestPointsTestCase))
    testSuite.addTest(loader.loadTestsFromTestCase(LinearLineOfSightTestCase.LinearLineOfSightTestCase))
    testSuite.addTest(loader.loadTestsFromTestCase(RadialLineOfSightTestCase.RadialLineOfSightTestCase))
    testSuite.addTest(loader.loadTestsFromTestCase(RadialLineOfSightAndRangeTestCase.RadialLineOfSightAndRangeTestCase))
    testSuite.addTest(loader.loadTestsFromTestCase(AddLLOSFieldsTestCase.AddLLOSFieldsTestCase))
    testSuite.addTest(loader.loadTestsFromTestCase(AddRLOSObserverFieldsTestCase.AddRLOSObserverFieldsTestCase))

    return testSuite

def testSuiteMain():
    testSuite = unittest.TestSuite()    
    testSuite.addTests(getTestSuite())
    result = unittest.TestResult()
    testSuite.run(result)

if __name__ == "__main__":
    testSuiteMain()