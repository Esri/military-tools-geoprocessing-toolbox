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
 VisTools.py
 --------------------------------------------------
 requirements: ArcGIS 10.3.1+, ArcGIS Pro 1.4+, Python 2.7 or Python 3.5+
 author: ArcGIS Solutions
 contact: support@esri.com
 company: Esri
 ==================================================
 description:
 Visibility Tool logic module.
 ==================================================
'''

import os
import arcpy
import sys
import traceback

try:
    from . import VisibilityUtilities
except ImportError:
    import VisibilityUtilities

class AddLinearLineOfSightFields(object):
    '''
     Adds an OFFSET field and user-defined/default value to
     an input Observer and input Target features.
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

            # 0 - Input Observer Features
            # 1 - Observer Height Above Surface
            # 2 - Input Target Features
            # 3 - Target Height Above Surface
            # 4 - Output Observer Features
            # 5 - Output Target Features

            return

        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""
            return

        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""
            msgWarnLessThanZero = r"Values less than zero may produce unexpected results."
            if self.params[1].altered:
                if self.params[1].value < 0.0:
                    self.params[1].setWarningMessage(msgWarnLessThanZero)
            if self.params[3].altered:
                if self.params[3].value < 0.0:
                    self.params[3].setWarningMessage(msgWarnLessThanZero)
            return

    def __init__(self):
        '''
        Add LLOS Fields tool constructor method
        '''
        self.label = "Add LLOS Fields"
        self.description = "Adds an OFFSET field and user-defined/default value to an input Observer and input Target features."
        self.category = "Visibility"
        self.canRunInBackground = False

    def getParameterInfo(self):
        '''
        Define parameter definitions
        '''

        # Input_Observer_Features
        param_1 = arcpy.Parameter()
        param_1.name = u'Input_Observer_Features'
        param_1.displayName = u'Input Observer Features'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Feature Layer'

        # Observer_Height_Above_Surface
        param_2 = arcpy.Parameter()
        param_2.name = u'Observer_Height_Above_Surface'
        param_2.displayName = u'Observer Height Above Surface'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Double'
        param_2.value = u'2.0'

        # Input_Target_Features
        param_3 = arcpy.Parameter()
        param_3.name = u'Input_Target_Features'
        param_3.displayName = u'Input Target Features'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Feature Layer'

        # Target_Height_Above_Surface
        param_4 = arcpy.Parameter()
        param_4.name = u'Target_Height_Above_Surface'
        param_4.displayName = u'Target Height Above Surface'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'Double'
        param_4.value = u'0.0'

        # Output_Observer_Features
        param_5 = arcpy.Parameter()
        param_5.name = u'Output_Observer_Features'
        param_5.displayName = u'Output Observer Features'
        param_5.parameterType = 'Derived'
        param_5.direction = 'Output'
        param_5.datatype = u'Feature Class'
        param_5.parameterDependencies = ['Input_Observer_Features']

        # Output_Target_Features
        param_6 = arcpy.Parameter()
        param_6.name = u'Output_Target_Features'
        param_6.displayName = u'Output Target Features'
        param_6.parameterType = 'Derived'
        param_6.direction = 'Output'
        param_6.datatype = u'Feature Class'
        param_6.parameterDependencies = ['Input_Target_Features']

        return [param_1, param_2, param_3, param_4, param_5, param_6]

    def updateParameters(self, parameters):
        '''
        Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed.
        '''
        validator = getattr(self, 'ToolValidator', None)
        if validator:
             return validator(parameters).updateParameters()

    def updateMessages(self, parameters):
        validator = getattr(self, 'ToolValidator', None)
        if validator:
             return validator(parameters).updateMessages()

    def execute(self, parameters, messages):
        ''' execute for toolbox'''

        inputObserverFeatures = parameters[0].valueAsText
        inputObserverHeight   = parameters[1].value
        inputTargetFeatures   = parameters[2].valueAsText
        inputTargetHeight     = parameters[3].value

        out_LLOS_added = VisibilityUtilities.addLLOSFields(inputObserverFeatures,
                                           inputObserverHeight,
                                           inputTargetFeatures,
                                           inputTargetHeight)

        return out_LLOS_added[0], out_LLOS_added[1]


class AddRadialLineOfSightObserverFields(object):
    '''
    Adds Observer fields and values to inputFeatures:
    OFFSETA: observer offset height above surface, default is 2.0
    OFFSETB: surface offset, default is 0.0
    RADIUS1: Near distance, default is 0.0
    RADIUS2: Farthest distance, default is 1000.0
    AZIMUTH1: Left Azimuth in horizontal field of view, default is 0.0
    AZIMUTH2: Right Azimuth in horizontal field of view, default is 360.0
    VERT1: Top Angle in vertical field of view, default is 90.0
    VERT2: Bottom Angle in vertical field of view, default is -90.0
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

            # 0 - Input Observer Features
            # 1 - Observer Offset
            # 2 - Surface Offset
            # 3 - Minimum Distance Radius
            # 4 - Maximum Distance Radius
            # 5 - Left Bearing Azimuth
            # 6 - Right Bearing Azimuth
            # 7 - Top Vertical Angle
            # 8 - Bottom Vertical Angle
            # 9 - Output Observer Features
            return

        def updateParameters(self):
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""
            # 0 - Input Observer Features
            # 1 - Observer Offset
            # 2 - Surface Offset
            # 3 - Minimum Distance Radius
            # 4 - Maximum Distance Radius
            # 5 - Left Bearing Azimuth
            # 6 - Right Bearing Azimuth
            # 7 - Top Vertical Angle
            # 8 - Bottom Vertical Angle
            # 9 - Output Observer Features
            return

        def updateMessages(self):
            """Modify the messages created by internal validation for each tool
            parameter.  This method is called after internal validation."""

            msgWarnLessThanZero = r"Value less than zero may produce unexpected results."
            msgErrorLessThanZero = r"Values must be greater than zero."
            msgErrorMaxDistGreater = r"Maximum Distance Radius value must be greater than Minimum Distance Radius value."
            msgErrorRightAzimGreater = r"Right Bearing Azimuth must be greater than Left Bearing Azimuth."
            msgErrorTopVertGreater = r"Top Vertical Angle must be greater than Bottom Vertical Angle."
            msgErrorHFOVRange = r"Azimuth/Bearing values must be between 0 and 360."
            msgErrorVFOVRange = r"Vertical Angles must be between 90 and -90."

            # 0 - Input Observer Features
            # 1 - Observer Offset
            if self.params[1].altered:
                if self.params[1].value < 0.0:
                    self.params[1].setWarningMessage(msgWarnLessThanZero)

            # 2 - Surface Offset
            if self.params[2].altered:
                if self.params[2].value < 0.0:
                    self.params[2].setErrorMessage(msgErrorLessThanZero)

            # 3 - Minimum Distance Radius
            if self.params[3].altered:
                if self.params[3].value < 0.0:
                    self.params[3].setErrorMessage(msgErrorLessThanZero)
                if self.params[3].value >= self.params[4].value:
                    self.params[3].setErrorMessage(msgErrorMaxDistGreater)

            # 4 - Maximum Distance Radius
            if self.params[4].altered:
                if self.params[4].value < 0.0:
                    self.params[4].setErrorMessage(msgErrorLessThanZero)
                if self.params[3].value >= self.params[4].value:
                    self.params[4].setErrorMessage(msgErrorMaxDistGreater)

            # 5 - Left Bearing Azimuth
            if self.params[5].altered:
                if self.params[5].value < 0.0 or self.params[5].value > 360.0:
                    self.params[5].setErrorMessage(msgErrorHFOVRange)
                if self.params[5].value >= self.params[6].value:
                    self.params[5].setErrorMessage(msgErrorRightAzimGreater)

            # 6 - Right Bearing Azimuth
            if self.params[6].altered:
                if self.params[6].value < 0.0 or self.params[6].value > 360.0:
                    self.params[6].setErrorMessage(msgErrorHFOVRange)
                if self.params[5].value >= self.params[6].value:
                    self.params[6].setErrorMessage(msgErrorRightAzimGreater)

            # 7 - Top Vertical Angle
            if self.params[7].altered:
                if self.params[7].value < -90.0 or self.params[7].value > 90.0:
                    self.params[7].setErrorMessage(msgErrorVFOVRange)
                if self.params[7].value <= self.params[8].value:
                    self.params[7].setErrorMessage(msgErrorTopVertGreater)

            # 8 - Bottom Vertical Angle
            if self.params[8].altered:
                if self.params[8].value < -90.0 or self.params[8].value > 90.0:
                    self.params[8].setErrorMessage(msgErrorVFOVRange)
                if self.params[7].value <= self.params[8].value:
                    self.params[8].setErrorMessage(msgErrorTopVertGreater)

            # 9 - Output Observer Features
            return

    def __init__(self):
        '''
        Add RLOS Fields tool constructor method
        '''
        self.label = "Add RLOS Fields"
        self.description = "Adds Observer fields and values to inputFeatures."
        self.category = "Visibility"
        self.canRunInBackground = False

    def getParameterInfo(self):
        # Input_Observer_Features
        input_observer_features = arcpy.Parameter()
        input_observer_features.name = 'input_observer_features'
        input_observer_features.displayName = 'Input Observer Features'
        input_observer_features.parameterType = 'Required'
        input_observer_features.direction = 'Input'
        input_observer_features.datatype = 'Feature Layer'

        # Observer_Offset
        input_OFFSETA = arcpy.Parameter()
        input_OFFSETA.name = 'Observer_Offset'
        input_OFFSETA.displayName = 'Observer Offset'
        input_OFFSETA.parameterType = 'Required'
        input_OFFSETA.direction = 'Input'
        input_OFFSETA.datatype = 'Double'
        input_OFFSETA.value = '2'

        # Surface_Offset
        input_OFFSETB = arcpy.Parameter()
        input_OFFSETB.name = 'Surface_Offset'
        input_OFFSETB.displayName = 'Surface Offset'
        input_OFFSETB.parameterType = 'Required'
        input_OFFSETB.direction = 'Input'
        input_OFFSETB.datatype = 'Double'
        input_OFFSETB.value = '0'

        # Minimum_Distance_Radius
        input_RADIUS1 = arcpy.Parameter()
        input_RADIUS1.name = 'Minimum_Distance_Radius'
        input_RADIUS1.displayName = 'Minimum Distance Radius'
        input_RADIUS1.parameterType = 'Required'
        input_RADIUS1.direction = 'Input'
        input_RADIUS1.datatype = 'Double'
        input_RADIUS1.value = '0'

        # Maximum_Distance_Radius
        input_RADIUS2 = arcpy.Parameter()
        input_RADIUS2.name = 'Maximum_Distance_Radius'
        input_RADIUS2.displayName = 'Maximum Distance Radius'
        input_RADIUS2.parameterType = 'Required'
        input_RADIUS2.direction = 'Input'
        input_RADIUS2.datatype = 'Double'
        input_RADIUS2.value = '1000'

        # Left_Bearing_Azimuth
        input_AZIMUTH1 = arcpy.Parameter()
        input_AZIMUTH1.name = 'Left_Bearing_Azimuth'
        input_AZIMUTH1.displayName = 'Left Bearing Azimuth'
        input_AZIMUTH1.parameterType = 'Required'
        input_AZIMUTH1.direction = 'Input'
        input_AZIMUTH1.datatype = 'Double'
        input_AZIMUTH1.value = '0'

        # Right_Bearing_Azimuth
        input_AZIMUTH2 = arcpy.Parameter()
        input_AZIMUTH2.name = 'Right_Bearing_Azimuth'
        input_AZIMUTH2.displayName = 'Right Bearing Azimuth'
        input_AZIMUTH2.parameterType = 'Required'
        input_AZIMUTH2.direction = 'Input'
        input_AZIMUTH2.datatype = 'Double'
        input_AZIMUTH2.value = '360'

        # Top_Vertical_Angle
        input_VERT1 = arcpy.Parameter()
        input_VERT1.name = 'Top_Vertical_Angle'
        input_VERT1.displayName = 'Top Vertical Angle'
        input_VERT1.parameterType = 'Required'
        input_VERT1.direction = 'Input'
        input_VERT1.datatype = 'Double'
        input_VERT1.value = '90'

        # Bottom_Vertical_Angle
        input_VERT2 = arcpy.Parameter()
        input_VERT2.name = 'Bottom_Vertical_Angle'
        input_VERT2.displayName = 'Bottom Vertical Angle'
        input_VERT2.parameterType = 'Required'
        input_VERT2.direction = 'Input'
        input_VERT2.datatype = 'Double'
        input_VERT2.value = '-90'

        # Output_Observer_Features
        output_observer_features = arcpy.Parameter()
        output_observer_features.name = 'Output_Observer_Features'
        output_observer_features.displayName = 'Output Observer Features'
        output_observer_features.parameterType = 'Derived'
        output_observer_features.direction = 'Output'
        output_observer_features.datatype = 'Feature Class'

        return [input_observer_features,
                input_OFFSETA,
                input_OFFSETB,
                input_RADIUS1,
                input_RADIUS2,
                input_AZIMUTH1,
                input_AZIMUTH2,
                input_VERT1,
                input_VERT2,
                output_observer_features]

    def updateParameters(self, parameters):
        '''
        Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed.
        '''
        validator = getattr(self, 'ToolValidator', None)
        if validator:
             return validator(parameters).updateParameters()


    def updateMessages(self, parameters):
        validator = getattr(self, 'ToolValidator', None)
        if validator:
             return validator(parameters).updateMessages()

    def execute(self, parameters, messages):
        ''' execute for toolbox'''

        # get/set environment
        arcpy.env.overwriteOutput = True

        inputObserverFeatures = parameters[0].valueAsText
        inputOFFSETA = parameters[1].value
        inputOFFSETB = parameters[2].value
        inputRADIUS1 = parameters[3].value
        inputRADIUS2 = parameters[4].value
        inputAZIMUTH1 = parameters[5].value
        inputAZIMUTH2 = parameters[6].value
        inputVERT1 = parameters[7].value
        inputVERT2 = parameters[8].value

        out_RLOS_added = VisibilityUtilities.addRLOSObserverFields(inputObserverFeatures,
                                                                    inputOFFSETA,
                                                                    inputOFFSETB,
                                                                    inputRADIUS1,
                                                                    inputRADIUS2,
                                                                    inputAZIMUTH1,
                                                                    inputAZIMUTH2,
                                                                    inputVERT1,
                                                                    inputVERT2)

        return out_RLOS_added

class RadialLineOfSightAndRange(object):

    def __init__(self):
        self.label = u'Radial Line Of Sight And Range'
        self.description = u'Shows visible areas to one or more observers. Shows the areas visible (green) and not visible (red) to an observer at a specified distance and viewing angle.'
        self.category = "Visibility"
        self.canRunInBackground = False

    def getParameterInfo(self):
        # Input_Observer
        param_1 = arcpy.Parameter()
        param_1.name = u'Input_Observer'
        param_1.displayName = u'Input Observer'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Feature Set'
        # Set the Feature Set schema
        input_layer_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                          "layers",
                                          "RangeRingInputObserversGDB.lyr")
        param_1.value = input_layer_file_path

        # Input_Surface
        param_2 = arcpy.Parameter()
        param_2.name = u'Input_Surface'
        param_2.displayName = u'Input Surface'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Raster Layer'

        # Near_Distance__RADIUS1_
        param_3 = arcpy.Parameter()
        param_3.name = u'Near_Distance__RADIUS1_'
        param_3.displayName = u'Near Distance (RADIUS1)'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'String'
        param_3.value = u'1000'

        # Maximum_Distance__RADIUS2_
        param_4 = arcpy.Parameter()
        param_4.name = u'Maximum_Distance__RADIUS2_'
        param_4.displayName = u'Maximum Distance (RADIUS2)'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'String'
        param_4.value = u'3000'

        # Left_Azimuth__AZIMUTH1_
        param_5 = arcpy.Parameter()
        param_5.name = u'Left_Azimuth__AZIMUTH1_'
        param_5.displayName = u'Left Azimuth (AZIMUTH1)'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'String'
        param_5.value = u'40'

        # Right_Azimuth__AZIMUTH2_
        param_6 = arcpy.Parameter()
        param_6.name = u'Right_Azimuth__AZIMUTH2_'
        param_6.displayName = u'Right Azimuth (AZIMUTH2)'
        param_6.parameterType = 'Required'
        param_6.direction = 'Input'
        param_6.datatype = u'String'
        param_6.value = u'120'

        # Observer_Offset__OFFSETA_
        param_7 = arcpy.Parameter()
        param_7.name = u'Observer_Offset__OFFSETA_'
        param_7.displayName = u'Observer Offset (OFFSETA)'
        param_7.parameterType = 'Required'
        param_7.direction = 'Input'
        param_7.datatype = u'String'
        param_7.value = u'20'

        # Output_Viewshed
        param_8 = arcpy.Parameter()
        param_8.name = u'Output_Viewshed'
        param_8.displayName = u'Output Viewshed'
        param_8.parameterType = 'Required'
        param_8.direction = 'Output'
        param_8.datatype = u'Feature Class'
        param_8.value = u'in_memory\\Viewshed'
        param_8.symbology = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                            "layers", "Radial Line Of Sight Output.lyr")

        # Output_Wedge
        param_9 = arcpy.Parameter()
        param_9.name = u'Output_Wedge'
        param_9.displayName = u'Ouput Field of View'
        param_9.parameterType = 'Required'
        param_9.direction = 'Output'
        param_9.datatype = u'Feature Class'
        param_9.value = u'in_memory\\Field_Of_View'
        param_9.symbology = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                            "layers", "RLOSPieWedge.lyr")

        # Output_FullWedge
        param_10 = arcpy.Parameter()
        param_10.name = u'Output_FullWedge'
        param_10.displayName = u'Output Range'
        param_10.parameterType = 'Required'
        param_10.direction = 'Output'
        param_10.datatype = u'Feature Class'
        param_10.value = u'in_memory\\Range'
        param_10.symbology = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                            "layers", "RLOSDonutWedge.lyr")

        return [param_1, param_2, param_3, param_4, param_5, param_6, param_7, param_8, param_9, param_10]

    def isLicensed(self):
        return arcpy.CheckExtension("3D") == "Available"

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
            from . import RadialLineOfSightAndRange
        except ImportError:
            import RadialLineOfSightAndRange

        inputObserverPoints = parameters[0].valueAsText
        elevationRaster     = parameters[1].valueAsText
        innerRadiusInput    = parameters[2].valueAsText
        outerRadiusInput    = parameters[3].valueAsText
        leftAzimuthInput    = parameters[4].valueAsText
        rightAzimuthInput   = parameters[5].valueAsText
        observerOffsetInput = parameters[6].valueAsText
        viewshed    = parameters[7].valueAsText
        sectorWedge = parameters[8].valueAsText
        fullWedge   = parameters[9].valueAsText

        # WORKAROUND (for Pro): clear layer selection (since last point is selected)
        # So tool will work on all points entered
        featureSetDescribe = arcpy.Describe(inputObserverPoints)
        if sys.version_info >= (3, 0) and (featureSetDescribe.dataType == "FeatureLayer"):
            arcpy.SelectLayerByAttribute_management(inputObserverPoints, "CLEAR_SELECTION")

        RadialLineOfSightAndRange.createViewshed(inputObserverPoints, elevationRaster, \
            outerRadiusInput, leftAzimuthInput, rightAzimuthInput, observerOffsetInput, \
            innerRadiusInput, viewshed, sectorWedge, fullWedge)

        return viewshed, sectorWedge, fullWedge

class LinearLineOfSight(object):

    def __init__(self):
        self.label = u'Linear Line Of Sight'
        self.description = u'Creates line(s) of sight between observers and targets.'
        self.canRunInBackground = False
        self.category = "Visibility"

    def getParameterInfo(self):
        # Observers
        param_1 = arcpy.Parameter()
        param_1.name = u'Observers'
        param_1.displayName = u'Observers'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Feature Set'
        input_layer_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                          "layers",
                                          "LLOS_InputObserversGDB.lyr")
        param_1.value = input_layer_file_path

        # Observer_Height_Above_Surface
        param_2 = arcpy.Parameter()
        param_2.name = u'Observer_Height_Above_Surface'
        param_2.displayName = u'Observer Height Above Surface'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Double'
        param_2.value = u'2'

        # Targets
        param_3 = arcpy.Parameter()
        param_3.name = u'Targets'
        param_3.displayName = u'Targets'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Feature Set'
        input_layer_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                          "layers",
                                          "LLOS_InputTargetsGDB.lyr")
        param_3.value = input_layer_file_path

        # Target_Height_Above_Surface
        param_4 = arcpy.Parameter()
        param_4.name = u'Target_Height_Above_Surface'
        param_4.displayName = u'Target Height Above Surface'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'Double'
        param_4.value = u'0'

        # Input_Elevation_Surface
        param_5 = arcpy.Parameter()
        param_5.name = u'Input_Elevation_Surface'
        param_5.displayName = u'Input Elevation Surface'
        param_5.parameterType = 'Required'
        param_5.direction = 'Input'
        param_5.datatype = u'Raster Layer'

        # Output_Line_Of_Sight_Features
        param_6 = arcpy.Parameter()
        param_6.name = u'Output_Line_Of_Sight_Features'
        param_6.displayName = u'Output Line Of Sight Features'
        param_6.parameterType = 'Required'
        param_6.direction = 'Output'
        param_6.datatype = u'Feature Class'
        param_6.value = u'%scratchGDB%/outputLOS'
        param_6.symbology = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                            "layers", "LLOS_OutputLLOS.lyr")

        # Output_Sight_Line_Features
        param_7 = arcpy.Parameter()
        param_7.name = u'Output_Sight_Line_Features'
        param_7.displayName = u'Output Sight Line Features'
        param_7.parameterType = 'Required'
        param_7.direction = 'Output'
        param_7.datatype = u'Feature Class'
        param_7.value = u'%scratchGDB%/outputSightLines'
        param_7.symbology = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                            "layers", "LLOS_OutputSightLines.lyr")

        # Output_Observer_Features
        param_8 = arcpy.Parameter()
        param_8.name = u'Output_Observer_Features'
        param_8.displayName = u'Output Observer Features'
        param_8.parameterType = 'Required'
        param_8.direction = 'Output'
        param_8.datatype = u'Feature Class'
        param_8.value = u'%scratchGDB%/outputObservers'
        param_8.symbology = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                            "layers", "LLOS_Output_Observers.lyr")

        # Output_Target_Features
        param_9 = arcpy.Parameter()
        param_9.name = u'Output_Target_Features'
        param_9.displayName = u'Output Target Features'
        param_9.parameterType = 'Required'
        param_9.direction = 'Output'
        param_9.datatype = u'Feature Class'
        param_9.value = u'%scratchGDB%/outputTargets'
        param_9.symbology = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                            "layers", "LLOS_Output_Targets.lyr")

        # Input_Obstruction_Features
        param_10 = arcpy.Parameter()
        param_10.name = u'Input_Obstruction_Features'
        param_10.displayName = u'Input Obstruction Features'
        param_10.parameterType = 'Optional'
        param_10.direction = 'Input'
        param_10.datatype = u'Feature Layer'

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

        inputObserverFeatures = parameters[0].valueAsText # 0 - Observers
        inputObserverHeight = parameters[1].value # 1 - Observer Height Above Surface
        inputTargetFeatures = parameters[2].valueAsText # 2 - Targets
        inputTargetHeight = parameters[3].value # 3 - Target Height Above Surface
        inputSurface = parameters[4].valueAsText # 4 - Input Elevation Surface
        outputLineOfSight = parameters[5].valueAsText # 5 - Output Line Of Sight Features
        outputSightLines = parameters[6].valueAsText # 6 - Output Sight Lines
        outputObservers = parameters[7].valueAsText # 7 - Output Observers
        outputTargets = parameters[8].valueAsText # 8 - Output Targets
        inputObstructionFeatures = parameters[9].valueAsText # 9 - Input Obstruction Features - optional

        arcpy.env.overwriteOutput = True

        llos = VisibilityUtilities.linearLineOfSight(inputObserverFeatures,
                                                inputObserverHeight,
                                                inputTargetFeatures,
                                                inputTargetHeight,
                                                inputSurface,
                                                outputLineOfSight,
                                                outputSightLines,
                                                outputObservers,
                                                outputTargets,
                                                inputObstructionFeatures)
        if llos == None:
            return None

        # Set output
        return llos[0],llos[1],llos[2],llos[3]

class RadialLineOfSight(object):

    def __init__(self):
        self.label = u'Radial Line Of Sight'
        self.description = u'Shows the areas visible (green) and not visible (red) to an observer at a specified distance and viewing angle.'
        self.canRunInBackground = False
        self.category = "Visibility"

    def getParameterInfo(self):

        # Input_Observer_Features
        param_1 = arcpy.Parameter()
        param_1.name = u'Input_Observer_Features'
        param_1.displayName = u'Input Observer Features'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = u'Feature Set'
        input_layer_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                          "layers",
                                          "LLOS_InputObserversGDB.lyr")
        param_1.value = input_layer_file_path

        # Observer_Height_Above_Surface
        param_2 = arcpy.Parameter()
        param_2.name = u'Observer_Height_Above_Surface'
        param_2.displayName = u'Observer Height Above Surface'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = u'Double'
        param_2.value = u'2'

        # Radius_Of_Observer
        param_3 = arcpy.Parameter()
        param_3.name = u'Radius_Of_Observer'
        param_3.displayName = u'Radius Of Observer'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = u'Double'
        param_3.value = u'1000'

        # Input_Surface
        param_4 = arcpy.Parameter()
        param_4.name = u'Input_Surface'
        param_4.displayName = u'Input Surface'
        param_4.parameterType = 'Required'
        param_4.direction = 'Input'
        param_4.datatype = u'Raster Layer'

        # Output_Visibility
        param_5 = arcpy.Parameter()
        param_5.name = u'Output_Visibility'
        param_5.displayName = u'Output Visibility'
        param_5.parameterType = 'Required'
        param_5.direction = 'Output'
        param_5.datatype = u'Feature Class'
        param_5.value = u'%scratchGDB%/outputRLOS'
        param_5.symbology = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                            "layers", "Radial Line Of Sight Output.lyr")

        # Force_Visibility_To_Infinity__Edge_Of_Surface_
        param_6 = arcpy.Parameter()
        param_6.name = u'Force_Visibility_To_Infinity__Edge_Of_Surface_'
        param_6.displayName = u'Force Visibility To Infinity (Edge Of Surface)'
        param_6.parameterType = 'Optional'
        param_6.direction = 'Input'
        param_6.datatype = u'Boolean'

        # Spatial_Reference
        param_7 = arcpy.Parameter()
        param_7.name = u'Spatial_Reference'
        param_7.displayName = u'Spatial Reference'
        param_7.parameterType = 'Optional'
        param_7.direction = 'Input'
        param_7.datatype = u'Spatial Reference'
        param_7.value = arcpy.SpatialReference(54032).exportToString() # World Azimuthal Equidistant

        return [param_1, param_2, param_3, param_4, param_5, param_6, param_7]

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

        inputObserverFeatures = parameters[0].valueAsText # Input Observer Features
        inputObserverHeight = parameters[1].value # Observer Height Above Surface
        inputRadiusOfObserver = parameters[2].value # Radius Of Observer
        inputSurface = parameters[3].valueAsText # Input Surface
        outputVisibility = parameters[4].valueAsText # Output Visibility
        inputForceVisibility = parameters[5].value # Force Visibility To Infinity (Edge of Surace)
        inputSpatialReference = parameters[6].value # Spatial Reference
        inputSpatialReferenceAsText = parameters[6].valueAsText

        if inputSpatialReferenceAsText == "#" or inputSpatialReferenceAsText == '':
            inputSpatialReference = arcpy.SpatialReference(54032) # World Azimuthal Equidistant

        arcpy.env.overwriteOutput = True

        outputVisibilityOut = VisibilityUtilities.radialLineOfSight(inputObserverFeatures,
                                              inputObserverHeight,
                                              inputRadiusOfObserver,
                                              inputSurface,
                                              outputVisibility,
                                              inputForceVisibility,
                                              inputSpatialReference)

        # Set output
        return outputVisibilityOut

class FindLocalPeaks(object):
    def __init__(self):
        self.label = 'Find Local Peaks'
        self.description = 'Finds the highest local maximums within the defined area. Peaks are found by inverting the surface and then finding the sinks in the surface. These points are then used to extract elevation values from the original surface, sorted based on elevation.'
        self.category = "Visibility"
        self.canRunInBackground = False

    def getParameterInfo(self):
        # Input_Area
        param_1 = arcpy.Parameter()
        param_1.name = 'Input_Area'
        param_1.displayName = 'Input Area'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = 'Feature Set'
        # Set the Feature Set schema
        input_layer_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                          "layers",
                                          "InputArea_FeatureSetGDB.lyr")
        param_1.value = input_layer_file_path

        # Number_Of_Peaks
        param_2 = arcpy.Parameter()
        param_2.name = 'Number_Of_Peaks'
        param_2.displayName = 'Number Of Peaks'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = 'Long'
        param_2.value = '10'

        # Input_Surface
        param_3 = arcpy.Parameter()
        param_3.name = 'Input_Surface'
        param_3.displayName = 'Input Surface'
        param_3.parameterType = 'Required'
        param_3.direction = 'Input'
        param_3.datatype = 'Raster Layer'

        # Output_Peak_Features
        param_4 = arcpy.Parameter()
        param_4.name = 'Output_Peak_Features'
        param_4.displayName = 'Output Peak Features'
        param_4.parameterType = 'Required'
        param_4.direction = 'Output'
        param_4.datatype = 'Feature Class'
        output_layer_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                          "layers",
                                          "Highest Point Output.lyr")
        param_4.symbology = output_layer_file_path

        return [param_1, param_2, param_3, param_4]

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        # 0 - Input Area
        # 1 - Number Of Peaks
        # 2 - Input Surface
        # 3 - Output Peak Features
        validator = getattr(self, 'ToolValidator', None)
        if validator:
             return validator(parameters).updateParameters()
        return

    def updateMessages(self, parameters):
        validator = getattr(self, 'ToolValidator', None)
        if validator:
             return validator(parameters).updateMessages()

    def execute(self, parameters, messages):
        try:
            from . import VisibilityUtilities
        except ImportError:
            import VisibilityUtilities

        input_area = parameters[0].valueAsText
        number_of_peaks = parameters[1].valueAsText
        input_surface = parameters[2].valueAsText
        output_peak_features = parameters[3].valueAsText

        out_findLocalPeaks = VisibilityUtilities.findLocalPeaks(input_area,
                                                                    number_of_peaks,
                                                                    input_surface,
                                                                    output_peak_features)

        return out_findLocalPeaks

class HighestPoints(object):
    def __init__(self):
        self.label = 'Highest Points'
        self.description = 'Finds the highest point (or points if several have the same elevation) of the input surface within a defined area.'
        self.category = "Visibility"
        self.canRunInBackground = False

    def getParameterInfo(self):
        # Input_Area
        param_1 = arcpy.Parameter()
        param_1.name = 'Input_Area'
        param_1.displayName = 'Input Area'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = 'Feature Set'
        # Set the Feature Set schema
        input_layer_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                          "layers",
                                          "InputArea_FeatureSetGDB.lyr")
        param_1.value = input_layer_file_path

        # Input_Surface
        param_2 = arcpy.Parameter()
        param_2.name = 'Input_Surface'
        param_2.displayName = 'Input Surface'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = 'Raster Layer'

        # Output_Highest_Point_Features
        param_3 = arcpy.Parameter()
        param_3.name = 'Output_Highest_Point_Features'
        param_3.displayName = 'Output Highest Point Features'
        param_3.parameterType = 'Required'
        param_3.direction = 'Output'
        param_3.datatype = 'Feature Class'
        output_layer_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                          "layers",
                                          "Highest Point Output.lyr")
        param_3.symbology = output_layer_file_path

        return [param_1, param_2, param_3]

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
            from . import VisibilityUtilities
        except ImportError:
            import VisibilityUtilities

        input_area = parameters[0].valueAsText
        input_surface = parameters[1].valueAsText
        output_highest_point_features = parameters[2].valueAsText
        hi_low_Switch = 'MAXIMUM'

        out_highest_points = VisibilityUtilities.hi_lowPointByArea(input_area,
                                                                    input_surface,
                                                                    hi_low_Switch,
                                                                    output_highest_point_features)
        return out_highest_points

class LowestPoints(object):
    def __init__(self):
        self.label = 'Lowest Points'
        self.description = 'Finds the lowest point (or points if several have the same elevation) of the input surface within a defined area.'
        self.category = "Visibility"
        self.canRunInBackground = False

    def getParameterInfo(self):
        # Input_Area
        param_1 = arcpy.Parameter()
        param_1.name = 'Input_Area'
        param_1.displayName = 'Input Area'
        param_1.parameterType = 'Required'
        param_1.direction = 'Input'
        param_1.datatype = 'Feature Set'
        # Set the Feature Set schema
        input_layer_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                          "layers",
                                          "InputArea_FeatureSetGDB.lyr")
        param_1.value = input_layer_file_path

        # Input_Surface
        param_2 = arcpy.Parameter()
        param_2.name = 'Input_Surface'
        param_2.displayName = 'Input Surface'
        param_2.parameterType = 'Required'
        param_2.direction = 'Input'
        param_2.datatype = 'Raster Layer'

        # Output_Lowest_Point_Features
        param_3 = arcpy.Parameter()
        param_3.name = 'Output_Lowest_Point_Features'
        param_3.displayName = 'Output Lowest Point Features'
        param_3.parameterType = 'Required'
        param_3.direction = 'Output'
        param_3.datatype = 'Feature Class'
        output_layer_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                          "layers",
                                          "Lowest Point Output.lyr")
        param_3.symbology = output_layer_file_path

        return [param_1, param_2, param_3]
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
            from . import VisibilityUtilities
        except ImportError:
            import VisibilityUtilities

        input_area = parameters[0].valueAsText
        input_surface = parameters[1].valueAsText
        output_lowest_point_features = parameters[2].valueAsText
        hi_low_Switch = 'MINIMUM'

        out_lowest_points = VisibilityUtilities.hi_lowPointByArea(input_area,
                                                                    input_surface,
                                                                    hi_low_Switch,
                                                                    output_lowest_point_features)
        return out_lowest_points
