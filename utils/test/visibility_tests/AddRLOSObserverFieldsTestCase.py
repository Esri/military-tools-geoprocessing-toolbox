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
# AddRLOSObserverFieldsTestCase.py
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
# ==================================================

import unittest
import arcpy
import os
import UnitTestUtilities
import Configuration

class AddRLOSObserverFieldsTestCase(unittest.TestCase):
    ''' Test all tools and methods related to the Add RLOS Observer Fields tool
    in the Military Tools toolbox'''

    inputTable = None
    outputPoints = None

    def setUp(self):
        if Configuration.DEBUG == True: print("     AddRLOSObserverFieldsTestCase.setUp")

        UnitTestUtilities.checkArcPy()
        if(Configuration.militaryScratchGDB == None) or (not arcpy.Exists(Configuration.militaryScratchGDB)):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.militaryDataPath)

        self.inputObservers = os.path.join(Configuration.militaryInputDataGDB, "Observers")

    def tearDown(self):
        if Configuration.DEBUG == True: print("     AddRLOSObserverFieldsTestCase.tearDown")
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)

    def test_add_rlos_observer_fields_desktop(self):
        try:
            arcpy.AddMessage("Testing Add RLOS Observer Fields (Desktop).")
            arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
            runToolMessage = "Running tool (Add RLOS Observer Fields)"
            arcpy.AddMessage(runToolMessage)
            Configuration.Logger.info(runToolMessage)

            self.assertTrue(arcpy.Exists(self.inputObservers), "Input dataset does not exist")

            arcpy.AddRLOSObserverFields_mt(self.inputObservers, 0, 1000, 2, 0, 0, 360, 90, -90)

            fieldList = arcpy.ListFields(self.inputObservers, "RADIUS1")
            fieldCount = len(fieldList)
            self.assertEqual(fieldCount, 1, "Expected a field count of 1")
            fieldList = arcpy.ListFields(self.inputObservers, "RADIUS2")
            fieldCount = len(fieldList)
            self.assertEqual(fieldCount, 1, "Expected a field count of 1")
            fieldList = arcpy.ListFields(self.inputObservers, "OFFSETA")
            fieldCount = len(fieldList)
            self.assertEqual(fieldCount, 1, "Expected a field count of 1")
            fieldList = arcpy.ListFields(self.inputObservers, "OFFSETB")
            fieldCount = len(fieldList)
            self.assertEqual(fieldCount, 1, "Expected a field count of 1")
            fieldList = arcpy.ListFields(self.inputObservers, "AZIMUTH1")
            fieldCount = len(fieldList)
            self.assertEqual(fieldCount, 1, "Expected a field count of 1")
            fieldList = arcpy.ListFields(self.inputObservers, "AZIMUTH2")
            fieldCount = len(fieldList)
            self.assertEqual(fieldCount, 1, "Expected a field count of 1")
            fieldList = arcpy.ListFields(self.inputObservers, "VERT1")
            fieldCount = len(fieldList)
            self.assertEqual(fieldCount, 1, "Expected a field count of 1")
            fieldList = arcpy.ListFields(self.inputObservers, "VERT2")
            fieldCount = len(fieldList)
            self.assertEqual(fieldCount, 1, "Expected a field count of 1")


        except arcpy.ExecuteError:
            self.fail(runToolMessage + "\n" + arcpy.GetMessages())
            UnitTestUtilities.handleArcPyError()

    def test_add_llos_fields_pro(self):
        try:
            arcpy.AddMessage("Testing Add RLOS Observer Fields (Pro).")
            arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
            runToolMessage = "Running tool (Add RLOS Observer Fields)"
            arcpy.AddMessage(runToolMessage)
            Configuration.Logger.info(runToolMessage)

            self.assertTrue(arcpy.Exists(self.inputObservers), "Input dataset does not exist")

            arcpy.AddRLOSObserverFields_mt(self.inputObservers, 0, 1000, 2, 0, 0, 360, 90, -90)

            fieldList = arcpy.ListFields(self.inputObservers, "RADIUS1")
            fieldCount = len(fieldList)
            self.assertEqual(fieldCount, 1, "Expected a field count of 1")
            fieldList = arcpy.ListFields(self.inputObservers, "RADIUS2")
            fieldCount = len(fieldList)
            self.assertEqual(fieldCount, 1, "Expected a field count of 1")
            fieldList = arcpy.ListFields(self.inputObservers, "OFFSETA")
            fieldCount = len(fieldList)
            self.assertEqual(fieldCount, 1, "Expected a field count of 1")
            fieldList = arcpy.ListFields(self.inputObservers, "OFFSETB")
            fieldCount = len(fieldList)
            self.assertEqual(fieldCount, 1, "Expected a field count of 1")
            fieldList = arcpy.ListFields(self.inputObservers, "AZIMUTH1")
            fieldCount = len(fieldList)
            self.assertEqual(fieldCount, 1, "Expected a field count of 1")
            fieldList = arcpy.ListFields(self.inputObservers, "AZIMUTH2")
            fieldCount = len(fieldList)
            self.assertEqual(fieldCount, 1, "Expected a field count of 1")
            fieldList = arcpy.ListFields(self.inputObservers, "VERT1")
            fieldCount = len(fieldList)
            self.assertEqual(fieldCount, 1, "Expected a field count of 1")
            fieldList = arcpy.ListFields(self.inputObservers, "VERT2")
            fieldCount = len(fieldList)
            self.assertEqual(fieldCount, 1, "Expected a field count of 1")

        except arcpy.ExecuteError:
            self.fail(runToolMessage + "\n" + arcpy.GetMessages())
            UnitTestUtilities.handleArcPyError()

