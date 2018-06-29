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
FindLocalPeaksTestCase.py
--------------------------------------------------
requirements:
* ArcGIS Desktop 10.X+ or ArcGIS Pro 1.X+
* Python 2.7 or Python 3.4

author: ArcGIS Solutions
company: Esri

==================================================
history:
5/11/2016 - JH - initial creation
5/31/2016 - MF - change error handling
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

class FindLocalPeaksTestCase(unittest.TestCase):
    ''' Test all tools and methods related to the Find Local Peaks tool
    in the Military Tools toolbox'''

    inputArea = None
    inputSurface = None
    outputPoints = None

    def setUp(self):
        ''' Initialization needed if running Test Case standalone '''
        Configuration.GetLogger()
        Configuration.GetPlatform()
        ''' End standalone initialization '''
            
        Configuration.Logger.debug(".....FindLocalPeaksTestCase.setUp")

        UnitTestUtilities.checkArcPy()
        if not arcpy.Exists(Configuration.militaryScratchGDB):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.currentPath)

        self.inputArea = os.path.join(Configuration.militaryInputDataGDB, "AreaofInterest")
        self.inputSurface = os.path.join(Configuration.militaryInputDataGDB, "ElevationUTM_Zone10")

        UnitTestUtilities.checkGeoObjects([Configuration.toolboxUnderTest, \
            self.inputArea, self.inputSurface])

        self.outputPoints = os.path.join(Configuration.militaryScratchGDB, "outputFindLocalPeaks")

        if arcpy.CheckExtension("Spatial") == "Available":
            arcpy.CheckOutExtension("Spatial")
            arcpy.AddMessage("Spatial checked out")

        arcpy.ImportToolbox(Configuration.toolboxUnderTest)  

    def tearDown(self):
        if Configuration.DEBUG == True: print(".....FindLocalPeaksTestCase.tearDown")
        arcpy.CheckInExtension("Spatial");
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)

    def test_find_local_peaks(self):
        ''' Test Find Local Peaks for ArcGIS Desktop '''
        Configuration.Logger.info(".....FindLocalPeaksTestCase.test_find_local_peaks")

        arcpy.env.overwriteOutput = True

        try:
            arcpy.FindLocalPeaks_mt(self.inputArea, 10, self.inputSurface, self.outputPoints)
        except:
            # WORKAROUND: To arpy exception with Pro: 
            # "DeprecationWarning: Product and extension licensing is no longer handled with this method."
            # when this tool is run in Pro from unit test driver
            if (Configuration.Platform == Configuration.PLATFORM_PRO):
                pass

        self.assertTrue(arcpy.Exists(self.outputPoints), "Output dataset does not exist or was not created")
        pointCount = int(arcpy.GetCount_management(self.outputPoints).getOutput(0))
        expectedFeatures = int(10)
        self.assertEqual(pointCount, expectedFeatures, "Expected %s features but got %s" % (str(expectedFeatures),str(pointCount)))
        return

    def test_find_local_peaks_no_input_area(self):
        ''' Test Find Local Peaks for ArcGIS Desktop '''
        Configuration.Logger.info(".....FindLocalPeaksTestCase.test_find_local_peaks_no_input_area")

        arcpy.env.overwriteOutput = True

        errorMsgs = None
        noInputArea = None # <-- Bad Input Area

        try : 
           arcpy.FindLocalPeaks_mt(noInputArea, 10, self.inputSurface, self.outputPoints)
        except arcpy.ExecuteError:
            # ExecuteError is expected because of bad input
            errorMsgs = arcpy.GetMessages(severity = 2)

        self.assertIsNotNone(errorMsgs, "Error Message Expected for No Input Area")
        # 2 Error Messages: "No Input Area" "Tool Failed" - errorMsgs is a string not list
        self.assertEqual(errorMsgs.count('\n'), 2, "Only 2 Error Messages Expected for No Input Area")

        return
        
if __name__ == "__main__":
    unittest.main()