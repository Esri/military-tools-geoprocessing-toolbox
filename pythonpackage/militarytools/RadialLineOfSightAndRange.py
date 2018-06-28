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
 RadialLineOfSightAndRange.py
 --------------------------------------------------
 requirements: ArcGIS 10.3+, Python 2.7+
 author: ArcGIS Solutions
 contact: support@esri.com
 company: Esri
 ==================================================
 description:
 Creates a viewshed within a range fan based on input parameters
 ==================================================
'''

import math
import os
import arcpy

DEBUG = False

def drawWedge(cx, cy, r1, r2, startBearing, endBearing):

    # Convert to radians and from north bearing to XY angle 
    start = math.radians(90.0 - startBearing)
    # Adjust end if it crosses 360
    if startBearing > endBearing:
        endBearing = endBearing + 360.0
    end = math.radians(90.0 - endBearing)

    point = arcpy.Point()
    array = arcpy.Array()

    # Calculate the end x,y for the wedge
    x_end = cx + r2*math.cos(start)
    y_end = cy + r2*math.sin(start)

    # Use intervalInDegrees as the angle step value for each circle point
    intervalInDegrees = 5
    intervalInRadians = math.radians(intervalInDegrees)

    # Calculate the outer edge of the wedge
    a = start

    # If r1 == 0 then create a wedge from the center point
    if r1 == 0:
        #Add the start point to the array
        point.X = cx
        point.Y = cy
        array.add(point)
        #Calculate the rest of the wedge
        while a >= end:
            point.X = cx + r2*math.cos(a)
            point.Y = cy + r2*math.sin(a)
            array.add(point)
            a -= intervalInRadians
        #Close the polygon
        point.X = cx
        point.Y = cy
        array.add(point)
    else:
        # Calculate the outer edge of the wedge (clockwise)
        while a >= end:
            point.X = cx + r2*math.cos(a)
            point.Y = cy + r2*math.sin(a)
            a -= intervalInRadians
            array.add(point)

        # Step back one interval - so angle matches last point added above  
        a += intervalInRadians

        # Calculate the inner edge of the wedge (counter-clockwise)
        while a <= start:
            point.X = cx + r1*math.cos(a)
            point.Y = cy + r1*math.sin(a)
            a += intervalInRadians
            array.add(point)

        # Close the polygon by adding the end point
        point.X = x_end
        point.Y = y_end
        array.add(point)

    #Create the polygon
    polygon = arcpy.Polygon(array)

    return polygon

def surfaceContainsPoints(pointFeatures, surfaceRaster):
    '''
    Check if points fall within surface extent, return True or False

    Note: projects both surface extent and pointFeatures to WGS84 so both will 
    have same Spatial Reference and within checks will work 
    '''
    surfaceDesc = arcpy.Describe(surfaceRaster)
    pointsDesc = arcpy.Describe(pointFeatures)

    surfaceSR = surfaceDesc.spatialReference
    pointsSR = pointsDesc.spatialReference

    # Warn if not the same Spatial Reference
    if (surfaceSR.Name != pointsSR.Name) or (surfaceSR.FactoryCode != pointsSR.FactoryCode) :
        arcpy.AddWarning('SurfaceContainsPoints: Spatial References do not match: ' \
            + pointsSR.Name + ' != ' + surfaceSR.Name + ' -or- ' \
            + str(pointsSR.FactoryCode) + ' != ' + str(surfaceSR.FactoryCode))

    surfaceExtent = surfaceDesc.extent

    srWGS84 = arcpy.SpatialReference(4326) # GCS_WGS_1984
    projSurfaceExtent = surfaceExtent.projectAs(srWGS84) 

    pointRows = arcpy.da.SearchCursor(pointFeatures, ["SHAPE@"])

    isWithin = False

    for pointRow in pointRows:
    
        point = pointRow[0]   
        projPoint = point.projectAs(srWGS84).firstPoint

        isWithin = projSurfaceExtent.contains(projPoint) # pointProj.within(surfaceExtent)  

        x = projPoint.X  
        y = projPoint.Y 
          
        if not isWithin : 
            arcpy.AddMessage("Point:({0}, {1})\n Within:({2})\n sr: {3}\n".format(x, y, \
                projSurfaceExtent, surfaceSR.name))
            break

    if DEBUG: arcpy.AddMessage("Input Points Within Surface: {0}".format(isWithin))

    return isWithin

# Solution reused from:
# http://joshwerts.com/blog/2015/09/10/arcpy-dot-project-in-memory-featureclass/
# create destination feature class using the source as a template to establish schema
# and set destination spatial reference
def copyFeaturesAndProject(source_fc, out_projected_fc, spatial_reference):
    """ projects source_fc to out_projected_fc using cursors (and supports in_memory workspace) """
    path, name = os.path.split(out_projected_fc)
    arcpy.management.CreateFeatureclass(path, name, \
                                        arcpy.Describe(source_fc).shapeType, \
                                        template=source_fc, \
                                        spatial_reference=spatial_reference)

    # specify copy of all fields from source to destination
    fields = ["Shape@"] + [f.name for f in arcpy.ListFields(source_fc) if not f.required]

    # project source geometries on the fly while inserting to destination featureclass
    with arcpy.da.SearchCursor(source_fc, fields, spatial_reference=spatial_reference) as source_curs, \
        arcpy.da.InsertCursor(out_projected_fc, fields) as ins_curs:
        for row in source_curs:
            ins_curs.insertRow(row)

def addViewshedFields(observerPointsFC, innerRadiusInput, outerRadiusInput, \
    leftAzimuthInput, rightAzimuthInput, observerOffsetInput, targetOffsetInput):

    desc = arcpy.Describe(observerPointsFC)
    fieldNames = [x.name for x in desc.Fields]

    # arcpy.AddMessage('Current Fields: ' + str(fieldNames))
    
    if "RADIUS1" not in fieldNames : 
        arcpy.AddField_management(observerPointsFC, "RADIUS1", "SHORT")
    arcpy.CalculateField_management(observerPointsFC, "RADIUS1", innerRadiusInput, "PYTHON_9.3", "")

    if "RADIUS2" not in fieldNames : 
        arcpy.AddField_management(observerPointsFC, "RADIUS2", "SHORT")
    arcpy.CalculateField_management(observerPointsFC, "RADIUS2", outerRadiusInput, "PYTHON_9.3", "")

    if "AZIMUTH1" not in fieldNames : 
        arcpy.AddField_management(observerPointsFC, "AZIMUTH1", "SHORT")
    arcpy.CalculateField_management(observerPointsFC, "AZIMUTH1", leftAzimuthInput, "PYTHON_9.3", "")

    if "AZIMUTH2" not in fieldNames : 
        arcpy.AddField_management(observerPointsFC, "AZIMUTH2", "SHORT")
    arcpy.CalculateField_management(observerPointsFC, "AZIMUTH2", rightAzimuthInput, "PYTHON_9.3", "")

    if "OFFSETA" not in fieldNames : 
        arcpy.AddField_management(observerPointsFC, "OFFSETA", "SHORT")
    arcpy.CalculateField_management(observerPointsFC, "OFFSETA", observerOffsetInput, "PYTHON_9.3", "")

    if "OFFSETB" not in fieldNames : 
        arcpy.AddField_management(observerPointsFC, "OFFSETB", "SHORT")
    arcpy.CalculateField_management(observerPointsFC, "OFFSETB", targetOffsetInput, "PYTHON_9.3", "")

def createViewshed(inputObserverPoints, elevationRaster, outerRadiusInput, \
    leftAzimuthInput, rightAzimuthInput, observerOffsetInput, \
    innerRadiusInput, viewshed, sectorWedge, fullWedge):

    # Error Checking:
    if arcpy.CheckExtension("3D") != "Available":
        arcpy.AddError("3D license is not available.")
        return

    if not arcpy.Exists(inputObserverPoints) :
        arcpy.AddError('Dataset does not exist: ' + str(inputObserverPoints))
        return

    if not arcpy.Exists(elevationRaster) :
        arcpy.AddError('Dataset does not exist: ' + str(elevationRaster))
        return

    inputPointsCount = int(arcpy.GetCount_management(inputObserverPoints).getOutput(0))
    if inputPointsCount == 0 :
        arcpy.AddError('No features in input feature set: ' + str(inputObserverPoints))
        return

    elevDesc = arcpy.Describe(elevationRaster)
    elevationSR = elevDesc.spatialReference

    if not elevationSR.type == "Projected":
        msgErrorNonProjectedSurface = \
            "Error: Input elevation raster must be in a projected coordinate system. Existing elevation raster is in {0}.".format(elevationSR.name)
        arcpy.AddError(msgErrorNonProjectedSurface)
        return

    # Done error checking, do processing:
    arcpy.env.outputCoordinateSystem = elevationSR

    donutWedges = []
    pieWedges = []

    tempObserverPoints = r"in_memory\tempPoints"
    copyFeaturesAndProject(inputObserverPoints, tempObserverPoints, elevationSR)

    # Check if points falls within surface extent
    isWithin = surfaceContainsPoints(tempObserverPoints, elevationRaster)
    if not isWithin:
        msgErrorPointNotInSurface = \
            "Error: Input Observer(s) does not fall within the extent of the input surface: {0}!".format(os.path.basename(elevationRaster))
        arcpy.AddError(msgErrorPointNotInSurface)
        return

    addViewshedFields(tempObserverPoints, innerRadiusInput, outerRadiusInput, \
        leftAzimuthInput, rightAzimuthInput, observerOffsetInput, \
        0) # Set Target Height to 0

    arcpy.AddMessage("Buffering observers...")
    arcpy.Buffer_analysis(tempObserverPoints, \
        r"in_memory\OuterBuffer", "RADIUS2", "FULL", "ROUND", "NONE", "", "GEODESIC")

    desc = arcpy.Describe(r"in_memory\OuterBuffer")
    xMin = desc.Extent.XMin
    yMin = desc.Extent.YMin
    xMax = desc.Extent.XMax
    yMax = desc.Extent.YMax
    Extent = str(xMin) + " " + str(yMin) + " " + str(xMax) + " " + str(yMax)

    arcpy.env.extent = desc.Extent

    # Set Raster Output Mask (to improve performance)
    arcpy.env.mask = r"in_memory\OuterBuffer"

    arcpy.AddMessage("Clipping image to observer buffer...")
    arcpy.Clip_management(elevationRaster, Extent, r"in_memory\clip")

    arcpy.AddMessage("Calculating viewshed...")
    arcpy.Viewshed_3d("in_memory\clip", tempObserverPoints, r"in_memory\intervis", "1", "FLAT_EARTH", "0.13")

    arcpy.AddMessage("Creating features from raster...")
    arcpy.RasterToPolygon_conversion(in_raster=r"in_memory\intervis", out_polygon_features=r"in_memory\unclipped",simplify="NO_SIMPLIFY")

    fields = ["SHAPE@XY","RADIUS1","RADIUS2","AZIMUTH1","AZIMUTH2"]
    ## get the attributes from the input point
    with arcpy.da.SearchCursor(tempObserverPoints,fields) as cursor:
        for row in cursor:
            centerX      = row[0][0]
            centerY      = row[0][1]
            radiusInner  = row[1]
            radiusOuter  = row[2]
            startBearing = row[3]
            endBearing   = row[4]

            # TODO/IMPORTANT: radius must be in map units
            donutWedge = drawWedge(centerX, centerY, radiusInner, radiusOuter, startBearing, endBearing)
            donutWedges.append(donutWedge)

            pieWedge = drawWedge(centerX, centerY, 0, radiusOuter, startBearing, endBearing)
            pieWedges.append(pieWedge)

    arcpy.CopyFeatures_management(donutWedges, sectorWedge)
    arcpy.CopyFeatures_management(pieWedges, fullWedge)

    arcpy.AddMessage("Finishing output features...")
    arcpy.Clip_analysis(r"in_memory\unclipped", sectorWedge, r"in_memory\dissolve")
    arcpy.Dissolve_management(r"in_memory\dissolve", viewshed, "gridcode", "", "MULTI_PART", "DISSOLVE_LINES")

    # Output Symbol layer requires the field to be "VISIBILITY"
    arcpy.AddField_management(viewshed, "VISIBILITY", "LONG")
    arcpy.CalculateField_management(viewshed, "VISIBILITY", '!gridcode!', "PYTHON_9.3")

def main():

    ########Script Parameters########

    inputObserverPoints = arcpy.GetParameterAsText(0)
    elevationRaster     = arcpy.GetParameterAsText(1)
    outerRadiusInput    = arcpy.GetParameterAsText(2)
    leftAzimuthInput    = arcpy.GetParameterAsText(3)
    rightAzimuthInput   = arcpy.GetParameterAsText(4)
    observerOffsetInput = arcpy.GetParameterAsText(5)
    innerRadiusInput    = arcpy.GetParameterAsText(6)
    viewshed    = arcpy.GetParameterAsText(7)
    sectorWedge = arcpy.GetParameterAsText(8)
    fullWedge   = arcpy.GetParameterAsText(9)

    createViewshed(inputObserverPoints, elevationRaster, \
        outerRadiusInput, leftAzimuthInput, rightAzimuthInput, observerOffsetInput, \
        innerRadiusInput, viewshed, sectorWedge, fullWedge)

# MAIN =============================================
if __name__ == "__main__":

    main()
