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
TableToLineOfBearingTestCase.py
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

class TableToLineOfBearingTestCase(unittest.TestCase, arcpyAssert.FeatureClassAssertMixin):
    ''' Test all tools and methods related to the Table To Line Of Bearing tool
    in the Military Tools toolbox'''
    
    inputTable = None
    outputLineOfBearing = None
    baseFC = None
    platform = None
  
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

        Configuration.Logger.debug("     TableToLineOfBearingTestCase.setUp")    
      
        csvFolder = os.path.join(Configuration.militaryDataPath, "CSV")
        self.inputTable = os.path.join(csvFolder, "TabletoLineOfBearing.csv")
        self.inputSingleTable = os.path.join(csvFolder, "TableToLineOfBearing_single.csv")
        self.baseFC = os.path.join(Configuration.militaryResultsGDB, "ExpectedOutputTableToLOB")

        UnitTestUtilities.checkGeoObjects([Configuration.toolboxUnderTest, \
            self.baseFC])
        UnitTestUtilities.checkFilePaths([self.inputTable, self.inputSingleTable])

        self.outputLineOfBearing = os.path.join(Configuration.militaryScratchGDB, "outputLines")
                
    def tearDown(self):
        Configuration.Logger.debug("     TableToLineOfBearingTestCase.tearDown")
    
    def test_table_to_lineofbearing(self):
        '''Test Table To Line Of Bearing for ArcGIS'''

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputLineOfBearing) :
            arcpy.Delete_management(self.outputLineOfBearing)

        Configuration.Logger.info(".....TableToLineOfBearingTestCase.test_table_to_lineofbearing")

        arcpy.TableToLineOfBearing_mt(self.inputTable, "DD_2", "x", "y", "DEGREES", "Orientation", \
            "METERS", "Distance", self.outputLineOfBearing, "GEODESIC", None)

        self.assertTrue(arcpy.Exists(self.outputLineOfBearing), "Output features do not exist or were not created")
        featureCount = int(arcpy.GetCount_management(self.outputLineOfBearing).getOutput(0))
        expectedFeatures = int(23)
        self.assertEqual(featureCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(featureCount)))

        # Set tolerances for compare
        attribute_tolerances = 'Shape_Length 0.0001;DDLat 0.00001;DDLon 0.00001' 
        xy_tolerance = 0.0001
        self.assertFeatureClassEqualSimple(self.baseFC, self.outputLineOfBearing, \
                                     "OID", xy_tolerance, attribute_tolerances)

        return

    def test_table_to_lineofbearing_GARS(self):
        '''Test Table To Line Of Bearing for ArcGIS_GARS'''

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputLineOfBearing) :
            arcpy.Delete_management(self.outputLineOfBearing)
    
        Configuration.Logger.info(".....TableToLineOfBearingTestCase.test_table_to_lineofbearing_GARS")

        arcpy.TableToLineOfBearing_mt(self.inputSingleTable, "GARS", "GARS", None, "DEGREES", "Orientation", "METERS", "Distance", self.outputLineOfBearing, "GEODESIC", None)

        self.assertTrue(arcpy.Exists(self.outputLineOfBearing), "Output features do not exist or were not created")
        featureCount = int(arcpy.GetCount_management(self.outputLineOfBearing).getOutput(0))
        expectedFeatures = int(23)
        self.assertEqual(featureCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(featureCount)))

        # TODO: Needs correct known good results featureclass
        # self.assertFeatureClassEqual(self.baseFC, self.outputLineOfBearing, \
        #                             "OBJECTID")

        return

    def test_table_to_lineofbearing_GEOREF(self):
        '''Test Table To Line Of Bearing for ArcGIS_GEOREF'''

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputLineOfBearing) :
            arcpy.Delete_management(self.outputLineOfBearing)
    
        Configuration.Logger.info(".....TableToLineOfBearingTestCase.test_table_to_lineofbearing_GEOREF")

        arcpy.TableToLineOfBearing_mt(self.inputSingleTable, "GEOREF", "GEOREF", None, "DEGREES", "Orientation", "METERS", "Distance", self.outputLineOfBearing, "GEODESIC", None)

        self.assertTrue(arcpy.Exists(self.outputLineOfBearing), "Output features do not exist or were not created")
        featureCount = int(arcpy.GetCount_management(self.outputLineOfBearing).getOutput(0))
        expectedFeatures = int(23)
        self.assertEqual(featureCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(featureCount)))

        # TODO: Needs correct known good results featureclass
        # self.assertFeatureClassEqual(self.baseFC, self.outputLineOfBearing, \
        #                             "OBJECTID")

        return

    def test_table_to_lineofbearing_USNG(self):
        '''Test Table To Line Of Bearing for ArcGIS_USNG'''

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputLineOfBearing) :
            arcpy.Delete_management(self.outputLineOfBearing)
    
        Configuration.Logger.info(".....TableToLineOfBearingTestCase.test_table_to_lineofbearing_USNG")

        arcpy.TableToLineOfBearing_mt(self.inputSingleTable, "USNG", "USNG", None, "DEGREES", "Orientation", "METERS", "Distance", self.outputLineOfBearing, "GEODESIC", None)

        self.assertTrue(arcpy.Exists(self.outputLineOfBearing), "Output features do not exist or were not created")
        featureCount = int(arcpy.GetCount_management(self.outputLineOfBearing).getOutput(0))
        expectedFeatures = int(23)
        self.assertEqual(featureCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(featureCount)))

        # TODO: Needs correct known good results featureclass
        # self.assertFeatureClassEqual(self.baseFC, self.outputLineOfBearing, \
        #                             "OBJECTID")

        return

    def test_table_to_lineofbearing_MGRS(self):
        '''Test Table To Line Of Bearing for ArcGIS_MGRS'''

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputLineOfBearing) :
            arcpy.Delete_management(self.outputLineOfBearing)
    
        Configuration.Logger.info(".....TableToLineOfBearingTestCase.test_table_to_lineofbearing_MGRS")

        arcpy.TableToLineOfBearing_mt(self.inputSingleTable, "MGRS", "MGRS", None, "DEGREES", "Orientation", "METERS", "Distance", self.outputLineOfBearing, "GEODESIC", None)

        self.assertTrue(arcpy.Exists(self.outputLineOfBearing), "Output features do not exist or were not created")
        featureCount = int(arcpy.GetCount_management(self.outputLineOfBearing).getOutput(0))
        expectedFeatures = int(23)
        self.assertEqual(featureCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(featureCount)))

        # TODO: Needs correct known good results featureclass
        # self.assertFeatureClassEqual(self.baseFC, self.outputLineOfBearing, \
        #                             "OBJECTID")

        return

    def test_table_to_lineofbearing_UTM_BANDS(self):
        '''Test Table To Line Of Bearing for ArcGIS_UTM_BANDS'''

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputLineOfBearing) :
            arcpy.Delete_management(self.outputLineOfBearing)
    
        Configuration.Logger.info(".....TableToLineOfBearingTestCase.test_table_to_lineofbearing_UTM_BANDS")

        arcpy.TableToLineOfBearing_mt(self.inputSingleTable, "UTM_BANDS", "UTM", None, "DEGREES", "Orientation", "METERS", "Distance", self.outputLineOfBearing, "GEODESIC", None)

        self.assertTrue(arcpy.Exists(self.outputLineOfBearing), "Output features do not exist or were not created")
        featureCount = int(arcpy.GetCount_management(self.outputLineOfBearing).getOutput(0))
        expectedFeatures = int(23)
        self.assertEqual(featureCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(featureCount)))

        # TODO: Needs correct known good results featureclass
        # self.assertFeatureClassEqual(self.baseFC, self.outputLineOfBearing, \
        #                             "OBJECTID")

        return

if __name__ == "__main__":
    unittest.main()