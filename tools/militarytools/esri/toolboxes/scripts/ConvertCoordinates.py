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
 ConvertCoordinates.py
------------------------------------------------------------------------------
 requirements:
 * ArcGIS Desktop 10.3+ or ArcGIS Pro 1.2+
 * Python 2.7 or Python 3.4
 author: ArcGIS Solutions
 company: Esri
========================================================================
 description:
 Converts coordinates in input table from one format to multipe output formats

========================================================================
 history:
 2014 - ? - initial creation
 6/9/2016 - mf - refactor ID count and internal methods
 11/18/2016 - mf - refactor as stand-alone GP script tool
========================================================================
'''

import sys, os, traceback
import arcpy
from arcpy import env

deleteIntermediateDatasets = []
DEBUG = False

def addUniqueID(dataset, fieldName):
    ''' adding unique ID field '''
    try:
        counter = 1
        arcpy.AddMessage("Adding field: " + str(fieldName))
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
        return dataset
    except arcpy.ExecuteError:
        error = True
        # Get the tool error messages
        msgs = arcpy.GetMessages()
        arcpy.AddError(msgs)
        #print msgs #UPDATE
        print(msgs)

def addNotation(notationType, fieldsToAdd, joinFieldName, outputTable, scratchTable,
                inputXField, inputYField, inputCoordinateFormat, inputSpatialReference):
    ''' '''
    try:
        arcpy.AddMessage("Converting & appending {0} with fields {1} ...".format(notationType, fieldsToAdd))
        arcpy.ConvertCoordinateNotation_management(outputTable,
                                                   scratchTable,
                                                   inputXField,
                                                   inputYField,
                                                   inputCoordinateFormat,
                                                   notationType,
                                                   joinFieldName,
                                                   inputSpatialReference)
        arcpy.JoinField_management(outputTable, joinFieldName,
                                   scratchTable, joinFieldName,
                                   fieldsToAdd)
            
        return True
    except arcpy.ExecuteError:
        error = True
        # Get the tool error messages
        msgs = arcpy.GetMessages()
        arcpy.AddError(msgs)
        #print msgs #UPDATE
        print(msgs)

def convertCoordinates(inputTable,
                       inputCoordinateFormat,
                       inputXField,
                       inputYField,
                       outputTable,
                       inputSpatialReference):
    '''
    inputTable - input table, each row will be a separate line feature in output
    inputCoordinateFormat - coordinate notation format of input vertices
    inputXField - field in inputTable for vertex x-coordinate, or full coordinate
    inputYField - field in inputTable for vertex y-coordinate, or None
    outputTable -  output table containing converted coordinate notations
    inputSpatialReference - spatial reference of input coordinates
    
    returns table
    
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
        currentOverwriteOutput = env.overwriteOutput
        env.overwriteOutput = True
        joinFieldName = "JoinID"
    
        scratchWS = env.scratchGDB
        if not scratchWS:
            scratchWS = r'in_memory'
    
        scratchTable = os.path.join(scratchWS,"cc_temp")
        deleteIntermediateDatasets.append(scratchTable)
    
        if DEBUG:
            arcpy.AddMessage("Copying %s to %s" % (inputTable, outputTable))
        arcpy.CopyRows_management(inputTable, outputTable)
        
        outputTable = addUniqueID(outputTable, joinFieldName)
    
        # {"format":"field_name(s)", ...}
        notationsToAdd = {"DD":"DDLat; DDLon",
                          "DDM":"DDMLat; DDMLon",
                          "DMS":"DMSLat; DMSLon",
                          "UTM_BANDS":"UTM_BANDS",
                          "MGRS":"MGRS",
                          "USNG":"USNG",
                          "GARS":"GARS",
                          "GEOREF":"GEOREF"}
    
        for notationFormat in notationsToAdd:
            if not addNotation(notationFormat, notationsToAdd[notationFormat],
                               joinFieldName, outputTable, scratchTable, 
                               inputXField, inputYField, inputCoordinateFormat, inputSpatialReference):
                raise Exception("Failed to convert notation {0}.".format(notationFormat))
    
        # cleanup
        arcpy.AddMessage("Removing scratch datasets...")
        for ds in deleteIntermediateDatasets:
            if arcpy.Exists(ds):
                arcpy.Delete_management(ds)
            
        return outputTable
        
    
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
        

# MAIN =============================================
if __name__ == "__main__":

    # Script arguments
    inputTable = arcpy.GetParameterAsText(0)
    inputCoordinateFormat = arcpy.GetParameterAsText(1)
    inputXField = arcpy.GetParameterAsText(2)
    inputYField = arcpy.GetParameterAsText(3)
    outputTable = arcpy.GetParameterAsText(4)
    inputSpatialReference = arcpy.GetParameterAsText(5)
    if not inputSpatialReference:
        inputSpatialReference = arcpy.SpatialReference(4326) #GCS_WGS_1984

    output = convertCoordinates(inputTable,
                       inputCoordinateFormat,
                       inputXField,
                       inputYField,
                       outputTable,
                       inputSpatialReference)
    arcpy.SetParameter(4, output)
    