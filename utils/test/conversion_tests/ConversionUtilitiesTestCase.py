# coding: utf-8
'''
-----------------------------------------------------------------------------
Copyright 2016 Esri
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-----------------------------------------------------------------------------

==================================================
ConversionUtilitesTestCase.py
--------------------------------------------------
requirements:
* ArcGIS Desktop 10.3.1+

* Python 2.7 or Python 3.4

author: ArcGIS Solutions
company: Esri

==================================================
history:
11/15/2016 - mf - placeholder
==================================================
'''

import unittest
import arcpy
import os
import UnitTestUtilities
import ConversionUtilites
import Configuration

class ConversionUtilitiesTestCase(unittest.TestCase):
    ''' Test all tools and methods related to the Conversion Utilites module
    in the Military Tools toolbox'''
    
    def setUp(self):
        if Configuration.DEBUG == True: print(".....ConversionUtilitiesTestCase.setUp")
        #TODO: inputPolylines
        if not arcpy.Exists(Configuration.militaryScratchGDB):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.currentPath)
        
        
    def tearDown(self):
        if Configuration.DEBUG == True: print(".....ConversionUtilitiesTestCase.tearDown")
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)
        
    def test_polylineToPolygon(self):
        '''
        '''
        
    '''
    Test the tool methods
    '''
        
    def test_tableToPolygon(self):
        '''
        '''
        