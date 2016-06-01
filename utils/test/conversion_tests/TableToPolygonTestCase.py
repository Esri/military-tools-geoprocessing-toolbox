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
# TableToPolygonTestCase.py
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

class TableToPolygonTestCase(unittest.TestCase):
    ''' Test all tools and methods related to the Table To Polygon tool
    in the Military Tools toolbox'''
    
    def setUp(self):
        if Configuration.DEBUG == True: print("     TableToPolygonTestCase.setUp")    
        
        UnitTestUtilities.checkArcPy()
        if(Configuration.militaryScratchGDB == None) or (not arcpy.Exists(Configuration.militaryScratchGDB)):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.militaryDataPath)
        
    def tearDown(self):
        if Configuration.DEBUG == True: print("     TableToPolygonTestCase.tearDown")
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)
    
    def test_table_to_polygon_desktop(self):
        '''Test Table To Polygon for ArcGIS Desktop'''
        try:
            runToolMessage = "TEST NOT COMPLETE.....TableToPolygonTestCase.test_table_to_polygon_desktop"
            
            #TODO: write the test here
            #arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
            arcpy.AddMessage(runToolMessage)
            #Configuration.Logger.info(runToolMessage)
            
            # arcpy.CheckOutExtension("Spatial")
            # arcpy.FarthestOnCircle_mdat(self.position, "#", "#", self.hoursOfTransit)
            
            # self.assertTrue(arcpy.Exists(self.hoursOfTransit), "error message here")
       
        except arcpy.ExecuteError:
            self.fail(runToolMessage + "\n" + arcpy.GetMessages())
            UnitTestUtilities.handleArcPyError()

        
    def test_table_to_polygon_pro(self):
        '''Test Table To Polygon for ArcGIS Pro'''
        try:
            runToolMessage = "TEST NOT COMPLETE.....TableToPolygonTestCase.test_table_to_polygon_pro"
            
            #TODO: write the test here
            # arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
            arcpy.AddMessage(runToolMessage)
            # Configuration.Logger.info(runToolMessage)
            
            # arcpy.CheckOutExtension("Spatial")
            # arcpy.FarthestOnCircle_mdat(self.position, "#", "#", self.hoursOfTransit)
            
            # self.assertTrue(arcpy.Exists(self.hoursOfTransit), "error message here")
       
        except arcpy.ExecuteError:
            self.fail(runToolMessage + "\n" + arcpy.GetMessages())
            UnitTestUtilities.handleArcPyError()
            