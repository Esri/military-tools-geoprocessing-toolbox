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
# TableToTwoPointLineTestCase.py
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
# 12/08/2016 - mf - added single cooridnate tests
# ==================================================

import unittest
import arcpy
import os
import UnitTestUtilities
import Configuration

class TableToTwoPointLineTestCase(unittest.TestCase):
    ''' Test all tools and methods related to the Table To 2-Point Line tool
    in the Military Tools toolbox'''
    
    inputTable = None
    outputLines = None
    
    def setUp(self):
        if Configuration.DEBUG == True: print("     TableToTwoPointLineTestCase.setUp")    
        
        UnitTestUtilities.checkArcPy()
        if(Configuration.militaryScratchGDB == None) or (not arcpy.Exists(Configuration.militaryScratchGDB)):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.militaryDataPath)
        
        csvFolder = os.path.join(Configuration.militaryDataPath, "CSV")
        self.inputTable = os.path.join(csvFolder, "TableTo2PointLine.csv")
        self.inputSingleTable = os.path.join(csvFolder, "TableTo2PointLine_single.csv")
        self.outputLines = os.path.join(Configuration.militaryScratchGDB, "output2PointLines")
        
        UnitTestUtilities.checkFilePaths([Configuration.militaryDataPath, Configuration.militaryInputDataGDB, Configuration.militaryScratchGDB, Configuration.militaryResultsGDB, Configuration.military_ProToolboxPath, Configuration.military_DesktopToolboxPath])
        
        
    def tearDown(self):
        if Configuration.DEBUG == True: print("     TableToTwoPointLineTestCase.tearDown")
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)
    
    def test_table_to_twopointline_desktop(self):
        '''Test Table To Two Point Line for ArcGIS Desktop'''
        runToolMessage = ".....TableToTwoPointLineTestCase.test_table_to_twopointline_desktop"
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableTo2PointLine_mt(self.inputTable, "DD_2", "POINT_X", "POINT_Y", "DD_2", "POINT_X2", "POINT_Y2", self.outputLines, "GEODESIC")
        self.assertTrue(arcpy.Exists(self.outputLines), "Output features do not exist or were not created")
        lineCount = int(arcpy.GetCount_management(self.outputLines).getOutput(0))
        expectedFeatures = int(3)
        self.assertEqual(lineCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(lineCount)))
        return
    #Test GARS
    def test_table_to_twopointline_desktop_GARS(self):
        '''Test Table To Two Point Line with GARS for ArcGIS Desktop'''
        runToolMessage = ".....TableToTwoPointLineTestCase.test_table_to_twopointline_desktop_GARS"
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableTo2PointLine_mt(self.inputSingleTable, "GARS", "GARS_1", None, "GARS", "GARS_2", None, self.outputLines, "GEODESIC")
        self.assertTrue(arcpy.Exists(self.outputLines), "Output features do not exist or were not created")
        lineCount = int(arcpy.GetCount_management(self.outputLines).getOutput(0))
        expectedFeatures = int(3)
        self.assertEqual(lineCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(lineCount)))
        return
    #Test USNG
    def test_table_to_twopointline_desktop_USNG(self):
        '''Test Table To Two Point Line with USNG for ArcGIS Desktop'''
        runToolMessage = ".....TableToTwoPointLineTestCase.test_table_to_twopointline_desktop_USNG"
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableTo2PointLine_mt(self.inputSingleTable, "USNG", "USNG_1", None, "USNG", "USNG_2", None, self.outputLines, "GEODESIC")
        self.assertTrue(arcpy.Exists(self.outputLines), "Output features do not exist or were not created")
        lineCount = int(arcpy.GetCount_management(self.outputLines).getOutput(0))
        expectedFeatures = int(3)
        self.assertEqual(lineCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(lineCount)))
        return
    #Test MGRS
    def test_table_to_twopointline_desktop_MGRS(self):
        '''Test Table To Two Point Line with MGRS for ArcGIS Desktop'''
        runToolMessage = ".....TableToTwoPointLineTestCase.test_table_to_twopointline_desktop_MGRS"
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableTo2PointLine_mt(self.inputSingleTable, "MGRS", "MGRS_1", None, "MGRS", "MGRS_2", None, self.outputLines, "GEODESIC")
        self.assertTrue(arcpy.Exists(self.outputLines), "Output features do not exist or were not created")
        lineCount = int(arcpy.GetCount_management(self.outputLines).getOutput(0))
        expectedFeatures = int(3)
        self.assertEqual(lineCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(lineCount)))
        return
    #Test GEOREF
    def test_table_to_twopointline_desktop_GEOREF(self):
        '''Test Table To Two Point Line with GEOREF for ArcGIS Desktop'''
        runToolMessage = ".....TableToTwoPointLineTestCase.test_table_to_twopointline_desktop_GEOREF"
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableTo2PointLine_mt(self.inputSingleTable, "GEOREF", "GEOREF_1", None, "GEOREF", "GEOREF_2", None, self.outputLines, "GEODESIC")
        self.assertTrue(arcpy.Exists(self.outputLines), "Output features do not exist or were not created")
        lineCount = int(arcpy.GetCount_management(self.outputLines).getOutput(0))
        expectedFeatures = int(3)
        self.assertEqual(lineCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(lineCount)))
        return
    #Test UTM_BANDS
    def test_table_to_twopointline_desktop_UTM_BANDS(self):
        '''Test Table To Two Point Line with UTM_BANDS for ArcGIS Desktop'''
        runToolMessage = ".....TableToTwoPointLineTestCase.test_table_to_twopointline_desktop_UTM_BANDS"
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableTo2PointLine_mt(self.inputSingleTable, "UTM_BANDS", "UTM_BANDS_1", None, "UTM_BANDS", "UTM_2", None, self.outputLines, "GEODESIC")
        self.assertTrue(arcpy.Exists(self.outputLines), "Output features do not exist or were not created")
        lineCount = int(arcpy.GetCount_management(self.outputLines).getOutput(0))
        expectedFeatures = int(3)
        self.assertEqual(lineCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(lineCount)))
        return
    
    def test_table_to_twopointline_pro(self):
        '''Test Table To Two Point Line for ArcGIS Pro'''
        runToolMessage = ".....TableToTwoPointLineTestCase.test_table_to_twopointline_pro"
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableTo2PointLine_mt(self.inputTable, "DD_2", "POINT_X", "POINT_Y", "DD_2", "POINT_X2", "POINT_Y2", self.outputLines, "GEODESIC")
        self.assertTrue(arcpy.Exists(self.outputLines), "Output features do not exist or were not created")
        lineCount = int(arcpy.GetCount_management(self.outputLines).getOutput(0))
        expectedFeatures = int(3)
        self.assertEqual(lineCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(lineCount)))
        return
    #Test GARS
    def test_table_to_twopointline_pro_GARS(self):
        '''Test Table To Two Point Line with GARS for ArcGIS Pro'''
        runToolMessage = ".....TableToTwoPointLineTestCase.test_table_to_twopointline_pro_gars"
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableTo2PointLine_mt(self.inputSingleTable, "GARS", "GARS_1", None, "GARS", "GARS_2", None, self.outputLines, "GEODESIC")
        self.assertTrue(arcpy.Exists(self.outputLines), "Output features do not exist or were not created")
        lineCount = int(arcpy.GetCount_management(self.outputLines).getOutput(0))
        expectedFeatures = int(3)
        self.assertEqual(lineCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(lineCount)))
        return
    #Test USNG
    def test_table_to_twopointline_pro_USNG(self):
        '''Test Table To Two Point Line with USNG for ArcGIS Pro'''
        runToolMessage = ".....TableToTwoPointLineTestCase.test_table_to_twopointline_pro_usng"
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableTo2PointLine_mt(self.inputSingleTable, "USNG", "USNG_1", None, "USNG", "USNG_2", None, self.outputLines, "GEODESIC")
        self.assertTrue(arcpy.Exists(self.outputLines), "Output features do not exist or were not created")
        lineCount = int(arcpy.GetCount_management(self.outputLines).getOutput(0))
        expectedFeatures = int(3)
        self.assertEqual(lineCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(lineCount)))
        return
    #Test MGRS
    def test_table_to_twopointline_pro_MGRS(self):
        '''Test Table To Two Point Line with MGRS for ArcGIS Pro'''
        runToolMessage = ".....TableToTwoPointLineTestCase.test_table_to_twopointline_pro_mgrs"
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableTo2PointLine_mt(self.inputSingleTable, "MGRS", "MGRS_1", None, "MGRS", "MGRS_2", None, self.outputLines, "GEODESIC")
        self.assertTrue(arcpy.Exists(self.outputLines), "Output features do not exist or were not created")
        lineCount = int(arcpy.GetCount_management(self.outputLines).getOutput(0))
        expectedFeatures = int(3)
        self.assertEqual(lineCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(lineCount)))
        return
    #Test GEOREF
    def test_table_to_twopointline_pro_GEOREF(self):
        '''Test Table To Two Point Line with GEOREF for ArcGIS Pro'''
        runToolMessage = ".....TableToTwoPointLineTestCase.test_table_to_twopointline_pro_GEOREF"
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableTo2PointLine_mt(self.inputSingleTable, "GEOREF", "GEOREF_1", None, "GEOREF", "GEOREF_2", None, self.outputLines, "GEODESIC")
        self.assertTrue(arcpy.Exists(self.outputLines), "Output features do not exist or were not created")
        lineCount = int(arcpy.GetCount_management(self.outputLines).getOutput(0))
        expectedFeatures = int(3)
        self.assertEqual(lineCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(lineCount)))
        return
    #Test UTM_BANDS
    def test_table_to_twopointline_pro_UTM_BANDS(self):
        '''Test Table To Two Point Line with UTM_BANDS for ArcGIS Pro'''
        runToolMessage = ".....TableToTwoPointLineTestCase.test_table_to_twopointline_pro_UTM_BANDS"
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableTo2PointLine_mt(self.inputSingleTable, "UTM_BANDS", "UTM_BANDS_1", None, "UTM_BANDS", "UTM_2", None, self.outputLines, "GEODESIC")
        self.assertTrue(arcpy.Exists(self.outputLines), "Output features do not exist or were not created")
        lineCount = int(arcpy.GetCount_management(self.outputLines).getOutput(0))
        expectedFeatures = int(3)
        self.assertEqual(lineCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(lineCount)))
        return