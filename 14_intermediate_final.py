# Python module imports.
import os, stat

# relax module imports.
from auto_analyses.dauvergne_protocol import dAuvergne_protocol
from pipe_control import pipes
import lib.io
import lib.plotting.grace

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
DIFF_MODEL = ['final']

# The grid search size (the number of increments per dimension).
GRID_INC = 11

# The number of Monte Carlo simulations to be used for error analysis at the end of the analysis.
# This has no influence in Model 1-5.
# For intermediate, we just take minimum
MC_NUM = 4

# The maximum number of iterations for the global iteration.  
# Set to None, then the algorithm iterates until convergence.
MAX_ITER = 20

# Define write out
out = 'result_10_intermediate_final'
write_results_dir = os.getcwd() + os.sep + out

# Run protocol
dAuvergne_protocol(pipe_name=pipe_name, pipe_bundle=pipe_bundle, 
   results_dir=results_dir,
   write_results_dir=write_results_dir,
   diff_model=DIFF_MODEL,
   grid_inc=GRID_INC,
   mc_sim_num=MC_NUM,
   max_iter=MAX_ITER)

# Write a python "grace to PNG/EPS/SVG..." conversion script.
# Open the file for writing.
file_name = "grace2images.py"
write_results_dir_grace = write_results_dir + os.sep + 'final' + os.sep + 'grace'
file_path = lib.io.get_file_path(file_name, write_results_dir_grace)
file = lib.io.open_write_file(file_path, force=True)
# Write the file.
lib.plotting.grace.script_grace2images(file=file)
file.close()
os.chmod(file_path, stat.S_IRWXU|stat.S_IRGRP|stat.S_IROTH)
