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

def rangeRingsFromMinMax(centerFC, rangeMin, rangeMax, distanceUnits, sr, outputRingFeatures):
    ''' Make range ring features from only two distances, a minimum and a maximum '''
    # center = _featureclassToPointGeometry(centerFC)
    # rangeList = [rangeMin, rangeMax]
    # ringMaker = RingMaker(center, rangeList, distanceUnits, sr)
    # ringMaker.saveRingsAsFeatures(outputRingFeatures)
    return outputRingFeatures

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
    #TODO: How to resolve SR of 'center' parameter to the 'sr' parameter?

    def __init__(self, center, inputRangeList, distanceUnits, sr):
        ''' initialize rings '''
        # project center to sr, and keep it as a Geometry object
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
        self.ringCount = len(self.rangeList)
        self.ringMin = min(self.rangeList)
        self.ringMax = max(self.rangeList)

    def _sortList(self, listToSort):
        ''' sort list of distances '''
        if len(listToSort) == 0:
            print("Empty distance list")
            return None
        return sorted(listToSort)

    def _addFieldsToTable(self, tab, fields):
        ''' add fields from dictionary: {'<fieldname>':'type'} '''
        for f in fields.keys():
            arcpy.AddField_management(tab, f, fields[f])
        return tab

    def _makeTempTable(self, name, fields):
        tab = os.path.join("in_memory", "inTable")
        arcpy.CreateTable_management(os.path.dirname(tab),
                                     os.path.basename(tab))
        if not fields:
            tab = self._addFieldsToTable(tab, fields)
        return tab

    def makeRingsFromDistances(self):
        ''' make geodesic rings from distance list '''
        # make a table for TableToEllipse
        fields = {'x':'DOUBLE', 'y':'DOUBLE', 'd':'DOUBLE'}
        inTable = _makeTempTable("inTable", fields)
        insertTab = arcpy.da.InsertCursor(inTable, fields.keys())
        for i in range(0, (self.center.pointCount - 1)):
            ptArray = self.center.getPart(i)
            pt = ptArray.getObject(0)
            for r in self.rangeList:
                insertTab.insertRow(pt.X, pt.Y, r)
        del insertTab
        outFeatures = os.path.join("in_memory", "outRings")
        arcpy.TableToEllipse_management(inTable, outFeatures,
                                        'x', 'y', 'd', 'd',
                                        self.distanceUnits,
                                        '#', '#', '#', self.sr)
        del inTable
        self.ringFeatures = outFeatures
        return outFeatures

    def makeRadials(self, numRadials):
        ''' make geodesic radials from number of radials '''
        segmentAngle = 360.0/numRadials
        segmentAngleList = range(0.0, 360.0, segmentAngle)
        fields = {'x':'DOUBLE', 'y':'DOUBLE', 'd':'DOUBLE', 'a':'DOUBLE'}

        self.radialFeatures = outRadialFeatures
        return outRadialFeatures

    def saveRingsAsFeatures(self, outputFeatureClass):
        ''' save rings to featureclass '''
        arcpy.CopyFeatures_management(self.ringFeatures, outputFeatureClass)
        return outputFeatureClass
