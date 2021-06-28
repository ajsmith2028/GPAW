Note
====

This directory contains files from older versions of GPAW, before the numbering system changed to reflect the release year.
We are just keeping them here for archival purposes.
We have moved some instructions over from our group's internal wiki into this folder, in case they are of any use.
Those instructions follow.


Installation instructions
-------------------------

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
