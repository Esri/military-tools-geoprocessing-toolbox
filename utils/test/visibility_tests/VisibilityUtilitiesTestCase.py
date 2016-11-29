# coding: utf-8
'''
------------------------------------------------------------------------------
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
------------------------------------------------------------------------------
 ==================================================
 VisibilityUtilitiesTestCase.py
 --------------------------------------------------
 requirements: ArcGIS 10.3+, Python 2.7 or Python 3.4
 author: ArcGIS Solutions
 contact: support@esri.com
 company: Esri
 ==================================================
 description:
 Unit tests for Visibility tools
 ==================================================
 history:
 11/28/2016 - mf - original coding
 ==================================================
'''

# IMPORTS ==========================================
import os
import sys
import traceback
import arcpy
from arcpy import env
import unittest
import UnitTestUtilities
import Configuration
import VisibilityUtilities

# LOCALS ===========================================
deleteIntermediateData = [] # intermediate datasets to be deleted
debug = True # extra messaging during development

# FUNCTIONS ========================================

class VisibilityUtilitiesTestCase(unittest.TestCase):
    '''
    '''

    def setUp(self):
        runToolMessage = ".....VisibilityUtilityTestCase.setup"
        arcpy.AddMessage(runToolMessage)
        if arcpy.CheckExtension("Spatial") == "Available":
            arcpy.CheckOutExtension("Spatial")
        else:
            raise Exception("Spatial license is not available.")
        
        if arcpy.CheckExtension("3D") == "Available":
            arcpy.CheckOutExtension("3D")
        else:
            raise Exception("3D license is not available.")
        
        UnitTestUtilities.checkArcPy()
        Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.militaryDataPath)
            
    def tearDown(self):
        runToolMessage = ".....VisibilityUtilityTestCase.teardown"
        arcpy.AddMessage(runToolMessage)
        arcpy.CheckInExtension("Spatial")
        arcpy.CheckInExtension("3D")
        for i in deleteIntermediateData:
            if arcpy.Exists(i):
                if debug: arcpy.AddMessage("Removing intermediate: {0}".format(i))
                arcpy.Delete_management(i)
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)

    # Test internal methods
    def test__getFieldNameList(self):
        '''
        Testing internal method _getFieldNameList()
        '''
        runToolMessage = ".....VisibilityUtilityTestCase.test__getFieldNameList"
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        
        expectedNames = ["ObjectID", "D1", "T2"]
        junkTable = os.path.join("in_memory","junkTable")
        #if arcpy.Exists(junkTable): arcpy.Delete_management(junkTable)
        arcpy.CreateTable_management(os.path.dirname(junkTable),
                                     os.path.basename(junkTable))
        deleteIntermediateData.append(junkTable)
        arcpy.AddField_management(junkTable, expectedNames[1], "DOUBLE")
        arcpy.AddField_management(junkTable, expectedNames[2], "TEXT")
        
        resultNames = VisibilityUtilities._getFieldNameList(junkTable)
        self.assertEqual(expectedNames, resultNames, "Did not get expected field names. Got {0} instead.".format(str(resultNames)))

    def test__addDoubleField(self):
        '''
        Testing internal method _addDoubleField()
        '''
        runToolMessage = ".....VisibilityUtilityTestCase.test__addDoubleField"
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        
        newFields = {"A1":[0.0, "A1 field"],
                     "A2":[1.1, "A2 field"]}
        
        junkTable = os.path.join("in_memory","junkTable")
        #if arcpy.Exists(junkTable): arcpy.Delete_management(junkTable)
        arcpy.CreateTable_management(os.path.dirname(junkTable),
                                     os.path.basename(junkTable))
        deleteIntermediateData.append(junkTable)
        
        VisibilityUtilities._addDoubleField(junkTable, newFields)
        
        resultFields = []
        for f in arcpy.ListFields(junkTable):
            resultFields.append(f.name)
        expectedFields = list(["ObjectID"] + newFields.keys())
        self.assertEqual(expectedFields,
                         resultFields,
                         "Expected fields {0} were not added. Got {1} instead.".format(expectedFields, resultFields))

    def test__calculateFieldValue(self):
        '''
        Testing internal method _calculateFieldValue()
        '''
        runToolMessage = ".....VisibilityUtilityTestCase.test__calculateFieldValue"
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        
        expectedNames = ["D1", "T2"]
        junkTable = os.path.join("in_memory","junkTable")
        #if arcpy.Exists(junkTable): arcpy.Delete_management(junkTable)
        arcpy.CreateTable_management(os.path.dirname(junkTable),
                                     os.path.basename(junkTable))
        arcpy.AddField_management(junkTable, expectedNames[0], "DOUBLE")
        arcpy.AddField_management(junkTable, expectedNames[1], "TEXT")
        deleteIntermediateData.append(junkTable)
        with arcpy.da.InsertCursor(junkTable, [expectedNames[0]]) as iCursor:
            for i in xrange(0,4):
                iCursor.insertRow([float(i)])
        del iCursor
        testValue = "'valueT2'"
        
        VisibilityUtilities._calculateFieldValue(junkTable,
                                                 expectedNames[1],
                                                 testValue)

        resultFieldValueSet = set([row[0] for row in arcpy.da.SearchCursor(junkTable, [expectedNames[1]])])
        self.assertEqual(len(resultFieldValueSet),1,"_calculateFieldValue returned bad field values: {0}".format(str(resultFieldValueSet)))


    # Test external methods

    # Test tool methods
    
    # def test_addLLOSFields001(self):
    #     '''
    #     Test addLLOSFields with user-defined values
    #     '''
    #     pass
    # 
    # def test_addLLOSFields002(self):
    #     '''
    #     Test addLLOSFields with default values
    #     '''
    #     pass
    # 
    # def test_addRLOSObserverFields001(self):
    #     '''
    #     Test addRLOSObserverFields with user-defined values
    #     '''
    #     pass
    #     
    # def test_addRLOSObserverFields002(self):
    #     '''
    #     Test addRLOSObserverFields with default values
    #     '''
    #     pass
