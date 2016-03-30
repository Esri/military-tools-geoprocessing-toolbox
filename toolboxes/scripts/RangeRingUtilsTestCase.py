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
==================================================
'''
import os
import arcpy
import unittest
import Configuration
import RangeRingUtils

class RangeRingUtilsTestCase(unittest.TestCase):
    ''' Test all methods and classes in RangeRingUtils.py '''

    srWAZED = arcpy.SpatialReference(54032)

    def setUp(self):
        ''' setup for tests'''
        if Configuration.DEBUG == True:
            print("     RangeRingsUtilsTestCase.setUp")
        self.OutputGDB = os.path.join(Configuration.currentPath, "data", "output.gdb")
        self.DataGDB = os.path.join(Configuration.currentPath, "data", "data.gdb")

        #create a temp point feature class
        ptCoords = [[0.0, 0.0], [10.0, 10.0], [3.0, 3.0], [5.5, 1.5]]
        self.pointGeographic = arcpy.CreateFeatureClass_management("in_memory", "tempfc", "POINT")[0]
        with arcpy.da.InsertCursor(fc, ["SHAPE@XY"]) as cursor:
            for (x, y) in ptCoords:
                cursor.insertRow([(x, y)])
        del cursor

        return

    def tearDown(self):
        ''' cleanup after tests'''
        del self.pointGeographic
        return

    # def test_rangeRingsFromList(self):
    #     ''' test case for RangeRingUtis.rangeRingsFromList method'''
    #     return

    # def test_rangeRingsFromMinMax(self):
    #     ''' test case for RangeRingUtis.rangeRingsFromMinMax method'''
    #     return

    # def test_rangeRingsFromInterval(self):
    #     ''' test case for RangeRingUtis.rangeRingsFromInterval method'''
    #     return

    def test_featureclassToPointGeometry(self):
        ''' test internal class method '''
        pg = RangeRingUtils._featureclassToPointGeometry(self.pointGeographic)
        self.assertEqual(pg.pointCount, int(4))
        return

    def test_RingMaker_init(self):
        ''' test class'''
        ringDistanceList = [10.0, 20.0, 30.0, 40.0]
        rm = RangeRingUtils.RingMaker(self.pointGeographic,
                                      ringDistanceList,
                                      "METERS",
                                      self.srWAZED)
        self.assertCountEqual(self, rm.ringCount, len(ringDistanceList))
        self.assertCountEqual(self, rm.ringMin, 10.0)
        self.assertCountEqual(self, rm.ringMax, 40.0)
        return

    def test_RingMaker_sortList_empty(self):
        ''' test RingMaker's internal _sortList method if it handles an empty list'''
        outList = RangeRingUtils.RingMaker._sortList([])
        self.assertIsNone(self, outList)
        return

    def test_RingMaker_sortedList_isSorted(self):
        ''' test Ringmaker's internal _sortedList method if it sorts a list'''
        l = [7, 5, 9, 3, 8, 1, 6, 2, 4, 0]
        outList = RangeRingUtils.RingMaker._sortList([])
        self.assertEqual(self, outList, sorted(l))
        return

    def test_RingMaker_addFieldsToTable(self):
        ''' test RingMaker's internal _addFieldsToTable method'''
        fc = arcpy.CreateFeatureClass_management("in_memory", "fcTestFields", "POINT")[0]
        numFieldsBefore = len(arcpy.ListFields(fc))
        numFieldsAfter = arcpy.ListFields(RangeRingUtils.RingMaker._addFieldsToTable(fc, {"a":"DOUBLE", "b":"TEXT"}))
        self.assertCountEqual(self, numFieldsBefore, numFieldsAfter + 2)
        return

    def test_RingMaker_makeTempTable(self):
        ''' test RingMaker's internal method'''
        tempTab = RangeRingUtils.RingMaker._makeTempTable("tempTab",{"a":"TEXT"})
        self.assertTrue(self, arcpy.Exists(tempTab))
        return

    def test_RingMaker_makeRingsFromDistances(self):
        ''' test RingMaker's internal method'''
        ringDistanceList = [10.0, 20.0, 30.0, 40.0]
        ringCountEstimate = len(ringDistanceList) * arcpy.getCount(self.pointGeographic)[0]
        rm = RangeRingUtils.RingMaker(self.pointGeographic, ringDistanceList, "METERS", self.srWAZED)
        rm.makeRingsFromDistances
        ringCountActual = int(arcpy.GetCount_management(rm.ringFeatures).getOutput(0))
        self.assertEqual(self, ringCountEstimate, ringCountActual)
        return

    # def test_RingMaker_makeRadials(self):
    #     ''' test RingMaker's internal method'''
    #     return

    def test_RingMaker_saveRingsAsFeatures(self):
        ''' test RingMaker's internal method'''
        ringDistanceList = [10.0, 20.0, 30.0, 40.0]
        ringCountEstimate = len(ringDistanceList) * arcpy.getCount(self.pointGeographic)[0]
        rm = RangeRingUtils.RingMaker(self.pointGeographic, ringDistanceList,
                                      "METERS", self.srWAZED)
        rm.makeRingsFromDistances()
        ringFeatures = rm.saveRingsAsFeatures(os.path.join("in_memory", "tempRings"))
        self.assertTrue(self, arcpy.Exists(ringFeatures))
        return

