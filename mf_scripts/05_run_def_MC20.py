# Python module imports.
from time import asctime, localtime
import os

# relax module imports.
from auto_analyses.dauvergne_protocol import dAuvergne_protocol

# Set up the data pipe.
#######################

# The following sequence of user function calls can be changed as needed.

# Create the data pipe.
bundle_name = "mf (%s)" % asctime(localtime())
name = "origin"
pipe.create(name, 'mf', bundle=bundle_name)

# Load the PDB file.
structure.read_pdb('energy_1.pdb', set_mol_name='ArcCALD', read_model=1)

# Set up the 15N and 1H spins (both backbone and Trp indole sidechains).
structure.load_spins('@N', ave_pos=True)
structure.load_spins('@NE1', ave_pos=True)
structure.load_spins('@H', ave_pos=True)
structure.load_spins('@HE1', ave_pos=True)

# Assign isotopes
spin.isotope('15N', spin_id='@N*')
spin.isotope('1H', spin_id='@H*')

# Load the relaxation data.
relax_data.read(ri_id='R1_600',  ri_type='R1',  frq=600.17*1e6, file='R1_600MHz_new_model_free.dat',  mol_name_col=1, res_num_col=2, res_name_col=3, spin_num_col=4, spin_name_col=5, data_col=6, error_col=7)
relax_data.read(ri_id='R2_600',  ri_type='R2',  frq=600.17*1e6, file='R2_600MHz_new_model_free.dat',  mol_name_col=1, res_num_col=2, res_name_col=3, spin_num_col=4, spin_name_col=5, data_col=6, error_col=7)
relax_data.read(ri_id='NOE_600',  ri_type='NOE',  frq=600.17*1e6, file='NOE_600MHz_new.dat',  mol_name_col=1, res_num_col=2, res_name_col=3, spin_num_col=4, spin_name_col=5, data_col=6, error_col=7)
relax_data.read(ri_id='R1_750',  ri_type='R1',  frq=750.06*1e6, file='R1_750MHz_model_free.dat',  mol_name_col=1, res_num_col=2, res_name_col=3, spin_num_col=4, spin_name_col=5, data_col=6, error_col=7)
relax_data.read(ri_id='R2_750',  ri_type='R2',  frq=750.06*1e6, file='R2_750MHz_model_free.dat',  mol_name_col=1, res_num_col=2, res_name_col=3, spin_num_col=4, spin_name_col=5, data_col=6, error_col=7)
relax_data.read(ri_id='NOE_750', ri_type='NOE', frq=750.06*1e6, file='NOE_750MHz.dat', mol_name_col=1, res_num_col=2, res_name_col=3, spin_num_col=4, spin_name_col=5, data_col=6, error_col=7)

# Define the magnetic dipole-dipole relaxation interaction.
interatom.define(spin_id1='@N', spin_id2='@H', direct_bond=True)
interatom.define(spin_id1='@NE1', spin_id2='@HE1', direct_bond=True)
interatom.set_dist(spin_id1='@N*', spin_id2='@H*', ave_dist=1.02 * 1e-10)
interatom.unit_vectors()

# Define the chemical shift relaxation interaction.
value.set(-172 * 1e-6, 'csa', spin_id='@N*')

# Analysis variables.
#####################
# The model-free models.  Do not change these unless absolutely necessary, the protocol is likely to fail if these are changed.
MF_MODELS = ['m0', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9']
#MF_MODELS = ['m1', 'm2']
LOCAL_TM_MODELS = ['tm0', 'tm1', 'tm2', 'tm3', 'tm4', 'tm5', 'tm6', 'tm7', 'tm8', 'tm9']

# The grid search size (the number of increments per dimension).
GRID_INC = 11

# The optimisation technique. Standard is: min_algor='newton' : and cannot be changed in the GUI.
MIN_ALGOR = 'newton'

# The number of Monte Carlo simulations to be used for error analysis at the end of the analysis.
#MC_NUM = 500
MC_NUM = 20
 
# The diffusion model. Standard is 'Fully automated', which means: DIFF_MODEL=['local_tm', 'sphere', 'prolate', 'oblate', 'ellipsoid', 'final']
# 'local_tm', 'sphere', ''prolate', 'oblate', 'ellipsoid', or 'final'
#DIFF_MODEL = 'local_tm'
DIFF_MODEL = ['local_tm', 'sphere', 'prolate', 'oblate', 'ellipsoid', 'final']
 
# The maximum number of iterations for the global iteration.  Set to None, then the algorithm iterates until convergence.
MAX_ITER = None
 
# Automatic looping over all rounds until convergence (must be a boolean value of True or False). Standard is: conv_loop=True : and cannot be changed in the GUI.
CONV_LOOP = True
 
# Change some minimise opt params. 
# This goes into: minimise.execute(self.min_algor, func_tol=self.opt_func_tol, max_iter=self.opt_max_iterations)
#####################
#dAuvergne_protocol.opt_func_tol = 1e-5 # Standard:  opt_func_tol = 1e-25   
#dAuvergne_protocol.opt_max_iterations = 1000 # Standard: opt_max_iterations = int(1e7)
#dAuvergne_protocol.opt_func_tol = 1e-10 # Standard:  opt_func_tol = 1e-25   
#dAuvergne_protocol.opt_max_iterations = int(1e5) # Standard: opt_max_iterations = int(1e7)
 
#####################################
 
# The results dir.
var = 'result_05'
results_dir = os.getcwd() + os.sep + var
 
# Save the state before running. Open and check in GUI!
state.save(state=var+'_ini.bz2', dir=results_dir, force=True)
 
# To check in GUI
# relax -g
# File -> Open relax state
# In folder "result_03" open "result_03_ini.bz2"
# View -> Data pipe editor
# Right click on pipe, and select "Associate with a new auto-analysis"
 
dAuvergne_protocol(pipe_name=name, pipe_bundle=bundle_name, results_dir=results_dir, diff_model=DIFF_MODEL, mf_models=MF_MODELS, local_tm_models=LOCAL_TM_MODELS, grid_inc=GRID_INC, min_algor=MIN_ALGOR, mc_sim_num=MC_NUM, max_iter=MAX_ITER, conv_loop=CONV_LOOP)
