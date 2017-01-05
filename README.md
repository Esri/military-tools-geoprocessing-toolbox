# military-tools-geoprocessing-toolbox
is a collection of models, scripts, and tools for use in ArcGIS for Desktop and ArcGIS Pro. This toolbox is one component that is a part of the Military Tools Product. 

![screenshot of tools](m-t-g-t_screenshot_600x400.png)

## Sections
* [Features](#features)
* [Requirements](#requirements)
* [Instructions](#instructions)
* [Issues](#issues)
* [Contact](#contact)
* [Contributing](#contributing)
* [Resources](#resources)
* [Licensing](#licensing)

## Features

This is an ArcGIS Geoprocessing Toolbox that contains collections of tools to import geometry from tables, determine ranges, and provide basic visibility analysis capabilities.

### Contents

* [Repository contents list](./Contents.md)

## Requirements

Tools for ArcMap are in the **Military_Tools_arcmap.tbx** toolbox and have the following requirements:

* **ArcGIS 10.3.1 for Desktop**
* **ArcGIS 10.4 for Desktop**
* **ArcGIS 10.4.1 for Desktop**


Tools for ArcGIS Pro are in the **Military_Tools_pro.tbx** toolbox and have the following requirements: 

* **ArcGIS Pro 1.2**
* **ArcGIS Pro 1.3**
* **ArcGIS Pro 1.4**

Additionally there are additional extensions needed for certain tools:

* Requires **ArcGIS Spatial Analyst**:
	* Find Local Peaks
	* Highest Points
	* Lowest Points
	* Radial Line Of Sight

* Requires **ArcGIS Spatial Analyst** *and* **ArcGIS 3D Analyst**:
	* Linear Line Of Sight

## Instructions

* [New to Github? Get started here.](http://htmlpreview.github.com/?https://github.com/Esri/esri.github.com/blob/master/help/esri-getting-to-know-github.html)
* [Intstructions on running the tests for this repository](./utils/test/Readme.md)
* [Want to help update the tools in this repository?](https://github.com/esri/contributing)

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
	* create a **New Pull Request** against the *dev* branch

Please see Esri general [guidelines for contributing](https://github.com/esri/contributing).

### Repository Points of Contact

Repository Owner: [Matt Funk](https://github.com/mfunk)

* Merge Pull Requests
* Creates Releases and Tags
* Manages Milestones
* Manages and Assigns Issues

Secondary Contact: [Lyle Wright](https://github.com/topowright)

* Backup when the Owner is away

## Resources

* [ArcGIS 10.3 Help](http://resources.arcgis.com/en/help/)
* [ArcGIS Blog](http://blogs.esri.com/esri/arcgis/)
* ![Twitter](https://g.twimg.com/twitter-bird-16x16.png)[@EsriDefense](http://twitter.com/EsriDefense)
* [ArcGIS Solutions Website](http://solutions.arcgis.com/military/)

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
