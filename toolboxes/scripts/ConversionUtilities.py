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
'''

import os
import sys
import arcpy
from arcpy import env
import traceback

debug = True

    
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
        if debug: arcpy.AddMessage("inFields: " + str(inFields))
        inRows = arcpy.da.SearchCursor(inputPolylines, inFields)
    
        #Open Insert cursor on polygons
        outRows = arcpy.da.InsertCursor(outpolygonsFC,inFields)
    
        for row in inRows:
            feat = row[0]
            if inputIDFieldName:
                inID = row[1]
    
            arcpy.AddMessage("Building points from lines.")
            #Build array of points for the line
            polyArray = arcpy.Array()
            partnum = 0
            for part in feat:
                for pnt in feat.getPart(partnum):
                    polyArray.add(arcpy.Point(pnt.X, pnt.Y))
                partnum += 1
    
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

''' TOOL METHODS '''
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
    '''
    try:
        
        scratch = 'in_memory'
        if env.scratchWorkspace:
            scratch = env.scratchWorkspace  
        
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