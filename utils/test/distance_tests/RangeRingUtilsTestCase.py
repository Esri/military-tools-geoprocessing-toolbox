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
RangeRingUtilsTestCase.py
--------------------------------------------------
requirements: ArcGIS X.X, Python 2.7 or Python 3.4
author: ArcGIS Solutions
company: Esri
==================================================
description: unittest test case for Range Rings
==================================================
history:
3/30/2016 - mf - initial coding
5/23/2016 - mf - update for framework
==================================================
'''
import os
import arcpy
import unittest
import UnitTestUtilities
import Configuration
#TODO: this is the problem line here:
from . import RangeRingUtils

srWebMerc = arcpy.SpatialReference(3857) #WGS_1984_Web_Mercator
srWGS84 = arcpy.SpatialReference(4326) #GCS_WGS_1984
srWAZED = arcpy.SpatialReference(54032) #World_Azimuthal_Equidistant
deleteIntermediateData = []

class RangeRingUtilsTestCase(unittest.TestCase):
    ''' Test all methods and classes in RangeRingUtils.py '''

    def setUp(self):
        ''' setup for tests'''
        if Configuration.DEBUG == True: print(".....RangeRingsUtilsTestCase.setUp")
        UnitTestUtilities.checkArcPy()
        if not arcpy.Exists(Configuration.militaryScratchGDB):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.currentPath)

        #create a temp point feature class
        ptCoords = [[0.0, 0.0], [10.0, 10.0], [3.0, 3.0], [5.5, 1.5]]
        tempfcPath = os.path.join("in_memory", "tempfc")
        if arcpy.Exists(tempfcPath):
            arcpy.Delete_management(tempfcPath)
        self.pointGeographic = arcpy.CreateFeatureclass_management(os.path.dirname(tempfcPath), os.path.basename(tempfcPath), "POINT", "#", "DISABLED", "DISABLED", srWGS84)[0]
        with arcpy.da.InsertCursor(self.pointGeographic, ["SHAPE@XY"]) as cursor:
            for (x, y) in ptCoords:
                cursor.insertRow([(x, y)])
        del cursor
        deleteIntermediateData.append(self.pointGeographic)
        return

    def tearDown(self):
        ''' cleanup after tests'''
        if Configuration.DEBUG == True: print(".....RangeRingsUtilsTestCase.tearDown")
        del self.pointGeographic
        for i in deleteIntermediateData:
            if arcpy.Exists(i):
                arcpy.Delete_management(i)
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)
        return

    def test_RingMaker_init(self):
        ''' test class'''
        runToolMessage = ".....RangeRingsUtilsTestCase.test_RingMaker_init"
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        
        ringDistanceList = [10.0, 20.0, 30.0, 40.0]
        rm = RangeRingUtils.RingMaker(self.pointGeographic,
                                      ringDistanceList,
                                      "METERS",
                                      srWAZED)
        self.assertEquals(rm.ringCount, len(ringDistanceList), "Incorrect ring count. Expected %s, but got %s" % (str(rm.ringCount), str(len(ringDistanceList))))
        expectedRingMin = float(10.0)
        self.assertEquals(rm.ringMin, expectedRingMin, "Incorrect min ring distance. Expected %s, but got %s" % (str(expectedRingMin), str(rm.ringMin)))
        expectedRingMax = float(40.0)
        self.assertEquals(rm.ringMax, expectedRingMax, "Incorrect max ring distance. Expected %s, but got %s" % (str(expectedRingMax), str(rm.ringMax)))
        return

    def test_RingMaker_sortList_empty(self):
        ''' test RingMaker's internal _sortList method if it handles an empty list'''
        runToolMessage = ".....RangeRingsUtilsTestCase.test_RingMaker_sortList_emtpy"
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        rr = RangeRingUtils.RingMaker(self.pointGeographic, [10.0, 20.0], "METERS", srWAZED)
        outList = rr._sortList([])
        self.assertIsNone(outList, "Expected empty sorted list, but got %s" % str(outList))
        return

    def test_RingMaker_sortList_isSorted(self):
        ''' test Ringmaker's internal _sortedList method if it sorts a list'''
        runToolMessage = "......RangeRingsUtilsTestCase.test_sortList_isSorted"
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        listToSort = [7, 5, 9, 3, 8, 1, 6, 2, 4, 0]
        rr = RangeRingUtils.RingMaker(self.pointGeographic, [10.0, 20.0], "METERS", srWAZED)
        outList = rr._sortList(listToSort)
        self.assertEqual(outList, sorted(listToSort), "List not sorted as expected")
        return

    def test_RingMaker_addFieldsToTable(self):
        ''' test RingMaker's internal _addFieldsToTable method'''
        runToolMessage = ".....RangeRingsUtilsTestCase.test_RingMaker_addFieldsToTable"
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        
        fc = arcpy.CreateFeatureclass_management("in_memory", "fcTestFields", "POINT")[0]
        numFieldsBefore = len(arcpy.ListFields(fc))

        fields = {"a":"DOUBLE", "b":"TEXT"}
        rm = RangeRingUtils.RingMaker(self.pointGeographic, [10.0, 20.0], "METERS", srWAZED)
        newfc = rm._addFieldsToTable(fc, fields)
        numFieldsAfter = len(list(arcpy.ListFields(newfc)))

        self.assertEqual(numFieldsAfter, numFieldsBefore + 2, "Error adding fields. Expected %s but got %s" % (str(numFieldsBefore + 2), str(numFieldsAfter)))
        deleteIntermediateData.append(fc)
        return

    def test_RingMaker_makeTempTable(self):
        ''' test RingMaker's internal method'''
        runToolMessage = ".....RangeRingsUtilsTestCase.test_RingMaker_makeTempTable"
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        
        rm = RangeRingUtils.RingMaker(self.pointGeographic, [10.0, 20.0], "METERS", srWAZED)
        tempTab = rm._makeTempTable("tempTab", {"a":"TEXT"})
        self.assertTrue(arcpy.Exists(tempTab), "Temp table was not created or does not exist")
        deleteIntermediateData.append(tempTab)
        return

    def test_RingMaker_makeRingsFromDistances(self):
        ''' test RingMaker's internal method'''
        runToolMessage = ".....RangeRingsUtilsTestCase.test_RingMaker_makeRingsFromDistances"
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        
        ringDistanceList = [10.0, 20.0, 30.0, 40.0]
        ringCountEstimate = len(ringDistanceList) * int(arcpy.GetCount_management(self.pointGeographic).getOutput(0))
        rm = RangeRingUtils.RingMaker(self.pointGeographic, ringDistanceList, "METERS", srWAZED)
        rm.makeRingsFromDistances()
        ringCountActual = int(arcpy.GetCount_management(rm.ringFeatures).getOutput(0))
        self.assertEqual(ringCountEstimate, ringCountActual, "Did not create rings correctly. Expected %s, but got %s" % (str(ringCountEstimate), str(ringCountActual)))
        return

    def test_RingMaker_makeRadials(self):
        ''' test RingMaker's internal method'''
        runToolMessage = ".....RangeRingsUtilsTestCase.test_RingMaker_makeRadials"
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        
        ringDistanceList = [10.0, 20.0, 30.0, 40.0]
        rm = RangeRingUtils.RingMaker(self.pointGeographic, ringDistanceList,
                                      "METERS", srWAZED)
        radialsToMake = 8
        radialCountEstimate = radialsToMake * int(arcpy.GetCount_management(self.pointGeographic).getOutput(0))
        rm.makeRadials(radialsToMake)
        radialCountActual = int(arcpy.GetCount_management(rm.radialFeatures).getOutput(0))
        self.assertEqual(radialCountEstimate, radialCountActual, "Did not create radials correctly. Expected %s but got %s" % (str(radialCountEstimate), str(radialCountActual)))
        return

    def test_RingMaker_saveRingsAsFeatures(self):
        ''' test RingMaker's internal method'''
        runToolMessage = ".....RangeRingsUtilsTestCase.test_RingMaker_saveRingsAsFeatures"
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        
        ringDistanceList = [10.0, 20.0, 30.0, 40.0]
        rm = RangeRingUtils.RingMaker(self.pointGeographic, ringDistanceList,
                                      "METERS", srWAZED)
        rm.makeRingsFromDistances()
        tempRings = os.path.join(Configuration.militaryScratchGDB, "tempRings")
        if arcpy.Exists(tempRings): arcpy.Delete_management(tempRings)
        ringFeatures = rm.saveRingsAsFeatures(tempRings)
        self.assertTrue(arcpy.Exists(ringFeatures), "Ring features were not created or do not exist")
        deleteIntermediateData.append(ringFeatures)
        return

    def test_RingMaker_saveRadialsAsFeatures(self):
        ''' test saving raidal features to feature class'''
        runToolMessage = ".....RangeRingsUtilsTestCase.test_RingMaker_saveRadialsAsFeatures"
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        
        ringDistanceList = [10.0, 20.0, 30.0, 40.0]
        rm = RangeRingUtils.RingMaker(self.pointGeographic, ringDistanceList,
                                      "METERS", srWAZED)
        rm.makeRadials(4)
        tempRadials = os.path.join(Configuration.militaryScratchGDB, "tempRadials")
        if arcpy.Exists(tempRadials): arcpy.Delete_management(tempRadials)
        radialFeatures = rm.saveRadialsAsFeatures(tempRadials)
        self.assertTrue(arcpy.Exists(radialFeatures), "Radial features were not created or do not exist")
        deleteIntermediateData.append(radialFeatures)
        return

    #=== TEST TOOL METHODS ==========================================

    def test_rangeRingsFromMinMax(self):
        ''' testing the tool method '''
        runToolMessage = ".....RangeRingsUtilsTestCase.test_rangeRingsFromMinMax"
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        
        numCenters = int(arcpy.GetCount_management(self.pointGeographic).getOutput(0))
        numRadials = 8
        rings = os.path.join(Configuration.militaryScratchGDB, "newRings")
        radials = os.path.join(Configuration.militaryScratchGDB, "newRadials") 
        rr = RangeRingUtils.rangeRingsFromMinMax(self.pointGeographic,
                                                 100.0,
                                                 1000.0,
                                                 "METERS",
                                                 numRadials,
                                                 rings,
                                                 radials,
                                                 srWAZED)
        outRings = rr[0]
        outRadials = rr[1]

        self.assertTrue(arcpy.Exists(outRings), "Ring features not created or do not exist")
        self.assertEqual(int(arcpy.GetCount_management(outRings).getOutput(0)), numCenters * 2, "Wrong number of expected ring features")

        self.assertTrue(arcpy.Exists(outRadials), "Radial features not created or do not exist")
        self.assertEqual(int(arcpy.GetCount_management(outRadials).getOutput(0)), numRadials * numCenters, "Wrong number of expected radial features")

        deleteIntermediateData.append(rings)
        deleteIntermediateData.append(radials)
        return

    def test_rangeRingsFromList(self):
        ''' testing rangeRingsFromList method'''
        runToolMessage = ".....RangeRingsUtilsTestCase.test_rangeRingsFromList"
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        
        numCenters = int(arcpy.GetCount_management(self.pointGeographic).getOutput(0))
        numRadials = 8
        rings = os.path.join(Configuration.militaryScratchGDB, "newRings")
        radials = os.path.join(Configuration.militaryScratchGDB, "newRadials")
        ringList = [1.0, 3.0, 9.0, 27.0, 81.0, 243.0, 729.0]
        rr = RangeRingUtils.rangeRingsFromList(self.pointGeographic,
                                               ringList,
                                               "METERS",
                                               numRadials,
                                               rings,
                                               radials,
                                               srWAZED)
        outRings = rr[0]
        outRadials = rr[1]

        self.assertTrue(arcpy.Exists(outRings), "Ring features not created or do not exist")
        self.assertEqual(int(arcpy.GetCount_management(outRings).getOutput(0)), len(ringList) * numCenters, "Wrong number of expected ring features")

        self.assertTrue(arcpy.Exists(outRadials), "Radial features not created or do not exist")
        self.assertEqual(int(arcpy.GetCount_management(outRadials).getOutput(0)), numRadials * numCenters, "Wrong number of expected radial features")

        deleteIntermediateData.append(rings)
        deleteIntermediateData.append(radials)
        return

    def test_rangeRingsFromInterval(self):
        ''' testing rangeRingsFromInterval method'''
        runToolMessage = ".....RangeRingsUtilsTestCase.test_rangeRingsFromInterval"
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        
        numCenters = int(arcpy.GetCount_management(self.pointGeographic).getOutput(0))
        numRadials = 8
        rings = os.path.join(Configuration.militaryScratchGDB, "newRings")
        radials = os.path.join(Configuration.militaryScratchGDB, "newRadials")
        numRings = 4
        distanceBetween = 200.0
        rr = RangeRingUtils.rangeRingsFromInterval(self.pointGeographic,
                                                   numRings,
                                                   distanceBetween,
                                                   "METERS",
                                                   numRadials,
                                                   rings,
                                                   radials,
                                                   srWAZED)
        outRings = rr[0]
        outRadials = rr[1]

        self.assertTrue(arcpy.Exists(outRings), "Ring features not created or do not exist")
        self.assertEqual(int(arcpy.GetCount_management(outRings).getOutput(0)), 4 * numCenters, "Wrong number of expected ring features")

        self.assertTrue(arcpy.Exists(outRadials), "Radial features not created or do not exist")
        self.assertEqual(int(arcpy.GetCount_management(outRadials).getOutput(0)), numRadials * numCenters, "Wrong number of expected radial features")

        deleteIntermediateData.append(rings)
        deleteIntermediateData.append(radials)
        return
