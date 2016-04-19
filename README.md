# military-tools-geoprocessing-toolbox
is a collection of models, scripts, and tools for use in ArcGIS for Desktop and ArcGIS Pro. This toolbox is one component that is a part of the Military Tools Product. 

## Features

This is an ArcGIS Geoprocessing Toolbox that contains collections of tools to import geometry from tables, determine ranges, and basic visibility analysis.

### Contents
* [toolboxes]
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
			* Polyline To Polygon
			* sourceCC
			* sourceRLOSscript
		* Terrain
			* Find Local Peaks
			* Highest Points
			* Lowest Point
		* Visibility
			* Linear Line Of Sight
			* Radial Line Of Sight
	* [scripts]
		* AddUniqueRowID.py
		* ConvertCoordinates.py
		* PolylineToPolygon.py
		* RangeRingsUtils.py
		* RangeRingFromMinMaxTable.py
		* RangeRingMinMax.py
		* RangeRingsFromInterval.py
		* RLOS.py
	* [layers]
		* Highest Point Output.lyr
		* Linear Line of Sight Output.lyr
		* Lowest Point Output.lyr
		* Radial Line Of Sight Output.lyr
		* RangeRadials.lyr
		* RangeRingInputObserver.lyr
		* RangeRings.lyr
	* [tooldata]
		* [Range Rings.gdb]
			* rrInputTable
* [testdata]
	* DataCreditsforMilitaryToolsGeoprocessingToolbox.txt
	* USGS SRTMData Citation_1.pdf
	* [MilitaryToolsTestData.gdb]
		* ElevationSurface - surface data
		* sampleRangePoints- sample point test data
		* SigActs - event test dta 
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

## Sections

* [Requirements](#requirements)
* [Instructions](#instructions)
* [Issues](#issues)
* [Contact](#contact)
* [Contributing](#contributing)
* [Resources](#resources)
* [Licensing](#licensing)

## Requirements

* ArcGIS Desktop 10.3.1 and Python 2.7
* ArcGIS Pro 1.3 and Python 3.4

## Instructions

* [New to Github? Get started here.](http://htmlpreview.github.com/?https://github.com/Esri/esri.github.com/blob/master/help/esri-getting-to-know-github.html)

### Testing the tools
In this case testing is to take the tools from the repository and report success and failure (log issues) without modifying the tools, or modifying the source code.

1. Click the **Download Zip** button.
2. Extract the ZIP tools to a working folder
3. Use the included [testdata] to manually test each tool
4. Log [issues](https://github.com/Esri/military-tools-geoprocessing-toolbox/issues) for any problems found (if they haven't been logged already)

### Building the tools
Building the tools means modifying existing tools or adding new tools. In this case you should be familiar with GitHub and creating geoprocessing tools.

1. Create a new branch from "dev" branch:
	* Include your initials in the branch name, eg. *"mf-new-tool"*
2. Clone it to your local machine
3. Make your changes locally
4. Commit your changes and Sync with your remote
5. Create a Pull Request to have your updates merged to "dev"

## Issues

Find a bug or want to request a new feature?  Please let us know by submitting an [issue](https://github.com/Esri/military-tools-geoprocessing-toolbox/issues).
Please note that issues might be copied or transferred to other repositories as needed.

1. Use a concise, one-line title
2. The Description should include:
	* A *detailed* description of what the problem or question is, what was expected, what differed.
	* A *numbered* list of steps to reproduce the problem (don't assume the person fixing the issue will know how to reproduce the problem)
	* Screenshots are helpful
	* blocks of script/code (if necessary)
4. Add labels:
	* Add the gray label **"-1 - Add To Backlog"**
	* Add one label from the red/pink **"B"** category (eg. "B - Bug")
	* Add one label from the green **"F"** category (eg. "F - Geodesy")
	* Add one label from the purple **"V"** category (eg. "V - 10.3.1")

## Contact

The primary Point of Contact (POC) for Issues/Contributions to this Repository is:

* [Matt Funk](https://github.com/mfunk)

Secondary POC:

* [Lyle Wright](https://github.com/topowright)

## Contributing

Esri welcomes contributions from anyone and everyone. Please see our [guidelines for contributing](https://github.com/esri/contributing).

## Resources

### Related repositories
* [solutions-geoprocessing-toolbox](https://github.com/Esri/solutions-geoprocessing-toolbox)
* [solutions-webappbuilder-widgets](https://github.com/Esri/solutions-webappbuilder-widgets)
* [coordinate-conversion-addin-dotnet](https://github.com/Esri/coordinate-conversion-addin-dotnet)
* [distance-direction-addin-dotnet](https://github.com/Esri/distance-direction-addin-dotnet)

## Licensing

Copyright 2016 Esri

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

A copy of the license is available in the repository's
[license.txt](license.txt) file.

[](Esri Tags: ArcGISSolutions Military Defense)
[](Esri Language: Python)