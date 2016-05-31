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
# TableToLineOfBearingTestCase.py
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

class TableToLineOfBearingTestCase(unittest.TestCase):
    ''' Test all tools and methods related to the Table To Line Of Bearing tool
    in the Military Tools toolbox'''
    
    inputTable = None
    outputLineOfBearing = None
    proBaseFC = None
    desktopBaseFC = None
    platform = None
    
    def setUp(self):
        if Configuration.DEBUG == True: print("     TableToLineOfBearingTestCase.setUp")    
        
        UnitTestUtilities.checkArcPy()
        if(Configuration.militaryScratchGDB == None) or (not arcpy.Exists(Configuration.militaryScratchGDB)):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.militaryDataPath)
        
        csvFolder = os.path.join(Configuration.militaryDataPath, "CSV")
        self.inputTable = os.path.join(csvFolder, "TabletoLineofBearing.csv")
        self.outputLineOfBearing = os.path.join(Configuration.militaryScratchGDB, "outputLines")
        self.proBaseFC = os.path.join(Configuration.militaryResultsGDB, "ExpectedOutputTableToLOBPro")
        self.desktopBaseFC = os.path.join(Configuration.militaryResultsGDB, "ExpectedOutputTableToLOB")
        
        UnitTestUtilities.checkFilePaths([Configuration.militaryDataPath, self.inputTable, Configuration.militaryScratchGDB, Configuration.militaryResultsGDB, Configuration.military_ProToolboxPath, Configuration.military_DesktopToolboxPath])
        
    def tearDown(self):
        if Configuration.DEBUG == True: print("     TableToLineOfBearingTestCase.tearDown")
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)
    
    def test_table_to_lineofbearing_desktop(self):
        arcpy.AddMessage("Testing Table To Line Of Bearing (Desktop).")
        self.platform = "Desktop"
        self.test_table_to_lineofbearing(Configuration.military_DesktopToolboxPath)
        
    def test_table_to_lineofbearing_pro(self):
        arcpy.AddMessage("Testing Table To Line Of Bearing (Pro).")
        self.platform = "Pro"
        self.test_table_to_lineofbearing(Configuration.military_ProToolboxPath)
        
    def test_table_to_lineofbearing(self, toolboxPath):
        try:
            if Configuration.DEBUG == True: print("     TableToLineOfBearingTestCase.test_table_to_lineofbearing") 
            
            arcpy.ImportToolbox(toolboxPath, "mt")
            runToolMessage = "Running tool (Table To Line Of Bearing)"
            arcpy.AddMessage(runToolMessage)
            Configuration.Logger.info(runToolMessage)
            
            arcpy.TableToLOB_mt(self.inputTable, "DD_2", "x", "y", "DEGREES", "Orientation", "METERS", "Distance", self.outputLineOfBearing, "GEODESIC")
            self.assertTrue(arcpy.Exists(self.outputLineOfBearing))
            
            featureCount = int(arcpy.GetCount_management(self.outputLineOfBearing).getOutput(0))
            self.assertEqual(featureCount, int(23))
            
            if self.platform == "Desktop":
                compareFeatures = arcpy.FeatureCompare_management(self.desktopBaseFC, self.outputLineOfBearing, "OID")
                
            else:
                compareFeatures = arcpy.FeatureCompare_management(self.proBaseFC, self.outputLineOfBearing, "OID")
                
            # identical = 'true' means that there are no differences between the base and the output feature class
            identical = compareFeatures.getOutput(1)
            self.assertEqual(identical, "true")
       
            
        except arcpy.ExecuteError:
            UnitTestUtilities.handleArcPyError()
            
        except:
            UnitTestUtilities.handleGeneralError()
            
            
        