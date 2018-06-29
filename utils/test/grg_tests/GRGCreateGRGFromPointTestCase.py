#------------------------------------------------------------------------------
# Copyright 2017-2018 Esri
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
#------------------------------------------------------------------------------

import os
import unittest

import arcpy

# Add parent folder to python path if running test case standalone
import sys
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))

import Configuration
import UnitTestUtilities

class GRGCreateGRGFromPointTestCase(unittest.TestCase):
    '''
    Test cases for GRG CreateGRGFromPoint GP Tool
    Unit Test Design at: 
    https://github.com/Esri/military-tools-geoprocessing-toolbox/wiki/GRG-From-Point
    '''

    pointTarget = None

    @classmethod
    def setUpClass(cls):
        # Run once per class creation
        ''' Initialization needed if running Test Case standalone '''
        Configuration.GetLogger()
        Configuration.GetPlatform()
        ''' End standalone initialization '''
            
        Configuration.Logger.debug("     GRGCreateGRGFromPointTestCase.setUpClass")    
        UnitTestUtilities.checkArcPy()

        if not arcpy.Exists(Configuration.militaryScratchGDB):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.currentPath)

        arcpy.env.overwriteOutput = True

    @classmethod
    def tearDownClass(cls):
        Configuration.Logger.debug("     GRGCreateGRGFromPointTestCase.tearDownClass")
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)

    def setUp(self):
        Configuration.Logger.debug("         GRGCreateGRGFromPointTestCase.setUp")

        # set up inputs
        self.pointTarget = os.path.join(Configuration.militaryInputDataGDB, r"GRGCenterPoint")

        Configuration.Logger.debug("Import Toolbox: " + Configuration.toolboxUnderTest)
        arcpy.ImportToolbox(Configuration.toolboxUnderTest)  
        Configuration.Logger.debug("Done Toolbox Import")

        UnitTestUtilities.checkGeoObjects([self.pointTarget])

    def tearDown(self):
        Configuration.Logger.debug("         GRGCreateGRGFromPointTestCase.tearDown")

    def testGRGPointTarget(self):
        Configuration.Logger.debug(".....GRGCreateGRGFromPointTestCase.testGRGPointTarget")

        #inputs
        rows = 5
        cols = 10
        cellWidth = 100
        cellHeight = 100
        cellUnits = "Meters"
        labelStart = "Lower-Left"
        labelStyle = "Alpha-Numeric"
        labelSeparator = "-" # TRICKY: Only used for Alpha-Alpha but required parameter?
        gridRotationAngle = 0 # No Rotation

        output = os.path.join(Configuration.militaryScratchGDB, "ptTarget")

        #Testing
        runToolMsg="Running tool (Point Target)"
        arcpy.AddMessage(runToolMsg)
        Configuration.Logger.info(runToolMsg)

        toolOutput = None

        try:
            # Calling the PointTargetGRG Script Tool
            toolOutput = arcpy.CreateGRGFromPoint_mt(self.pointTarget, \
                rows, cols, \
                cellWidth, cellHeight, cellUnits, \
                labelStart, labelStyle, labelSeparator, gridRotationAngle, \
                output)
        except arcpy.ExecuteError:
            UnitTestUtilities.handleArcPyError()
        except:
            UnitTestUtilities.handleGeneralError()

        # 1: Check the expected return value and that output exists
        self.assertIsNotNone(toolOutput, "No output returned from tool")
        outputOut = toolOutput.getOutput(0)
        self.assertEqual(output, outputOut, "Unexpected return value from tool") 
        self.assertTrue(arcpy.Exists(outputOut), "Output does not exist")

        # 2: Check the number of features created 
        result = arcpy.GetCount_management(output)
        count = int(result.getOutput(0))
        expectedCount = rows * cols
        self.assertEqual(count, expectedCount, "Unexpected number of output feature created")

        # 3: Checks 3 and 4 - check size of feature shape and grid zone label
        # for each feature matches the expected values
        expectedPerimeter = (cellWidth * 2.0) + (cellHeight * 2.0)
        tolerance = 0.001
        field_names = ["Grid", "Shape_Length"]
        with arcpy.da.SearchCursor(outputOut, field_names) as cursor:
            for row in cursor:
                gridDesignator = row[0]
                perimeterLength = row[1]
                perimeterDelta = abs(expectedPerimeter - perimeterLength)
                # Check 3 - Grid Perimeter length matched expected (within tolerance)
                self.assertLessEqual(perimeterDelta, tolerance)
                # Check 4 - Grid Zone Designator matches expected format
                regexExpression = '[A-Z][0-9]+$' # [LETTER A-Z][One or more digits]

                # assertRegex (Python 3) vs assertRegexpMatches (Python 2.7)
                if sys.version_info >= (3,2):
                    self.assertRegex(gridDesignator, regexExpression)
                else:
                    self.assertRegexpMatches(gridDesignator, regexExpression)

    def testGRGPointTarget_Numeric(self):
        Configuration.Logger.debug(".....GRGCreateGRGFromPointTestCase.testGRGPointTarget_Numeric")

        #inputs
        rows = 10
        cols = 20
        cellWidth = 100
        cellHeight = 200
        cellUnits = "Meters"
        labelStart = "Lower-Left"
        labelStyle = "Numeric"
        labelSeparator = "-" # TRICKY: Only used for Alpha-Alpha but required parameter?
        gridRotationAngle = 0 # No Rotation

        output = os.path.join(Configuration.militaryScratchGDB, "ptTarget")

        #Testing
        runToolMsg="Running tool (Point Target)"
        arcpy.AddMessage(runToolMsg)
        Configuration.Logger.info(runToolMsg)

        toolOutput = None

        try:
            # Calling the PointTargetGRG Script Tool
            toolOutput = arcpy.CreateGRGFromPoint_mt(self.pointTarget, \
                rows, cols, \
                cellWidth, cellHeight, cellUnits, \
                labelStart, labelStyle, labelSeparator, gridRotationAngle, \
                output)
        except arcpy.ExecuteError:
            UnitTestUtilities.handleArcPyError()
        except:
            UnitTestUtilities.handleGeneralError()

        # 1: Check the expected return value and that output exists
        self.assertIsNotNone(toolOutput, "No output returned from tool")
        outputOut = toolOutput.getOutput(0)
        self.assertEqual(output, outputOut, "Unexpected return value from tool") 
        self.assertTrue(arcpy.Exists(outputOut), "Output does not exist")

        # 2: Check the number of features created 
        result = arcpy.GetCount_management(output)
        count = int(result.getOutput(0))
        expectedCount = rows * cols
        self.assertEqual(count, expectedCount, "Unexpected number of output feature created")

        # 3: Checks 3 and 4 - check size of feature shape and grid zone label
        # for each feature matches the expected values
        expectedPerimeter = (cellWidth * 2.0) + (cellHeight * 2.0)
        tolerance = 0.001
        field_names = ["Grid", "Shape_Length"]
        with arcpy.da.SearchCursor(outputOut, field_names) as cursor:
            for row in cursor:
                gridDesignator = row[0]
                perimeterLength = row[1]
                perimeterDelta = abs(expectedPerimeter - perimeterLength)
                # Check 3 - Grid Perimeter length matched expected (within tolerance)
                self.assertLessEqual(perimeterDelta, tolerance)
                # Check 4 - Grid Zone Designator matches expected format
                regexExpression = '[0-9]+$' # [One or more digits]

                # assertRegex (Python 3) vs assertRegexpMatches (Python 2.7)
                if sys.version_info >= (3,2):
                    self.assertRegex(gridDesignator, regexExpression)
                else:
                    self.assertRegexpMatches(gridDesignator, regexExpression)

    def testGRGPointTarget_Rotated(self):
        Configuration.Logger.debug(".....GRGCreateGRGFromPointTestCase.testGRGPointTarget_Rotated")

        #inputs
        rows = 5
        cols = 10
        cellWidth = 100
        cellHeight = 100
        cellUnits = "Meters"
        labelStart = "Lower-Left"
        labelStyle = "Alpha-Numeric"
        labelSeparator = "-" # TRICKY: Only used for Alpha-Alpha but required parameter?
        gridRotationAngle = 10

        output = os.path.join(Configuration.militaryScratchGDB, "ptTarget")

        #Testing
        runToolMsg="Running tool (Point Target)"
        arcpy.AddMessage(runToolMsg)
        Configuration.Logger.info(runToolMsg)

        toolOutput = None

        try:
            # Calling the PointTargetGRG Script Tool
            toolOutput = arcpy.CreateGRGFromPoint_mt(self.pointTarget, \
                rows, cols, \
                cellWidth, cellHeight, cellUnits, \
                labelStart, labelStyle, labelSeparator, gridRotationAngle, \
                output)
        except arcpy.ExecuteError:
            UnitTestUtilities.handleArcPyError()
        except:
            UnitTestUtilities.handleGeneralError()

        # 1: Check the expected return value
        self.assertIsNotNone(toolOutput, "No output returned from tool")
        outputOut = toolOutput.getOutput(0)
        self.assertEqual(output, outputOut, "Unexpected return value from tool") 
        self.assertTrue(arcpy.Exists(outputOut), "Output does not exist")

        # 2: Check the number of features created 
        result = arcpy.GetCount_management(output)
        count = int(result.getOutput(0))
        expectedCount = rows * cols
        self.assertEqual(count, expectedCount, "Unexpected number of output feature created")

if __name__ == "__main__":
    unittest.main()       
