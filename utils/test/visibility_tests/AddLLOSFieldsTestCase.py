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
# AddLLOSFieldsTestCase.py
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

class AddLLOSFieldsTestCase(unittest.TestCase):
    ''' Test all tools and methods related to the Add LLOS Fields tool
    in the Military Tools toolbox'''

    inputTable = None
    outputPoints = None

    def setUp(self):
        if Configuration.DEBUG == True: print("     AddLLOSFieldsTestCase.setUp")

        UnitTestUtilities.checkArcPy()
        if(Configuration.militaryScratchGDB == None) or (not arcpy.Exists(Configuration.militaryScratchGDB)):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.militaryDataPath)

        self.inputObservers = os.path.join(Configuration.militaryInputDataGDB, "Observers")
        self.inputTargets = os.path.join(Configuration.militaryInputDataGDB, "Targets")

    def tearDown(self):
        if Configuration.DEBUG == True: print("     AddLLOSFieldsTestCase.tearDown")
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)

    def test_add_llos_fields_desktop(self):
        arcpy.AddMessage("Testing Add LLOS Fields (Desktop).")
        self.test_add_llos_fields(Configuration.military_DesktopToolboxPath)

    def test_add_llos_fields_pro(self):
        arcpy.AddMessage("Testing Add LLOS Fields (Pro).")
        self.test_add_llos_fields(Configuration.military_ProToolboxPath)

    def test_add_llos_fields(self, toolboxPath):
        try:
            if Configuration.DEBUG == True: print("     AddLLOSFieldsTestCase.test_add_llos_fields")

            arcpy.ImportToolbox(toolboxPath, "mt")
            runToolMessage = "Running tool (Add LLOS Fields)"
            arcpy.AddMessage(runToolMessage)
            Configuration.Logger.info(runToolMessage)

            arcpy.AddLLOSFields_mt(self.inputObservers, 2, self.inputTargets, 0)

            self.assertTrue(arcpy.Exists(self.inputObservers))
            self.assertTrue(arcpy.Exists(self.inputTargets))

            fieldList = arcpy.ListFields(self.inputObservers, "height")
            fieldCount = len(fieldList)

            self.assertEquals(fieldCount, 1)

            fieldList = arcpy.ListFields(self.inputTargets, "height")
            fieldCount = len(fieldList)

            self.assertEquals(fieldCount, 1)

        except arcpy.ExecuteError:
            UnitTestUtilities.handleArcPyError()

        except:
            UnitTestUtilities.handleGeneralError()


