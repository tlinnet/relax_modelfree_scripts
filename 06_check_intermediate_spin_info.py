# Python module imports.
import os
 
# relax module imports.
from pipe_control import pipes
import lib.io
from pipe_control.mol_res_spin import spin_loop
 
# Read the state with the setup
var = 'result_06_check_intermediate'
results_dir = os.getcwd() + os.sep + var + os.sep + 'final'
# Load the state with setup data.
state.load(state='results.bz2', dir=results_dir, force=True)
 
# Show pipes
pipe.display()
pipe_name = pipes.cdp_name()
pipe_bundle = pipes.get_bundle(pipe_name)
 
# Get model
value.write(param='model', file='model.txt', dir=results_dir, force=True)
# Get equation
value.write(param='equation', file='equation.txt', dir=results_dir, force=True)
 
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
file_path = lib.io.get_file_path(file_name, results_dir)
file = lib.io.open_write_file(file_path, force=True)
 
# Write the file.
headings = ["mol", "resi", "resn", "element", "id", "model", "equation"]
lib.io.write_data(out=file, headings=headings, data=out_results)
file.close()

