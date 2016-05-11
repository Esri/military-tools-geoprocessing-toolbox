# coding: utf-8
'''
-----------------------------------------------------------------------------
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
ConversionTestSuite.py
--------------------------------------------------
requirments:
* ArcGIS Desktop 10.X+ or ArcGIS Pro 1.X+
* Python 2.7 or Python 3.4
author: ArcGIS Solutions
company: Esri
==================================================
description:
This test suite collects all of the tests in the Conversion toolset within the Military Tools toolbox:


==================================================
history:
5/10/2016 - JH - initial creation
==================================================
'''

import logging
import unittest
import Configuration
from . import MilitaryAspectsOfWeatherTestSuite

def getConversionTestSuites():
    ''' This pulls together all of the toolbox test suites in this folder '''
    if Configuration.DEBUG == True:
        print("   ConversionTestSuite.getConversionTestSuites")    
    Configuration.Logger.info("Adding Conversion tests including: ")
    testSuite = unittest.TestSuite()
    
    # TODO: add all Conversion tests here
    # testSuite.addTests(MaritimeDecisionAidToolsTestSuite.getMaritimeTestSuite())
    
    return testSuite
        
