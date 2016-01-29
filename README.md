![Image of repository-template](MilitaryAnalystGraphic.png)

# MilitaryAnalyst-Geoprocessing-Toolbox
is a collection of models, scripts, and tools for use in ArcGIS for Desktop and ArcGIS Pro. This toolbox is one component that is a part of the Military Analyst Product. 

## Features

This is an ArcGIS Geoprocessing Toolbox that contains collections of tools to import geometry from tables, determine ranges, and basic visibility analysis.

### Contents
* [toolboxes]
	* Military Analyst Tools.tbx
		* Conversion
			* Convert Coordinates
			* Table To 2-Point Line
			* Table To Ellipse
			* Table To Line Of Bearing
			* Table To Point
			* Table To Polygon
			* Table To Polyline
		* Geodesy and Range
			* Range Rings
		* Source Scripts
			* Add Unique Row ID
			* Polyline To Polygon
			* sourceCC
			* sourceRR
	* [scripts]
		* AddUniqueRowID.py
		* ConvertCoordinates.py
		* PolylineToPolygon.py
		* RangeRings.py
	* [layers]
		* RangeRadials.lyr
		* RangeRings.lyr
* [testdata]
	* [MATestData.gdb]
		* ellipsewizard - preliminary test data - DO NOT DISTRIBUTE
		* linewizard- preliminary test data - DO NOT DISTRIBUTE
		* lobwizard- preliminary test data - DO NOT DISTRIBUTE
		* pointwizard- preliminary test data - DO NOT DISTRIBUTE
		* sampleRangePoints- preliminary test data - DO NOT DISTRIBUTE
		* SigActs- preliminary test data - DO NOT DISTRIBUTE
	* ellipsewizard.csv - preliminary test data - DO NOT DISTRIBUTE
	* linewizard.csv - preliminary test data - DO NOT DISTRIBUTE
	* lobwizard.csv - preliminary test data - DO NOT DISTRIBUTE
	* pointwizard.csv - preliminary test data - DO NOT DISTRIBUTE
	* SigActs.csv - preliminary test data - DO NOT DISTRIBUTE

## Sections

* [Requirements](#requirements)
* [Instructions](#instructions)
* [Issues](#issues)
* [Contact](#contact)
* [Contributing](#contributing)
* [Resources](#resources)
* [Licensing](#licensing)

## Requirements

* ArcGIS Desktop 10.3.1

## Instructions

* [New to Github? Get started here.](http://htmlpreview.github.com/?https://github.com/Esri/esri.github.com/blob/master/help/esri-getting-to-know-github.html)

### Testing the tools
In this case testing is to take the tools from the repository and report success and failure (log issues) without modifying the tools, or modifying the source code.

1. Click the **Download Zip** button.
2. Extract the ZIP tools to a working folder
3. Use the included [testdata] to manually test each tool
4. Log [issues](https://github.com/ArcGIS/MilitaryAnalyst-Geoprocessing-Toolbox/issues) for any problems found (if they haven't been logged already)

### Building the tools
Building the tools means modifying existing tools or adding new tools. In this case you should be familiar with GitHub and creating geoprocessing tools.

1. Fork the "dev" branch.
2. Clone it to your local machine
3. Make your changes locally
4. Commit your changes and Sync with your remote
5. Create a Pull Request to have your updates merged to "dev"

## Issues

Find a bug or want to request a new feature?  Please let us know by submitting an [issue]().
Please note that issues might be copied or transferred to other repositories as needed.

### Contact

The primary Point of Contact (POC) for Issues/Contributions to this Repository is:

* [Matt Funk](https://github.com/mfunk)

Secondary POC:

* [Lyle Wright](https://github.com/topowright)

## Contributing

Esri welcomes contributions from anyone and everyone. Please see our [guidelines for contributing](https://github.com/esri/contributing).

## Resources

* [Solution's Guide to Creating Geoprocessing Tools](https://github.com/ArcGIS/Solutions-Resources/blob/master/Python/Style/SolutionsGuideToCreatingGeoprocessingTools.md)

### Related repositories
* [solutions-geoprocessing-toolbox](https://github.com/Esri/solutions-geoprocessing-toolbox)
* [solutions-webappbuilder-widgets](https://github.com/Esri/solutions-webappbuilder-widgets)
* [coordinate-tool-addin-dotnet](https://github.com/Esri/coordinate-tool-addin-dotnet)
* [geodesy-and-range-addin-dotnet](https://github.com/ArcGIS/geodesy-and-range-addin-dotnet)

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

[](Esri Tags: ArcGISSolutions Military Defense {TODO-ADD-OTHERS} )
[](Esri Language: Python)