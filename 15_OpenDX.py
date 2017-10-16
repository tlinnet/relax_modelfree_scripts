# Python module imports.
import os

# relax module imports.
import lib.io
from pipe_control.mol_res_spin import spin_loop

# Read the state with the setup
# The results dir.
#var = raw_input("Please enter the name of the results_dir[result_10]:") or "result_10"
var = raw_input("Please enter the name of the results_dir[result_06]:") or "result_06"
results_dir = os.getcwd() + os.sep + var
print("Results dir is: %s"%results_dir)
write_results_dir = os.getcwd() + os.sep + var
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

ans_i = raw_input("Select which pipe to load:") or 0
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

ans_i = raw_input("Select which spin #Nr to make dx map for:") or 0
ans_i = int(ans_i)
sel_spin = spin_res[ans_i]
print("You selected: %s"%sel_spin)
print("")

###########################################################################################
#Write dx file
dxfl = []
dxfl.append('pipe.create("%s_%s", "mf", bundle="temp")'%(sel_pipe[0], sel_pipe[1]) + '\n') 
dxfl.append('results.read(file="results", dir="%s")'%(sel_pipe[3]) + '\n') 

for line in dxfl:
    print line,

#dx.map(params=['dw', 'pA', 'kex'], map_type='Iso3D', spin_id=":1@N", inc=70, lower=None, upper=None, axis_incs=5,
#        file_prefix=file_name, dir=ds.resdir, point=None, point_file='point', remap=None)
