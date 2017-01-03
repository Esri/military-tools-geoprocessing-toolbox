@ECHO OFF
rem ------------------------------------------------------------------------------
rem  Copyright 2015 Esri
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
rem  TestKickStart.bat
rem ------------------------------------------------------------------------------
rem  requirements:
rem  * ArcGIS Desktop 10.X+ or ArcGIS Pro 1.X+
rem  * Python 2.7 or Python 3.4
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
rem ==================================================

REM === TEST SETUP ===================================
ECHO Copying RangeRingUtils.py ...
COPY ..\..\toolboxes\scripts\RangeRingUtils.py .\distance_tests\RangeRingUtils.py
ECHO Copying VisibilityUtilities.py
COPY ..\..\toolboxes\scripts\VisibilityUtilities.py .\visibility_tests\VisibilityUtilities.py
REM === TEST SETUP ===================================


REM === LOG SETUP ====================================
REM usage: set LOG=<defaultLogFileName.log>
REM name is optional; if not specified, name will be specified for you
set LOG=
REM === LOG SETUP ====================================


REM === SINGLE VERSION ==================================
REM If you only have ONE version of Python installed
REM uncomment the following lines
REM =====================================================
python TestRunner.py
IF %ERRORLEVEL% NEQ 0 (
   ECHO 'One or more tests failed'
)
REM === SINGLE VERSION ==================================


rem REM === MULTIPLE VERSIONS ===============================
rem REM If you have BOTH versions of Python installed use
rem REM these lines
rem REM =====================================================
rem ECHO Python 3.4 Tests ===============================
rem REM py -3.4 TestRunner.py %LOG%
rem REM The location of python.exe will depend upon your installation
rem REM of ArcGIS Pro. Modify the following line as necessary:
rem REM "C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" TestRunner.py %LOG%
rem py -3.4 TestRunner.py %LOG%
rem REM check if ArcGIS Pro/Python 3.4 tests failed
rem IF %ERRORLEVEL% NEQ 0 (
rem    ECHO 'One or more tests failed'
rem )
rem ECHO Python 2.7 Tests ===============================
rem py -2.7 TestRunner.py %LOG%
rem REM check if Desktop for ArcGIS/Python 2.7 tests failed
rem IF %ERRORLEVEL% NEQ 0 (
rem    ECHO 'One or more tests failed'
rem )
rem REM === MULTIPLE VERSIONS ===============================


REM === CLEANUP =========================================
ECHO Removing RangeRingUtils.py ...
DEL ".\distance_tests\RangeRingUtils.py"
ECHO Removing VisibilityUtilities.py ...
DEL ".\visibility_tests\VisibilityUtilities.py"
REM === CLEANUP =========================================

pause
