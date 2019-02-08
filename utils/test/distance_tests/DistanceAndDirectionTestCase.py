# coding: utf-8
'''
-----------------------------------------------------------------------------
Copyright 2016-2018 Esri
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
DistanceAndDirectionTestCase.py
--------------------------------------------------
requirements: ArcGIS X.X, Python 2.7 or Python 3.4
author: ArcGIS Solutions
company: Esri
==================================================
description: unittest test case for Distance and Direction Tools
==================================================
'''

import os
import unittest
import arcpy

# Add parent folder to python path if running test case standalone
import sys
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))

import UnitTestUtilities
import Configuration

class DistanceAndDirectionTestCase(unittest.TestCase):

    srWGS84 = arcpy.SpatialReference(4326) #GCS_WGS_1984
    srWAZED = arcpy.SpatialReference(54032) #World_Azimuthal_Equidistant  
    pointGeographic = None

    @classmethod
    def setUpClass(cls):
        # Run once per class creation
        ''' Initialization needed if running Test Case standalone '''
        Configuration.GetLogger()
        Configuration.GetPlatform()
        ''' End standalone initialization '''
            
        Configuration.Logger.debug("     DistanceAndDirectionTestCase.setUpClass")    
        UnitTestUtilities.checkArcPy()

        if not arcpy.Exists(Configuration.militaryScratchGDB):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.currentPath)

        Configuration.Logger.debug("Import Toolbox: " + Configuration.toolboxUnderTest)
        arcpy.ImportToolbox(Configuration.toolboxUnderTest)  
        Configuration.Logger.debug("Done Toolbox Import")

        arcpy.env.overwriteOutput = True

    @classmethod
    def tearDownClass(cls):
        Configuration.Logger.debug("     DistanceAndDirectionTestCase.tearDownClass")
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)

    def setUp(self):

        Configuration.Logger.debug("     DistanceAndDirectionTestCase.setUp")

        self.pointGeographic = os.path.join(Configuration.militaryInputDataGDB, "RLOS_Observers")

        UnitTestUtilities.checkGeoObjects([Configuration.toolboxUnderTest, \
            self.pointGeographic])

    def tearDown(self):
        Configuration.Logger.debug("     DistanceAndDirectionTestCase.tearDown")

    #=== TEST TOOL METHODS ==========================================

    def test_rangeRingsFromMinMax(self):
        ''' testing the tool method '''
        runToolMessage = ".....DistanceAndDirectionTestCase.test_rangeRingsFromMinMax"
        Configuration.Logger.info(runToolMessage)
        
        numCenters = int(arcpy.GetCount_management(self.pointGeographic).getOutput(0))
        inputMinimumRange = 100.0
        inputMaximumRange = 1000.0
        inputDistanceUnits = "METERS"
        numRadials = 8
        rings = os.path.join(Configuration.militaryScratchGDB, "newRings")
        radials = os.path.join(Configuration.militaryScratchGDB, "newRadials") 

        toolOutput = None

        try :      
            toolOutput = arcpy.RangeRingFromMinimumAndMaximum_mt(self.pointGeographic,
                                                 inputMinimumRange,
                                                 inputMaximumRange,
                                                 inputDistanceUnits,
                                                 numRadials,
                                                 rings,
                                                 radials,
                                                 self.srWAZED)
        except arcpy.ExecuteError:
            UnitTestUtilities.handleArcPyError()
        except:
            UnitTestUtilities.handleGeneralError()

        # 1: Check the expected return value
        self.assertIsNotNone(toolOutput, "No output returned from tool")
        outRings = toolOutput.getOutput(0)
        outRadials = toolOutput.getOutput(1)

        self.assertEqual(outRings, rings, "Unexpected return value from tool") 
        self.assertEqual(outRadials, radials, "Unexpected return value from tool") 

        # 2: Check the number of features created 
        self.assertTrue(arcpy.Exists(outRings), "Ring features not created or do not exist")
        self.assertEqual(int(arcpy.GetCount_management(outRings).getOutput(0)), numCenters * 2, "Wrong number of expected ring features")

        self.assertTrue(arcpy.Exists(outRadials), "Radial features not created or do not exist")
        self.assertEqual(int(arcpy.GetCount_management(outRadials).getOutput(0)), numRadials * numCenters, "Wrong number of expected radial features")

        return

    def test_rangeRingsFromMinAndMaxTable(self):
        ''' testing rangeRingsFromMinAndMaxTable method'''

        runToolMessage = ".....DistanceAndDirectionTestCase.test_rangeRingsFromMinAndMaxTable"
        Configuration.Logger.info(runToolMessage)
        
        numCenters = int(arcpy.GetCount_management(self.pointGeographic).getOutput(0))
        inputTable = os.path.join(Configuration.militaryToolboxesPath, \
                                   "tooldata", "RangeRings.gdb", "rrInputTable")
        inputSelectedType = 'M249'
        numRadials = 8
        rings = os.path.join(Configuration.militaryScratchGDB, "newRings")
        radials = os.path.join(Configuration.militaryScratchGDB, "newRadials")

        self.assertTrue(arcpy.Exists(inputTable), "Required table does not exist: " + inputTable)

        toolOutput = None

        try :      
            toolOutput = arcpy.RangeRingsFromMinAndMaxTable_mt(self.pointGeographic,
                                               inputTable,
                                               inputSelectedType,
                                               numRadials,
                                               rings,
                                               radials,
                                               self.srWAZED)
        except arcpy.ExecuteError:
            UnitTestUtilities.handleArcPyError()
        except:
            UnitTestUtilities.handleGeneralError()

        # 1: Check the expected return value
        self.assertIsNotNone(toolOutput, "No output returned from tool")
        outRings = toolOutput.getOutput(0)
        outRadials = toolOutput.getOutput(1)

        self.assertEqual(outRings, rings, "Unexpected return value from tool") 
        self.assertEqual(outRadials, radials, "Unexpected return value from tool") 

        # 2: Check the number of features created 
        self.assertTrue(arcpy.Exists(outRings), "Ring features not created or do not exist")
        self.assertEqual(int(arcpy.GetCount_management(outRings).getOutput(0)), numCenters * 2, "Wrong number of expected ring features")

        self.assertTrue(arcpy.Exists(outRadials), "Radial features not created or do not exist")
        self.assertEqual(int(arcpy.GetCount_management(outRadials).getOutput(0)), numRadials * numCenters, "Wrong number of expected radial features")

        return

    def test_rangeRingsFromInterval(self):
        ''' testing rangeRingsFromInterval method'''

        runToolMessage = ".....DistanceAndDirectionTestCase.test_rangeRingsFromInterval"
        Configuration.Logger.info(runToolMessage)
        
        numCenters = int(arcpy.GetCount_management(self.pointGeographic).getOutput(0))
        distanceBetween = 200.0
        distanceUnits = "METERS"
        numRings = 4
        numRadials = 8
        rings = os.path.join(Configuration.militaryScratchGDB, "newRings")
        radials = os.path.join(Configuration.militaryScratchGDB, "newRadials")

        toolOutput = None

        try :
            toolOutput = arcpy.RangeRingsFromInterval_mt(self.pointGeographic,
                                        numRings,
                                        distanceBetween,
                                        distanceUnits,
                                        numRadials,
                                        rings,
                                        radials,
                                        self.srWAZED)
        except arcpy.ExecuteError:
            UnitTestUtilities.handleArcPyError()
        except:
            UnitTestUtilities.handleGeneralError()

        # 1: Check the expected return value
        self.assertIsNotNone(toolOutput, "No output returned from tool")
        outRings = toolOutput.getOutput(0)
        outRadials = toolOutput.getOutput(1)

        self.assertEqual(outRings, rings, "Unexpected return value from tool") 
        self.assertEqual(outRadials, radials, "Unexpected return value from tool") 

        # 2: Check the number of features created 
        self.assertTrue(arcpy.Exists(outRings), "Ring features not created or do not exist")
        self.assertEqual(int(arcpy.GetCount_management(outRings).getOutput(0)), 4 * numCenters, "Wrong number of expected ring features")

        self.assertTrue(arcpy.Exists(outRadials), "Radial features not created or do not exist")
        self.assertEqual(int(arcpy.GetCount_management(outRadials).getOutput(0)), numRadials * numCenters, "Wrong number of expected radial features")

        return

    def test_rangeRingsFromIntervalNoSR(self):
        ''' testing rangeRingsFromInterval method'''

        runToolMessage = ".....DistanceAndDirectionTestCase.test_rangeRingsFromIntervalNoSR"
        Configuration.Logger.info(runToolMessage)
        
        numCenters = int(arcpy.GetCount_management(self.pointGeographic).getOutput(0))
        distanceBetween = 200.0
        distanceUnits = "METERS"
        numRings = 4
        numRadials = 8
        rings = os.path.join(Configuration.militaryScratchGDB, "newRings")
        radials = os.path.join(Configuration.militaryScratchGDB, "newRadials")

        toolOutput = None

        try :
            toolOutput = arcpy.RangeRingsFromInterval_mt(self.pointGeographic,
                                        numRings,
                                        distanceBetween,
                                        distanceUnits,
                                        numRadials,
                                        rings,
                                        radials) 
                                        # SR is not set
        except arcpy.ExecuteError:
            UnitTestUtilities.handleArcPyError()
        except:
            UnitTestUtilities.handleGeneralError()

        # 1: Check the expected return value
        self.assertIsNotNone(toolOutput, "No output returned from tool")
        outRings = toolOutput.getOutput(0)
        outRadials = toolOutput.getOutput(1)

        self.assertEqual(outRings, rings, "Unexpected return value from tool") 
        self.assertEqual(outRadials, radials, "Unexpected return value from tool") 

        # 2: Check the number of features created 
        self.assertTrue(arcpy.Exists(outRings), "Ring features not created or do not exist")
        self.assertEqual(int(arcpy.GetCount_management(outRings).getOutput(0)), 4 * numCenters, "Wrong number of expected ring features")

        self.assertTrue(arcpy.Exists(outRadials), "Radial features not created or do not exist")
        self.assertEqual(int(arcpy.GetCount_management(outRadials).getOutput(0)), numRadials * numCenters, "Wrong number of expected radial features")

        return

if __name__ == "__main__":
    unittest.main()
