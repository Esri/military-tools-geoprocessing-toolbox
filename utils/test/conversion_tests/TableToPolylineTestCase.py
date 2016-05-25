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
# TableToPolylineTestCase.py
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

class TableToPolylineTestCase(unittest.TestCase):
    ''' Test all tools and methods related to the Table To Polyline tool
    in the Military Tools toolbox'''
    
    inputTable = None
    outputPolylines = None
    
    def setUp(self):
        if Configuration.DEBUG == True: print("     TableToPolylineTestCase.setUp")    
        
        UnitTestUtilities.checkArcPy()
        if(Configuration.militaryScratchGDB == None) or (not arcpy.Exists(Configuration.militaryScratchGDB)):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.militaryDataPath)

        csvPath = os.path.join(Configuration.militaryDataPath, "CSV")
        self.inputTable = os.path.join(csvPath, "TabletoPolyline.csv")
        self.outputPolylines = os.path.join(Configuration.militaryScratchGDB, "outputPolylines")
        
    def tearDown(self):
        if Configuration.DEBUG == True: print("     TableToPolylineTestCase.tearDown")
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)
    
    def test_table_to_polyline_desktop(self):
        arcpy.AddMessage("Testing Table To Polyline (Desktop).")
        self.test_table_to_polyline(Configuration.military_DesktopToolboxPath)
        
    def test_table_to_polyline_pro(self):
        arcpy.AddMessage("Testing Table To Polyline (Pro).")
        self.test_table_to_polyline(Configuration.military_ProToolboxPath)
        
    def test_table_to_polyline(self, toolboxPath):
        try:
            if Configuration.DEBUG == True: print("     TableToPolylineTestCase.test_table_to_polyline") 

            arcpy.ImportToolbox(toolboxPath, "mt")
            runToolMessage = "Running tool (Table To Polyline)"
            arcpy.AddMessage(runToolMessage)
            Configuration.Logger.info(runToolMessage)
            
            arcpy.TableToPolyline_mt(self.inputTable, "DD_2", "POINT_X", "POINT_Y", self.outputPolylines)
            
            self.assertTrue(arcpy.Exists(self.outputPolylines))
            
            polylineCount = int(arcpy.GetCount_management(self.outputPolylines).getOutput(0))
            self.assertEqual(polylineCount, int(1))
       
            
        except arcpy.ExecuteError:
            UnitTestUtilities.handleArcPyError()
            
        except:
            UnitTestUtilities.handleGeneralError()
            
            
        