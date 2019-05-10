$ErrorActionPreference = 'Stop'
Set-PSDebug -Trace 2

# Download GAMS
Start-FileDownload 'https://d37drm4t2jghv5.cloudfront.net/distributions/25.1.1/windows/windows_x64_64.exe'

# Install GAMS
& ".\windows_x64_64.exe" "/SP- /NORESTART /DIR=.\gams /NOICONS"

$env:PATH = $(Get-Location).Path + '\gams;' + $env:PATH

# Update conda

# These correspond to folder naming of miniconda installs on appveyor
# See https://www.appveyor.com/docs/windows-images-software/#miniconda
if ( $env:PYTHON_VERSION -eq '2.7' ) {
  $MC_PYTHON_VERSION = ''
} else {
  $MC_PYTHON_VERSION = $env:PYTHON_VERSION.Replace('.', '')
}
if ( $env:PYTHON_ARCH -eq '64' ) { $ARCH_LABEL = '-x64' }

$CR = 'C:\Miniconda' + $MC_PYTHON_VERSION + $ARCH_LABEL

$env:CONDA_ROOT = $CR
$env:PATH = $CR + ';' + $CR + '\Scripts;' + $CR + '\Library\bin;' + $env:PATH

Write-Output $env:PATH

conda update --yes conda 2>&1

# TODO create a 'testing' env as on Travis?

conda install -c conda-forge --yes ixmp pytest coveralls pytest_cov 2>&1
conda remove --force --yes ixmp 2>&1

# Show information
conda info --all


# # Set up r-appveyor
# Bootstrap
#
# # Install R packages needed for testing
# travis-tool.sh install_r devtools IRkernel
# Rscript -e "IRkernel::installspec()"
