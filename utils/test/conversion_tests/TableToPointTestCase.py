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

import unittest
import arcpy
import os
import UnitTestUtilities
import Configuration

class TableToPointTestCase(unittest.TestCase):
    ''' Test all tools and methods related to the Table To Point tool
    in the Military Tools toolbox'''

    inputTable = None
    outputPoints = None
    proBaseFC = None
    BaseFC = None
    platform = None

    def setUp(self):
        if Configuration.DEBUG == True: print("     TableToPointTestCase.setUp")

        UnitTestUtilities.checkArcPy()
        if(Configuration.militaryScratchGDB == None) or (not arcpy.Exists(Configuration.militaryScratchGDB)):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.militaryDataPath)
        csvFolder = os.path.join(Configuration.militaryDataPath, "CSV")
        self.inputTable = os.path.join(csvFolder, "TableToPoint.csv")
        self.inputSingleTable = os.path.join(csvFolder, "TableToPoint_single.csv")
        self.outputPoints = os.path.join(Configuration.militaryScratchGDB, "outputTableToPoint")
        self.BaseFC = os.path.join(Configuration.militaryResultsGDB, "ExpectedOutputTableToPoint")
        
        UnitTestUtilities.checkFilePaths([Configuration.militaryDataPath, Configuration.militaryInputDataGDB, Configuration.militaryScratchGDB, Configuration.militaryResultsGDB, Configuration.military_ProToolboxPath, Configuration.military_DesktopToolboxPath])

    def tearDown(self):
        if Configuration.DEBUG == True: print("     TableToPointTestCase.tearDown")
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)

    def test_table_to_point_desktop(self):
        '''Test Table To Point for ArcGIS Desktop'''
        runToolMessage = ".....TableToPointTestCase.test_table_to_point_desktop"
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToPoint_mt(self.inputTable, "DD_2", "x", "y", self.outputPoints)
        self.assertTrue(arcpy.Exists(self.outputPoints), "Output features do not exist or were not created")
        pointCount = int(arcpy.GetCount_management(self.outputPoints).getOutput(0))
        expectedFeatures = int(288)
        self.assertEqual(pointCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(pointCount)))
        compareFeatures = arcpy.FeatureCompare_management(self.BaseFC, self.outputPoints, "OID")         
        # identical = 'true' means that there are no differences between the baseFC and the output feature class
        identical = compareFeatures.getOutput(1)
        self.assertEqual(identical, "true", "Feature compare failed: \n %s" % arcpy.GetMessages())
        return
    def test_table_to_point_desktop_MGRS(self):
        '''Test Table To Point for ArcGIS Desktop_MGRS'''
        runToolMessage = ".....TableToPointTestCase.test_table_to_point_desktop_MGRS"
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToPoint_mt(self.inputSingleTable, "MGRS", "MGRS", None, self.outputPoints)
        self.assertTrue(arcpy.Exists(self.outputPoints), "Output features do not exist or were not created")
        pointCount = int(arcpy.GetCount_management(self.outputPoints).getOutput(0))
        expectedFeatures = int(288)
        self.assertEqual(pointCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(pointCount)))
        compareFeatures = arcpy.FeatureCompare_management(self.BaseFC, self.outputPoints, "OID")         
        # identical = 'true' means that there are no differences between the baseFC and the output feature class
        identical = compareFeatures.getOutput(1)
        self.assertEqual(identical, "true", "Feature compare failed: \n %s" % arcpy.GetMessages())
        return
    def test_table_to_point_desktop_GARS(self):
        '''Test Table To Point for ArcGIS Desktop_GARS'''
        runToolMessage = ".....TableToPointTestCase.test_table_to_point_desktop_GARS"
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToPoint_mt(self.inputSingleTable, "GARS", "GARS", None, self.outputPoints)
        self.assertTrue(arcpy.Exists(self.outputPoints), "Output features do not exist or were not created")
        pointCount = int(arcpy.GetCount_management(self.outputPoints).getOutput(0))
        expectedFeatures = int(288)
        self.assertEqual(pointCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(pointCount)))
        compareFeatures = arcpy.FeatureCompare_management(self.BaseFC, self.outputPoints, "OID")         
        # identical = 'true' means that there are no differences between the baseFC and the output feature class
        identical = compareFeatures.getOutput(1)
        self.assertEqual(identical, "true", "Feature compare failed: \n %s" % arcpy.GetMessages())
        return
    def test_table_to_point_desktop_GEOREF(self):
        '''Test Table To Point for ArcGIS Desktop_GEOREF'''
        runToolMessage = ".....TableToPointTestCase.test_table_to_point_desktop_GEOREF"
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToPoint_mt(self.inputSingleTable, "GEOREF", "GEOREF", None, self.outputPoints)
        self.assertTrue(arcpy.Exists(self.outputPoints), "Output features do not exist or were not created")
        pointCount = int(arcpy.GetCount_management(self.outputPoints).getOutput(0))
        expectedFeatures = int(288)
        self.assertEqual(pointCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(pointCount)))
        compareFeatures = arcpy.FeatureCompare_management(self.BaseFC, self.outputPoints, "OID")         
        # identical = 'true' means that there are no differences between the baseFC and the output feature class
        identical = compareFeatures.getOutput(1)
        self.assertEqual(identical, "true", "Feature compare failed: \n %s" % arcpy.GetMessages())
        return
    def test_table_to_point_desktop_USNG(self):
        '''Test Table To Point for ArcGIS Desktop_USNG'''
        runToolMessage = ".....TableToPointTestCase.test_table_to_point_desktop_USNG"
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToPoint_mt(self.inputSingleTable, "USNG", "USNG", None, self.outputPoints)
        self.assertTrue(arcpy.Exists(self.outputPoints), "Output features do not exist or were not created")
        pointCount = int(arcpy.GetCount_management(self.outputPoints).getOutput(0))
        expectedFeatures = int(288)
        self.assertEqual(pointCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(pointCount)))
        compareFeatures = arcpy.FeatureCompare_management(self.BaseFC, self.outputPoints, "OID")         
        # identical = 'true' means that there are no differences between the baseFC and the output feature class
        identical = compareFeatures.getOutput(1)
        self.assertEqual(identical, "true", "Feature compare failed: \n %s" % arcpy.GetMessages())
        return
    def test_table_to_point_desktop_UTM_BANDS(self):
        '''Test Table To Point for ArcGIS Desktop_UTM_BANDS'''
        runToolMessage = ".....TableToPointTestCase.test_table_to_point_desktop_UTM_BANDS"
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToPoint_mt(self.inputSingleTable, "UTM_BANDS", "UTM", None, self.outputPoints)
        self.assertTrue(arcpy.Exists(self.outputPoints), "Output features do not exist or were not created")
        pointCount = int(arcpy.GetCount_management(self.outputPoints).getOutput(0))
        expectedFeatures = int(288)
        self.assertEqual(pointCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(pointCount)))
        compareFeatures = arcpy.FeatureCompare_management(self.BaseFC, self.outputPoints, "OID")         
        # identical = 'true' means that there are no differences between the baseFC and the output feature class
        identical = compareFeatures.getOutput(1)
        self.assertEqual(identical, "true", "Feature compare failed: \n %s" % arcpy.GetMessages())
        return

    def test_table_to_point_pro(self):
        '''Test Table To Point for ArcGIS Pro'''
        runToolMessage = ".....TableToPointTestCase.test_table_to_point_pro"
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToPoint_mt(self.inputTable, "DD_2", "x", "y", self.outputPoints)
        self.assertTrue(arcpy.Exists(self.outputPoints), "Output features do not exist or were not created")
        pointCount = int(arcpy.GetCount_management(self.outputPoints).getOutput(0))
        expectedFeatures = int(288)
        self.assertEqual(pointCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(pointCount)))
        compareFeatures = arcpy.FeatureCompare_management(self.BaseFC, self.outputPoints, "OID")            
        # identical = 'true' means that there are no differences between the baseFC and the output feature class
        identical = compareFeatures.getOutput(1)
        self.assertEqual(identical, "true", "Feature compare failed: \n %s" % arcpy.GetMessages())
        return
    def test_table_to_point_pro_MGRS(self):
        '''Test Table To Point for ArcGIS Pro_MGRS'''
        runToolMessage = ".....TableToPointTestCase.test_table_to_point_pro_MGRS"
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToPoint_mt(self.inputSingleTable, "MGRS", "MGRS", None, self.outputPoints)
        self.assertTrue(arcpy.Exists(self.outputPoints), "Output features do not exist or were not created")
        pointCount = int(arcpy.GetCount_management(self.outputPoints).getOutput(0))
        expectedFeatures = int(288)
        self.assertEqual(pointCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(pointCount)))
        compareFeatures = arcpy.FeatureCompare_management(self.BaseFC, self.outputPoints, "OID")            
        # identical = 'true' means that there are no differences between the baseFC and the output feature class
        identical = compareFeatures.getOutput(1)
        self.assertEqual(identical, "true", "Feature compare failed: \n %s" % arcpy.GetMessages())
        return
    def test_table_to_point_pro_GARS(self):
        '''Test Table To Point for ArcGIS Pro_GARS'''
        runToolMessage = ".....TableToPointTestCase.test_table_to_point_pro_GARS"
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToPoint_mt(self.inputSingleTable, "GARS", "GARS", None, self.outputPoints)
        self.assertTrue(arcpy.Exists(self.outputPoints), "Output features do not exist or were not created")
        pointCount = int(arcpy.GetCount_management(self.outputPoints).getOutput(0))
        expectedFeatures = int(288)
        self.assertEqual(pointCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(pointCount)))
        compareFeatures = arcpy.FeatureCompare_management(self.BaseFC, self.outputPoints, "OID")            
        # identical = 'true' means that there are no differences between the baseFC and the output feature class
        identical = compareFeatures.getOutput(1)
        self.assertEqual(identical, "true", "Feature compare failed: \n %s" % arcpy.GetMessages())
        return
    def test_table_to_point_pro_GEOREF(self):
        '''Test Table To Point for ArcGIS Pro_GEOREF'''
        runToolMessage = ".....TableToPointTestCase.test_table_to_point_pro_GEOREF"
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToPoint_mt(self.inputSingleTable, "GEOREF", "GEOREF", None, self.outputPoints)
        self.assertTrue(arcpy.Exists(self.outputPoints), "Output features do not exist or were not created")
        pointCount = int(arcpy.GetCount_management(self.outputPoints).getOutput(0))
        expectedFeatures = int(288)
        self.assertEqual(pointCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(pointCount)))
        compareFeatures = arcpy.FeatureCompare_management(self.BaseFC, self.outputPoints, "OID")            
        # identical = 'true' means that there are no differences between the baseFC and the output feature class
        identical = compareFeatures.getOutput(1)
        self.assertEqual(identical, "true", "Feature compare failed: \n %s" % arcpy.GetMessages())
        return
    def test_table_to_point_pro_USNG(self):
        '''Test Table To Point for ArcGIS Pro_USNG'''
        runToolMessage = ".....TableToPointTestCase.test_table_to_point_pro_USNG"
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToPoint_mt(self.inputSingleTable, "USNG", "USNG", None, self.outputPoints)
        self.assertTrue(arcpy.Exists(self.outputPoints), "Output features do not exist or were not created")
        pointCount = int(arcpy.GetCount_management(self.outputPoints).getOutput(0))
        expectedFeatures = int(288)
        self.assertEqual(pointCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(pointCount)))
        compareFeatures = arcpy.FeatureCompare_management(self.BaseFC, self.outputPoints, "OID")            
        # identical = 'true' means that there are no differences between the baseFC and the output feature class
        identical = compareFeatures.getOutput(1)
        self.assertEqual(identical, "true", "Feature compare failed: \n %s" % arcpy.GetMessages())
        return
    def test_table_to_point_pro_UTM_BANDS(self):
        '''Test Table To Point for ArcGIS Pro_UTM_BANDS'''
        runToolMessage = ".....TableToPointTestCase.test_table_to_point_pro_UTM_BANDS"
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.TableToPoint_mt(self.inputSingleTable, "UTM_BANDS", "UTM", None, self.outputPoints)
        self.assertTrue(arcpy.Exists(self.outputPoints), "Output features do not exist or were not created")
        pointCount = int(arcpy.GetCount_management(self.outputPoints).getOutput(0))
        expectedFeatures = int(288)
        self.assertEqual(pointCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(pointCount)))
        compareFeatures = arcpy.FeatureCompare_management(self.BaseFC, self.outputPoints, "OID")            
        # identical = 'true' means that there are no differences between the baseFC and the output feature class
        identical = compareFeatures.getOutput(1)
        self.assertEqual(identical, "true", "Feature compare failed: \n %s" % arcpy.GetMessages())
        return
