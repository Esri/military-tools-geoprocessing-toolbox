# coding: utf-8
'''
-----------------------------------------------------------------------------
Copyright 2016 Esri
Licensed under the Apache License, Version 2.0 (the "License");
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
TableToPointTestCase.py
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

class TableToPointTestCase(unittest.TestCase, arcpyAssert.FeatureClassAssertMixin):
    ''' Test all tools and methods related to the Table To Point tool
    in the Military Tools toolbox'''

    inputTable = None
    outputPoints = None
    baseFC = None

    @classmethod
    def setUpClass(cls):
        # Run once per class creation
        ''' Initialization needed if running Test Case standalone '''
        Configuration.GetLogger()
        Configuration.GetPlatform()
        ''' End standalone initialization '''
            
        Configuration.Logger.debug("     TableToPointTestCase.setUpClass")    
        UnitTestUtilities.checkArcPy()

        if not arcpy.Exists(Configuration.militaryScratchGDB):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.currentPath)

        Configuration.Logger.debug("Import Toolbox: " + Configuration.toolboxUnderTest)
        arcpy.ImportToolbox(Configuration.toolboxUnderTest)  
        Configuration.Logger.debug("Done Toolbox Import")

    @classmethod
    def tearDownClass(cls):
        Configuration.Logger.debug("     TableToPointTestCase.tearDownClass")
        # UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)

    def setUp(self):

        Configuration.Logger.debug("     TableToPointTestCase.setUp")

        csvFolder = os.path.join(Configuration.militaryDataPath, "CSV")
        self.inputTable = os.path.join(csvFolder, "TableToPoint.csv")
        self.inputSingleTable = os.path.join(csvFolder, "TableToPoint_single.csv")
        self.inputTableDifferentSR = os.path.join(csvFolder, "POI_UTM_X_Y.csv")
        self.baseFC = os.path.join(Configuration.militaryResultsGDB, "ExpectedOutputTableToPoint")
        
        UnitTestUtilities.checkGeoObjects([Configuration.toolboxUnderTest, \
            self.baseFC])
        UnitTestUtilities.checkFilePaths([self.inputTable, self.inputSingleTable])

        self.outputPoints = os.path.join(Configuration.militaryScratchGDB, "outputTableToPoint")

    def tearDown(self):
        Configuration.Logger.debug("     TableToPointTestCase.tearDown")
        # UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)

    def test_table_to_point(self):
        '''Test Table To Point for ArcGIS Desktop'''

        Configuration.Logger.info(".....TableToPointTestCase.test_table_to_point")

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputPoints) :
            arcpy.Delete_management(self.outputPoints)

        arcpy.TableToPoint_mt(self.inputTable, "DD_2", "x", "y", self.outputPoints)

        self.assertTrue(arcpy.Exists(self.outputPoints), "Output features do not exist or were not created")
        pointCount = int(arcpy.GetCount_management(self.outputPoints).getOutput(0))
        expectedFeatures = int(1000)
        self.assertEqual(pointCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(pointCount)))

        # TODO: Needs correct known good results featureclass
        #attribute_tolerances = 'DDLat 0.00001;DDLon 0.00001' 
        #xy_tolerance = 0.0001
        #self.assertFeatureClassEqualSimple(self.baseFC, self.outputPoints, \
        #                             "OID", xy_tolerance, attribute_tolerances)

        return

    def test_table_to_point_different_SR(self):
        '''Test Table To Point with a different Spatial Reference (SR) for ArcGIS Desktop'''

        Configuration.Logger.info(".....TableToPointTestCase.test_table_to_point_different_SR")

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputPoints) :
            arcpy.Delete_management(self.outputPoints)

        napervilleSR = arcpy.SpatialReference(3443) # 3443 = NAD_1983_HARN_StatePlane_Illinois_East_FIPS_1201_Feet

        arcpy.TableToPoint_mt(self.inputTableDifferentSR, "DD_2", "POINT_X", "POINT_Y", self.outputPoints, napervilleSR)

        self.assertTrue(arcpy.Exists(self.outputPoints), "Output features do not exist or were not created")
        pointCount = int(arcpy.GetCount_management(self.outputPoints).getOutput(0))
        expectedFeatures = int(1000)
        self.assertEqual(pointCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(pointCount)))

        # Make sure there are no empty geometries

        # Open Search cursor on output points
        inFields = ["SHAPE@", "ORIG_OID"]
        inRows = arcpy.da.SearchCursor(self.outputPoints, inFields)
        for row in inRows:
            featShape = row[0]
            origOid = row[1]

            self.assertIsNotNone(featShape, "Output feature shape should not be None")
            self.assertIsNotNone(origOid, "Output feature field should not be None")

        return

    def test_table_to_point_MGRS(self):
        '''Test Table To Point for ArcGIS Desktop_MGRS'''

        Configuration.Logger.info(".....TableToPointTestCase.test_table_to_point_MGRS")

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputPoints) :
            arcpy.Delete_management(self.outputPoints)

        arcpy.TableToPoint_mt(self.inputSingleTable, "MGRS", "MGRS", None, self.outputPoints)

        self.assertTrue(arcpy.Exists(self.outputPoints), "Output features do not exist or were not created")
        pointCount = int(arcpy.GetCount_management(self.outputPoints).getOutput(0))
        expectedFeatures = int(1000)
        self.assertEqual(pointCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(pointCount)))

        # TODO: Needs correct known good results featureclass
        # self.assertFeatureClassEqualSimple(self.baseFC, self.outputPoints, \
        #                             "OID", 0.0001)

        return

    def test_table_to_point_GARS(self):
        '''Test Table To Point for ArcGIS Desktop_GARS'''

        Configuration.Logger.info(".....TableToPointTestCase.test_table_to_point_GARS")

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputPoints) :
            arcpy.Delete_management(self.outputPoints)

        arcpy.TableToPoint_mt(self.inputSingleTable, "GARS", "GARS", None, self.outputPoints)

        self.assertTrue(arcpy.Exists(self.outputPoints), "Output features do not exist or were not created")
        pointCount = int(arcpy.GetCount_management(self.outputPoints).getOutput(0))
        expectedFeatures = int(1000)
        self.assertEqual(pointCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(pointCount)))

        # TODO: Needs correct known good results featureclass
        # self.assertFeatureClassEqualSimple(self.baseFC, self.outputPoints, \
        #                             "OID", 0.0001)

        return

    def test_table_to_point_GEOREF(self):
        '''Test Table To Point for ArcGIS Desktop_GEOREF'''

        Configuration.Logger.info(".....TableToPointTestCase.test_table_to_point_GEOREF")

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputPoints) :
            arcpy.Delete_management(self.outputPoints)

        arcpy.TableToPoint_mt(self.inputSingleTable, "GEOREF", "GEOREF", None, self.outputPoints)

        self.assertTrue(arcpy.Exists(self.outputPoints), "Output features do not exist or were not created")
        pointCount = int(arcpy.GetCount_management(self.outputPoints).getOutput(0))
        expectedFeatures = int(1000)
        self.assertEqual(pointCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(pointCount)))

        # TODO: Needs correct known good results featureclass
        # self.assertFeatureClassEqualSimple(self.baseFC, self.outputPoints, \
        #                             "OID", 0.0001)

        return

    def test_table_to_point_USNG(self):
        '''Test Table To Point for ArcGIS Desktop_USNG'''

        Configuration.Logger.info(".....TableToPointTestCase.test_table_to_point_USNG")

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputPoints) :
            arcpy.Delete_management(self.outputPoints)

        arcpy.TableToPoint_mt(self.inputSingleTable, "USNG", "USNG", None, self.outputPoints)

        self.assertTrue(arcpy.Exists(self.outputPoints), "Output features do not exist or were not created")
        pointCount = int(arcpy.GetCount_management(self.outputPoints).getOutput(0))
        expectedFeatures = int(1000)
        self.assertEqual(pointCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(pointCount)))

        # TODO: Needs correct known good results featureclass
        # self.assertFeatureClassEqualSimple(self.baseFC, self.outputPoints, \
        #                             "OID", 0.0001)

        return

    def test_table_to_point_UTM_BANDS(self):
        '''Test Table To Point for ArcGIS Desktop_UTM_BANDS'''

        Configuration.Logger.info(".....TableToPointTestCase.test_table_to_point_UTM_BANDS")

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputPoints) :
            arcpy.Delete_management(self.outputPoints)

        arcpy.TableToPoint_mt(self.inputSingleTable, "UTM_BANDS", "UTM", None, self.outputPoints)

        self.assertTrue(arcpy.Exists(self.outputPoints), "Output features do not exist or were not created")
        pointCount = int(arcpy.GetCount_management(self.outputPoints).getOutput(0))
        expectedFeatures = int(1000)
        self.assertEqual(pointCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(pointCount)))

        # TODO: Needs correct known good results featureclass
        # self.assertFeatureClassEqualSimple(self.baseFC, self.outputPoints, \
        #                             "OID", 0.0001)

        return

if __name__ == "__main__":
    unittest.main()
