#!/bin/bash
#SBATCH --ntasks-per-node=4
#SBATCH --nodes=1
#SBATCH --mem=16g
#SBATCH --time=5:00:00

# This script is for testing a gpaw installation, which can take some
# hours. It needs to be run from your gpaw source directory (i.e.,
# the top-level directory that you downloaded), with all of your 
# normal gpaw environment variables loaded.

mpiexec -n 4 pytest -v
