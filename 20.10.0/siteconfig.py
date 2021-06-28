"""User provided customizations.

Here one changes the default arguments for compiling _gpaw.so.

Here are all the lists that can be modified:

* libraries
  List of libraries to link: -l<lib1> -l<lib2> ...
* library_dirs
  Library search directories: -L<dir1> -L<dir2> ...
* include_dirs
  Header search directories: -I<dir1> -I<dir2> ...
* extra_link_args
  Arguments forwarded directly to linker
* extra_compile_args
  Arguments forwarded directly to compiler
* runtime_library_dirs
  Runtime library search directories: -Wl,-rpath=<dir1> -Wl,-rpath=<dir2> ...
* extra_objects
* define_macros

The following lists work like above, but are only linked when compiling
the parallel interpreter:

* mpi_libraries
* mpi_library_dirs
* mpi_include_dirs
* mpi_runtime_library_dirs
* mpi_define_macros

To override use the form:

    libraries = ['somelib', 'otherlib']

To append use the form

    libraries += ['somelib', 'otherlib']
"""

# flake8: noqa

# compiler = 'gcc'
# mpicompiler = 'mpicc'
# mpilinker = 'mpicc'
compiler = 'icc'      # CCV
mpicompiler = 'mpicc' # CCV
mpilinker = 'mpicc'   # CCV
# platform_id = ''

###### CCV ######
# LIBRARIES 
libraries = ['xc', 'mkl_intel_lp64', 'mkl_sequential', 'mkl_core',
             'mkl_lapack95_lp64', 'mkl_blacs_intelmpi_lp64',
             'mkl_avx2', 'mkl_def',
             'pthread']
library_dirs += ['/gpfs/rt/7.2/opt/intel/2020.2/compilers_and_libraries_2020.2.254/linux/mkl/lib/intel64_lin']
library_dirs += ['/gpfs/runtime/opt/gpaw/20.10.0_hpcx_2.7.0_intel_2020.2_slurm20/depends/lib']
include_dirs += ['/gpfs/rt/7.2/opt/intel/2020.2/compilers_and_libraries_2020.2.254/linux/mkl/include']
include_dirs += ['/gpfs/runtime/opt/gpaw/20.10.0_hpcx_2.7.0_intel_2020.2_slurm20/depends/include']
###### CCV ######

# FFTW3:
#fftw = False  # CCV
fftw = True    # CCV
if fftw:
    libraries += ['fftw3']

# ScaLAPACK (version 2.0.1+ required):
#scalapack = False  # CCV
scalapack = True    # CCV
if scalapack:
#    libraries += ['scalapack-openmpi']     # CCV
    libraries += ['mkl_scalapack_lp64']     # CCV

# Use Elpa (requires ScaLAPACK and Elpa API 20171201):
if 0:
    elpa = True
    elpadir = '/home/user/elpa'
    libraries += ['elpa']
    library_dirs += ['{}/lib'.format(elpadir)]
    extra_link_args += ['-Wl,-rpath={}/lib'.format(elpadir)]
    include_dirs += ['{}/include/elpa-xxxx.xx.xxx'.format(elpadir)]

# LibXC:
# In order to link libxc installed in a non-standard location
# (e.g.: configure --prefix=/home/user/libxc-2.0.1-1), use:

# - static linking:
if 1:
#    xc = '/home/user/libxc-4.0.4/'   # CCV
    xc = '/gpfs/runtime/opt/gpaw/20.10.0_hpcx_2.7.0_intel_2020.2_slurm20/depends/'   # CCV
    xc = '/users/ap31/data/software/libxc-4.2.3/'  # AAP
    include_dirs += [xc + 'include']
    extra_link_args += [xc + 'lib/libxc.a']
    if 'xc' in libraries:
        libraries.remove('xc')

# - dynamic linking (requires rpath or setting LD_LIBRARY_PATH at runtime):
if 0:
#    xc = '/home/user/libxc-4.0.4/'   # CCV
    xc = '/gpfs/runtime/opt/gpaw/20.10.0_hpcx_2.7.0_intel_2020.2_slurm20/depends/'   # CCV
    include_dirs += [xc + 'include']
    library_dirs += [xc + 'lib']
    # You can use rpath to avoid changing LD_LIBRARY_PATH:
    extra_link_args += ['-Wl,-rpath={xc}/lib'.format(xc=xc)]
    if 'xc' not in libraries:
        libraries.append('xc')


# libvdwxc:
if 0:
    libvdwxc = True
    path = '/home/user/libvdwxc'
    extra_link_args += ['-Wl,-rpath=%s/lib' % path]
    library_dirs += ['%s/lib' % path]
    include_dirs += ['%s/include' % path]
    libraries += ['vdwxc']
