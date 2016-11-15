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
# TableToEllipseTestCase.py
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

class TableToEllipseTestCase(unittest.TestCase):
    ''' Test all tools and methods related to the Table To Ellipse tool
    in the Military Tools toolbox'''
    
    inputTable = None
    outputEllipses = None
    baseFC = None
    
    def setUp(self):
        if Configuration.DEBUG == True: print("     TableToEllipseTestCase.setUp")    
        
        UnitTestUtilities.checkArcPy()
        if(Configuration.militaryScratchGDB == None) or (not arcpy.Exists(Configuration.militaryScratchGDB)):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.militaryDataPath)
            
        csvPath = os.path.join(Configuration.militaryDataPath, "CSV")
        self.inputTable = os.path.join(csvPath, "TableToEllipse.csv")
        self.outputEllipses = os.path.join(Configuration.militaryScratchGDB, "outputEllipses")
        self.baseFC = os.path.join(Configuration.militaryResultsGDB, "ExpectedOutputTableToEllipse")
        
        UnitTestUtilities.checkFilePaths([Configuration.militaryDataPath, self.inputTable, Configuration.militaryScratchGDB, Configuration.militaryResultsGDB, Configuration.military_ProToolboxPath, Configuration.military_DesktopToolboxPath])
        
        
    def tearDown(self):
        if Configuration.DEBUG == True: print("     TableToEllipseTestCase.tearDown")
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)
    
    def test_table_to_ellipse_desktop(self):
        '''test_table_to_ellipse_desktop '''
        runToolMessage = ".....TableToEllipseTestCase.test_table_to_ellipse_desktop"
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        
        arcpy.TableToEllipse_mt(self.inputTable, "DD_2", "x", "y", "Major", "Minor", "KILOMETERS", self.outputEllipses)
        self.assertTrue(arcpy.Exists(self.outputEllipses), "Output dataset does not exist.")
        
        ellipseCount = int(arcpy.GetCount_management(self.outputEllipses).getOutput(0))
        expectedFeatures = int(23)
        self.assertEqual(ellipseCount, expectedFeatures, "Expected %s features but got %s" % (str(expectedFeatures),str(ellipseCount)))
        
        compareFeatures = arcpy.FeatureCompare_management(self.baseFC, self.outputEllipses, "JoinID")
            
        # identical = 'true' means that there are no differences between the base and the output feature class
        identical = compareFeatures.getOutput(1)
        self.assertEqual(identical, "true", "Feature Compare failed: \n %s" % arcpy.GetMessages())
        return
        
        
    def test_table_to_ellipse_pro(self):
        '''test_table_to_ellipse_pro'''
        runToolMessage = ".....TableToEllipseTestCase.test_table_to_ellipse_pro"           
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        
        arcpy.TableToEllipse_mt(self.inputTable, "DD_2", "x", "y", "Major", "Minor", "KILOMETERS", self.outputEllipses)
        self.assertTrue(arcpy.Exists(self.outputEllipses), "Output dataset does not exist.")
        
        ellipseCount = int(arcpy.GetCount_management(self.outputEllipses).getOutput(0))
        expectedFeatures = int(23)
        self.assertEqual(ellipseCount, expectedFeatures, "Expected %s features but got %s" % (str(expectedFeatures),str(ellipseCount)))
        
        compareFeatures = arcpy.FeatureCompare_management(self.baseFC, self.outputEllipses, "JoinID")
            
        # identical = 'true' means that there are no differences between the base and the output feature class
        identical = compareFeatures.getOutput(1)
        self.assertEqual(identical, "true", "Feature Compare failed: \n %s" % arcpy.GetMessages())
        return
