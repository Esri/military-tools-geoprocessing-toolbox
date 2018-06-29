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
# TableToEllipseTestCase.py
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
# 12/9/2016 - MF - added single field input tests
# ==================================================

import os
import unittest

import arcpy

# Add parent folder to python path if running test case standalone
import sys
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))

import UnitTestUtilities
import Configuration
import arcpyAssert

class TableToEllipseTestCase(unittest.TestCase, arcpyAssert.FeatureClassAssertMixin):
    ''' Test all tools and methods related to the Table To Ellipse tool
    in the Military Tools toolbox'''
    
    inputTable = None
    outputEllipses = None
    baseFC = None
    
    @classmethod
    def setUpClass(cls):
        # Run once per class creation
        ''' Initialization needed if running Test Case standalone '''
        Configuration.GetLogger()
        Configuration.GetPlatform()
        ''' End standalone initialization '''
            
        Configuration.Logger.debug("     TableToEllipseTestCase.setUpClass")    
        UnitTestUtilities.checkArcPy()

        if not arcpy.Exists(Configuration.militaryScratchGDB):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.currentPath)

        Configuration.Logger.debug("Import Toolbox: " + Configuration.toolboxUnderTest)
        arcpy.ImportToolbox(Configuration.toolboxUnderTest)  
        Configuration.Logger.debug("Done Toolbox Import")

    @classmethod
    def tearDownClass(cls):
        Configuration.Logger.debug("     TableToEllipseTestCase.tearDownClass")
        # UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)

    def setUp(self):
        # Run before each test case
        Configuration.Logger.debug("     TableToEllipseTestCase.setUp")    

        csvPath = os.path.join(Configuration.militaryDataPath, "CSV")
        self.inputTable = os.path.join(csvPath, "TableToEllipse.csv")
        self.inputSingleTable = os.path.join(csvPath, "TableToEllipse_single.csv")

        self.baseFC = os.path.join(Configuration.militaryResultsGDB, "ExpectedOutputTableToEllipse")

        UnitTestUtilities.checkGeoObjects([Configuration.toolboxUnderTest, \
            self.baseFC])
        UnitTestUtilities.checkFilePaths([self.inputTable, self.inputSingleTable])

        self.outputEllipses = os.path.join(Configuration.militaryScratchGDB, "outputEllipses")

    def tearDown(self):
        Configuration.Logger.debug("     TableToEllipseTestCase.tearDown")
    
    def test_table_to_ellipse(self):
        '''test_table_to_ellipse '''

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputEllipses) :
            arcpy.Delete_management(self.outputEllipses)

        Configuration.Logger.info(".....TableToEllipseTestCase.test_table_to_ellipse")

        arcpy.TableToEllipse_mt(self.inputTable, "DD_2", "x", "y", "Major", "Minor", \
            "KILOMETERS", self.outputEllipses, "Orient", "DEGREES")

        self.assertTrue(arcpy.Exists(self.outputEllipses), "Output dataset does not exist.")
        ellipseCount = int(arcpy.GetCount_management(self.outputEllipses).getOutput(0))
        expectedFeatures = int(23)
        self.assertEqual(ellipseCount, expectedFeatures, \
            "Expected %s features but got %s" % (str(expectedFeatures),str(ellipseCount)))

        attribute_tolerances = 'Shape_Length 0.0001;Shape_Area 0.0001;DDLat 0.00001;DDLon 0.00001' 
        xy_tolerance = 0.0001
        self.assertFeatureClassEqualSimple(self.baseFC, self.outputEllipses, \
                                     "OBJECTID", xy_tolerance, attribute_tolerances)

        return

    def test_table_to_ellipse_GARS(self):
        '''test_table_to_ellipse_GARS '''

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputEllipses) :
            arcpy.Delete_management(self.outputEllipses)

        Configuration.Logger.info(".....TableToEllipseTestCase.test_table_to_ellipse_GARS")

        arcpy.TableToEllipse_mt(self.inputSingleTable, "GARS", "GARS", None, \
            "Major", "Minor", "KILOMETERS", self.outputEllipses)

        self.assertTrue(arcpy.Exists(self.outputEllipses), "Output dataset does not exist.")
        ellipseCount = int(arcpy.GetCount_management(self.outputEllipses).getOutput(0))
        expectedFeatures = int(23)
        self.assertEqual(ellipseCount, expectedFeatures, "Expected %s features but got %s" % (str(expectedFeatures),str(ellipseCount)))

        # TODO: Needs correct known good results featureclass
        # self.assertFeatureClassEqual(self.baseFC, self.outputEllipses, \
        #                             "OBJECTID")

        return

    def test_table_to_ellipse_GEOREF(self):
        '''test_table_to_ellipse_GEOREF '''

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputEllipses) :
            arcpy.Delete_management(self.outputEllipses)

        Configuration.Logger.info(".....TableToEllipseTestCase.test_table_to_ellipse_GEOREF")

        arcpy.TableToEllipse_mt(self.inputSingleTable, "GEOREF", "GEOREF", None, \
            "Major", "Minor", "KILOMETERS", self.outputEllipses)

        self.assertTrue(arcpy.Exists(self.outputEllipses), "Output dataset does not exist.")
        ellipseCount = int(arcpy.GetCount_management(self.outputEllipses).getOutput(0))
        expectedFeatures = int(23)
        self.assertEqual(ellipseCount, expectedFeatures, \
            "Expected %s features but got %s" % (str(expectedFeatures),str(ellipseCount)))

        # TODO: Needs correct known good results featureclass
        # self.assertFeatureClassEqual(self.baseFC, self.outputEllipses, \
        #                             "OBJECTID")

        return

    def test_table_to_ellipse_USNG(self):
        '''test_table_to_ellipse_USNG '''

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputEllipses) :
            arcpy.Delete_management(self.outputEllipses)
    
        Configuration.Logger.info(".....TableToEllipseTestCase.test_table_to_ellipse_USNG")

        arcpy.TableToEllipse_mt(self.inputSingleTable, "USNG", "USNG", None, \
            "Major", "Minor", "KILOMETERS", self.outputEllipses)

        self.assertTrue(arcpy.Exists(self.outputEllipses), "Output dataset does not exist.")
        ellipseCount = int(arcpy.GetCount_management(self.outputEllipses).getOutput(0))
        expectedFeatures = int(23)
        self.assertEqual(ellipseCount, expectedFeatures, \
            "Expected %s features but got %s" % (str(expectedFeatures),str(ellipseCount)))

        # TODO: Needs correct known good results featureclass
        # self.assertFeatureClassEqual(self.baseFC, self.outputEllipses, \
        #                             "OBJECTID")

        return

    def test_table_to_ellipse_MGRS(self):
        '''test_table_to_ellipse_MGRS '''

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputEllipses) :
            arcpy.Delete_management(self.outputEllipses)

        Configuration.Logger.info(".....TableToEllipseTestCase.test_table_to_ellipse_USNG")

        arcpy.TableToEllipse_mt(self.inputSingleTable, "MGRS", "MGRS", None, \
            "Major", "Minor", "KILOMETERS", self.outputEllipses)

        self.assertTrue(arcpy.Exists(self.outputEllipses), "Output dataset does not exist.")
        ellipseCount = int(arcpy.GetCount_management(self.outputEllipses).getOutput(0))
        expectedFeatures = int(23)
        self.assertEqual(ellipseCount, expectedFeatures, \
            "Expected %s features but got %s" % (str(expectedFeatures),str(ellipseCount)))

        # TODO: Needs correct known good results featureclass
        # self.assertFeatureClassEqual(self.baseFC, self.outputEllipses, \
        #                             "OBJECTID")

        return

    def test_table_to_ellipse_UTM_BANDS(self):
        '''test_table_to_ellipse_UTM_BANDS '''

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputEllipses) :
            arcpy.Delete_management(self.outputEllipses)

        Configuration.Logger.info(".....TableToEllipseTestCase.test_table_to_ellipse_UTM_BANDS")

        arcpy.TableToEllipse_mt(self.inputSingleTable, "UTM_BANDS", "UTM", None, \
            "Major", "Minor", "KILOMETERS", self.outputEllipses)

        self.assertTrue(arcpy.Exists(self.outputEllipses), "Output dataset does not exist.")
        ellipseCount = int(arcpy.GetCount_management(self.outputEllipses).getOutput(0))
        expectedFeatures = int(23)
        self.assertEqual(ellipseCount, expectedFeatures, \
            "Expected %s features but got %s" % (str(expectedFeatures),str(ellipseCount)))

        # TODO: Needs correct known good results featureclass
        # self.assertFeatureClassEqual(self.baseFC, self.outputEllipses, \
        #                             "OBJECTID")

        return

if __name__ == "__main__":
    unittest.main()
