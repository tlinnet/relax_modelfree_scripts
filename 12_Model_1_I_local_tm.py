# Python module imports.
import os

# relax module imports.
from auto_analyses.dauvergne_protocol import dAuvergne_protocol
from pipe_control import pipes

# The results dir.
var = 'result_10'
results_dir = os.getcwd() + os.sep + var

# Load the state with setup.
state.load(state=var+'_ini.bz2', dir=results_dir, force=True)

# Read the pipe info
pipe.display()
pipe_name = pipes.cdp_name()
pipe_bundle = pipes.get_bundle(pipe_name)

# Analysis variables.
#####################
# The diffusion model. Standard is 'Fully automated', which means: DIFF_MODEL=['local_tm', 'sphere', 'prolate', 'oblate', 'ellipsoid', 'final']
# 'local_tm', 'sphere', ''prolate', 'oblate', 'ellipsoid', or 'final'
#DIFF_MODEL = ['local_tm', 'sphere', 'prolate', 'oblate', 'ellipsoid', 'final']
DIFF_MODEL = ['local_tm']

# The grid search size (the number of increments per dimension).
GRID_INC = 11

# The number of Monte Carlo simulations to be used for error analysis at the end of the analysis.
# This has no influence in Model 1-5
MC_NUM = 0

# The maximum number of iterations for the global iteration.  
# Set to None, then the algorithm iterates until convergence.
MAX_ITER = 20

# Run protocol
dAuvergne_protocol(pipe_name=pipe_name, pipe_bundle=pipe_bundle, 
   results_dir=results_dir,
   write_results_dir=results_dir,
   diff_model=DIFF_MODEL,
   grid_inc=GRID_INC,
   mc_sim_num=MC_NUM,
   max_iter=MAX_ITER)

#####
# After local_tm, then get some info
#####

# Define out_dir
write_results_dir = results_dir + os.sep + 'local_tm'

# Get model
value.write(param='model', file='model.txt', dir=write_results_dir, force=True)
# Get equation
value.write(param='equation', file='equation.txt', dir=write_results_dir, force=True)
# Get local_tm
value.write(param='local_tm', file='local_tm.txt', dir=write_results_dir, force=True)
