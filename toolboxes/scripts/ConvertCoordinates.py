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
 * ArcGIS Desktop 10.X+ or ArcGIS Pro 1.X+
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
========================================================================
'''

#Imports
import sys, os, traceback
import arcpy
from arcpy import env

deleteIntermediateDatasets = []
joinFieldName = "JoinID"
scratchTable = None
Output_Table = None
DEBUG = True

def addUniqueID(dataset, fieldName):
    ''' adding unique ID field '''
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

def addNotation(notationType, fieldsToAdd):
    ''' '''
    arcpy.AddMessage("Converting & appending %s ..." % notationType)
    arcpy.ConvertCoordinateNotation_management(Output_Table,
                                               scratchTable,
                                               X_Field__Longitude__UTM__MGRS__USNG__GARS__GeoRef_,
                                               Y_Field__Latitude_,
                                               Input_Coordinate_Format,
                                               notationType,
                                               joinFieldName,
                                               Spatial_Reference)
    arcpy.JoinField_management(Output_Table, joinFieldName,
                               scratchTable, joinFieldName,
                               fieldsToAdd)
    return True

try:
    
    # Script arguments
    Input_Table = arcpy.GetParameterAsText(0)

    Input_Coordinate_Format = arcpy.GetParameterAsText(1)
    if not Input_Coordinate_Format:
        Input_Coordinate_Format = "DD" # provide a default value if unspecified

    X_Field__Longitude__UTM__MGRS__USNG__GARS__GeoRef_ = arcpy.GetParameterAsText(2)
    if not X_Field__Longitude__UTM__MGRS__USNG__GARS__GeoRef_:
        X_Field__Longitude__UTM__MGRS__USNG__GARS__GeoRef_ = "Lond" # provide a default value if unspecified

    Y_Field__Latitude_ = arcpy.GetParameterAsText(3)
    if not Y_Field__Latitude_:
        Y_Field__Latitude_ = "Latd" # provide a default value if unspecified

    Output_Table = arcpy.GetParameterAsText(4)
    if not Output_Table:
        pass

    Spatial_Reference = arcpy.GetParameterAsText(5)
    if not Spatial_Reference:
        Spatial_Reference = arcpy.SpatialReference(4326) #GCS_WGS_1984

    currentOverwriteOutput = env.overwriteOutput
    env.overwriteOutput = True

    scratchWS = env.scratchGDB
    if not scratchWS:
        scratchWS = r'in_memory'

    scratchTable = os.path.join(scratchWS,"cc_temp")
    deleteIntermediateDatasets.append(scratchTable)

    if DEBUG:
        arcpy.AddMessage("Copying %s to %s" % (Input_Table, Output_Table))
    arcpy.CopyRows_management(Input_Table, Output_Table)
    
    Output_Table = addUniqueID(Output_Table, "JoinID")

    # {"format":"field_name(s)", ...}
    notationsToAdd = {"GARS":"GARS",
                      "DD":"DDLat; DDLon",
                      "DDM":"DDMLat; DDMLon",
                      "DMS":"DMS",
                      "UTM":"UTM",
                      "MGRS":"MGRS",
                      "UTM":"UTM",
                      "GEOREF":"GEOREF"}

    for notationFormat in notationsToAdd:
        if not addNotation(notationFormat, notationsToAdd[notationFormat]):
            raise

    # cleanup
    arcpy.AddMessage("Removing scratch datasets...")
    for ds in deleteIntermediateDatasets:
        #arcpy.AddMessage(str(ds))
        arcpy.Delete_management(ds)

    arcpy.SetParameter(4, Output_Table)
    env.overwriteOutput = currentOverwriteOutput

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
