Param([string]$package)
$ErrorActionPreference = 'Stop'

# The easiest thing to do would be 'conda config --set anaconda_upload yes', but we cannot set the label this way during upload.

# Grab the location where the package will be created.
$path = $(conda build $package --output-folder .\conda_output --output).Split()[-1]
conda build $package --output-folder .\conda_output
anaconda --token .\token upload $path --label "main"