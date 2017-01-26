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
5/31/2016 - MF - change error handling
==================================================
'''

import unittest
import arcpy
import os
import UnitTestUtilities
import Configuration

class HighestPointsTestCase(unittest.TestCase):
    ''' Test all tools and methods related to the Highest Points tool
    in the Military Tools toolbox'''

    inputTable = None
    outputPoints = None

    def setUp(self):
        if Configuration.DEBUG == True: print(".....HighestPointsTestCase.setUp")

        UnitTestUtilities.checkArcPy()
        if not arcpy.Exists(Configuration.militaryScratchGDB):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.currentPath)

        self.inputArea = os.path.join(Configuration.militaryInputDataGDB, "AreaofInterest")
        self.inputSurface = os.path.join(Configuration.militaryInputDataGDB, "ElevationUTM_Zone10")
        self.outputPoints = os.path.join(Configuration.militaryScratchGDB, "outputHighestPoints")

        if arcpy.CheckExtension("Spatial") == "Available":
            arcpy.CheckOutExtension("Spatial")
            arcpy.AddMessage(".....Spatial checked out")

    def tearDown(self):
        if Configuration.DEBUG == True: print(".....HighestPointsTestCase.tearDown")
        arcpy.CheckInExtension("Spatial");
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)

    def test_highest_points_desktop(self):
        ''' Test Highest Points for ArcGIS Desktop '''
        runToolMessage = "...HighestPointsTestCase.test_highest_points_desktop"
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.env.overwriteOutput = True
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.HighestPoints_mt(self.inputArea, self.inputSurface, self.outputPoints)
        self.assertTrue(arcpy.Exists(self.outputPoints), "Output dataset does not exist or was not created")
        pointCount = int(arcpy.GetCount_management(self.outputPoints).getOutput(0))
        expectedFeatures = int(1)
        self.assertEqual(pointCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures),str(pointCount)))
        rows = arcpy.SearchCursor(self.outputPoints)
        row = rows.next()
        while row:
            elevation = row.Elevation
            self.assertEqual(elevation, int(1123), "Bad elevation value: %s" % str(elevation))
            row = rows.next()
        return

    def test_highest_points_pro(self):
        ''' Test Highest Points for ArcGIS Pro '''
        runToolMessage = "...HighestPointsTestCase.test_highest_points_pro"
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.env.overwriteOutput = True
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.HighestPoints_mt(self.inputArea, self.inputSurface, self.outputPoints)
        self.assertTrue(arcpy.Exists(self.outputPoints), "Output dataset does not exist or was not created")
        pointCount = int(arcpy.GetCount_management(self.outputPoints).getOutput(0))
        expectedFeatures = int(1)
        self.assertEqual(pointCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures),str(pointCount)))
        rows = arcpy.SearchCursor(self.outputPoints)
        row = rows.next()
        while row:
            elevation = row.Elevation
            self.assertEqual(elevation, int(1123), "Bad elevation value: %s" % str(elevation))
            row = rows.next()
        return
