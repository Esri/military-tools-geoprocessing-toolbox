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
 TableToPolyline.py
 --------------------------------------------------
 requirements: ArcGIS 10.3+, Python 2.7 or Python 3.4
 author: ArcGIS Solutions
 contact: support@esri.com
 company: Esri
 ==================================================
 description:
 Converts a table of vertices to one or more polyline features.
 ==================================================
 history:
 11/22/2016 - mf - Original conversion from Model to script tool
 ==================================================
'''

# IMPORTS ==========================================
import os
import sys
import traceback
import arcpy
from arcpy import env
import ConversionUtilities

inputTable = arcpy.GetParameterAsText(0) # Input Table
inputCoordinateFormat = arcpy.GetParameterAsText(1) # Input Coordinate Format - from ValueList
inputXField = arcpy.GetParameterAsText(2) # X Field (Longitude, UTM, MGRS, USNG, GARS, GeoRef) - from inputTable
inputYField = arcpy.GetParameterAsText(3) # Y Field (Latitude)
outputPolylineFeatures = arcpy.GetParameterAsText(4) # Output Polygon Features
inputLineField = arcpy.GetParameterAsText(5) # Line Field (optional) - from inputTable
inputSortField = arcpy.GetParameterAsText(6) # Sort Field (optional) - from inputTable
inputSpatialReference = arcpy.GetParameterAsText(7) # Spatial Reference (optional)
if not inputSpatialReference or inputSpatialReference == "" or inputSpatialReference == "#":
    inputSpatialReference = arcpy.SpatialReference(4326) #default is GCS_WGS_1984

# LOCALS ===========================================
deleteme = [] # intermediate datasets to be deleted
debug = True # extra messaging during development

# FUNCTIONS ========================================

def main():
    try:
        # get/set environment
        env.overwriteOutput = True
        ConversionUtilities.tableToPolyline(inputTable,
                                            inputCoordinateFormat,
                                            inputXField,
                                            inputYField,
                                            outputPolylineFeatures,
                                            inputLineField,
                                            inputSortField,
                                            inputSpatialReference)

        # Set output
        arcpy.SetParameter(4, outputPolylineFeatures)


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



# MAIN =============================================
if __name__ == "__main__":
    main()