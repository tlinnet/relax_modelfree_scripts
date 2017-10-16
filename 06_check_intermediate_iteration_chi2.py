# Python module imports.
import os

# relax module imports.
from pipe_control import pipes
import lib.io
from specific_analyses.api import return_api

# Read the state with the setup
var = 'result_06_check_intermediate'
results_dir = os.getcwd() + os.sep + var + os.sep + 'final'
# Load the state with setup data.
state.load(state='results.bz2', dir=results_dir, force=True)

# Show pipes
pipe.display()
pipe_name = pipes.cdp_name()
pipe_bundle = pipes.get_bundle(pipe_name)

# Define write out
write_out = results_dir + os.sep + 'grace'

# chi2 per iteration? But does not work?
grace.write(x_data_type='iter', y_data_type='chi2',  file='iter_chi2.agr', dir=write_out, force=True)

#############

# This does not do what we want. So let us try manually.
var_ori = 'result_06'
results_dir_ori = os.getcwd() + os.sep + var_ori

dir_list = os.listdir(results_dir_ori)

all_models = ['local_tm', 'sphere', 'prolate', 'oblate', 'ellipsoid']
opt_models = []
for model in all_models:
    if model in dir_list:
        opt_models.append(model)

# Loop over models MII to MV.
out_results = []
for model in ['sphere', 'prolate', 'oblate', 'ellipsoid']:
    # Skip missing models.
    if model not in opt_models:
        continue
    # Make the model dir
    mdir = results_dir_ori + os.sep + model
    rdir = [ name for name in os.listdir(mdir) if os.path.isdir(os.path.join(mdir, name)) ]
    rdirs = lib.io.sort_filenames(rdir)

    # Loop over rounds
    for rd in rdirs:
        if "round_" in rd:
            dir_model_round = mdir + os.sep + rd + os.sep + 'opt'
            if os.path.isdir(dir_model_round):
                # Create pipe to read data
                pipe_name_rnd = "%s_%s" % (model, rd)
                pipe.create(pipe_name_rnd, 'mf', bundle="temp")
                results.read(file='results', dir=dir_model_round)

                # Get info
                round_i = rd.split("_")[-1]
                cdp_iter = str(cdp.iter)
                chi2 = str(cdp.chi2)
                tm = str(cdp.diff_tensor.tm)

                # Get the api to get number of parameters
                api = return_api(pipe_name=pipe_name)
                model_loop = api.model_loop
                model_desc = api.model_desc
                model_statistics = api.model_statistics

                for model_info in model_loop():
                    desc = model_desc(model_info)
                    # Num_params_(k)
                    # Num_data_sets_(n)
                    k_glob, n_glob, chi2_glob = model_statistics(model_info, global_stats=True)
                    break

                k_glob = str(k_glob)
                n_glob = str(n_glob)
                chi2_glob = str(chi2_glob)

                # Append to results
                out_results.append([pipe_name_rnd, model, round_i, cdp_iter, chi2, tm, k_glob, n_glob, chi2_glob])
                print("\n# Data:")
                print(out_results[-1])

# Change back to original pipe
pipe.switch(pipe_name)
cdp.out_results = out_results

#print result
for res in out_results:
    print res

# Write file
file_name = "results_collected.txt"
file_path = lib.io.get_file_path(file_name, results_dir)
file = lib.io.open_write_file(file_path, force=True)

# Write the file.
headings = ["pipe_name", "model", "round_i", "cdp_iter", "chi2", "tm", "k_glob_Num_params", "n_glob_Num_data_sets", "chi2_glob"]
lib.io.write_data(out=file, headings=headings, data=out_results)
file.close()

# Save the state
state.save(state='results_collected.bz2', dir=results_dir, force=True)

