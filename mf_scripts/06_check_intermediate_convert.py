# Python module imports.
import os

# relax module imports.

# Read the state with the setup
var = 'result_06_check_intermediate'
results_dir = os.getcwd() + os.sep + var + os.sep + 'final'
# Load the state with setup data.
state.load(state='results.bz2', dir=results_dir, force=True)

######
#Create the Modelfree4 input files.
#####

#Defaults
# dir:  The directory to place the files.
# force:  A flag which if set to True will cause the results file to be overwritten if it already exists.
# binary:  The name of the executable Modelfree program file.
# diff_search:  See the Modelfree4 manual for 'diffusion_search'.
# sims:  The number of Monte Carlo simulations.
# sim_type:  See the Modelfree4 manual.
# trim:  See the Modelfree4 manual.
# steps:  See the Modelfree4 manual.
# constraints:  A flag specifying whether the parameters should be constrained.  The default is to turn constraints on (constraints=True).
# heteronuc_type:  A three letter string describing the heteronucleus type, ie '15N', '13C', etc.
# atom1:  The symbol of the X heteronucleus in the PDB file.
# atom2:  The symbol of the H nucleus in the PDB file.
# spin_id:  The spin identification string.

# The following files are created
# - 'dir/mfin'
# - 'dir/mfdata'
# - 'dir/mfpar'
# - 'dir/mfmodel'
# - 'dir/run.sh'

# The file 'dir/run.sh' contains the single command,
# 'modelfree4 -i mfin -d mfdata -p mfpar -m mfmodel -o mfout -e out',

# which can be used to execute modelfree4.
# If you would like to use a different Modelfree executable file, change the binary name to the
# appropriate file name.  If the file is not located within the environment's path, include the full
# path in front of the binary file name.

#palmer.create(dir=None, force=False, 
#    binary='modelfree4', diff_search='none', sims=0,
#    sim_type='pred', trim=0, steps=20, 
#    constraints=True, heteronuc_type='15N', atom1='N', atom2='H',
#    spin_id=None)

# Define write out
write_modelfree = os.getcwd() + os.sep + var + os.sep + "Modelfree4"
# Fix bug
cdp.structure.structural_data[0].mol[0].file_path = '.'

outdir = os.getcwd() 
palmer.create(dir=write_modelfree, force=True, 
    binary='modelfree4', diff_search='none', sims=0,
    sim_type='pred', trim=0, steps=20, 
    constraints=True, heteronuc_type='15N', atom1='N', atom2='H',
    spin_id=None)
    
######
#Create the Dasha script 
#####

#Defaults
# algor:  The minimisation algorithm.
# dir:  The directory to place the files.
# force:  A flag which if set to True will cause the results file to be overwritten if it already exists.

# Optimisation algorithms
#The two minimisation algorithms within Dasha are accessible through the algorithm which can be set to:
# 'LM':  The Levenberg-Marquardt algorithm,
# 'NR':  Newton-Raphson algorithm.
# For Levenberg-Marquardt minimisation, the function 'lmin' will be called, while for Newton-Raphson, 
# the function 'min' will be executed.

# dasha.create(algor='LM', dir=None, force=False)

# Define write out
out = 'result_06_check_intermediate'
write_dasha = os.getcwd() + os.sep + out + os.sep + "Dasha"
#dasha.create(algor='LM', dir=write_dasha, force=True)

