The military-tools-geoprocessing-toolbox repository contains the following folders, files, and data.

* [toolboxes](./toolboxes)
	* Military Tools.tbx (same tools as below)
	* Military Tools_10.3.tbx
		* Conversion
			* Convert Coordinates
			* Table To 2-Point Line
			* Table To Ellipse
			* Table To Line Of Bearing
			* Table To Point
			* Table To Polygon
			* Table To Polyline
		* Distance and Direction
			* Range Rings (from Interval)
			* Range Rings from Minimum Maximum
			* Range Rings from Minimum Maximum Table
		* Source Scripts
			* Add Unique Row ID
			* Attach Profile Graph To LLOS
			* Polyline To Polygon
			* sourceCC
			* sourceRLOSscript
		* Visibility
			* Add LLOS Fields
			* Add RLOS Observer Fields
			* Linear Line Of Sight
			* Radial Line Of Sight
			* Find Local Peaks
			* Highest Points
			* Lowest Point
	* [scripts](./toolboxes/scripts)
		* AddUniqueRowID.py
		* ConvertCoordinates.py
		* LLOSProfileGraphAttachments.py
		* PolylineToPolygon.py
		* RangeRingsUtils.py
		* RangeRingFromMinMaxTable.py
		* RangeRingMinMax.py
		* RangeRingsFromInterval.py
		* RLOS.py
	* [layers](./toolboxes/layers)
		* Highest Point Output.lyr
		* Linear Line of Sight Output.lyr
		* LinearLineOfSight.lyrx
		* LLOS_Output_Observers.lyr
		* LLOS_Output_Observers.lyrx
		* LLOS_Output_Targets.lyr
		* LLOS_Output_Targets.lyrx
		* LLOS_OutputLLOS.lyr
		* LLOS_OutputLLOS.lyrx
		* LLOS_OutputSightLines.lyr
		* LLOS_OutputSightLines.lyrx
		* Lowest Point Output.lyr
		* Radial Line Of Sight Output.lyr
		* RadialLineOfSightOutput.lyrx
		* RangeRadials.lyr
		* RangeRingInputObserver.lyr
		* RangeRings.lyr
		* SightLines.lyrx
	* [tooldata](./toolboxes/tooldata)
		* [Range Rings.gdb]
			* rrInputTable
* [testdata](./testdata)
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
	* [test]
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
		
