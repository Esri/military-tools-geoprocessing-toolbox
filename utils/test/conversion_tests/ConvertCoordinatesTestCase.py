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

import os
import unittest

import arcpy

# Add parent folder to python path if running test case standalone
import sys
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))

import UnitTestUtilities
import Configuration

class ConvertCoordinatesTestCase(unittest.TestCase):

    ''' Test all tools and methods related to the Convert Coordinates tool
    in the Military Tools toolbox'''
    
    inputTable = None
    outputConvert = None
    
    def setUp(self):   
        ''' Initialization needed if running Test Case standalone '''
        Configuration.GetLogger()
        Configuration.GetPlatform()
        ''' End standalone initialization '''
            
        Configuration.Logger.debug(".....ConvertCoordinatesTestCase.setUp")    

        UnitTestUtilities.checkArcPy()
        if not arcpy.Exists(Configuration.militaryScratchGDB):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.currentPath)

        self.inputTable = os.path.join(Configuration.militaryInputDataGDB, "SigActs")

        UnitTestUtilities.checkGeoObjects([Configuration.toolboxUnderTest, \
            self.inputTable])

        self.outputConvert = os.path.join(Configuration.militaryScratchGDB, "outputConvert")

        arcpy.env.overwriteOutput = True
        
    def tearDown(self):
        Configuration.Logger.debug(".....ConvertCoordinatesTestCase.tearDown")
        #UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)
    
    def test_convert_coordinates(self):
        '''Test Convert Coordinates in ArcGIS Desktop'''
        Configuration.Logger.info(".....ConvertCoordinatesTestCase.test_convert_coordinates_desktop")

        arcpy.ImportToolbox(Configuration.toolboxUnderTest)
        
        arcpy.ConvertCoordinates_mt(self.inputTable, "DD_2", "Location_X", "Location_Y", self.outputConvert)
        
        self.assertTrue(arcpy.Exists(self.outputConvert), "Output features do not exist or were not created")
        
        featureCount = int(arcpy.GetCount_management(self.outputConvert).getOutput(0))
        expectedFeatures = int(288)
        self.assertGreaterEqual(featureCount, expectedFeatures, "Expected %s features, but got %s" % (str(expectedFeatures), str(featureCount)))

        # Were all of the expected added?
        expected_field_names = ["DDLat","DDLon","DMSLat","DMSLon","DDMLat","DDMLon","MGRS","USNG","UTM_BANDS","GEOREF","GARS"]
        field_list = arcpy.ListFields(self.outputConvert)
        out_field_names_list = []
        for out_field in field_list:
            out_field_name = str(out_field.name)
            out_field_names_list.append(out_field_name)

        for expected_name in expected_field_names:
            self.assertTrue(expected_name in out_field_names_list, ("Field %s is not present!" % expected_name))

        return

if __name__ == "__main__":
    unittest.main() 

