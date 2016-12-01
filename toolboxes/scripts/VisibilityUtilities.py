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
 ==================================================
'''

# IMPORTS ==========================================
import os
import sys
import traceback
import arcpy
from arcpy import env

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
scratch = None
# FUNCTIONS ========================================
def _getFieldNameList(targetTable):
    '''
    Returns a list of field names from targetTable
    '''
    nameList = []
    try:
        if not targetTable:
            raise Exception("Source table {0} does not exist or is null.".format(targetTable))
        fields = arcpy.ListFields(targetTable)
        for field in fields:
            nameList.append(field.name)
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
        existingFields = _getFieldNameList(targetTable)
        for currentField in list(fieldsToAdd.keys()):
            if currentField in existingFields:
                arcpy.AddWarning("Field {0} is already in {1}. Skipping this field name.".format(currentField, targetTable))
            else:
                fName = currentField
                #fDefault = float(fieldsToAdd[currentField][0])
                fAlias = fieldsToAdd[currentField][1]
                if debug: arcpy.AddMessage("Adding field [{0}] with alias [{1}]".format(fName,fAlias))
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
        existingFields = _getFieldNameList(targetTable)
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
        existingFields = _getFieldNameList(targetTable)
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

#TODO: _isValidLLOS()
#TODO: _getImageFileName()
#TODO: _MakePofileGraph()
#TODO: _enableAttachments()

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
        outputObserverTable = _calculateFieldValue(outputObserverTable,
                                                   "OFFSET",
                                                   float(inputObserverDefault))
        #Add field to Target table
        arcpy.AddMessage("Adding Target fields...")
        outputTargetTable = _addDoubleField(inputTargetTable,
                                            llosFields)
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
        invertedSinks = os.path.join(scratch, "invertedSinks")
        saSink.save(invertedSinks)
        deleteme.append(invertedSinks)
        
        #raster to point (Grid_code)
        pointSinks = os.path.join(scratch, "pointSinks")
        arcpy.RasterToPoint_conversion(invertedSinks, pointSinks)
        deleteme.append(pointSinks)
        
        #extract values to points
        arcpy.AddMessage("Extracting elevation values from {0}...".format(inputSurfaceRaster))
        sinkValues = os.path.join(scratch, "sinkValues")
        sa.ExtractValuesToPoints(pointSinks, inputSurfaceRaster, sinkValues, "NONE", "VALUE_ONLY")
        deleteme.append(sinkValues)
        
        # select X highest values.
        valueField = "RASTERVALU"
        uniqueElevationList = _getUniqueValuesFromField(sinkValues, valueField)
        cutoffValue = uniqueElevationList[int(inputNumberOfPeaks) - 1]
        arcpy.AddMessage("Using cutoff value of {0} to find {1} highest peak elevations...".format(cutoffValue, inputNumberOfPeaks))
        arcpy.MakeFeatureLayer_management(sinkValues, "sortedPoints")
        selectExpression = r'{0} >= {1}'.format(valueField, cutoffValue)
        arcpy.SelectLayerByAttribute_management("sortedPoints",
                                                "NEW_SELECTION",
                                                selectExpression)
        arcpy.CopyFeatures_management("sortedPoints", outputPeakFeatures)
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

def linearLineOfSight():
    '''
    '''
    global scratch
    try:
        #Need Spatial Analyst to run this tool
        if arcpy.CheckExtension("Spatial") == "Available":
            arcpy.CheckOutExtension("Spatial")
        else:
            raise Exception("Spatial Analyst license is not available.")
        from arcpy import sa
        
        if arcpy.env.scratchWorkspace:
            scratch = arcpy.env.scratchWorkspace
        else:
            scratch = r"%scratchGDB%"


        return
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
            
def radialLineOfSight():
    '''
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


        return
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