# Python module imports.
import os

# relax module imports.
import lib.io
from pipe_control.mol_res_spin import spin_loop

ans=True
while ans:
    print("")
    print("  0: Store in intermediate final run")
    print("  1: Store in final run")

    ans=raw_input("What would you like to do?[0]:") or 0
    if ans=="0": 
        print("")
        print("------------------------------------------")
        print("|    Intermediate run                    |")
        print("------------------------------------------")
        mode = "intermediate"
        out_dir = "_intermediate_final"
        ans=False

    elif ans=="1": 
        print("")
        print("------------------------------------------")
        print("|    Final run                           |")
        print("------------------------------------------")
        out_dir = "_final"
        mode = "final"
        ans=False

    elif ans !="" or ans =="":
        print("\n-Not Valid Choice - Try again-\n")
        ans=True

# Read the state with the setup
# The results dir.
#var = raw_input("Please enter the name of the results_dir[result_10]:") or "result_10"
var = raw_input("Please enter the name of the results_dir[result_06]:") or "result_06"
results_dir = os.getcwd() + os.sep + var
print("Results dir is: %s"%results_dir)
write_results_dir = os.getcwd() + os.sep + var+out_dir
print("write_results dir is: %s"%write_results_dir)

# Find last round file
dir_list = os.listdir(results_dir)

all_models = ['local_tm', 'sphere', 'prolate', 'oblate', 'ellipsoid']
opt_models = []
for model in all_models:
    if model in dir_list:
        opt_models.append(model)

# Loop over models MII to MV.
out_results = []
i = 0
for model in ['sphere', 'prolate', 'oblate', 'ellipsoid']:
    # Skip missing models.
    if model not in opt_models:
        continue
    out_results.append([model, "", "", ""]) 

    # Make the model dir
    mdir = results_dir + os.sep + model
    rdir = [ name for name in os.listdir(mdir) if os.path.isdir(os.path.join(mdir, name)) ]
    rdirs = lib.io.sort_filenames(rdir)

    # Loop over rounds
    for rd in rdirs:
        if "round_" in rd:
            dir_round = int(rd.split("_")[-1])
            dir_model_round = mdir + os.sep + rd + os.sep + 'opt'
            if os.path.isdir(dir_model_round):
                out_results[i][1] = rd
                out_results[i][2] = dir_round
                out_results[i][3] = dir_model_round
    i += 1

print("\n###########")
print("Select which pipe to load")
for i, o in enumerate(out_results):
    print("%s : %s"%(i, o[:2]))

ans_i = raw_input("Select which pipe to load[0]:") or 0
ans_i = int(ans_i)
sel_pipe = out_results[ans_i]
print("You selected: %s"%sel_pipe[:2])

pipe.create("%s_%s"%(sel_pipe[0], sel_pipe[1]), 'mf', bundle="temp")
results.read(file='results', dir=sel_pipe[3])

# Loop over the spins, take 1 spin
spin_res = []
i = 0
print("\n###########")
print("Select which #Nr spin to make dx map for")
for c_s, c_s_mol, c_s_resi, c_s_resn, c_s_id in spin_loop(full_info=True, return_id=True, skip_desel=True):
    spin_res.append([c_s_id, c_s_resi, c_s_resn, c_s.params])
    print("%s : %s"%(i, spin_res[-1]))
    i += 1

ans_i = raw_input("Select which spin #Nr to make dx map for[0]:") or 0
ans_i = int(ans_i)
sel_spin = spin_res[ans_i]
print("You selected: %s"%sel_spin)
print("")

# Select parameters
params = sel_spin[-1]
params_sel = []
for i in range(3):
    print("")
    for j, param in enumerate(params):
        print("%s : %s"%(j, param))
    ans_i = raw_input("Select which param #Nr to make dx map for[0]:") or 0
    ans_i = int(ans_i)
    param_sel = params.pop(ans_i)
    params_sel.append(param_sel)
    print("You selected: %s"%param_sel)
print("\nThe params selected is: %s"%params_sel)

###########################################################################################
#Write dx file
file_name_dx = "%s_%s_%s_%s_%s_%s_%s"%(sel_pipe[0], sel_pipe[1], sel_spin[1], sel_spin[2], params_sel[0], params_sel[1], params_sel[2])
write_results_dir_dx = write_results_dir + os.sep + 'final' + os.sep + 'dx'

dxfl = []
dxfl.append('pipe.create("%s_%s", "mf", bundle="temp")'%(sel_pipe[0], sel_pipe[1]) + '\n') 
dxfl.append('results.read(file="results", dir="%s")'%(sel_pipe[3]) + '\n') 
dxfl.append('' + '\n')
dxfl.append('fix("all", fixed=True)' + '\n') 
dxfl.append('' + '\n')
dxfl.append('dx.map(params=%s, #The parameters to be mapped.'%(params_sel) + '\n') 
dxfl.append('    map_type="Iso3D", #The type of map to create.' + '\n') 
dxfl.append('    spin_id="%s", #The spin ID string.'%(sel_spin[0]) + '\n') 
dxfl.append('    inc=20, #The number of increments to map in each dimension.  This value controls the resolution ofthe map.' + '\n') 
dxfl.append('    lower=None, # The lower bounds of the space.' + '\n')
dxfl.append('    upper=None, # The upper bounds of the space.' + '\n')
dxfl.append('    axis_incs=5, #  The number of increments or ticks displaying parameter values along the axes of the OpenDX plot.' + '\n')
dxfl.append('    file_prefix="%s", #The file name. All the output files are prefixed with this name.'%(file_name_dx) + '\n')
dxfl.append('    dir="%s", # The directory to output files to.'%(write_results_dir_dx) + '\n')
dxfl.append('    point=None, # [x, y, z] This argument allows specific points in the optimisation space to be displayed as coloured spheres.' + '\n')
dxfl.append('    point_file="point" # The name of that the point output files will be prefixed with' + '\n')
dxfl.append('    )' + '\n')
dxfl.append('' + '\n')
dxfl.append('' + '\n')
dxfl.append('' + '\n')
dxfl.append('' + '\n')
dxfl.append('' + '\n')
dxfl.append('' + '\n')
dxfl.append('' + '\n')

# Define write out
file_name = file_name_dx + ".py"
file = lib.io.open_write_file(file_name=file_name, dir=write_results_dir_dx, force=True)
# Write the file.
for line in dxfl:
    file.write(line)
file.close()
