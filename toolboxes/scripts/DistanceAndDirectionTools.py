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

# ----------------------------------------------------------------------------------
# RangeRingsFromInterval Tool
# ----------------------------------------------------------------------------------
class RangeRingsFromInterval(object):
    
    def __init__(self):
        self.label = u'Range Rings From Interval'
        self.description = u'Create a concentric circle from a center, with a number of rings, and the distance between rings.'
        self.category = u'Distance and Direction'
        self.canRunInBackground = False
        
    def getParameterInfo(self):
        # Input_Center_Features
        param_1 = arcpy.Parameter()
        param_1.name = u'Input_Center_Features'
        param_1.displayName = u'Input Center Features'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'        
        param_1.datatype = u'Feature Set'  # Same as u'GPFeatureRecordSetLayer'
        
        # Set the Feature Set schema
        input_layer_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                          "layers",
                                          "RangeRingInputObserversGDB.lyr")
        param_1.value = input_layer_file_path

        # Number_of_Rings
        param_2 = arcpy.Parameter()
        param_2.name = u'Number_of_Rings'
        param_2.displayName = u'Number of Rings'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Long'
        param_2.value = u'4'

        # Interval_Between_Rings
        param_3 = arcpy.Parameter()
        param_3.name = u'Interval_Between_Rings'
        param_3.displayName = u'Interval Between Rings'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Double'
        param_3.value = u'100'

        # Distance_Units
        param_4 = arcpy.Parameter()
        param_4.name = u'Distance_Units'
        param_4.displayName = u'Distance Units'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'String'
        param_4.value = u'METERS'
        param_4.filter.list = [u'METERS', u'KILOMETERS', u'MILES', u'NAUTICAL_MILES', u'FEET', u'US_SURVEY_FEET']

        # Number_of_Radials
        param_5 = arcpy.Parameter()
        param_5.name = u'Number_of_Radials'
        param_5.displayName = u'Number of Radials'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'Long'
        param_5.value = u'8'

        # Output_Ring_Features
        param_6 = arcpy.Parameter()
        param_6.name = u'Output_Ring_Features'
        param_6.displayName = u'Output Ring Features'
        param_6.parameterType = 'Required'
        param_6.direction = 'Output'
        param_6.datatype = u'Feature Class'
        param_6.value = u'%scratchGDB%\\Rings'
        param_6.symbology = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                            "layers", "RangeRings.lyr")

        # Output_Radial_Features
        param_7 = arcpy.Parameter()
        param_7.name = u'Output_Radial_Features'
        param_7.displayName = u'Output Radial Features'
        param_7.parameterType = 'Required'
        param_7.direction = 'Output'
        param_7.datatype = u'Feature Class'
        param_7.value = u'%scratchGDB%\\Radials'
        param_7.symbology = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                            "layers", "RangeRadials.lyr")

        # Spatial_Reference
        param_8 = arcpy.Parameter()
        param_8.name = u'Spatial_Reference'
        param_8.displayName = u'Spatial Reference'
        param_8.parameterType = 'Optional'
        param_8.direction = 'Input'
        param_8.datatype = u'Spatial Reference'

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
        inputNumberOfRadials = parameters[4].value
        outputRingFeatures = parameters[5].valueAsText
        outputRadialFeatures = parameters[6].valueAsText
        optionalSpatialReference = parameters[7].value
        optionalSpatialReferenceAsText = parameters[7].valueAsText

        if optionalSpatialReferenceAsText == "#" or optionalSpatialReferenceAsText == "":
            optionalSpatialReference = None

        # WORKAROUND (for Pro): clear layer selection (since last point is selected)
        # So tool will work on all points entered
        featureSetDescribe = arcpy.Describe(inputCenterFeatures)
        if sys.version_info >= (3, 0) and (featureSetDescribe.dataType == "FeatureLayer"):
            arcpy.SelectLayerByAttribute_management(inputCenterFeatures, "CLEAR_SELECTION")

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

    def __init__(self):
        self.label = u'Range Rings From Minimum And Maximum'
        self.description = u'Create a concentric circle from a center with two rings depicting a minimum range and a maximum range.'
        self.category = u'Distance and Direction'
        self.canRunInBackground = False

    def getParameterInfo(self):
        # Input_Center_Features
        param_1 = arcpy.Parameter()
        param_1.name = u'Input_Center_Features'
        param_1.displayName = u'Input Center Features'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Feature Set'

        # Set the Feature Set schema
        input_layer_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                          "layers",
                                          "RangeRingInputObserversGDB.lyr")
        param_1.value = input_layer_file_path

        # Minimum_Range
        param_2 = arcpy.Parameter()
        param_2.name = u'Minimum_Range'
        param_2.displayName = u'Minimum Range'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Double'
        param_2.value = u'10'

        # Maximum_Range
        param_3 = arcpy.Parameter()
        param_3.name = u'Maximum_Range'
        param_3.displayName = u'Maximum Range'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Double'
        param_3.value = u'100'

        # Distance_Units
        param_4 = arcpy.Parameter()
        param_4.name = u'Distance_Units'
        param_4.displayName = u'Distance Units'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'String'
        param_4.value = u'METERS'
        param_4.filter.list = [u'METERS', u'KILOMETERS', u'MILES', u'NAUTICAL_MILES', u'FEET', u'US_SURVEY_FEET']

        # Number_of_Radials
        param_5 = arcpy.Parameter()
        param_5.name = u'Number_of_Radials'
        param_5.displayName = u'Number of Radials'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'Long'
        param_5.value = u'8'

        # Output_Ring_Features
        param_6 = arcpy.Parameter()
        param_6.name = u'Output_Ring_Features'
        param_6.displayName = u'Output Ring Features'
        param_6.parameterType = 'Required'
        param_6.direction = 'Output'
        param_6.datatype = u'Feature Class'
        param_6.value = u'%scratchGDB%\\rings'
        param_6.symbology = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                            "layers", "RangeRings.lyr")

        # Output_Radial_Features
        param_7 = arcpy.Parameter()
        param_7.name = u'Output_Radial_Features'
        param_7.displayName = u'Output Radial Features'
        param_7.parameterType = 'Required'
        param_7.direction = 'Output'
        param_7.datatype = u'Feature Class'
        param_7.value = u'%scratchGDB%\\radials'
        param_7.symbology = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                            "layers", "RangeRadials.lyr")

        # Spatial_Reference
        param_8 = arcpy.Parameter()
        param_8.name = u'Spatial_Reference'
        param_8.displayName = u'Spatial Reference'
        param_8.parameterType = 'Optional'
        param_8.direction = 'Input'
        param_8.datatype = u'Spatial Reference'

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
        inputNumberOfRadials = parameters[4].value
        outputRingFeatures = parameters[5].valueAsText
        outputRadialFeatures = parameters[6].valueAsText
        optionalSpatialReference = parameters[7].value
        optionalSpatialReferenceAsText = parameters[7].valueAsText

        if optionalSpatialReferenceAsText == "#" or optionalSpatialReferenceAsText == "":
            optionalSpatialReference = None

        # WORKAROUND (for Pro): clear layer selection (since last point is selected)
        # So tool will work on all points entered
        featureSetDescribe = arcpy.Describe(inputCenterFeatures)
        if sys.version_info >= (3, 0) and (featureSetDescribe.dataType == "FeatureLayer"):
            arcpy.SelectLayerByAttribute_management(inputCenterFeatures, "CLEAR_SELECTION")

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
    
            # Input Center Features (Feature Set) [0]
            # Input Table (Table) [1]
            # Selected Type (String) [2]
            # Number of Radials (Long) [3]
            # Output Ring Features (Feature Class) [4]
            # Output Radial Features (Feature Class) [5]
            # Spatial Reference (Spatial Reference) [6]
            # Input Table Type Name Field (Field) [7]
            # Input Table Minimum Range Field (Field) [8]
            # Input Table Maximum Range Field (Field) [9]

            inputParamsTable = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                          "tooldata", "Range Rings.gdb", "rrInputTable")
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
                msg = r"ERROR LOADING INPUT TABLE!!"
                Names.append(msg)
                messages.AddErrorMessage(msg)
            return Names

    def __init__(self):
        self.label = u'Range Rings From Minimum And Maximum Table'
        self.description = u'Create a concentric circle from a center with two rings depicting a minimum range and a maximum range from a table.'
        self.category = u'Distance and Direction'
        self.canRunInBackground = False

    def getParameterInfo(self):

        # Input_Center_Features
        param_1 = arcpy.Parameter()
        param_1.name = u'Input_Center_Features'
        param_1.displayName = u'Input Center Features'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Feature Set'
        # Set the Feature Set schema
        input_layer_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                          "layers",
                                          "RangeRingInputObserversGDB.lyr")
        param_1.value = input_layer_file_path

        # Input_Table
        param_2 = arcpy.Parameter()
        param_2.name = u'Input_Table'
        param_2.displayName = u'Input Table'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Table'
        # military-tools-geoprocessing-toolbox\\toolboxes\\tooldata\\Range
        # Rings.gdb\\rrInputTable'
        param_2.value = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                          "tooldata", "Range Rings.gdb", "rrInputTable")

        # Selected_Type
        param_3 = arcpy.Parameter()
        param_3.name = u'Selected_Type'
        param_3.displayName = u'Selected Type'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'String'
        param_3.value = u'M4'
        param_3.filter.list = [u'M4', u'M249']

        # Number_Of_Radials
        param_4 = arcpy.Parameter()
        param_4.name = u'Number_Of_Radials'
        param_4.displayName = u'Number Of Radials'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'Long'
        param_4.value = u'8'

        # Output_Ring_Features
        param_5 = arcpy.Parameter()
        param_5.name = u'Output_Ring_Features'
        param_5.displayName = u'Output Ring Features'
        param_5.parameterType = 'Required'
        param_5.direction = 'Output'
        param_5.datatype = u'Feature Class'
        param_5.value = u'%scratchGDB%\\Rings'
        param_5.symbology = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                            "layers", "RangeRings.lyr")

        # Output_Radial_Features
        param_6 = arcpy.Parameter()
        param_6.name = u'Output_Radial_Features'
        param_6.displayName = u'Output Radial Features'
        param_6.parameterType = 'Required'
        param_6.direction = 'Output'
        param_6.datatype = u'Feature Class'
        param_6.value = u'%scratchGDB%\\Radials'
        param_6.symbology = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                            "layers", "RangeRadials.lyr")

        # Spatial_Reference
        param_7 = arcpy.Parameter()
        param_7.name = u'Spatial_Reference'
        param_7.displayName = u'Spatial Reference'
        param_7.parameterType = 'Optional'
        param_7.direction = 'Input'
        param_7.datatype = u'Spatial Reference'

        # Input_Table_Type_Name_Field
        param_8 = arcpy.Parameter()
        param_8.name = u'Input_Table_Type_Name_Field'
        param_8.displayName = u'Input Table Type Name Field'
        param_8.parameterType = 'Optional'
        param_8.direction = 'Input'
        param_8.datatype = u'Field'
        param_8.value = u'Name'
        param_8.parameterDependencies = ["Input_Table"]
        param_8.category = "Input Table Options"

        # Input_Table_Minimum_Range_Field
        param_9 = arcpy.Parameter()
        param_9.name = u'Input_Table_Minimum_Range_Field'
        param_9.displayName = u'Input Table Minimum Range Field'
        param_9.parameterType = 'Optional'
        param_9.direction = 'Input'
        param_9.datatype = u'Field'
        param_9.value = u'Min'
        param_9.parameterDependencies = ["Input_Table"]
        param_9.category = "Input Table Options"

        # Input_Table_Maximum_Range_Field
        param_10 = arcpy.Parameter()
        param_10.name = u'Input_Table_Maximum_Range_Field'
        param_10.displayName = u'Input Table Maximum Range Field'
        param_10.parameterType = 'Optional'
        param_10.direction = 'Input'
        param_10.datatype = u'Field'
        param_10.value = u'Max'
        param_10.parameterDependencies = ["Input_Table"]
        param_10.category = "Input Table Options"

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
        inputNumberOfRadials = parameters[3].value
        outputRingFeatures = parameters[4].valueAsText
        outputRadialFeatures = parameters[5].valueAsText
        optionalSpatialReference = parameters[6].value
        optionalSpatialReferenceAsText = parameters[6].valueAsText

        if optionalSpatialReferenceAsText == "#" or optionalSpatialReferenceAsText == '':
            optionalSpatialReference = None

        # WORKAROUND (for Pro): clear layer selection (since last point is selected)
        # So tool will work on all points entered
        featureSetDescribe = arcpy.Describe(inputCenterFeatures)
        if sys.version_info >= (3, 0) and (featureSetDescribe.dataType == "FeatureLayer"):
            arcpy.SelectLayerByAttribute_management(inputCenterFeatures, "CLEAR_SELECTION")

        #Weapon Table Options
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
