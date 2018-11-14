@set outname=%~dp0bld
rmdir %outname% /s /q
mkdir %outname%
cd "C:\Program Files\ArcGIS\Pro\bin\Python\Scripts"
conda-build "%~dp0meta.yaml" --output-folder "%outname%"