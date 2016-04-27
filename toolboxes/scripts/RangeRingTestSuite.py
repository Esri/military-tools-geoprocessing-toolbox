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
RangeRingTestSuite.py
--------------------------------------------------
requirments:
* ArcGIS Desktop 10.X+ or ArcGIS Pro 1.X+
* Python 2.7 or Python 3.4
author: ArcGIS Solutions
company: Esri
==================================================
description:
This test suite collects all of the range ring tests.

To run tests from command line:
* cd ./military-tools-geoprocessing-toolbox/toolboxes/scripts
* python rangeringtestsuite.py -v

==================================================
history:
3/30/2016 - mf - original coding
==================================================
'''

import unittest

TestSuite = unittest.TestSuite()

def runTestSuite():
    ''' collect all test suites before running them '''
    result = unittest.TestResult()
    tests = getRangeRingTestSuite()

    print("running " + str(TestSuite.countTestCases()) + " tests...")
    TestSuite.run(result)
    print("Test success: {0}".format(str(result.wasSuccessful())))
    return result

def getRangeRingTestSuite():
    ''' Range Rings test suite '''

    testCaseList = ['test_RingMaker_init',
                    'test_RingMaker_sortList_empty',
                    'test_RingMaker_sortList_isSorted',
                    'test_RingMaker_addFieldsToTable',
                    'test_RingMaker_makeTempTable',
                    'test_RingMaker_makeRingsFromDistances',
                    'test_RingMaker_saveRingsAsFeatures',
                    'test_RingMaker_makeRadials',
                    'test_RingMaker_saveRadialsAsFeatures',
                    'test_rangeRingsFromMinMax',
                    'test_rangeRingsFromList',
                    'test_rangeRingsFromInterval']

    addRangeRingUtilsTests(testCaseList)
    print("ALL TESTS ADDED")
    return TestSuite

def addRangeRingUtilsTests(inputTestList):
    ''' add all of the tests from RangeRingTestCase.py '''
    #from . import RangeRingUtilsTestCase
    import RangeRingUtilsTestCase
    for test in inputTestList:
        print(" adding test: " + str(test))
        TestSuite.addTest(RangeRingUtilsTestCase.RangeRingUtilsTestCase(test))

def resultsHeader(result):
    ''' Generic header for the results in the log file '''
    msg = "RESULTS =================================================\n\n"
    msg += "Number of tests run: " + str(result.testsRun) + "\n"
    msg += "Number of errors: " + str(len(result.errors)) + "\n"
    msg += "Number of failures: " + str(len(result.failures)) + "\n"
    return msg

def resultsErrors(result):
    ''' Error results formatting '''
    msg = "ERRORS =================================================\n\n"
    for i in result.errors:
        for j in i:
            msg += str(j)
        msg += "\n"
    return msg

def resultsFailures(result):
    ''' Assert failures formatting '''
    msg = "FAILURES ===============================================\n\n"
    for i in result.failures:
        for j in i:
            msg += str(j)
        msg += "\n"
    return msg

def main():
    ''' main '''
    print("BEGIN TESTING")
    result = runTestSuite()
    resultHead = resultsHeader(result)
    print(resultHead)
    if len(result.errors) > 0:
        rError = resultsErrors(result)
        print(rError)
    if len(result.failures) > 0:
        rFail = resultsFailures(result)
        print(rFail)
    print("END OF RESULTS===========================================\n")

# MAIN =============================================
if __name__ == "__main__":
    main()

