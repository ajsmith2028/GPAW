Installation instructions
=========================

CCV module version
------------------

As of this writing (2021-06-28), the last CCV module version was 21.1.0.
Therefore, if you'd like to use versionn 21.6.0 or newer, you can just follow the custom installation instructions below.

Custom installation
-------------------

If you'd like the latest development version; for example to use or test new features, or better to have your own copy to hack on, these instructions should work.
You should also have a look at the official instructions on the [GPAW website](https://wiki.fysik.dtu.dk/gpaw/devel/developer_installation.html).


Here, we'll create everything in a standalone environment, such that when you want to use gpaw later you can do so by calling the command `loadgpawdeveloper`.
We'll assume you already have ASE installed, which is located at `/path/to/my/ase`.
(If you want to be careful, your ASE version should be ASE-3.21.1 to match GPAW version 21.6.0.)
These instructions are based off of how Paul Hall installed `gpaw/21.1.0_openmpi_4.0.5_gcc_10.2_slurm20` on the CCV in June 2021.
Note that these instructions use the environment variables (mpi, etc.) created for 21.1.0, which seem to work fine with 21.6.0.
These instructions are virtually identical to those of 21.1.0, just with version numbers updated.

First load the necessary modules:

```bash
module load mpi/openmpi_4.0.5_gcc_10.2_slurm20 gcc/10.2 intel/2020.2 python/3.9.0
```

I'll assume you are installing GPAW in `~/usr/installs`.
You will create a python virtual environment (`venv`) within that directory and install the needed python packages.
(Note that whatever you pick for `GPAWPATH` needs to be the *permanent* installation location; you can't easily move it later.)

```bash
GPAWPATH=$HOME/usr/installs/gpaw
mkdir -p $GPAWPATH
cd $GPAWPATH
python3 -m venv gpaw-venv
source gpaw-venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install numpy
python3 -m pip install scipy
python3 -m pip install matplotlib
python3 -m pip install ipython
python3 -m pip install flake8
python3 -m pip install pytest
python3 -m pip install pytest-xdist
```

Paul installed the tricky things we need, FFTW and libxc for us, and we can pick those up by setting the environment variables as below.
Note that there is a bug in libxc version 5.0.0, so this uses a 4.x version.

```bash
export C_INCLUDE_PATH=/gpfs/runtime/opt/gpaw/21.1.0_openmpi_4.0.5_gcc_10.2_slurm20/depends/include:$C_INCLUDE_PATH
export LIBRARY_PATH=/gpfs/runtime/opt/gpaw/21.1.0_openmpi_4.0.5_gcc_10.2_slurm20/depends/lib:$LIBRARY_PATH
export LD_LIBRARY_PATH=/gpfs/runtime/opt/gpaw/21.1.0_openmpi_4.0.5_gcc_10.2_slurm20/depends/lib:$LD_LIBRARY_PATH
export PATH=/gpfs/runtime/opt/gpaw/21.1.0_openmpi_4.0.5_gcc_10.2_slurm20/depends/bin:$PATH
```

Add ASE to your python path, if it's not there already.
This assumes you already have ASE installed at `/path/to/my/ase`.
(As noted above, the "correct" version of ASE for this version of GPAW is ASE-3.21.1, but this is usually quite forgiving.)

```bash
ASEPATH=/path/to/my/ase
export PATH="$ASEPATH/tools:$PATH"
export PATH="$ASEPATH/bin:$PATH"
export PYTHONPATH="$ASEPATH:$PYTHONPATH"
complete -o default -C "$GPAWPATH/gpaw-venv/bin/python3 $ASEPATH/ase/cli/complete.py" ase
```

We've stored the configuration files and submission scripts that are unique to Brown in the "brown-gpaw" repository.
(Presumably, you are reading this file from within this repository!)
Clone this so you can get these files, using one of the two modes below.

```bash
git clone git@bitbucket.org:andrewpeterson/brown-gpaw.git
#git clone https://bitbucket.org/andrewpeterson/brown-gpaw.git
```

Download GPAW into a local folder, which we'll call `source`.
Choose one of the methods below, depending on if you want the latest development version, the exact stable 21.6.0 version, or your own development version.
Also copy our own version of `siteconfig.py` to this directory.
*Note:* If you are planning on working on a merge request, make sure to clone your own version of gpaw!
E.g., `git clone git@gitlab.com:andrew_peterson/gpaw.git`.

```bash
mkdir source
cd source
git clone https://gitlab.com/gpaw/gpaw.git  # Latest development version
#git clone -b 21.6.0 https://gitlab.com/gpaw/gpaw.git  # Exact 21.6.0 version
#git clone git@gitlab.com:andrew_peterson/gpaw.git  # E.g., your own development version
cd gpaw
cp ../../brown-gpaw/21.6.0/siteconfig.py .
```

Cross your fingers, and install with

```bash
python3 -m pip install --editable .
```

(If you are developing GPAW: The `--editable` flag means that the installation will point to the git source files, so you don't have to re-install every time you change something in python. If you are installing a permanent version, you can leave this flag off. It doesn't really matter in that case.)

Check that the installation exists, install the PAW setups, and test:

```bash
cd $GPAWPATH
gpaw info  # Checks where stuff is installed.
gpaw install-data .  # Installs the setups. Probably say 'y' to register the path.
gpaw info  # Make sure the new setup directory shows up.
gpaw test
gpaw -P 4 test
```

If you are doing something fancy, you may want to run the complete test suite, which will take some hours:

```bash
cd source/gpaw
pytest -v
# Or better, submit it as a job to the queue as:
cp ../../brown-gpaw/21.6.0/run-gpaw-tests.py .
sbatch run-gpaw-tests.py
```

If all looks good, you now have a functional copy.
Now you should make a command to load it whenever you want to run a job.
Add the following to your `.bashrc` (making sure your ASE path is right):

```bash
loadgpawdeveloper(){
ASEPATH=/path/to/my/ase
GPAWPATH=$HOME/usr/installs/gpaw
module load mpi/openmpi_4.0.5_gcc_10.2_slurm20 gcc/10.2 intel/2020.2 python/3.9.0
source $GPAWPATH/gpaw-venv/bin/activate
export PATH="$ASEPATH/tools:$PATH"
export PATH="$ASEPATH/bin:$PATH"
export PYTHONPATH="$ASEPATH:$PYTHONPATH"
complete -o default -C "$GPAWPATH/gpaw-venv/bin/python3 $ASEPATH/ase/cli/complete.py" ase
export C_INCLUDE_PATH=/gpfs/runtime/opt/gpaw/21.1.0_openmpi_4.0.5_gcc_10.2_slurm20/depends/include:$C_INCLUDE_PATH
export LIBRARY_PATH=/gpfs/runtime/opt/gpaw/21.1.0_openmpi_4.0.5_gcc_10.2_slurm20/depends/lib:$LIBRARY_PATH
export LD_LIBRARY_PATH=/gpfs/runtime/opt/gpaw/21.1.0_openmpi_4.0.5_gcc_10.2_slurm20/depends/lib:$LD_LIBRARY_PATH
export PATH=/gpfs/runtime/opt/gpaw/21.1.0_openmpi_4.0.5_gcc_10.2_slurm20/depends/bin:$PATH
}
```

You will also need submit files that you use to submit your python scripts.
You can copy them into your bin directory as

```bash
cp $GPAWPATH/brown-gpaw/21.6.0/gpaw-debug-submit $GPAWPATH/gpaw-venv/bin/gpaw-debug-submit
cp $GPAWPATH/brown-gpaw/21.6.0/gpaw-submit $GPAWPATH/gpaw-venv/bin/gpaw-submit
```

Then you should be able to submit jobs as normal, like

```bash
loadgpawdeveloper # you only need to run this once per session
gpaw-debug-submit -c 4 -t 0:15:00 run.py
```

CCV Installation Notes
======================

For archival purposes, the file CCVREADME is one created by the CCV which contains the installation procedure that the CCV used in installing this.
Note that this file is contained in the 20.1.0 folder, as this version uses the identical CCV install files.
