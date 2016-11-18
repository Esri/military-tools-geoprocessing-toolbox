# coding: utf-8
'''
------------------------------------------------------------------------------
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
--------------------------------------------------------------------------

 ==================================================
 ConversionUtilities.py
 --------------------------------------------------
 requirments: ArcGIS 10.3.1+, Python 2.7 or Python 3.4
 author: ArcGIS Solutions
 contact: support@esri.com
 company: Esri
 ==================================================
 description:
 Utility module for conversion tools.
 Supports the following tools:
 * Table To Line Of Bearing
 * Table To Polygon
 ==================================================
 history:
 11/15/2016 - MF - Original writeup
 11/16/2016 - MF - Added Table To Line Of Bearing
 ==================================================

'''

import os
import sys
import arcpy
from arcpy import env
import traceback

debug = True
srWGS84 = arcpy.SpatialReference(4326) # GCS_WGS_1984
#srWAZED = arcpy.SpatialReference() # World Azimuthal Equidistant
    
def polylineToPolygon(inputPolylines, inputIDFieldName, outputPolygons):
    '''
    Converts polyline to polygon features. All closed features will
    be converted to polygons. Unclosed polylines, or polylines with
    less than 2 vertices will not convert.
    
    inputPolylines - input polyline feature class
    idFieldName - field in inputPolylines to separate individual features
    outputPolygons - polygon feature class to be created
    
    returns polygon feature class
    '''
    try:
        env.overwriteOutput = True
        #Create output Poly FC
        sr = arcpy.Describe(inputPolylines).spatialReference
        if debug:
            arcpy.AddMessage("Spatial reference is " + str(sr.name))
        arcpy.AddMessage("Creating output feature class...")
        outpolygonsFC = arcpy.CreateFeatureclass_management(os.path.dirname(outputPolygons),
                                                            os.path.basename(outputPolygons),
                                                            "POLYGON",
                                                            "#",
                                                            "#",
                                                            "#",
                                                            sr)
    
        
        inFields = ["SHAPE@"]
        if inputIDFieldName:
            #Add ID field
            arcpy.AddMessage("Adding ID field: %s ..." % str(inputIDFieldName))
            arcpy.AddField_management(outpolygonsFC,inputIDFieldName,"TEXT")
            inFields = ["SHAPE@", inputIDFieldName]
            
        arcpy.AddMessage("Opening cursors ...")
        #Open Search cursor on polyline
        inRows = arcpy.da.SearchCursor(inputPolylines, inFields)
    
        #Open Insert cursor on polygons
        outRows = arcpy.da.InsertCursor(outpolygonsFC,inFields)
    
        for row in inRows:
            feat = row[0]
            if inputIDFieldName:
                inID = row[1]
    
            if debug:
                arcpy.AddMessage("Building points from lines.")
            #Build array of points for the line
            polyArray = arcpy.Array()
            partnum = 0
            for part in feat:
                for pnt in feat.getPart(partnum):
                    polyArray.add(arcpy.Point(pnt.X, pnt.Y))
                partnum += 1
    
            if debug:
                arcpy.AddMessage("Creating polygon from points.")
            #convert the array to a polygon, and insert the features
            outPoly = arcpy.Polygon(polyArray)
            if inputIDFieldName:
                outRows.insertRow([outPoly, inID])
            else:
                outRows.insertRow([outPoly])
    
        #close cursors
        del outRows
        del inRows
        return outputPolygons
    
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
        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
        msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages() + "\n"

        # Return python error messages for use in script tool or Python Window
        arcpy.AddError(pymsg)
        arcpy.AddError(msgs)

        # Print Python error messages for use in Python / Python Window
        print(pymsg + "\n")
        print(msgs)

def addUniqueRowID(dataset, fieldName="JoinID"):
    '''
    Adds a unique row "ID" to each row in an input table
    
    dataset - table to get the ID field
    fieldName - name of the field to add. Default is "JoinID"
    
    returns orignal table
    '''
    try:
        counter = 1
        # add unique ID field
        arcpy.AddMessage("Adding LONG field " + str(fieldName))
        arcpy.AddField_management(dataset,fieldName,"LONG")
    
        # add unique numbers to each row
        fields = [str(fieldName)]
        arcpy.AddMessage("Adding unique row IDs...")
        rows = arcpy.da.UpdateCursor(dataset,fields)
        for row in rows:
            row[0] = counter
            rows.updateRow(row)
            counter += 1
        del rows
        
        # set output
        return dataset
        
    
    except arcpy.ExecuteError:
        error = True
        # Get the tool error messages 
        msgs = arcpy.GetMessages() 
        arcpy.AddError(msgs) 
        #print msgs #UPDATE
        print(msgs)
    
    except:
        # Get the traceback object
        error = True
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
    
        # Concatenate information together concerning the error into a message string
        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
        msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages() + "\n"
    
        # Return python error messages for use in script tool or Python Window
        arcpy.AddError(pymsg)
        arcpy.AddError(msgs)
    
        # Print Python error messages for use in Python / Python Window
        #print pymsg + "\n" #UPDATE
        print(pymsg + "\n")
        #print msgs #UPDATE
        print(msgs)

def _formatLat(sLat):
    '''
    For DD latitude fields with "S" hemisphere indicators,
    change to "-"
    '''
    if sLat[-1:] == "S":
       sLat = -1.0 * float(sLat[:-1])
    else:
       sLat = float(sLat[:-1])
    return sLat

def _formatLon(sLon):
    '''
    for DD longitude fields with "W" hemisphere indicators,
    change to "-"
    '''
    if sLon[-1:] == "W":
       sLon = -1.0 * float(sLon[:-1])
    else:
       sLon = float(sLon[:-1])
    return sLon

''' TOOL METHODS '''
def tableToLineOfBearing(inputTable,
                         inputCoordinateFormat,
                         inputXField,
                         inputYField,
                         inputBearingUnits,
                         inputBearingField,
                         inputDistanceUnits,
                         outputLineFeatures,
                         inputLineType,
                         inputSpatialReference):
    '''
    Tool method for converting a table of starting points, bearings, and distances
    to line features.
    
    inputTable - input table, each row will be a separate line feature in output
    inputCoordinateFormat - coordinate notation format of input vertices
    inputXField - field in inputTable for vertex x-coordinate, or full coordinate
    inputYField - field in inputTable for vertex y-coordinate, or None
    inputBearingUnits -
    inputBearingField -
    inputDistanceUnits -
    inputDistanceField -
    outputLineFeatures - polyline feature class to create
    inputLineType - 
    inputSpatialReference - spatial reference of input coordinates
    
    returns polyline feature class
    
    inputCoordinateFormat must be one of the following:
    •	DD_1: Both longitude and latitude values are in a single field. Two values are separated by a space, a comma, or a slash.
    •	DD_2: Longitude and latitude values are in two separate fields.
    •	DDM_1: Both longitude and latitude values are in a single field. Two values are separated by a space, a comma, or a slash.
    •	DDM_2: Longitude and latitude values are in two separate fields.
    •	DMS_1: Both longitude and latitude values are in a single field. Two values are separated by a space, a comma, or a slash.
    •	DMS_2: Longitude and latitude values are in two separate fields.
    •	GARS: Global Area Reference System. Based on latitude and longitude, it divides and subdivides the world into cells.
    •	GEOREF: World Geographic Reference System. A grid-based system that divides the world into 15-degree quadrangles and then subdivides into smaller quadrangles.
    •	UTM_ZONES: The letter N or S after the UTM zone number designates only North or South hemisphere.
    •	UTM_BANDS: The letter after the UTM zone number designates one of the 20 latitude bands. N or S does not designate a hemisphere.
    •	USNG: United States National Grid. Almost exactly the same as MGRS but uses North American Datum 1983 (NAD83) as its datum.
    •	MGRS: Military Grid Reference System. Follows the UTM coordinates and divides the world into 6-degree longitude and 20 latitude bands, but MGRS then further subdivides the grid zones into smaller 100,000-meter grids. These 100,000-meter grids are then divided into 10,000-meter, 1,000-meter, 100-meter, 10-meter, and 1-meter grids.
    •	SHAPE: Only available when a point feature layer is selected as input. The coordinates of each point are used to define the output format
    
    inputBearingUnits must be one of the following:
    •	DEGREES
    •	MILS
    •	RADS
    •	GRAD
    
    inputDistanceUnits must be one of the following:
    •	METERS
    •	KILOMETERS
    •	MILES
    •	NAUTICAL_MILES
    •	FEET
    •	US_SURVEY_FEET
    
    inputLineType must be one of the following:
    
    '''
    deleteme = []
    try:
        deleteme = []
        scratch = 'in_memory'
        if env.scratchWorkspace:
            scratch = env.scratchWorkspace
            
        if not inputSpatialReference:
            arcpy.AddMessage("Defaulting to {0}".format(srWGS84.name))
            inputSpatialReference = srWGS84
            
        copyRows = os.path.join(scratch, "copyRows")
        arcpy.CopyRows_management(inputTable, copyRows)
        
        copyCCN = os.path.join(scratch, "copyCCN")
        arcpy.ConvertCoordinateNotation_management(copyRows,
                                                   copyCCN,
                                                   inputXField,
                                                   inputYField,
                                                   inputCoordinateFormat,
                                                   "DD_2",
                                                   "#",
                                                   inputSpatialReference.exportToString())
        
        # Fix DDLat and DDLon field values
        fields = ['DDLat', 'DDLon']
        with arcpy.da.UpdateCursor(copyCCN, fields) as rows:
            for row in rows:
                # update latitude
                row[0] = _formatLat(row[0])
                # update longitude
                row[1] = _formatLon(row[1])
                rows.updateRow(row)
        del row
        del rows
                    
        arcpy.BearingDistanceToLine_management(copyCCN,
                                               outputLineFeatures,
                                               "DDLon",
                                               "DDLat",
                                               inputDistanceField,
                                               inputDistanceUnits,
                                               inputBearingField,
                                               inputBearingUnits,
                                               inputLineType,
                                               "#",
                                               inputSpatialReference)
        
        return outputLineFeatures
    
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
        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
        msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages() + "\n"

        # Return python error messages for use in script tool or Python Window
        arcpy.AddError(pymsg)
        arcpy.AddError(msgs)

        # Print Python error messages for use in Python / Python Window
        print(pymsg + "\n")
        print(msgs)
        
    finally:
        if debug == False and len(deleteme) > 0:
            # cleanup intermediate datasets
            if debug == True: arcpy.AddMessage("Removing intermediate datasets...")
            for i in deleteme:
                if debug == True: arcpy.AddMessage("Removing: " + str(i))
                arcpy.Delete_management(i)
            if debug == True: arcpy.AddMessage("Done")

def tableToPolygon(inputTable, inputCoordinateFormat,
                   inputXField, inputYField,
                   outputPolygonFeatures, inputLineField,
                   inputSortField, inputSpatialReference):
    '''
    Tool method for converting a table of vertices to polygon features.
    
    inputTable - input table, each row is a vertex
    inputCoordinateFormat - coordinate notation format of input vertices
    inputXField - field in inputTable for vertex x-coordinate, or full coordinate
    inputYField - field in inputTable for vertex y-coordinate, or None
    outputPolygnFeatures - polygon feature class to create
    inputLineField - field in inputTable to identify separate polygons
    inputSortField - field in inputTable to sort vertices
    inputSpatialReference - spatial reference of input coordinates
    
    returns polygon feature class
    
    inputCoordinateFormat must be one of the following:
    •	DD_1: Both longitude and latitude values are in a single field. Two values are separated by a space, a comma, or a slash.
    •	DD_2: Longitude and latitude values are in two separate fields.
    •	DDM_1: Both longitude and latitude values are in a single field. Two values are separated by a space, a comma, or a slash.
    •	DDM_2: Longitude and latitude values are in two separate fields.
    •	DMS_1: Both longitude and latitude values are in a single field. Two values are separated by a space, a comma, or a slash.
    •	DMS_2: Longitude and latitude values are in two separate fields.
    •	GARS: Global Area Reference System. Based on latitude and longitude, it divides and subdivides the world into cells.
    •	GEOREF: World Geographic Reference System. A grid-based system that divides the world into 15-degree quadrangles and then subdivides into smaller quadrangles.
    •	UTM_ZONES: The letter N or S after the UTM zone number designates only North or South hemisphere.
    •	UTM_BANDS: The letter after the UTM zone number designates one of the 20 latitude bands. N or S does not designate a hemisphere.
    •	USNG: United States National Grid. Almost exactly the same as MGRS but uses North American Datum 1983 (NAD83) as its datum.
    •	MGRS: Military Grid Reference System. Follows the UTM coordinates and divides the world into 6-degree longitude and 20 latitude bands, but MGRS then further subdivides the grid zones into smaller 100,000-meter grids. These 100,000-meter grids are then divided into 10,000-meter, 1,000-meter, 100-meter, 10-meter, and 1-meter grids.
    •	SHAPE: Only available when a point feature layer is selected as input. The coordinates of each point are used to define the output format
        
    '''
    try:
        deleteme = []
        scratch = 'in_memory'
        if env.scratchWorkspace:
            scratch = env.scratchWorkspace
            
        if not inputSpatialReference:
            arcpy.AddMessage("Defaulting to {0}".format(srWGS84.name))
            inputSpatialReference = srWGS84
        
        copyRows = os.path.join(scratch, "copyRows")
        arcpy.CopyRows_management(inputTable, copyRows)
        copyCCN = os.path.join(scratch, "copyCCN")
        
        arcpy.ConvertCoordinateNotation_management(copyRows,
                                                   copyCCN,
                                                   inputXField,
                                                   inputYField,
                                                   inputCoordinateFormat,
                                                   "DD_2",
                                                   "#",
                                                   inputSpatialReference.exportToString())
        
        copyPointsToLine = os.path.join(scratch, "copyPointsToLine")
        arcpy.PointsToLine_management(copyCCN,
                                      copyPointsToLine,
                                      inputLineField,
                                      inputSortField,
                                      "CLOSE")
        
        polylineToPolygon(copyPointsToLine, inputLineField, outputPolygonFeatures)
        
        return outputPolygonFeatures
    
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
        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
        msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages() + "\n"

        # Return python error messages for use in script tool or Python Window
        arcpy.AddError(pymsg)
        arcpy.AddError(msgs)

        # Print Python error messages for use in Python / Python Window
        print(pymsg + "\n")
        print(msgs)
        
    finally:
        if debug == False and len(deleteme) > 0:
            # cleanup intermediate datasets
            if debug == True: arcpy.AddMessage("Removing intermediate datasets...")
            for i in deleteme:
                if debug == True: arcpy.AddMessage("Removing: " + str(i))
                arcpy.Delete_management(i)
            if debug == True: arcpy.AddMessage("Done")