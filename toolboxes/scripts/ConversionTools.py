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

    coordinateFormats = [u'DD_1', u'DD_2', u'DDM_1', u'DDM_2', u'DMS_1', u'DMS_2', u'GARS', u'GEOREF', u'UTM_BANDS', u'UTM_ZONES', u'USNG', u'MGRS']

    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""
      
        singleFieldTypes = ["DD_1", "DDM_1", "DMS_1", "GARS", "GEOREF", "UTM_BANDS", "UTM_ZONES", "USNG", "MGRS"]
    
        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters
    
        def initializeParameters(self):
            """Refine the properties of a tool's parameters.  This method is
            called when the tool is opened."""
            #0 - Input Table
            #1 - Input Coordinate Format
            #2 - X Field
            #3 - Y Field
            #4 - Output Table
            #5 - Spatial Reference
        
            return
    
        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""
            #0 - Input Table
            #1 - Input Coordinate Format
            if self.params[1].altered:
                if self.params[1].value in self.singleFieldTypes:
                    self.params[3].value = self.params[2].value
                    self.params[3].enabled = False
                else:
                    self.params[3].enabled = True
            #2 - X Field
            #3 - Y Field
            #4 - Output Table
            #5 - Spatial Reference
            return
    
        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            #0 - Input Table
            #1 - Input Coordinate Format
            #2 - X Field
            #3 - Y Field
            if not self.params[1].value in self.singleFieldTypes:
                if self.params[3].value == None or self.params[3].value == "":
                    self.params[3].setErrorMessage("Coordinate formats 'DD_2', 'DDM_2', and 'DMS_2' require both X Field and Y Field from the input table.")
            #4 - Output Table
            #5 - Spatial Reference
            return

    def __init__(self):
        self.label = u'Table to Polygon'
        self.description = u'Converts an input table of vertex points to one or more polygon features.'
        self.category = u'Conversion'
        self.canRunInBackground = False
        
    def getParameterInfo(self):

        # Input_Table
        param_0 = arcpy.Parameter()
        param_0.name = u'Input_Table'
        param_0.displayName = u'Input Table'
        param_0.parameterType = 'Required'
        param_0.direction = 'Input'
        param_0.datatype = u'Table View'
        
        # Input_Coordinate_Format
        param_1 = arcpy.Parameter()
        param_1.name = u'Input_Coordinate_Format'
        param_1.displayName = u'Input Coordinate Format'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'String'
        param_1.value = u'DD_2'
        param_1.filter.list = self.coordinateFormats

        # X_Field__Longitude__UTM__MGRS__USNG__GARS__GeoRef_
        param_2 = arcpy.Parameter()
        param_2.name = u'X_Field_Longitude_UTM_MGRS_USNG_GARS_GeoRef_'
        param_2.displayName = u'X Field (Longitude, UTM, MGRS, USNG, GARS, GeoRef)'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Field'
        param_2.parameterDependencies = ["Input_Table"]
        
        # Y_Field__Latitude_
        param_3 = arcpy.Parameter()
        param_3.name = u'Y_Field__latitude_'
        param_3.displayName = u'Y Field (Latitude)'
        param_3.parameterType = 'Optional'
        param_3.direction = 'Input'
        param_3.datatype = u'Field'
        param_3.parameterDependencies = ["Input_Table"]
        
        # Output_Polygon_Features
        param_4 = arcpy.Parameter()
        param_4.name = u'Output_Polygon_Features'
        param_4.displayName = u'Output Polygon Features'
        param_4.parameterType = 'Required'
        param_4.direction = 'Output'
        param_4.datatype = u'Feature Class'
        param_4.value = u'%scratchGDB%/outputPolygons'
     
        # Line_Field
        param_5 = arcpy.Parameter()
        param_5.name = u'Line_Field'
        param_5.displayName = u'Line Field'
        param_5.parameterType = 'Optional'
        param_5.direction = 'Input'
        param_5.datatype = u'Field'
        param_5.parameterDependencies = ["Input_Table"]
                
        # Sort_Field
        param_6 = arcpy.Parameter()
        param_6.name = u'Sort_Field'
        param_6.displayName = u'Sort Field'
        param_6.parameterType = 'Optional'
        param_6.direction = 'Input' 
        param_6.datatype = u'Field'
        param_6.parameterDependencies = ["Input_Table"]
                
        # Spatial_Reference
        param_7 = arcpy.Parameter()
        param_7.name = u'Spatial_Reference'
        param_7.displayName = u'Spatial Reference'
        param_7.parameterType = 'Optional'
        param_7.direction = 'Input'
        param_7.datatype = u'Spatial Reference'
        param_7.value = arcpy.SpatialReference(4326).exportToString()
               
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
                
        inputTable = parameters[0].valueAsText
        inputCoordinateFormat = parameters[1].valueAsText
        inputXField = parameters[2].valueAsText
        inputYField = parameters[3].valueAsText 
        outputPolygonFeatures = parameters[4].valueAsText
        inputLineField = parameters[5].valueAsText
        inputSortField = parameters[6].valueAsText
        inputSpatialReference = parameters[7].value
        inputSpatialReferenceAsText = parameters[7].valueAsText
            
        if not inputSpatialReference or inputSpatialReferenceAsText == "" or inputSpatialReferenceAsText == "#":
            inputSpatialReference = arcpy.SpatialReference(4326) #default is GCS_WGS_1984
            
        #get/set environment
        arcpy.env.overwriteOutput = True
        
        #call tool method
        outputPolygonFeaturesOut = ConversionUtilities.tableToPolygon(inputTable,
                                                         inputCoordinateFormat,
                                                         inputXField,
                                                         inputYField,
                                                         outputPolygonFeatures,
                                                         inputLineField,
                                                         inputSortField,
                                                         inputSpatialReference)
        #set output
        return outputPolygonFeaturesOut



