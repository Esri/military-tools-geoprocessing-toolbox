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
history:
5/10/2016 - JH - initial creation
12/09/2016 - MF - added single field tests
==================================================
'''

import logging
import unittest
import Configuration

TestSuite = unittest.TestSuite()

def getConversionTestSuites():
    ''' Add all of the tests in ./conversion_tests to the test suite '''
    
    convertCoordinatesDesktopTests = ['test_convert_coordinates_desktop']
    convertCoordinatesProTests = ['test_convert_coordinates_pro']
    tableToTwoPointDesktopTests = ['test_table_to_twopointline_desktop',
                               'test_table_to_twopointline_desktop_GARS',
                               'test_table_to_twopointline_desktop_USNG',
                               'test_table_to_twopointline_desktop_MGRS',
                               'test_table_to_twopointline_desktop_GEOREF',
                               'test_table_to_twopointline_desktop_UTM_BANDS']
    tableToTwoPointProTests = ['test_table_to_twopointline_pro',
                               'test_table_to_twopointline_pro_GARS',
                               'test_table_to_twopointline_pro_USNG',
                               'test_table_to_twopointline_pro_MGRS',
                               'test_table_to_twopointline_pro_GEOREF',
                               'test_table_to_twopointline_pro_UTM_BANDS']
    tableToEllipseDesktopTests = ['test_table_to_ellipse_desktop',
                                  'test_table_to_ellipse_desktop_GARS',
                                  'test_table_to_ellipse_desktop_GEOREF',
                                  'test_table_to_ellipse_desktop_USNG',
                                  'test_table_to_ellipse_desktop_MGRS',
                                  'test_table_to_ellipse_desktop_UTM_BANDS']
    tableToEllipseProTests = ['test_table_to_ellipse_pro',
                              'test_table_to_ellipse_pro_GARS',
                              'test_table_to_ellipse_pro_GEOREF',
                              'test_table_to_ellipse_pro_USNG',
                              'test_table_to_ellipse_pro_MGRS',
                              'test_table_to_ellipse_pro_UTM_BANDS']
    tableToLineOfBearingDesktopTests = ['test_table_to_lineofbearing_desktop',
                                        'test_table_to_lineofbearing_desktop_MGRS',
                                        'test_table_to_lineofbearing_desktop_GARS',
                                        'test_table_to_lineofbearing_desktop_GEOREF',
                                        'test_table_to_lineofbearing_desktop_USNG',
                                        'test_table_to_lineofbearing_desktop_UTM_BANDS']
    tableToLineOfBearingProTests = ['test_table_to_lineofbearing_pro',
                                    'test_table_to_lineofbearing_pro_MGRS',
                                    'test_table_to_lineofbearing_pro_GARS',
                                    'test_table_to_lineofbearing_pro_GEOREF',
                                    'test_table_to_lineofbearing_pro_USNG',
                                    'test_table_to_lineofbearing_pro_UTM_BANDS']
    tableToPointDesktopTests = ['test_table_to_point_desktop',
                                'test_table_to_point_desktop_MGRS',
                                'test_table_to_point_desktop_GARS',
                                'test_table_to_point_desktop_GEOREF',
                                'test_table_to_point_desktop_USNG',
                                'test_table_to_point_desktop_UTM_BANDS']
    tableToPointProTests = ['test_table_to_point_pro',
                            'test_table_to_point_pro_MGRS',
                            'test_table_to_point_pro_GARS',
                            'test_table_to_point_pro_GEOREF',
                            'test_table_to_point_pro_USNG',
                            'test_table_to_point_pro_UTM_BANDS']
    tableToPolygonDesktopTests = ['test_table_to_polygon_desktop',
                                  'test_table_to_polygon_desktop_MGRS',
                                  'test_table_to_polygon_desktop_GARS',
                                  'test_table_to_polygon_desktop_GEOREF',
                                  'test_table_to_polygon_desktop_USNG',
                                  'test_table_to_polygon_desktop_UTM_BANDS']
    tableToPolygonProTests = ['test_table_to_polygon_pro',
                              'test_table_to_polygon_pro_MGRS',
                              'test_table_to_polygon_pro_GARS',
                              'test_table_to_polygon_pro_GEOREF',
                              'test_table_to_polygon_pro_USNG',
                              'test_table_to_polygon_pro_UTM_BANDS']
    tableToPolylineDesktopTests = ['test_table_to_polyline_desktop',
                                   'test_table_to_polyline_desktop_MGRS',
                                   'test_table_to_polyline_desktop_GARS',
                                   'test_table_to_polyline_desktop_GEOREF',
                                   'test_table_to_polyline_desktop_USNG',
                                   'test_table_to_polyline_desktop_UTM_BANDS']
    tableToPolylineProTests = ['test_table_to_polyline_pro',
                               'test_table_to_polyline_pro_MGRS',
                               'test_table_to_polyline_pro_GARS',
                               'test_table_to_polyline_pro_GEOREF',
                               'test_table_to_polyline_pro_USNG',
                               'test_table_to_polyline_pro_UTM_BANDS']
    
    if Configuration.DEBUG == True:
        print("   ConversionTestSuite.getConversionTestSuites")
        
    Configuration.Logger.info("Adding Conversion tests including: ")
    
    if Configuration.Platform == "DESKTOP":
        Configuration.Logger.info("Conversion Desktop tests")
        addConvertCoordinatesTests(convertCoordinatesDesktopTests)
        addTableToTwoPointLineTests(tableToTwoPointDesktopTests)
        addTableToEllipseTests(tableToEllipseDesktopTests)
        addTableToLineOfBearingTests(tableToLineOfBearingDesktopTests)
        addTableToPointTests(tableToPointDesktopTests)
        addTableToPolygonTests(tableToPolygonDesktopTests)
        addTableToPolylineTests(tableToPolylineDesktopTests)
        
    else:
        Configuration.Logger.info("Conversion Pro tests")
        addConvertCoordinatesTests(convertCoordinatesProTests)
        addTableToTwoPointLineTests(tableToTwoPointProTests)
        addTableToEllipseTests(tableToEllipseProTests)
        addTableToLineOfBearingTests(tableToLineOfBearingProTests)
        addTableToPointTests(tableToPointProTests)
        addTableToPolygonTests(tableToPolygonProTests)
        addTableToPolylineTests(tableToPolylineProTests)
    
    
    return TestSuite
    
def addConvertCoordinatesTests(inputTestList):
    if Configuration.DEBUG == True: print("      ConversionTestSuite.addConvertCoordinatesTests")
    from . import ConvertCoordinatesTestCase
    for test in inputTestList:
        print("adding test: " + str(test))
        Configuration.Logger.info(test)
        TestSuite.addTest(ConvertCoordinatesTestCase.ConvertCoordinatesTestCase(test))  

def addTableToTwoPointLineTests(inputTestList):
    if Configuration.DEBUG == True: print("      ConversionTestSuite.addTableToTwoPointLineTests")
    from . import TableToTwoPointLineTestCase
    for test in inputTestList:
        print("adding test: " + str(test))
        Configuration.Logger.info(test)
        TestSuite.addTest(TableToTwoPointLineTestCase.TableToTwoPointLineTestCase(test))

def addTableToEllipseTests(inputTestList):
    if Configuration.DEBUG == True: print("      ConversionTestSuite.addTableToEllipseTests")
    from . import TableToEllipseTestCase
    for test in inputTestList:
        print("adding test: " + str(test))
        Configuration.Logger.info(test)
        TestSuite.addTest(TableToEllipseTestCase.TableToEllipseTestCase(test))

def addTableToLineOfBearingTests(inputTestList):
    if Configuration.DEBUG == True: print("      ConversionTestSuite.addTableToLineOfBearingTests")
    from . import TableToLineOfBearingTestCase
    for test in inputTestList:
        print("adding test: " + str(test))
        Configuration.Logger.info(test)
        TestSuite.addTest(TableToLineOfBearingTestCase.TableToLineOfBearingTestCase(test))

def addTableToPointTests(inputTestList):
    if Configuration.DEBUG == True: print("      ConversionTestSuite.addTableToPointTests")
    from . import TableToPointTestCase
    for test in inputTestList:
        print("adding test: " + str(test))
        Configuration.Logger.info(test)
        TestSuite.addTest(TableToPointTestCase.TableToPointTestCase(test))

def addTableToPolygonTests(inputTestList):
    if Configuration.DEBUG == True: print("      ConversionTestSuite.addTableToPolygonTests")
    from . import TableToPolygonTestCase
    for test in inputTestList:
        print("adding test: " + str(test))
        Configuration.Logger.info(test)
        TestSuite.addTest(TableToPolygonTestCase.TableToPolygonTestCase(test))

def addTableToPolylineTests(inputTestList):
    if Configuration.DEBUG == True: print("      ConversionTestSuite.addTableToPolylineTests")
    from . import TableToPolylineTestCase
    for test in inputTestList:
        print("adding test: " + str(test))
        Configuration.Logger.info(test)
        TestSuite.addTest(TableToPolylineTestCase.TableToPolylineTestCase(test))
        
 
        