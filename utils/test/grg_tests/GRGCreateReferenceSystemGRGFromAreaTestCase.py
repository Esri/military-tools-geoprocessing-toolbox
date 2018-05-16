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
import arcpyAssert

class GRGCreateReferenceSystemGRGFromAreaTestCase(unittest.TestCase, arcpyAssert.FeatureClassAssertMixin):
    '''
    Test cases for Create Reference System GRG From Area in the Gridded Reference Graphic Tools toolbox.
    Unit Test Design at: 
    https://github.com/Esri/military-tools-geoprocessing-toolbox/wiki/GRG-CreateReferenceSystemGRGFromArea
    '''

    inputArea = None
    inputArea10m = None
    ref_grid = None
    large_grid_handling = None
    ignore_options = None
    xy_tolerance = None

    @classmethod
    def setUpClass(cls):
        # Run once per class creation
        ''' Initialization needed if running Test Case standalone '''
        Configuration.GetLogger()
        Configuration.GetPlatform()
        ''' End standalone initialization '''
            
        Configuration.Logger.debug("     GRGCreateReferenceSystemGRGFromAreaTestCase.setUpClass")    
        UnitTestUtilities.checkArcPy()

        if not arcpy.Exists(Configuration.militaryScratchGDB):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.currentPath)

        Configuration.Logger.debug("Import Toolbox: " + Configuration.toolboxUnderTest)
        arcpy.ImportToolbox(Configuration.toolboxUnderTest)  
        Configuration.Logger.debug("Done Toolbox Import")

        arcpy.env.overwriteOutput = True

    @classmethod
    def tearDownClass(cls):
        Configuration.Logger.debug("     GRGCreateReferenceSystemGRGFromAreaTestCase.tearDownClass")
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)

    def setUp(self):
        Configuration.Logger.debug("         GRGCreateReferenceSystemGRGFromAreaTestCase.setUp")

        # set up inputs
        self.inputArea = os.path.join(Configuration.militaryInputDataGDB, r"GRGInputAO")
        self.inputArea10m = os.path.join(Configuration.militaryInputDataGDB, r"GRGInputAO10m")
        self.ref_grid = "MGRS"
        self.large_grid_handling = "ALLOW_LARGE_GRIDS"
        self.xy_tolerance = 0.0000001
        self.ignore_options = ["IGNORE_M",
                               "IGNORE_Z",
                               "IGNORE_POINTID",
                               "IGNORE_EXTENSION_PROPERTIES",
                               "IGNORE_SUBTYPES",
                               "IGNORE_RELATIONSHIPCLASSES",
                               "IGNORE_REPRESENTATIONCLASSES"]

        UnitTestUtilities.checkGeoObjects([self.inputArea, self.inputArea10m])

    def tearDown(self):
        Configuration.Logger.debug("         GRGCreateReferenceSystemGRGFromAreaTestCase.tearDown")

    # GZD Test
    def testCreateReferenceSystemGRGFromArea_GZD(self):
        '''
        Testing with Grid Zone Designator
        '''
        Configuration.Logger.debug(".....GRGCreateReferenceSystemGRGFromAreaTestCase.testCreateReferenceSystemGRGFromArea_GZD")

        #inputs
        grid_size = "GRID_ZONE_DESIGNATOR"
        output = os.path.join(Configuration.militaryScratchGDB, "outgrg_GZD")

        #Testing
        runToolMsg = "Running tool (CreateReferenceSystemGRGFromArea)"
        arcpy.AddMessage(runToolMsg)
        Configuration.Logger.info(runToolMsg)
        compareDataset = os.path.join(Configuration.militaryResultsGDB, \
                                                       "CompareGZD")
        toolOutput = None

        try:
            toolOutput = arcpy.CreateReferenceSystemGRGFromArea_mt(self.inputArea,
                                                       self.ref_grid,
                                                       grid_size,
                                                       output,
                                                       self.large_grid_handling)
            arcpy.AddSpatialIndex_management(output)
        except arcpy.ExecuteError:
            UnitTestUtilities.handleArcPyError()
        except:
            UnitTestUtilities.handleGeneralError()

        # 1: Check the expected return value
        self.assertIsNotNone(toolOutput, "No output returned from tool")
        outputOut = toolOutput.getOutput(0)
        self.assertEqual(output, outputOut, "Unexpected return value from tool") 
        self.assertTrue(arcpy.Exists(outputOut), "Output does not exist") 

        # 2: Check the features created 
        self.assertFeatureClassEqual(compareDataset,
                                     output,
                                     arcpy.Describe(output).oidFieldName,
                                     None,
                                     "ALL",
                                     self.ignore_options,
                                     self.xy_tolerance)

    # 100KM Test
    def testCreateReferenceSystemGRGFromArea_100KM(self):
        '''
        Testing with 100KM grid
        '''
        Configuration.Logger.debug(".....GRGCreateReferenceSystemGRGFromAreaTestCase.testCreateReferenceSystemGRGFromArea_100KM")

        #inputs
        grid_size = "100000M_GRID"
        output = os.path.join(Configuration.militaryScratchGDB, "outgrg_100KM")

        #Testing
        runToolMsg = "Running tool (CreateReferenceSystemGRGFromArea)"
        arcpy.AddMessage(runToolMsg)
        Configuration.Logger.info(runToolMsg)
        compareDataset = os.path.normpath(os.path.join(Configuration.militaryResultsGDB,
                                                       "Compare100km"))
        toolOutput = None

        try:
            toolOutput = arcpy.CreateReferenceSystemGRGFromArea_mt(self.inputArea,
                                                  self.ref_grid,
                                                  grid_size,
                                                  output,
                                                  self.large_grid_handling)
            arcpy.AddSpatialIndex_management(output)
        except arcpy.ExecuteError:
            UnitTestUtilities.handleArcPyError()
        except:
            UnitTestUtilities.handleGeneralError()

        # 1: Check the expected return value
        self.assertIsNotNone(toolOutput, "No output returned from tool")
        outputOut = toolOutput.getOutput(0)
        self.assertEqual(output, outputOut, "Unexpected return value from tool") 
        self.assertTrue(arcpy.Exists(outputOut), "Output does not exist") 

        # 2: Check the features created 
        self.assertFeatureClassEqual(compareDataset,
                                     output,
                                     arcpy.Describe(output).oidFieldName,
                                     None,
                                     "ALL",
                                     self.ignore_options,
                                     self.xy_tolerance)

    # 10KM Test
    def testCreateReferenceSystemGRGFromArea_10KM(self):
        '''
        Testing with 10KM grid
        '''
        Configuration.Logger.debug(".....GRGCreateReferenceSystemGRGFromAreaTestCase.testCreateReferenceSystemGRGFromArea_10KM")

        #inputs
        grid_size = "10000M_GRID"
        output = os.path.join(Configuration.militaryScratchGDB, "outgrg_10KM")

        #Testing
        runToolMsg = "Running tool (CreateReferenceSystemGRGFromArea)"
        arcpy.AddMessage(runToolMsg)
        Configuration.Logger.info(runToolMsg)
        compareDataset = os.path.normpath(os.path.join(Configuration.militaryResultsGDB,
                                                       "Compare10km"))
        toolOutput = None

        try:
            toolOutput = arcpy.CreateReferenceSystemGRGFromArea_mt(self.inputArea,
                                                       self.ref_grid,
                                                       grid_size,
                                                       output,
                                                       self.large_grid_handling)
            arcpy.AddSpatialIndex_management(output)
        except arcpy.ExecuteError:
            UnitTestUtilities.handleArcPyError()
        except:
            UnitTestUtilities.handleGeneralError()

        # 1: Check the expected return value
        self.assertIsNotNone(toolOutput, "No output returned from tool")
        outputOut = toolOutput.getOutput(0)
        self.assertEqual(output, outputOut, "Unexpected return value from tool") 
        self.assertTrue(arcpy.Exists(outputOut), "Output does not exist") 

        # 2: Check the features created 
        self.assertFeatureClassEqual(compareDataset,
                                     output,
                                     arcpy.Describe(output).oidFieldName,
                                     None,
                                     "ALL",
                                     self.ignore_options,
                                     self.xy_tolerance)

    # 1000M Test
    def testCreateReferenceSystemGRGFromArea_1000M(self):
        '''
        Testing with 1000M grid
        '''
        Configuration.Logger.debug(".....GRGCreateReferenceSystemGRGFromAreaTestCase.testCreateReferenceSystemGRGFromArea_1000M")

        #inputs
        grid_size = "1000M_GRID"
        output = os.path.join(Configuration.militaryScratchGDB, "outgrg_1000M")

        #Testing
        runToolMsg = "Running tool (CreateReferenceSystemGRGFromArea)"
        arcpy.AddMessage(runToolMsg)
        Configuration.Logger.info(runToolMsg)
        compareDataset = os.path.normpath(os.path.join(Configuration.militaryResultsGDB,
                                                       "Compare1000m"))
        toolOutput = None

        try:
            toolOutput = arcpy.CreateReferenceSystemGRGFromArea_mt(self.inputArea,
                                                       self.ref_grid,
                                                       grid_size,
                                                       output,
                                                       self.large_grid_handling)
            arcpy.AddSpatialIndex_management(output)
        except arcpy.ExecuteError:
            UnitTestUtilities.handleArcPyError()
        except:
            UnitTestUtilities.handleGeneralError()

        # 1: Check the expected return value
        self.assertIsNotNone(toolOutput, "No output returned from tool")
        outputOut = toolOutput.getOutput(0)
        self.assertEqual(output, outputOut, "Unexpected return value from tool") 
        self.assertTrue(arcpy.Exists(outputOut), "Output does not exist") 

        # 2: Check the features created 
        self.assertFeatureClassEqual(compareDataset,
                                     output,
                                     arcpy.Describe(output).oidFieldName,
                                     None,
                                     "ALL",
                                     self.ignore_options,
                                     self.xy_tolerance)

    # 100M Test
    def testCreateReferenceSystemGRGFromArea_100M(self):
        '''
        Testing with 100M grid
        '''
        Configuration.Logger.debug(".....GRGCreateReferenceSystemGRGFromAreaTestCase.testCreateReferenceSystemGRGFromArea_100M")

        #inputs
        grid_size = "100M_GRID"
        output = os.path.join(Configuration.militaryScratchGDB, "outgrg_100M")

        #Testing
        runToolMsg = "Running tool (CreateReferenceSystemGRGFromArea)"
        arcpy.AddMessage(runToolMsg)
        Configuration.Logger.info(runToolMsg)
        compareDataset = os.path.normpath(os.path.join(Configuration.militaryResultsGDB,
                                                       "Compare100m"))
        toolOutput = None

        try:
            toolOutput = arcpy.CreateReferenceSystemGRGFromArea_mt(self.inputArea,
                                                       self.ref_grid,
                                                       grid_size,
                                                       output,
                                                       self.large_grid_handling)
            arcpy.AddSpatialIndex_management(output)
        except arcpy.ExecuteError:
            UnitTestUtilities.handleArcPyError()
        except:
            UnitTestUtilities.handleGeneralError()

        # 1: Check the expected return value
        self.assertIsNotNone(toolOutput, "No output returned from tool")
        outputOut = toolOutput.getOutput(0)
        self.assertEqual(output, outputOut, "Unexpected return value from tool") 
        self.assertTrue(arcpy.Exists(outputOut), "Output does not exist") 

        # 2: Check the features created 
        self.assertFeatureClassEqual(compareDataset,
                                     output,
                                     arcpy.Describe(output).oidFieldName,
                                     None,
                                     "ALL",
                                     self.ignore_options,
                                     self.xy_tolerance)

    # 10M Test
    def testCreateReferenceSystemGRGFromArea_10M(self):
        '''
        Testing with 10M grid
        '''
        Configuration.Logger.debug(".....GRGCreateReferenceSystemGRGFromAreaTestCase.testCreateReferenceSystemGRGFromArea_10M")

        #inputs
        grid_size = "10M_GRID"
        output = os.path.join(Configuration.militaryScratchGDB, "outgrg_10M")

        #Testing
        runToolMsg = "Running tool (CreateReferenceSystemGRGFromArea)"
        arcpy.AddMessage(runToolMsg)
        Configuration.Logger.info(runToolMsg)
        compareDataset = os.path.normpath(os.path.join(Configuration.militaryResultsGDB,
                                                       "Compare10m"))
        toolOutput = None

        try:
            toolOutput = arcpy.CreateReferenceSystemGRGFromArea_mt(self.inputArea10m,
                                                       self.ref_grid,
                                                       grid_size,
                                                       output,
                                                       self.large_grid_handling)
            arcpy.AddSpatialIndex_management(output)
        except arcpy.ExecuteError:
            UnitTestUtilities.handleArcPyError()
        except:
            UnitTestUtilities.handleGeneralError()

        # 1: Check the expected return value
        self.assertIsNotNone(toolOutput, "No output returned from tool")
        outputOut = toolOutput.getOutput(0)
        self.assertEqual(output, outputOut, "Unexpected return value from tool") 
        self.assertTrue(arcpy.Exists(outputOut), "Output does not exist") 

        # 2: Check the features created 
        self.assertFeatureClassEqual(compareDataset,
                                     output,
                                     arcpy.Describe(output).oidFieldName,
                                     None,
                                     "ALL",
                                     self.ignore_options,
                                     self.xy_tolerance)

    # Check that no large grids created for 10m
    def testCreateReferenceSystemGRGFromArea_10mNoLargeGrids(self):
        '''
        Testing tool will raise error with NO_LARGE_GRIDS option.
        '''
        Configuration.Logger.debug(".....GRGCreateReferenceSystemGRGFromAreaTestCase.testCreateReferenceSystemGRGFromArea_10mNoLargeGrids")

        #inputs
        grid_size = "10M_GRID"
        output = os.path.join(Configuration.militaryScratchGDB, "outgrg_10M_fail")

        #Testing
        runToolMsg = "Running tool (CreateReferenceSystemGRGFromArea)"
        arcpy.AddMessage(runToolMsg)
        Configuration.Logger.info(runToolMsg)

        with self.assertRaises(arcpy.ExecuteError) as manage_raise:
            arcpy.CreateReferenceSystemGRGFromArea_mt(self.inputArea10m,
                                                       self.ref_grid,
                                                       grid_size,
                                                       output,
                                                       "NO_LARGE_GRIDS")
        self.assertTrue('exceeds large grid value for' in str(manage_raise.exception))

if __name__ == "__main__":
    unittest.main()   
