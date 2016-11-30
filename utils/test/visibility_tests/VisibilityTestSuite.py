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
This test suite collects all of the tests in the Visibility toolset within the Military Tools toolbox:


==================================================
history:
5/10/2016 - JH - initial creation
==================================================
'''

import logging
import unittest
import Configuration

TestSuite = unittest.TestSuite()

def getVisibilityTestSuites():
    ''' Add all of the tests in ./visibility_tests to the test suite '''
    visibilityUtilitiesTests = ['test__getFieldNameList',
                                'test__addDoubleField',
                                'test__calculateFieldValue',
                                'test__getRasterMinMax',
                                'test__getUniqueValuesFromField001',
                                'test__getUniqueValuesFromField002',
                                'test__clipRasterToArea']
    findLocalPeaksDesktopTests = ['test_find_local_peaks_desktop']
    findLocalPeaksProTests = ['test_find_local_peaks_pro']
    lowestPointsDesktopTests = ['test_lowest_points_desktop']
    lowestPointsProTests = ['test_lowest_points_pro']
    highestPointsDesktopTests = ['test_highest_points_desktop']
    highestPointsProTests = ['test_highest_points_pro']
    linearLineOfSightDesktopTests = ['test_linear_line_of_sight_desktop']
    linearLineOfSightProTests = ['test_linear_line_of_sight_pro']
    radialLineOfSightDesktopTests = ['test_radial_line_of_sight_desktop']
    radialLineOfSightProTests = ['test_radial_line_of_sight_pro']
    addLLOSFieldsProTests = ['test_add_llos_fields_pro']
    addLLOSFieldsDesktopTests = ['test_add_llos_fields_desktop']
    addRLOSObserverDesktopTests = ['test_add_rlos_observer_fields_desktop']
    addRLOSObserverProTests = ['test_add_rlos_observer_fields_pro']

    if Configuration.DEBUG == True:
        print("   VisibilityTestSuite.getVisibilityTestSuites")

    Configuration.Logger.info("Adding Visibility tests including: ")

    if Configuration.Platform == "DESKTOP":
        Configuration.Logger.info("Visibility Desktop tests")
        addVisibilityUtilitiesTests(visibilityUtilitiesTests)
        addFindLocalPeaksTests(findLocalPeaksDesktopTests)
        addHighestPointsTests(highestPointsDesktopTests)
        addLowestPointsTests(lowestPointsDesktopTests)
        addAddLLOSFieldsTests(addLLOSFieldsDesktopTests)
        addAddRLOSObserverFieldsTests(addRLOSObserverDesktopTests)
        addLinearLineOfSightTests(linearLineOfSightDesktopTests)
        addRadialLineOfSightTests(radialLineOfSightDesktopTests)

    else:
        Configuration.Logger.info("Visibility Pro tests")
        addVisibilityUtilitiesTests(visibilityUtilitiesTests)
        addFindLocalPeaksTests(findLocalPeaksProTests)
        addHighestPointsTests(highestPointsProTests)
        addLowestPointsTests(lowestPointsProTests)
        addLinearLineOfSightTests(linearLineOfSightProTests)
        addRadialLineOfSightTests(radialLineOfSightProTests)
        addAddLLOSFieldsTests(addLLOSFieldsProTests)
        addAddRLOSObserverFieldsTests(addRLOSObserverProTests)

    return TestSuite

def addVisibilityUtilitiesTests(inputTestList):
    if Configuration.DEBUG == True: print(".....VisibilityTestSuite.addVisibilityUtilitiesTests")
    from . import VisibilityUtilitiesTestCase
    for test in inputTestList:
        print("adding test: {0}".format(str(test)))
        Configuration.Logger.info(test)
        TestSuite.addTest(VisibilityUtilitiesTestCase.VisibilityUtilitiesTestCase(test))

def addFindLocalPeaksTests(inputTestList):
    if Configuration.DEBUG == True: print("      VisibilityTestSuite.addFindLocalPeaksTests")
    from . import FindLocalPeaksTestCase
    for test in inputTestList:
        print("adding test: " + str(test))
        Configuration.Logger.info(test)
        TestSuite.addTest(FindLocalPeaksTestCase.FindLocalPeaksTestCase(test))

def addHighestPointsTests(inputTestList):
    if Configuration.DEBUG == True: print("      VisibilityTestSuite.addHighestPointsTests")
    from . import HighestPointsTestCase
    for test in inputTestList:
        print("adding test: " + str(test))
        Configuration.Logger.info(test)
        TestSuite.addTest(HighestPointsTestCase.HighestPointsTestCase(test))

def addLowestPointsTests(inputTestList):
    if Configuration.DEBUG == True: print("      VisibilityTestSuite.addLowestPointsTests")
    from . import LowestPointsTestCase
    for test in inputTestList:
        print("adding test: " + str(test))
        Configuration.Logger.info(test)
        TestSuite.addTest(LowestPointsTestCase.LowestPointsTestCase(test))

def addLinearLineOfSightTests(inputTestList):
    if Configuration.DEBUG == True: print("      VisibilityTestSuite.addLinearLineOfSightTests")
    from . import LinearLineOfSightTestCase
    for test in inputTestList:
        print("adding test: " + str(test))
        Configuration.Logger.info(test)
        TestSuite.addTest(LinearLineOfSightTestCase.LinearLineOfSightTestCase(test))

def addRadialLineOfSightTests(inputTestList):
    if Configuration.DEBUG == True: print("      VisibilityTestSuite.addRadialLineOfSightTests")
    from . import RadialLineOfSightTestCase
    for test in inputTestList:
        print("adding test: " + str(test))
        Configuration.Logger.info(test)
        TestSuite.addTest(RadialLineOfSightTestCase.RadialLineOfSightTestCase(test))

def addAddLLOSFieldsTests(inputTestList):
    if Configuration.DEBUG == True: print("      VisibilityTestSuite.addAddLLOSFieldsTests")
    from . import AddLLOSFieldsTestCase
    for test in inputTestList:
        print("adding test: " + str(test))
        Configuration.Logger.info(test)
        TestSuite.addTest(AddLLOSFieldsTestCase.AddLLOSFieldsTestCase(test))

def addAddRLOSObserverFieldsTests(inputTestList):
    if Configuration.DEBUG == True: print("      VisibilityTestSuite.addAddRLOSObserverFieldsTests")
    from . import AddRLOSObserverFieldsTestCase
    for test in inputTestList:
        print("adding test: " + str(test))
        Configuration.Logger.info(test)
        TestSuite.addTest(AddRLOSObserverFieldsTestCase.AddRLOSObserverFieldsTestCase(test))





