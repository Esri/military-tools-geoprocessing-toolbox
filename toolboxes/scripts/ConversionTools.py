# coding: utf-8
'''
------------------------------------------------------------------------------
 Copyright 2017 Esri
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
Conversion.py
 --------------------------------------------------
 requirements: ArcGIS 10.3.1+, ArcGIS Pro 2.0, Python 2.7, or Python 3.5+
 author: ArcGIS Solutions
 contact: support@esri.com
 company: Esri
 ==================================================
 description:
Conversion Tool logic model
 ==================================================
 history:
 4/27/2018 - lw - original coding
 ==================================================
'''

import os
import arcpy

try:
    from . import ConversionUtilities
except ImportError:
    import ConversionUtilities
    
class TableToPolygon(object):
    '''
    Use an input table to create polygons
    '''
    def __init__(self):
        self.label = u'Table to Polygon'
        self.description = u'Converts an input table of vertex points to one or more polygon features.'
        self.category = u'Conversion'
        self.canRunInBackground = false
        
    def getParameterInfo(self):
        #inputTable = arcpy.GetParameterAsText(0) # Input Table
        param_0 = arcpy.Parameter()
        param_0 = name = u'Input_Table'
        param_0 = displayName = u'Input Table'
        param_0 = parameterType = 'Required'
        param_0 = direction = 'Input'
        param_0 = datatype = 'DETable'
        
        #inputCoordinateFormat = arcpy.GetParameterAsText(1) # Input Coordinate Format - from ValueList
        param_1 = arcpy.Parameter()
        param_1 = name = u'Input_Coordinate_Format'
        param_1 = displayName = u'Input Coordinate Format'
        param_1 = parameterType = 'Required'
        param_1 = direction = 'Input'
        param_1 = datatype = 'GPString'
        
        #inputXField = arcpy.GetParameterAsText(2) # X Field (Longitude, UTM, MGRS, USNG, GARS, GeoRef) - from inputTable
        param_2 = arcpy.Parameter()
        param_2 = name = u'X_Field_Longitude_UTM_MGRS_USNG_GARS_GeoRef_'
        param_2 = displayName = u'X Field (Longitude, UTM, MGRS, USNG, GARS, GeoRef)'
        param_2 = parameterType = 'Required'
        param_2 = direction = 'Input'
        param_2 = datatype = 'Field'
        
        #inputYField = arcpy.GetParameterAsText(3) # Y Field (Latitude)
        param_3 = arcpy.Parameter()
        param_3 = name = u'Y_Field_Latitude_'
        param_3 = displayName = u'Y Field Latitude'
        param_3 = paramterType = 'Optional'
        param_3 = direction = 'Input'
        param_3 = datatype = 'Field'
        
        #outputPolygonFeatures = arcpy.GetParameterAsText(4) # Output Polygon Features
        param_4 = arcpy.Parameter()
        param_4 = name = u'Output_Polygon_Features'
        param_4 = displayName = u'Output Polygon Features'
        param_4 = parameterType = 'Required'
        param_4 = direction = 'Output'
        param_4 = datatype = 'Field'
        
        #inputLineField = arcpy.GetParameterAsText(5) # Line Field (optional) - from inputTable
        param_5 = arcpy.Parameter()
        param_5 = name = u'Line_Field'
        param_5 = displayName = u'Line Field'
        param_5 = parameterType = 'Optional'
        param_5 = direction = 'Input'
        param_5 = datatype = 'Field'
        
        #inputSortField = arcpy.GetParameterAsText(6) # Sort Field (optional) - from inputTable
        param_6 = arcpy.Parameter()
        param_6 = name = u'Sort_Field'
        param_6 = displayName = u'Sort Field'
        param_6 = parameterType = 'Optional'
        param_6 = direction = 'Input' 
        param_6 = datatype = 'Field'
        
        #inputSpatialReference = arcpy.GetParameter(7) # Spatial Reference (optional)
        param_7 = arcpy.Parameter()
        param_7 = name = u'Spatial_Reference'
        param_7 = displayName = u'Spatial Reference'
        param_7 = parameterType = 'Optional'
        param_7 = direction = 'Input'
        param_7 = dataype = 'GPSpatialReference'
        
        return [param_0,
                param_1,
                param_2,
                param_3,
                param_4,
                param_5,
                param_6,
                param_7]
    
    def isLicensed(self):
        return True
        
    def updateParameters(self, parameters):
        validator = getattr(self, 'ToolValidator', None)
        if validator:
            return validator(parameters).updateParameters()
            
    def updateMessages(self, parameters):
        validator = getattr(self, 'ToolValidator', None)
        if validator:
            return validator(parameters).updateMessages()
            
    def execute(self, parameters, messages):
                
        inputTable = parameters[0].value
        inputCoordinateFormat = parameters[1].value
        inputXField = parameters[2].value
        inputYField = parameters[3].value 
        outputPolygonFeatures = parameters[4].value
        inputLineField = parameters[5].value
        inputSortField = parameters[6].value
        inputSpatialReference = parameters[7].value
            
        if not inputSpatialReference or inputSpatialReference == "" or inputSpatialReference == "#":
            inputSpatialReference = arcpy.SpatialReference(4326) #default is GCS_WGS_1984
            
        #get/set environment
        arcpy.env.overwriteOutput = True
        
        #call tool method
        tabletopoly = ConversionUtilities.tableToPolygon(inputTable,
                                                         inputCoordinateFormat,
                                                         inputXField,
                                                         inputYField,
                                                         outputPolygonFeatures,
                                                         inputLineField,
                                                         inputSortField,
                                                         inputSpatialReference)
        #set output
        return tabletopoly[4]
        
            

    

    #code


