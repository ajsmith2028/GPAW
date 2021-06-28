Installation instructions
=========================

CCV module version
------------------

If you are just looking for the standard installation of GPAW, version 21.1.0, then you can use the module installed on the CCV.
You'll need to load a few other libraries and set some environment variables in addition to the modules available on the CCV.
It's simplest to define a bash macro for this.
You can put the following in your `~/.bashrc` file:

```bash
loadgpaw21_1(){
ASEPATH=~/path/to/my/ase
module load gpaw/21.1.0_openmpi_4.0.5_gcc_10.2_slurm20
module load mpi/openmpi_4.0.5_gcc_10.2_slurm20 gcc/10.2 intel/2020.2 python/3.9.0
GPAWPATH=/gpfs/runtime/opt/gpaw/21.1.0_openmpi_4.0.5_gcc_10.2_slurm20/gpaw.venv
source $GPAWPATH/bin/activate
export PATH="$ASEPATH/tools:$PATH"
export PATH="$ASEPATH/bin:$PATH"
export PYTHONPATH="$ASEPATH:$PYTHONPATH"
complete -o default -C "$GPAWPATH/bin/python3 $ASEPATH/ase/cli/complete.py" ase
export C_INCLUDE_PATH=$GPAWPATH/depends/include:$C_INCLUDE_PATH
export LIBRARY_PATH=$GPAWPATH/depends/lib:$LIBRARY_PATH
export LD_LIBRARY_PATH=$GPAWPATH/depends/lib:$LD_LIBRARY_PATH
export LIBRARY_PATH=/users/ap31/data/software/libxc-4.2.3/lib:$LIBRARY_PATH
export LD_LIBRARY_PATH=/users/ap31/data/software/libxc-4.2.3/lib:$LD_LIBRARY_PATH
export C_INCLUDE_PATH=/users/ap31/data/software/libxc-4.2.3/include:$C_INCLUDE_PATH
}
```

Here we are assuming you have your own ASE installed at `~/path/to/my/ase`.
(The official ASE release that accompanies this GPAW version is ASE-3.21.0, if you want to be careful.)

You can use the scripts `gpaw-submit` and `gpaw-debug-submit` to start your jobs, for example like

```bash
gpaw-submit -n 1 -c 24 run.py
```

where `run.py` is the name of the script you would like to run.
You can store `gpaw-submit` and `gpaw-debug-submit` wherever you store your executables.

Custom installation
-------------------

If you'd like the latest development version; for example to use or test new features, or better to have your own copy to hack on, these instructions should work.
You should also have a look at the official instructions on the [GPAW website](https://wiki.fysik.dtu.dk/gpaw/devel/developer_installation.html).

OLD UPDATE ME!!!!!
------------------

Here, we'll create everything in a standalone environment, such that when you want to use gpaw later you can do so by calling the command `load_gpaw`. We'll assume you already have ASE installed, which is located at `/path/to/my/ase`. These instructions are based off of how Paul Hall installed GPAW 20.10 on the CCV. Note you will need to be on login005 or login006, which have the new slurm, if you are doing this before January 5, 2021. After that the new slurm will be the default.

First load the necessary modules:

```bash
module load mpi/hpcx_2.7.0_intel_2020.2_slurm20 intel/2020.2 python/3.9.0
```

I'll assume you are installing GPAW in `~/usr/installs`. Create a virtual python environment within that and install needed packages. (Note that whatever you pick for `GPAWPATH` needs to be the *permanent* installation location; you can't easily move it later.)

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
Paul installed the tricky things we need, FFTW and libxc for us, and we can pick those up by setting the environment variables as below. Note the last few lines point to libxc4.2.3, because there is a bug in version 5.0.0.

```bash
export C_INCLUDE_PATH=/gpfs/runtime/opt/gpaw/20.10.0_hpcx_2.7.0_intel_2020.2_slurm20/gpaw.venv/depends/include:$C_INCLUDE_PATH
export LIBRARY_PATH=/gpfs/runtime/opt/gpaw/20.10.0_hpcx_2.7.0_intel_2020.2_slurm20/gpaw.venv/depends/lib:$LIBRARY_PATH
export LD_LIBRARY_PATH=/gpfs/runtime/opt/gpaw/20.10.0_hpcx_2.7.0_intel_2020.2_slurm20/gpaw.venv/depends/lib:$LD_LIBRARY_PATH
export LIBRARY_PATH=/users/ap31/data/software/libxc-4.2.3/lib:$LIBRARY_PATH
export LD_LIBRARY_PATH=/users/ap31/data/software/libxc-4.2.3/lib:$LD_LIBRARY_PATH
export C_INCLUDE_PATH=/users/ap31/data/software/libxc-4.2.3/include:$C_INCLUDE_PATH
```

Add ASE to your python path, if it's not there already:

```bash
ASEPATH=/path/to/my/ase
export PATH="$ASEPATH/tools:$PATH"
export PATH="$ASEPATH/bin:$PATH"
export PYTHONPATH="$ASEPATH:$PYTHONPATH"
complete -o default -C "$GPAWPATH/gpaw-venv/bin/python3 $ASEPATH/ase/cli/complete.py" ase
```

We've stored the configuration files and submission scripts that are unique to Brown in the "brown-gpaw" repository. Clone this so you can get these files, using one of the two modes below.

```bash
git clone git@bitbucket.org:andrewpeterson/brown-gpaw.git
#git clone https://bitbucket.org/andrewpeterson/brown-gpaw.git
```

Download GPAW into a folder which we'll call source. Here we are getting the developer version with `git`, but you can also download a numbered version with `wget`. (Also, try the https version of git if this doesn't work.) Also copy our own version of `siteconfig.py` to this directory. *Note:* If you are planning on working on a merge request, make sure to clone your own version of gpaw! E.g., `git clone git@gitlab.com:andrew_peterson/gpaw.git`.

```bash
mkdir source
cd source
git clone git@gitlab.com:gpaw/gpaw.git
cd gpaw
cp ../../brown-gpaw/2020-10/siteconfig.py .
```

Cross your fingers, and install with

```bash
python3 -m pip install --editable .
```

(If you are developing GPAW: The `--editable` flag means that the installation will point to the git source files, so you don't have to re-install every time you change something in python. If you are installing a permanent version, you can leave this flag off.)

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
cp ../../brown-gpaw/2020-10/run-gpaw-tests.py .
sbatch run-gpaw-tests.py
```

If all looks good, you now have a functional copy. Now you should make a command to load it whenever you want to run a job. Add the following to your `.bashrc` (making sure your ASE path is right):

```bash
loadgpaw(){
ASEPATH=/path/to/my/ase
GPAWPATH=$HOME/usr/installs/gpaw
module load mpi/hpcx_2.7.0_intel_2020.2_slurm20 intel/2020.2 python/3.9.0
source $GPAWPATH/gpaw-venv/bin/activate
export PATH="$ASEPATH/tools:$PATH"
export PATH="$ASEPATH/bin:$PATH"
export PYTHONPATH="$ASEPATH:$PYTHONPATH"
complete -o default -C "$GPAWPATH/gpaw-venv/bin/python3 $ASEPATH/ase/cli/complete.py" ase
export C_INCLUDE_PATH=/gpfs/runtime/opt/gpaw/20.10.0_hpcx_2.7.0_intel_2020.2_slurm20/gpaw.venv/depends/include:$C_INCLUDE_PATH
export LIBRARY_PATH=/gpfs/runtime/opt/gpaw/20.10.0_hpcx_2.7.0_intel_2020.2_slurm20/gpaw.venv/depends/lib:$LIBRARY_PATH
export LD_LIBRARY_PATH=/gpfs/runtime/opt/gpaw/20.10.0_hpcx_2.7.0_intel_2020.2_slurm20/gpaw.venv/depends/lib:$LD_LIBRARY_PATH
export LIBRARY_PATH=/users/ap31/data/software/libxc-4.2.3/lib:$LIBRARY_PATH
export LD_LIBRARY_PATH=/users/ap31/data/software/libxc-4.2.3/lib:$LD_LIBRARY_PATH
export C_INCLUDE_PATH=/users/ap31/data/software/libxc-4.2.3/include:$C_INCLUDE_PATH
}
```

You will also need submit files that you use to submit your python scripts. You can copy them into your bin directory as

```bash
cp $GPAWPATH/brown-gpaw/2020-10/gpaw-debug-submit $GPAWPATH/gpaw-venv/bin/gpaw-debug-submit
cp $GPAWPATH/brown-gpaw/2020-10/gpaw-submit $GPAWPATH/gpaw-venv/bin/gpaw-submit
```

Then you should be able to submit jobs as normal, like

```bash
gpaw-debug-submit -c 4 -t 0:15:00 run.py
```

If you want to hack your copy of gpaw and want to be able to see your changes take place immediately, then you should also add the following as the last line of the `load_gpaw()` function in your `.bashrc`. This assumes you are only editing python parts, not compiled portions of the code. This also lets you pull updates and see them immediately. (Apparently this could have also been done by supplying using `python3 -m pip install --editable .` earlier.)

```bash
export PYTHONPATH=$GPAWPATH/source/gpaw:$PYTHONPATH
```




