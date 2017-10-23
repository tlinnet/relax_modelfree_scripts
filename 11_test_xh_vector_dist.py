# Python module imports.
import os, sys, stat

# relax module imports.
from pipe_control import pipes, relax_data
import lib.io
import lib.plotting.grace

# Get the directories in the folder
dirs = lib.io.sort_filenames([f for f in os.listdir(os.getcwd()) if os.path.isdir(f)])
for cdir in dirs:
    if 'result' in cdir:
        cdir_sel = cdir
        break
    else:
        cdir_sel = "result_10"

# Read the state with the setup
# The results dir.
#var = raw_input("Please enter the name of the results_dir[result_10]:") or "result_10"
var = raw_input("Please enter the name of the results_dir[%s]:"%cdir_sel) or cdir_sel
results_dir = os.getcwd() + os.sep + var
if not os.path.isdir(results_dir):
    sys.exit("\nThe result dir does not exists! :%s"%results_dir)

# Load the state with setup.
state.load(state=var+'_ini.bz2', dir=results_dir, force=True)

# Read the pipe info
pipe.display()
pipe_name = pipes.cdp_name()
pipe_bundle = pipes.get_bundle(pipe_name)

# Define out
out_dir = "_xh_bond"
write_results_dir_xh = results_dir+out_dir
print("write_results dir is: %s"%write_results_dir_xh)

# Create the PDB file representing the vector distribution.
structure.create_vector_dist(file='vect_dist.pdb', dir=write_results_dir_xh, force=True)

# Write structure
structure.write_pdb(file='protein.pdb', dir=write_results_dir_xh, force=True)

pymol_script = r"""
# Start settings
reinitialize
bg_color white
set scene_buttons, 1

# Load protein and set name
load protein.pdb
load vect_dist.pdb

# Visualize
hide everything, protein
show cartoon, protein
"""

file_name = "0_0_apply_all_pymol_commands.pml"
file = lib.io.open_write_file(file_name=file_name, dir=write_results_dir_xh, force=True)
# Write the file.
file.write(pymol_script)
#lib.plotting.grace.script_grace2images(file=file)
file.close()
