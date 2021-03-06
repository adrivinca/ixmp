# Installation script for Linux/macOS CI on Travis

# GAMS: install
$CACHE/$GAMSFNAME > install.out

# Show location
which gams


# Miniconda: install
# -b: run in batch mode with no user input
# -u: update existing installation
# -p: install prefix
$CACHE/$CONDAFNAME -b -u -p $HOME/miniconda

# Configure:
# - give --yes for every command
# - search conda-forge in addition to the default channels, for e.g. JPype
conda config --set always_yes true
conda config --append channels conda-forge

# Update conda and packages in the base environment
conda update --quiet --name base conda

# Create and activate a named environment for testing
conda create --name testing python=$PYVERSION pip
. activate testing

# Install dependencies
conda install --name testing --file ci/conda-requirements.txt
# pip install --requirement ci/pip-requirements.txt

# Show information
conda info --all

# Install IR kernel spec for Jupyter notebook
Rscript -e "IRkernel::installspec()"
