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
# TableToPointTestCase.py
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

class TableToPointTestCase(unittest.TestCase):
    ''' Test all tools and methods related to the Table To Point tool
    in the Military Tools toolbox'''
    
    inputTable = None
    outputPoints = None
    
    def setUp(self):
        if Configuration.DEBUG == True: print("     TableToPointTestCase.setUp")    
        
        UnitTestUtilities.checkArcPy()
        if(Configuration.militaryScratchGDB == None) or (not arcpy.Exists(Configuration.militaryScratchGDB)):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.militaryDataPath)

        self.inputTable = os.path.join(Configuration.militaryInputDataGDB, "SigActs")
        self.outputPoints = os.path.join(Configuration.militaryScratchGDB, "outputTableToPoint")
            
    def tearDown(self):
        if Configuration.DEBUG == True: print("     TableToPointTestCase.tearDown")
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)
    
    def test_table_to_point_desktop(self):
        arcpy.AddMessage("Testing Table To Point (Desktop).")
        self.test_table_to_point(Configuration.military_DesktopToolboxPath)
        
    def test_table_to_point_pro(self):
        arcpy.AddMessage("Testing Table To Point (Pro).")
        self.test_table_to_point(Configuration.military_ProToolboxPath)
        
    def test_table_to_point(self, toolboxPath):
        try:
            if Configuration.DEBUG == True: print("     TableToPointTestCase.test_table_to_point") 
            
            arcpy.ImportToolbox(toolboxPath, "ma")
            runToolMessage = "Running tool (Table To Point)"
            arcpy.AddMessage(runToolMessage)
            Configuration.Logger.info(runToolMessage)
            
            arcpy.TableToPoint_ma(self.inputTable, "#", "Location_X", "Location_Y", self.outputPoints)
            
            self.assertTrue(arcpy.Exists(self.outputPoints))
            
            pointCount = int(arcpy.GetCount_management(self.outputPoints).getOutput(0))
            self.assertEqual(pointCount, int(288))
       
            
        except arcpy.ExecuteError:
            UnitTestUtilities.handleArcPyError()
            
        except:
            UnitTestUtilities.handleGeneralError()
            
            
        