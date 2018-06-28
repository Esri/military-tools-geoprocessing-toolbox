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
------------------------------------------------------------------------------
 ==================================================
 VisibilityUtilities.py
 --------------------------------------------------
 requirements: ArcGIS 10.3+, Python 2.7 or Python 3.4
 author: ArcGIS Solutions
 contact: support@esri.com
 company: Esri
 ==================================================
 description:
 Provides methods for Visibility tools:
 * Add LLOS Fields
 * Add RLOS Observer Fields
 * Find Local Peaks
 ==================================================
 history:
 11/28/2016 - mf - Original coding
 11/29/2016 - mf - Added Find Local Peaks tool
 12/2/2016 - mf - Added additional tools
 12/6/2016 - mf - LLOS and profile graph
 12/12/2016 - mf - fix #189 - extra escape char in local srWAZED
 ==================================================
'''

# IMPORTS ==========================================
import os
import sys
import re
import traceback
import arcpy
from arcpy import env
import pylab
import math

# LOCALS ===========================================
deleteme = [] # intermediate datasets to be deleted
debug = True # extra messaging during development
srWGS84 = arcpy.SpatialReference(4326) # GCS_WGS_1984
srWAZED = arcpy.SpatialReference(54032) # World Azimuthal Equidistant
llosFields = {"OFFSET":[2.0, "Offset height above surface"]}
rlosFields = {"OFFSETA":[2.0, "Observer offset above surface"],
              "OFFSETB":[0.0, "Target offset above surface"],
              "RADIUS1":[0.0, "Minimum range from observer"],
              "RADIUS2":[1000.0, "Maximum range from observer"],
              "AZIMUTH1":[0.0, "Left azimuth"],
              "AZIMUTH2":[360.0, "Right azimuth"],
              "VERT1":[90.0, "Top vertical angle"],
              "VERT2":[-90.0, "Bottom vertical angle"]}
acceptableDistanceUnits = ['METERS', 'KILOMETERS',
                           'MILES', 'NAUTICAL_MILES',
                           'FEET', 'US_SURVEY_FEET']
joinExcludeFields = ['OBJECTID', 'OID', 'ObjectID',
                     'SHAPE', 'Shape', 'Shape_Length', 'Shape_Area']
scratch = None

# FUNCTIONS ========================================
def _getFieldNameList(targetTable, excludeList):
    '''
    Returns a list of field names from targetTable
    '''
    nameList = []
    try:
        if not targetTable:
            raise Exception("Source table {0} does not exist or is null.".format(targetTable))
        fields = arcpy.ListFields(targetTable)
        for field in fields:
            if not excludeList or not excludeList == []:
                if not field.name in excludeList:
                    nameList.append(field.name.upper())
            else:
                nameList.append(field.name.upper())
        return nameList
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

def _addDoubleField(targetTable, fieldsToAdd):
    '''
    Adds a list of fields to a targetTable
    '''
    try:
        existingFields = _getFieldNameList(targetTable, joinExcludeFields)
        for currentField in list(fieldsToAdd.keys()):
            if currentField in existingFields:
                arcpy.AddWarning("Field {0} is already in {1}. Skipping this field name.".format(currentField, targetTable))
            else:
                fName = currentField
                fDefault = float(fieldsToAdd[currentField][0])
                fAlias = fieldsToAdd[currentField][1]
                if debug: arcpy.AddMessage("Adding field {0} with alias {1}".format(fName,fAlias))
                arcpy.AddField_management(targetTable,
                                          fName,
                                          "DOUBLE",
                                          '',
                                          '',
                                          '',
                                          fAlias) 
        return targetTable
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

def _calculateDefaultFieldValues(targetTable, fieldsToAdd):
    '''
    Calculates default field values from built-in list
    '''
    try:
        existingFields = _getFieldNameList(targetTable, joinExcludeFields)
        for currentField in fieldsToAdd:
            if not currentField in existingFields:
                arcpy.AddWarning("Cannot calculate default for {0}. Field does not exist in {1}".format(currentField, targetTable))
            else:
                if debug:
                    arcpy.AddMessage("Calculating default for {0}".format(currentField))
                arcpy.CalculateField_management(targetTable,
                                                currentField,
                                                fieldsToAdd[currentField][0],
                                                "PYTHON_9.3")
                
        return targetTable
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

def _calculateFieldValue(targetTable, fieldName, fieldValue):
    '''
    Calculates field value from argument
    '''
    try:
        existingFields = _getFieldNameList(targetTable, joinExcludeFields)
        if not fieldName in existingFields:
            raise Exception("Field {0} is not in {1}".format(fieldName, targetTable))
        else:
            arcpy.CalculateField_management(targetTable,
                                            fieldName,
                                            fieldValue,
                                            "PYTHON_9.3")
        return targetTable
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

def _getRasterMinMax(inputRaster):
    '''
    returns minimum and maximum statistic value from an input raster
    '''
    try:
        min = float(arcpy.GetRasterProperties_management(inputRaster, "MINIMUM").getOutput(0))
        max = float(arcpy.GetRasterProperties_management(inputRaster, "MAXIMUM").getOutput(0))
        if debug: arcpy.AddMessage("_getRasterMinMax min={0}, max={1}".format(min, max))
        return [min, max]
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

def _clipRasterToArea(inputSurface, inputArea, outputClip):
    '''
    returns a raster subset that is clipped from inputSurface using inputArea.
    '''
    try:
        #Need Spatial Analyst to run this tool
        if arcpy.CheckExtension("Spatial") == "Available":
            arcpy.CheckOutExtension("Spatial")
        else:
            raise Exception("Spatial Analyst license is not available.")
        from arcpy import sa
        env.overwriteOutput = True
        arcpy.AddMessage("Clipping {0} to area {1}...".format(os.path.basename(inputSurface),
                                                              os.path.basename(inputArea)))
        saClipSurface = sa.ExtractByMask(inputSurface, inputArea)
        saClipSurface.save(outputClip)
        return outputClip
    
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

def _getUniqueValuesFromField(inputTable, inputField):
    '''
    Get a list of unique values from inputField in inputTable
    '''
    try:
        valueList = []
        with arcpy.da.SearchCursor(inputTable, inputField) as cursor:
            for row in cursor:
                if not row[0] in valueList:
                    valueList.append(row[0])
        valueList.sort(reverse=True)
        #if debug: arcpy.AddMessage("Sorted list: {0}".format(valueList))
        return valueList
    
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

def _getCentroid(inputFeatures):
    '''
    Gets the centroid of Featureclass using Minimum Bounding Geometry's Rectange By Width option
    returns a PointGeometry
    '''
    try:
        featureSR = arcpy.Describe(inputFeatures).spatialReference
        #centroidPoint = None
        observerMBG = os.path.join("in_memory", "observerMBG")
        result = arcpy.MinimumBoundingGeometry_management(inputFeatures,
                                                          observerMBG,
                                                          "RECTANGLE_BY_WIDTH")
        deleteme.append(observerMBG)
        with arcpy.da.SearchCursor(observerMBG, ["SHAPE@"]) as cursor:
            for row in cursor:
                plyCentroid = row[0].centroid
                centroidPoint = arcpy.PointGeometry(plyCentroid, featureSR)
        return centroidPoint
    
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

def _getLocalWAZED(inputPoint):
    '''
    return a localized World Azimuthal Equidistant
    Spatial Reference based on inputPoint as PointGeometry
    '''
    try:
        newSR = arcpy.SpatialReference()
        pntGeom = inputPoint.projectAs(srWGS84)
        pnt = pntGeom.firstPoint
        strAZED = srWAZED.exportToString()
        arcpy.AddMessage("Using Central Meridian: {0}, and Latitude of Origin: {1}.".format(pnt.X, pnt.Y))
        strAZED = re.sub('PARAMETER\[\'Central_Meridian\'\,.+?]',
               'PARAMETER[\'Central_Meridian\',{0}]'.format(str(pnt.X)),
               strAZED)
        strAZED = re.sub('PARAMETER\[\'Latitude_Of_Origin\'\,.+?]',
               'PARAMETER[\'Latitude_Of_Origin\',{0}]'.format(str(pnt.Y)),
               strAZED)
        newSR.loadFromString(strAZED)

        return newSR
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

def _prepPointFromSurface(inputPoints, inputSurface, outputPoints, offsetFieldName, spotFieldName):
    '''
    Adds attributes and SPOT and makes 3D Points
    '''
    try:
        if debug: arcpy.AddMessage("Adding surface info for {0}".format(os.path.basename(inputPoints)))
        zFieldName = "Z"
        # get Z from surface for points
        arcpy.AddSurfaceInformation_3d(inputPoints,
                                       inputSurface,
                                       zFieldName,
                                       "BILINEAR")
        inputPoints = _addDoubleField(inputPoints,
                                      {spotFieldName:[0.0, spotFieldName]})
        # calculate SPOT = Z + OFFSET
        arcpy.CalculateField_management(inputPoints,
                                        spotFieldName,
                                        "!{0}! + !{1}!".format(zFieldName, offsetFieldName),
                                        "PYTHON_9.3")
        
        # Make 3D point from SPOT
        arcpy.FeatureTo3DByAttribute_3d(inputPoints,
                                     outputPoints,
                                     spotFieldName)
        
        return outputPoints
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

def makeProfileGraph(inputFeatures):
    '''
    '''
    
    scratchFolder = arcpy.env.scratchFolder
    srInput = arcpy.Describe(inputFeatures).spatialReference


    try:
        rawLOS = {}
        profileGraphName = "profile"
        # Current: {<SourceOID> : [<TarIsVis>, [<observerD=0.0>,<observerZ>],
        #                                      [<targetD>,<targetZ>],
        #                                      [<segmentList>]]]}
        #
        #             where
        #           [<segment>] is [<visibilityCode>,[d0,...,dN],[z0,...,zN]]
            
        # Unique sight lines
        sightLineIDs = []
        #with arcpy.da.SearchCursor(inputFeatures,["SourceOID","{0}@".format(arcpy.Describe(inputFeatures).oidFieldName)]) as rows:
        with arcpy.da.SearchCursor(inputFeatures,["SourceOID"]) as rows:
            for row in rows:
                thisID = row[0]
                if thisID not in sightLineIDs:
                    sightLineIDs.append(thisID)
        #del rows
        #if debug == True: arcpy.AddMessage("sightLineIDs list: " + str(sightLineIDs))
        arcpy.AddMessage("Found {0} unique sight line IDs ...".format(len(sightLineIDs)))
        
        arcpy.AddField_management(inputFeatures,profileGraphName,"TEXT")
        expression = '"profile" + str(!SourceOID!) + ".png"'
        arcpy.CalculateField_management(inputFeatures,profileGraphName,expression, "PYTHON")
        
        # get visible and non-visible lines for each LLOS
        for currentID in sightLineIDs:
            whereclause = ('"SourceOID" = {0}'.format(currentID))
            tarIsViz = None
            cursorFields = ["OID@","SHAPE@", "SourceOID", "TarIsVis","VisCode","ObsSPOT","TgtSPOT","OID_OBSERV","OID_TARGET"]
            with arcpy.da.SearchCursor(inputFeatures, cursorFields,whereclause) as rows:
                startX = None
                startY = None
                tgtD = 0.0
                line = 0
                segmentList = []
                for row in rows:
                    oid = row[0]
                    geometry = row[1]
                    sourceOID = row[2]
                    targetIsViz = row[3]
                    visibilityCode = row[4]
                    obsD = 0.0
                    obsZ = row[5]
                    tgtZ = row[6]
                    obsID = row[7]
                    tgtID = row[8]
                    partNum = 0
                    point = 0
                    partCount = geometry.partCount
                    #if debug == True: arcpy.AddMessage("OID: " + str(oid))
                    # go through parts in the line
                    for part in geometry:
                        #if debug == True: arcpy.AddMessage("Line: " + str(line) + " Part: " + str(partNum) + " PointCount: " + str(len(part)))
                        segment = []
                        partD = []
                        partZ = []
                        for pnt in part:
                            if (line == 0) and (partNum == 0) and (point == 0): # if it is the very first point in the LLOS
                                startX = pnt.X
                                startY = pnt.Y
                                #if debug == True: arcpy.AddMessage("startX,startY: " + str(startX) + "," + str(startY))
                                distFromStart = 0
                                partD.append(0.0)
                                partZ.append(pnt.Z)
        
                            else: # for all other points in the LLOS
                                distFromStart = math.sqrt((pnt.X - startX)**2 + (pnt.Y - startY)**2)
                                if distFromStart > tgtD:
                                    tgtD = distFromStart
                                partD.append(distFromStart)
                                partZ.append(pnt.Z)
                            point += 1
                            #if debug == True: arcpy.AddMessage("Adding parts to segment ...")
                            segment = [visibilityCode,partD,partZ]
                            #if debug == True: arcpy.AddMessage("\nsegment: " + str(segment) + "\n")
                        partNum += 1
                        #if debug == True: arcpy.AddMessage("Adding segment to segment list ...")
                        segmentList.append(segment)
                    line += 1
            #del rows
            rawLOS[currentID] = [targetIsViz,[obsD,obsZ,obsID],[tgtD,tgtZ,tgtID],segmentList]
        #if debug == True: arcpy.AddMessage("rawLOS: " + str(rawLOS))
        
        # build a graph for each LLOS
        graphLocationDict = {}
        arcpy.AddMessage("Building graphs for lines ...")
        #for llosID in rawLOS.keys(): #UPDATE
        for llosID in list(rawLOS.keys()):
                
                graphInputList = rawLOS[llosID]
                # get the values for the current llos
                # Current: {<SourceOID> : [<TarIsVis>, [<observerD=0.0>,<observerZ>],
                #                                      [<segmentList0>,...,<segmentListN>]]}
                
                targetVisibility = graphInputList[0]
                observer = graphInputList[1]
                obsD = observer[0]
                obsZ = observer[1]
                obsID = observer[2]
                target = graphInputList[2]
                tgtD = target[0]
                tgtZ = target[1]
                tgtID = target[2]
                segmentList = graphInputList[3]
                arcpy.AddMessage("Building graph from observer " + str(obsID) + " to target " + str(tgtID) + " ..." )
                # plot the line of sight
                pylab.plot([obsD,tgtD],[obsZ,tgtZ],'k--',linewidth=1)
                
                # plot the visible profile
                for segment in segmentList:
                    if segment[0] == 1 and len(segment[1]) != 0: # for visible segments - plot in green
                        segmentVizColor = 'g'
                    if segment[0] == 2 and len(segment[1]) != 0: # for non-visible segments - plot in red
                        segmentVizColor = 'r'
                    pylab.plot(segment[1], segment[2], segmentVizColor, linewidth=1)
                    
                # plot observer
                blueFilledCircle = 'bo'
                greenFilledCircle = 'go'
                redFilledCircle = 'ro'
                pylab.plot(obsD, obsZ, blueFilledCircle)
                # plot target
                if targetVisibility == 1:
                    targetSymbol = greenFilledCircle
                else:
                    targetSymbol = redFilledCircle
                pylab.plot(tgtD, tgtZ, targetSymbol)
                
                # titles & labels
                if (targetVisibility == 1):
                    targetVisibilityMsg = "VISIBLE"
                else:
                    targetVisibilityMsg = "NOT VISIBLE"
                pylab.title("Target {0} is {1} to observer {2}".format(tgtID, targetVisibilityMsg, obsID))
                pylab.ylabel("Elevation above sea level")
                pylab.xlabel("Distance to target ({0})".format(srInput.linearUnitName))
                pylab.grid(True)
                
                # save the graph to a PNG file in the scratch folder
                graphPath = os.path.join(scratchFolder, "profile{0}.png".format(llosID))
                #if debug == True: arcpy.AddMessage("graphPath: " + str(graphPath))
                pylab.savefig(graphPath, dpi=900)
                pylab.cla() # clear the graph???
                pylab.close()  #closing pylab to prevent crashes
                
                graphLocationDict[llosID] = graphPath
                deleteme.append(graphPath)
            
        # TODO: start an update cursor
        arcpy.AddMessage("Enabling attachments ...")
        arcpy.EnableAttachments_management(inputFeatures)
        
        matchTable = os.path.join(scratch,"matchTable")
        deleteme.append(matchTable)
        arcpy.AddMessage("Building match table ...")
        arcpy.GenerateAttachmentMatchTable_management(inputFeatures,scratchFolder,matchTable,profileGraphName,"*.png","ABSOLUTE")
        
        arcpy.AddMessage("Attaching profile graphs to sightlines ...")
        inOIDField = arcpy.Describe(inputFeatures).OIDFieldName
        arcpy.AddAttachments_management(inputFeatures,inOIDField,matchTable,"MatchID","Filename")
        
            
        # cleanup
        # arcpy.AddMessage("Removing scratch data ...")
        # for ds in deleteme:
        #     if arcpy.Exists(ds):
        #         arcpy.Delete_management(ds)
        #         if debug == True: arcpy.AddMessage(str(ds))
    
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

''' TOOL METHODS '''

def hi_lowPointByArea(inputAreaFeature,
                      inputSurfaceRaster,
                      hi_low_Switch,
                      outputPointFeature):
    '''
    Finds the highest or lowest point by pixel value in a given inputAreaFeature of inputSurfaceRaster
    inputAreaFeature - input polygon feature
    inputSurfaceRaster - input raster of elevation
    hi_low_Switch - MAXIMUM for highest,
                    or MINIMUM for lowest
    outputPointFeature - point feature class containing results
    
    returns point feature class
    '''
    global scratch
    try:
        # Check if a valid input area is supplied
        if not inputAreaFeature:
            arcpy.AddError("Please provide a valid input area")
            return
        # Check if there are any features in the input area
        if int(arcpy.GetCount_management(inputAreaFeature).getOutput(0)) == 0:
            arcpy.AddError("Please provide at least one input area feature")
            return
        #Need Spatial Analyst to run this tool
        if arcpy.CheckExtension("Spatial") == "Available":
            arcpy.CheckOutExtension("Spatial")
        else:
            raise Exception("Spatial Analyst license is not available.")
        from arcpy import sa
        
        env.overwriteOutput = True
        if arcpy.env.scratchWorkspace:
            scratch = arcpy.env.scratchWorkspace
        else:
            scratch = r"%scratchGDB%"
        
        #Get SR of the surface and set as default output
        surfaceDescribe = arcpy.Describe(inputSurfaceRaster)
        srSurface = surfaceDescribe.spatialReference
        #surfaceCellSize = max(surfaceDescribe.meanCellHeight, surfaceDescribe.meanCellWidth)
        arcpy.env.outputCoordinateSystem = srSurface
        arcpy.AddMessage("Using {0} for analysis.".format(srSurface.name))
        
        #TODO: Warn user if clipping large area of small cells, and processing will take time
            
        #Make a copy of the input Area in the SR of the surface
        tempAreaFeatures = os.path.join(scratch, "tempAreaFeatures")
        arcpy.Project_management(inputAreaFeature,
                                 tempAreaFeatures,
                                 srSurface)
        deleteme.append(tempAreaFeatures)
        
        #TODO: Compare extents of area and surface, if area not inside, raise Exception
        
        #Clipping surface to area
        clipSurface = os.path.join(scratch, "clipSurface")
        clipSurface = _clipRasterToArea(inputSurfaceRaster, tempAreaFeatures, clipSurface)
        deleteme.append(clipSurface)
        
        #Get stats for clipped surface
        filterStatValue = None
        minStatValue, maxStatValue = _getRasterMinMax(clipSurface)
        if hi_low_Switch == "MAXIMUM":
            filterStatValue = maxStatValue
        else:
            filterStatValue = minStatValue
        

        #Filter the cells from clipped raster
        arcpy.AddMessage("Finding cells with {0} value of {1}...".format(hi_low_Switch, filterStatValue))
        expressionSetNull = r"VALUE <> {0}".format(filterStatValue)
        setNull = os.path.join(scratch, "setNull")
        resultSetNull = sa.SetNull(clipSurface, clipSurface, expressionSetNull)
        resultSetNull.save(setNull)
        deleteme.append(setNull)
        
        #Converting to points
        arcpy.RasterToPoint_conversion(setNull, outputPointFeature, "VALUE")
        #Add 'Elevation' field, and remove 'Grid_code'
        addFieldName = "Elevation"
        dropFieldName = "grid_code"
        outputPointFeature = _addDoubleField(outputPointFeature, {addFieldName:[0,addFieldName]})
        expressionCalcField = r"!{0}!".format(dropFieldName)
        arcpy.CalculateField_management(outputPointFeature, addFieldName, expressionCalcField, "PYTHON_9.3")
        arcpy.DeleteField_management(outputPointFeature, [dropFieldName, "pointid"])

        return outputPointFeature
    
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
                if arcpy.Exists(i):
                    if debug == True: arcpy.AddMessage("Removing: " + str(i))
                    arcpy.Delete_management(i)
            if debug == True: arcpy.AddMessage("Done")

def addLLOSFields(inputObserverTable,
                  inputObserverDefault,
                  inputTargetTable,
                  inputTargetDefault):
    '''
    Adds field OFFSET to both observer and target point and line features
    
    inputObserverTable - input observer features
    inputObserverDefault - the input default value to calculate for observer offset
    inputTargetTable - input target features
    inputTargetDefault - the input default value to calculate for target offset
    
    returns list with two feature classes:
    outputObserverTable - inputObserverTable with offset fields added
    outputTargetTable - inputTargetTable with offset fields added
    '''
    try:
        # Add field to Observer table
        env.overwriteOutput = True
        arcpy.AddMessage("Adding Observer fields...")
        outputObserverTable = _addDoubleField(inputObserverTable,
                                      llosFields)
        arcpy.AddMessage("Calculating Observer values...")                              
        outputObserverTable = _calculateFieldValue(outputObserverTable,
                                                   "OFFSET",
                                                   float(inputObserverDefault))
        #Add field to Target table
        arcpy.AddMessage("Adding Target fields...")
        outputTargetTable = _addDoubleField(inputTargetTable,
                                            llosFields)
        arcpy.AddMessage("Calculating Target values...")                                    
        outputObserverTable = _calculateFieldValue(outputTargetTable,
                                                   "OFFSET",
                                                   float(inputTargetDefault))
        
        return [outputObserverTable, outputTargetTable]
    
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
                if arcpy.Exists(i):
                    if debug == True: arcpy.AddMessage("Removing: " + str(i))
                    arcpy.Delete_management(i)
            if debug == True: arcpy.AddMessage("Done")

def addRLOSObserverFields(inputFeatures,
                          inputOFFSETA,
                          inputOFFSETB,
                          inputRADIUS1,
                          inputRADIUS2,
                          inputAZIMUTH1,
                          inputAZIMUTH2,
                          inputVERT1,
                          inputVERT2):
    '''
    Adds Observer fields and values to inputFeatures:
    OFFSETA: observer offset height above surface, default is 2.0
    OFFSETB: surface offset, default is 0.0
    RADIUS1: Near distance, default is 0.0
    RADIUS2: Farthest distance, default is 1000.0
    AZIMUTH1: Left Azimuth in horizontal field of view, default is 0.0
    AZIMUTH2: Right Azimuth in horizontal field of view, default is 360.0
    VERT1: Top Angle in vertical field of view, default is 90.0
    VERT2: Bottom Angle in vertical field of view, default is -90.0
    
    returns the inputFeatures
    
    '''
    try:
        env.overwriteOutput = True
        if not inputOFFSETA: inputOFFSETA = 2.0
        if not inputOFFSETB: inputOFFSETB = 0.0
        if not inputRADIUS1: inputRADIUS1 = 0.0
        if not inputRADIUS2: inputRADIUS2 = 1000.0
        if not inputAZIMUTH1: inputAZIMUTH1 = 0.0
        if not inputAZIMUTH2: inputAZIMUTH2 = 360.0
        if not inputVERT1: inputVERT1 = 90.0
        if not inputVERT2: inputVERT2 = -90.0
        
        _addDoubleField(inputFeatures, rlosFields)
        
        arcpy.AddMessage("Updating Observer values...")        
        _calculateFieldValue(inputFeatures, "OFFSETA", inputOFFSETA)
        _calculateFieldValue(inputFeatures, "OFFSETB", inputOFFSETB)
        _calculateFieldValue(inputFeatures, "RADIUS1", inputRADIUS1)
        _calculateFieldValue(inputFeatures, "RADIUS2", inputRADIUS2)
        _calculateFieldValue(inputFeatures, "AZIMUTH1", inputAZIMUTH1)
        _calculateFieldValue(inputFeatures, "AZIMUTH2", inputAZIMUTH2)
        _calculateFieldValue(inputFeatures, "VERT1", inputVERT1)
        _calculateFieldValue(inputFeatures, "VERT2", inputVERT2)
        
        return inputFeatures
    
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
                if arcpy.Exists(i):
                    if debug == True: arcpy.AddMessage("Removing: " + str(i))
                    arcpy.Delete_management(i)
            if debug == True: arcpy.AddMessage("Done")

def findLocalPeaks(inputAreaFeature,
                   inputNumberOfPeaks,
                   inputSurfaceRaster,
                   outputPeakFeatures):
    '''
    Uses an inverted sinks method to find several local peaks on a surface
    inputAreaFeature - Input Area where to find the peaks
    inputNumberOfPeaks - Number of Highest Points (peaks)  to find
    inputSurfaceRaster - Input Surface to find peaks
    outputPeakFeatures - Output Peak Points to create
    
    returns output point feature class
    '''
    global scratch
    try:
        # Check if a valid input area is supplied
        if not inputAreaFeature:
            arcpy.AddError("Please provide a valid input area")
            return
        # Check if there are any features in the input area
        if int(arcpy.GetCount_management(inputAreaFeature).getOutput(0)) == 0:
            arcpy.AddError("Please provide at least one input area feature")
            return
        #Need Spatial Analyst to run this tool
        if arcpy.CheckExtension("Spatial") == "Available":
            arcpy.CheckOutExtension("Spatial")
        else:
            raise Exception("Spatial Analyst license is not available.")
        from arcpy import sa
        
        env.overwriteOutput = True
        if arcpy.env.scratchWorkspace:
            scratch = arcpy.env.scratchWorkspace
        else:
            scratch = r"%scratchGDB%"            
        
        #Get SR of the surface and set as default output
        surfaceDescribe = arcpy.Describe(inputSurfaceRaster)
        srSurface = surfaceDescribe.spatialReference
        surfaceCellSize = max(surfaceDescribe.meanCellHeight, surfaceDescribe.meanCellWidth)
        arcpy.env.outputCoordinateSystem = srSurface
        arcpy.AddMessage("Using {0} for analysis.".format(srSurface.name))
            
        #Make a copy of the input Area in the SR of the surface
        tempAreaFeatures = os.path.join(scratch, "tempAreaFeatures")
        arcpy.Project_management(inputAreaFeature,
                                 tempAreaFeatures,
                                 srSurface)
        deleteme.append(tempAreaFeatures)
        
        #TODO: Compare extents of area and surface, if area not inside, raise Exception
        
        #Clipping surface to area
        clipSurface = os.path.join(scratch, "clipSurface")
        clipSurface = _clipRasterToArea(inputSurfaceRaster, tempAreaFeatures, clipSurface)
        deleteme.append(clipSurface)
        arcpy.AddMessage("Inverting clipped surface...")
        minStatValue, maxStatValue = _getRasterMinMax(clipSurface)
        invertedMapAlgebra = (((arcpy.Raster(clipSurface) - minStatValue) * -1) + maxStatValue)

        #flow direction & sink
        arcpy.AddMessage("Finding inverted sinks...")
        saFlowDirection = sa.FlowDirection(invertedMapAlgebra, "NORMAL")
        saSink = sa.Sink(saFlowDirection)
        invertedSinks = os.path.join("in_memory", "invertedSinks")
        saSink.save(invertedSinks)
        deleteme.append(invertedSinks)
             
        #need to make sure there is a VAT for GetCount
        arcpy.BuildRasterAttributeTable_management(invertedSinks, "Overwrite")
                   
        #check the number of sink values before proceeding as no sinks will cause an error
        result = arcpy.GetCount_management(invertedSinks)
        numberSinkValues = int(result.getOutput(0))
        
        arcpy.AddMessage("{0} sinks found".format(numberSinkValues))
        
        if numberSinkValues == 0:
            # No sink holes found in input area raise error
            raise Exception("The input area contains no unique peaks")
        else:
            #convert the sink values to a polygon feature class,
            #This prevents adjacent cells of the same pixel value being seen as separate sink areas 
            arcpy.AddMessage("Converting sink values to polygon features...")
            sinkPolys = os.path.join(scratch, "sinkPolys")
            rasterValueField = "Value"
            conversionField = "Gridcode"
            simplifyShape = "NO_SIMPLIFY"
            arcpy.RasterToPolygon_conversion(invertedSinks,
                                             sinkPolys,
                                             simplifyShape,
                                             rasterValueField)
            deleteme.append(sinkPolys)
        
            #convert the polygon fc to a point fc to get central point of each feature
            pointSinks = os.path.join(scratch, "pointSinks")
            arcpy.FeatureToPoint_management(sinkPolys, pointSinks)
            deleteme.append(pointSinks)
            
            #extract values to points
            arcpy.AddMessage("Extracting elevation values from {0}...".format(inputSurfaceRaster))
            sinkValues = os.path.join(scratch, "sinkValues")            
            sa.ExtractValuesToPoints(pointSinks, inputSurfaceRaster, sinkValues, "NONE", "VALUE_ONLY")
            deleteme.append(sinkValues)
            
            #check the number of sink values is greater the the number of peaks inputted by the users
            if(numberSinkValues <  int(inputNumberOfPeaks)):
                arcpy.AddMessage("The input area does not contain {0} unique peaks, returning top {1} peaks...".format(inputNumberOfPeaks, numberSinkValues))
                inputNumberOfPeaks = numberSinkValues
            
            #we need to store the object ids of the top (x) number of peaks
            highestPoint_IDs = []
            
            #File geodatabase do not allow us to use a SQL prefix of TOP so we will have to do it through a search cursor
            with arcpy.da.SearchCursor(sinkValues, ['RASTERVALU','OID@'] ,sql_clause=(None, 'ORDER BY RASTERVALU DESC')) as cursor:
                counter = 1
                for row in cursor:
                  if counter <= int(inputNumberOfPeaks):
                    highestPoint_IDs.append(row[1])
                    counter = counter + 1
            del row
            del cursor
            
            arcpy.MakeFeatureLayer_management(sinkValues, "sortedPoints")
            
            #we need to define a different query if the value number of peaks to find is only 1
            if len(highestPoint_IDs) == 1:
                selectExpression = r'"OBJECTID" = {0}'.format(highestPoint_IDs[0])
            else:
                selectExpression = r'"OBJECTID" IN {0}'.format(tuple(highestPoint_IDs))
            
            arcpy.SelectLayerByAttribute_management("sortedPoints",
                                                    "NEW_SELECTION",
                                                    selectExpression)
            arcpy.CopyFeatures_management("sortedPoints", outputPeakFeatures)
            
            
            # select X highest values.
            valueField = "RASTERVALU"
            uniqueElevationList = _getUniqueValuesFromField(outputPeakFeatures, valueField)
            
            peakCount = arcpy.GetCount_management(outputPeakFeatures).getOutput(0)
            peakList = uniqueElevationList[:int(inputNumberOfPeaks)]
            arcpy.AddMessage("Found {0} peaks of with elevations {1}".format(peakCount, peakList))
                    
            # Add 'Elevation' field
            elevField = "Elevation"
            arcpy.AddField_management(outputPeakFeatures,
                                      elevField,
                                      "DOUBLE")
            calculateFieldExpression = r"!{0}!".format(valueField)
            arcpy.CalculateField_management(outputPeakFeatures,
                                            elevField,
                                            calculateFieldExpression,
                                            "PYTHON_9.3")
            # Remove unnecessary fields
            arcpy.DeleteField_management(outputPeakFeatures, [valueField, "grid_code", "pointid"])

            return outputPeakFeatures
    
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
                if arcpy.Exists(i):
                    if debug == True: arcpy.AddMessage("Removing: " + str(i))
                    arcpy.Delete_management(i)
            if debug == True: arcpy.AddMessage("Done")

def linearLineOfSight(inputObserverFeatures,
                      inputObserverHeight,
                      inputTargetFeatures,
                      inputTargetHeight,
                      inputSurface,
                      outputLineOfSight,
                      outputSightLines,
                      outputObservers,
                      outputTargets,
                      inputObstructionFeatures):
    '''    
    '''
    global scratch
    addProfileGraphToSurfaceLine = True
    try:
        # Check if a valid observer is supplied
        if not inputObserverFeatures:
            arcpy.AddError("Please provide a valid observer")
            return
        # Check if there are any features in the observer
        if int(arcpy.GetCount_management(inputObserverFeatures).getOutput(0)) == 0:
            arcpy.AddError("Please provide at least one observer")
            return
        # Check if a valid target is supplied
        if not inputTargetFeatures:
            arcpy.AddError("Please provide a valid target feature")
            return
        # Check if there are any features for the target
        if int(arcpy.GetCount_management(inputTargetFeatures).getOutput(0)) == 0:
            arcpy.AddError("Please provide at least one target feature")
            return

        #Need Spatial Analyst to run this tool
        if arcpy.CheckExtension("Spatial") == "Available":
            arcpy.CheckOutExtension("Spatial")
        else:
            raise Exception("Spatial Analyst license is not available.")
        from arcpy import sa
        if arcpy.CheckExtension("3D") == "Available":
            arcpy.CheckOutExtension("3D")
        else:
            raise Exception("3D Analyst license is not available.")
        
        if arcpy.env.scratchWorkspace:
            scratch = arcpy.env.scratchWorkspace
        else:
            scratch = r"%scratchGDB%"
        
        #get spatial reference of surface
        srSurface = arcpy.Describe(inputSurface).spatialReference
        offsetFieldName = "OFFSET"
        #Check if Observers have "OFFSET" field
        hasObsOffset, hasTgtOffset = True, True
        inputObsFields = _getFieldNameList(inputObserverFeatures, [])
        if not offsetFieldName in inputObsFields:
            arcpy.AddMessage("OFFSET field not in Observers. Using Observer Height Above Surface value of {0}".format(inputObserverHeight))
            hasObsOffset = False
        #Check if Targets have "OFFSET" field
        inputTgtFields = _getFieldNameList(inputTargetFeatures, [])
        if not offsetFieldName in inputTgtFields:
            arcpy.AddMessage("OFFSET field not in Targets. Using Target Height Above Surface value of {0}".format(inputTargetHeight))
            hasTgtOffset = False
        
        #Project Observers and add fields if needed
        arcpy.AddMessage("Projecting Observers and Targets to Input Surface spatial reference {0}".format(srSurface.name))
        prjObservers = os.path.join(scratch, "prjObservers")
        arcpy.Project_management(inputObserverFeatures,
                                 prjObservers,
                                 srSurface)
        deleteme.append(prjObservers)
        if not hasObsOffset:
            prjObservers = _addDoubleField(prjObservers,
                                           {offsetFieldName:[inputObserverHeight, "Offset above surface"]})
            prjObservers = _calculateFieldValue(prjObservers,
                                                offsetFieldName,
                                                inputObserverHeight)
        #Project targets and add fields
        prjTargets = os.path.join(scratch, "prjTargets")
        arcpy.Project_management(inputTargetFeatures,
                                 prjTargets,
                                 srSurface)
        deleteme.append(prjTargets)
        if not hasTgtOffset:
            prjTargets = _addDoubleField(prjTargets,
                                         {offsetFieldName:[inputTargetHeight, "Offset above surface"]})
            prjTargets = _calculateFieldValue(prjTargets,
                                              offsetFieldName,
                                              inputTargetHeight)

        #Get elevation of Observers and Targets over surface
        obsSpotFieldName = "ObsSPOT"
        dddObservers = os.path.join(scratch, "dddObservers")
        arcpy.AddMessage("Building 3D observer points...")
        dddObservers = _prepPointFromSurface(prjObservers,
                                             inputSurface,
                                             dddObservers,
                                             offsetFieldName,
                                             obsSpotFieldName)
        deleteme.append(dddObservers)
        tgtSpotFieldName = "TgtSPOT"
        dddTargets = os.path.join(scratch,"dddTargets")
        arcpy.AddMessage("Building 3D target points...")
        dddTargets = _prepPointFromSurface(prjTargets,
                                           inputSurface,
                                           dddTargets,
                                           offsetFieldName,
                                           tgtSpotFieldName)
        deleteme.append(dddTargets)
        
        
        #Construct Sight Lines
        arcpy.AddMessage("Constructing Sight Lines between observers and targets...")
        dddSightLines = os.path.join(scratch, "dddSightLines")
        arcpy.ConstructSightLines_3d(dddObservers,
                                     dddTargets,
                                     dddSightLines,
                                     obsSpotFieldName,
                                     tgtSpotFieldName,
                                     None,
                                     None,
                                     "OUTPUT_THE_DIRECTION")
        deleteme.append(dddSightLines)

        #TODO: use Intervisibility_3d to determine obstructions from other data types?

        #Build MBR, set as mask
        arcpy.AddMessage("Building minimum bounding rectangle of sight lines for analysis mask...")
        mbrSightLines = os.path.join(scratch, "mbrSightLines")
        arcpy.MinimumBoundingGeometry_management(dddSightLines,
                                                 mbrSightLines,
                                                 "RECTANGLE_BY_WIDTH")


        #Line Of Sight
        arcpy.AddMessage("Building Line Of Sight...")
        #arcpy.env.mask = mbrSightLines
        llosObstructionPoints = os.path.join(scratch, "llosObstructionPoints")
        #llosResults = os.path.join(scratch, "llosResults")
        arcpy.LineOfSight_3d(inputSurface,
                             dddSightLines,
                             outputLineOfSight,
                             llosObstructionPoints,
                             "#",
                             "#",
                             None,
                             None,
                             inputObstructionFeatures)
        deleteme.append(llosObstructionPoints)
        #deleteme.append(llosResults)


        arcpy.AddMessage("Joining attribute results...")
        #join sightline attributes to surfaceline
        arcpy.JoinField_management(outputLineOfSight,
                                    "SourceOID",
                                    dddSightLines,
                                    "OID",
                                    ["OID_OBSERV",
                                     "OID_TARGET",
                                     "DIST_ALONG",
                                     "AZIMUTH"])
        #join surfaceline attributes to sightline
        arcpy.JoinField_management(dddSightLines,
                                    "OID",
                                    outputLineOfSight,
                                    "SourceOID",
                                    ["TarIsVis",
                                     "OID_OBSERV",
                                     "OID_TARGET"])
        #join observer spot field to surface line
        arcpy.JoinField_management(outputLineOfSight,
                                   "OID_OBSERV",
                                   dddObservers,
                                   arcpy.Describe(dddObservers).oidFieldName,
                                   ["ObsSPOT"])
        #join target spot field to surface line
        arcpy.JoinField_management(outputLineOfSight,
                                   "OID_TARGET",
                                   dddTargets,
                                   arcpy.Describe(dddTargets).oidFieldName,
                                   ["TgtSPOT"])

        #Get target visibility for each target, add to Observers and Targets and Sight Lines
        arcpy.AddMessage("Attributing output Observer features...")
        llosStartVertex = os.path.join(scratch, "llosStartVertex")
        arcpy.FeatureVerticesToPoints_management(dddSightLines,
                                                 llosStartVertex,
                                                 "START")
        deleteme.append(llosStartVertex)
        arcpy.Identity_analysis(llosStartVertex,
                                dddObservers,
                                outputObservers,
                                "ALL")

        #Get target visibility count stats on targets
        arcpy.AddMessage("Calculating frequency on Target features...")
        llosEndVertex = os.path.join(scratch, "llosEndVertex")
        arcpy.FeatureVerticesToPoints_management(dddSightLines,
                                                 llosEndVertex,
                                                 "END")
        arcpy.Identity_analysis(llosEndVertex,
                                dddTargets,
                                outputTargets,
                                "ALL")
        deleteme.append(llosEndVertex)
        arcpy.MakeFeatureLayer_management(outputTargets, "targetLayer")
        arcpy.SelectLayerByAttribute_management("targetLayer",
                                                "NEW_SELECTION",
                                                '''"TarIsVis" = 1''')
        targetStats = os.path.join(scratch, "targetStats")
        statsFields = [["TarIsVis",  "COUNT"]]
        caseField = "OID_TARGET"
        arcpy.Statistics_analysis("targetLayer",
                                targetStats,
                                statsFields,
                                caseField)
        deleteme.append(targetStats)
        arcpy.JoinField_management(outputTargets,
                        caseField,
                        targetStats,
                        caseField,
                        ["FREQUENCY", "COUNT_TarIsVis"])

        #copy outputs
        arcpy.CopyFeatures_management(dddSightLines,
                                      outputSightLines)

        # Build profile graphs for each Line Of Sight
        if addProfileGraphToSurfaceLine:
            arcpy.AddMessage("Building profile graph...")
            makeProfileGraph(outputLineOfSight)

        #drop fields
        #arcpy.DeleteField_management(outputLineOfSight, [])
        arcpy.DeleteField_management(outputSightLines, ["OID_OBSERV_1",
                                                        "OID_TARGET_1"])
        arcpy.DeleteField_management(outputObservers, ["Height",
                                                       "FID_llosStartVertex",
                                                       "OID_OBSERV_1",
                                                       "OID_TARGET_1",
                                                       "ORIG_FID",
                                                       "FID_dddObservers"])
        arcpy.DeleteField_management(outputTargets, ["Height",
                                                     "ORIG_FID",
                                                     "OID_OBSERV_1",
                                                     "OID_TARGET_1",
                                                     "FID_llosEndVertex",
                                                     "FID_dddTargets"])

        return [outputLineOfSight,
                outputSightLines,
                outputObservers,
                outputTargets]


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
            
def radialLineOfSight(inputObserverFeatures,
                      inputObserverHeight,
                      inputRadiusOfObserver,
                      inputSurface,
                      outputVisibility,
                      inputForceVisibility,
                      inputSpatialReference):
    '''
    Builds a viewshed from one or more observer point features and an input surface.
    
    inputObserverFeatures - one or more observer features
    inputObserverHeight - If OFFSETA is not present in inputObserverFeatures use this value
    inputRadiusOfObserver - If RADIUS2 is not present in inputObserverFeatures use this value
    inputSurface - Surface to consider for visibility analysis
    outputVisibility - polygon features showing areas visible and not-visible to observers
    inputForceVisibility - Force visiblity to edge of the surface (use a local, spherical horizon)
    inputSpatial Reference - spatial reference of outputVisibility features
    '''
    global scratch
    
    try:
        #Need Spatial Analyst to run this tool
        if arcpy.CheckExtension("Spatial") == "Available":
            arcpy.CheckOutExtension("Spatial")
        else:
            raise Exception("Spatial Analyst license is not available.")
        from arcpy import sa
        env.overwriteOutput = True
        #Set scratch as temp workspace
        if arcpy.env.scratchWorkspace:
            scratch = arcpy.env.scratchWorkspace
        else:
            scratch = r"%scratchGDB%" 

        #get original spatial reference of inputs
        srObservers = arcpy.Describe(inputObserverFeatures).spatialReference
        srSurface = arcpy.Describe(inputSurface).spatialReference
        
        #Check observer fields for RADIUS2 and OFFSETA
        hasRADIUS2 = True
        hasOFFSETA = True
        observerFieldList = _getFieldNameList(inputObserverFeatures, [])
        if not "RADIUS2" in observerFieldList:
            arcpy.AddMessage("RADIUS2 field not in Input Observer Features. Using Radius Of Observer {0}".format(inputRadiusOfObserver))
            hasRADIUS2 = False
        else:
            inputRadiusOfObserver = _getUniqueValuesFromField(inputObserverFeatures,
                                                              "RADIUS2")[:1][0]
            arcpy.AddMessage("RADIUS2 field in Input Observer Features. Using maximum radius of {0}".format(inputRadiusOfObserver))
        if not "OFFSETA" in observerFieldList:
            arcpy.AddMessage("OFFSETA field not in Input Observer Features. Using Observer Height Above Surface {0}".format(inputObserverHeight))
            hasOFFSETA = False
        
        #get number of observers:
        numberOfObservers = int(arcpy.GetCount_management(inputObserverFeatures).getOutput(0))
        
        #get centroid of observers in Lat/Lon
        arcpy.AddMessage("Getting centroid of input observer points...")
        centroidPoint = _getCentroid(inputObserverFeatures)
        ddCentroidPoint = centroidPoint.projectAs(srWGS84)
        
        #make localized WAZED
        arcpy.AddMessage("Using localized World Azimuthal Equidistant for analysis...")
        srLocalWAZED = _getLocalWAZED(ddCentroidPoint)
        arcpy.env.outputCoordinateSystem = srLocalWAZED
        
        #project Observers to temp dataset in local WAZED
        tempObservers = os.path.join(scratch, "tempObservers")
        arcpy.Project_management(inputObserverFeatures, tempObservers, srLocalWAZED)
        deleteme.append(tempObservers)
        
        #If not hasRADIUS2: add RADIUS2
        if not hasRADIUS2:
            tempObservers = _addDoubleField(tempObservers, {"RADIUS2":[inputRadiusOfObserver, "RADIUS2"]})
            tempObservers = _calculateFieldValue(tempObservers, "RADIUS2", inputRadiusOfObserver)
        #If not hasOFFSETA: add OFFSETA
        if not hasOFFSETA:
            tempObservers = _addDoubleField(tempObservers, {"OFFSETA":[inputObserverHeight, "OFFSETA"]})
            tempObservers = _calculateFieldValue(tempObservers, "OFFSETA", inputObserverHeight)
        
        if inputForceVisibility:
            '''
            if going to infinity what we really need is the distance to the horizon
            based on height/elevation
            '''
            arcpy.AddWarning("Force Visibility To Infinity is not implemented at this time.")
            # arcpy.AddMessage("Finding horizon distance ...")
            # result = arcpy.GetCellValue_management(input_surface,
            #                                        str(ddCentroidPoint.firstPoint.X) + " " +
            #                                        str(ddCentroidPoint.firstPoint.Y))
            # centroid_elev = result.getOutput(0)
            # R2 = float(centroid_elev) + float(maxOffset)
            # # length, in meters, of semimajor axis of WGS_1984 spheroid.
            # R = 6378137.0
            # horizonDistance = math.sqrt(math.pow((R + R2), 2) - math.pow(R, 2))
            # arcpy.AddMessage(str(horizonDistance) + " meters.")
            # horizonExtent = (str(mbgCenterX - horizonDistance) + " " +
            #                  str(mbgCenterY - horizonDistance) + " " +
            #                  str(mbgCenterX + horizonDistance) + " " +
            #                  str(mbgCenterY + horizonDistance))
            # # since we are doing infinity we can drop the RADIUS2 field
            # arcpy.AddMessage("Analysis to edge of surface, dropping RADIUS2 field ...")
            # arcpy.DeleteField_management(observers, "RADIUS2")
        
        #Buffer observers
        bufferObservers = os.path.join(scratch, "bufferObservers")
        distanceUnits = "METERS"
        bufferDistance = "{0} {1}".format(inputRadiusOfObserver, distanceUnits)
        arcpy.AddMessage("Buffering observers to {0}".format(bufferDistance))
        arcpy.Buffer_analysis(tempObservers,
                              bufferObservers,
                              bufferDistance,
                              "FULL",
                              "ROUND",
                              "ALL",
                              None,
                              "GEODESIC")
        deleteme.append(bufferObservers)

        arcpy.AddMessage("Projecting observers to match surface...")
        observersSurfaceSR = os.path.join(scratch, "observersSurfaceSR")
        arcpy.Project_management(tempObservers,
                                 observersSurfaceSR,
                                 srSurface,
                                 None,
                                 srLocalWAZED,
                                 "PRESERVE_SHAPE")
        deleteme.append(observersSurfaceSR)
        arcpy.AddMessage("Projecting buffer to match surface...")
        bufferSurfaceSR = os.path.join(scratch, "bufferSurfaceSR")
        arcpy.Project_management(bufferObservers,
                                 bufferSurfaceSR,
                                 srSurface,
                                 None,
                                 srLocalWAZED,
                                 "PRESERVE_SHAPE")
        deleteme.append(bufferSurfaceSR)
        
        arcpy.AddMessage("Clipping image to observer buffers...")
        
        clipSurface = os.path.join(scratch, "clipSurface")

        clipSurface = _clipRasterToArea(inputSurface, bufferSurfaceSR, clipSurface)        
        deleteme.append(clipSurface)

        arcpy.AddMessage("Building viewshed of observers to surface...")
        tempViewshed = os.path.join(scratch, "tempViewshed")
        tempAGL = os.path.join(scratch, "tempAGL")
        saViewshed = sa.Viewshed(clipSurface,
                                 observersSurfaceSR,
                                 1.0,
                                 "CURVED_EARTH",
                                 0.13,
                                 tempAGL)
        saViewshed.save(tempViewshed)
        deleteme.append(tempViewshed)
        deleteme.append(tempAGL)

        arcpy.AddMessage("Converting viewshed to polygon features...")
        viewshedPolys = os.path.join(scratch, "viewshedPolys")
        rasterValueField = "Value"
        conversionField = "Gridcode"
        simplifyShape = "SIMPLIFY"
        arcpy.RasterToPolygon_conversion(tempViewshed,
                                         viewshedPolys,
                                         simplifyShape,
                                         rasterValueField)
        deleteme.append(viewshedPolys)

        arcpy.AddMessage("Clipping polygons to max buffer...")
        clippedPolys = os.path.join(scratch, "clippedPolys")
        arcpy.Intersect_analysis([viewshedPolys, bufferSurfaceSR], clippedPolys, "NO_FID")
        deleteme.append(clippedPolys)

        arcpy.AddMessage("Projecting to output spatial reference...")
        arcpy.Project_management(clippedPolys, outputVisibility, inputSpatialReference)
        arcpy.AddField_management(outputVisibility,
                                  "VISIBILITY",
                                  "LONG")
        arcpy.CalculateField_management(outputVisibility,
                                        "VISIBILITY",
                                        '!{0}!'.format(conversionField),
                                        "PYTHON_9.3")
        dropFields = [conversionField, 'Id']
        arcpy.DeleteField_management(outputVisibility, dropFields)

        return outputVisibility
    
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