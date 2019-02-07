# coding: utf-8
'''
------------------------------------------------------------------------------
 Copyright 2016-2017 Esri
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
   http://www.apache.org/licenses/LICENSE-2.0
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
------------------------------------------------------------------------------
 ==================================================
 RadialLineOfSightAndRangeTestCase.py
 --------------------------------------------------
 requirements: ArcGIS 10.3+, Python 2.7
 author: ArcGIS Solutions
 contact: support@esri.com
 company: Esri
 ==================================================
 description:
 Unit tests for Visibility tools RadialLineOfSightAndRange
 ==================================================
'''

# IMPORTS ==========================================
import os
import unittest

import arcpy

# Add parent folder to python path if running test case standalone
import sys
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))

import UnitTestUtilities
import Configuration

# Add scripts to path so can call methods directly
Configuration.addScriptsPath()
import RadialLineOfSightAndRange
import VisibilityUtilities

class RadialLineOfSightAndRangeTestCase(unittest.TestCase):

    def setUp(self):
        ''' Initialization needed if running Test Case standalone '''
        Configuration.GetLogger()
        Configuration.GetPlatform()
        ''' End standalone initialization '''
            
        Configuration.Logger.debug('.....RadialLineOfSightAndRangeTestCase.setUp')
        arcpy.env.overwriteOutput = True 

    def tearDown(self):
        Configuration.Logger.debug(".....RadialLineOfSightAndRangeTestCase.tearDown")
        
    def test_toolboxMain(self):

        arcpy.ImportToolbox(Configuration.toolboxUnderTest)  

        if arcpy.CheckExtension("3D") == "Available":
            arcpy.CheckOutExtension("3D")
        else:
            raise Exception("3D license is not available.")

        inputObserverPoints = os.path.join(Configuration.militaryInputDataGDB, "RLOS_Observers")
        elevationRaster = os.path.join(Configuration.militaryInputDataGDB, "ElevationUTM_Zone10")
        outerRadiusInput    = '1000'
        leftAzimuthInput    = '90'
        rightAzimuthInput   = '180'
        observerOffsetInput = '20'
        innerRadiusInput    = '500'
        viewshed    = r'in_memory\viewshed'
        sectorWedge = r'in_memory\wedge'
        fullWedge   = r'in_memory\fullwedge'

        toolOutput = None

        try : 
            toolOutput = arcpy.RadialLineOfSightAndRange_mt(inputObserverPoints, elevationRaster, \
                outerRadiusInput, leftAzimuthInput, rightAzimuthInput, observerOffsetInput, \
                innerRadiusInput, viewshed, sectorWedge, fullWedge)
        except :
            UnitTestUtilities.handleArcPyError()

        # 1: Check the expected return value
        self.assertIsNotNone(toolOutput, "No output returned from tool")
        viewshedOut = toolOutput.getOutput(0)
        sectorWedgeOut = toolOutput.getOutput(1)
        fullWedgeOut = toolOutput.getOutput(2)

        self.assertEqual(viewshed, viewshedOut, "Unexpected return value from tool") 
        self.assertEqual(sectorWedge, sectorWedgeOut, "Unexpected return value from tool") 
        self.assertEqual(fullWedge, fullWedgeOut, "Unexpected return value from tool") 

        # 2: Verify some output was created
        viewshedFeaturesCount    = int(arcpy.GetCount_management(viewshedOut).getOutput(0))
        sectorWedgeFeaturesCount = int(arcpy.GetCount_management(sectorWedgeOut).getOutput(0))
        fullWedgeFeaturesCount   = int(arcpy.GetCount_management(fullWedgeOut).getOutput(0))

        self.assertGreater(viewshedFeaturesCount, 0, "No output features created for " + str(viewshedFeaturesCount))
        self.assertGreater(sectorWedgeFeaturesCount, 0, "No output features created for " + str(sectorWedgeFeaturesCount))
        self.assertGreater(fullWedgeFeaturesCount, 0, "No output features created for " + str(fullWedgeFeaturesCount))

    def test_createViewshed(self):

        Configuration.Logger.info(".....RadialLineOfSightAndRange.test_createViewshed")

        if arcpy.CheckExtension("3D") == "Available":
            arcpy.CheckOutExtension("3D")
        else:
            raise Exception("3D license is not available.")

        observers = os.path.join(Configuration.militaryInputDataGDB, "RLOS_Observers")
        elevationSurface = os.path.join(Configuration.militaryInputDataGDB, "ElevationUTM_Zone10")

        viewshedFC   = r'in_memory\viewshed'
        donutWedgeFC = r'in_memory\wedge'
        pieWedgeFC   = r'in_memory\fullwedge'

        RadialLineOfSightAndRange.createViewshed(observers, \
           elevationSurface, \
           '1000', '90', '180', '20', '500', \
           viewshedFC, donutWedgeFC, pieWedgeFC)

        viewshedFeaturesCount = int(arcpy.GetCount_management(viewshedFC).getOutput(0))
        donutFeaturesCount    = int(arcpy.GetCount_management(donutWedgeFC).getOutput(0))
        pieFeaturesCount      = int(arcpy.GetCount_management(pieWedgeFC).getOutput(0))

        self.assertGreater(viewshedFeaturesCount, 0, "No output features created for " + str(viewshedFC))
        self.assertGreater(donutFeaturesCount, 0, "No output features created for " + str(donutWedgeFC))
        self.assertGreater(pieFeaturesCount, 0, "No output features created for " + str(pieWedgeFC))

    def test_surfaceContainsPoint(self):
        '''
        Check if elevation dataset contains the specified point
        '''
        Configuration.Logger.info(".....RadialLineOfSightAndRange.test_surfaceContainsPoint")

        observers = os.path.join(Configuration.militaryInputDataGDB, "RLOS_Observers")

        elevationSurface = os.path.join(Configuration.militaryInputDataGDB, "ElevationUTM_Zone10")

        pointsIn = VisibilityUtilities.surfaceContainsPoints(observers, elevationSurface)

        self.assertTrue(pointsIn, 'Points not within Surface as Expected')

    def test_surfaceContainsPointWgs84(self): 
        '''
        Check if elevation dataset contains the specified point not in same SR as surface
        '''
        Configuration.Logger.info(".....RadialLineOfSightAndRange.test_surfaceContainsPointWgs84")

        # List of coordinates
        coordinates = [[-121.5, 36.5], [-121.2, 36.1]]

        # Create an in_memory feature class to contain the coordinate pairs
        observerFeatureClass = arcpy.CreateFeatureclass_management(
            "in_memory", "tempfc", "POINT", spatial_reference=arcpy.SpatialReference(4326))[0]

        # Open an insert cursor
        with arcpy.da.InsertCursor(observerFeatureClass, ["SHAPE@"]) as cursor:
            # Iterate through list of coordinates and add to cursor
            for (x, y) in coordinates:
                point = arcpy.Point(x, y)
                pointGeo = arcpy.PointGeometry(point, \
                    arcpy.SpatialReference(4326))
                cursor.insertRow([pointGeo])

        elevationSurface = os.path.join(Configuration.militaryInputDataGDB, "ElevationUTM_Zone10")

        arePointsIn = VisibilityUtilities.surfaceContainsPoints(observerFeatureClass, elevationSurface)

        self.assertTrue(arePointsIn, 'Points not within Surface as Expected')
        
if __name__ == "__main__":
    unittest.main()