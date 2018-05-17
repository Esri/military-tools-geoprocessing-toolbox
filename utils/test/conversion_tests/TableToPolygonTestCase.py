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

import os
import unittest

import arcpy

# Add parent folder to python path if running test case standalone
import sys
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))

import UnitTestUtilities
import Configuration

class TableToPolygonTestCase(unittest.TestCase):
    ''' Test all tools and methods related to the Table To Polygon tool
    in the Military Tools toolbox'''
    
    inputTable = None
    outputPolygons = None
  
    @classmethod
    def setUpClass(cls):
        # Run once per class creation
        ''' Initialization needed if running Test Case standalone '''
        Configuration.GetLogger()
        Configuration.GetPlatform()
        ''' End standalone initialization '''
            
        Configuration.Logger.debug("     TableToLineOfBearingTestCase.setUpClass")    
        UnitTestUtilities.checkArcPy()

        if not arcpy.Exists(Configuration.militaryScratchGDB):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.currentPath)

        Configuration.Logger.debug("Import Toolbox: " + Configuration.toolboxUnderTest)
        arcpy.ImportToolbox(Configuration.toolboxUnderTest)  
        Configuration.Logger.debug("Done Toolbox Import")

    @classmethod
    def tearDownClass(cls):
        Configuration.Logger.debug("     TableToLineOfBearingTestCase.tearDownClass")
        # UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)
              
    def setUp(self):

        Configuration.Logger.debug("     TableToPolygonTestCase.setUp")

        csvFolder = os.path.join(Configuration.militaryDataPath, "CSV")
        self.inputTable = os.path.join(csvFolder, "TableToPolygon.csv")
        self.inputSingleTable = os.path.join(csvFolder, "TableToPolygon_single.csv")

        UnitTestUtilities.checkGeoObjects([Configuration.toolboxUnderTest])
        UnitTestUtilities.checkFilePaths([self.inputTable, self.inputSingleTable])

        self.outputPolygons = os.path.join(Configuration.militaryScratchGDB, "outputPolygons")
        
    def tearDown(self):
        Configuration.Logger.debug("     TableToPolygonTestCase.tearDown")
    
    def test_table_to_polygon(self):
        '''Test Table To Polygon for ArcGIS Desktop'''

        Configuration.Logger.info(".....TableToPolygonTestCase.test_table_to_polygon")

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputPolygons) :
            arcpy.Delete_management(self.outputPolygons)

        arcpy.TableToPolygon_mt(self.inputTable, "DD_2", "POINT_X", "POINT_Y", self.outputPolygons)

        self.assertTrue(arcpy.Exists(self.outputPolygons), "Output polygons do not exist or were not created")
        polygonCount = int(arcpy.GetCount_management(self.outputPolygons).getOutput(0))
        expectedFeatures = int(1)
        self.assertEqual(polygonCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(polygonCount)))

        return

    def test_table_to_polygon_w_grouping(self):
        '''Test Table To Polygon using Name field as the grouping Line Field'''

        Configuration.Logger.info(".....TableToPolygonTestCase.test_table_to_polygon_w_grouping")

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputPolygons) :
            arcpy.Delete_management(self.outputPolygons)

        # Note: tool fails when run with input "Name" and "Vsort" fields as params
        groupingFieldName = 'Name'
        toolOutput = arcpy.TableToPolygon_mt(self.inputTable, "DD_2", "POINT_X", "POINT_Y", self.outputPolygons, groupingFieldName, "Vsort")

        # 1: Check the expected return value
        self.assertIsNotNone(toolOutput, "No output returned from tool")
        outputOut = toolOutput.getOutput(0)
        self.assertEqual(self.outputPolygons, outputOut, "Unexpected return value from tool")
        self.assertTrue(arcpy.Exists(self.outputPolygons), "Output features do not exist or were not created")

        # Process to check tool results for Grouping
        # Step 1: Make in_memory table to get frequency of
        inMemTable = arcpy.TableToTable_conversion(self.inputTable, "in_memory", "TableToPolygon_single_In_Mem")

        # Step 2: Get the frequency of unique "group values" in the input table
        # Get Frequency of the unique names in the input table
        freqInputTable = arcpy.Frequency_analysis(inMemTable, "in_memory\\CountOfUniqueNames", groupingFieldName, "")

        # Get Count of the unique names
        freqTableCount = arcpy.GetCount_management(freqInputTable)
        expectedFeatureCount = int(freqTableCount.getOutput(0))

        polygonCount = int(arcpy.GetCount_management(self.outputPolygons).getOutput(0))
        self.assertEqual(polygonCount, expectedFeatureCount, "Expected %s features, but got %s" % (str(expectedFeatureCount), str(polygonCount)))

        return

    def test_table_to_polygon_MGRS(self):
        '''Test Table To Polygon for ArcGIS Desktop_MGRS'''

        Configuration.Logger.info(".....TableToPolygonTestCase.test_table_to_polygon_MGRS")

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputPolygons) :
            arcpy.Delete_management(self.outputPolygons)

        arcpy.TableToPolygon_mt(self.inputSingleTable, "MGRS", "MGRS", None, self.outputPolygons)

        self.assertTrue(arcpy.Exists(self.outputPolygons), "Output polygons do not exist or were not created")
        polygonCount = int(arcpy.GetCount_management(self.outputPolygons).getOutput(0))
        expectedFeatures = int(1)
        self.assertEqual(polygonCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(polygonCount)))

        return

    def test_table_to_polygon_GARS(self):
        '''Test Table To Polygon for ArcGIS Desktop_GARS'''

        Configuration.Logger.info(".....TableToPolygonTestCase.test_table_to_polygon_GARS")

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputPolygons) :
            arcpy.Delete_management(self.outputPolygons)

        arcpy.TableToPolygon_mt(self.inputSingleTable, "GARS", "GARS", None, self.outputPolygons)

        self.assertTrue(arcpy.Exists(self.outputPolygons), "Output polygons do not exist or were not created")
        polygonCount = int(arcpy.GetCount_management(self.outputPolygons).getOutput(0))
        expectedFeatures = int(1)
        self.assertEqual(polygonCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(polygonCount)))

        return

    def test_table_to_polygon_GEOREF(self):
        '''Test Table To Polygon for ArcGIS Desktop_GEOREF'''

        Configuration.Logger.info(".....TableToPolygonTestCase.test_table_to_polygon_GEOREF")

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputPolygons) :
            arcpy.Delete_management(self.outputPolygons)

        arcpy.TableToPolygon_mt(self.inputSingleTable, "GEOREF", "GEOREF", None, self.outputPolygons)

        self.assertTrue(arcpy.Exists(self.outputPolygons), "Output polygons do not exist or were not created")
        polygonCount = int(arcpy.GetCount_management(self.outputPolygons).getOutput(0))
        expectedFeatures = int(1)
        self.assertEqual(polygonCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(polygonCount)))

        return

    def test_table_to_polygon_USNG(self):
        '''Test Table To Polygon for ArcGIS Desktop_USNG'''

        Configuration.Logger.info(".....TableToPolygonTestCase.test_table_to_polygon_USNG")

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputPolygons) :
            arcpy.Delete_management(self.outputPolygons)

        arcpy.TableToPolygon_mt(self.inputSingleTable, "USNG", "USNG", None, self.outputPolygons)

        self.assertTrue(arcpy.Exists(self.outputPolygons), "Output polygons do not exist or were not created")
        polygonCount = int(arcpy.GetCount_management(self.outputPolygons).getOutput(0))
        expectedFeatures = int(1)
        self.assertEqual(polygonCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(polygonCount)))

        return

    def test_table_to_polygon_UTM_BANDS(self):
        '''Test Table To Polygon for ArcGIS Desktop_UTM_BANDS'''

        Configuration.Logger.info(".....TableToPolygonTestCase.test_table_to_polygon_UTM_BANDS")

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputPolygons) :
            arcpy.Delete_management(self.outputPolygons)

        arcpy.TableToPolygon_mt(self.inputSingleTable, "UTM_BANDS", "UTM", None, self.outputPolygons)

        self.assertTrue(arcpy.Exists(self.outputPolygons), "Output polygons do not exist or were not created")
        polygonCount = int(arcpy.GetCount_management(self.outputPolygons).getOutput(0))
        expectedFeatures = int(1)
        self.assertEqual(polygonCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(polygonCount)))

        return

if __name__ == "__main__":
    unittest.main()
            