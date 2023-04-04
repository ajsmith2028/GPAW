Installation instructions
=========================

These notes are an attempt to install with libvdwxc.
It doesn't seem two work right; we should probably delete them, but leaving them for now in case we need them to figure it out.

CCV module version
------------------

As of this writing (2022-01-21), the last CCV module version was 21.1.0.
Therefore, if you'd like to use version 22.1.0 or newer, you can just follow the custom installation instructions below.

Pre-installed Peterson group version
------------------------------------

If you have read-access to the Peterson group's shared software directory (/gpfs/data/ap31/software), then you should be able to run a pre-installed version of GPAW 22.8.0 by adding the line below to your `.modules` file:

```bash
# Group software installations.
source /gpfs/data/ap31/software/2023/source_me
```

Now (after logging back in again), you can load GPAW 22.8.0 with `pgroup-load-gpaw-22.08.0`.
You can submit GPAW jobs with `gpaw-submit` and `gpaw-debug-submit`.
(You don't need to follow any further instructions below.)

Custom installation
-------------------

(These instructions have now been updated to include the libvdwxc library, which allows you to use BEEF-vdw.)

If you'd like to install your own version of GPAW 22.8.0 or the latest development version; for example to use or test new features, or better to have your own copy to hack on, these instructions should work.
You should also have a look at the official instructions on the [GPAW website](https://wiki.fysik.dtu.dk/gpaw/devel/developer_installation.html).

Here, we'll create everything in a standalone environment, such that when you want to use gpaw later you can do so by calling the command `loadgpawdeveloper`.
This approach shouldn't put hidden files all over your system, so you should be able to un-install later, if you choose, by just removing the directory with all of the GPAW files.
Let's first create that directory; you can place it somewhere else if you choose by modifying `$INSTALLPATH`:

```bash
INSTALLPATH=$HOME/installs/gpaw-22.8  # Feel free to re-name; must be absolute path.
mkdir -p $INSTALLPATH
cd $INSTALLPATH
```

Next we'll load all the modules that we'll need for this installation:

```bash
module load mpi/openmpi_4.0.7_gcc_10.2_slurm22 gcc/10.2 intel/2020.2 python/3.9.0

export C_INCLUDE_PATH=/gpfs/runtime/opt/gpaw/21.1.0_openmpi_4.0.5_gcc_10.2_slurm20/depends/include:$C_INCLUDE_PATH
export LIBRARY_PATH=/gpfs/runtime/opt/gpaw/21.1.0_openmpi_4.0.5_gcc_10.2_slurm20/depends/lib:$LIBRARY_PATH
export LD_LIBRARY_PATH=/gpfs/runtime/opt/gpaw/21.1.0_openmpi_4.0.5_gcc_10.2_slurm20/depends/lib:$LD_LIBRARY_PATH
export PATH=/gpfs/runtime/opt/gpaw/21.1.0_openmpi_4.0.5_gcc_10.2_slurm20/depends/bin:$PATH
```

Now, install libvdwxc, which will give us the BEEF-vdw functional:


```bash
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
```

We'll create a virtual environment that contains all the python dependencies.
We'll re-load this virtual environment every time we want to run a GPAW job with this version.


```bash
cd $INSTALLPATH
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
```

Here we'll assume you don't have ASE already installed; if you have another version you'd prefer to use you should be able to just point `ASEPATH` to that directory and skip the git step.
Download and link ASE:

```bash
ASEPATH=$INSTALLPATH/ase
mkdir -p $ASEPATH
cd $ASEPATH
git clone -b 3.22.1 https://gitlab.com/ase/ase.git  # for version 3.22.1
export PATH="$ASEPATH/tools:$PATH"
export PATH="$ASEPATH/bin:$PATH"
export PYTHONPATH="$ASEPATH/ase:$PYTHONPATH"
complete -o default -C "$INSTALLPATH/gpaw-venv/bin/python3 $ASEPATH/ase/ase/cli/complete.py" ase
```

We've stored the configuration files and submission scripts that are unique to Brown in the "brown-gpaw" repository.
(Presumably, you are reading this file from within this repository!)
Clone this so you can get these files, using one of the two modes below.

```bash
cd $INSTALLPATH
git clone git@bitbucket.org:andrewpeterson/brown-gpaw.git
#git clone https://bitbucket.org/andrewpeterson/brown-gpaw.git
```

Download GPAW into a local folder, which we'll call `source`.
Choose one of the methods below, depending on if you want the latest development version, the exact stable 22.8.0 version, or your own development version.
Also copy our own version of `siteconfig.py` to this directory.
*Note:* If you are planning on working on a merge request, make sure to clone your own version of gpaw!
E.g., `git clone git@gitlab.com:andrew_peterson/gpaw.git`, and make sure your own repository is correctly updated to the version you want.

```bash
mkdir source
cd source
git clone https://gitlab.com/gpaw/gpaw.git  # Latest development version
#git clone -b 22.8.0 https://gitlab.com/gpaw/gpaw.git  # Exact 22.8.0 version
#git clone git@gitlab.com:andrew_peterson/gpaw.git  # E.g., your own development version
cd gpaw
cp ../../brown-gpaw/22.8.0/siteconfig.py .
```

*Important:* if you have installed somewhere other than what we suggest here, you will need to update the libvdwxc portion of siteconfig.py to correctly point to your libvdwxc installation before proceeding.
See line 112.
(That is, make it match $INSTALLPATH.)

Cross your fingers, and install with

```bash
python3 -m pip install --editable .
```

(If you are developing GPAW: The `--editable` flag means that the installation will point to the git source files, so you don't have to re-install every time you change something in python. If you are installing a permanent version, you can leave this flag off. It doesn't really matter in that case.)

Check that the installation exists, install the PAW setups, and test:

```bash
cd $INSTALLPATH
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
cp ../../brown-gpaw/22.8.0/run-gpaw-tests.py .
sbatch run-gpaw-tests.py
```

If all looks good, you now have a functional copy.
Now you should make a command to load it whenever you want to run a job.
Add the following to your `.bashrc` (making sure your ASE path is right):

```bash
loadgpawdeveloper(){
INSTALLPATH=$HOME/installs/gpaw-22.8  # Update if necessary.
ASEPATH=$INSTALLPATH/ase
module load mpi/openmpi_4.0.7_gcc_10.2_slurm22 gcc/10.2 intel/2020.2 python/3.9.0
source $INSTALLPATH/gpaw-venv/bin/activate
export PATH="$ASEPATH/tools:$PATH"
export PATH="$ASEPATH/bin:$PATH"
export PYTHONPATH="$ASEPATH/ase:$PYTHONPATH"
complete -o default -C "$INSTALLPATH/gpaw-venv/bin/python3 $ASEPATH/ase/ase/cli/complete.py" ase
export C_INCLUDE_PATH=/gpfs/runtime/opt/gpaw/21.1.0_openmpi_4.0.5_gcc_10.2_slurm20/depends/include:$C_INCLUDE_PATH
export LIBRARY_PATH=/gpfs/runtime/opt/gpaw/21.1.0_openmpi_4.0.5_gcc_10.2_slurm20/depends/lib:$LIBRARY_PATH
export LD_LIBRARY_PATH=/gpfs/runtime/opt/gpaw/21.1.0_openmpi_4.0.5_gcc_10.2_slurm20/depends/lib:$LD_LIBRARY_PATH
export PATH=/gpfs/runtime/opt/gpaw/21.1.0_openmpi_4.0.5_gcc_10.2_slurm20/depends/bin:$PATH
# Uncomment the next line if you chose not to register your setups.
export GPAW_SETUP_PATH=$INSTALLPATH/gpaw-setups-0.9.20000
}
```

You will also need submit files that you use to submit your python scripts.
You can copy them into your bin directory as

```bash
cp $INSTALLPATH/brown-gpaw/22.8.0/gpaw-debug-submit $INSTALLPATH/gpaw-venv/bin/
cp $INSTALLPATH/brown-gpaw/22.8.0/gpaw-submit $INSTALLPATH/gpaw-venv/bin/
```

Then you should be able to submit jobs as normal, like

```bash
loadgpawdeveloper # you only need to run this once per session
#gpaw-debug-submit -c 4 -t 0:15:00 run.py  # debug job
gpaw-submit -n 1 -c 24 -t 50:00:00 run.py
```

CCV Installation Notes
======================

For archival purposes, the file CCVREADME is one created by the CCV which contains the installation procedure that the CCV used in installing this.
Note that this file is contained in the 20.1.0 folder, as this version uses the identical CCV install files.

AGTS: Big Tests and Documentation Figures
=========================================

(Don't worry about this section unless you know you need AGTS! Most people don't.)

GPAW uses the "Advanced GPAW Testing System" (AGTS) to run especially long tests and to make figures for the documentation that are compute-intensive.
This is basically a queueing / job-management system through `myqueue`, a side package of GPAW.
So you will need to first install myqueue and get it configured for the CCV.

Here we will assume you have done all the steps above and have created a `loadgpawdeveloper` command.
First, load this (to activate your virtual environment), then install `myqueue` with pip:

```bash
loadgpawdeveloper
python3 -m pip install myqueue
```

Next you will need a `config.py` file for our system at Brown.
Note the example we have in this repository assumes you are a member of the `ap31` group; if not, change this line as appropriate.
(You can also delete this line and will just submit to the default queue.)

```bash
cp $GPAWPATH/brown-gpaw/21.6.0/config.py ~/.myqueue/
# edit the file above as appropriate!
```

*Hack:* Myqueue does not seem to inherit the system environment in the same manner as normal job submissions does, and we did not figure out an elegant way to pass the system environment variables through.
So the workaround is to temporarily add `loadgpawdeveloper` to your `.bashrc` file; this will make sure that GPAW is always accessible to all logged-in sessions.
You only need this while the AGTS jobs are running, you can remove it later.
Do this, and you can submit the whole test suite, for example, by

```bash
cd $GPAWPATH/source/gpaw
mq workflow -p agts.py .
mq list  # see what's happening
```
