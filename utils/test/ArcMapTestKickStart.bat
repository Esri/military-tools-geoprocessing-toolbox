@ECHO OFF
rem ------------------------------------------------------------------------------
rem  Copyright 2017 Esri
rem  Licensed under the Apache License, Version 2.0 (the "License");
rem  you may not use this file except in compliance with the License.
rem  You may obtain a copy of the License at
rem 
rem    http://www.apache.org/licenses/LICENSE-2.0
rem 
rem  Unless required by applicable law or agreed to in writing, software
rem  distributed under the License is distributed on an "AS IS" BASIS,
rem  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
rem  See the License for the specific language governing permissions and
rem  limitations under the License.
rem ------------------------------------------------------------------------------
rem  ArcMapTestKickStart.bat
rem ------------------------------------------------------------------------------
rem  requirements:
rem  * ArcGIS Desktop 10.X+ or ArcGIS Pro 1.X+
rem  * Python 2.7 
rem  * Python added to executable PATH
rem  author: ArcGIS Solutions
rem  company: Esri
rem ==================================================
rem  description:
rem  This file starts the test running for Desktop (Python 2.7+) and
rem  ArcGIS Pro (Python 3.4+).
rem 
rem ==================================================
rem  history:
rem  5/9/2016: JH - initial creation
rem  6/1/2016: MF - Add RangeRingUtils.py copy for testing
rem  6/3/2016: MF - work on exit codes
rem  12/22/2016: MF - change back to single execution for Jenkins builds
rem  1/5/2017: MF - separate into Pro and Desktop test BAT
rem ==================================================

REM === LOG SETUP ====================================
REM usage: set LOG=<defaultLogFileName.log>
REM name is optional; if not specified, name will be specified for you
set LOG=
REM === LOG SETUP ====================================

REM You may need to add this section in if ArcMap Python is not in your PATH
REM SET ARCMAP_PYTHON_PATH=C:\Python27\ArcGIS10.4
REM SET PATH=%ARCMAP_PYTHON_PATH%;%PATH%

ECHO Testing with ArcMap ===============================

python TestRunner.py %LOG%

REM check if Desktop for ArcGIS/Python 2.7 tests failed
IF %ERRORLEVEL% NEQ 0 (
   ECHO 'One or more tests failed'
)

REM pause
