# coding: utf-8
# -----------------------------------------------------------------------------
# Copyright 2016 Esri
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------

# ==================================================
# LowestPointsTestCase.py
# --------------------------------------------------
# requirements:
# * ArcGIS Desktop 10.X+ or ArcGIS Pro 1.X+
# * Python 2.7 or Python 3.4
#
# author: ArcGIS Solutions
# company: Esri
#
# ==================================================
# history:
# 5/11/2016 - JH - initial creation
# ==================================================

import unittest
import arcpy
import os
import UnitTestUtilities
import Configuration

class LowestPointsTestCase(unittest.TestCase):
    ''' Test all tools and methods related to the Lowest Points tool
    in the Military Tools toolbox'''

    inputTable = None
    outputPoints = None

    def setUp(self):
        if Configuration.DEBUG == True: print("     LowestPointsTestCase.setUp")

        UnitTestUtilities.checkArcPy()
        if(Configuration.militaryScratchGDB == None) or (not arcpy.Exists(Configuration.militaryScratchGDB)):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.militaryDataPath)

        self.inputArea = os.path.join(Configuration.militaryInputDataGDB, "AreaofInterest")
        self.inputSurface = os.path.join(Configuration.militaryInputDataGDB, "ElevationUTM_Zone10")
        self.outputPoints = os.path.join(Configuration.militaryScratchGDB, "outputLowestPoints")

        if arcpy.CheckExtension("Spatial") == "Available":
            arcpy.CheckOutExtension("Spatial")
            arcpy.AddMessage("Spatial checked out")

    def tearDown(self):
        if Configuration.DEBUG == True: print("     LowestPointsTestCase.tearDown")
        arcpy.CheckInExtension("Spatial");
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)

    def test_lowest_points_desktop(self):
        arcpy.AddMessage("Testing Lowest Points (Desktop).")
        self.test_lowest_points(Configuration.military_DesktopToolboxPath)

    def test_lowest_points_pro(self):
        arcpy.AddMessage("Testing Lowest Points (Pro).")
        self.test_lowest_points(Configuration.military_ProToolboxPath)

    def test_lowest_points(self, toolboxPath):
        try:
            if Configuration.DEBUG == True: print("     LowestPointsTestCase.test_lowest_points")

            arcpy.ImportToolbox(toolboxPath, "mt")
            runToolMessage = "Running tool (Lowest Points)"
            arcpy.AddMessage(runToolMessage)
            Configuration.Logger.info(runToolMessage)

            arcpy.LowestPoints_mt(self.inputArea, self.inputSurface, self.outputPoints)

            self.assertTrue(arcpy.Exists(self.outputPoints))

            pointCount = int(arcpy.GetCount_management(self.outputPoints).getOutput(0))
            print(pointCount)
            self.assertEqual(pointCount, int(5))


        except arcpy.ExecuteError:
            UnitTestUtilities.handleArcPyError()

        except:
            UnitTestUtilities.handleGeneralError()


