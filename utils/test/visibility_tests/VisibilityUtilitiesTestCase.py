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
 .py
 --------------------------------------------------
 requirements: ArcGIS X.X, Python 2.7 or Python 3.4
 author: ArcGIS Solutions
 contact: support@esri.com
 company: Esri
 ==================================================
 description: <Description>
 ==================================================
 history:
 <date> - <initals> - <modifications>
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

    def setup(self):
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
            
    def teardown(self):
        arcpy.CheckInExtension("Spatial")
        arcpy.CheckInExtension("3D")
        for i in deleteIntermediateData:
            if arcpy.Exists(i):
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
        
        expectedNames = ["D1", "T2"]
        junkTable = arcpy.RecordSet()
        arcpy.AddTable_Management(junkTable, expectedNames[0], "DOUBLE")
        arcpy.AddTable_Management(junkTable, expectedNames[1], "TEXT")
        
        resultNames = VisibilityUtilities._getFieldNameList(junkTable)
        self.assertEqual(expectedNames, resultNames, "Did not get expected field names. Got {0} instead.".format(str(resultNames)))
        del junkTable

    def test__addDoubleField(self):
        '''
        Testing internal method _addDoubleField()
        '''
        runToolMessage = ".....VisibilityUtilityTestCase.test__addDoubleField"
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        
        newFields = {"A1":[0.0, "A1 field"],
                     "A2":[1.1, "A2 field"]}
        
        junkTable = arcpy.RecordSet()
        resultTable = VisibilityUtilities._addDoubleField(junkTable, newFields)
        
        resultFields = []
        for f in arcpy.ListFields(resultTable):
            resultFields.append(f.name)
        self.assertEqual(list(newFields.keys()), resultFields, "Expected fields were not added.")
        del junkTable

    def test__calculateFieldValue(self):
        '''
        Testing internal method _calculateFieldValue()
        '''
        runToolMessage = ".....VisibilityUtilityTestCase.test__addDoubleField"
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        
        expectedNames = ["D1", "T2"]
        junkTable = arcpy.RecordSet()
        arcpy.AddTable_Management(junkTable, expectedNames[0], "DOUBLE")
        arcpy.AddTable_Management(junkTable, expectedNames[1], "TEXT")
        with arcpy.da.InsertCursor(junkTable, [expectedNames[0]]) as iCursor:
            for i in xrange(0,4):
                iCursor.insertow(float(i))
        del iCursor
        testValue = 'valueT2'
        resultTable = VisibilityUtilities._calculateFieldValue(junkTable,
                                                               expectedNames[1],
                                                               testValue)

        resultFieldValueSet = set([row[0] for row in arcpy.da.SearchCursor(resultTable, [expectedNames[1]])])
        self.assertEqual(len(resultFieldValueSet),1,"_calculateFieldValue returned bad field values: {0}".format(str(resultFieldValueSet)))


    # Test external methods

    # Test tool methods
    def test_addLLOSFields(self):
        '''
        '''
        