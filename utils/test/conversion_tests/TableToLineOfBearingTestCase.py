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

import unittest
import arcpy
import os
import UnitTestUtilities
import Configuration

class TableToLineOfBearingTestCase(unittest.TestCase):
    ''' Test all tools and methods related to the Table To Line Of Bearing tool
    in the Military Tools toolbox'''
    
    inputTable = None
    outputLineOfBearing = None
    proBaseFC = None
    desktopBaseFC = None
    platform = None
    
    def setUp(self):
        if Configuration.DEBUG == True: print("     TableToLineOfBearingTestCase.setUp")    
        
        UnitTestUtilities.checkArcPy()
        if(Configuration.militaryScratchGDB == None) or (not arcpy.Exists(Configuration.militaryScratchGDB)):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.militaryDataPath)
        
        csvFolder = os.path.join(Configuration.militaryDataPath, "CSV")
        self.inputTable = os.path.join(csvFolder, "TabletoLineOfBearing.csv")
        self.inputSingleTable = os.path.join(csvFolder, "TableToLineOfBearing_single.csv")
        self.outputLineOfBearing = os.path.join(Configuration.militaryScratchGDB, "outputLines")
        self.BaseFC = os.path.join(Configuration.militaryResultsGDB, "ExpectedOutputTableToLOB")
        
        UnitTestUtilities.checkFilePaths([Configuration.militaryDataPath, self.inputTable, Configuration.militaryScratchGDB, Configuration.militaryResultsGDB, Configuration.military_ProToolboxPath, Configuration.military_DesktopToolboxPath])
        
    def tearDown(self):
        if Configuration.DEBUG == True: print("     TableToLineOfBearingTestCase.tearDown")
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)
    
    def test_table_to_lineofbearing_desktop(self):
        '''Test Table To Line Of Bearing for ArcGIS Desktop'''
        runToolMessage = ".....TableToLineOfBearingTestCase.test_table_to_lineofbearing_desktop"
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToLineOfBearing_mt(self.inputTable, "DD_2", "x", "y", "DEGREES", "Orientation", "METERS", "Distance", self.outputLineOfBearing, "GEODESIC", None)
        self.assertTrue(arcpy.Exists(self.outputLineOfBearing), "Output features do not exist or were not created")
        featureCount = int(arcpy.GetCount_management(self.outputLineOfBearing).getOutput(0))
        expectedFeatures = int(23)
        self.assertEqual(featureCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(featureCount)))
        compareFeatures = arcpy.FeatureCompare_management(self.BaseFC, self.outputLineOfBearing, "OID")
        # identical = 'true' means that there are no differences between the base and the output feature class
        identical = compareFeatures.getOutput(1)
        self.assertEqual(identical, "true", "Feature compare failed: \n %s" % arcpy.GetMessages())
        return
    def test_table_to_lineofbearing_desktop_GARS(self):
        '''Test Table To Line Of Bearing for ArcGIS Desktop_GARS'''
        runToolMessage = ".....TableToLineOfBearingTestCase.test_table_to_lineofbearing_desktop_GARS"
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToLineOfBearing_mt(self.inputSingleTable, "GARS", "GARS", None, "DEGREES", "Orientation", "METERS", "Distance", self.outputLineOfBearing, "GEODESIC", None)
        self.assertTrue(arcpy.Exists(self.outputLineOfBearing), "Output features do not exist or were not created")
        featureCount = int(arcpy.GetCount_management(self.outputLineOfBearing).getOutput(0))
        expectedFeatures = int(23)
        self.assertEqual(featureCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(featureCount)))
        compareFeatures = arcpy.FeatureCompare_management(self.BaseFC, self.outputLineOfBearing, "OID")
        # identical = 'true' means that there are no differences between the base and the output feature class
        identical = compareFeatures.getOutput(1)
        self.assertEqual(identical, "true", "Feature compare failed: \n %s" % arcpy.GetMessages())
        return
    def test_table_to_lineofbearing_desktop_GEOREF(self):
        '''Test Table To Line Of Bearing for ArcGIS Desktop_GEOREF'''
        runToolMessage = ".....TableToLineOfBearingTestCase.test_table_to_lineofbearing_desktop_GEOREF"
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToLineOfBearing_mt(self.inputSingleTable, "GEOREF", "GEOREF", None, "DEGREES", "Orientation", "METERS", "Distance", self.outputLineOfBearing, "GEODESIC", None)
        self.assertTrue(arcpy.Exists(self.outputLineOfBearing), "Output features do not exist or were not created")
        featureCount = int(arcpy.GetCount_management(self.outputLineOfBearing).getOutput(0))
        expectedFeatures = int(23)
        self.assertEqual(featureCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(featureCount)))
        compareFeatures = arcpy.FeatureCompare_management(self.BaseFC, self.outputLineOfBearing, "OID")
        # identical = 'true' means that there are no differences between the base and the output feature class
        identical = compareFeatures.getOutput(1)
        self.assertEqual(identical, "true", "Feature compare failed: \n %s" % arcpy.GetMessages())
        return
    def test_table_to_lineofbearing_desktop_USNG(self):
        '''Test Table To Line Of Bearing for ArcGIS Desktop_USNG'''
        runToolMessage = ".....TableToLineOfBearingTestCase.test_table_to_lineofbearing_desktop_USNG"
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToLineOfBearing_mt(self.inputSingleTable, "USNG", "USNG", None, "DEGREES", "Orientation", "METERS", "Distance", self.outputLineOfBearing, "GEODESIC", None)
        self.assertTrue(arcpy.Exists(self.outputLineOfBearing), "Output features do not exist or were not created")
        featureCount = int(arcpy.GetCount_management(self.outputLineOfBearing).getOutput(0))
        expectedFeatures = int(23)
        self.assertEqual(featureCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(featureCount)))
        compareFeatures = arcpy.FeatureCompare_management(self.BaseFC, self.outputLineOfBearing, "OID")
        # identical = 'true' means that there are no differences between the base and the output feature class
        identical = compareFeatures.getOutput(1)
        self.assertEqual(identical, "true", "Feature compare failed: \n %s" % arcpy.GetMessages())
        return
    def test_table_to_lineofbearing_desktop_MGRS(self):
        '''Test Table To Line Of Bearing for ArcGIS Desktop_MGRS'''
        runToolMessage = ".....TableToLineOfBearingTestCase.test_table_to_lineofbearing_desktop_MGRS"
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToLineOfBearing_mt(self.inputSingleTable, "MGRS", "MGRS", None, "DEGREES", "Orientation", "METERS", "Distance", self.outputLineOfBearing, "GEODESIC", None)
        self.assertTrue(arcpy.Exists(self.outputLineOfBearing), "Output features do not exist or were not created")
        featureCount = int(arcpy.GetCount_management(self.outputLineOfBearing).getOutput(0))
        expectedFeatures = int(23)
        self.assertEqual(featureCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(featureCount)))
        compareFeatures = arcpy.FeatureCompare_management(self.BaseFC, self.outputLineOfBearing, "OID")
        # identical = 'true' means that there are no differences between the base and the output feature class
        identical = compareFeatures.getOutput(1)
        self.assertEqual(identical, "true", "Feature compare failed: \n %s" % arcpy.GetMessages())
        return
    def test_table_to_lineofbearing_desktop_UTM_BANDS(self):
        '''Test Table To Line Of Bearing for ArcGIS Desktop_UTM_BANDS'''
        runToolMessage = ".....TableToLineOfBearingTestCase.test_table_to_lineofbearing_desktop_UTM_BANDS"
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToLineOfBearing_mt(self.inputSingleTable, "UTM_BANDS", "UTM", None, "DEGREES", "Orientation", "METERS", "Distance", self.outputLineOfBearing, "GEODESIC", None)
        self.assertTrue(arcpy.Exists(self.outputLineOfBearing), "Output features do not exist or were not created")
        featureCount = int(arcpy.GetCount_management(self.outputLineOfBearing).getOutput(0))
        expectedFeatures = int(23)
        self.assertEqual(featureCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(featureCount)))
        compareFeatures = arcpy.FeatureCompare_management(self.BaseFC, self.outputLineOfBearing, "OID")
        # identical = 'true' means that there are no differences between the base and the output feature class
        identical = compareFeatures.getOutput(1)
        self.assertEqual(identical, "true", "Feature compare failed: \n %s" % arcpy.GetMessages())
        return

    def test_table_to_lineofbearing_pro(self):
        '''Test Table To Line Of Bearing for ArcGIS Pro'''
        runToolMessage = ".....TableToLineOfBearingTestCase.test_table_to_lineofbearing_pro"
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToLineOfBearing_mt(self.inputTable, "DD_2", "x", "y", "DEGREES", "Orientation", "METERS", "Distance", self.outputLineOfBearing, "GEODESIC", None)
        self.assertTrue(arcpy.Exists(self.outputLineOfBearing), "Output features do not exist or were not created")
        featureCount = int(arcpy.GetCount_management(self.outputLineOfBearing).getOutput(0))
        expectedFeatures = int(23)
        self.assertEqual(featureCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(featureCount)))
        compareFeatures = arcpy.FeatureCompare_management(self.BaseFC, self.outputLineOfBearing, "OID")
        # identical = 'true' means that there are no differences between the base and the output feature class
        identical = compareFeatures.getOutput(1)
        self.assertEqual(identical, "true", "Feature compare failed: \n %s" % arcpy.GetMessages())
        return
    def test_table_to_lineofbearing_pro_MGRS(self):
        '''Test Table To Line Of Bearing for ArcGIS Pro_MGRS'''
        runToolMessage = ".....TableToLineOfBearingTestCase.test_table_to_lineofbearing_pro_MGRS"
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToLineOfBearing_mt(self.inputSingleTable, "MGRS", "MGRS", None, "DEGREES", "Orientation", "METERS", "Distance", self.outputLineOfBearing, "GEODESIC", None)
        self.assertTrue(arcpy.Exists(self.outputLineOfBearing), "Output features do not exist or were not created")
        featureCount = int(arcpy.GetCount_management(self.outputLineOfBearing).getOutput(0))
        expectedFeatures = int(23)
        self.assertEqual(featureCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(featureCount)))
        compareFeatures = arcpy.FeatureCompare_management(self.BaseFC, self.outputLineOfBearing, "OID")
        # identical = 'true' means that there are no differences between the base and the output feature class
        identical = compareFeatures.getOutput(1)
        self.assertEqual(identical, "true", "Feature compare failed: \n %s" % arcpy.GetMessages())
        return
    def test_table_to_lineofbearing_pro_GARS(self):
        '''Test Table To Line Of Bearing for ArcGIS Pro_GARS'''
        runToolMessage = ".....TableToLineOfBearingTestCase.test_table_to_lineofbearing_pro_GARS"
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToLineOfBearing_mt(self.inputSingleTable, "GARS", "GARS", None, "DEGREES", "Orientation", "METERS", "Distance", self.outputLineOfBearing, "GEODESIC", None)
        self.assertTrue(arcpy.Exists(self.outputLineOfBearing), "Output features do not exist or were not created")
        featureCount = int(arcpy.GetCount_management(self.outputLineOfBearing).getOutput(0))
        expectedFeatures = int(23)
        self.assertEqual(featureCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(featureCount)))
        compareFeatures = arcpy.FeatureCompare_management(self.BaseFC, self.outputLineOfBearing, "OID")
        # identical = 'true' means that there are no differences between the base and the output feature class
        identical = compareFeatures.getOutput(1)
        self.assertEqual(identical, "true", "Feature compare failed: \n %s" % arcpy.GetMessages())
        return
    def test_table_to_lineofbearing_pro_GEOREF(self):
        '''Test Table To Line Of Bearing for ArcGIS Pro_GEOREF'''
        runToolMessage = ".....TableToLineOfBearingTestCase.test_table_to_lineofbearing_pro_GEOREF"
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToLineOfBearing_mt(self.inputSingleTable, "GEOREF", "GEOREF", None, "DEGREES", "Orientation", "METERS", "Distance", self.outputLineOfBearing, "GEODESIC", None)
        self.assertTrue(arcpy.Exists(self.outputLineOfBearing), "Output features do not exist or were not created")
        featureCount = int(arcpy.GetCount_management(self.outputLineOfBearing).getOutput(0))
        expectedFeatures = int(23)
        self.assertEqual(featureCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(featureCount)))
        compareFeatures = arcpy.FeatureCompare_management(self.BaseFC, self.outputLineOfBearing, "OID")
        # identical = 'true' means that there are no differences between the base and the output feature class
        identical = compareFeatures.getOutput(1)
        self.assertEqual(identical, "true", "Feature compare failed: \n %s" % arcpy.GetMessages())
        return
    def test_table_to_lineofbearing_pro_USNG(self):
        '''Test Table To Line Of Bearing for ArcGIS Pro_USNG'''
        runToolMessage = ".....TableToLineOfBearingTestCase.test_table_to_lineofbearing_pro_USNG"
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToLineOfBearing_mt(self.inputSingleTable, "USNG", "USNG", None, "DEGREES", "Orientation", "METERS", "Distance", self.outputLineOfBearing, "GEODESIC", None)
        self.assertTrue(arcpy.Exists(self.outputLineOfBearing), "Output features do not exist or were not created")
        featureCount = int(arcpy.GetCount_management(self.outputLineOfBearing).getOutput(0))
        expectedFeatures = int(23)
        self.assertEqual(featureCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(featureCount)))
        compareFeatures = arcpy.FeatureCompare_management(self.BaseFC, self.outputLineOfBearing, "OID")
        # identical = 'true' means that there are no differences between the base and the output feature class
        identical = compareFeatures.getOutput(1)
        self.assertEqual(identical, "true", "Feature compare failed: \n %s" % arcpy.GetMessages())
        return
    def test_table_to_lineofbearing_pro_UTM_BANDS(self):
        '''Test Table To Line Of Bearing for ArcGIS Pro_UTM_BANDS'''
        runToolMessage = ".....TableToLineOfBearingTestCase.test_table_to_lineofbearing_pro_UTM_BANDS"
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToLineOfBearing_mt(self.inputSingleTable, "UTM_BANDS", "UTM", None, "DEGREES", "Orientation", "METERS", "Distance", self.outputLineOfBearing, "GEODESIC", None)
        self.assertTrue(arcpy.Exists(self.outputLineOfBearing), "Output features do not exist or were not created")
        featureCount = int(arcpy.GetCount_management(self.outputLineOfBearing).getOutput(0))
        expectedFeatures = int(23)
        self.assertEqual(featureCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(featureCount)))
        compareFeatures = arcpy.FeatureCompare_management(self.BaseFC, self.outputLineOfBearing, "OID")
        # identical = 'true' means that there are no differences between the base and the output feature class
        identical = compareFeatures.getOutput(1)
        self.assertEqual(identical, "true", "Feature compare failed: \n %s" % arcpy.GetMessages())
        return

