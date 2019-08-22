# coding: utf-8
'''
------------------------------------------------------------------------------
 Copyright 2018 Esri
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
 DistanceAndDirectionTools.py
 --------------------------------------------------
 requirements: ArcGIS 10.3.1+, ArcGIS Pro 1.4+, Python 2.7 or Python 3.5+
 author: ArcGIS Solutions
 contact: support@esri.com
 company: Esri
 ==================================================
 description:
 Distance and Direction Toolset Tools
 ==================================================
'''

import os
import sys
import arcpy

try:
    from . import RangeRingUtils
except ImportError:
    import RangeRingUtils


######################### Globals ####################################

supportedDistanceUnits = ['METERS', 'KILOMETERS', 'MILES', 'NAUTICAL_MILES', 'FEET', 'US_SURVEY_FEET']

msgPositiveValueRequired = "Positive integer values are required."

# ----------------------------------------------------------------------------------
# RangeRingsFromInterval Tool
# ----------------------------------------------------------------------------------
class RangeRingsFromInterval(object):

    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""
    
        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters
    
        def initializeParameters(self):
            """Refine the properties of a tool's parameters.  This method is
            called when the tool is opened."""
    
            return
    
        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""
    
            return
    
        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
             parameter.  This method is called after internal validation."""

            if self.params[1].altered:
                if self.params[1].value <= 0:
                    self.params[1].setWarningMessage(msgPositiveValueRequired)

            if self.params[2].altered:
                if self.params[2].value <= 0:
                    self.params[2].setWarningMessage(msgPositiveValueRequired)

            if self.params[6].altered:
                if self.params[6].value <= 0:
                    self.params[6].setWarningMessage(msgPositiveValueRequired)
                    self.params[7].enabled = False
                    self.params[7].parameterType = 'Optional'
                else:
                    self.params[7].enabled = True
                    self.params[7].parameterType = 'Required'

            return
        # end Class ToolValidator
    
    def __init__(self):
        self.label = 'Generate Range Rings From Interval'
        self.description = 'Create a concentric circle from a center, with a number of rings, and the distance between rings.'
        self.category = 'Distance and Direction'
        self.canRunInBackground = False
        
    def getParameterInfo(self):

        # in_features
        param_1 = arcpy.Parameter()
        param_1.name = 'in_features'
        param_1.displayName = 'Input Features (Center Points)'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'        
        param_1.datatype = 'Feature Set'  # Same as 'GPFeatureRecordSetLayer'
        
        # Set the Feature Set schema and symbology
        input_layer_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                          "layers",
                                          "MTInputPoints.lyrx")
        param_1.value = input_layer_file_path
        param_1.displayOrder = 0

        # in_number_of_rings
        param_2 = arcpy.Parameter()
        param_2.name = 'in_number_of_rings'
        param_2.displayName = 'Number of Rings'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = 'Long'
        param_2.value = '4'
        param_2.displayOrder = 1

        # in_interval_between_rings
        param_3 = arcpy.Parameter()
        param_3.name = 'in_interval_between_rings'
        param_3.displayName = 'Interval Between Rings'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = 'Double'
        param_3.value = '100'
        param_3.displayOrder = 2

        # in_distance_units
        param_4 = arcpy.Parameter()
        param_4.name = 'in_distance_units'
        param_4.displayName = 'Distance Units'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = 'String'
        param_4.value = supportedDistanceUnits[0]
        param_4.filter.list = supportedDistanceUnits
        param_4.displayOrder = 3

        # output_feature_class_rings
        param_5 = arcpy.Parameter()
        param_5.name = 'output_feature_class_rings'
        param_5.displayName = 'Output Feature Class (Rings)'
        param_5.parameterType = 'Required'
        param_5.direction = 'Output'
        param_5.datatype = 'Feature Class'
        param_5.value = '%scratchGDB%\\Rings'
        param_5.symbology = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                            "layers", "RangeRings.lyrx")
        param_5.displayOrder = 5

        # in_spatial_reference
        param_6 = arcpy.Parameter()
        param_6.name = 'in_spatial_reference'
        param_6.displayName = 'Spatial Reference'
        param_6.parameterType = 'Optional'
        param_6.direction = 'Input'
        param_6.datatype = 'Spatial Reference'
        param_6.displayOrder = 7

        # in_number_of_radials 
        param_7 = arcpy.Parameter()
        param_7.name = 'in_number_of_radials'
        param_7.displayName = 'Number of Radials'
        param_7.parameterType = 'Optional'
        param_7.direction = 'Input'
        param_7.datatype = 'Long'
        param_7.value = ''
        param_7.displayOrder = 4

        # Output_Radial_Features
        param_8 = arcpy.Parameter()
        param_8.name = 'output_feature_class_radials'
        param_8.displayName = 'Output Feature Class (Radials)'
        param_8.parameterType = 'Optional'
        param_8.direction = 'Output'
        param_8.datatype = 'Feature Class'
        param_8.value = '%scratchGDB%\\Radials'
        param_8.symbology = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                            "layers", "RangeRadials.lyrx")
        param_8.enabled = False  # disable until number_of_radials set
        param_8.displayOrder = 6

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

        inputCenterFeatures = parameters[0].valueAsText
        inputNumberOfRings = parameters[1].value
        inputDistanceBetween = parameters[2].value
        inputDistanceUnits = parameters[3].value
        outputRingFeatures = parameters[4].valueAsText
        optionalSpatialReference = parameters[5].value
        optionalSpatialReferenceAsText = parameters[5].valueAsText
        inputNumberOfRadials = parameters[6].value
        outputRadialFeatures = parameters[7].valueAsText

        if optionalSpatialReferenceAsText == "#" or optionalSpatialReferenceAsText == "":
            optionalSpatialReference = None

        if inputNumberOfRadials == "#" or inputNumberOfRadials == "" or inputNumberOfRadials is None :
            inputNumberOfRadials = 0
            outputRadialFeatures = None

        if outputRadialFeatures == "#" or outputRadialFeatures == "" or outputRadialFeatures is None:
            inputNumberOfRadials = 0
            outputRadialFeatures = None

        # get/set environment
        arcpy.env.overwriteOutput = True

        # Call tool method
        rr = RangeRingUtils.rangeRingsFromInterval(inputCenterFeatures,
                                                   inputNumberOfRings,
                                                   inputDistanceBetween,
                                                   inputDistanceUnits,
                                                   inputNumberOfRadials,
                                                   outputRingFeatures,
                                                   outputRadialFeatures,
                                                   optionalSpatialReference)

        # Set output
        return rr[0], rr[1]

# ----------------------------------------------------------------------------------
# RangeRingFromMinimumAndMaximum Tool
# ----------------------------------------------------------------------------------
class RangeRingFromMinimumAndMaximum(object):

    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""
    
        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters
    
        def initializeParameters(self):
            """Refine the properties of a tool's parameters.  This method is
            called when the tool is opened."""
    
            return
    
        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""
    
            return
    
        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
             parameter.  This method is called after internal validation."""

            if self.params[1].altered:
                if self.params[1].value <= 0:
                    self.params[1].setWarningMessage(msgPositiveValueRequired)

            if self.params[2].altered:
                if self.params[2].value <= 0:
                    self.params[2].setWarningMessage(msgPositiveValueRequired)

            if self.params[6].altered:
                if self.params[6].value <= 0:
                    self.params[6].setWarningMessage(msgPositiveValueRequired)
                    self.params[7].enabled = False
                    self.params[7].parameterType = 'Optional'
                else:
                    self.params[7].enabled = True
                    self.params[7].parameterType = 'Required'

            return
        # end Class ToolValidator

    def __init__(self):
        self.label = 'Generate Range Rings From Minimum And Maximum'
        self.description = 'Create a concentric circle from a center with two rings depicting a minimum range and a maximum range.'
        self.category = 'Distance and Direction'
        self.canRunInBackground = False

    def getParameterInfo(self):

        # in_features
        param_1 = arcpy.Parameter()
        param_1.name = 'in_features'
        param_1.displayName = 'Input Features (Center Points)'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = 'Feature Set'
        # Set the Feature Set schema and symbology
        input_layer_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                          "layers",
                                          "MTInputPoints.lyrx")
        param_1.value = input_layer_file_path
        param_1.displayOrder = 0

        # in_minimum_range
        param_2 = arcpy.Parameter()
        param_2.name = 'in_minimum_range'
        param_2.displayName = 'Minimum Range'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = 'Double'
        param_2.value = '100'
        param_2.displayOrder = 1

        # in_maximum_range
        param_3 = arcpy.Parameter()
        param_3.name = 'in_maximum_range'
        param_3.displayName = 'Maximum Range'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = 'Double'
        param_3.value = '1000'
        param_3.displayOrder = 2

        # in_distance_units
        param_4 = arcpy.Parameter()
        param_4.name = 'in_distance_units'
        param_4.displayName = 'Distance Units'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = 'String'
        param_4.value = supportedDistanceUnits[0]
        param_4.filter.list = supportedDistanceUnits
        param_4.displayOrder = 3

        # output_feature_class_rings
        param_5 = arcpy.Parameter()
        param_5.name = 'output_feature_class_rings'
        param_5.displayName = 'Output Feature Class (Rings)'
        param_5.parameterType = 'Required'
        param_5.direction = 'Output'
        param_5.datatype = 'Feature Class'
        param_5.value = '%scratchGDB%\\rings'
        param_5.symbology = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                            "layers", "RangeRings.lyrx")
        param_5.displayOrder = 5

        # in_spatial_reference
        param_6 = arcpy.Parameter()
        param_6.name = 'in_spatial_reference'
        param_6.displayName = 'Spatial Reference'
        param_6.parameterType = 'Optional'
        param_6.direction = 'Input'
        param_6.datatype = 'Spatial Reference'
        param_6.displayOrder = 7

        # in_number_of_radials
        param_7 = arcpy.Parameter()
        param_7.name = 'in_number_of_radials'
        param_7.displayName = 'Number of Radials'
        param_7.parameterType = 'Optional'
        param_7.direction = 'Input'
        param_7.datatype = 'Long'
        param_7.value = ''
        param_7.displayOrder = 4

        # output_feature_class_radials
        param_8 = arcpy.Parameter()
        param_8.name = 'output_feature_class_radials'
        param_8.displayName = 'Output Feature Class (Radials)'
        param_8.parameterType = 'Optional'
        param_8.direction = 'Output'
        param_8.datatype = 'Feature Class'
        param_8.value = '%scratchGDB%\\radials'
        param_8.symbology = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                            "layers", "RangeRadials.lyrx")
        param_8.enabled = False  # disable until number_of_radials set
        param_8.displayOrder = 6

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

        inputCenterFeatures = parameters[0].valueAsText
        inputMinimumRange = parameters[1].value
        inputMaximumRange = parameters[2].value
        inputDistanceUnits = parameters[3].value
        outputRingFeatures = parameters[4].valueAsText
        optionalSpatialReference = parameters[5].value
        optionalSpatialReferenceAsText = parameters[5].valueAsText
        inputNumberOfRadials = parameters[6].value
        outputRadialFeatures = parameters[7].valueAsText

        if optionalSpatialReferenceAsText == "#" or optionalSpatialReferenceAsText == "":
            optionalSpatialReference = None

        if inputNumberOfRadials == "#" or inputNumberOfRadials == "" or inputNumberOfRadials is None :
            inputNumberOfRadials = 0
            outputRadialFeatures = None

        if outputRadialFeatures == "#" or outputRadialFeatures == "" or outputRadialFeatures is None:
            inputNumberOfRadials = 0
            outputRadialFeatures = None

        rr = RangeRingUtils.rangeRingsFromMinMax(inputCenterFeatures,
                                                 inputMinimumRange,
                                                 inputMaximumRange,
                                                 inputDistanceUnits,
                                                 inputNumberOfRadials,
                                                 outputRingFeatures,
                                                 outputRadialFeatures,
                                                 optionalSpatialReference)

        # Set output
        return rr[0], rr[1]

# ----------------------------------------------------------------------------------
# RangeRingsFromMinAndMaxTable Tool
# ----------------------------------------------------------------------------------
class RangeRingsFromMinAndMaxTable(object):
    
    class ToolValidator(object):
        """Class for validating a tool's parameter values and controlling
        the behavior of the tool's dialog."""
    
        def __init__(self, parameters):
            """Setup arcpy and the list of tool parameters."""
            self.params = parameters
    
        def initializeParameters(self):
            """Refine the properties of a tool's parameters.  This method is
            called when the tool is opened."""

            inputParamsTable = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                          "tooldata", "RangeRings.gdb", "rrInputTable")
            self.params[1].value = inputParamsTable
            # Get list of type names from InputTable [1]
            typeNames = self.updateTypes(str(self.params[1].value))
            self.params[2].filter.list = typeNames
            self.params[2].value = typeNames[0]

            return
    
        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""
    
            if self.params[1].altered:
                # Update list of type names from Input Table [1]
                self.params[2].filter.list = self.updateTypes(str(self.params[1].value))
    
            return
    
        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
             parameter.  This method is called after internal validation."""

            if self.params[5].altered:
                if self.params[5].value <= 0:
                    self.params[5].setWarningMessage(msgPositiveValueRequired)
                    self.params[6].enabled = False
                    self.params[6].parameterType = 'Optional'
                else:
                    self.params[6].enabled = True
                    self.params[6].parameterType = 'Required'

            return
    
        def updateTypes(self,inputTable):
            # Make a list of 'name' field from the input table
            Names = []
            try:
                tableRows = arcpy.da.SearchCursor(inputTable,["Name"])
                for row in tableRows:
                    name = str(row[0])
                    Names.append(name)
                del tableRows
            except:
                msg = "ERROR LOADING INPUT TABLE!!"
                Names.append(msg)
                messages.AddErrorMessage(msg)
            return Names

    def __init__(self):
        self.label = 'Generate Range Rings From Minimum And Maximum Table'
        self.description = 'Create a concentric circle from a center with two rings depicting a minimum range and a maximum range from a table.'
        self.category = 'Distance and Direction'
        self.canRunInBackground = False

    def getParameterInfo(self):

        # in_features
        param_1 = arcpy.Parameter()
        param_1.name = 'in_features'
        param_1.displayName = 'Input Features (Center Points)'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = 'Feature Set'
        # Set the Feature Set schema
        input_layer_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                          "layers",
                                          "MTInputPoints.lyrx")
        param_1.value = input_layer_file_path
        param_1.displayOrder = 0

        # in_table
        param_2 = arcpy.Parameter()
        param_2.name = 'in_table'
        param_2.displayName = 'Input Table (Name and Min/Max Ranges)'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = 'Table'
        # military-tools-geoprocessing-toolbox\\toolboxes\\tooldata\\Range
        # Rings.gdb\\rrInputTable'
#
# --> TODO: we will not be able to deploy this table in Pro so this needs to be removed
#
        param_2.value = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                          "tooldata", "RangeRings.gdb", "rrInputTable")
        param_2.displayOrder = 1

        # selected_type
        param_3 = arcpy.Parameter()
        param_3.name = 'in_selected_type'
        param_3.displayName = 'Selected Type'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = 'String'
        param_3.value = 'M4'
        param_3.filter.list = ['M4', 'M249']
        param_3.displayOrder = 2

        # output_feature_class_rings
        param_4 = arcpy.Parameter()
        param_4.name = 'output_feature_class_rings'
        param_4.displayName = 'Output Feature Class (Rings)'
        param_4.parameterType = 'Required'
        param_4.direction = 'Output'
        param_4.datatype = 'Feature Class'
        param_4.value = '%scratchGDB%\\Rings'
        param_4.symbology = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                            "layers", "RangeRings.lyrx")
        param_4.displayOrder = 4

        # in_spatial_reference
        param_5 = arcpy.Parameter()
        param_5.name = 'in_spatial_reference'
        param_5.displayName = 'Spatial Reference'
        param_5.parameterType = 'Optional'
        param_5.direction = 'Input'
        param_5.datatype = 'Spatial Reference'
        param_5.displayOrder = 6

        # in_number_of_radials
        param_6 = arcpy.Parameter()
        param_6.name = 'in_number_of_radials'
        param_6.displayName = 'Number Of Radials'
        param_6.parameterType = 'Optional'
        param_6.direction = 'Input'
        param_6.datatype = 'Long'
        param_6.value = '8'
        param_6.displayOrder = 3

        # output_feature_class_radials
        param_7 = arcpy.Parameter()
        param_7.name = 'output_feature_class_radials'
        param_7.displayName = 'Output Feature Class (Radials)'
        param_7.parameterType = 'Required'
        param_7.direction = 'Output'
        param_7.datatype = 'Feature Class'
        param_7.value = '%scratchGDB%\\Radials'
        param_7.symbology = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                            "layers", "RangeRadials.lyrx")
        param_7.displayOrder = 5

        # in_field_table_type_name
        param_8 = arcpy.Parameter()
        param_8.name = 'in_field_table_type_name'
        param_8.displayName = 'Input Table Type Name Field'
        param_8.parameterType = 'Optional'
        param_8.direction = 'Input'
        param_8.datatype = 'Field'
        param_8.value = 'Name'
        param_8.parameterDependencies = ["in_table"]
        param_8.category = "Input Table Options"
        param_8.displayOrder = 7

        # in_field_table_minimum_range
        param_9 = arcpy.Parameter()
        param_9.name = 'in_field_table_minimum_range'
        param_9.displayName = 'Input Table Minimum Range Field'
        param_9.parameterType = 'Optional'
        param_9.direction = 'Input'
        param_9.datatype = 'Field'
        param_9.value = 'Min'
        param_9.parameterDependencies = ["in_table"]
        param_9.category = "Input Table Options"
        param_9.displayOrder = 8

        # in_field_table_maximum_range
        param_10 = arcpy.Parameter()
        param_10.name = 'in_field_table_maximum_range'
        param_10.displayName = 'Input Table Maximum Range Field'
        param_10.parameterType = 'Optional'
        param_10.direction = 'Input'
        param_10.datatype = 'Field'
        param_10.value = 'Max'
        param_10.parameterDependencies = ["in_table"]
        param_10.category = "Input Table Options"
        param_10.displayOrder = 9

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

        inputCenterFeatures = parameters[0].valueAsText
        inputTable = parameters[1].valueAsText
        inputSelectedType = parameters[2].value
        outputRingFeatures = parameters[3].valueAsText
        optionalSpatialReference = parameters[4].value
        optionalSpatialReferenceAsText = parameters[4].valueAsText
        inputNumberOfRadials = parameters[5].value
        outputRadialFeatures = parameters[6].valueAsText

        if optionalSpatialReferenceAsText == "#" or optionalSpatialReferenceAsText == '':
            optionalSpatialReference = None

        if inputNumberOfRadials == "#" or inputNumberOfRadials == "" or inputNumberOfRadials is None :
            inputNumberOfRadials = 0
            outputRadialFeatures = None

        if outputRadialFeatures == "#" or outputRadialFeatures == "" or outputRadialFeatures is None:
            inputNumberOfRadials = 0
            outputRadialFeatures = None

        # Weapon Table Options
        if (len(parameters) > 7) :
            inputTypeNameField = parameters[7].valueAsText
        if (len(parameters) > 8) :
            inputTypeMinRangeField = parameters[8].valueAsText
        if (len(parameters) > 9) :
            inputTypeMaxRangeField = parameters[9].valueAsText

        if inputTypeNameField != "#" and inputTypeNameField != "" and \
            inputTypeMinRangeField != "#" and inputTypeMinRangeField != "" and \
            inputTypeMaxRangeField != "#" and inputTypeMaxRangeField != "" :
            #get min and max range for selected weapon
            cursorFields = [inputTypeNameField, inputTypeMinRangeField, inputTypeMaxRangeField]
            with arcpy.da.SearchCursor(inputTable, cursorFields) as cursor:
                for row in cursor:
                    if str(inputSelectedType) == str(row[0]):
                        inputMinimumRange = row[1]
                        inputMaximumRange = row[2]

        # get/set environment
        arcpy.env.overwriteOutput = True

        # Call tool method
        rr = RangeRingUtils.rangeRingsFromMinMax(inputCenterFeatures,
                                                 inputMinimumRange,
                                                 inputMaximumRange,
                                                 "METERS",
                                                 inputNumberOfRadials,
                                                 outputRingFeatures,
                                                 outputRadialFeatures,
                                                 optionalSpatialReference)

        # Set output
        return rr[0], rr[1]
