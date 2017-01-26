# coding: utf-8
'''
----------------------------------------------------------------------------
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
5/31/2016 - MF - change error handling
==================================================
'''

import unittest
import arcpy
import os
import UnitTestUtilities
import Configuration

class RadialLineOfSightTestCase(unittest.TestCase):
    ''' Test all tools and methods related to the Radial Line Of Sight tool
    in the Military Tools toolbox'''

    inputTable = None
    outputPoints = None

    def setUp(self):
        if Configuration.DEBUG == True: print("     RadialLineOfSightTestCase.setUp")

        UnitTestUtilities.checkArcPy()
        if not arcpy.Exists(Configuration.militaryScratchGDB):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.currentPath)

        self.observers = os.path.join(Configuration.militaryInputDataGDB, "RLOS_Observers")
        self.inputSurface = os.path.join(Configuration.militaryInputDataGDB, "ElevationUTM_Zone10")
        self.outputRLOS = os.path.join(Configuration.militaryScratchGDB, "outputRadialLineOfSight")

        if arcpy.CheckExtension("Spatial") == "Available":
            arcpy.CheckOutExtension("Spatial")
            arcpy.AddMessage(".....Spatial checked out")

    def tearDown(self):
        if Configuration.DEBUG == True: print("     RadialLineOfSightTestCase.tearDown")
        arcpy.CheckInExtension("Spatial");
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)

    def test_radial_line_of_sight_desktop(self):
        ''' Test Radial Line Of Sight in ArcGIS Desktop'''
        runToolMessage = ".....RadialLineOfSightTestCase.test_Radial_line_of_sight_desktop"
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.RadialLineOfSight_mt(self.observers, 2.0, 2000.0, self.inputSurface, self.outputRLOS)
        self.assertTrue(arcpy.Exists(self.outputRLOS), "Output dataset does not exist or was not created")
        featureCount = int(arcpy.GetCount_management(self.outputRLOS).getOutput(0))
        expectedFeatures = int(3501)
        self.assertEqual(featureCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(featureCount)))
        return

    def test_radial_line_of_sight_pro(self):
        ''' Test Radial Line Of Sight in ArcGIS Pro'''
        runToolMessage = ".....RadialLineOfSightTestCase.test_Radial_line_of_sight_pro"
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.RadialLineOfSight_mt(self.observers, 2.0, 2000.0, self.inputSurface, self.outputRLOS)
        self.assertTrue(arcpy.Exists(self.outputRLOS), "Output dataset does not exist or was not created")
        featureCount = int(arcpy.GetCount_management(self.outputRLOS).getOutput(0))
        expectedFeatures = int(3501)
        self.assertEqual(featureCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(featureCount)))
        return