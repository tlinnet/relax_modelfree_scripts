# Python module imports.
import os

# relax module imports.
import lib.io
from pipe_control.mol_res_spin import spin_loop


out_dir = "_dx"
# Get the directories in the folder
dirs = lib.io.sort_filenames([f for f in os.listdir(os.getcwd()) if os.path.isdir(f)])
for cdir in dirs:
    if 'out' in cdir:
        cdir_sel = cdir
        break
    else:
        cdir_sel = "result"

# Read the state with the setup
# The results dir.
#var = raw_input("Please enter the name of the results_dir[result_10]:") or "result_10"
var = raw_input("Please enter the name of the results_dir[%s]:"%cdir_sel) or cdir_sel
results_dir = os.getcwd() + os.sep + var
if not os.path.isdir(results_dir):
    sys.exit("\nThe result dir does not exists! :%s"%results_dir)

print("Results dir is: %s"%results_dir)
write_results_dir = os.getcwd() + os.sep + var+out_dir
print("write_results dir is: %s"%write_results_dir)

state.load('final_state', dir=results_dir)

# Loop over the spins, take 1 spin
spin_res = []
i = 0
print("\n###########")
print("Select which #Nr spin to make dx map for")
for c_s, c_s_mol, c_s_resi, c_s_resn, c_s_id in spin_loop(full_info=True, return_id=True, skip_desel=True):
    spin_res.append([c_s, c_s_id, c_s_resi, c_s_resn, c_s.model, c_s.params])
    print("%s : %s"%(i, spin_res[-1][1:]))
    i += 1

ans_i = raw_input("Select which spin #Nr to make dx map for[0]:") or 0
ans_i = int(ans_i)
sel_spin = spin_res[ans_i]
print("You selected: %s"%sel_spin[1:])
print("")

# Select parameters
params = sel_spin[-1]
cur_spin = sel_spin[0]
params_sel = []
points_sel = []
for i in range(3):
    print("")
    for j, param in enumerate(params):
        print("%s : %s"%(j, param))
    ans_i = raw_input("Select which param #Nr to make dx map for[0]:") or 0
    ans_i = int(ans_i)
    param_sel = params.pop(ans_i)
    params_sel.append(param_sel)
    # Get point
    point_sel = getattr(cur_spin, param_sel)
    points_sel.append(point_sel)

    print("You selected: %s with value: %s"%(param_sel, point_sel))
print("\nThe params selected is: %s"%params_sel)

###########################################################################################
#Write dx file
file_name_dx = "%s_%s_%s_%s_%s"%(sel_spin[2], sel_spin[3], params_sel[0], params_sel[1], params_sel[2])
write_results_dir_dx = write_results_dir + os.sep + 'dx'

dxfl = []
dxfl.append('state.load("final_state", dir="%s")'%(results_dir) + '\n') 
dxfl.append('' + '\n')
dxfl.append('dx.map(params=%s, #The parameters to be mapped.'%(params_sel) + '\n') 
dxfl.append('    map_type="Iso3D", #The type of map to create.' + '\n') 
dxfl.append('    spin_id="%s", #The spin ID string.'%(sel_spin[1]) + '\n') 
dxfl.append('    inc=10, #The number of increments to map in each dimension.  This value controls the resolution ofthe map.' + '\n') 
dxfl.append('    lower=None, # The lower bounds of the space.' + '\n')
dxfl.append('    upper=None, # The upper bounds of the space.' + '\n')
dxfl.append('    axis_incs=5, #  The number of increments or ticks displaying parameter values along the axes of the OpenDX plot.' + '\n')
dxfl.append('    file_prefix="%s", #The file name. All the output files are prefixed with this name.'%(file_name_dx) + '\n')
dxfl.append('    dir="%s", # The directory to output files to.'%(write_results_dir_dx) + '\n')
dxfl.append('    point=%s, # [x, y, z] This argument allows specific points in the optimisation space to be displayed as coloured spheres.'%points_sel + '\n')
dxfl.append('    point_file="%s_point", # "point" The name of that the point output files will be prefixed with'%(file_name_dx) + '\n')
dxfl.append('    create_par_file=False' + '\n')
dxfl.append('    )' + '\n')
dxfl.append('' + '\n')
dxfl.append('' + '\n')
dxfl.append('' + '\n')
dxfl.append('' + '\n')
dxfl.append('' + '\n')
dxfl.append('' + '\n')
dxfl.append('' + '\n')

# Define write out
file_name = "gen_"+file_name_dx + ".py"
file = lib.io.open_write_file(file_name=file_name, dir=write_results_dir_dx, force=True)
# Write the file.
for line in dxfl:
    file.write(line)
file.close()
