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
TableToPointTestCase.py
--------------------------------------------------
requirements:
* ArcGIS Desktop 10.X+ or ArcGIS Pro 1.X+
* Python 2.7 or Python 3.4

author: ArcGIS Solutions
company: Esri

==================================================
history:
5/18/2016 - DJH - initial creation
5/24/2016 - MF - update for parameter changes in Pro
5/31/2016 - MF - change error handling
11/15/2016 - MF - update for change in offsets and observer & target outputs
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

class LinearLineOfSightTestCase(unittest.TestCase):
    ''' Test all tools and methods related to the Linear Line Of Sight tool
    in the Military Tools toolbox'''

    observers = None
    targets = None
    inputSurface = None
    outputLOS = None
    outputSightLines = None
    outputObservers = None
    outputTargets = None

    def setUp(self):
        ''' Initialization needed if running Test Case standalone '''
        Configuration.GetLogger()
        Configuration.GetPlatform()
        ''' End standalone initialization '''
            
        Configuration.Logger.debug("     LinearLineOfSightTestCase.setUp")

        UnitTestUtilities.checkArcPy()
        if not arcpy.Exists(Configuration.militaryScratchGDB):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.currentPath)

        self.observers = os.path.join(Configuration.militaryInputDataGDB, "LLOS_Observers")
        self.targets = os.path.join(Configuration.militaryInputDataGDB, "LLOS_Targets")
        self.inputSurface = os.path.join(Configuration.militaryInputDataGDB, "ElevationUTM_Zone10")

        self.observers_empty = os.path.join(Configuration.militaryInputDataGDB, "LLOS_Observers_Empty")
        self.targets_empty = os.path.join(Configuration.militaryInputDataGDB, "LLOS_Targets_Empty")

        UnitTestUtilities.checkGeoObjects([Configuration.toolboxUnderTest, \
            self.observers, self.targets, self.inputSurface])

        self.outputLOS = os.path.join(Configuration.militaryScratchGDB, "outputLinearLineOfSight")
        self.outputSightLines = os.path.join(Configuration.militaryScratchGDB, "outputSightLines")
        self.outputObservers = os.path.join(Configuration.militaryScratchGDB, "outputObservers")
        self.outputTargets = os.path.join(Configuration.militaryScratchGDB, "outputTargets")

        # Note: Should not be necessary since tool does this:
        #if arcpy.CheckExtension("3D") == "Available":
        #    arcpy.CheckOutExtension("3D")
        #    arcpy.AddMessage("3D checked out")

        arcpy.ImportToolbox(Configuration.toolboxUnderTest)

        return

    def tearDown(self):
        Configuration.Logger.debug("     LinearLineOfSightTestCase.tearDown")
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)
        # Note: Should not be necessary since tool does this:
        # arcpy.CheckInExtension("3D")

    def test_linear_line_of_sight(self):
        ''' Test Linear Line Of Sight in ArcGIS Desktop'''
        Configuration.Logger.info(".....LinearLineOfSightTestCase.test_linear_line_of_sight")

        arcpy.env.overwriteOutput = True

        toolOutput = None
        try :         
            toolOutput = arcpy.LinearLineOfSight_mt(self.observers,
                                       2.0,
                                       self.targets,
                                       0.0,
                                       self.inputSurface,
                                       self.outputLOS,
                                       self.outputSightLines,
                                       self.outputObservers,
                                       self.outputTargets)
        except:
            # WORKAROUND: To arpy exception with Pro: 
            # "DeprecationWarning: Product and extension licensing is no longer handled with this method."
            # when this tool is run in Pro from unit test driver
            if (Configuration.Platform == Configuration.PLATFORM_PRO):
                pass

        # WORKAROUND: see above - toolOutput not being set because of exception on return
        if (Configuration.Platform != Configuration.PLATFORM_PRO):        
            # 1: Check the expected return value
            self.assertIsNotNone(toolOutput, "No output returned from tool")

            outputLineOfSightOut = toolOutput.getOutput(0)
            outputSightLinesOut  = toolOutput.getOutput(1)
            outputObserversOut   = toolOutput.getOutput(2)
            outputTargetsOut     = toolOutput.getOutput(3)

            self.assertEqual(self.outputLOS, outputLineOfSightOut, "Unexpected return value from tool") 
            self.assertEqual(self.outputSightLines, outputSightLinesOut, "Unexpected return value from tool") 
            self.assertEqual(self.outputObservers, outputObserversOut, "Unexpected return value from tool") 
            self.assertEqual(self.outputTargets, outputTargetsOut, "Unexpected return value from tool") 

        # 2: Verify output was created
        self.assertTrue(arcpy.Exists(self.outputLOS), "Output LOS does not exist or was not created")
        self.assertTrue(arcpy.Exists(self.outputSightLines), "Output Sight Lines to not exist or were not created")
        self.assertTrue(arcpy.Exists(self.outputObservers), "Output Observers do not exist or were not created")
        self.assertTrue(arcpy.Exists(self.outputTargets), "Output Targets do not exist or were not created")
        
        featureCount = int(arcpy.GetCount_management(self.outputLOS).getOutput(0))
        expectedFeatures = int(32)
        self.assertEqual(featureCount, expectedFeatures, "Expected %s features but got %s" % (str(expectedFeatures), str(featureCount)))
        featureCountSightLines = int(arcpy.GetCount_management(self.outputSightLines).getOutput(0))
        self.assertEqual(featureCountSightLines, int(16), "Expected 16 Sight Lines but got {0}".format(featureCountSightLines))
        expectedObserverCount = int(arcpy.GetCount_management(self.observers).getOutput(0)) * 4
        actualObserverCount = int(arcpy.GetCount_management(self.outputObservers).getOutput(0))
        self.assertEqual(expectedObserverCount,
                         actualObserverCount,
                         "Expected {0} observers but got {1}".format(expectedObserverCount, actualObserverCount))
        expectedTargetCount = int(arcpy.GetCount_management(self.targets).getOutput(0)) * 4
        actualTargetCount = int(arcpy.GetCount_management(self.outputTargets).getOutput(0))
        self.assertEqual(expectedTargetCount,
                         actualTargetCount,
                         "Expected {0} targets but got {1}".format(expectedTargetCount, actualTargetCount))
        
        #TODO: check attached profile graphs were created

        return

    def test_empty_observer(self):
        toolOutput = None
        # Check for empty observer input parameter
        with self.assertRaises(arcpy.ExecuteError) as manage_raise:
            toolOutput = arcpy.LinearLineOfSight_mt(self.observers_empty,
                                       2.0,
                                       self.targets,
                                       0.0,
                                       self.inputSurface,
                                       self.outputLOS,
                                       self.outputSightLines,
                                       self.outputObservers,
                                       self.outputTargets)
        self.assertTrue("Please provide at least one observer" in str(manage_raise.exception))
        return

    def test_empty_observer(self):
        toolOutput = None
        # Check for empty target input parameter
        with self.assertRaises(arcpy.ExecuteError) as manage_raise:
            toolOutput = arcpy.LinearLineOfSight_mt(self.observers,
                                       2.0,
                                       self.targets_empty,
                                       0.0,
                                       self.inputSurface,
                                       self.outputLOS,
                                       self.outputSightLines,
                                       self.outputObservers,
                                       self.outputTargets)
        self.assertTrue("Please provide at least one target feature" in str(manage_raise.exception))
        return
        
if __name__ == "__main__":
    unittest.main()