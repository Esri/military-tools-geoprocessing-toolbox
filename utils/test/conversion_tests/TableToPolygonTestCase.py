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
    
    inputTable = None
    outputPolygons = None
    
    def setUp(self):
        if Configuration.DEBUG == True: print("     TableToPolygonTestCase.setUp")    
        UnitTestUtilities.checkArcPy()
        if(Configuration.militaryScratchGDB == None) or (not arcpy.Exists(Configuration.militaryScratchGDB)):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.militaryDataPath)
        csvFolder = os.path.join(Configuration.militaryDataPath, "CSV")
        self.inputTable = os.path.join(csvFolder, "TableToPolygon.csv")
        self.inputSingleTable = os.path.join(csvFolder, "TableToPolygon_single.csv")
        self.outputPolygons = os.path.join(Configuration.militaryScratchGDB, "outputPolygons")
        UnitTestUtilities.checkFilePaths([Configuration.militaryDataPath, Configuration.militaryInputDataGDB, Configuration.militaryScratchGDB, Configuration.militaryResultsGDB, Configuration.military_ProToolboxPath, Configuration.military_DesktopToolboxPath])
        
    def tearDown(self):
        if Configuration.DEBUG == True: print("     TableToPolygonTestCase.tearDown")
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)
    
    def test_table_to_polygon_desktop(self):
        '''Test Table To Polygon for ArcGIS Desktop'''
        runToolMessage = ".....TableToPolygonTestCase.test_table_to_polygon_desktop"
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToPolygon_mt(self.inputTable, "DD_2", "POINT_X", "POINT_Y", self.outputPolygons)
        self.assertTrue(arcpy.Exists(self.outputPolygons), "Output polygons do not exist or were not created")
        polygonCount = int(arcpy.GetCount_management(self.outputPolygons).getOutput(0))
        expectedFeatures = int(1)
        self.assertEqual(polygonCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(polygonCount)))
        return
    def test_table_to_polygon_desktop_MGRS(self):
        '''Test Table To Polygon for ArcGIS Desktop_MGRS'''
        runToolMessage = ".....TableToPolygonTestCase.test_table_to_polygon_desktop_MGRS"
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToPolygon_mt(self.inputSingleTable, "MGRS", "MGRS", None, self.outputPolygons)
        self.assertTrue(arcpy.Exists(self.outputPolygons), "Output polygons do not exist or were not created")
        polygonCount = int(arcpy.GetCount_management(self.outputPolygons).getOutput(0))
        expectedFeatures = int(1)
        self.assertEqual(polygonCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(polygonCount)))
        return
    def test_table_to_polygon_desktop_GARS(self):
        '''Test Table To Polygon for ArcGIS Desktop_GARS'''
        runToolMessage = ".....TableToPolygonTestCase.test_table_to_polygon_desktop_GARS"
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToPolygon_mt(self.inputSingleTable, "GARS", "GARS", None, self.outputPolygons)
        self.assertTrue(arcpy.Exists(self.outputPolygons), "Output polygons do not exist or were not created")
        polygonCount = int(arcpy.GetCount_management(self.outputPolygons).getOutput(0))
        expectedFeatures = int(1)
        self.assertEqual(polygonCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(polygonCount)))
        return
    def test_table_to_polygon_desktop_GEOREF(self):
        '''Test Table To Polygon for ArcGIS Desktop_GEOREF'''
        runToolMessage = ".....TableToPolygonTestCase.test_table_to_polygon_desktop_GEOREF"
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToPolygon_mt(self.inputSingleTable, "GEOREF", "GEOREF", None, self.outputPolygons)
        self.assertTrue(arcpy.Exists(self.outputPolygons), "Output polygons do not exist or were not created")
        polygonCount = int(arcpy.GetCount_management(self.outputPolygons).getOutput(0))
        expectedFeatures = int(1)
        self.assertEqual(polygonCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(polygonCount)))
        return
    def test_table_to_polygon_desktop_USNG(self):
        '''Test Table To Polygon for ArcGIS Desktop_USNG'''
        runToolMessage = ".....TableToPolygonTestCase.test_table_to_polygon_desktop_USNG"
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToPolygon_mt(self.inputSingleTable, "USNG", "USNG", None, self.outputPolygons)
        self.assertTrue(arcpy.Exists(self.outputPolygons), "Output polygons do not exist or were not created")
        polygonCount = int(arcpy.GetCount_management(self.outputPolygons).getOutput(0))
        expectedFeatures = int(1)
        self.assertEqual(polygonCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(polygonCount)))
        return
    def test_table_to_polygon_desktop_UTM_BANDS(self):
        '''Test Table To Polygon for ArcGIS Desktop_UTM_BANDS'''
        runToolMessage = ".....TableToPolygonTestCase.test_table_to_polygon_desktop_UTM_BANDS"
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToPolygon_mt(self.inputSingleTable, "UTM_BANDS", "UTM", None, self.outputPolygons)
        self.assertTrue(arcpy.Exists(self.outputPolygons), "Output polygons do not exist or were not created")
        polygonCount = int(arcpy.GetCount_management(self.outputPolygons).getOutput(0))
        expectedFeatures = int(1)
        self.assertEqual(polygonCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(polygonCount)))
        return

    def test_table_to_polygon_pro(self):
        '''Test Table To Polygon for ArcGIS Pro'''
        runToolMessage = ".....TableToPolygonTestCase.test_table_to_polygon_pro"
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        
        arcpy.TableToPolygon_mt(self.inputTable, "DD_2", "POINT_X", "POINT_Y", self.outputPolygons)
        
        self.assertTrue(arcpy.Exists(self.outputPolygons), "Output polygons do not exist or were not created")
        
        polygonCount = int(arcpy.GetCount_management(self.outputPolygons).getOutput(0))
        expectedFeatures = int(1)
        self.assertEqual(polygonCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(polygonCount)))
        return
    def test_table_to_polygon_pro_MGRS(self):
        '''Test Table To Polygon for ArcGIS Pro_MGRS'''
        runToolMessage = ".....TableToPolygonTestCase.test_table_to_polygon_pro_MGRS"
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToPolygon_mt(self.inputSingleTable, "MGRS", "MGRS", None, self.outputPolygons)
        self.assertTrue(arcpy.Exists(self.outputPolygons), "Output polygons do not exist or were not created")
        polygonCount = int(arcpy.GetCount_management(self.outputPolygons).getOutput(0))
        expectedFeatures = int(1)
        self.assertEqual(polygonCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(polygonCount)))
        return
    def test_table_to_polygon_pro_GARS(self):
        '''Test Table To Polygon for ArcGIS Pro_GARS'''
        runToolMessage = ".....TableToPolygonTestCase.test_table_to_polygon_pro_GARS"
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToPolygon_mt(self.inputSingleTable, "GARS", "GARS", None, self.outputPolygons)
        self.assertTrue(arcpy.Exists(self.outputPolygons), "Output polygons do not exist or were not created")
        polygonCount = int(arcpy.GetCount_management(self.outputPolygons).getOutput(0))
        expectedFeatures = int(1)
        self.assertEqual(polygonCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(polygonCount)))
        return
    def test_table_to_polygon_pro_GEOREF(self):
        '''Test Table To Polygon for ArcGIS Pro_GEOREF'''
        runToolMessage = ".....TableToPolygonTestCase.test_table_to_polygon_pro_GEOREF"
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToPolygon_mt(self.inputSingleTable, "GEOREF", "GEOREF", None, self.outputPolygons)
        self.assertTrue(arcpy.Exists(self.outputPolygons), "Output polygons do not exist or were not created")
        polygonCount = int(arcpy.GetCount_management(self.outputPolygons).getOutput(0))
        expectedFeatures = int(1)
        self.assertEqual(polygonCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(polygonCount)))
        return
    def test_table_to_polygon_pro_USNG(self):
        '''Test Table To Polygon for ArcGIS Pro_USNG'''
        runToolMessage = ".....TableToPolygonTestCase.test_table_to_polygon_pro_USNG"
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToPolygon_mt(self.inputSingleTable, "USNG", "USNG", None, self.outputPolygons)
        self.assertTrue(arcpy.Exists(self.outputPolygons), "Output polygons do not exist or were not created")
        polygonCount = int(arcpy.GetCount_management(self.outputPolygons).getOutput(0))
        expectedFeatures = int(1)
        self.assertEqual(polygonCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(polygonCount)))
        return
    def test_table_to_polygon_pro_UTM_BANDS(self):
        '''Test Table To Polygon for ArcGIS Pro_UTM_BANDS'''
        runToolMessage = ".....TableToPolygonTestCase.test_table_to_polygon_pro_UTM_BANDS"
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToPolygon_mt(self.inputSingleTable, "UTM_BANDS", "UTM", None, self.outputPolygons)
        self.assertTrue(arcpy.Exists(self.outputPolygons), "Output polygons do not exist or were not created")
        polygonCount = int(arcpy.GetCount_management(self.outputPolygons).getOutput(0))
        expectedFeatures = int(1)
        self.assertEqual(polygonCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(polygonCount)))
        return
            