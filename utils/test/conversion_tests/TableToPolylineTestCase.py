# coding: utf-8
'''
-----------------------------------------------------------------------------
Copyright 2016 Esri
Licensed ungder the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-----------------------------------------------------------------------------

==================================================
TableToPolylineTestCase.py
--------------------------------------------------
requirements:
* ArcGIS Desktop 10.X+ or ArcGIS Pro 1.X+
* Python 2.7 or Python 3.4

author: ArcGIS Solutions
company: Esri

==================================================
history:
5/11/2016 - JH - initial creation
6/1/2016 - MF - update error handling
==================================================
'''

import os
import unittest

import arcpy

# Add parent folder to python path if running test case standalone
import sys
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))

import UnitTestUtilities
import Configuration
import arcpyAssert

class TableToPolylineTestCase(unittest.TestCase, arcpyAssert.FeatureClassAssertMixin):
    ''' Test all tools and methods related to the Table To Polyline tool
    in the Military Tools toolbox'''
    
    inputTable = None
    outputPolylines = None
    baseFC = None
    
    @classmethod
    def setUpClass(cls):
        # Run once per class creation
        ''' Initialization needed if running Test Case standalone '''
        Configuration.GetLogger()
        Configuration.GetPlatform()
        ''' End standalone initialization '''
            
        Configuration.Logger.debug("     TableToPolylineTestCase.setUpClass")    
        UnitTestUtilities.checkArcPy()

        if not arcpy.Exists(Configuration.militaryScratchGDB):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.currentPath)

        Configuration.Logger.debug("Import Toolbox: " + Configuration.toolboxUnderTest)
        arcpy.ImportToolbox(Configuration.toolboxUnderTest)  
        Configuration.Logger.debug("Done Toolbox Import")

    @classmethod
    def tearDownClass(cls):
        Configuration.Logger.debug("     TableToPolylineTestCase.tearDownClass")
        # UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)

    def setUp(self):
           
        Configuration.Logger.debug("     TableToPolylineTestCase.setUp")    

        csvPath = os.path.join(Configuration.militaryDataPath, "CSV")
        self.inputTable = os.path.join(csvPath, "TabletoPolyline.csv")
        self.inputSingleTable = os.path.join(csvPath, "TableToPolyline_single.csv")
        self.baseFC = os.path.join(Configuration.militaryResultsGDB, "ExpectedOutputTableToPolyline")

        UnitTestUtilities.checkGeoObjects([Configuration.toolboxUnderTest, \
            self.baseFC])
        UnitTestUtilities.checkFilePaths([self.inputTable, self.inputSingleTable])

        self.outputPolylines = os.path.join(Configuration.militaryScratchGDB, "outputPolylines")
                        
    def tearDown(self):
        Configuration.Logger.debug("     TableToPolylineTestCase.tearDown")
    
    def test_table_to_polyline(self):
        '''Test Table To Polyline for ArcGIS Desktop'''

        Configuration.Logger.info(".....TableToPolylineTestCase.test_table_to_polyline")

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputPolylines) :
            arcpy.Delete_management(self.outputPolylines)


        toolOutput = arcpy.TableToPolyline_mt(self.inputTable, "DD_2", "POINT_X", "POINT_Y", \
            self.outputPolylines, "Group_")


        # 1: Check the expected return value
        self.assertIsNotNone(toolOutput, "No output returned from tool")
        outputOut = toolOutput.getOutput(0)
        self.assertEqual(self.outputPolylines, outputOut, "Unexpected return value from tool")
        self.assertTrue(arcpy.Exists(self.outputPolylines), "Output features do not exist or were not created")

        # Process to check tool results for grouping
        # Step 1: Make in_memory table to get frequency of
        inMemTable = arcpy.TableToTable_conversion(self.inputTable, "in_memory", "TableToPolyline_single_In_Mem")

        # Step 2: Get the frequency of unique "group values" in the input table
        # Get Frequency of the unique names in the input table
        freqInputTable = arcpy.Frequency_analysis(inMemTable, "in_memory\\CountOfUniqueNames", "Group_", "")

        # Get Count of the unique names
        freqTableCount = arcpy.GetCount_management(freqInputTable)
        expectedFeatureCount = int(freqTableCount.getOutput(0))
        polylineCount = int(arcpy.GetCount_management(self.outputPolylines).getOutput(0))
        self.assertEqual(polylineCount, expectedFeatureCount, "Expected %s features, but got %s" % (str(expectedFeatureCount), str(polylineCount)))

        # Tool is not producing correct output - commented out check for now
        # See: https://github.com/Esri/military-tools-geoprocessing-toolbox/issues/254
        # self.assertFeatureClassEqualSimple(self.baseFC, self.outputPolylines, \
        #                        "OBJECTID", 0.0001)

        return  



    def test_table_to_polyline_MGRS(self):
        '''Test Table To Polyline for ArcGIS Desktop_MGRS'''

        Configuration.Logger.info(".....TableToPolylineTestCase.test_table_to_polyline_MGRS")

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputPolylines) :
            arcpy.Delete_management(self.outputPolylines)

        arcpy.TableToPolyline_mt(self.inputSingleTable, "MGRS", "MGRS", None, self.outputPolylines)

        self.assertTrue(arcpy.Exists(self.outputPolylines), "Output features do not exist or were not created")
        polylineCount = int(arcpy.GetCount_management(self.outputPolylines).getOutput(0))
        expectedFeatures = int(1)
        self.assertEqual(polylineCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(polylineCount)))

        # TODO: Needs correct known good results featureclass
        # self.assertFeatureClassEqual(self.baseFC, self.outputPolylines, \
        #                             "OBJECTID")

        return 

    def test_table_to_polyline_GARS(self):
        '''Test Table To Polyline for ArcGIS Desktop_GARS'''

        Configuration.Logger.info(".....TableToPolylineTestCase.test_table_to_polyline_GARS")

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputPolylines) :
            arcpy.Delete_management(self.outputPolylines)

        arcpy.TableToPolyline_mt(self.inputSingleTable, "GARS", "GARS", None, self.outputPolylines)

        self.assertTrue(arcpy.Exists(self.outputPolylines), "Output features do not exist or were not created")
        polylineCount = int(arcpy.GetCount_management(self.outputPolylines).getOutput(0))
        expectedFeatures = int(1)
        self.assertEqual(polylineCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(polylineCount)))

        # TODO: Needs correct known good results featureclass
        # self.assertFeatureClassEqual(self.baseFC, self.outputPolylines, \
        #                             "OBJECTID")

        return 

    def test_table_to_polyline_GEOREF(self):
        '''Test Table To Polyline for ArcGIS Desktop_GEOREF'''

        Configuration.Logger.info(".....TableToPolylineTestCase.test_table_to_polyline_GEOREF")

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputPolylines) :
            arcpy.Delete_management(self.outputPolylines)

        arcpy.TableToPolyline_mt(self.inputSingleTable, "GEOREF", "GEOREF", None, self.outputPolylines)

        self.assertTrue(arcpy.Exists(self.outputPolylines), "Output features do not exist or were not created")
        polylineCount = int(arcpy.GetCount_management(self.outputPolylines).getOutput(0))
        expectedFeatures = int(1)
        self.assertEqual(polylineCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(polylineCount)))

        # TODO: Needs correct known good results featureclass
        # self.assertFeatureClassEqual(self.baseFC, self.outputPolylines, \
        #                             "OBJECTID")

        return 

    def test_table_to_polyline_USNG(self):
        '''Test Table To Polyline for ArcGIS Desktop_USNG'''

        Configuration.Logger.info(".....TableToPolylineTestCase.test_table_to_polyline_USNG")

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputPolylines) :
            arcpy.Delete_management(self.outputPolylines)

        arcpy.TableToPolyline_mt(self.inputSingleTable, "USNG", "USNG", None, self.outputPolylines)

        self.assertTrue(arcpy.Exists(self.outputPolylines), "Output features do not exist or were not created")
        polylineCount = int(arcpy.GetCount_management(self.outputPolylines).getOutput(0))
        expectedFeatures = int(1)
        self.assertEqual(polylineCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(polylineCount)))

        # TODO: Needs correct known good results featureclass
        # self.assertFeatureClassEqual(self.baseFC, self.outputPolylines, \
        #                             "OBJECTID")

        return 

    def test_table_to_polyline_UTM_BANDS(self):
        '''Test Table To Polyline for ArcGIS Desktop_UTM_BANDS'''

        Configuration.Logger.info(".....TableToPolylineTestCase.test_table_to_polyline_UTM_BANDS")

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputPolylines) :
            arcpy.Delete_management(self.outputPolylines)

        arcpy.TableToPolyline_mt(self.inputSingleTable, "UTM_BANDS", "UTM", None, self.outputPolylines)

        self.assertTrue(arcpy.Exists(self.outputPolylines), "Output features do not exist or were not created")
        polylineCount = int(arcpy.GetCount_management(self.outputPolylines).getOutput(0))
        expectedFeatures = int(1)
        self.assertEqual(polylineCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(polylineCount)))

        # TODO: Needs correct known good results featureclass
        # self.assertFeatureClassEqual(self.baseFC, self.outputPolylines, \
        #                             "OBJECTID")

        return 

    def test_table_to_polyline_check_vertex_count(self):
        '''Test Table To Polyline to verify that a last vertex is not being added to close the line to a polygon'''
        # Test for issue 254

        Configuration.Logger.info(".....TableToPolylineTestCase.test_table_to_polyline_check_vertex_count")

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputPolylines) :
            arcpy.Delete_management(self.outputPolylines)


        toolOutput = arcpy.TableToPolyline_mt(self.inputTable, "DD_2", "POINT_X", "POINT_Y", \
            self.outputPolylines, "Group_")


        # 1: Check the expected return value
        self.assertIsNotNone(toolOutput, "No output returned from tool")
        outputOut = toolOutput.getOutput(0)
        self.assertEqual(self.outputPolylines, outputOut, "Unexpected return value from tool")

        # 2: Count the number of vertices in the output to see that it matches the number of rows in input table
        # Set counter to 0
        vertex_count = 0
        # Enter for loop for each feature
        for row in arcpy.da.SearchCursor(outputOut, ["OID@", "SHAPE@"]):
            partnum = 0
            # Step through each part of the feature
            for part in row[1]:
                # Step through each vertex in the feature
                for pnt in part:
                    if pnt:
                        # Increment the vertex count
                        vertex_count += 1
                    else:
                        # If pnt is None, this represents an interior ring
                        print("Interior Ring:")
                partnum += 1

        # 3: Check if this count matches the number of input table rows
        input_table_row_count = int(arcpy.GetCount_management(self.inputTable).getOutput(0))
        self.assertEqual(vertex_count, input_table_row_count, "Expected %s vertices, but got %s" % (str(input_table_row_count), str(vertex_count)))
        return


if __name__ == "__main__":
    unittest.main()
