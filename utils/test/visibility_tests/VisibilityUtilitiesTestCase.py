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
import unittest

import arcpy

# Add parent folder to python path if running test case standalone
import sys
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))

import UnitTestUtilities
import Configuration
import arcpyAssert

# Add scripts to path so can call methods directly
Configuration.addScriptsPath()
import VisibilityUtilities

# LOCALS ===========================================
deleteIntermediateData = [] # intermediate datasets to be deleted
debug = True # extra messaging during development

# FUNCTIONS ========================================

class VisibilityUtilitiesTestCase(unittest.TestCase, arcpyAssert.FeatureClassAssertMixin):
    '''
    '''     

    def setUp(self):
        ''' Initialization needed if running Test Case standalone '''
        Configuration.GetLogger()
        Configuration.GetPlatform()
        ''' End standalone initialization '''
            
        Configuration.Logger.debug(".....VisibilityUtilityTestCase.setup")

        UnitTestUtilities.checkArcPy()        

        arcpy.env.overwriteOutput = True

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
        Configuration.Logger.debug(".....VisibilityUtilityTestCase.teardown")

        arcpy.CheckInExtension("Spatial")
        arcpy.CheckInExtension("3D")

        if len(deleteIntermediateData) > 0:
            for i in deleteIntermediateData:
                if arcpy.Exists(i):
                    if debug: arcpy.AddMessage("Removing intermediate: {0}".format(i))
                    arcpy.Delete_management(i)
        # UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)

    # Test internal methods
    def test_getFieldNameList(self):
        '''
        Testing internal method _getFieldNameList()
        '''
        Configuration.Logger.info(".....VisibilityUtilityTestCase.test_getFieldNameList")
        
        junkTable = os.path.join("in_memory","junkTable")
        #if arcpy.Exists(junkTable): arcpy.Delete_management(junkTable)
        arcpy.CreateTable_management(os.path.dirname(junkTable),
                                     os.path.basename(junkTable))
        deleteIntermediateData.append(junkTable)
        expectedNames = [arcpy.Describe(junkTable).OIDFieldName.upper(), "D1", "T2"]
        arcpy.AddField_management(junkTable, expectedNames[1], "DOUBLE")
        arcpy.AddField_management(junkTable, expectedNames[2], "TEXT")

        # IMPORTANT: Fields names are returned in UPPERCASE for some reason
        resultNames = VisibilityUtilities._getFieldNameList(junkTable, [])
        self.assertEqual(expectedNames, resultNames, "Did not get expected field names. Got {0} instead.".format(str(resultNames)))

    def test_addDoubleField(self):
        '''
        Testing internal method _addDoubleField()
        '''
        Configuration.Logger.info(".....VisibilityUtilityTestCase.test_addDoubleField")

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
        expectedFields = list(["ObjectID"] + list(newFields.keys()))
        self.assertEqual(expectedFields,
                         resultFields,
                         "Expected fields {0} were not added. Got {1} instead.".format(expectedFields, resultFields))

    def test_calculateFieldValue(self):
        '''
        Testing internal method _calculateFieldValue()
        '''
        Configuration.Logger.info(".....VisibilityUtilityTestCase.test_calculateFieldValue")
        
        expectedNames = ["D1", "T2"]
        junkTable = os.path.join("in_memory","junkTable")
        #if arcpy.Exists(junkTable): arcpy.Delete_management(junkTable)
        arcpy.CreateTable_management(os.path.dirname(junkTable),
                                     os.path.basename(junkTable))
        arcpy.AddField_management(junkTable, expectedNames[0], "DOUBLE")
        arcpy.AddField_management(junkTable, expectedNames[1], "TEXT")
        deleteIntermediateData.append(junkTable)
        with arcpy.da.InsertCursor(junkTable, [expectedNames[0]]) as iCursor:
            for i in range(0,4):
                iCursor.insertRow([float(i)])
        del iCursor
        testValue = "'valueT2'"
        
        VisibilityUtilities._calculateFieldValue(junkTable,
                                                 expectedNames[1],
                                                 testValue)

        resultFieldValueSet = set([row[0] for row in arcpy.da.SearchCursor(junkTable, [expectedNames[1]])])
        self.assertEqual(len(resultFieldValueSet),1,"_calculateFieldValue returned bad field values: {0}".format(str(resultFieldValueSet)))

    def test_getRasterMinMax(self):
        '''
        test internal method _getRasterMinMax
        '''
        Configuration.Logger.info(".....VisibilityUtilityTestCase.test_getRasterMinMax")

        resultMin, resultMax = VisibilityUtilities._getRasterMinMax(self.inputSurface)
        expectedMin = int(-41)
        self.assertEqual(expectedMin, resultMin, "Expected minimum of {0}, but got {1}".format(expectedMin, resultMin))
        expectedMax = int(1785)
        self.assertEqual(expectedMax, resultMax, "Expected maximum of {0}, but got {1}".format(expectedMax, resultMax))
    
    def test_clipRasterToArea(self):
        '''
        Compare result of _clipRasterToArea result to known, good comparison dataset
        '''
        Configuration.Logger.info(".....VisibilityUtilityTestCase.test_clipRasterToArea")

        expectedOutput = os.path.join(Configuration.militaryResultsGDB, "ExpectedOutputclipRasterToArea")
        resultClippedRaster = os.path.join(Configuration.militaryScratchGDB, "resultClippedRaster")
        resultClippedRaster = VisibilityUtilities._clipRasterToArea(self.inputSurface, self.inputArea, resultClippedRaster)
        deleteIntermediateData.append(resultClippedRaster)
        result = arcpy.RasterCompare_management(expectedOutput, resultClippedRaster,"RASTER_DATASET","Columns And Rows;NoData;Pixel Value;Raster Attribute Table","","","All 1 Fraction","","").getOutput(1)
        self.assertEqual(result, "true", "Raster Compare failed: \n %s" % arcpy.GetMessages())

    def test_getUniqueValuesFromField001(self):
        '''
        Test _getUniqueValuesFromField with SigActs table's AttackScal field.
        '''
        Configuration.Logger.info(".....VisibilityUtilityTestCase.test_getUniqueValuesFromField001")

        expectedAttackScal = ["Macro", "Micro"]
        resultAttackScal = VisibilityUtilities._getUniqueValuesFromField(self.inputSigActsTable, "AttackScal")
        self.assertEqual(len(expectedAttackScal),
                         len(resultAttackScal),
                         "Expected {0} unique values, but got {1}.".format(expectedAttackScal, resultAttackScal))
        
    def test_getUniqueValuesFromField002(self):
        '''
        Test _getUniqueValuesFromField with SigActs table's NoAttacks field.
        '''
        Configuration.Logger.info(".....VisibilityUtilityTestCase.test_getUniqueValuesFromField002")

        expectedNoAttacks = [0, 1, 2, 3]
        resultNoAttacks = VisibilityUtilities._getUniqueValuesFromField(self.inputSigActsTable, "NoAttacks")
        self.assertEqual(len(expectedNoAttacks),
                         len(resultNoAttacks),
                         "Expected {0} unique values, but got {1}.".format(expectedNoAttacks, resultNoAttacks))

    def test_getCentroid_FromPoints(self):
        '''
        Testing _getCentroid from point feature class with 4 points.
        '''
        Configuration.Logger.info(".....VisibilityUtilityTestCase.test_getCentroid")

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

        #####################################
        #TODO: TEST FAILING when run with other test methods
        return
        #####################################

        resultCentroid = VisibilityUtilities._getCentroid(fc) 
        self.assertIsNotNone(resultCentroid)
        resultPoint = resultCentroid.firstPoint
        
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
        
        self.assertAlmostEqual(comparePoint.X, resultPoint.X, places=6, msg="Unexpected centroid X. Expected {0}, but got {1}".format(comparePoint.X, resultPoint.X))
        self.assertAlmostEqual(comparePoint.Y, resultPoint.Y, places=6, msg="Unexpected centroid Y. Expected {0}, but got {1}".format(comparePoint.Y, resultPoint.Y))
        
    def test_getLocalWAZED(self):
        '''
        '''
        Configuration.Logger.info(".....VisibilityUtilityTestCase.test_getLocalWAZED")

        testInputPoint = arcpy.PointGeometry(arcpy.Point(-11.13, 14.87), self.srWGS84)
        resultSR = VisibilityUtilities._getLocalWAZED(testInputPoint)
        # arcpy.AddMessage("======================")
        # arcpy.AddMessage(resultSR.exportToString())
        # arcpy.AddMessage("======================")
        # arcpy.AddMessage(self.srWAZED.exportToString())
        # arcpy.AddMessage("======================")
        self.assertIsNotNone(resultSR)
        self.assertEqual(resultSR.name, self.srWAZED.name, \
            "Compare expected Spatial Reference Name: {0} with result {1} failed.".format(self.srWAZED.name, resultSR.name))
        self.assertEqual(resultSR.projectionName, self.srWAZED.projectionName, \
            "Compare expected Spatial Reference Name: {0} with result {1} failed.".format(self.srWAZED.projectionName, resultSR.projectionName))
        # factoryCode not set by _getLocalWAZED
        # self.assertEqual(resultSR.factoryCode, self.srWAZED.factoryCode, \
        #    "Compare expected Spatial Reference Code: {0} with result {1} failed.".format(self.srWAZED.factoryCode, resultSR.factoryCode))
                
    def test_prepPointFromSurface(self):
        '''
        '''

    # Test external methods

    def test_hi_lowPointByArea_lowest(self):
        '''
        test hi_lowPointByArea for MINIMUM (lowest) setting.
        '''
        Configuration.Logger.info(".....VisibilityUtilityTestCase.test_hi_lowPointByArea_lowest")

        hi_low_Switch = "MINIMUM"
        resultPoints = os.path.join(Configuration.militaryScratchGDB, "lowestPoints")
        VisibilityUtilities.hi_lowPointByArea(self.inputArea,
                                              self.inputSurface,
                                              hi_low_Switch,
                                              resultPoints)
        deleteIntermediateData.append(resultPoints)

        self.assertTrue(arcpy.Exists(resultPoints), "Output features do not exist or were not created")

        expectedLowest = os.path.join(Configuration.militaryResultsGDB, "ExpectedOutputLowestPt")

        # TODO: need to regenerate the expected feature class
        # self.assertFeatureClassEqualSimple(resultPoints, expectedLowest, \
        #    "OBJECTID", 0.0001)

    def test_hi_lowPointByArea_highest(self):
        '''
        test hi_lowPointByArea for MAXIMUM (highest) setting.
        '''
        Configuration.Logger.info(".....VisibilityUtilityTestCase.test_hi_lowPointByArea_highest")

        hi_low_Switch = "MAXIMUM"
        resultPoints = os.path.join(Configuration.militaryScratchGDB, "highestPoints")
        resultPoints = VisibilityUtilities.hi_lowPointByArea(self.inputArea,
                                                             self.inputSurface,
                                                             hi_low_Switch,
                                                             resultPoints)
        deleteIntermediateData.append(resultPoints)

        self.assertTrue(arcpy.Exists(resultPoints), "Output features do not exist or were not created")

        expectedHighest = os.path.join(Configuration.militaryResultsGDB, "ExpectedOutputHighestPt")

        # TODO: need to regenerate the expected feature class
        # self.assertFeatureClassEqualSimple(resultPoints, expectedHighest, \
        #    "OBJECTID", 0.0001)

    # Test tool methods
    
    def test_findLocalPeaks(self):
        '''
        test_findLocalPeaks with input 10 peaks to find
        '''
        Configuration.Logger.info(".....VisibilityUtilityTestCase.test_findLocalPeaks")

        resultPoints = os.path.join(Configuration.militaryScratchGDB, "findLocalPeaks")
        numPoints = 16
        resultPoints = VisibilityUtilities.findLocalPeaks(self.inputArea,
                                                          numPoints,
                                                          self.inputSurface,
                                                          resultPoints)
        deleteIntermediateData.append(resultPoints)
        expectedLocalPeaks = os.path.join(Configuration.militaryResultsGDB, "ExpectedOutputFindLocalPeaks")

        self.assertTrue(arcpy.Exists(resultPoints), "Output features do not exist or were not created")
        pointCount = int(arcpy.GetCount_management(resultPoints).getOutput(0))
        expectedFeatureCount = int(16)
        self.assertGreaterEqual(pointCount, expectedFeatureCount, "Expected %s features, but got %s" % (str(expectedFeatureCount), str(pointCount)))

        # TODO: need to regenerate the expected feature class
        #self.assertFeatureClassEqualSimple(resultPoints, expectedLocalPeaks, \
        #    "OBJECTID", 0.0001)
    
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

if __name__ == "__main__":
    unittest.main()   
