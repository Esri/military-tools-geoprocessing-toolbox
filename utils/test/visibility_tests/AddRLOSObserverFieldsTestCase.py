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
AddRLOSObserverFieldsTestCase.py
--------------------------------------------------
requirements:
* ArcGIS Desktop 10.X+ or ArcGIS Pro 1.X+
* Python 2.7 or Python 3.4

author: ArcGIS Solutions
company: Esri

==================================================
history:
? - dh - original test writeup
6/17/2016
 11/29/2016 - mf - remove input check in unittest (unnecessary)
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

class AddRLOSObserverFieldsTestCase(unittest.TestCase):
    ''' Test all tools and methods related to the Add RLOS Observer Fields tool
    in the Military Tools toolbox'''

    inputObservers = None
    inputTargets = None

    def setUp(self):
        ''' Initialization needed if running Test Case standalone '''
        Configuration.GetLogger()
        Configuration.GetPlatform()
        ''' End standalone initialization '''
            
        Configuration.Logger.debug(".....AddRLOSObserverFieldsTestCase.setUp")

        UnitTestUtilities.checkArcPy()
        if not arcpy.Exists(Configuration.militaryScratchGDB):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.currentPath)

        arcpy.env.overwriteOutput = True

        originalObservers = os.path.join(Configuration.militaryInputDataGDB, "RLOS_Observers")
        self.inputObservers = os.path.join(Configuration.militaryScratchGDB, "RLOS_Observers")
        Configuration.Logger.debug("Copying %s to %s..." % (originalObservers, self.inputObservers))
        arcpy.CopyFeatures_management(originalObservers, self.inputObservers)
        
        arcpy.ImportToolbox(Configuration.toolboxUnderTest)  

        return

    def tearDown(self):
        Configuration.Logger.debug(".....AddRLOSObserverFieldsTestCase.tearDown")
        # UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)

        return

    def test_add_rlos_observer_fields(self):
        Configuration.Logger.info("...AddRLOSObserverFieldsTestCase.test_add_rlos_observer_fields")

        #self.assertTrue(arcpy.Exists(self.inputObservers), "Input dataset does not exist: %s" % self.inputObservers)
        
        arcpy.AddRadialLineOfSightObserverFields_mt(self.inputObservers, 2.0, 0.0, 0.0, 1000.0, 0.0, 360.0, 90.0, -90.0)
        
        fieldList = arcpy.ListFields(self.inputObservers, "RADIUS1")
        fieldCount = len(fieldList)
        self.assertEqual(fieldCount, 1, "Expected a field count of 1 for RADIUS1 but got %s" % str(fieldCount))
        fieldList = arcpy.ListFields(self.inputObservers, "RADIUS2")
        fieldCount = len(fieldList)
        self.assertEqual(fieldCount, 1, "Expected a field count of 1 for RADIUS2 but got %s" % str(fieldCount))
        fieldList = arcpy.ListFields(self.inputObservers, "OFFSETA")
        fieldCount = len(fieldList)
        self.assertEqual(fieldCount, 1, "Expected a field count of 1 for OFFSETA but got %s" % str(fieldCount))
        fieldList = arcpy.ListFields(self.inputObservers, "OFFSETB")
        fieldCount = len(fieldList)
        self.assertEqual(fieldCount, 1, "Expected a field count of 1 for OFFSETB but got %s" % str(fieldCount))
        fieldList = arcpy.ListFields(self.inputObservers, "AZIMUTH1")
        fieldCount = len(fieldList)
        self.assertEqual(fieldCount, 1, "Expected a field count of 1 for AZIMUTH1 but got %s" % str(fieldCount))
        fieldList = arcpy.ListFields(self.inputObservers, "AZIMUTH2")
        fieldCount = len(fieldList)
        self.assertEqual(fieldCount, 1, "Expected a field count of 1 for AZIMUTH2 but got %s" % str(fieldCount))
        fieldList = arcpy.ListFields(self.inputObservers, "VERT1")
        fieldCount = len(fieldList)
        self.assertEqual(fieldCount, 1, "Expected a field count of 1 for VERT1 but got %s" % str(fieldCount))
        fieldList = arcpy.ListFields(self.inputObservers, "VERT2")
        fieldCount = len(fieldList)
        self.assertEqual(fieldCount, 1, "Expected a field count of 1 for VERT2 but got %s" % str(fieldCount))
        rows = arcpy.SearchCursor(self.inputObservers)
        row = rows.next()
        while row:
            radius1 = row.RADIUS1
            self.assertEqual(radius1, float(0), "Bad RADIUS1 value: %s" % str(radius1))
            radius2 = row.RADIUS2
            self.assertEqual(radius2, float(1000), "Bad RADIUS2 value: %s" % str(radius2))
            offseta = row.OFFSETA
            self.assertEqual(offseta, float(2), "Bad OFFSETA value: %s" % str(offseta))
            offsetb = row.OFFSETB
            self.assertEqual(offsetb, float(0), "Bad OFFSETB value: %s" % str(offsetb))
            azimuth1 = row.AZIMUTH1
            self.assertEqual(azimuth1, float(0), "Bad AZIMUTH1 value: %s" % str(azimuth1))
            azimuth2 = row.AZIMUTH2
            self.assertEqual(azimuth2, float(360), "Bad AZIMUTH2 value: %s" % str(azimuth2))
            vert1 = row.VERT1
            self.assertEqual(vert1, float(90), "Bad VERT1 value: %s" % str(vert1))
            vert2 = row.VERT2
            self.assertEqual(vert2, float(-90), "Bad VERT2 value: %s" % str(vert2))
            row = rows.next()
        return

if __name__ == "__main__":
    unittest.main()