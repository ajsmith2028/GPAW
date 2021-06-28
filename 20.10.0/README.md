Installation instructions
=========================

The installation instructions for this version were included within the peterson group internal wiki page. But note that there is a bug in this particular version having to do with Brown's version of hpcx. A newer version built with openmpi is more stable. Please use that one.

However, if for some reason you need to re-create this, we have put the instructions we were using below.


Old instructions
----------------
If you need to compile a version of GPAW --- for example, to have the latest development version with Georg's dipole correction in planewave mode, etc. --- these instructions should work. You should also go through the instructions on the [GPAW website](https://wiki.fysik.dtu.dk/gpaw/devel/developer_installation.html).

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






## Old version -- probably can be deleted ##

This method creates a clean directory to hold all your gpaw files, then creates a custom command to set your PYTHONPATH and PATH variables to point to these when you want to load this. In this way, everything here is completely reversible.

(Note that the previous method here made a virtual environment. This has a problem that it makes all the executables load only the local version of python, which can create a few compatibility issues. These instructions now use a developer environment.)

Start by creating the directory to hold GPAW, and downloading the latest GPAW with git. We'll also download a repository that has a couple of customization files to make GPAW work on Brown's CCV. The newest version of GPAW requires at least python 2.7.13 and ASE 3.15.0 (you have to unload ase in the cluster by doing `module unload ase/X.Y.Z` where `X.Y.Z` refers to the version currently being used in your environment. All loaded modules can be seen with `module list`). 

```bash
mkdir -p ~/usr/env
cd ~/usr/env
module load git
module load python/2.7.13
pip install --user --upgrade numpy
pip install --user --upgrade ase
git clone https://gitlab.com/gpaw/gpaw.git
git clone https://andrewpeterson@bitbucket.org/andrewpeterson/brown-gpaw.git
```
We need a copy of customize.py which is made for our system. We can copy the version we just downloaded into our gpaw repository. Then, we run the installation. Note we run setup.py with the build_ext flag, which just builds it locally within this directory instead of making changes to your account.

```bash
cp brown-gpaw/customize.py gpaw/
cd gpaw
module load mvapich2
python setup.py build_ext
```

Everything we need is now in place; it is a matter of setting our environment to point to the right paths. The simplest is to define a macro in your `.bashrc` file that loads what you want. (This is equivalent to calling "module load ..."). For example, add the following lines to your bashrc:

```bash
loadgpawdeveloper()
{
export PYTHONPATH=$HOME/usr/env/gpaw:$PYTHONPATH
export PYTHONPATH=$HOME/usr/env/gpaw/build/lib.linux-x86_64-2.7:$PYTHONPATH
export PATH=$HOME/usr/env/brown-gpaw/bin:$PATH
export PATH=$HOME/usr/env/gpaw/tools:$PATH
export PATH=$HOME/usr/env/gpaw/build/bin.linux-x86_64-2.7:$PATH
export LD_LIBRARY_PATH="/gpfs/runtime/opt/openblas/0.2.8/lib:/gpfs/runtime/opt/gpaw/1.1.0/src/libxc-install-3.0.0/lib":/gpfs/runtime/opt/mvapich2/2.0rc1/lib:/gpfs/runtime/opt/python/2.7.3/lib:/gpfs/runtime/opt/java/7u5/jre/lib/amd64:/gpfs/runtime/opt/intel/2013.1.106/lib/intel64:/gpfs/runtime/opt/intel/2013.1.106/mkl/lib/intel64:/gpfs/runtime/opt/centos-libs/6.5/lib64:/gpfs/runtime/opt/centos-libs/6.5/lib:/gpfs/runtime/opt/centos-libs/6.5/lib64/mysql:/gpfs/runtime/opt/centos-libs/6.5/lib64/samba
export GPAW_SETUP_PATH="/gpfs/runtime/opt/gpaw/1.1.0/gpaw-setups-0.9.20000"
}
```

It should be fully installed now. You should be able to switch to your new version of GPAW with `loadgpawdeveloper`. Then you can submit jobs with `gpaw-squeue` as normal, and can also run at the command line or in an interactive session as normal. Note you should check the paths at the beginning of the *.txt file produced by GPAW to verify that it is using the version you think it is.

In this installation strategy, you can choose which version of GPAW you want. That is, if you do not first run `loadgpawdeveloper` in your session, you should get your old default version of GPAW that you had installed previously. If you run `loadgpawdeveloper` in your session, you will get your new developer version. Again, always check the *.txt file to make sure.

## Compiling GPAW in the Red Hat OS (login node003)   ##

Soon all the user accounts on the ccv will be transferred to a new operating system. Once that happened some of our codes will have to be recompiled.

In order to access a recent developers version of gpaw, there is version 1.3.1b1 compiled in the directory
```~/data/software/gpaw_redhat```. In order to use it, the ```~/.bashrc``` should contain the following:

```bash
load_gpaw_redhat()
{                
    export LD_LIBRARY_PATH=$HOME/data/software/libxc-4.0.4/lib:$LD_LIBRARY_PATH
    export LD_LIBRARY_PATH=/gpfs/runtime/opt/openblas/0.2.19/lib:$LD_LIBRARY_PATH
    export PYTHONPATH=$HOME/data/software/gpaw_redhat:$PYTHONPATH
    export PYTHONPATH=$HOME/data/software/ase_redhat/build/lib:$PYTHONPATH    
    export PATH=$HOME/data/software/gpaw_redhat/build/bin.linux-x86_64-2.7:$PATH
    export GPAW_SETUP_PATH=$HOME/data/software/gpaw_redhat/gpaw-setups-0.9.20000
}    
```
You can also compile your own version of gpaw. In that case the tutorial above has to by slightly changed:

```bash
mkdir -p ~/usr/env
cd ~/usr/env
module load git
git clone https://gitlab.com/gpaw/gpaw.git
git clone https://gitlab.com/ase/ase.git
cd gpaw
cp ~/data/software/gpaw_redhat/customize.py .
```
Compiling can then be done by writing

```bash
module load gcc/6.2
module load mpi
python setup.py build
```
The lines needed in the .bashrc are now:

```bash
load_gpaw_redhat()
{
    export LD_LIBRARY_PATH=$HOME/data/software/libxc-4.0.4/lib:$LD_LIBRARY_PATH
    export LD_LIBRARY_PATH=/gpfs/runtime/opt/openblas/0.2.19/lib:$LD_LIBRARY_PATH
    export PYTHONPATH=$HOME/usr/env/gpaw:$PYTHONPATH
    export PYTHONPATH=$HOME/usr/env/ase:$PYTHONPATH    
    export PATH=$HOME/usr/env/gpaw/build/bin.linux-x86_64-2.7:$PATH
    export GPAW_SETUP_PATH=$HOME/data/software/gpaw_redhat/gpaw-setups-0.9.20000
}
```

**Note:** 

The ```gpaw-squeue``` script changed slightly, too. It is contained in ```~/data/software/gpaw_redhat/build/bin.linux-x86_64-2.7``` and will, therefore, be usable if the pre-installed version is used. For a custom installation, copy it into a directory your ```PATH``` variable points to, for example

```bash
cp ~/data/software/gpaw_redhat/build/bin.linux-x86_64-2.7/gpaw-squeue ~/usr/env/gpaw/build/bin.linux-x86_64-2.7
```
