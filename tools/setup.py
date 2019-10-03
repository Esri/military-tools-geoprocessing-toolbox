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
'''

#from distutils.core import setup
from setuptools import setup, find_packages

setup(name='militarytools',
      version='3.6.0',
      description=r"Military Tools for ArcGIS",
      license='Apache-2.0', 
      url=r'http://solutions.arcgis.com/defense/help/military-tools/',
      author=r'Esri Solutions',
      author_email=r"support@esri.com",
      keywords=r"military tools arcgis arcpy solutions esri",
      packages=find_packages(),
      package_dir={'militarytools': 'militarytools'},
      package_data={'militarytools':
                    [r'*.*',
                     r'esri/toolboxes/scripts/*.*',
                     r'esri/toolboxes/layers/*.*',
                     r'esri/toolboxes/layers/featuresetsWebMerc.gdb/*.*',
                     r'esri/toolboxes/layers/featuresetsWebMerc.gdb/*',
                     r'esri/toolboxes/tooldata/*.*',
                     r'esri/toolboxes/tooldata/RangeRings.gdb/*.*',
                     r'esri/toolboxes/tooldata/RangeRings.gdb/*',
                     r'esri/toolboxes/*.*',
                     r'esri/*.*',
                     r'esri/arcpy/*.*', # Not currently used
                     r'esri/help/*.*',  # Not currently used
                     r'esri/help/gp/*.*', # Not currently used
                     r'esri/help/gp/toolboxes/*.*', # Not currently used
                     ]
                   },
     )
