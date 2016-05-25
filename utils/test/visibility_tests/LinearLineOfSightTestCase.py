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
        if(Configuration.militaryScratchGDB == None) or (not arcpy.Exists(Configuration.militaryScratchGDB)):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.militaryDataPath)

        self.observers = os.path.join(Configuration.militaryInputDataGDB, "LLOS_Observers_ArcMap")
        self.targets = os.path.join(Configuration.militaryInputDataGDB, "LLOS_Targets_ArcMap")
        self.inputSurface = os.path.join(Configuration.militaryInputDataGDB, "ElevationUTM_Zone10")
        self.outputLOS = os.path.join(Configuration.militaryScratchGDB, "outputLinearLineOfSight")
        self.outputSightLines = os.path.join(Configuration.militaryScratchGDB, "outputSightLines")

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
        arcpy.AddMessage("Testing Linear Line Of Sight (Desktop).")
        self.test_linear_line_of_sight(Configuration.military_DesktopToolboxPath)

    def test_linear_line_of_sight_pro(self):
        arcpy.AddMessage("Testing Linear Line Of Sight (Pro).")
        try:
            if Configuration.DEBUG == True: print("     LinearLineOfSightTestCase.test_linear_line_of_sight")

            arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
            runToolMessage = "Running tool (Linear Line Of Sight)"
            arcpy.AddMessage(runToolMessage)
            Configuration.Logger.info(runToolMessage)

            #
            arcpy.LinearLineOfSight_mt(self.observers, self.targets, self.inputSurface, self.outputLOS, self.outputSightLines)
            self.assertTrue(arcpy.Exists(self.outputLOS))
            self.assertTrue(arcpy.Exists(self.outputSightLines))

            featureCount = int(arcpy.GetCount_management(self.outputLOS).getOutput(0))
            self.assertEqual(featureCount, int(32))
            
            featureCountSightLines = int(arcpy.GetCount_management(self.outputSightLines).getOutput(0))
            #self.assertEqual(featureCountSightLines, int(1))

        except arcpy.ExecuteError:
            UnitTestUtilities.handleArcPyError()

        except:
            UnitTestUtilities.handleGeneralError()

    def test_linear_line_of_sight(self, toolboxPath):
        try:
            if Configuration.DEBUG == True: print("     LinearLineOfSightTestCase.test_linear_line_of_sight")

            arcpy.ImportToolbox(toolboxPath, "mt")
            runToolMessage = "Running tool (Linear Line Of Sight)"
            arcpy.AddMessage(runToolMessage)
            Configuration.Logger.info(runToolMessage)

            arcpy.LinearLineOfSight_mt(self.observers, self.targets, self.inputSurface, self.outputLOS)
            self.assertTrue(arcpy.Exists(self.outputLOS))

            featureCount = int(arcpy.GetCount_management(self.outputLOS).getOutput(0))
            self.assertEqual(featureCount, int(32))

            '''pointCount = int(arcpy.GetCount_management(self.outputPoints).getOutput(0))
            self.assertEqual(pointCount, int(1))

            rows = arcpy.SearchCursor(self.outputPoints)
            row = rows.next()
            while row:
                elevation = row.Elevation
                self.assertEqual(elevation, int(1123))
                row = rows.next()'''


        except arcpy.ExecuteError:
            UnitTestUtilities.handleArcPyError()

        except:
            UnitTestUtilities.handleGeneralError()


