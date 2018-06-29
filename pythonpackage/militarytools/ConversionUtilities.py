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
 * Table To 2-Point Line
 * Table To Ellipse
 * Table To Line Of Bearing
 * Table To Point
 * Table To Polygon
 ==================================================
 history:
 11/15/2016 - MF - Original writeup
 11/16/2016 - MF - Added Table To Line Of Bearing
 11/21/2016 - MF - Added other script tools
 12/08/2016 - MF - Fix for JoinID failing in Pro with OBJECTID (#181, #182, #183)
 ==================================================
'''

import os
import sys
import arcpy
from arcpy import env
import traceback
import types

debug = True
srWGS84 = arcpy.SpatialReference(4326) # GCS_WGS_1984
#srWAZED = arcpy.SpatialReference() # World Azimuthal Equidistant

unitsAngle = ["DEGREES", "MILS", "RADS", "GRADS"]
unitsDistance = ["METERS", "KILOMETERS",
                 "MILES", "NAUTICAL_MILES",
                 "FEET", "US_SURVEY_FEET"]
formatsCoordinateNotation = ["DD_1", "DD_2",
                             "DDM_1", "DDM_2",
                             "DMS_1", "DMS_2",
                             "GARS", "GEOREF",
                             "UTM", "MGRS",
                             "USNG"]
formatsLineTypes = ["GEODESIC", "GREAT_CIRCLE", "RHUMB_LINE", "NORMAL_SECTION"]
joinExcludeFields = ['OBJECTID', 'OID', 'ObjectID',
                     'SHAPE', 'Shape', 'Shape_Length', 'Shape_Area', 'JoinID']

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
        # if debug:
        #     arcpy.AddMessage("Spatial reference is " + str(sr.name))
        #     arcpy.AddMessage("Creating output feature class...")
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
            if debug:
                arcpy.AddMessage("Adding ID field: %s ..." % str(inputIDFieldName))
            arcpy.AddField_management(outpolygonsFC,inputIDFieldName, "TEXT")
            inFields = ["SHAPE@", inputIDFieldName]

        if debug:
            arcpy.AddMessage("Converting Polylines to Polygons...")

        #Open Search cursor on polyline
        inRows = arcpy.da.SearchCursor(inputPolylines, inFields)
    
        #Open Insert cursor on polygons
        outRows = arcpy.da.InsertCursor(outpolygonsFC, inFields)
    
        polyArray = arcpy.Array()

        rowCount = 0

        for row in inRows:

            rowCount += 1

            # Provide feedback, since this method may take a while for large datasets
            if debug and not (rowCount % 100):
                arcpy.AddMessage('Processing Row: ' + str(rowCount))

            if inputIDFieldName:
                inID = str(row[1])

            # Polyline will only have one part
            featShape = row[0]
            polyline = featShape.getPart(0)

            polyArray.removeAll()
            polyArray.append(polyline)

            outPoly = arcpy.Polygon(polyArray, sr)

            if inputIDFieldName:
                outRows.insertRow([outPoly, inID])
            else:
                outRows.insertRow([outPoly])

        if debug:
            arcpy.AddMessage("Done converting polylines to polygons ...")
                
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

        # add unique ID field if it does not already exist
        desc = arcpy.Describe(dataset)
        if not fieldName in [field.name for field in desc.Fields] :
            if debug: arcpy.AddMessage("Adding Text field: " + str(fieldName))
            arcpy.AddField_management(dataset, fieldName, "TEXT")
    
        # add unique numbers to each row
        updatedFields = [str(fieldName)]
        arcpy.AddMessage("Adding unique row IDs...")
        rows = arcpy.da.UpdateCursor(dataset, updatedFields)
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

def _tableFieldNames(inputTable, excludeList):
    '''
    Uses arcpy.ListFields to get a list of field NAMES
    
    inputTable - input table to get field names from
    excludeList - list of field names that will NOT be included in the returned list
    
    returns list of strings
    '''
    try:
        fieldNames = []
        #if debug: arcpy.AddMessage("Excluding fields: {0}".format(excludeList))
        for f in arcpy.ListFields(inputTable):
            if not excludeList:
                if not f.name in excludeList:
                    #arcpy.AddMessage("Adding {0}.".format(f.name))
                    fieldNames.append(f.name)
            else:
                fieldNames.append(f.name)
        return fieldNames
    
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
    
def _checkSpatialRef(inputSpatialReference):
    '''
    if None make it WGS_84, if it is an object, make it a string
    '''
    if not inputSpatialReference:
        arcpy.AddMessage("Defaulting to {0}".format(srWGS84.name))
        inputSpatialReference = srWGS84
    elif not isinstance(inputSpatialReference, str if sys.version_info[0] >= 3 else basestring):
        inputSpatialReference = inputSpatialReference.exportToString()
    return inputSpatialReference

''' TOOL METHODS '''

def tableTo2PointLine(inputTable,
                        inputStartCoordinateFormat,
                        inputStartXField,
                        inputStartYField,
                        inputEndCoordinateFormat,
                        inputEndXField,
                        inputEndYField,
                        outputLineFeatures,
                        inputLineType,
                        inputSpatialReference):
    '''
    Creates line features from a start point coordinate and an endpoint coordinate.

    inputTable - Input Table
    inputStartCoordinateFormat - Start Point Format (from Value List)
    inputStartXField - Start X Field (longitude, UTM, MGRS, USNG, GARS, GEOREF)(from Input Table)
    inputStartYField - Start Y Field (latitude)(from Input Table)
    inputEndCoordinateFormat - End Point Format (from Value List)
    inputEndXField - End X Field (longitude, UTM, MGRS, USNG, GARS, GEOREF)(from Input Table)
    inputEndYField - End Y Field (latitude) (from Input Table)
    outputLineFeatures - Output Line
    inputLineType - Line Type (from Value List)
    inputSpatialReference - Spatial Reference, default is GCS_WGS_1984

    returns line feature class

    inputStartCoordinateFormat and inputEndCoordinateFormat must be one of the following:
    * DD_1: Both longitude and latitude values are in a single field. Two values are separated by a space, a comma, or a slash.
    * DD_2: Longitude and latitude values are in two separate fields.
    * DDM_1: Both longitude and latitude values are in a single field. Two values are separated by a space, a comma, or a slash.
    * DDM_2: Longitude and latitude values are in two separate fields.
    * DMS_1: Both longitude and latitude values are in a single field. Two values are separated by a space, a comma, or a slash.
    * DMS_2: Longitude and latitude values are in two separate fields.
    * GARS: Global Area Reference System. Based on latitude and longitude, it divides and subdivides the world into cells.
    * GEOREF: World Geographic Reference System. A grid-based system that divides the world into 15-degree quadrangles and then subdivides into smaller quadrangles.
    * UTM_ZONES: The letter N or S after the UTM zone number designates only North or South hemisphere.
    * UTM_BANDS: The letter after the UTM zone number designates one of the 20 latitude bands. N or S does not designate a hemisphere.
    * USNG: United States National Grid. Almost exactly the same as MGRS but uses North American Datum 1983 (NAD83) as its datum.
    * MGRS: Military Grid Reference System. Follows the UTM coordinates and divides the world into 6-degree longitude and 20 latitude bands, but MGRS then further subdivides the grid zones into smaller 100,000-meter grids. These 100,000-meter grids are then divided into 10,000-meter, 1,000-meter, 100-meter, 10-meter, and 1-meter grids.
    
    inputLineType must be one of the following:
    * GEODESIC:
    * GREAT_CIRCLE:
    * RHUMB_LINE:
    * NORMAL_SECTION:

    '''
    try:
        # get/set environment
        env.overwriteOutput = True
        
        deleteme = []
        scratch = '%scratchGDB%'
        
        joinFieldName = "JoinID"
        startXFieldName = "startX"
        startYFieldName = "startY"
        endXFieldName = "endX"
        endYFieldName = "endY"
        
        if env.scratchWorkspace:
            scratch = env.scratchWorkspace
        
        inputSpatialReference = _checkSpatialRef(inputSpatialReference)
            
        copyRows = os.path.join(scratch, "copyRows")
        arcpy.CopyRows_management(inputTable, copyRows)
        originalTableFieldNames = _tableFieldNames(inputTable, joinExcludeFields)
        addUniqueRowID(copyRows, joinFieldName)
        
        #Convert Start Point
        arcpy.AddMessage("Formatting start point...")
        startCCN = os.path.join(scratch, "startCCN")
        arcpy.ConvertCoordinateNotation_management(copyRows,
                                                   startCCN,
                                                   inputStartXField,
                                                   inputStartYField,
                                                   inputStartCoordinateFormat,
                                                   "DD_NUMERIC",
                                                   joinFieldName)
        arcpy.AddField_management(startCCN, startXFieldName, "DOUBLE")
        arcpy.CalculateField_management(startCCN, startXFieldName, "!DDLon!","PYTHON_9.3")
        arcpy.AddField_management(startCCN, startYFieldName, "DOUBLE")
        arcpy.CalculateField_management(startCCN, startYFieldName, "!DDLat!","PYTHON_9.3")
        arcpy.JoinField_management(copyRows, joinFieldName,
                                   startCCN, joinFieldName,
                                   [startXFieldName, startYFieldName]) 

        #Convert End Point
        arcpy.AddMessage("Formatting end point...")
        endCCN = os.path.join(scratch, "endCCN")
        arcpy.ConvertCoordinateNotation_management(copyRows,
                                                   endCCN,
                                                   inputEndXField,
                                                   inputEndYField,
                                                   inputEndCoordinateFormat,
                                                   "DD_NUMERIC",
                                                   joinFieldName)
        arcpy.AddField_management(endCCN, endXFieldName, "DOUBLE")
        arcpy.CalculateField_management(endCCN, endXFieldName, "!DDLon!","PYTHON_9.3")
        arcpy.AddField_management(endCCN, endYFieldName, "DOUBLE")
        arcpy.CalculateField_management(endCCN, endYFieldName, "!DDLat!","PYTHON_9.3")
        arcpy.JoinField_management(copyRows, joinFieldName,
                                   endCCN, joinFieldName,
                                   [endXFieldName, endYFieldName])

        #XY TO LINE
        arcpy.AddMessage("Connecting start point to end point as {0}...".format(inputLineType))
        arcpy.XYToLine_management(copyRows,
                                  outputLineFeatures,
                                  startXFieldName, startYFieldName,
                                  endXFieldName, endYFieldName,
                                  inputLineType,
                                  joinFieldName,
                                  inputSpatialReference)
        
        #Join original table fields to output
        arcpy.AddMessage("Joining fields from input table to output line features...")
        arcpy.JoinField_management(outputLineFeatures, joinFieldName,
                                   copyRows, joinFieldName,
                                   originalTableFieldNames)
        
        arcpy.DeleteField_management(outputLineFeatures, [joinFieldName,
                                                startXFieldName, startYFieldName,
                                                endXFieldName, endYFieldName])

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
        if len(deleteme) > 0:
            # cleanup intermediate datasets
            if debug == True: arcpy.AddMessage("Removing intermediate datasets...")
            for i in deleteme:
                if debug == True: arcpy.AddMessage("Removing: " + str(i))
                arcpy.Delete_management(i)
            if debug == True: arcpy.AddMessage("Done")

def tableToEllipse(inputTable,
                   inputCoordinateFormat,
                   inputXField,
                   inputYField,
                   inputMajorAxisField,
                   inputMinorAxisField,
                   inputDistanceUnits,
                   outputEllipseFeatures,
                   inputAzimuthField,
                   inputAzimuthUnits,
                   inputSpatialReference):

    '''
    inputTable - input table, each row will be a separate line feature in output
    inputCoordinateFormat - coordinate notation format of input vertices
    inputXField - field in inputTable for vertex x-coordinate, or full coordinate
    inputYField - field in inputTable for vertex y-coordinate, or None
    inputMajorAxisField -
    inputMinorAxisField - 
    inputDistanceUnits -
    outputEllipseFeatures - polyline feature class to create
    inputAzimuthField - field in inputTable of rotation of ellipse from north
    inputAzimuthUnits - angular units of azimuth (rotation)
    inputSpatialReference - spatial reference of input coordinates
    
    returns polygon ellipse feature class
    
    inputCoordinateFormat must be one of the following:
    * DD_1: Both longitude and latitude values are in a single field. Two values are separated by a space, a comma, or a slash.
    * DD_2: Longitude and latitude values are in two separate fields.
    * DDM_1: Both longitude and latitude values are in a single field. Two values are separated by a space, a comma, or a slash.
    * DDM_2: Longitude and latitude values are in two separate fields.
    * DMS_1: Both longitude and latitude values are in a single field. Two values are separated by a space, a comma, or a slash.
    * DMS_2: Longitude and latitude values are in two separate fields.
    * GARS: Global Area Reference System. Based on latitude and longitude, it divides and subdivides the world into cells.
    * GEOREF: World Geographic Reference System. A grid-based system that divides the world into 15-degree quadrangles and then subdivides into smaller quadrangles.
    * UTM_ZONES: The letter N or S after the UTM zone number designates only North or South hemisphere.
    * UTM_BANDS: The letter after the UTM zone number designates one of the 20 latitude bands. N or S does not designate a hemisphere.
    * USNG: United States National Grid. Almost exactly the same as MGRS but uses North American Datum 1983 (NAD83) as its datum.
    * MGRS: Military Grid Reference System. Follows the UTM coordinates and divides the world into 6-degree longitude and 20 latitude bands, but MGRS then further subdivides the grid zones into smaller 100,000-meter grids. These 100,000-meter grids are then divided into 10,000-meter, 1,000-meter, 100-meter, 10-meter, and 1-meter grids.
    
    inputAzimuthUnits must be one of the following:
    * DEGREES
    * MILS
    * RADS
    * GRAD
    
    inputDistanceUnits must be one of the following:
    * METERS
    * KILOMETERS
    * MILES
    * NAUTICAL_MILES
    * FEET
    * US_SURVEY_FEET
    '''
    try:
        env.overwriteOutput = True

        deleteme = []
        scratch = '%scratchGDB%'
        joinFieldName = "JoinID"
        
        if env.scratchWorkspace:
            scratch = env.scratchWorkspace
            
        inputSpatialReference = _checkSpatialRef(inputSpatialReference)
            
        copyRows = os.path.join(scratch, "copyRows")
        arcpy.CopyRows_management(inputTable, copyRows)
        deleteme.append(copyRows)
        originalTableFieldNames = _tableFieldNames(inputTable, joinExcludeFields)
        addUniqueRowID(copyRows, joinFieldName)
        
        copyCCN = os.path.join(scratch, "copyCCN")
        arcpy.ConvertCoordinateNotation_management(copyRows,
                                                   copyCCN,
                                                   inputXField,
                                                   inputYField,
                                                   inputCoordinateFormat,
                                                   "DD_NUMERIC",
                                                   joinFieldName,
                                                   inputSpatialReference)
        deleteme.append(copyCCN)
    
        #Table To Ellipse
        copyEllipse = os.path.join(scratch, "copyEllipse")
        arcpy.TableToEllipse_management(copyCCN,
                                        copyEllipse,
                                        "DDLon", "DDLat",
                                        inputMajorAxisField,
                                        inputMinorAxisField,
                                        inputDistanceUnits,
                                        inputAzimuthField,
                                        inputAzimuthUnits,
                                        joinFieldName,
                                        inputSpatialReference)
        deleteme.append(copyEllipse)
        
        #Polyline To Polygon
        polylineToPolygon(copyEllipse, joinFieldName, outputEllipseFeatures)
        
        #Join original table fields to output
        arcpy.AddMessage("Joining fields from input table to output line features...")
        arcpy.JoinField_management(outputEllipseFeatures, joinFieldName,
                                   copyRows, joinFieldName,
                                   originalTableFieldNames)
        
        arcpy.DeleteField_management(outputEllipseFeatures,
                                     [joinFieldName])

        return outputEllipseFeatures
    
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
        if len(deleteme) > 0:
            # cleanup intermediate datasets
            if debug : arcpy.AddMessage("Removing intermediate datasets...")
            for i in deleteme:
                if debug : arcpy.AddMessage("Removing Temp Dataset: " + str(i))
                # Comment this next line to skip delete:
                arcpy.Delete_management(i)
        if debug : arcpy.AddMessage("Done")

def tableToLineOfBearing(inputTable,
                         inputCoordinateFormat,
                         inputXField,
                         inputYField,
                         inputBearingUnits,
                         inputBearingField,
                         inputDistanceUnits,
                         inputDistanceField,
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
    * DD_1: Both longitude and latitude values are in a single field. Two values are separated by a space, a comma, or a slash.
    * DD_2: Longitude and latitude values are in two separate fields.
    * DDM_1: Both longitude and latitude values are in a single field. Two values are separated by a space, a comma, or a slash.
    * DDM_2: Longitude and latitude values are in two separate fields.
    * DMS_1: Both longitude and latitude values are in a single field. Two values are separated by a space, a comma, or a slash.
    * DMS_2: Longitude and latitude values are in two separate fields.
    * GARS: Global Area Reference System. Based on latitude and longitude, it divides and subdivides the world into cells.
    * GEOREF: World Geographic Reference System. A grid-based system that divides the world into 15-degree quadrangles and then subdivides into smaller quadrangles.
    * UTM_ZONES: The letter N or S after the UTM zone number designates only North or South hemisphere.
    * UTM_BANDS: The letter after the UTM zone number designates one of the 20 latitude bands. N or S does not designate a hemisphere.
    * USNG: United States National Grid. Almost exactly the same as MGRS but uses North American Datum 1983 (NAD83) as its datum.
    * MGRS: Military Grid Reference System. Follows the UTM coordinates and divides the world into 6-degree longitude and 20 latitude bands, but MGRS then further subdivides the grid zones into smaller 100,000-meter grids. These 100,000-meter grids are then divided into 10,000-meter, 1,000-meter, 100-meter, 10-meter, and 1-meter grids.
    
    inputBearingUnits must be one of the following:
    * DEGREES
    * MILS
    * RADS
    * GRAD
    
    inputDistanceUnits must be one of the following:
    * METERS
    * KILOMETERS
    * MILES
    * NAUTICAL_MILES
    * FEET
    * US_SURVEY_FEET
    
    inputLineType must be one of the following:
    * GEODESIC:
    * GREAT_CIRCLE:
    * RHUMB_LINE:
    * NORMAL_SECTION:
    
    '''
    try:
        env.overwriteOutput = True

        deleteme = []
        joinFieldName = "JoinID"
        scratch = '%scratchGDB%'
        if env.scratchWorkspace:
            scratch = env.scratchWorkspace
            
        inputSpatialReference = _checkSpatialRef(inputSpatialReference)
            
        copyRows = os.path.join(scratch, "copyRows")
        arcpy.CopyRows_management(inputTable, copyRows)
        originalTableFieldNames = _tableFieldNames(inputTable, joinExcludeFields)
        addUniqueRowID(copyRows, joinFieldName)
        
        arcpy.AddMessage("Formatting start point...")
        copyCCN = os.path.join(scratch, "copyCCN")
        arcpy.ConvertCoordinateNotation_management(copyRows,
                                                   copyCCN,
                                                   inputXField,
                                                   inputYField,
                                                   inputCoordinateFormat,
                                                   "DD_NUMERIC",
                                                   joinFieldName,
                                                   inputSpatialReference)
        
        arcpy.AddMessage("Creating lines as {0}...".format(inputLineType))
        arcpy.BearingDistanceToLine_management(copyCCN,
                                               outputLineFeatures,
                                               "DDLon",
                                               "DDLat",
                                               inputDistanceField,
                                               inputDistanceUnits,
                                               inputBearingField,
                                               inputBearingUnits,
                                               inputLineType,
                                               joinFieldName,
                                               inputSpatialReference)
        
        #Join original table fields to output
        arcpy.AddMessage("Joining fields from input table to output line features...")
        arcpy.JoinField_management(outputLineFeatures, joinFieldName,
                                   copyRows, joinFieldName,
                                   originalTableFieldNames)
        arcpy.DeleteField_management(outputLineFeatures,
                                     [joinFieldName])
        
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
        if len(deleteme) > 0:
            # cleanup intermediate datasets
            if debug == True: arcpy.AddMessage("Removing intermediate datasets...")
            for i in deleteme:
                if debug == True: arcpy.AddMessage("Removing: " + str(i))
                arcpy.Delete_management(i)
            if debug == True: arcpy.AddMessage("Done")

def tableToPoint(inputTable,
                 inputCoordinateFormat,
                 inputXField,
                 inputYField,
                 outputPointFeatures,
                 inputSpatialReference):
    '''
    Converts table of coordinate formats to point features.
    
    inputTable - input table, each row will be a separate line feature in output
    inputCoordinateFormat - coordinate notation format of input vertices
    inputXField - field in inputTable for vertex x-coordinate, or full coordinate
    inputYField - field in inputTable for vertex y-coordinate, or None
    outputPointFeatures - output point features to create
    inputSpatialReference - spatial reference of input coordinates
    
    returns point feature class
    
    inputCoordinateFormat must be one of the following:
    * DD_1: Both longitude and latitude values are in a single field. Two values are separated by a space, a comma, or a slash.
    * DD_2: Longitude and latitude values are in two separate fields.
    * DDM_1: Both longitude and latitude values are in a single field. Two values are separated by a space, a comma, or a slash.
    * DDM_2: Longitude and latitude values are in two separate fields.
    * DMS_1: Both longitude and latitude values are in a single field. Two values are separated by a space, a comma, or a slash.
    * DMS_2: Longitude and latitude values are in two separate fields.
    * GARS: Global Area Reference System. Based on latitude and longitude, it divides and subdivides the world into cells.
    * GEOREF: World Geographic Reference System. A grid-based system that divides the world into 15-degree quadrangles and then subdivides into smaller quadrangles.
    * UTM_ZONES: The letter N or S after the UTM zone number designates only North or South hemisphere.
    * UTM_BANDS: The letter after the UTM zone number designates one of the 20 latitude bands. N or S does not designate a hemisphere.
    * USNG: United States National Grid. Almost exactly the same as MGRS but uses North American Datum 1983 (NAD83) as its datum.
    * MGRS: Military Grid Reference System. Follows the UTM coordinates and divides the world into 6-degree longitude and 20 latitude bands, but MGRS then further subdivides the grid zones into smaller 100,000-meter grids. These 100,000-meter grids are then divided into 10,000-meter, 1,000-meter, 100-meter, 10-meter, and 1-meter grids.

    '''
    try:
        env.overwriteOutput = True
       
        deleteme = []
        scratch = '%scratchGDB%'
        if env.scratchWorkspace:
            scratch = env.scratchWorkspace
            
        inputSpatialReference = _checkSpatialRef(inputSpatialReference)
        
        arcpy.ConvertCoordinateNotation_management(inputTable,
                                                   outputPointFeatures,
                                                   inputXField,
                                                   inputYField,
                                                   inputCoordinateFormat,
                                                   "DD_NUMERIC",
                                                   "#",
                                                   inputSpatialReference)
        return outputPointFeatures
    
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
        if len(deleteme) > 0:
            # cleanup intermediate datasets
            if debug == True: arcpy.AddMessage("Removing intermediate datasets...")
            for i in deleteme:
                if debug == True: arcpy.AddMessage("Removing: " + str(i))
                arcpy.Delete_management(i)
            if debug == True: arcpy.AddMessage("Done")

def tableToPolygon(inputTable,
                   inputCoordinateFormat,
                   inputXField,
                   inputYField,
                   outputPolygonFeatures,
                   inputLineField,
                   inputSortField,
                   inputSpatialReference):
    '''
    Tool method for converting a table of vertices to polygon features.
    
    inputTable - input table, each row is a vertex
    inputCoordinateFormat - coordinate notation format of input vertices
    inputXField - field in inputTable for vertex x-coordinate, or full coordinate
    inputYField - field in inputTable for vertex y-coordinate, or None
    outputPolygonFeatures - polygon feature class to create
    inputLineField - field in inputTable to identify separate polygons
    inputSortField - field in inputTable to sort vertices
    inputSpatialReference - spatial reference of input coordinates
    
    returns polygon feature class
    
    inputCoordinateFormat must be one of the following:
    * DD_1: Both longitude and latitude values are in a single field. Two values are separated by a space, a comma, or a slash.
    * DD_2: Longitude and latitude values are in two separate fields.
    * DDM_1: Both longitude and latitude values are in a single field. Two values are separated by a space, a comma, or a slash.
    * DDM_2: Longitude and latitude values are in two separate fields.
    * DMS_1: Both longitude and latitude values are in a single field. Two values are separated by a space, a comma, or a slash.
    * DMS_2: Longitude and latitude values are in two separate fields.
    * GARS: Global Area Reference System. Based on latitude and longitude, it divides and subdivides the world into cells.
    * GEOREF: World Geographic Reference System. A grid-based system that divides the world into 15-degree quadrangles and then subdivides into smaller quadrangles.
    * UTM_ZONES: The letter N or S after the UTM zone number designates only North or South hemisphere.
    * UTM_BANDS: The letter after the UTM zone number designates one of the 20 latitude bands. N or S does not designate a hemisphere.
    * USNG: United States National Grid. Almost exactly the same as MGRS but uses North American Datum 1983 (NAD83) as its datum.
    * MGRS: Military Grid Reference System. Follows the UTM coordinates and divides the world into 6-degree longitude and 20 latitude bands, but MGRS then further subdivides the grid zones into smaller 100,000-meter grids. These 100,000-meter grids are then divided into 10,000-meter, 1,000-meter, 100-meter, 10-meter, and 1-meter grids.
        
    '''
    try:
        env.overwriteOutput = True

        deleteme = []
        scratch = '%scratchGDB%'
        if env.scratchWorkspace:
            scratch = env.scratchWorkspace
            
        inputSpatialReference = _checkSpatialRef(inputSpatialReference)
        
        copyRows = os.path.join(scratch, "copyRows")
        arcpy.CopyRows_management(inputTable, copyRows)
        copyCCN = os.path.join(scratch, "copyCCN")
        
        arcpy.ConvertCoordinateNotation_management(copyRows,
                                                   copyCCN,
                                                   inputXField,
                                                   inputYField,
                                                   inputCoordinateFormat,
                                                   "DD_NUMERIC",
                                                   "#",
                                                   inputSpatialReference)
        
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
        if len(deleteme) > 0:
            # cleanup intermediate datasets
            if debug == True: arcpy.AddMessage("Removing intermediate datasets...")
            for i in deleteme:
                if debug == True: arcpy.AddMessage("Removing: " + str(i))
                arcpy.Delete_management(i)
            if debug == True: arcpy.AddMessage("Done")
              
def tableToPolyline(inputTable,
                    inputCoordinateFormat,
                    inputXField,
                    inputYField,
                    outputPolylineFeatures,
                    inputLineField,
                    inputSortField,
                    inputSpatialReference):
    '''
    Converts a table of vertices to one or more polyline features.
    
    inputTable - input table, each row is a vertex
    inputCoordinateFormat - coordinate notation format of input vertices
    inputXField - field in inputTable for vertex x-coordinate, or full coordinate
    inputYField - field in inputTable for vertex y-coordinate, or None
    outputPolylineFeatures - polyline feature class to create
    inputLineField - field in inputTable to identify separate polylines
    inputSortField - field in inputTable to sort vertices
    inputSpatialReference - spatial reference of input coordinates
    
    returns polyline feature class
    
    inputCoordinateFormat must be one of the following:
    * DD_1: Both longitude and latitude values are in a single field. Two values are separated by a space, a comma, or a slash.
    * DD_2: Longitude and latitude values are in two separate fields.
    * DDM_1: Both longitude and latitude values are in a single field. Two values are separated by a space, a comma, or a slash.
    * DDM_2: Longitude and latitude values are in two separate fields.
    * DMS_1: Both longitude and latitude values are in a single field. Two values are separated by a space, a comma, or a slash.
    * DMS_2: Longitude and latitude values are in two separate fields.
    * GARS: Global Area Reference System. Based on latitude and longitude, it divides and subdivides the world into cells.
    * GEOREF: World Geographic Reference System. A grid-based system that divides the world into 15-degree quadrangles and then subdivides into smaller quadrangles.
    * UTM_ZONES: The letter N or S after the UTM zone number designates only North or South hemisphere.
    * UTM_BANDS: The letter after the UTM zone number designates one of the 20 latitude bands. N or S does not designate a hemisphere.
    * USNG: United States National Grid. Almost exactly the same as MGRS but uses North American Datum 1983 (NAD83) as its datum.
    * MGRS: Military Grid Reference System. Follows the UTM coordinates and divides the world into 6-degree longitude and 20 latitude bands, but MGRS then further subdivides the grid zones into smaller 100,000-meter grids. These 100,000-meter grids are then divided into 10,000-meter, 1,000-meter, 100-meter, 10-meter, and 1-meter grids.
     
    '''
    try:
        env.overwriteOutput = True

        deleteme = []
        joinFieldName = "JoinID"
        scratch = '%scratchGDB%'
        if env.scratchWorkspace:
            scratch = env.scratchWorkspace
            
        inputSpatialReference = _checkSpatialRef(inputSpatialReference)
        
        copyRows = os.path.join(scratch, "copyRows")
        arcpy.CopyRows_management(inputTable, copyRows)
        addUniqueRowID(copyRows, joinFieldName)
        
        copyCCN = os.path.join(scratch, "copyCCN")
        arcpy.ConvertCoordinateNotation_management(copyRows,
                                                   copyCCN,
                                                   inputXField,
                                                   inputYField,
                                                   inputCoordinateFormat,
                                                   "DD_NUMERIC",
                                                   joinFieldName,
                                                   inputSpatialReference)
        
        arcpy.PointsToLine_management(copyCCN,
                                      outputPolylineFeatures,
                                      inputLineField,
                                      inputSortField,
                                      "NO_CLOSE")
        
        return outputPolylineFeatures
    
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
        if len(deleteme) > 0:
            # cleanup intermediate datasets
            if debug == True: arcpy.AddMessage("Removing intermediate datasets...")
            for i in deleteme:
                if debug == True: arcpy.AddMessage("Removing: " + str(i))
                arcpy.Delete_management(i)
            if debug == True: arcpy.AddMessage("Done")