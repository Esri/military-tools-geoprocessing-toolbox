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
Configuration.py
Description: Common objects/methods used by test scripts
Requirements: ArcGIS Desktop Standard

----------------------------------------------------------------------------
'''

import logging
import os
import sys

DEBUG = True # this guy is a flag for extra messaging while debugging tests

#NOTE: Logger and Platform are initialized in TestRunner's main() or Configuration.GetLogger/Platform
Logger = None
LoggerFile = None

Platform = None

PLATFORM_PRO = "PRO"
PLATFORM_DESKTOP = "DESKTOP"

''' Testing paths '''
currentPath = os.path.dirname(__file__) # should go to .\military-tools-geoprocessing-toolbox\utils\test
repoPath = os.path.dirname(os.path.dirname(currentPath))

''' Log Path: the folder where the log files go wild and multiply '''
logPath = os.path.normpath(os.path.join(currentPath, r"log")) # should go to .\military-geoprocessing-toolbox\utils\test\log

''' Data path '''
militaryDataPath = os.path.normpath(os.path.join(currentPath, r"../testdata/"))
militaryInputDataGDB = os.path.normpath(os.path.join(militaryDataPath, "MilitaryToolsTestData.gdb"))
militaryResultsGDB = os.path.normpath(os.path.join(militaryDataPath, "Results.gdb"))
militaryScratchGDB = os.path.normpath(os.path.join(currentPath, "scratch.gdb"))

''' Toolboxes paths '''
militaryToolboxesPath = os.path.normpath(os.path.join(currentPath, r"../../tools/militarytools/esri/toolboxes/"))
military_ToolboxPath  = os.path.normpath(os.path.join(militaryToolboxesPath, "MilitaryTools.pyt"))
toolboxUnderTest = None # Set to Pro or ArcMap toolbox at runtime

''' Conversion Path'''
conversionPath = os.path.normpath(os.path.join(currentPath, r"conversion_tests"))

''' Distance Path '''
distancePath = os.path.normpath(os.path.join(currentPath, r"distance_tests"))

''' Visibility Path '''
visibilityPath = os.path.normpath(os.path.join(currentPath, r"visibility_tests"))

''' Script Path (needed by some tests that test functions directly '''
scriptsPath = os.path.join(militaryToolboxesPath, 'scripts')

def addScriptsPath() : 
    if (scriptsPath not in sys.path) :
        sys.path.append(scriptsPath) 

def checkTokenizeWorkaround() :
    #################################################
    # WORKAROUND: for Python 3 choking on reading some binary files (with nulls)
    # For example in ArcPy when loading a toolbox when run from command line
    # Get error like: detect_encoding...tokenize.py...find_cookie...raise SyntaxError(msg)
    # ...SyntaxError: invalid or missing encoding declaration for '...XXXX.tbx'
    # Workaround borrowed/used from:
    # https://github.com/habnabit/passacre/commit/2ea05ba94eab2d26951ae7b4b51abf53132b20f0

    # Code should work with Python 2, but only do workaround for Python 3
    # Workaround needed in Versions 3.0 - 3.5.2
    if sys.version_info >= (3, 0) and sys.version_info < (3, 5, 3):
        import tokenize

        try:
            _detect_encoding = tokenize.detect_encoding
        except AttributeError:
            pass
        else:
            def detect_encoding(readline):
                try:
                    return _detect_encoding(readline)
                except SyntaxError:
                    return 'latin-1', []

            tokenize.detect_encoding = detect_encoding
    ## END WORKAROUND
    #################################################

def GetLogger(logLevel = logging.DEBUG) :

    global Logger

    if Logger is None:

        import UnitTestUtilities

        logName = UnitTestUtilities.getLoggerName()
        Logger = UnitTestUtilities.initializeLogger(logName, logLevel)

    return Logger

def GetPlatform() :

    global Platform, toolboxUnderTest

    if Platform is None :

        import arcpy

        Platform = PLATFORM_DESKTOP

        installInfo = arcpy.GetInstallInfo()
        if installInfo['ProductName'] == 'ArcGISPro':
            Platform = PLATFORM_PRO
            checkTokenizeWorkaround()

        # Both Pro and ArcMap just the .pyt toolbox now:
        toolboxUnderTest = military_ToolboxPath

    return Platform

