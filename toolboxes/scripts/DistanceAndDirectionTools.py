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
import arcpy

try:
    from . import RangeRingUtils
except ImportError:
    import RangeRingUtils

class RangeRingsFromInterval(object):

    """
    
    """
    
    def __init__(self):
        self.label = u'Range Rings From Interval'
        self.description = u'Create a concentric circle from a center, with a number of rings, and the distance between rings.'
        self.category = "Distance and Direction"        
        self.canRunInBackground = False
        
    def getParameterInfo(self):
        # Input_Center_Features
        param_1 = arcpy.Parameter()
        param_1.name = u'Input_Center_Features'
        param_1.displayName = u'Input Center Features'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        
        param_1.datatype = u'Feature Set'
        # param_1.datatype = u'GPFeatureRecordSetLayer'
        
        input_layer_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                          "layers",
                                          "RelativeGRGInputPoint.lyr")
                                          # "RangeRingInputObservers.lyrx")
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

        inputCenterFeatures = parameters[0].value
        inputNumberOfRings = parameters[1].value
        inputDistanceBetween = parameters[2].value
        inputDistanceUnits = parameters[3].value
        inputNumberOfRadials = parameters[4].value
        outputRingFeatures = parameters[5].value
        outputRadialFeatures = parameters[6].value
        optionalSpatialReference = parameters[7].value
        optionalSpatialReferenceAsText = str(parameters[7].value)

        # WORKAROUND (for Pro): clear layer selection (since last point is selected)
        # So tool will work on all points entered 
        arcpy.SelectLayerByAttribute_management(inputCenterFeatures, "CLEAR_SELECTION", None, None)

        if optionalSpatialReferenceAsText == "#" or optionalSpatialReferenceAsText == "":
            optionalSpatialReference = None

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
