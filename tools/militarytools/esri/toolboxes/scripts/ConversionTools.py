'''
 ==================================================
 ConversionTools.py
 --------------------------------------------------
 Requirements: ArcGIS Pro
 Author: ArcGIS Solutions
 Contact: support@esri.com
 Company: Esri
 ==================================================
 Description: Conversion Toolset 
 ==================================================
'''

import os
import arcpy

try:
    from . import ConversionUtilities
except ImportError:
    import ConversionUtilities

# String constants shared by tools:
defaultcoordinateFormat = 'DD_2'
coordinateFormats = ['DD_1', 'DD_2', 'DDM_1', 'DDM_2', 'DMS_1', 'DMS_2', 'GARS', 'GEOREF', 'UTM_BANDS', 'UTM_ZONES', 'USNG', 'MGRS']
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
# GenerateCoordinateNotations Tool
# -----------------------------------------------------------------------------
class GenerateCoordinateNotations(object):

    class ToolValidator(object):
    
        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters
    
        def initializeParameters(self):
            """Refine the properties of a tool's parameters.  This method is
            called when the tool is opened."""
            #0 - Input Table
            #1 - Output Table
            #2 - X Field
            #3 - Input Coordinate Format
            #4 - Y Field (Optional)
            #5 - Input Coordinate System (Optional)                
            return
    
        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""
            #0 - Input Table
            #1 - Output Table
            #2 - X Field
            #3 - Input Coordinate Format
            #4 - Y Field (Optional)
            #5 - Input Coordinate System (Optional)   
            if self.params[3].value in singleFieldTypes:
                self.params[4].value = self.params[4].value
                self.params[4].enabled = False
            else:
                self.params[4].enabled = True

            return
    
        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            #0 - Input Table
            #1 - Output Table
			#2 - X Field
            #3 - Input Coordinate Format
            #4 - Y Field (Optional)
            #5 - Input Coordinate System (Optional)
            if not self.params[3].value in singleFieldTypes:
                if self.params[4].value == None or self.params[4].value == "":
                    self.params[4].setErrorMessage(coordinate2ErrorMsg)
               
            return

        # END ToolValidator

    def __init__(self):
        self.label = 'Generate Coordinate Notations'
        self.description = 'Converts source coordinates in a table to multiple coordinate formats.  ' + \
            'This tool uses an input table with coordinates and outputs a new table with fields for ' + \
            'the following coordinate formats: Decimal Degrees, Decimal Degrees Minutes, ' + \
            'Degrees Minutes Seconds, Universal Transverse Mercator, Military Grid Reference System, ' + \
            'U.S. National Grid, Global Area Reference System, and World Geographic Reference System'
        self.category = 'Conversion'
        self.canRunInBackground = False

    def getParameterInfo(self):

        # in_table
        param_1 = arcpy.Parameter()
        param_1.name = 'in_table'
        param_1.displayName = 'Input Table'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = 'Table View'
        param_1.displayOrder = 0

        # out_table
        param_2 = arcpy.Parameter()
        param_2.name = 'out_table'
        param_2.displayName = 'Output Table'
        param_2.parameterType = 'Required'
        param_2.direction = 'Output'
        param_2.datatype = 'Table'
        param_2.value = 'convertedCoordsTable'
        param_2.displayOrder = 4

        # x_or_longitude_field
        param_3 = arcpy.Parameter()
        param_3.name = 'x_or_longitude_field'
        param_3.displayName = 'X Field (longitude, UTM, MGRS, USNG, GARS, GEOREF)'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = 'Field'
        param_3.parameterDependencies = ["in_table"]
        param_3.displayOrder = 2

        # input_coordinate_format
        param_4 = arcpy.Parameter()
        param_4.name = 'input_coordinate_format'
        param_4.displayName = 'Input Coordinate Format'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = 'String'
        param_4.value = defaultcoordinateFormat
        param_4.filter.list = coordinateFormats
        param_4.displayOrder = 1

        # y_or_latitude_field
        param_5 = arcpy.Parameter()
        param_5.name = 'y_or_latitude_field'
        param_5.displayName = 'Y Field (latitude)'
        param_5.parameterType = 'Optional'
        param_5.direction = 'Input'
        param_5.datatype = 'Field'
        param_5.parameterDependencies = ["in_table"]
        param_5.displayOrder = 3

        # in_coordinate_system
        param_6 = arcpy.Parameter()
        param_6.name = 'in_coordinate_system'
        param_6.displayName = 'Input Coordinate System'
        param_6.parameterType = 'Optional'
        param_6.direction = 'Input'
        param_6.datatype = 'Spatial Reference'
        param_6.value = srWGS84.exportToString()
        param_6.displayOrder = 5

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
        outputTable = parameters[1].valueAsText
        inputXField = parameters[2].valueAsText
        inputCoordinateFormat = parameters[3].valueAsText
        inputYField = parameters[4].valueAsText
        optionalSpatialReference = parameters[5].value
        optionalSpatialReferenceAsText = parameters[5].valueAsText

        if optionalSpatialReferenceAsText == "#" or optionalSpatialReferenceAsText == "":
            optionalSpatialReference = srWGS84 #GCS_WGS_1984

        arcpy.env.overwriteOutput = True

        output = ConversionUtilities.convertCoordinateNotations(inputTable,
                           inputCoordinateFormat,
                           inputXField,
                           inputYField,
                           outputTable,
                           optionalSpatialReference)

        return output

    # END GenerateCoordinateTable

# -----------------------------------------------------------------------------
# CoordinateTableToPoint Tool
# -----------------------------------------------------------------------------
class CoordinateTableToPoint(object):

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
            #1 - Output Features			
            #2 - X Field
            #3 - Input Coordinate Format
            #4 - Y Field (Optional)
            #5 - Input Coordinate System (Optional)
            return
    
        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""
            #0 - Input Table
            #1 - Output Features			
            #2 - X Field
            #3 - Input Coordinate Format
            #4 - Y Field (Optional)
            #5 - Input Coordinate System (Optional)
            if self.params[3].altered:
                if self.params[3].value in singleFieldTypes:
                    self.params[4].value = self.params[2].value
                    self.params[4].enabled = False
                else:
                    self.params[4].enabled = True
            return
    
        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            #0 - Input Table
            #1 - Output Features			
            #2 - X Field
            #3 - Input Coordinate Format
            #4 - Y Field (Optional)
            #5 - Input Coordinate System (Optional)
            if not self.params[3].value in singleFieldTypes:
                if self.params[4].value == None or self.params[4].value == "":
                    self.params[4].setErrorMessage(coordinate2ErrorMsg)
            return

        # END ToolValidator

    def __init__(self):
        self.label = 'Coordinate Table To Point'
        self.description = 'Creates point features from tabular coordinates.'
        self.category = 'Conversion'
        self.canRunInBackground = False

    def getParameterInfo(self):

        # in_table
        param_1 = arcpy.Parameter()
        param_1.name = 'in_table'
        param_1.displayName = 'Input Table'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = 'Table View'
        param_1.displayOrder = 0

        # output_features
        param_2 = arcpy.Parameter()
        param_2.name = 'output_features'
        param_2.displayName = 'Output Point Features'
        param_2.parameterType = 'Required'
        param_2.direction = 'Output'
        param_2.datatype = 'Feature Class'
        param_2.value = 'outputPoints'
        param_2.displayOrder = 4

        # x_or_longitude_field
        param_3 = arcpy.Parameter()
        param_3.name = 'x_or_longitude_field'
        param_3.displayName = 'X Field (longitude, UTM, MGRS, USNG, GARS, GEOREF)'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = 'Field'
        param_3.parameterDependencies = ["in_table"]
        param_3.displayOrder = 2

        # input_coordinate_format
        param_4 = arcpy.Parameter()
        param_4.name = 'input_coordinate_format'
        param_4.displayName = 'Input Coordinate Format'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = 'String'
        param_4.value = defaultcoordinateFormat
        param_4.filter.list = coordinateFormats
        param_4.displayOrder = 1

        # y_or_latitude_field
        param_5 = arcpy.Parameter()
        param_5.name = 'y_or_latitude_field'
        param_5.displayName = 'Y Field (latitude)'
        param_5.parameterType = 'Optional'
        param_5.direction = 'Input'
        param_5.datatype = 'Field'
        param_5.parameterDependencies = ["in_table"]
        param_5.displayOrder = 3

        # in_coordinate_system
        param_6 = arcpy.Parameter()
        param_6.name = 'in_coordinate_system'
        param_6.displayName = 'Input Coordinate System'
        param_6.parameterType = 'Optional'
        param_6.direction = 'Input'
        param_6.datatype = 'Spatial Reference'
        param_6.value = srWGS84.exportToString()
        param_6.displayOrder = 5

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

        inputTable = parameters[0].valueAsText
        outputPointFeatures   = parameters[1].valueAsText
        inputXField = parameters[2].valueAsText
        inputCoordinateFormat = parameters[3].valueAsText
        inputYField = parameters[4].valueAsText
        optionalSpatialReference = parameters[5].value
        optionalSpatialReferenceAsText = parameters[5].valueAsText

        if optionalSpatialReferenceAsText == "#" or optionalSpatialReferenceAsText == "":
            optionalSpatialReference = srWGS84 #GCS_WGS_1984

        arcpy.env.overwriteOutput = True

        outputPointFeaturesOut = ConversionUtilities.tableToPoint(inputTable,
                                    inputCoordinateFormat,
                                    inputXField,
                                    inputYField,
                                    outputPointFeatures,
                                    optionalSpatialReference)

        return outputPointFeaturesOut

    # END CoordinateNotationToPoint

# -----------------------------------------------------------------------------
# CoordinateTableToEllipse Tool
# -----------------------------------------------------------------------------
class CoordinateTableToEllipse(object):

    class ToolValidator(object):
    
        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters
    
        def initializeParameters(self):
            """Refine the properties of a tool's parameters.  This method is
            called when the tool is opened."""
            #0 - Input Table
            #1 - Output Ellipse
            #2 - X Field
            #3 - Major Field
            #4 - Minor Field
            #5 - Input Coordinate Format		
            #6 - Distance Units
            #7 - Y Field
            #8 - Azimuth Field
            #9 - Azimuth Units
            #10 - Input Coordinate System        
            return
    
        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""
            #0 - Input Table
            #1 - Output Ellipse
            #2 - X Field
            #3 - Major Field
            #4 - Minor Field
            #5 - Input Coordinate Format		
            #6 - Distance Units
            #7 - Y Field
            #8 - Azimuth Field
            #9 - Azimuth Units
            #10 - Input Coordinate System  
            if self.params[5].altered:
                if self.params[5].value in singleFieldTypes:
                    self.params[7].value = self.params[2].value
                    self.params[7].enabled = False
                else:
                    self.params[7].enabled = True
                    
            return
    
        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            #0 - Input Table
            #1 - Output Ellipse
            #2 - X Field
            #3 - Major Field
            #4 - Minor Field
            #5 - Input Coordinate Format		
            #6 - Distance Units
            #7 - Y Field
            #8 - Azimuth Field
            #9 - Azimuth Units
            #10 - Input Coordinate System  
            if not self.params[5].value in singleFieldTypes:
                if self.params[7].value == None or self.params[7].value == "":
                    self.params[7].setErrorMessage(coordinate2ErrorMsg)
   
            return
            
        # END ToolValidator

    def __init__(self):
        self.label = 'Coordinate Table To Ellipse'
        self.description = 'Creates ellipse features from tabular coordinates and input data values. ' + \
            'This tool uses an input table with coordinate values for ellipse centers and values for major ' + \
            'and minor axis lengths.'
        self.category = 'Conversion'
        self.canRunInBackground = False

    def getParameterInfo(self):

        # in_table
        param_1 = arcpy.Parameter()
        param_1.name = 'in_table'
        param_1.displayName = 'Input Table'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = 'Table View'
        param_1.displayOrder = 0

        # output_features
        param_2 = arcpy.Parameter()
        param_2.name = 'output_features'
        param_2.displayName = 'Output Ellipse Features'
        param_2.parameterType = 'Required'
        param_2.direction = 'Output'
        param_2.datatype = 'Feature Class'
        param_2.value = 'outputEllipse'
        param_2.displayOrder = 7

       # x_or_longitude_field
        param_3 = arcpy.Parameter()
        param_3.name = 'x_or_longitude_field'
        param_3.displayName = 'X Field (longitude, UTM, MGRS, USNG, GARS, GeoRef)'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = 'Field'
        param_3.parameterDependencies = ["in_table"]
        param_3.displayOrder = 2

        # major_field
        param_4 = arcpy.Parameter()
        param_4.name = 'major_field'
        param_4.displayName = 'Major Field'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = 'Field'
        param_4.parameterDependencies = ["in_table"]
        param_4.displayOrder = 4

        # minor_field
        param_5 = arcpy.Parameter()
        param_5.name = 'minor_field'
        param_5.displayName = 'Minor Field'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = 'Field'
        param_5.parameterDependencies = ["in_table"]
        param_5.displayOrder = 5

        # input_coordinate_format
        param_6 = arcpy.Parameter()
        param_6.name = 'input_coordinate_format'
        param_6.displayName = 'Input Coordinate Format'
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = 'String'
        param_6.value = defaultcoordinateFormat
        param_6.filter.list = coordinateFormats
        param_6.displayOrder = 1

         # distance_units
        param_7 = arcpy.Parameter()
        param_7.name = 'distance_units'
        param_7.displayName = 'Distance Units'
        param_7.parameterType = 'Required'
        param_7.direction = 'Input'
        param_7.datatype = 'String'
        param_7.value = defaultDistanceType
        param_7.filter.list = distanceTypes
        param_7.displayOrder = 6

        # y_or_latitude_field
        param_8 = arcpy.Parameter()
        param_8.name = 'y_or_latitude_field'
        param_8.displayName = 'Y Field (latitude)'
        param_8.parameterType = 'Optional'
        param_8.direction = 'Input'
        param_8.datatype = 'Field'
        param_8.parameterDependencies = ["in_table"]
        param_8.displayOrder = 3

        # azimuth_field
        param_9 = arcpy.Parameter()
        param_9.name = 'azimuth_field'
        param_9.displayName = 'Azimuth Field'
        param_9.parameterType = 'Optional'
        param_9.direction = 'Input'
        param_9.datatype = 'Field'
        param_9.parameterDependencies = ["in_table"]
        param_9.displayOrder = 8

        # azimuth_units
        param_10 = arcpy.Parameter()
        param_10.name = 'azimuth_units'
        param_10.displayName = 'Azimuth Units'
        param_10.parameterType = 'Optional'
        param_10.direction = 'Input'
        param_10.datatype = 'String'
        param_10.value = defaultAngleType
        param_10.filter.list = angleTypes
        param_10.displayOrder = 9

        # in_coordinate_system
        param_11 = arcpy.Parameter()
        param_11.name = 'in_coordinate_system'
        param_11.displayName = 'Input Coordinate System'
        param_11.parameterType = 'Optional'
        param_11.direction = 'Input'
        param_11.datatype = 'Spatial Reference'
        param_11.value = srWGS84.exportToString()
        param_11.displayOrder = 10

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

        inputTable = parameters[0].valueAsText # Input Table
        outputEllipseFeatures = parameters[1].valueAsText # Output Ellipse
        inputXField = parameters[2].valueAsText # X Field (Longitude, UTM, MGRS, USNG, GARS, GeoRef) - from inputTable
        inputMajorAxisField = parameters[3].valueAsText # Major Field - from inputTable
        inputMinorAxisField = parameters[4].valueAsText # Minor Field - from inputTable
        inputCoordinateFormat = parameters[5].valueAsText # Input Coordinate Format
        inputDistanceUnits = parameters[6].valueAsText # Distance Units - from valuelist
        inputYField = parameters[7].valueAsText # Y Field (Latitude)
        inputAzimuthField = parameters[8].valueAsText # Azimuth Field - from inputTable
        inputAzimuthUnits = parameters[9].valueAsText # Azimuth Units - from valuelist
        optionalSpatialReference = parameters[10].value # Spatial Reference
        optionalSpatialReferenceAsText = parameters[10].valueAsText

        if optionalSpatialReferenceAsText == "#" or optionalSpatialReferenceAsText == "":
            optionalSpatialReference = srWGS84 #GCS_WGS_1984

        arcpy.env.overwriteOutput = True

        outputEllipseFeaturesOut = ConversionUtilities.tableToEllipse(inputTable,
                                           inputCoordinateFormat,
                                           inputXField,
                                           inputYField,
                                           inputMajorAxisField,
                                           inputMinorAxisField,
                                           inputDistanceUnits,
                                           outputEllipseFeatures,
                                           inputAzimuthField,
                                           inputAzimuthUnits,
                                           optionalSpatialReference)

        return outputEllipseFeaturesOut

    # END TableToEllipse

# -----------------------------------------------------------------------------
# CoordinateTableTo2PointLine Tool
# -----------------------------------------------------------------------------
class CoordinateTableTo2PointLine(object):

    class ToolValidator(object):
    
        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters
    
        def initializeParameters(self):
            """Refine the properties of a tool's parameters.  This method is
            called when the tool is opened."""
            #0 - Input Table
            #1 - Output Lines
            #2 - Start X Field
            #3 - End X Field
            #4 - Input Coordinate Format
            #5 - Start Y Field (Optional)
            #6 - End Y Field (Optional)
            #7 - Line Type (Optional)
            #8 - Input Coordinate System  (Optional)         
            return
    
        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""
            #0 - Input Table
            #1 - Output Lines
            #2 - Start X Field
            #3 - End X Field
            #4 - Input Coordinate Format
            #5 - Start Y Field (Optional)
            #6 - End Y Field (Optional)
            #7 - Line Type (Optional)
            #8 - Input Coordinate System  (Optional)         
            if self.params[4].altered:
                if self.params[4].value in singleFieldTypes:
                    self.params[5].value = self.params[2].value
                    self.params[5].enabled = False
                    self.params[6].value = self.params[3].value
                    self.params[6].enabled = False
                else:
                    self.params[5].enabled = True
                    self.params[6].enabled = True

            return
    
        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            #0 - Input Table
            #1 - Output Lines
            #2 - Start X Field
            #3 - End X Field
            #4 - Input Coordinate Format
            #5 - Start Y Field (Optional)
            #6 - End Y Field (Optional)
            #7 - Line Type (Optional)
            #8 - Input Coordinate System  (Optional)         
            if not self.params[4].value in singleFieldTypes:
                if self.params[5].value == None or self.params[5].value == "":
                    self.params[5].setErrorMessage(coordinate2ErrorMsg)
                if self.params[6].value == None or self.params[6].value == "":
                    self.params[6].setErrorMessage(coordinate2ErrorMsg)

            return
            
        # END ToolValidator

    def __init__(self):
        self.label = 'Coordinate Table To 2-Point Line'
        self.description = 'Creates a line feature from start and end point coordinates. ' + \
            'This tool uses an input table with coordinate pairs and outputs line features.'
        self.category = 'Conversion'
        self.canRunInBackground = False

    def getParameterInfo(self):

        # in_table
        param_1 = arcpy.Parameter()
        param_1.name = 'in_table'
        param_1.displayName = 'Input Table'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = 'Table View'
        param_1.displayOrder = 0

        # output_features
        param_2 = arcpy.Parameter()
        param_2.name = 'output_features'
        param_2.displayName = 'Output Line Features'
        param_2.parameterType = 'Required'
        param_2.direction = 'Output'
        param_2.datatype = 'Feature Class'
        param_2.value = 'outputLines'
        param_2.displayOrder = 7
        # Possible TODO: add symbology if desired:
        # param_8.symbology =         
 
        # start_x_or_longitude_field
        param_3 = arcpy.Parameter()
        param_3.name = 'start_x_or_longitude_field'
        param_3.displayName = 'Start X Field (longitude, UTM, MGRS, USNG, GARS, GEOREF)'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = 'Field'
        param_3.parameterDependencies = ["in_table"]
        param_3.displayOrder = 2

        # end_x_or_longitude_field
        param_4 = arcpy.Parameter()
        param_4.name = 'end_x_or_longitude_field'
        param_4.displayName = 'End X Field (longitude, UTM, MGRS, USNG, GARS, GEOREF)'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = 'Field'
        param_4.parameterDependencies = ["in_table"]
        param_4.displayOrder = 5

        # input_coordinate_format
        param_5 = arcpy.Parameter()
        param_5.name = 'input_coordinate_format'
        param_5.displayName = 'Input Coordinate Format'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = 'String'
        param_5.value = defaultcoordinateFormat
        param_5.filter.list = coordinateFormats
        param_5.displayOrder = 1

        # start_y_or_latitude_field
        param_6 = arcpy.Parameter()
        param_6.name = 'start_y_or_latitude_field'
        param_6.displayName = 'Start Y Field (latitude)'
        param_6.parameterType = 'Optional'
        param_6.direction = 'Input'
        param_6.datatype = 'Field'
        param_6.parameterDependencies = ["in_table"]
        param_6.displayOrder = 3

        # end_y_or_latitude_field
        param_7 = arcpy.Parameter()
        param_7.name = 'end_y_or_latitude_field'
        param_7.displayName = 'End Y Field (latitude)'
        param_7.parameterType = 'Optional'
        param_7.direction = 'Input'
        param_7.datatype = 'Field'
        param_7.parameterDependencies = ["in_table"]
        param_7.displayOrder = 6

        # line_type
        param_8 = arcpy.Parameter()
        param_8.name = 'line_type'
        param_8.displayName = 'Line Type'
        param_8.parameterType = 'Optional'
        param_8.direction = 'Input'
        param_8.datatype = 'String'
        param_8.value = defaultLineType
        param_8.filter.list = lineTypes
        param_8.displayOrder = 7

        # in_coordinate_system
        param_9 = arcpy.Parameter()
        param_9.name = 'in_coordinate_system'
        param_9.displayName = 'Input Coordinate System'
        param_9.parameterType = 'Optional'
        param_9.direction = 'Input'
        param_9.datatype = 'Spatial Reference'
        param_9.value = srWGS84.exportToString()
        param_9.displayOrder = 8

        return [param_1, param_2, param_3, param_4, param_5, param_6, param_7, param_8, param_9]

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

        inputTable = parameters[0].valueAsText # Input Table
        outputLineFeatures = parameters[1].valueAsText # Output Line
        inputStartXField = parameters[2].valueAsText # Start X Field (longitude, UTM, MGRS, USNG, GARS, GEOREF)(from Input Table)
        inputEndXField = parameters[3].valueAsText # End X Field (longitude, UTM, MGRS, USNG, GARS, GEOREF)(from Input Table)
        inputEndCoordinateFormat = inputStartCoordinateFormat = parameters[4].valueAsText # Start Point Format (from Value List)
        inputStartYField = parameters[5].valueAsText # Start Y Field (latitude)(from Input Table)
        inputEndYField = parameters[6].valueAsText # End Y Field (latitude) (from Input Table)
        inputLineType = parameters[7].valueAsText # Line Type (from Value List)
        optionalSpatialReference = parameters[8].value # Spatial Reference
        optionalSpatialReferenceAsText = parameters[8].valueAsText

        if optionalSpatialReferenceAsText == "#" or optionalSpatialReferenceAsText == "":
            optionalSpatialReference = srWGS84 #GCS_WGS_1984

        arcpy.env.overwriteOutput = True

        outputLineFeaturesOut = ConversionUtilities.tableTo2PointLine(inputTable,
                                              inputStartCoordinateFormat,
                                              inputStartXField,
                                              inputStartYField,
                                              inputEndCoordinateFormat,
                                              inputEndXField,
                                              inputEndYField,
                                              outputLineFeatures,
                                              inputLineType,
                                              optionalSpatialReference)

        # Set output
        return outputLineFeaturesOut

    # END TableTo2PointLine


# *******************************************************************************************************
# OLD TOOLS:
# *******************************************************************************************************


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
        self.label = 'Convert Coordinates'
        self.description = 'Converts source coordinates in a table to multiple coordinate formats.  This tool uses an input table with coordinates and outputs a new table with fields for the following coordinate formats: Decimal Degrees, Decimal Degrees Minutes, Degrees Minutes Seconds, Universal Transverse Mercator, Military Grid Reference System, U.S. National Grid, Global Area Reference System, and World Geographic Reference System'
        self.category = 'Conversion'
        self.canRunInBackground = False

    def getParameterInfo(self):
        # Input_Table
        param_1 = arcpy.Parameter()
        param_1.name = 'Input_Table'
        param_1.displayName = 'Input Table'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = 'Table View'

        # Input_Coordinate_Format
        param_2 = arcpy.Parameter()
        param_2.name = 'Input_Coordinate_Format'
        param_2.displayName = 'Input Coordinate Format'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = 'String'
        param_2.value = defaultcoordinateFormat
        param_2.filter.list = coordinateFormats

        # X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_
        param_3 = arcpy.Parameter()
        param_3.name = 'X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_'
        param_3.displayName = 'X Field (longitude, UTM, MGRS, USNG, GARS, GEOREF)'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = 'Field'
        param_3.parameterDependencies = ["Input_Table"]

        # Y_Field__latitude_
        param_4 = arcpy.Parameter()
        param_4.name = 'Y_Field__latitude_'
        param_4.displayName = 'Y Field (latitude)'
        param_4.parameterType = 'Optional'
        param_4.direction = 'Input'
        param_4.datatype = 'Field'
        param_4.parameterDependencies = ["Input_Table"]

        # Output_Table
        param_5 = arcpy.Parameter()
        param_5.name = 'Output_Table'
        param_5.displayName = 'Output Table'
        param_5.parameterType = 'Required'
        param_5.direction = 'Output'
        param_5.datatype = 'Table'
        param_5.value = 'convertCoords'

        # Spatial_Reference
        param_6 = arcpy.Parameter()
        param_6.name = 'Spatial_Reference'
        param_6.displayName = 'Spatial Reference'
        param_6.parameterType = 'Optional'
        param_6.direction = 'Input'
        param_6.datatype = 'Spatial Reference'
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

        arcpy.env.overwriteOutput = True

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
        self.label = 'Table To 2-Point Line'
        self.description = 'Creates a line feature from start and end point coordinates.  This tool uses an input table with coordinate pairs and outputs line features.   '
        self.category = 'Conversion'
        self.canRunInBackground = False

    def getParameterInfo(self):
        # Input_Table
        param_1 = arcpy.Parameter()
        param_1.name = 'Input_Table'
        param_1.displayName = 'Input Table'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = 'Table View'

        # Start_Point_Format
        param_2 = arcpy.Parameter()
        param_2.name = 'Start_Point_Format'
        param_2.displayName = 'Start Point Format'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = 'String'
        param_2.value = defaultcoordinateFormat
        param_2.filter.list = coordinateFormats

        # Start_X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_
        param_3 = arcpy.Parameter()
        param_3.name = 'Start_X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_'
        param_3.displayName = 'Start X Field (longitude, UTM, MGRS, USNG, GARS, GEOREF)'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = 'Field'
        param_3.parameterDependencies = ["Input_Table"]

        # Start_Y_Field__latitude_
        param_4 = arcpy.Parameter()
        param_4.name = 'Start_Y_Field__latitude_'
        param_4.displayName = 'Start Y Field (latitude)'
        param_4.parameterType = 'Optional'
        param_4.direction = 'Input'
        param_4.datatype = 'Field'
        param_4.parameterDependencies = ["Input_Table"]

        # End_Point_Format
        param_5 = arcpy.Parameter()
        param_5.name = 'End_Point_Format'
        param_5.displayName = 'End Point Format'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = 'String'
        param_5.value = defaultcoordinateFormat
        param_5.filter.list = coordinateFormats

        # End_X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_
        param_6 = arcpy.Parameter()
        param_6.name = 'End_X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_'
        param_6.displayName = 'End X Field (longitude, UTM, MGRS, USNG, GARS, GEOREF)'
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = 'Field'
        param_6.parameterDependencies = ["Input_Table"]

        # End_Y_Field__latitude_
        param_7 = arcpy.Parameter()
        param_7.name = 'End_Y_Field__latitude_'
        param_7.displayName = 'End Y Field (latitude)'
        param_7.parameterType = 'Optional'
        param_7.direction = 'Input'
        param_7.datatype = 'Field'
        param_7.parameterDependencies = ["Input_Table"]

        # Output_Lines
        param_8 = arcpy.Parameter()
        param_8.name = 'Output_Lines'
        param_8.displayName = 'Output Lines'
        param_8.parameterType = 'Required'
        param_8.direction = 'Output'
        param_8.datatype = 'Feature Class'
        param_8.value = 'outputLines'
        # Possible TODO: add symbology if desired:
        # param_8.symbology = 

        # Line_Type
        param_9 = arcpy.Parameter()
        param_9.name = 'Line_Type'
        param_9.displayName = 'Line Type'
        param_9.parameterType = 'Optional'
        param_9.direction = 'Input'
        param_9.datatype = 'String'
        param_9.value = defaultLineType
        param_9.filter.list = lineTypes

        # Spatial_Reference
        param_10 = arcpy.Parameter()
        param_10.name = 'Spatial_Reference'
        param_10.displayName = 'Spatial Reference'
        param_10.parameterType = 'Optional'
        param_10.direction = 'Input'
        param_10.datatype = 'Spatial Reference'
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

        inputTable = parameters[0].valueAsText # Input Table
        inputStartCoordinateFormat = parameters[1].valueAsText # Start Point Format (from Value List)
        inputStartXField = parameters[2].valueAsText # Start X Field (longitude, UTM, MGRS, USNG, GARS, GEOREF)(from Input Table)
        inputStartYField = parameters[3].valueAsText # Start Y Field (latitude)(from Input Table)
        inputEndCoordinateFormat = parameters[4].valueAsText # End Point Format (from Value List)
        inputEndXField = parameters[5].valueAsText # End X Field (longitude, UTM, MGRS, USNG, GARS, GEOREF)(from Input Table)
        inputEndYField = parameters[6].valueAsText # End Y Field (latitude) (from Input Table)
        outputLineFeatures = parameters[7].valueAsText # Output Line
        inputLineType = parameters[8].valueAsText # Line Type (from Value List)
        optionalSpatialReference = parameters[9].value # Spatial Reference
        optionalSpatialReferenceAsText = parameters[9].valueAsText

        if optionalSpatialReferenceAsText == "#" or optionalSpatialReferenceAsText == "":
            optionalSpatialReference = srWGS84 #GCS_WGS_1984

        arcpy.env.overwriteOutput = True

        outputLineFeaturesOut = ConversionUtilities.tableTo2PointLine(inputTable,
                                              inputStartCoordinateFormat,
                                              inputStartXField,
                                              inputStartYField,
                                              inputEndCoordinateFormat,
                                              inputEndXField,
                                              inputEndYField,
                                              outputLineFeatures,
                                              inputLineType,
                                              optionalSpatialReference)

        # Set output
        return outputLineFeaturesOut

    # END TableTo2PointLine

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
        self.label = 'Table To Line Of Bearing'
        self.description = 'Creates lines of bearing from tabular coordinates.   '
        self.category = 'Conversion'
        self.canRunInBackground = False

    def getParameterInfo(self):
        # Input_Table
        param_1 = arcpy.Parameter()
        param_1.name = 'Input_Table'
        param_1.displayName = 'Input Table'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = 'Table View'

        # Input_Coordinate_Format
        param_2 = arcpy.Parameter()
        param_2.name = 'Input_Coordinate_Format'
        param_2.displayName = 'Input Coordinate Format'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = 'String'
        param_2.value = defaultcoordinateFormat
        param_2.filter.list = coordinateFormats

        # X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_
        param_3 = arcpy.Parameter()
        param_3.name = 'X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_'
        param_3.displayName = 'X Field (longitude, UTM, MGRS, USNG, GARS, GEOREF)'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = 'Field'
        param_3.parameterDependencies = ["Input_Table"]

        # Y_Field__latitude_
        param_4 = arcpy.Parameter()
        param_4.name = 'Y_Field__latitude_'
        param_4.displayName = 'Y Field (latitude)'
        param_4.parameterType = 'Optional'
        param_4.direction = 'Input'
        param_4.datatype = 'Field'
        param_4.parameterDependencies = ["Input_Table"]

        # Bearing_Units
        param_5 = arcpy.Parameter()
        param_5.name = 'Bearing_Units'
        param_5.displayName = 'Bearing Units'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = 'String'
        param_5.value = defaultAngleType
        param_5.filter.list = angleTypes

        # Bearing_Field
        param_6 = arcpy.Parameter()
        param_6.name = 'Bearing_Field'
        param_6.displayName = 'Bearing Field'
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = 'Field'
        param_6.parameterDependencies = ["Input_Table"]

        # Distance_Units
        param_7 = arcpy.Parameter()
        param_7.name = 'Distance_Units'
        param_7.displayName = 'Distance Units'
        param_7.parameterType = 'Required'
        param_7.direction = 'Input'
        param_7.datatype = 'String'
        param_7.value = defaultDistanceType
        param_7.filter.list = distanceTypes

        # Distance_Field
        param_8 = arcpy.Parameter()
        param_8.name = 'Distance_Field'
        param_8.displayName = 'Distance Field'
        param_8.parameterType = 'Required'
        param_8.direction = 'Input'
        param_8.datatype = 'Field'
        param_8.parameterDependencies = ["Input_Table"]

        # Output_Lines
        param_9 = arcpy.Parameter()
        param_9.name = 'Output_Lines'
        param_9.displayName = 'Output Lines'
        param_9.parameterType = 'Required'
        param_9.direction = 'Output'
        param_9.datatype = 'Feature Class'
        param_9.value = 'outputLines'
        # Possible TODO: add symbology if desired:
        # param_9.symbology = 

        # Line_Type
        param_10 = arcpy.Parameter()
        param_10.name = 'Line_Type'
        param_10.displayName = 'Line Type'
        param_10.parameterType = 'Optional'
        param_10.direction = 'Input'
        param_10.datatype = 'String'
        param_10.value = defaultLineType
        param_10.filter.list = lineTypes

        # Spatial_Reference
        param_11 = arcpy.Parameter()
        param_11.name = 'Spatial_Reference'
        param_11.displayName = 'Spatial Reference'
        param_11.parameterType = 'Optional'
        param_11.direction = 'Input'
        param_11.datatype = 'Spatial Reference'
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

        inputTable = parameters[0].valueAsText # Input Table
        inputCoordinateFormat = parameters[1].valueAsText # Input Coordinate Format
        inputXField = parameters[2].valueAsText # X Field (Longitude, UTM, MGRS, USNG, GARS, GeoRef) - from inputTable
        inputYField = parameters[3].valueAsText # Y Field (Latitude)
        inputBearingUnits = parameters[4].valueAsText # Bearing Units - from ValueList
        inputBearingField = parameters[5].valueAsText # Bearing Field - from inputTable
        inputDistanceUnits = parameters[6].valueAsText # Distance Units - from ValueList
        inputDistanceField = parameters[7].valueAsText # Distance Field - from inputTable
        outputLineFeatures = parameters[8].valueAsText # Output Lines
        inputLineType = parameters[9].valueAsText # Line Type - from ValueList
        optionalSpatialReference = parameters[10].value # Spatial Reference
        optionalSpatialReferenceAsText = parameters[10].valueAsText

        if optionalSpatialReferenceAsText == "#" or optionalSpatialReferenceAsText == "":
            optionalSpatialReference = srWGS84 #GCS_WGS_1984

        arcpy.env.overwriteOutput = True

        outputLineFeaturesOut = ConversionUtilities.tableToLineOfBearing(inputTable,
                                                 inputCoordinateFormat,
                                                 inputXField,
                                                 inputYField,
                                                 inputBearingUnits,
                                                 inputBearingField,
                                                 inputDistanceUnits,
                                                 inputDistanceField,
                                                 outputLineFeatures,
                                                 inputLineType,
                                                 optionalSpatialReference)

        return outputLineFeaturesOut

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
        self.label = 'Table To Point'
        self.description = 'Creates point features from tabular coordinates.'
        self.category = 'Conversion'
        self.canRunInBackground = False

    def getParameterInfo(self):
        # Input_Table
        param_1 = arcpy.Parameter()
        param_1.name = 'Input_Table'
        param_1.displayName = 'Input Table'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = 'Table View'

        # Input_Coordinate_Format
        param_2 = arcpy.Parameter()
        param_2.name = 'Input_Coordinate_Format'
        param_2.displayName = 'Input Coordinate Format'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = 'String'
        param_2.value = defaultcoordinateFormat
        param_2.filter.list = coordinateFormats

        # X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_
        param_3 = arcpy.Parameter()
        param_3.name = 'X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_'
        param_3.displayName = 'X Field (longitude, UTM, MGRS, USNG, GARS, GEOREF)'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = 'Field'
        param_3.parameterDependencies = ["Input_Table"]

        # Y_Field__latitude_
        param_4 = arcpy.Parameter()
        param_4.name = 'Y_Field__latitude_'
        param_4.displayName = 'Y Field (latitude)'
        param_4.parameterType = 'Optional'
        param_4.direction = 'Input'
        param_4.datatype = 'Field'
        param_4.parameterDependencies = ["Input_Table"]

        # Output_Points
        param_5 = arcpy.Parameter()
        param_5.name = 'Output_Points'
        param_5.displayName = 'Output Points'
        param_5.parameterType = 'Required'
        param_5.direction = 'Output'
        param_5.datatype = 'Feature Class'
        param_5.value = 'outputPoints'

        # Spatial_Reference
        param_6 = arcpy.Parameter()
        param_6.name = 'Spatial_Reference'
        param_6.displayName = 'Spatial Reference'
        param_6.parameterType = 'Optional'
        param_6.direction = 'Input'
        param_6.datatype = 'Spatial Reference'
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

        inputTable = parameters[0].valueAsText
        inputCoordinateFormat = parameters[1].valueAsText
        inputXField = parameters[2].valueAsText
        inputYField = parameters[3].valueAsText
        outputPointFeatures = parameters[4].valueAsText
        optionalSpatialReference = parameters[5].value
        optionalSpatialReferenceAsText = parameters[5].valueAsText

        if optionalSpatialReferenceAsText == "#" or optionalSpatialReferenceAsText == "":
            optionalSpatialReference = srWGS84 #GCS_WGS_1984

        arcpy.env.overwriteOutput = True

        outputPointFeaturesOut = ConversionUtilities.tableToPoint(inputTable,
                                    inputCoordinateFormat,
                                    inputXField,
                                    inputYField,
                                    outputPointFeatures,
                                    optionalSpatialReference)

        return outputPointFeaturesOut

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
        self.label = 'Table To Polygon'
        self.description = 'Converts an input table of vertex points to one or more polygon features.'
        self.category = 'Conversion'
        self.canRunInBackground = False
        
    def getParameterInfo(self):

        # Input_Table
        param_0 = arcpy.Parameter()
        param_0.name = 'Input_Table'
        param_0.displayName = 'Input Table'
        param_0.parameterType = 'Required'
        param_0.direction = 'Input'
        param_0.datatype = 'Table View'
        
        # Input_Coordinate_Format
        param_1 = arcpy.Parameter()
        param_1.name = 'Input_Coordinate_Format'
        param_1.displayName = 'Input Coordinate Format'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = 'String'
        param_1.value = defaultcoordinateFormat
        param_1.filter.list = coordinateFormats

        # X_Field__Longitude__UTM__MGRS__USNG__GARS__GeoRef_
        param_2 = arcpy.Parameter()
        param_2.name = 'X_Field_Longitude_UTM_MGRS_USNG_GARS_GeoRef_'
        param_2.displayName = 'X Field (Longitude, UTM, MGRS, USNG, GARS, GeoRef)'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = 'Field'
        param_2.parameterDependencies = ["Input_Table"]
        
        # Y_Field__Latitude_
        param_3 = arcpy.Parameter()
        param_3.name = 'Y_Field__latitude_'
        param_3.displayName = 'Y Field (Latitude)'
        param_3.parameterType = 'Optional'
        param_3.direction = 'Input'
        param_3.datatype = 'Field'
        param_3.parameterDependencies = ["Input_Table"]
        
        # Output_Polygon_Features
        param_4 = arcpy.Parameter()
        param_4.name = 'Output_Polygon_Features'
        param_4.displayName = 'Output Polygon Features'
        param_4.parameterType = 'Required'
        param_4.direction = 'Output'
        param_4.datatype = 'Feature Class'
        param_4.value = 'outputPolygons'
     
        # Line_Field
        param_5 = arcpy.Parameter()
        param_5.name = 'Line_Field'
        param_5.displayName = 'Line Field'
        param_5.parameterType = 'Optional'
        param_5.direction = 'Input'
        param_5.datatype = 'Field'
        param_5.parameterDependencies = ["Input_Table"]
                
        # Sort_Field
        param_6 = arcpy.Parameter()
        param_6.name = 'Sort_Field'
        param_6.displayName = 'Sort Field'
        param_6.parameterType = 'Optional'
        param_6.direction = 'Input' 
        param_6.datatype = 'Field'
        param_6.parameterDependencies = ["Input_Table"]
                
        # Spatial_Reference
        param_7 = arcpy.Parameter()
        param_7.name = 'Spatial_Reference'
        param_7.displayName = 'Spatial Reference'
        param_7.parameterType = 'Optional'
        param_7.direction = 'Input'
        param_7.datatype = 'Spatial Reference'
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
        optionalSpatialReference = parameters[7].value
        optionalSpatialReferenceAsText = parameters[7].valueAsText
            
        if optionalSpatialReferenceAsText == "#" or optionalSpatialReferenceAsText == "":
            optionalSpatialReference = srWGS84 #GCS_WGS_1984
                        
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
                                                         optionalSpatialReference)
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
        self.label = 'Table To Polyline'
        self.description = 'Creates polyline features from tabular coordinates.    '
        self.category = 'Conversion'
        self.canRunInBackground = False

    def getParameterInfo(self):
        # Input_Table
        param_1 = arcpy.Parameter()
        param_1.name = 'Input_Table'
        param_1.displayName = 'Input Table'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = 'Table View'

        # Input_Coordinate_Format
        param_2 = arcpy.Parameter()
        param_2.name = 'Input_Coordinate_Format'
        param_2.displayName = 'Input Coordinate Format'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = 'String'
        param_2.value = defaultcoordinateFormat
        param_2.filter.list = coordinateFormats

        # X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_
        param_3 = arcpy.Parameter()
        param_3.name = 'X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_'
        param_3.displayName = 'X Field (longitude, UTM, MGRS, USNG, GARS, GEOREF)'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = 'Field'
        param_3.parameterDependencies = ["Input_Table"]

        # Y_Field__latitude_
        param_4 = arcpy.Parameter()
        param_4.name = 'Y_Field__latitude_'
        param_4.displayName = 'Y Field (latitude)'
        param_4.parameterType = 'Optional'
        param_4.direction = 'Input'
        param_4.datatype = 'Field'
        param_4.parameterDependencies = ["Input_Table"]

        # Output_Polyline_Features
        param_5 = arcpy.Parameter()
        param_5.name = 'Output_Polyline_Features'
        param_5.displayName = 'Output Polyline Features'
        param_5.parameterType = 'Required'
        param_5.direction = 'Output'
        param_5.datatype = 'Feature Class'
        param_5.value = 'outputPolylines'

        # Line_Field
        param_6 = arcpy.Parameter()
        param_6.name = 'Line_Field'
        param_6.displayName = 'Line Field'
        param_6.parameterType = 'Optional'
        param_6.direction = 'Input'
        param_6.datatype = 'Field'
        param_6.parameterDependencies = ["Input_Table"]

        # Sort_Field
        param_7 = arcpy.Parameter()
        param_7.name = 'Sort_Field'
        param_7.displayName = 'Sort Field'
        param_7.parameterType = 'Optional'
        param_7.direction = 'Input'
        param_7.datatype = 'Field'
        param_7.parameterDependencies = ["Input_Table"]

        # Spatial_Reference
        param_8 = arcpy.Parameter()
        param_8.name = 'Spatial_Reference'
        param_8.displayName = 'Spatial Reference'
        param_8.parameterType = 'Optional'
        param_8.direction = 'Input'
        param_8.datatype = 'Spatial Reference'
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

        inputTable = parameters[0].valueAsText # Input Table
        inputCoordinateFormat = parameters[1].valueAsText # Input Coordinate Format - from ValueList
        inputXField = parameters[2].valueAsText # X Field (Longitude, UTM, MGRS, USNG, GARS, GeoRef) - from inputTable
        inputYField = parameters[3].valueAsText # Y Field (Latitude)
        outputPolylineFeatures = parameters[4].valueAsText # Output Polygon Features
        inputLineField = parameters[5].valueAsText # Line Field (optional) - from inputTable
        inputSortField = parameters[6].valueAsText # Sort Field (optional) - from inputTable
        optionalSpatialReference = parameters[7].value # Spatial Reference
        optionalSpatialReferenceAsText = parameters[7].valueAsText

        if optionalSpatialReferenceAsText == "#" or optionalSpatialReferenceAsText == "":
            optionalSpatialReference = srWGS84 #GCS_WGS_1984

        arcpy.env.overwriteOutput = True

        outputPolylineFeaturesOut = ConversionUtilities.tableToPolyline(inputTable,
                                            inputCoordinateFormat,
                                            inputXField,
                                            inputYField,
                                            outputPolylineFeatures,
                                            inputLineField,
                                            inputSortField,
                                            optionalSpatialReference)

        return outputPolylineFeaturesOut

    # END TableToPolyline

# -----------------------------------------------------------------------------
# TableToEllipse Tool
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
        self.label = 'Table To Ellipse'
        self.description = 'Creates ellipse features from tabular coordinates and input data values.  This tool uses an input table with coordinate values for ellipse centers and values for major and minor axis lengths.'
        self.category = 'Conversion'
        self.canRunInBackground = False

    def getParameterInfo(self):
        # Input_Table
        param_1 = arcpy.Parameter()
        param_1.name = 'Input_Table'
        param_1.displayName = 'Input Table'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = 'Table View'

        # Input_Coordinate_Format
        param_2 = arcpy.Parameter()
        param_2.name = 'Input_Coordinate_Format'
        param_2.displayName = 'Input Coordinate Format'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = 'String'
        param_2.value = defaultcoordinateFormat
        param_2.filter.list = coordinateFormats

        # X_Field__longitude__UTM__MGRS__USNG__GARS__GeoRef_
        param_3 = arcpy.Parameter()
        param_3.name = 'X_Field__longitude__UTM__MGRS__USNG__GARS__GeoRef_'
        param_3.displayName = 'X Field (longitude, UTM, MGRS, USNG, GARS, GeoRef)'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = 'Field'
        param_3.parameterDependencies = ["Input_Table"]

        # Y_Field__latitude_
        param_4 = arcpy.Parameter()
        param_4.name = 'Y_Field__latitude_'
        param_4.displayName = 'Y Field (latitude)'
        param_4.parameterType = 'Optional'
        param_4.direction = 'Input'
        param_4.datatype = 'Field'
        param_4.parameterDependencies = ["Input_Table"]

        # Major_Field
        param_5 = arcpy.Parameter()
        param_5.name = 'Major_Field'
        param_5.displayName = 'Major Field'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = 'Field'
        param_5.parameterDependencies = ["Input_Table"]

        # Minor_Field
        param_6 = arcpy.Parameter()
        param_6.name = 'Minor_Field'
        param_6.displayName = 'Minor Field'
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = 'Field'
        param_6.parameterDependencies = ["Input_Table"]

        # Distance_Units
        param_7 = arcpy.Parameter()
        param_7.name = 'Distance_Units'
        param_7.displayName = 'Distance Units'
        param_7.parameterType = 'Required'
        param_7.direction = 'Input'
        param_7.datatype = 'String'
        param_7.value = defaultDistanceType
        param_7.filter.list = distanceTypes

        # Output_Ellipse
        param_8 = arcpy.Parameter()
        param_8.name = 'Output_Ellipse'
        param_8.displayName = 'Output Ellipse'
        param_8.parameterType = 'Required'
        param_8.direction = 'Output'
        param_8.datatype = 'Feature Class'
        param_8.value = 'outputEllipse'

        # Azimuth_Field
        param_9 = arcpy.Parameter()
        param_9.name = 'Azimuth_Field'
        param_9.displayName = 'Azimuth Field'
        param_9.parameterType = 'Optional'
        param_9.direction = 'Input'
        param_9.datatype = 'Field'
        param_9.parameterDependencies = ["Input_Table"]

        # Azimuth_Units
        param_10 = arcpy.Parameter()
        param_10.name = 'Azimuth_Units'
        param_10.displayName = 'Azimuth Units'
        param_10.parameterType = 'Optional'
        param_10.direction = 'Input'
        param_10.datatype = 'String'
        param_10.value = defaultAngleType
        param_10.filter.list = angleTypes

        # Spatial_Reference
        param_11 = arcpy.Parameter()
        param_11.name = 'Spatial_Reference'
        param_11.displayName = 'Spatial Reference'
        param_11.parameterType = 'Optional'
        param_11.direction = 'Input'
        param_11.datatype = 'Spatial Reference'
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

        inputTable = parameters[0].valueAsText # Input Table
        inputCoordinateFormat = parameters[1].valueAsText # Input Coordinate Format
        inputXField = parameters[2].valueAsText # X Field (Longitude, UTM, MGRS, USNG, GARS, GeoRef) - from inputTable
        inputYField = parameters[3].valueAsText # Y Field (Latitude)
        inputMajorAxisField = parameters[4].valueAsText # Major Field - from inputTable
        inputMinorAxisField = parameters[5].valueAsText # Minor Field - from inputTable
        inputDistanceUnits = parameters[6].valueAsText # Distance Units - from valuelist
        outputEllipseFeatures = parameters[7].valueAsText # Output Ellipse
        inputAzimuthField = parameters[8].valueAsText # Azimuth Field - from inputTable
        inputAzimuthUnits = parameters[9].valueAsText # Azimuth Units - from valuelist
        optionalSpatialReference = parameters[10].value # Spatial Reference
        optionalSpatialReferenceAsText = parameters[10].valueAsText

        if optionalSpatialReferenceAsText == "#" or optionalSpatialReferenceAsText == "":
            optionalSpatialReference = srWGS84 #GCS_WGS_1984

        arcpy.env.overwriteOutput = True

        outputEllipseFeaturesOut = ConversionUtilities.tableToEllipse(inputTable,
                                           inputCoordinateFormat,
                                           inputXField,
                                           inputYField,
                                           inputMajorAxisField,
                                           inputMinorAxisField,
                                           inputDistanceUnits,
                                           outputEllipseFeatures,
                                           inputAzimuthField,
                                           inputAzimuthUnits,
                                           optionalSpatialReference)

        return outputEllipseFeaturesOut

    # END TableToEllipse

