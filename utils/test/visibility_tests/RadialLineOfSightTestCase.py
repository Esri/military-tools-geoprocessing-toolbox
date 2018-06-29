# coding: utf-8
'''
----------------------------------------------------------------------------
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
5/18/2016 - DJH - initial creation
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

class RadialLineOfSightTestCase(unittest.TestCase):
    ''' Test all tools and methods related to the Radial Line Of Sight tool
    in the Military Tools toolbox'''

    observers = None
    inputSurface = None
    outputRLOS = None

    def setUp(self):
        ''' Initialization needed if running Test Case standalone '''
        Configuration.GetLogger()
        Configuration.GetPlatform()
        ''' End standalone initialization '''
            
        Configuration.Logger.debug("     RadialLineOfSightTestCase.setUp")

        UnitTestUtilities.checkArcPy()
        if not arcpy.Exists(Configuration.militaryScratchGDB):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.currentPath)

        self.observers = os.path.join(Configuration.militaryInputDataGDB, "RLOS_Observers")
        self.inputSurface = os.path.join(Configuration.militaryInputDataGDB, "ElevationUTM_Zone10")

        UnitTestUtilities.checkGeoObjects([Configuration.toolboxUnderTest, \
            self.observers, self.inputSurface])

        self.outputRLOS = os.path.join(Configuration.militaryScratchGDB, "outputRadialLineOfSight")

        # Note: Should not be necessary since tool does this:
        #if arcpy.CheckExtension("Spatial") == "Available":
        #    arcpy.CheckOutExtension("Spatial")
        #    arcpy.AddMessage(".....Spatial checked out")

        arcpy.ImportToolbox(Configuration.toolboxUnderTest)

    def tearDown(self):
        Configuration.Logger.debug("     RadialLineOfSightTestCase.tearDown")
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)
        # Note: Should not be necessary since tool does this:
        # arcpy.CheckInExtension("Spatial");

    def test_radial_line_of_sight(self):
        ''' Test Radial Line Of Sight in ArcGIS Desktop'''
        Configuration.Logger.info(".....RadialLineOfSightTestCase.test_Radial_line_of_sight")

        # Delete the output feature class if already exists
        if arcpy.Exists(self.outputRLOS) :
            arcpy.Delete_management(self.outputRLOS)

        inputObserverHeight = 2.0
        inputRadiusOfObserver = 2000.0

        # WORKAROUND: Setting this workspace became necessary to workaround a problem  
        # at Pro 2.2 with VisibilityUtilities.radialLineOfSight at: 
        # Project_management(tempObservers -> using the expansion '%scratchgdb%'
        arcpy.env.scratchWorkspace = Configuration.militaryScratchGDB

        toolOutput = None
        try : 
            toolOutput = arcpy.RadialLineOfSight_mt(self.observers, 
                                                    inputObserverHeight, 
                                                    inputRadiusOfObserver, 
                                                    self.inputSurface, 
                                                    self.outputRLOS)
        except:
            # WORKAROUND: To arpy exception with Pro: 
            # "DeprecationWarning: Product and extension licensing is no longer handled with this method."
            # when this tool is run in Pro from unit test driver
            pass

        # WORKAROUND: see about - toolOutput not being set because of exception on return
        Configuration.GetPlatform()
        if (Configuration.Platform != Configuration.PLATFORM_PRO):
            # 1: Check the expected return value
            self.assertIsNotNone(toolOutput, "No output returned from tool")

            outputRLOSOut = toolOutput.getOutput(0)
            self.assertEqual(self.outputRLOS, outputRLOSOut, "Unexpected return value from tool") 

        # 2: Verify output was created
        self.assertTrue(arcpy.Exists(self.outputRLOS), "Output dataset does not exist or was not created")
        featureCount = int(arcpy.GetCount_management(self.outputRLOS).getOutput(0))
        minimumNumberOfExpectedFeatures = int(400)
        self.assertGreaterEqual(featureCount, minimumNumberOfExpectedFeatures, "Expected %s features, but got %s" % (str(minimumNumberOfExpectedFeatures), str(featureCount)))
        return

if __name__ == "__main__":
    unittest.main()
