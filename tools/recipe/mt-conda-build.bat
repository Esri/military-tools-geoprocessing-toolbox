echo off
setlocal ENABLEEXTENSIONS

SET condaroot=C:\Program Files\ArcGIS\Pro\bin\Python\Scripts

:: Check that conda-build exists
if exist "%condaroot%\conda-build.exe" goto prereqs_exists_ok

echo ***************************************
echo ERROR: conda-build is not installed at: "%condaroot%"
echo ***************************************

goto :EOF

:prereqs_exists_ok

@set outname=%~dp0bld
rmdir "%outname%" /s /q
mkdir "%outname%"
cd "%condaroot%"
conda-build "%~dp0meta.yaml" --output-folder "%outname%"
