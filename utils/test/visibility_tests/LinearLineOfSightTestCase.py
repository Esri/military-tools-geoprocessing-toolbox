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

import unittest
import arcpy
import os
import UnitTestUtilities
import Configuration

class LinearLineOfSightTestCase(unittest.TestCase):
    ''' Test all tools and methods related to the Linear Line Of Sight tool
    in the Military Tools toolbox'''

    inputTable = None
    outputPoints = None

    def setUp(self):
        if Configuration.DEBUG == True: print("     LinearLineOfSightTestCase.setUp")

        UnitTestUtilities.checkArcPy()
        if not arcpy.Exists(Configuration.militaryScratchGDB):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.currentPath)

        self.observers = os.path.join(Configuration.militaryInputDataGDB, "LLOS_Observers")
        self.targets = os.path.join(Configuration.militaryInputDataGDB, "LLOS_Targets")
        self.inputSurface = os.path.join(Configuration.militaryInputDataGDB, "ElevationUTM_Zone10")
        self.outputLOS = os.path.join(Configuration.militaryScratchGDB, "outputLinearLineOfSight")
        self.outputSightLines = os.path.join(Configuration.militaryScratchGDB, "outputSightLines")
        self.outputObservers = os.path.join(Configuration.militaryScratchGDB, "outputObservers")
        self.outputTargets = os.path.join(Configuration.militaryScratchGDB, "outputTargets")

        if arcpy.CheckExtension("Spatial") == "Available":
            arcpy.CheckOutExtension("Spatial")
            arcpy.AddMessage("Spatial checked out")
        if arcpy.CheckExtension("3D") == "Available":
            arcpy.CheckOutExtension("3D")
            arcpy.AddMessage("3D checked out")

    def tearDown(self):
        if Configuration.DEBUG == True: print("     LinearLineOfSightTestCase.tearDown")
        arcpy.CheckInExtension("Spatial");
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)

    def test_linear_line_of_sight_desktop(self):
        ''' Test Linear Line Of Sight in ArcGIS Desktop'''
        runToolMessage = ".....LinearLineOfSightTestCase.test_linear_line_of_sight_desktop"
        arcpy.env.overwriteOutput = True
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        
        arcpy.LinearLineOfSight_mt(self.observers,
                                   2.0,
                                   self.targets,
                                   0.0,
                                   self.inputSurface,
                                   self.outputLOS,
                                   self.outputSightLines,
                                   self.outputObservers,
                                   self.outputTargets)
        
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

    def test_linear_line_of_sight_pro(self):
        ''' Test Linear Line Of Sight in ArcGIS Pro '''
        runToolMessage = ".....LinearLineOfSightTestCase.test_linear_line_of_sight_pro"
        arcpy.env.overwriteOutput = True
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.LinearLineOfSight_mt(self.observers,
                                   2.0,
                                   self.targets,
                                   0.0,
                                   self.inputSurface,
                                   self.outputLOS,
                                   self.outputSightLines,
                                   self.outputObservers,
                                   self.outputTargets)
        self.assertTrue(arcpy.Exists(self.outputLOS), "Output LOS does not exist or was not created")
        self.assertTrue(arcpy.Exists(self.outputSightLines), "Output Sight Lines do not exist or were not created")
        self.assertTrue(arcpy.Exists(self.outputObservers), "Output Observers do not exist or were not created")
        self.assertTrue(arcpy.Exists(self.outputTargets), "Output Targets do not exist or were not created")
        featureCount = int(arcpy.GetCount_management(self.outputLOS).getOutput(0))
        expectedFeatures = int(32)
        self.assertEqual(featureCount, expectedFeatures, "Expected %s features but got %s" % (str(expectedFeatures), str(featureCount)))
        featureCountSightLines = int(arcpy.GetCount_management(self.outputSightLines).getOutput(0))
        self.assertEqual(featureCountSightLines, int(16), "Expected 16 Sight Lines but got {0}".format(featureCountSightLines))
        expectedObserverCount = int(arcpy.GetCount_management(self.observers).getOutput(0))
        actualObserverCount = int(arcpy.GetCount_management(self.outputObservers).getOutput(0))
        self.assertEqual(expectedObserverCount,
                         actualObserverCount,
                         "Expected {0} observers but got {1}".format(expectedObserverCount, actualObserverCount))
        expectedTargetCount = int(arcpy.GetCount_management(self.targets).getOutput(0))
        actualTargetCount = int(arcpy.GetCount_management(self.outputTargets).getOutput(0))
        self.assertEqual(expectedTargetCount,
                         actualTargetCount,
                         "Expected {0} targets but got {1}".format(expectedTargetCount, actualTargetCount))
        #TODO: check attached profile graphs were created
        return
