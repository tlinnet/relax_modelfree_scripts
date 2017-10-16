# Python module imports.
import os, stat
 
# relax module imports.
from auto_analyses.dauvergne_protocol import dAuvergne_protocol
from pipe_control import pipes
import lib.io
import lib.plotting.grace
from pipe_control.mol_res_spin import spin_loop
 
ans=True
while ans:
    print("")
    print("  1: Do intermediate final run")
    print("  2: Do final run")

    ans=raw_input("What would you like to do? ") 
    if ans=="1": 
        print("")
        print("------------------------------------------")
        print("|    Intermediate run                    |")
        print("------------------------------------------")
        MC_NUM = 3
        mode = "intermediate"
        out_dir = "_intermediate_final"
        ans=False

    elif ans=="2": 
        print("")
        print("------------------------------------------")
        print("|    Final run                           |")
        print("------------------------------------------")
        out_dir = "_final"
        mode = "final"
        MC_NUM = raw_input("Please enter nr of Monte-Carlo simulations MC_NUM[500]:") or 500
        MC_NUM = int(MC_NUM)
        ans=False

    elif ans !="" or ans =="":
        print("\n-Not Valid Choice - Try again-\n")
        ans=True

print("MC_NUM=%i"%MC_NUM)

# Read the state with the setup
# The results dir.
#var = raw_input("Please enter the name of the results_dir[result_10]:") or "result_10"
var = raw_input("Please enter the name of the results_dir[result_06]:") or "result_06"
results_dir = os.getcwd() + os.sep + var
print("Results dir is: %s"%results_dir)
write_results_dir = os.getcwd() + os.sep + var+out_dir
print("write_results dir is: %s"%write_results_dir)

###########################################################################################
# Write a python "grace to PNG/EPS/SVG..." conversion script.
# Open the file for writing.
file_name = "grace2images.py"
write_results_dir_grace = write_results_dir + os.sep + 'final' + os.sep + 'grace'
file_path = lib.io.get_file_path(file_name, write_results_dir_grace)
file = lib.io.open_write_file(file_name=file_name, dir=write_results_dir_grace, force=True)
# Write the file.
lib.plotting.grace.script_grace2images(file=file)
file.close()
os.chmod(file_path, stat.S_IRWXU|stat.S_IRGRP|stat.S_IROTH)
###########################################################################################

# Load the state with setup data.
state.load(state=var+'_ini.bz2', dir=results_dir, force=True)

# Read the pipe info
pipe.display()
pipe_name = pipes.cdp_name()
pipe_bundle = pipes.get_bundle(pipe_name)

# The diffusion model. 
DIFF_MODEL = ['final']

# Run protocol
ans = raw_input("Should I run the dAuvergne_protocol?[n]:") or "n"
if ans == 'y':
    dAuvergne_protocol(pipe_name=pipe_name, pipe_bundle=pipe_bundle, 
        results_dir=results_dir, 
        write_results_dir=write_results_dir, 
        diff_model=DIFF_MODEL, 
        mc_sim_num=MC_NUM)

###########################################################################################
#Create the Modelfree4 input files.

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
if ans == 'y':
    #ans_m4 = raw_input("Should I make input files for palmer Modelfree4?[n]:") or "n"
    ans_m4 = "y"
    if ans_m4 == 'y':
        # Define write out
        write_results_dir_modelfree = write_results_dir + os.sep + 'Modelfree4'
        # Fix bug
        cdp.structure.structural_data[0].mol[0].file_path = '.'

        outdir = os.getcwd() 
        palmer.create(dir=write_results_dir_modelfree, force=True, 
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
if ans == 'y':
    ans_dasha = "n"
    if ans_dasha == 'y':
        # Define write out
        write_results_dir_modelfree = write_results_dir + os.sep + 'Modelfree4'

        # Define write out
        out = 'result_06_check_intermediate'
        write_results_dir_dasha = write_results_dir + os.sep +  + "Dasha"
        dasha.create(algor='LM', dir=write_results_dir_dasha, force=True)

###########################################################################################
#Get more spin information

if ans == 'y':
    # Get model
    value.write(param='model', file='model.txt', dir=write_results_dir, force=True)
    # Get equation
    value.write(param='equation', file='equation.txt', dir=write_results_dir, force=True)

    # Inspect manually
    out_results = []
    i=0
    for c_s, c_s_mol, c_s_resi, c_s_resn, c_s_id in spin_loop(full_info=True, return_id=True, skip_desel=True):
        # See what we can extract from the spin container
        if i == 0:
            print dir(c_s)
     
        # First convert to string
        c_s_resi = str(c_s_resi)
        # Append
        out_results.append([c_s_mol, c_s_resi, c_s_resn, c_s.element, c_s_id, c_s.model, c_s.equation])
        # Print
        print("mol: %s, resi: %s, resn: %s, element: %s, id: %s, model: %s, equation: %s" % tuple(out_results[-1]) )
        i += 1
     
    # Write file
    file_name = "results_collected_spin_info.txt"
    file_path = lib.io.get_file_path(file_name, write_results_dir)
    file = lib.io.open_write_file(file_path, force=True)
     
    # Write the file.
    headings = ["mol", "resi", "resn", "element", "id", "model", "equation"]
    lib.io.write_data(out=file, headings=headings, data=out_results)
    file.close()
