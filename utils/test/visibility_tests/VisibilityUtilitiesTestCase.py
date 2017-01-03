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
from . import VisibilityUtilities

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
        UnitTestUtilities.checkArcPy()        
        if arcpy.CheckExtension("Spatial") == "Available":
            arcpy.CheckOutExtension("Spatial")
        else:
            raise Exception("Spatial license is not available.")
        
        if arcpy.CheckExtension("3D") == "Available":
            arcpy.CheckOutExtension("3D")
        else:
            raise Exception("3D license is not available.")
        self.srWGS84 = arcpy.SpatialReference(4326) # GCS_WGS_1984
        self.srWAZED = arcpy.SpatialReference(54032) # World Azimuthal Equidistant    
        self.inputArea = os.path.join(Configuration.militaryInputDataGDB, "AreaofInterest")
        self.inputSurface = os.path.join(Configuration.militaryInputDataGDB, "ElevationUTM_Zone10")
        self.inputSigActsTable = os.path.join(Configuration.militaryInputDataGDB, "SigActs")
        
        if not arcpy.Exists(Configuration.militaryScratchGDB):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.currentPath)
            
    def tearDown(self):
        runToolMessage = ".....VisibilityUtilityTestCase.teardown"
        arcpy.AddMessage(runToolMessage)
        arcpy.CheckInExtension("Spatial")
        arcpy.CheckInExtension("3D")
        if len(deleteIntermediateData) > 0:
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
        
        resultNames = VisibilityUtilities._getFieldNameList(junkTable, [])
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

    def test__getRasterMinMax(self):
        '''
        test internal method _getRasterMinMax
        '''
        runToolMessage = ".....VisibilityUtilityTestCase.test__getRasterMinMax"
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        resultMin, resultMax = VisibilityUtilities._getRasterMinMax(self.inputSurface)
        expectedMin = int(-41)
        self.assertEqual(expectedMin, resultMin, "Expected minimum of {0}, but got {1}".format(expectedMin, resultMin))
        expectedMax = int(1785)
        self.assertEqual(expectedMax, resultMax, "Expected maximum of {0}, but got {1}".format(expectedMax, resultMax))
    
    def test__clipRasterToArea(self):
        '''
        Compare result of _clipRasterToArea result to known, good comparison dataset
        '''
        runToolMessage = ".....VisibilityUtilityTestCase.test__clipRasterToArea"
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        expectedOutput = os.path.join(Configuration.militaryResultsGDB, "ExpectedOutputclipRasterToArea")
        resultClippedRaster = os.path.join(Configuration.militaryScratchGDB, "resultClippedRaster")
        resultClippedRaster = VisibilityUtilities._clipRasterToArea(self.inputSurface, self.inputArea, resultClippedRaster)
        deleteIntermediateData.append(resultClippedRaster)
        result = arcpy.RasterCompare_management(expectedOutput, resultClippedRaster, "RASTER_DATASET").getOutput(1)
        self.assertEqual(result, "true", "Raster Compare failed: \n %s" % arcpy.GetMessages())

    def test__getUniqueValuesFromField001(self):
        '''
        Test __getUniqueValuesFromField with SigActs table's AttackScal field.
        '''
        runToolMessage = ".....VisibilityUtilityTestCase.test__getUniqueValuesFromField001"
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        expectedAttackScal = ["Macro", "Micro"]
        resultAttackScal = VisibilityUtilities._getUniqueValuesFromField(self.inputSigActsTable, "AttackScal")
        self.assertEqual(len(expectedAttackScal),
                         len(resultAttackScal),
                         "Expected {0} unique values, but got {1}.".format(expectedAttackScal, resultAttackScal))
        
    def test__getUniqueValuesFromField002(self):
        '''
        Test __getUniqueValuesFromField with SigActs table's NoAttacks field.
        '''
        runToolMessage = ".....VisibilityUtilityTestCase.test__getUniqueValuesFromField002"
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        expectedNoAttacks = [0, 1, 2, 3]
        resultNoAttacks = VisibilityUtilities._getUniqueValuesFromField(self.inputSigActsTable, "NoAttacks")
        self.assertEqual(len(expectedNoAttacks),
                         len(resultNoAttacks),
                         "Expected {0} unique values, but got {1}.".format(expectedNoAttacks, resultNoAttacks))

    def test__getCentroid_FromPoints(self):
        '''
        Testing _getCentroid from point feature class with 4 points.
        '''
        runToolMessage = ".....VisibilityUtilityTestCase.test__getCentroid"
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        # make a featureclass of points
        pntArray = arcpy.Array([arcpy.Point(0,0),
                               arcpy.Point(0,2),
                               arcpy.Point(2,0),
                               arcpy.Point(2,2)])
        fc = arcpy.CreateFeatureclass_management("in_memory", "fc",
                                                 "POINT", None,
                                                 "DISABLED", "DISABLED",
                                                 self.srWGS84)[0]
        with arcpy.da.InsertCursor(fc, ["SHAPE@"]) as cursor:
            for pnt in pntArray:
                cursor.insertRow([arcpy.PointGeometry(pnt)])
        resultPoint = VisibilityUtilities._getCentroid(fc).firstPoint
        
        # determine centroid of X and Y coordinate sets
        pX, pY, count = 0, 0, 0
        for p in pntArray:
            pX += p.X
            pY += p.Y
            count += 1
        cX = float(pX)/float(count)
        cY = float(pY)/float(count)
        comparePoint = arcpy.Point(cX, cY)
        
        arcpy.AddMessage("comparePoint.X: {0}".format(comparePoint.X))
        arcpy.AddMessage(comparePoint.X)
        arcpy.AddMessage("resultPoint.X: {0}".format(resultPoint.X))
        arcpy.AddMessage(resultPoint.X)
        arcpy.AddMessage("comparePoint.X is resultPoint.X: {0}".format(comparePoint.X is resultPoint.X))
        arcpy.AddMessage("comparePoint.X == resultPoint.X: {0}".format(comparePoint.X == resultPoint.X))
        
        self.assertEqual(comparePoint.X, resultPoint.X, "Unexpected centroid X. Expected {0}, but got {1}".format(comparePoint.X, resultPoint.X))
        self.assertEqual(comparePoint.Y, resultPoint.Y, "Unexpected centroid Y. Expected {0}, but got {1}".format(comparePoint.Y, resultPoint.Y))
        
    def test__getLocalWAZED(self):
        '''
        '''
        runToolMessage = ".....VisibilityUtilityTestCase.test__getLocalWAZED"
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        testInputPoint = arcpy.PointGeometry(arcpy.Point(-11.13, 14.87), self.srWGS84)
        resultSR = VisibilityUtilities._getLocalWAZED(testInputPoint)
        # arcpy.AddMessage("======================")
        # arcpy.AddMessage(resultSR.exportToString())
        # arcpy.AddMessage("======================")
        # arcpy.AddMessage(self.srWAZED.exportToString())
        # arcpy.AddMessage("======================")
        self.assertIs(resultSR, self.srWAZED, "Compare expected Spatial Reference {0} with result {1} failed.".format(self.srWAZED, resultSR))
                
    def test__prepPointFromSurface(self):
        '''
        '''

    # Test external methods

    def test_hi_lowPointByArea_lowest(self):
        '''
        test hi_lowPointByArea for MINIMUM (lowest) setting.
        '''
        runToolMessage = ".....VisibilityUtilityTestCase.test_hi_lowPointByArea_lowest"
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        hi_low_Switch = "MINIMUM"
        resultPoints = os.path.join(Configuration.militaryScratchGDB, "lowestPoints")
        VisibilityUtilities.hi_lowPointByArea(self.inputArea,
                                              self.inputSurface,
                                              hi_low_Switch,
                                              resultPoints)
        deleteIntermediateData.append(resultPoints)
        expectedLowest = os.path.join(Configuration.militaryResultsGDB, "ExpectedOutputLowestPt")
        compareResults = arcpy.FeatureCompare_management(resultPoints, expectedLowest, "OBJECTID").getOutput(1)
        self.assertEqual(compareResults, "true", "Feature Compare failed: \n %s" % arcpy.GetMessages())

    def test_hi_lowPointByArea_highest(self):
        '''
        test hi_lowPointByArea for MAXIMUM (highest) setting.
        '''
        runToolMessage = ".....VisibilityUtilityTestCase.test_hi_lowPointByArea_highest"
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        hi_low_Switch = "MAXIMUM"
        resultPoints = os.path.join(Configuration.militaryScratchGDB, "highestPoints")
        resultPoints = VisibilityUtilities.hi_lowPointByArea(self.inputArea,
                                                             self.inputSurface,
                                                             hi_low_Switch,
                                                             resultPoints)
        deleteIntermediateData.append(resultPoints)
        expectedHighest = os.path.join(Configuration.militaryResultsGDB, "ExpectedOutputHighestPt")
        compareResults = arcpy.FeatureCompare_management(resultPoints, expectedHighest,"OBJECTID").getOutput(1)
        self.assertEqual(compareResults, "true", "Feature Compare failed: \n %s" % arcpy.GetMessages())

    # Test tool methods
    
    def test_findLocalPeaks(self):
        '''
        test_findLocalPeaks with input 10 peaks to find
        '''
        runToolMessage = ".....VisibilityUtilityTestCase.test_findLocalPeaks"
        arcpy.AddMessage(runToolMessage)
        Configuration.Logger.info(runToolMessage)
        resultPoints = os.path.join(Configuration.militaryScratchGDB, "findLocalPeaks")
        numPoints = 16
        resultPoints = VisibilityUtilities.findLocalPeaks(self.inputArea,
                                                          numPoints,
                                                          self.inputSurface,
                                                          resultPoints)
        deleteIntermediateData.append(resultPoints)
        expectedLocalPeaks = os.path.join(Configuration.militaryResultsGDB, "ExpectedOutputFindLocalPeaks")
        compareResults = arcpy.FeatureCompare_management(resultPoints, expectedLocalPeaks, "OBJECTID").getOutput(1)
        self.assertEqual(compareResults, "true", "Feature Compare failed: \n %s" % arcpy.GetMessages())

    
    
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
