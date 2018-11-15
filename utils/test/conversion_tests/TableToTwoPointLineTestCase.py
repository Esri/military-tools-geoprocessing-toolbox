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

import os
import unittest
import math

import arcpy

# Add parent folder to python path if running test case standalone
import sys
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))

import UnitTestUtilities
import Configuration

class TableToTwoPointLineTestCase(unittest.TestCase):
    ''' Test all tools and methods related to the Table To 2-Point Line tool
    in the Military Tools toolbox'''
    
    inputTable = None
    outputLines = None
  
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

        Configuration.Logger.debug("     TableToTwoPointLineTestCase.setUp")    
                
        csvFolder = os.path.join(Configuration.militaryDataPath, "CSV")
        self.inputTable = os.path.join(csvFolder, "TableTo2PointLine.csv")
        self.inputSingleTable = os.path.join(csvFolder, "TableTo2PointLine_single.csv")

        UnitTestUtilities.checkGeoObjects([Configuration.toolboxUnderTest, \
            self.inputTable])

        UnitTestUtilities.checkFilePaths([self.inputTable, self.inputSingleTable])

        self.outputLines = os.path.join(Configuration.militaryScratchGDB, "output2PointLines") 
        
    def tearDown(self):
        Configuration.Logger.debug("     TableToTwoPointLineTestCase.tearDown")
        # UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)
    
    def test_table_to_twopointline(self):
        '''Test Table To Two Point Line for ArcGIS Desktop'''

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputLines) :
            arcpy.Delete_management(self.outputLines)

        runToolMessage = ".....TableToTwoPointLineTestCase.test_table_to_twopointline"
        Configuration.Logger.info(runToolMessage)

        arcpy.TableTo2PointLine_mt(self.inputTable, "DD_2", "POINT_X", "POINT_Y", "DD_2", \
            "POINT_X2", "POINT_Y2", self.outputLines, "GEODESIC")

        # Check 1
        # Does the output feature class exist.
        self.assertTrue(arcpy.Exists(self.outputLines), "Output features do not exist or were not created")
        
        # Check 2
        # Compare the number of rows in the input vs the number of features in the output.  
        # Expected: inputLineCount = outputLineCount 
        
        inputLineCount = int(arcpy.GetCount_management(self.inputTable).getOutput(0))
        outputLineCount = int(arcpy.GetCount_management(self.outputLines).getOutput(0))
     
        self.assertEqual(inputLineCount, outputLineCount, "Expected %s features, but got %s" % (str(inputLineCount), str(outputLineCount)))
        
        # Check 3
        # Check line length from output created.
        # Expected: For each feature in the feature class get the attributes (Point_X, Point_Y) and (Point_X2, Point_Y2). Calculate the expected line length using these attributes.
        # Shape_Length attribute should be the same as expected line length.
        # POINT_X POINT_Y POINT_X2 POINT_Y2

        tolerance = 0.0001
        field_names = ["Shape_Length","POINT_X","POINT_Y", "POINT_X2", "POINT_Y2"]
        with arcpy.da.SearchCursor(self.outputLines, field_names) as cursor:
            for row in cursor:
                actualLineLength = row[0]
                point_X = row[1]
                point_Y = row[2]
                point_X2 = row[3]
                point_Y2 = row[4]

                deltaX = float(point_X2)-float(point_X)
                deltaY = float(point_Y2)-float(point_Y)

                expectedLineLength = math.sqrt((deltaY*deltaY)+(deltaX*deltaX))
           
                deltaLineLength = abs(expectedLineLength - actualLineLength)
                self.assertLessEqual(deltaLineLength, tolerance)
       
        return


    #Test GARS
    def test_table_to_twopointline_GARS(self):
        '''Test Table To Two Point Line with GARS for ArcGIS Desktop'''

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputLines) :
            arcpy.Delete_management(self.outputLines)

        runToolMessage = ".....TableToTwoPointLineTestCase.test_table_to_twopointline_GARS"
        Configuration.Logger.info(runToolMessage)

        arcpy.TableTo2PointLine_mt(self.inputSingleTable, "GARS", "GARS_1", None, \
            "GARS", "GARS_2", None, self.outputLines, "GEODESIC")

        self.assertTrue(arcpy.Exists(self.outputLines), "Output features do not exist or were not created")
        lineCount = int(arcpy.GetCount_management(self.outputLines).getOutput(0))
        expectedFeatures = int(3)
        self.assertEqual(lineCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(lineCount)))
        return

    #Test USNG
    def test_table_to_twopointline_USNG(self):
        '''Test Table To Two Point Line with USNG for ArcGIS Desktop'''

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputLines) :
            arcpy.Delete_management(self.outputLines)

        runToolMessage = ".....TableToTwoPointLineTestCase.test_table_to_twopointline_USNG"
        Configuration.Logger.info(runToolMessage)
        arcpy.TableTo2PointLine_mt(self.inputSingleTable, "USNG", "USNG_1", None, "USNG", "USNG_2", \
            None, self.outputLines, "GEODESIC")

        self.assertTrue(arcpy.Exists(self.outputLines), "Output features do not exist or were not created")
        lineCount = int(arcpy.GetCount_management(self.outputLines).getOutput(0))
        expectedFeatures = int(3)
        self.assertEqual(lineCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(lineCount)))
        return

    #Test MGRS
    def test_table_to_twopointline_MGRS(self):
        '''Test Table To Two Point Line with MGRS for ArcGIS Desktop'''

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputLines) :
            arcpy.Delete_management(self.outputLines)

        runToolMessage = ".....TableToTwoPointLineTestCase.test_table_to_twopointline_MGRS"
        Configuration.Logger.info(runToolMessage)

        arcpy.TableTo2PointLine_mt(self.inputSingleTable, "MGRS", "MGRS_1", None, \
            "MGRS", "MGRS_2", None, self.outputLines, "GEODESIC")

        self.assertTrue(arcpy.Exists(self.outputLines), "Output features do not exist or were not created")
        lineCount = int(arcpy.GetCount_management(self.outputLines).getOutput(0))
        expectedFeatures = int(3)
        self.assertEqual(lineCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(lineCount)))
        return

    #Test GEOREF
    def test_table_to_twopointline_GEOREF(self):
        '''Test Table To Two Point Line with GEOREF for ArcGIS Desktop'''

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputLines) :
            arcpy.Delete_management(self.outputLines)

        runToolMessage = ".....TableToTwoPointLineTestCase.test_table_to_twopointline_GEOREF"
        Configuration.Logger.info(runToolMessage)

        arcpy.TableTo2PointLine_mt(self.inputSingleTable, "GEOREF", "GEOREF_1", None, \
            "GEOREF", "GEOREF_2", None, self.outputLines, "GEODESIC")

        self.assertTrue(arcpy.Exists(self.outputLines), "Output features do not exist or were not created")
        lineCount = int(arcpy.GetCount_management(self.outputLines).getOutput(0))
        expectedFeatures = int(3)
        self.assertEqual(lineCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(lineCount)))
        return

    #Test UTM_BANDS
    def test_table_to_twopointline_UTM_BANDS(self):
        '''Test Table To Two Point Line with UTM_BANDS for ArcGIS Desktop'''

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputLines) :
            arcpy.Delete_management(self.outputLines)

        runToolMessage = ".....TableToTwoPointLineTestCase.test_table_to_twopointline_UTM_BANDS"
        Configuration.Logger.info(runToolMessage)

        arcpy.TableTo2PointLine_mt(self.inputSingleTable, "UTM_BANDS", "UTM_BANDS_1", None, \
            "UTM_BANDS", "UTM_2", None, self.outputLines, "GEODESIC")

        self.assertTrue(arcpy.Exists(self.outputLines), "Output features do not exist or were not created")
        lineCount = int(arcpy.GetCount_management(self.outputLines).getOutput(0))
        expectedFeatures = int(3)
        self.assertEqual(lineCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(lineCount)))
        return
    
if __name__ == "__main__":
    unittest.main() 
