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
