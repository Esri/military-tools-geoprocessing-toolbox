# coding: utf-8
'''
------------------------------------------------------------------------------
 Copyright 2019 Esri
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
 TestTools.py
 --------------------------------------------------
 requirements: ArcGIS 10.4.1+, ArcGIS Pro 2.2+, Python 2.7 or Python 3.5+
 author: ArcGIS Solutions
 contact: support@esri.com
 company: Esri
 ==================================================
 description:
 GRG Tool logic module.
 ==================================================
'''

import os
import arcpy

try:
    from . import TrajectoryPath
    from . import Utilities
except ImportError:
    import TrajectoryPath
    import Utilities

class ComputeTrajectory(object):
    '''
    TODO: add decription
    '''
    def __init__(self):
        '''
        Tool constructor method
        '''
        self.label = 'Compute Trajectory'
        self.description = 'Compute Trajectory builds a simple line representing the flight path of a projectile (mortar or artillery) based on a set of intitial parameters.'
        self.category = "Evaluation Tools"

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def getParameterInfo(self):
        '''
        Define parameter definitions
        '''

        input_start_location = arcpy.Parameter(name='weapon_location',
                                               displayName='Weapon Location',
                                               direction='Input',
                                               datatype='GPFeatureRecordSetLayer',
                                               parameterType='Required',
                                               enabled=True,
                                               multiValue=False)

        # TODO: add/change symbology if desired:
        input_layer_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                             "layers",
                                             "RangeRingInputObserversGDB.lyr")  # <-- Using this input schema layer for now
        input_start_location.value = input_layer_file_path

        initial_velocity = arcpy.Parameter(name='initial_velocity',
                                     displayName='Initial Velocity (Meters / Second)',
                                     direction='Input',
                                     datatype='GPDouble',
                                     parameterType='Required',
                                     enabled=True,
                                     multiValue=False)
        initial_velocity.value = 350.0

        elevation_angle = arcpy.Parameter(name='elevation_angle',
                                     displayName='Elevation Angle (degrees from level)',
                                     direction='Input',
                                     datatype='GPDouble',
                                     parameterType='Required',
                                     enabled=True,
                                     multiValue=False)
        elevation_angle.value = 45

        azimuth_angle = arcpy.Parameter(name='azimuth_angle',
                                     displayName='Azimuth Angle (degrees from North)',
                                     direction='Input',
                                     datatype='GPDouble',
                                     parameterType='Required',
                                     enabled=True,
                                     multiValue=False)
        azimuth_angle.value = 315

        trajectory_model = arcpy.Parameter(name='trajectory_model',
                                     displayName='Trajectory Model',
                                     direction='Input',
                                     datatype='GPString',
                                     parameterType='Required',
                                     enabled=True,
                                     multiValue=False)
        trajectory_model.filter.type = 'ValueList'
        trajectory_model.filter.list = ['IDEAL']
        trajectory_model.value = trajectory_model.filter.list[0]

        input_surface = arcpy.Parameter(name = 'input_surface',
                                displayName = 'Input Surface',
                                parameterType = 'Required',
                                direction = 'Input',
                                datatype = 'Raster Layer',
                                enabled=True,
                                multiValue=False)

        output_features= arcpy.Parameter(name='output_features',
                                         displayName='Output Features',
                                         direction='Output',
                                         datatype='DEFeatureClass',
                                         parameterType='Required',
                                         enabled=True,
                                         multiValue=False)
        output_features.value = r"%scratchGDB%/output_trajectory"

        layerFile = "Trajectory3D.lyrx"
        app = Utilities.GetPlatform()
        if (app == 'ARCMAP'):
            layerFile = "RangeRings.lyr"
        output_features.symbology = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                                 "layers", layerFile)

        return [input_start_location,
                initial_velocity,
                elevation_angle,
                azimuth_angle,
                trajectory_model,
                input_surface,
                output_features]

    def updateParameters(self, parameters):
        '''
        Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed.
        '''
        return

    def updateMessages(self, parameters):
        '''
        '''
        return

    def execute(self, parameters, messages):
        ''' execute for toolbox'''

        #arcpy.AddError("Not built yet.")

        inputFeature       = parameters[0].valueAsText
        initialVelocityMPS = parameters[1].value
        elevationAngleDegrees = parameters[2].value
        azimuthAngleDegrees   = parameters[3].value
        analysisType = parameters[4].valueAsText
        inputSurface = parameters[5].valueAsText
        outFeatures  = parameters[6].valueAsText

        output_features = TrajectoryPath.computeTrajectory( \
                       inputFeature, initialVelocityMPS, elevationAngleDegrees, \
                       azimuthAngleDegrees, analysisType, inputSurface, outFeatures)

        return output_features


