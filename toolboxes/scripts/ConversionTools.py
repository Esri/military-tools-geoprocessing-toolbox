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
'''

import os
import arcpy

try:
    from . import ConversionUtilities
except ImportError:
    import ConversionUtilities

# String constants shared by tools:
defaultcoordinateFormat = u'DD_2'
coordinateFormats = [u'DD_1', u'DD_2', u'DDM_1', u'DDM_2', u'DMS_1', u'DMS_2', u'GARS', u'GEOREF', u'UTM_BANDS', u'UTM_ZONES', u'USNG', u'MGRS']
singleFieldTypes = ["DD_1", "DDM_1", "DMS_1", "GARS", "GEOREF", "UTM_BANDS", "UTM_ZONES", "USNG", "MGRS"]
defaultLineType = "GEODESIC"
lineTypes = ["GEODESIC", "GREAT_CIRCLE", "RHUMB_LINE", "NORMAL_SECTION"]
defaultAngleType = "DEGREES"
angleTypes = ["DEGREES", "MILS", "RADS", "GRADS"]
defaultDistanceType = "METERS"
distanceTypes = ["METERS", "KILOMETERS", "MILES", "NAUTICAL_MILES", "FEET", "US_SURVEY_FEET"]

# Other shared objects
srWGS84 = arcpy.SpatialReference(4326)  # GCS_WGS_1984
coordinate2ErrorMsg = "Coordinate formats 'DD_2', 'DDM_2', and 'DMS_2' require both X Field and Y Field from the input table."

# -----------------------------------------------------------------------------
# ConvertCoordinates Tool
# -----------------------------------------------------------------------------
class ConvertCoordinates(object):

    class ToolValidator(object):
    
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
            if self.params[1].value in singleFieldTypes:
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
            if not self.params[1].value in singleFieldTypes:
                if self.params[3].value == None or self.params[3].value == "":
                    self.params[3].setErrorMessage(coordinate2ErrorMsg)
            #2 - X Field
            #3 - Y Field
            #4 - Output Table
            #5 - Spatial Reference             
            return

        # END ToolValidator

    def __init__(self):
        self.label = u'Convert Coordinates'
        self.description = u'Converts source coordinates in a table to multiple coordinate formats.  This tool uses an input table with coordinates and outputs a new table with fields for the following coordinate formats: Decimal Degrees, Decimal Degrees Minutes, Degrees Minutes Seconds, Universal Transverse Mercator, Military Grid Reference System, U.S. National Grid, Global Area Reference System, and World Geographic Reference System'
        self.category = u'Conversion'
        self.canRunInBackground = False

    def getParameterInfo(self):
        # Input_Table
        param_1 = arcpy.Parameter()
        param_1.name = u'Input_Table'
        param_1.displayName = u'Input Table'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Table View'

        # Input_Coordinate_Format
        param_2 = arcpy.Parameter()
        param_2.name = u'Input_Coordinate_Format'
        param_2.displayName = u'Input Coordinate Format'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'String'
        param_2.value = defaultcoordinateFormat
        param_2.filter.list = coordinateFormats

        # X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_
        param_3 = arcpy.Parameter()
        param_3.name = u'X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_'
        param_3.displayName = u'X Field (longitude, UTM, MGRS, USNG, GARS, GEOREF)'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Field'
        param_3.parameterDependencies = ["Input_Table"]

        # Y_Field__latitude_
        param_4 = arcpy.Parameter()
        param_4.name = u'Y_Field__latitude_'
        param_4.displayName = u'Y Field (latitude)'
        param_4.parameterType = 'Optional'
        param_4.direction = 'Input'
        param_4.datatype = u'Field'
        param_4.parameterDependencies = ["Input_Table"]

        # Output_Table
        param_5 = arcpy.Parameter()
        param_5.name = u'Output_Table'
        param_5.displayName = u'Output Table'
        param_5.parameterType = 'Required'
        param_5.direction = 'Output'
        param_5.datatype = u'Table'
        param_5.value = u'%scratchGDB%/convertCoords'

        # Spatial_Reference
        param_6 = arcpy.Parameter()
        param_6.name = u'Spatial_Reference'
        param_6.displayName = u'Spatial Reference'
        param_6.parameterType = 'Optional'
        param_6.direction = 'Input'
        param_6.datatype = u'Spatial Reference'
        param_6.value = srWGS84.exportToString()

        return [param_1, param_2, param_3, param_4, param_5, param_6]

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

        try:
            from . import ConvertCoordinates
        except ImportError:
            import ConvertCoordinates

        inputTable = parameters[0].valueAsText
        inputCoordinateFormat = parameters[1].valueAsText
        inputXField = parameters[2].valueAsText
        inputYField = parameters[3].valueAsText
        outputTable = parameters[4].valueAsText
        optionalSpatialReference = parameters[5].value
        optionalSpatialReferenceAsText = parameters[5].valueAsText

        if optionalSpatialReferenceAsText == "#" or optionalSpatialReferenceAsText == "":
            optionalSpatialReference = srWGS84 #GCS_WGS_1984

        output = ConvertCoordinates.convertCoordinates(inputTable,
                           inputCoordinateFormat,
                           inputXField,
                           inputYField,
                           outputTable,
                           optionalSpatialReference)

        return output

    # END ConvertCoordinates

# -----------------------------------------------------------------------------
# TableTo2PointLine Tool
# -----------------------------------------------------------------------------
class TableTo2PointLine(object):

    class ToolValidator(object):
    
        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters
    
        def initializeParameters(self):
            """Refine the properties of a tool's parameters.  This method is
            called when the tool is opened."""
            #0 - Input Table
            #1 - Start Point Format
            #2 - Start X Field
            #3 - Start Y Field
            #4 - End Point Format
            #5 - End X Field
            #6 - End Y Field
            #7 - Output Lines
            #8 - Line Type
            #9 - Spatial Reference            
            return
    
        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""
            #0 - Input Table
            #1 - Start Point Format
            if self.params[1].altered:
                if self.params[1].value in singleFieldTypes:
                    self.params[3].value = self.params[2].value
                    self.params[3].enabled = False
                else:
                    self.params[3].enabled = True
            #2 - Start X Field
            #3 - Start Y Field
            #4 - End Point Format
            if self.params[4].altered:
                if self.params[4].value in singleFieldTypes:
                    self.params[6].value = self.params[5].value
                    self.params[6].enabled = False
                else:
                    self.params[6].enabled = True
            #5 - End X Field
            #6 - End Y Field
            #7 - Output Lines
            #8 - Line Type
            #9 - Spatial Reference                   return
    
        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            #0 - Input Table
            #1 - Start Point Format
            #2 - Start X Field
            #3 - Start Y Field
            if not self.params[1].value in singleFieldTypes:
                if self.params[3].value == None or self.params[3].value == "":
                    self.params[3].setErrorMessage(coordinate2ErrorMsg)
            #4 - End Point Format
            #5 - End X Field
            #6 - End Y Field
            if not self.params[4].value in singleFieldTypes:
                if self.params[6].value == None or self.params[6].value == "":
                    self.params[6].setErrorMessage(coordinate2ErrorMsg)
            #7 - Output Lines
            #8 - Line Type
            #9 - Spatial Reference            
            return
            
        # END ToolValidator

    def __init__(self):
        self.label = u'Table To 2-Point Line'
        self.description = u'Creates a line feature from start and end point coordinates.  This tool uses an input table with coordinate pairs and outputs line features.   '
        self.category = u'Conversion'
        self.canRunInBackground = False

    def getParameterInfo(self):
        # Input_Table
        param_1 = arcpy.Parameter()
        param_1.name = u'Input_Table'
        param_1.displayName = u'Input Table'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Table View'

        # Start_Point_Format
        param_2 = arcpy.Parameter()
        param_2.name = u'Start_Point_Format'
        param_2.displayName = u'Start Point Format'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'String'
        param_2.value = defaultcoordinateFormat
        param_2.filter.list = coordinateFormats

        # Start_X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_
        param_3 = arcpy.Parameter()
        param_3.name = u'Start_X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_'
        param_3.displayName = u'Start X Field (longitude, UTM, MGRS, USNG, GARS, GEOREF)'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Field'
        param_3.parameterDependencies = ["Input_Table"]

        # Start_Y_Field__latitude_
        param_4 = arcpy.Parameter()
        param_4.name = u'Start_Y_Field__latitude_'
        param_4.displayName = u'Start Y Field (latitude)'
        param_4.parameterType = 'Optional'
        param_4.direction = 'Input'
        param_4.datatype = u'Field'
        param_4.parameterDependencies = ["Input_Table"]

        # End_Point_Format
        param_5 = arcpy.Parameter()
        param_5.name = u'End_Point_Format'
        param_5.displayName = u'End Point Format'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'String'
        param_5.value = defaultcoordinateFormat
        param_5.filter.list = coordinateFormats

        # End_X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_
        param_6 = arcpy.Parameter()
        param_6.name = u'End_X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_'
        param_6.displayName = u'End X Field (longitude, UTM, MGRS, USNG, GARS, GEOREF)'
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = u'Field'
        param_6.parameterDependencies = ["Input_Table"]

        # End_Y_Field__latitude_
        param_7 = arcpy.Parameter()
        param_7.name = u'End_Y_Field__latitude_'
        param_7.displayName = u'End Y Field (latitude)'
        param_7.parameterType = 'Optional'
        param_7.direction = 'Input'
        param_7.datatype = u'Field'
        param_7.parameterDependencies = ["Input_Table"]

        # Output_Lines
        param_8 = arcpy.Parameter()
        param_8.name = u'Output_Lines'
        param_8.displayName = u'Output Lines'
        param_8.parameterType = 'Required'
        param_8.direction = 'Output'
        param_8.datatype = u'Feature Class'
        param_8.value = u'%scratchGDB%/outputLines'
        # Possible TODO: add symbology if desired:
        # param_8.symbology = 

        # Line_Type
        param_9 = arcpy.Parameter()
        param_9.name = u'Line_Type'
        param_9.displayName = u'Line Type'
        param_9.parameterType = 'Optional'
        param_9.direction = 'Input'
        param_9.datatype = u'String'
        param_9.value = defaultLineType
        param_9.filter.list = lineTypes

        # Spatial_Reference
        param_10 = arcpy.Parameter()
        param_10.name = u'Spatial_Reference'
        param_10.displayName = u'Spatial Reference'
        param_10.parameterType = 'Optional'
        param_10.direction = 'Input'
        param_10.datatype = u'Spatial Reference'
        param_10.value = srWGS84.exportToString()

        return [param_1, param_2, param_3, param_4, param_5, param_6, param_7, param_8, param_9, param_10]

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

        #TODO: 
        pass

# -----------------------------------------------------------------------------
# TableToLineOfBearing Tool
# -----------------------------------------------------------------------------
class TableToLineOfBearing(object):

    class ToolValidator(object):
    
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
            #4 - Bearing Units
            #5 - Bearing Field
            #6 - Distance Units
            #7 - Distance Field
            #8 - Output Lines
            #9 - Line Type
            #10 - Spatial Reference
            return
    
        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""
            #0 - Input Table
            #1 - Input Coordinate Format
            if self.params[1].altered:
                if self.params[1].value in singleFieldTypes:
                    self.params[3].value = self.params[2].value
                    self.params[3].enabled = False
                else:
                    self.params[3].enabled = True
            #2 - X Field
            #3 - Y Field
            #4 - Bearing Units
            #5 - Bearing Field
            #6 - Distance Units
            #7 - Distance Field
            #8 - Output Lines
            #9 - Line Type
            #10 - Spatial Reference
            return
    
        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            #0 - Input Table
            #1 - Input Coordinate Format
            #2 - X Field
            #3 - Y Field
            if not self.params[1].value in singleFieldTypes:
                if self.params[3].value == None or self.params[3].value == "":
                    self.params[3].setErrorMessage(coordinate2ErrorMsg)
            #4 - Bearing Units
            #5 - Bearing Field
            #6 - Distance Units
            #7 - Distance Field
            #8 - Output Lines
            #9 - Line Type
            #10 - Spatial Reference
            return

         # END ToolValidator
   
    def __init__(self):
        self.label = u'Table To Line Of Bearing'
        self.description = u'Creates lines of bearing from tabular coordinates.   '
        self.category = u'Conversion'
        self.canRunInBackground = False

    def getParameterInfo(self):
        # Input_Table
        param_1 = arcpy.Parameter()
        param_1.name = u'Input_Table'
        param_1.displayName = u'Input Table'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Table View'

        # Input_Coordinate_Format
        param_2 = arcpy.Parameter()
        param_2.name = u'Input_Coordinate_Format'
        param_2.displayName = u'Input Coordinate Format'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'String'
        param_2.value = defaultcoordinateFormat
        param_2.filter.list = coordinateFormats

        # X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_
        param_3 = arcpy.Parameter()
        param_3.name = u'X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_'
        param_3.displayName = u'X Field (longitude, UTM, MGRS, USNG, GARS, GEOREF)'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Field'
        param_3.parameterDependencies = ["Input_Table"]

        # Y_Field__latitude_
        param_4 = arcpy.Parameter()
        param_4.name = u'Y_Field__latitude_'
        param_4.displayName = u'Y Field (latitude)'
        param_4.parameterType = 'Optional'
        param_4.direction = 'Input'
        param_4.datatype = u'Field'
        param_4.parameterDependencies = ["Input_Table"]

        # Bearing_Units
        param_5 = arcpy.Parameter()
        param_5.name = u'Bearing_Units'
        param_5.displayName = u'Bearing Units'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'String'
        param_5.value = defaultAngleType
        param_5.filter.list = angleTypes

        # Bearing_Field
        param_6 = arcpy.Parameter()
        param_6.name = u'Bearing_Field'
        param_6.displayName = u'Bearing Field'
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = u'Field'
        param_6.parameterDependencies = ["Input_Table"]

        # Distance_Units
        param_7 = arcpy.Parameter()
        param_7.name = u'Distance_Units'
        param_7.displayName = u'Distance Units'
        param_7.parameterType = 'Required'
        param_7.direction = 'Input'
        param_7.datatype = u'String'
        param_7.value = defaultDistanceType
        param_7.filter.list = distanceTypes

        # Distance_Field
        param_8 = arcpy.Parameter()
        param_8.name = u'Distance_Field'
        param_8.displayName = u'Distance Field'
        param_8.parameterType = 'Required'
        param_8.direction = 'Input'
        param_8.datatype = u'Field'
        param_8.parameterDependencies = ["Input_Table"]

        # Output_Lines
        param_9 = arcpy.Parameter()
        param_9.name = u'Output_Lines'
        param_9.displayName = u'Output Lines'
        param_9.parameterType = 'Required'
        param_9.direction = 'Output'
        param_9.datatype = u'Feature Class'
        param_9.value = u'%scratchGDB%/outputLines'
        # Possible TODO: add symbology if desired:
        # param_9.symbology = 

        # Line_Type
        param_10 = arcpy.Parameter()
        param_10.name = u'Line_Type'
        param_10.displayName = u'Line Type'
        param_10.parameterType = 'Optional'
        param_10.direction = 'Input'
        param_10.datatype = u'String'
        param_10.value = defaultLineType
        param_10.filter.list = lineTypes

        # Spatial_Reference
        param_11 = arcpy.Parameter()
        param_11.name = u'Spatial_Reference'
        param_11.displayName = u'Spatial Reference'
        param_11.parameterType = 'Optional'
        param_11.direction = 'Input'
        param_11.datatype = u'Spatial Reference'
        param_11.value = srWGS84.exportToString()

        return [param_1, param_2, param_3, param_4, param_5, param_6, param_7, param_8, param_9, param_10, param_11]

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

        pass

    # END TableToLineOfBearing

# -----------------------------------------------------------------------------
# TableToPoint Tool
# -----------------------------------------------------------------------------
class TableToPoint(object):

    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""
        
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
            #4 - Output Points
            #5 - Spatial Reference
            return
    
        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""
            #0 - Input Table
            #1 - Input Coordinate Format
            if self.params[1].altered:
                if self.params[1].value in singleFieldTypes:
                    self.params[3].value = self.params[2].value
                    self.params[3].enabled = False
                else:
                    self.params[3].enabled = True
            #2 - X Field
            #3 - Y Field
            #4 - Output Points
            #5 - Spatial Reference
            return
    
        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            #0 - Input Table
            #1 - Input Coordinate Format
            #2 - X Field
            #3 - Y Field
            if not self.params[1].value in singleFieldTypes:
                if self.params[3].value == None or self.params[3].value == "":
                    self.params[3].setErrorMessage(coordinate2ErrorMsg)
            #4 - Output Points
            #5 - Spatial Reference
            return

        # END ToolValidator

    def __init__(self):
        self.label = u'Table To Point'
        self.description = u'Creates point features from tabular coordinates.'
        self.category = u'Conversion'
        self.canRunInBackground = False

    def getParameterInfo(self):
        # Input_Table
        param_1 = arcpy.Parameter()
        param_1.name = u'Input_Table'
        param_1.displayName = u'Input Table'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Table View'

        # Input_Coordinate_Format
        param_2 = arcpy.Parameter()
        param_2.name = u'Input_Coordinate_Format'
        param_2.displayName = u'Input Coordinate Format'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'String'
        param_2.value = defaultcoordinateFormat
        param_2.filter.list = coordinateFormats

        # X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_
        param_3 = arcpy.Parameter()
        param_3.name = u'X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_'
        param_3.displayName = u'X Field (longitude, UTM, MGRS, USNG, GARS, GEOREF)'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Field'
        param_3.parameterDependencies = ["Input_Table"]

        # Y_Field__latitude_
        param_4 = arcpy.Parameter()
        param_4.name = u'Y_Field__latitude_'
        param_4.displayName = u'Y Field (latitude)'
        param_4.parameterType = 'Optional'
        param_4.direction = 'Input'
        param_4.datatype = u'Field'
        param_4.parameterDependencies = ["Input_Table"]

        # Output_Points
        param_5 = arcpy.Parameter()
        param_5.name = u'Output_Points'
        param_5.displayName = u'Output Points'
        param_5.parameterType = 'Required'
        param_5.direction = 'Output'
        param_5.datatype = u'Feature Class'
        param_5.value = u'%scratchGDB%/outputPoints'

        # Spatial_Reference
        param_6 = arcpy.Parameter()
        param_6.name = u'Spatial_Reference'
        param_6.displayName = u'Spatial Reference'
        param_6.parameterType = 'Optional'
        param_6.direction = 'Input'
        param_6.datatype = u'Spatial Reference'
        param_6.value = srWGS84.exportToString()

        return [param_1, param_2, param_3, param_4, param_5, param_6]

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
        pass

    # END TableToPoint

# -----------------------------------------------------------------------------
# TableToPolygon Tool
# -----------------------------------------------------------------------------
class TableToPolygon(object):
    '''
    Use an input table to create polygons
    '''

    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""
          
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
                if self.params[1].value in singleFieldTypes:
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
            if not self.params[1].value in singleFieldTypes:
                if self.params[3].value == None or self.params[3].value == "":
                    self.params[3].setErrorMessage(coordinate2ErrorMsg)
            #4 - Output Table
            #5 - Spatial Reference
            return

        # END ToolValidator

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
        param_1.value = defaultcoordinateFormat
        param_1.filter.list = coordinateFormats

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
        param_7.value = srWGS84.exportToString()
               
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

    # END TableToPolygon

# -----------------------------------------------------------------------------
# TableToPolyline Tool
# -----------------------------------------------------------------------------
class TableToPolyline(object):

    class ToolValidator(object):
    
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
            #4 - Output Polyline Features
            #5 - Line Field
            #6 - Sort Field
            #7 - Spatial Reference               
            return
    
        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""
            #0 - Input Table
            #1 - Input Coordinate Format
            if self.params[1].altered:
                if self.params[1].value in singleFieldTypes:
                    self.params[3].value = self.params[2].value
                    self.params[3].enabled = False
                else:
                    self.params[3].enabled = True
            #2 - X Field
            #3 - Y Field
            #4 - Output Polyline Features
            #5 - Line Field
            #6 - Sort Field
            #7 - Spatial Reference 
            return
    
        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            #0 - Input Table
            #1 - Input Coordinate Format
            if not self.params[1].value in singleFieldTypes:
                if self.params[3].value == None or self.params[3].value == "":
                    self.params[3].setErrorMessage(coordinate2ErrorMsg)
            #2 - X Field
            #3 - Y Field
            #4 - Output Polyline Features
            #5 - Line Field
            #6 - Sort Field
            #7 - Spatial Reference            
            return
            
        # END ToolValidator

    def __init__(self):
        self.label = u'Table To Polyline'
        self.description = u'Creates polyline features from tabular coordinates.    '
        self.category = u'Conversion'
        self.canRunInBackground = False

    def getParameterInfo(self):
        # Input_Table
        param_1 = arcpy.Parameter()
        param_1.name = u'Input_Table'
        param_1.displayName = u'Input Table'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Table View'

        # Input_Coordinate_Format
        param_2 = arcpy.Parameter()
        param_2.name = u'Input_Coordinate_Format'
        param_2.displayName = u'Input Coordinate Format'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'String'
        param_2.value = defaultcoordinateFormat
        param_2.filter.list = coordinateFormats

        # X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_
        param_3 = arcpy.Parameter()
        param_3.name = u'X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_'
        param_3.displayName = u'X Field (longitude, UTM, MGRS, USNG, GARS, GEOREF)'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Field'
        param_3.parameterDependencies = ["Input_Table"]

        # Y_Field__latitude_
        param_4 = arcpy.Parameter()
        param_4.name = u'Y_Field__latitude_'
        param_4.displayName = u'Y Field (latitude)'
        param_4.parameterType = 'Optional'
        param_4.direction = 'Input'
        param_4.datatype = u'Field'
        param_4.parameterDependencies = ["Input_Table"]

        # Output_Polyline_Features
        param_5 = arcpy.Parameter()
        param_5.name = u'Output_Polyline_Features'
        param_5.displayName = u'Output Polyline Features'
        param_5.parameterType = 'Required'
        param_5.direction = 'Output'
        param_5.datatype = u'Feature Class'
        param_5.value = u'%scratchGDB%/outputPolylines'

        # Line_Field
        param_6 = arcpy.Parameter()
        param_6.name = u'Line_Field'
        param_6.displayName = u'Line Field'
        param_6.parameterType = 'Optional'
        param_6.direction = 'Input'
        param_6.datatype = u'Field'
        param_6.parameterDependencies = ["Input_Table"]

        # Sort_Field
        param_7 = arcpy.Parameter()
        param_7.name = u'Sort_Field'
        param_7.displayName = u'Sort Field'
        param_7.parameterType = 'Optional'
        param_7.direction = 'Input'
        param_7.datatype = u'Field'
        param_7.parameterDependencies = ["Input_Table"]

        # Spatial_Reference
        param_8 = arcpy.Parameter()
        param_8.name = u'Spatial_Reference'
        param_8.displayName = u'Spatial Reference'
        param_8.parameterType = 'Optional'
        param_8.direction = 'Input'
        param_8.datatype = u'Spatial Reference'
        param_8.value = srWGS84.exportToString()

        return [param_1, param_2, param_3, param_4, param_5, param_6, param_7, param_8]

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
        pass

    # END TableToPolyline

# -----------------------------------------------------------------------------
# TableToPolyline Tool
# -----------------------------------------------------------------------------
class TableToEllipse(object):

    class ToolValidator(object):
    
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
            #4 - Major Field
            #5 - Minor Field
            #6 - Distance Units
            #7 - Output Ellipse
            #8 - Azimuth Field
            #9 - Azimuth Units
            #10 - Spatial Reference          
            return
    
        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""
            #0 - Input Table
            #1 - Input Coordinate Format
            if self.params[1].altered:
                if self.params[1].value in singleFieldTypes:
                    self.params[3].value = self.params[2].value
                    self.params[3].enabled = False
                else:
                    self.params[3].enabled = True
            #2 - X Field
            #3 - Y Field
            #4 - Major Field
            #5 - Minor Field
            #6 - Distance Units
            #7 - Output Ellipse
            #8 - Azimuth Field
            #9 - Azimuth Units
            #10 - Spatial Reference    
            return
    
        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            #0 - Input Table
            #1 - Input Coordinate Format
            if not self.params[1].value in singleFieldTypes:
                if self.params[3].value == None or self.params[3].value == "":
                    self.params[3].setErrorMessage(coordinate2ErrorMsg)
            #2 - X Field
            #3 - Y Field
            #4 - Major Field
            #5 - Minor Field
            #6 - Distance Units
            #7 - Output Ellipse
            #8 - Azimuth Field
            #9 - Azimuth Units
            #10 - Spatial Reference    
            return
            
        # END ToolValidator

    def __init__(self):
        self.label = u'Table To Ellipse'
        self.description = u'Creates ellipse features from tabular coordinates and input data values.  This tool uses an input table with coordinate values for ellipse centers and values for major and minor axis lengths.'
        self.category = u'Conversion'
        self.canRunInBackground = False

    def getParameterInfo(self):
        # Input_Table
        param_1 = arcpy.Parameter()
        param_1.name = u'Input_Table'
        param_1.displayName = u'Input Table'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Table View'

        # Input_Coordinate_Format
        param_2 = arcpy.Parameter()
        param_2.name = u'Input_Coordinate_Format'
        param_2.displayName = u'Input Coordinate Format'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'String'
        param_2.value = defaultcoordinateFormat
        param_2.filter.list = coordinateFormats

        # X_Field__longitude__UTM__MGRS__USNG__GARS__GeoRef_
        param_3 = arcpy.Parameter()
        param_3.name = u'X_Field__longitude__UTM__MGRS__USNG__GARS__GeoRef_'
        param_3.displayName = u'X Field (longitude, UTM, MGRS, USNG, GARS, GeoRef)'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Field'
        param_3.parameterDependencies = ["Input_Table"]

        # Y_Field__latitude_
        param_4 = arcpy.Parameter()
        param_4.name = u'Y_Field__latitude_'
        param_4.displayName = u'Y Field (latitude)'
        param_4.parameterType = 'Optional'
        param_4.direction = 'Input'
        param_4.datatype = u'Field'
        param_4.parameterDependencies = ["Input_Table"]

        # Major_Field
        param_5 = arcpy.Parameter()
        param_5.name = u'Major_Field'
        param_5.displayName = u'Major Field'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'Field'
        param_5.parameterDependencies = ["Input_Table"]

        # Minor_Field
        param_6 = arcpy.Parameter()
        param_6.name = u'Minor_Field'
        param_6.displayName = u'Minor Field'
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = u'Field'
        param_6.parameterDependencies = ["Input_Table"]

        # Distance_Units
        param_7 = arcpy.Parameter()
        param_7.name = u'Distance_Units'
        param_7.displayName = u'Distance Units'
        param_7.parameterType = 'Required'
        param_7.direction = 'Input'
        param_7.datatype = u'String'
        param_7.value = defaultDistanceType
        param_7.filter.list = distanceTypes

        # Output_Ellipse
        param_8 = arcpy.Parameter()
        param_8.name = u'Output_Ellipse'
        param_8.displayName = u'Output Ellipse'
        param_8.parameterType = 'Required'
        param_8.direction = 'Output'
        param_8.datatype = u'Feature Class'
        param_8.value = u'%scratchGDB%/outputEllipse'

        # Azimuth_Field
        param_9 = arcpy.Parameter()
        param_9.name = u'Azimuth_Field'
        param_9.displayName = u'Azimuth Field'
        param_9.parameterType = 'Optional'
        param_9.direction = 'Input'
        param_9.datatype = u'Field'
        param_9.parameterDependencies = ["Input_Table"]

        # Azimuth_Units
        param_10 = arcpy.Parameter()
        param_10.name = u'Azimuth_Units'
        param_10.displayName = u'Azimuth Units'
        param_10.parameterType = 'Optional'
        param_10.direction = 'Input'
        param_10.datatype = u'String'
        param_10.value = defaultAngleType
        param_10.filter.list = angleTypes

        # Spatial_Reference
        param_11 = arcpy.Parameter()
        param_11.name = u'Spatial_Reference'
        param_11.displayName = u'Spatial Reference'
        param_11.parameterType = 'Optional'
        param_11.direction = 'Input'
        param_11.datatype = u'Spatial Reference'
        param_11.value = srWGS84.exportToString()

        return [param_1, param_2, param_3, param_4, param_5, param_6, param_7, param_8, param_9, param_10, param_11]

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
        pass

    # END TableToEllipse

