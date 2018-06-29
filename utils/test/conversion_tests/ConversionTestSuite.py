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
ConversionTestSuite.py
--------------------------------------------------
requirments:
* ArcGIS Desktop 10.X+ or ArcGIS Pro 1.X+
* Python 2.7 or Python 3.4
author: ArcGIS Solutions
company: Esri
==================================================
description:
This test suite collects all of the tests in the Conversion toolset within the Military Tools toolbox:
==================================================
'''

import unittest
import logging

try:
    from . import ConvertCoordinatesTestCase
    from . import TableToTwoPointLineTestCase    
    from . import TableToEllipseTestCase
    from . import TableToLineOfBearingTestCase
    from . import TableToPointTestCase
    from . import TableToPolygonTestCase
    from . import TableToPolylineTestCase
except:
    import ConvertCoordinatesTestCase
    import TableToTwoPointLineTestCase    
    import TableToEllipseTestCase
    import TableToLineOfBearingTestCase
    import TableToPointTestCase
    import TableToPolygonTestCase
    import TableToPolylineTestCase

def getTestSuite():

    testSuite = unittest.TestSuite()

    ''' Add the Conversion tests '''
 
    loader = unittest.TestLoader()

    testSuite.addTest(loader.loadTestsFromTestCase(ConvertCoordinatesTestCase.ConvertCoordinatesTestCase))
    testSuite.addTest(loader.loadTestsFromTestCase(TableToTwoPointLineTestCase.TableToTwoPointLineTestCase))
    testSuite.addTest(loader.loadTestsFromTestCase(TableToEllipseTestCase.TableToEllipseTestCase))
    testSuite.addTest(loader.loadTestsFromTestCase(TableToLineOfBearingTestCase.TableToLineOfBearingTestCase))
    testSuite.addTest(loader.loadTestsFromTestCase(TableToPointTestCase.TableToPointTestCase))
    testSuite.addTest(loader.loadTestsFromTestCase(TableToPolygonTestCase.TableToPolygonTestCase))
    testSuite.addTest(loader.loadTestsFromTestCase(TableToPolylineTestCase.TableToPolylineTestCase))

    return testSuite

def testSuiteMain():
    testSuite = unittest.TestSuite()    
    testSuite.addTests(getTestSuite())
    result = unittest.TestResult()
    testSuite.run(result)

if __name__ == "__main__":
    testSuiteMain()
     