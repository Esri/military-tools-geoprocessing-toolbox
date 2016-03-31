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
RangeRingUtils.py
--------------------------------------------------
requirements: ArcGIS X.X, Python 2.7 or Python 3.4
author: ArcGIS Solutions
company: Esri
==================================================
description: Utilities to create range ring features
==================================================
history:
3/29/2016 - mf - design & original coding
==================================================
'''
import os
import sys
import traceback
import arcpy

acceptableDistanceUnits = ['METERS', 'KILOMETERS',
                           'MILE', 'NAUTICAL_MILES',
                           'FEET', 'US_SURVEY_FEET']
srDefault = arcpy.SpatialReference(54032) # World_Azimuthal_Equidistant

# def makeRadials(center, number, distance, sr, outputRadialFeatures):
#     ''' make radials from number of radials, center point, and max distance '''
'''
use
BearingDistanceToLine_management (in_table, out_featureclass,
                                        x_field, y_field,
                                        distance_field, {distance_units},
                                        bearing_field, {bearing_units},
                                        {line_type}, {id_field}, {spatial_reference})

as

use BearingDistanceToLine_management (in_table, outRadialFeatures,
                                        x_field, y_field,
                                        distance_field, {distance_units},
                                        bearing_field, {bearing_units},
                                        'GEODESIC', {id_field}, {spatial_reference})
'''
#     return outputRadialFeatures

def rangeRingsFromList(centerFC, rangeList, distanceUnits, sr, outputRingFeatures):
    ''' Make range ring features from a center, and list of distances '''
    ringMaker = RingMaker(centerFC, rangeList, distanceUnits, sr)
    ringMaker.makeRingsFromDistances()
    ringMaker.saveRingsAsFeatures(outputRingFeatures)
    #ringMaker.makeRadials
    return outputRingFeatures

def rangeRingsFromMinMax(centerFC, rangeMin, rangeMax, distanceUnits, numRadials, outputRingFeatures, outputRadialFeatures, sr):
    ''' Make range ring features from only two distances, a minimum and a maximum '''
    try:
        # make our range list from min and max
        rangeMin = min(rangeMin, rangeMax)
        rangeMax = max(rangeMin, rangeMax)
        ringDistanceList = [rangeMin, rangeMax]

        rm = RingMaker(centerFC, ringDistanceList, distanceUnits, sr)

        # make the rings and save them
        rm.makeRingsFromDistances()
        outRings = rm.saveRingsAsFeatures(outputRingFeatures)

        # Do we need to create radials?
        rm.makeRadials(numRadials)
        outRadials = rm.saveRadialsAsFeatures(outputRadialFeatures)

        return [outRings, outRadials]
    except arcpy.ExecuteError:
        # Get the tool error messages
        msgs = arcpy.GetMessages()
        arcpy.AddError(msgs)
        print(msgs)

    except:
        # Get the traceback object
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]

        # Concatenate information together concerning the error into a message string
        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + \
                "\nError Info:\n" + str(sys.exc_info()[1])
        msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages() + "\n"

        # Return python error messages for use in script tool or Python Window
        arcpy.AddError(pymsg)
        arcpy.AddError(msgs)
        # Print Python error messages for use in Python / Python Window
        print(pymsg + "\n")
        print(msgs)

def rangeRingsFromInterval(centerFC, numRings, distBetween, distanceUnits, sr, outputRingFeatures):
    ''' Classic range rings from center, number of rings, and distance between rings  '''
    # center = _featureclassToPointGeometry(centerFC)
    # rangeList = []
    # for r in range(1, numRings):
    #     rangeList.append(r * distBetween)
    # ringMaker = RingMaker(center, rangeList, distanceUnits, sr)
    # ringMaker.saveRingsAsFeatures(outputRingFeatures)
    return outputRingFeatures


class RingMaker:
    '''
    Core class for making range rings.

    Inputs:
        center = arcpy.PointGeometry of ring centers
        rangeList = Python list of ring distances
        distanceUnits = unit of length for rangeList
        sr = Spatial Reference of rings

    Outputs:
    '''

    def __init__(self, center, inputRangeList, distanceUnits, sr):
        ''' initialize rings '''

        self.deleteme = []

        # project center to sr, and keep it as a list of PointGeometries object
        originalGeom = arcpy.CopyFeatures_management(center, arcpy.Geometry())
        newGeom = []
        for g in originalGeom:
            newGeom.append(g.projectAs(sr))
        self.center = newGeom

        self.rangeList = self._sortList(inputRangeList)
        if distanceUnits == None or distanceUnits == "#" or distanceUnits == "":
            self.distanceUnits = sr.linearUnitName
        else:
            self.distanceUnits = distanceUnits

        if not sr == None or not sr == "#" or not sr == "":
            self.sr = sr
        else:
            self.sr = srDefault

        self.ringFeatures = None
        self.radialFeatures = None
        self.ringCount = len(self.rangeList)
        self.ringMin = min(self.rangeList)
        self.ringMax = max(self.rangeList)


    def __del__(self):
        ''' clean up rings '''
        for i in self.deleteme:
            if arcpy.Exists(i):
                arcpy.Delete_management(i)

    def _sortList(self, listToSort):
        ''' sort list of distances '''
        if len(listToSort) == 0:
            print("Empty distance list")
            return None
        return sorted(listToSort)

    def _addFieldsToTable(self, tab, fields):
        ''' add fields from dictionary: {'<fieldname>':'type'} '''
        for f in list(fields.keys()):
            arcpy.AddField_management(tab, f, fields[f])
        return tab

    def _makeTempTable(self, name, fields):
        ''' make a temporary, in_memory table '''
        tab = os.path.join("in_memory", name)
        arcpy.CreateTable_management(os.path.dirname(tab),
                                     os.path.basename(tab))
        self.deleteme.append(tab)
        if fields:
            newtab = self._addFieldsToTable(tab, fields)
        else:
            print("no fields to add")
            newtab = tab
        return newtab

    def makeRingsFromDistances(self):
        ''' make geodesic rings from distance list '''
        # make a table for TableToEllipse
        fields = {'x':'DOUBLE', 'y':'DOUBLE', 'd':'DOUBLE'}
        inTable = self._makeTempTable("ringTable", fields)
        cursor = arcpy.da.InsertCursor(inTable, ['x', 'y', 'd'])
        #self.center is a list of PointGeometry
        for i in self.center:
            pt = i.firstPoint
            for r in self.rangeList:
                cursor.insertRow([pt.X, pt.Y, r * 2])
        del cursor
        self.deleteme.append(inTable)
        outFeatures = os.path.join("in_memory", "outRings")
        arcpy.TableToEllipse_management(inTable, outFeatures,
                                        'x', 'y', 'd', 'd',
                                        self.distanceUnits,
                                        '#', '#', '#', self.sr)
        self.deleteme.append(outFeatures)
        self.ringFeatures = outFeatures
        return outFeatures

    def makeRadials(self, numRadials):
        ''' make geodesic radials from number of radials '''
        segmentAngle = 360.0/numRadials
        segmentAngleList = []
        a = 0.0
        while a < 360.0:
            segmentAngleList.append(a)
            a += segmentAngle

        fields = {'x':'DOUBLE', 'y':'DOUBLE', 'rang':'DOUBLE', 'rlen':'DOUBLE'}
        tab = self._makeTempTable("radTable", fields)
        cursor = arcpy.da.InsertCursor(tab, ['x', 'y', 'rang', 'rlen'])
        for i in self.center:
            pt = i.firstPoint
            for r in segmentAngleList:
                cursor.insertRow([pt.X, pt.Y, r, self.ringMax])
        del cursor
        self.deleteme.append(tab)
        outRadialFeatures = os.path.join("in_memory", "outRadials")
        arcpy.BearingDistanceToLine_management(tab, outRadialFeatures, 'x', 'y',
                                               'rlen', self.distanceUnits, 'rang', "DEGREES",
                                               "GEODESIC", "#", self.sr)
        self.deleteme.append(outRadialFeatures)
        self.radialFeatures = outRadialFeatures
        return outRadialFeatures

    def saveRingsAsFeatures(self, outputFeatureClass):
        ''' save rings to featureclass '''
        arcpy.CopyFeatures_management(self.ringFeatures, outputFeatureClass)
        return outputFeatureClass

    def saveRadialsAsFeatures(self, outputFeatureClass):
        ''' save radials to featureclass '''
        arcpy.CopyFeatures_management(self.radialFeatures, outputFeatureClass)
        return outputFeatureClass
