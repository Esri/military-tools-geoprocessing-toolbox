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
ConvertCoordinatesTestCase.py
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

class ConvertCoordinatesTestCase(unittest.TestCase):
    ''' Test all tools and methods related to the Convert Coordinates tool
    in the Military Tools toolbox'''
    
    inputTable = None
    outputConvert = None
    
    def setUp(self):
        if Configuration.DEBUG == True: print(".....ConvertCoordinatesTestCase.setUp")    
        
        UnitTestUtilities.checkArcPy()
        if not arcpy.Exists(Configuration.militaryScratchGDB):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.currentPath)

        self.inputTable = os.path.join(Configuration.militaryInputDataGDB, "SigActs")
        self.outputConvert = os.path.join(Configuration.militaryScratchGDB, "outputConvert")
        
    def tearDown(self):
        if Configuration.DEBUG == True: print(".....ConvertCoordinatesTestCase.tearDown")
        #UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)
    
    def test_convert_coordinates_desktop(self):
        '''Test Convert Coordinates in ArcGIS Desktop'''
        runToolMessage = ".....ConvertCoordinatesTestCase.test_convert_coordinates_desktop"
        arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        
        arcpy.ConvertCoordinates_mt(self.inputTable, "DD_2", "Location_X", "Location_Y", self.outputConvert)
        
        self.assertTrue(arcpy.Exists(self.outputConvert), "Output features do not exist or were not created")
        
        featureCount = int(arcpy.GetCount_management(self.outputConvert).getOutput(0))
        expectedFeatures = int(288)
        self.assertEqual(featureCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(featureCount)))
        #TODO: Were correct fields added to the output?
        return


    def test_convert_coordinates_pro(self):
        '''Test Convert Coordinates in ArcGIS Pro'''
        runToolMessage = ".....ConvertCoordinatesTestCase.test_convert_coordinates_pro"
        arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        arcpy.ConvertCoordinates_mt(self.inputTable, "DD_2", "Location_X", "Location_Y", self.outputConvert)
        self.assertTrue(arcpy.Exists(self.outputConvert), "Output features do not exist or were not created")
        featureCount = int(arcpy.GetCount_management(self.outputConvert).getOutput(0))
        expectedFeatures = int(288)
        self.assertEqual(featureCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(featureCount)))
        #TODO: Were correct fields added to the output?
        return
