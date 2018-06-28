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
 AddRLOSObserverFields.py
 --------------------------------------------------
 requirements: ArcGIS 10.3+, Python 2.7 or Python 3.4
 author: ArcGIS Solutions
 contact: support@esri.com
 company: Esri
 ==================================================
 description:
 Adds Observer fields and values to inputFeatures:
 OFFSETA: observer offset height above surface, default is 2.0
 OFFSETB: surface offset, default is 0.0
 RADIUS1: Near distance, default is 0.0
 RADIUS2: Farthest distance, default is 1000.0
 AZIMUTH1: Left Azimuth in horizontal field of view, default is 0.0
 AZIMUTH2: Right Azimuth in horizontal field of view, default is 360.0
 VERT1: Top Angle in vertical field of view, default is 90.0
 VERT2: Bottom Angle in vertical field of view, default is -90.0
 ==================================================
 history:
 11/29/2016 - mf - Convert model to script
 ==================================================
'''

# IMPORTS ==========================================
import os
import sys
import traceback
import arcpy
from arcpy import env
from . import VisibilityUtilities

# LOCALS ===========================================
deleteme = [] # intermediate datasets to be deleted
debug = True # extra messaging during development

# FUNCTIONS ========================================
inputObserverFeatures = arcpy.GetParameterAsText(0) # Input Observer Features
inputOFFSETA = arcpy.GetParameterAsText(1) # Observer Offset
inputOFFSETB = arcpy.GetParameterAsText(2) # Surface Offset
inputRADIUS1 = arcpy.GetParameterAsText(3) # Minimum Distance Radius
inputRADIUS2 = arcpy.GetParameterAsText(4) # Maximum Distance Radius
inputAZIMUTH1 = arcpy.GetParameterAsText(5) # Left Bearing Azimuth
inputAZIMUTH2 = arcpy.GetParameterAsText(6) # Right Bearing Azimuth
inputVERT1 = arcpy.GetParameterAsText(7) # Top Vertical Angle
inputVERT2 = arcpy.GetParameterAsText(8) # Bottom Vertical Angle

def main():
    try:
        # get/set environment
        env.overwriteOutput = True

        outputObserverFeatures = VisibilityUtilities.addRLOSObserverFields(inputObserverFeatures,
                                                                           inputOFFSETA,
                                                                           inputOFFSETB,
                                                                           inputRADIUS1,
                                                                           inputRADIUS2,
                                                                           inputAZIMUTH1,
                                                                           inputAZIMUTH2,
                                                                           inputVERT1,
                                                                           inputVERT2)

        # Set output
        arcpy.SetParameter(9, outputObserverFeatures)


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