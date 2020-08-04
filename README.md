# military-tools-geoprocessing-toolbox
___Beginning at ArcGIS Pro 2.6 this functionality is installed with ArcGIS Pro. This repository will only be updated with critical fixes to ArcGIS Desktop.___


The Military Tools for ArcGIS toolbox is an ArcGIS Python toolbox supporting defense and intelligence workflows. The toolbox is a component of the [Military Tools for ArcGIS product](http://solutions.arcgis.com/defense/help/military-tools/). 

![screenshot of tools](m-t-g-t_screenshot_600x400.png)

## Sections

* [Features](#features)
* [Requirements](#requirements)
* [Instructions](#instructions)
* [Issues](#issues)
* [Contact](#contact-us)
* [Contributing](#contributing)
* [Resources](#resources)
* [Licensing](#licensing)

## Features

The Military Tools for ArcGIS toolbox is an ArcGIS Geoprocessing Python toolbox supporting defense and intelligence workflows such as importing geometry from tables, determining ranges, creating gridded reference graphics, providing visibility analysis, and other capabilities.

### Contents

* [Repository contents list](./Contents.md)

## Requirements

The **Military Tools for ArcGIS** Python toolbox (`.pyt`) has the following requirements:

* **ArcGIS 10.4.1+ for Desktop**

-or-

* **ArcGIS Pro 2.2+**

Additionally there are extensions required to run certain tools:

* Requires **ArcGIS Spatial Analyst**:
	* Find Local Peaks
	* Highest Points
	* Lowest Points
	* Radial Line Of Sight

* Requires **ArcGIS Spatial Analyst**:
	* Linear Line Of Sight

## Instructions

* To use the tools, clone the repository and open the [Python Toolbox]( ./tools/militarytools/esri/toolboxes)
* [Instructions for building the package on Conda](./tools/recipe/Readme.md)
* [Instructions for running the Python tests in this repository](./utils/test/Readme.md)

## Issues

Find a bug or want to request a new feature?  Please let us know by submitting an [issue](https://github.com/Esri/military-tools-geoprocessing-toolbox/issues).
Please note that issues might be copied or transferred to other repositories as needed.

1. Click **New issue**
2. Fill out the issue template with as much detail as possible. Add screenshots as needed.
3. Click **Submit new issue**

## Contributing

Esri welcomes contributions from anyone and everyone.

Repository specific instructions:

* Make a new branch from *dev* branch
* Clone the repository to your local machine
* Make changes on your local machine
* Synchronize changes with your branch often
* When you would like to share your changes:
	* Pull the recent updates from *dev*
	* Create a **New Pull Request** against the *dev* branch

Please see Esri general [guidelines for contributing](https://github.com/esri/contributing).

## Contact Us 

Contact the [Military Tools team](mailto:defensesolutions@esri.com)

## Resources

* [Military Tools for ArcGIS](http://solutions.arcgis.com/defense/help/military-tools/)
* [ArcGIS Solutions Website](http://solutions.arcgis.com/military/)
* [ArcGIS for Defense Downloads](http://appsforms.esri.com/products/download/#ArcGIS_for_Defense)
* [ArcGIS 10.X Help](http://resources.arcgis.com/en/help/)
* [ArcGIS Pro Help](http://pro.arcgis.com/en/pro-app/)
* [ArcGIS Blog](http://blogs.esri.com/esri/arcgis/)

### Related repositories

* [solutions-geoprocessing-toolbox](https://github.com/Esri/solutions-geoprocessing-toolbox)
* [coordinate-conversion-addin-dotnet](https://github.com/Esri/coordinate-conversion-addin-dotnet)
* [distance-direction-addin-dotnet](https://github.com/Esri/distance-direction-addin-dotnet)
* [military-tools-desktop-addins](https://github.com/Esri/military-tools-desktop-addins)

## Licensing

Copyright 2018–2020 Esri

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at:

   http://www.apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

A copy of the license is available in the repository's [license.txt](./License.txt) file.
