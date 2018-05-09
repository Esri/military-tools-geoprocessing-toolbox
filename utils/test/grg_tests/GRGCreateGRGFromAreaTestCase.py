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

class GRGCreateGRGFromAreaTestCase(unittest.TestCase):

    inputArea = None

    @classmethod
    def setUpClass(cls):
        # Run once per class creation
        ''' Initialization needed if running Test Case standalone '''
        Configuration.GetLogger()
        Configuration.GetPlatform()
        ''' End standalone initialization '''
            
        Configuration.Logger.debug("     GRGCreateGRGFromAreaTestCase.setUpClass")    
        UnitTestUtilities.checkArcPy()

        if not arcpy.Exists(Configuration.militaryScratchGDB):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.currentPath)

        Configuration.Logger.debug("Import Toolbox: " + Configuration.toolboxUnderTest)
        arcpy.ImportToolbox(Configuration.toolboxUnderTest)  
        Configuration.Logger.debug("Done Toolbox Import")

        arcpy.env.overwriteOutput = True

    @classmethod
    def tearDownClass(cls):
        Configuration.Logger.debug("     GRGCreateGRGFromAreaTestCase.tearDownClass")
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)

    def setUp(self):

        Configuration.Logger.debug("     GRGCreateGRGFromAreaTestCase.setUp")

        # set up inputs
        self.inputArea = os.path.join(Configuration.militaryInputDataGDB, r"GRGAreaofOperations")

        UnitTestUtilities.checkGeoObjects([self.inputArea])

    def tearDown(self):
        Configuration.Logger.debug("         GRGTestCase.tearDown")

    def testGRGAreaGRG(self):

        Configuration.Logger.debug(".....GRGCreateGRGFromAreaTestCase.testGRGAreaGRG")

        #inputs
        cellWidth = 100
        cellHeight = 100
        cellunits = "Meters"
        labelStart = "Lower-Left"
        labelStyle = "Alpha-Numeric"
        labelSeparator = "-" # Only used for Alpha-Alpha but required parameter?
        output = os.path.join(Configuration.militaryScratchGDB, "grg")

        #Testing
        runToolMsg="Running tool (Canvas Area GRG)"
        arcpy.AddMessage(runToolMsg)
        Configuration.Logger.info(runToolMsg)

        toolOutput = None

        try:
            # Calling the Create GRG From Area script tool
            toolOutput = arcpy.CreateGRGFromArea_mt(self.inputArea, \
                cellWidth, cellHeight, cellunits, \
                labelStart, labelStyle, labelSeparator, output)

        except arcpy.ExecuteError:
            UnitTestUtilities.handleArcPyError()
        except:
            UnitTestUtilities.handleGeneralError()

        # 1: Check the expected return value
        self.assertIsNotNone(toolOutput, "No output returned from tool")
        outputOut = toolOutput.getOutput(0)
        self.assertEqual(output, outputOut, "Unexpected return value from tool") 

        # 2: Check the number of features created 
        result = arcpy.GetCount_management(output)
        count = int(result.getOutput(0))
        Configuration.Logger.debug("Output number features: " + str(count))
        self.assertEqual(count, 40)

if __name__ == "__main__":
    unittest.main()       