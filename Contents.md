The military-tools-geoprocessing-toolbox repository contains the following folders, files, and data.

* [toolboxes](./tools/militarytools/esri/toolboxes)
	* Military Tools.pyt (Python toolbox, containing the tools from **Military_Tools_arcmap.tbx** and **Military_Tools_pro.tbx** toolboxes, plus GRG tools)
		* **Conversion**
			* Convert Coordinates
			* Table To 2-Point Line
			* Table To Ellipse
			* Table To Line Of Bearing
			* Table To Point
			* Table To Polygon
			* Table To Polyline
		* **Distance and Direction**
			* Range Rings (from Interval)
			* Range Rings from Minimum Maximum
			* Range Rings from Minimum Maximum Table
		* **GRG**
			* Create GRG from Area
			* Create GRG from Point
			* Create Reference System GRG from Area	
			* Number Features		
		* **Visibility**
			* Add LLOS Fields
			* Add RLOS Observer Fields
			* Linear Line Of Sight
			* Radial Line Of Sight
			* Find Local Peaks
			* Highest Points
			* Lowest Point
			
	
	* [scripts](./tools/militarytools/esri/toolboxes/scripts)
		* AddLLOSFields.py
		* AddRLOSObserverFields.py
		* ConversionTools.py
		* ConversionUtilities.py
		* ConvertCoordinates.py
		* DistanceAndDirectionTools.py
		* FindLocalPeaks.py
		* GRGTools.py
		* GRGUtilities.py
		* HighestPoints.py
		* LinearLineOfSight.py
		* LowestPoints.py
		* NumberFeaturesTool.py
		* RadialLineOfSight.py
		* RadialLineOfSightAndRange.py
		* RangeRingFromMinMaxTable.py
		* RangeRingMinMax.py
		* RangeRingsFromInterval.py
		* RangeRingUtils.py
		* RefGrid.py
		* TableTo2PointLine.py
		* TableToEllipse.py
		* TableToLineOfBearing.py
		* TableToPoint.py
		* TableToPolygon.py
		* TableToPolyline.py
		* Utilities.py
		* VisibilityUtilities.py
		* VisTools.py
	* [layers](./tools/militarytools/esri/toolboxes/layers)
		* GRG.lyr
		* GRGInputArea.lyr
		* GRGInputPoint.lyr
		* GRG.lyrx
		* Highest Point Output.lyr
		* Highest_Point_Output.lyrx
		* InputArea_FeatureSet.lyr
		* InputArea_FeatureSetGDB.lyr
		* InputArea_FeatureSet.lyrx
		* Linear Line of Sight Output.lyr
		* LinearLineOfSight.lyrx
		* Linear_Line_of_Sight_Output.lyrx
		* LLOS_Output_Observers.lyrx
		* LLOS_Output_Targets.lyrx
		* LLOS_InputObservers.lyr
		* LLOS_InputObserversGDB.lyr
		* LLOS_InputTargets.lyr
		* LLOS_InputTargetsGDB.lyr
		* LLOS_InputObservers.lyrx
		* LLOS_InputTargets.lyrx
		* LLOS_OutputLLOS.lyr
		* LLOS_OutputSightLines.lyr
		* LLOS_Output_Observers.lyr
		* LLOS_Output_Targets.lyr
		* LLOS_OutputLLOS.lyrx
		* LLOS_OutputSightLines.lyrx
		* Lowest Point Output.lyr
		* Lowest_Point_Output.lyrx
		* NumberedStructures.lyr
		* NumberFeaturesAreaInput.lyr
		* NumberedStructures.lyrx
		* OutputRefGrid.lyr
		* RangeRings.lyrx
		* Radial Line Of Sight Output.lyr
		* Radial_Line_Of_Sight_Output.lyrx
		* RangeRadials.lyr
		* RangeRingInputObservers.lyr
		* RangeRingInputObserversGDB.lyr
		* RangeRings.lyr
		* RangeRadials.lyrx
		* RangeRingInputObservers.lyrx
		* RelativeGRGInputArea.lyr
		* RelativeGRGInputPoint.lyr
		* RelativeNumberFeaturesAreaInput.lyr
		* RLOSDonutWedge.lyr
		* RLOSPieWedge.lyr
		* SightLines.lyrx
		* TableToLineOfBearingOutput.lyr
		* TableToLineOfBearingOutput.lyrx

	* [tooldata](./tools/militarytools/esri/toolboxes/tooldata)
		* [Range Rings.gdb]
			* rrInputTable
* [testdata](./utils/testdata)
	* CSV
		* TableTo2PointLine.csv
		* TableToEllipse.csv
		* TabletoLineofBearing.csv
		* TableToPoint.csv
		* TableToPolygon.csv
		* TabletoPolyline.csv
	* DataCreditsforMilitaryToolsGeoprocessingToolbox.txt
	* Elevation
		* USGS SRTMData Citation_1.pdf
		* [SRTM30M]
			* 36.dt2
		* [SRTM90M]
			* [dted]
				* [w121]
					* n35.dt1
					* n36.dt1
				* [w122]
					* n35.dt1
					* n36.dt1
				* [w123]
					* n36.dt1
	* [MilitaryToolsTestData.gdb]
		* ElevationSurface - surface data
		* LLOS_Observers
		* LLOS_Targets
		* RLOS_Observers
		* sampleRangePoints- sample points
		* SigActs - event and coordinate test data 
		* ElevationUTM_Zone10 (elevation data)
	* Results.gdb
		* ExpectedOutputTableToEllipse
		* ExpectedOutputTableToLOB
		* ExpectedOutputTableToPoint
		* ExpectedOutputTableToPolyline
		* Viewshed
* [utils](./utils)
	* [test](./utils/test)
		* TestKickStart.bat
		* TestRunner.py
		* UnitTestUtilities.py
		* Configuration.py
		* Readme.md
		* [conversion_tests]
			* ConversionTestSuite.py
			* ConvertCoordinatesTestCase.py
			* TableToEllipseTestCase.py
			* TableToLineOfBearingTestCase.py
			* TableToPointTestCase.py
			* TableToPolygonTestCase.py
			* TableToPolylineTestCase.py
			* TableToTwoPointLineTestCase.py
		* [distance_tests]
			* RangeRingTestSuite.py
			* RangeRingUtilsTestCase.py
			* RangeRingUtilsTestCase.py
		* [visibility_tests]
			* VisibilityTestSuite.py
			* AddLLOSFieldsTestCase.py
			* AddRLOSObserverFieldsTestCase.py
			* FindLocalPeaksTestCase.py
			* HighestPointsTestCase.py
			* LinearLineOfSiggihtTestCase.py
			* LowestPointsTestCase.py
			* RadialLineOfSightTestCase.py

