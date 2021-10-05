config = {'scheduler': 'slurm',
          'nodes': [('batch', {'cores': 24,
                               'memory': '92G'})],
          'mpiexec': '/usr/local/bin/srun --mpi=pmix',
          'extra_args': ['--account=ap31-condo']}
