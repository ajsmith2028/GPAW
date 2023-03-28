
# Environment, including MPI and FFTW.

module load mpi/openmpi_4.0.7_gcc_10.2_slurm22 gcc/10.2 intel/2020.2 python/3.9.0

export C_INCLUDE_PATH=/gpfs/runtime/opt/gpaw/21.1.0_openmpi_4.0.5_gcc_10.2_slurm20/depends/include:$C_INCLUDE_PATH
export LIBRARY_PATH=/gpfs/runtime/opt/gpaw/21.1.0_openmpi_4.0.5_gcc_10.2_slurm20/depends/lib:$LIBRARY_PATH
export LD_LIBRARY_PATH=/gpfs/runtime/opt/gpaw/21.1.0_openmpi_4.0.5_gcc_10.2_slurm20/depends/lib:$LD_LIBRARY_PATH
export PATH=/gpfs/runtime/opt/gpaw/21.1.0_openmpi_4.0.5_gcc_10.2_slurm20/depends/bin:$PATH


# Make high-level installation directory.
INSTALLPATH=$HOME/installs
mkdir -p $INSTALLPATH
cd $INSTALLPATH

# Install libvdwxc.
mkdir -p $INSTALLPATH/libvdwxc-source
cd $INSTALLPATH/libvdwxc-source
wget https://launchpad.net/libvdwxc/stable/0.4.0/+download/libvdwxc-0.4.0.tar.gz
tar -xzvf libvdwxc-0.4.0.tar.gz
rm libvdwxc-0.4.0.tar.gz
cd libvdwxc-0.4.0
mkdir local-build
cd local-build
../configure --with-mpi --prefix="$INSTALLPATH/libvdwxc"
make -j4   # Run make using 4 processors
make check
make install

# Install ASE.
ASEPATH=$INSTALLPATH/ase
mkdir -p $ASEPATH
cd $ASEPATH
git clone -b 3.22.1 https://gitlab.com/ase/ase.git  # for version 3.22.1

# Install GPAW's virtual environment and python packages.
GPAWPATH=$INSTALLPATH/gpaw
mkdir -p $GPAWPATH
cd $GPAWPATH
python3 -m venv gpaw-venv
source gpaw-venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install numpy
python3 -m pip install scipy
python3 -m pip install matplotlib
# Below are optional, mostly for those doing development.
python3 -m pip install ipython  # for interactive python shell
python3 -m pip install flake8  # for code style / bug checking
python3 -m pip install pytest  # for unit tests
python3 -m pip install pytest-xdist  # for unit tests
python3 -m pip install sphinx  # for documentation building
python3 -m pip install sphinx-rtd-theme  # for documentation building

# Link to ASE.
export PATH="$ASEPATH/tools:$PATH"
export PATH="$ASEPATH/bin:$PATH"
export PYTHONPATH="$ASEPATH/ase:$PYTHONPATH"
complete -o default -C "$GPAWPATH/gpaw-venv/bin/python3 $ASEPATH/ase/ase/cli/complete.py" ase

# Get siteconfig and stuff.
git clone git@bitbucket.org:andrewpeterson/brown-gpaw.git

# Download GPAW.
mkdir source
cd source
git clone https://gitlab.com/gpaw/gpaw.git  # Latest development version
#git clone -b 22.8.0 https://gitlab.com/gpaw/gpaw.git  # Exact 22.8.0 version
#git clone git@gitlab.com:andrew_peterson/gpaw.git  # E.g., your own development version
cd gpaw
cp ../../brown-gpaw/22.8.0/siteconfig.py .

# Now edit siteconfig.py to include libvdwxc and right path!

# Install.
python3 -m pip install --editable .
