# Install GAMS
$CACHE/$GAMSFNAME > install.out

# Show location
which gams


# Install and update conda
$CACHE/$CONDAFNAME -b -p $HOME/miniconda
conda update --yes conda

# Create named env
conda create -n testing python=$PYVERSION --yes

# Install deps
conda install -n testing -c conda-forge --yes \
      ixmp \
      pytest \
      coveralls \
      pytest-cov
conda remove -n testing --force --yes ixmp

# Show information
conda info --all


# Install R packages needed for testing
echo 'options(repos=c("https://cloud.r-project.org"))' >$R_PROFILE
Rscript -e 'install.packages("devtools")'
Rscript -e 'devtools::install_dev_deps("retixmp/source")'
