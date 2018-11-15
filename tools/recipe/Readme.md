# Conda Packaging of militarytools Library

This folder contains the files necessary to build the militarytools Conda Package. 

## Requirements

1. ArcGIS Pro (includes Conda)
2. Conda **conda-build** package installed in **the Conda root environment**
    1. If you do not have conda-build installed 
    2. Go to: `C:\Program Files\ArcGIS\Pro\bin\Python\Scripts`
    3. Run `proenv.bat` **As Administrator**
    4. `activate root`
    5. `conda install conda-build`

## Steps

1. Run the Windows batch file: [mt-conda-build.bat](./mt-conda-build.bat)
2. Ensure there are no errors
3. Obtain the built package from the folder `recipe\bld\win-64`


