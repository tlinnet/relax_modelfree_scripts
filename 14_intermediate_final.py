# Python module imports.
import os, stat, sys
 
# relax module imports.
from auto_analyses.dauvergne_protocol import dAuvergne_protocol
from pipe_control import pipes
import lib.io
import lib.plotting.grace
from pipe_control.mol_res_spin import spin_loop
from specific_analyses.api import return_api
 
ans=True
while ans:
    print("")
    print("  0: Do intermediate final run")
    print("  1: Do final run")

    ans=raw_input("What would you like to do?[0]:") or "0"
    if ans=="0": 
        print("")
        print("------------------------------------------")
        print("|    Intermediate run                    |")
        print("------------------------------------------")
        MC_NUM = 3
        mode = "intermediate"
        out_dir = "_intermediate_final"
        ans=False

    elif ans=="1": 
        print("")
        print("------------------------------------------")
        print("|    Final run                           |")
        print("------------------------------------------")
        mode = "final"
        MC_NUM = raw_input("Please enter nr of Monte-Carlo simulations MC_NUM[500]:") or 500
        MC_NUM = int(MC_NUM)
        out_dir = "_final_MC_%i"%(MC_NUM)
        ans=False

print("MC_NUM=%i"%MC_NUM)

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

print("Results dir is: %s"%results_dir)
write_results_dir = os.getcwd() + os.sep + var+out_dir
print("write_results dir is: %s"%write_results_dir)

###########################################################################################
# Write a python "grace to PNG/EPS/SVG..." conversion script.
# Open the file for writing.
file_name = "grace2images.py"
write_results_dir_grace = write_results_dir + os.sep + 'final' + os.sep + 'grace'
file = lib.io.open_write_file(file_name=file_name, dir=write_results_dir_grace, force=True)
# Write the file.
lib.plotting.grace.script_grace2images(file=file)
file.close()
file_path = lib.io.get_file_path(file_name, write_results_dir_grace)
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
    file = lib.io.open_write_file(file_name=file_name, dir=write_results_dir, force=True)
     
    # Write the file.
    headings = ["mol", "resi", "resn", "element", "id", "model", "equation"]
    lib.io.write_data(out=file, headings=headings, data=out_results)
    file.close()

###########################################################################################
#Write pymol file
pyml = []
pyml.append('# Start settings' + '\n') 
pyml.append('reinitialize' + '\n')
pyml.append('bg_color white' + '\n')
pyml.append('set scene_buttons, 1' + '\n')
pyml.append('' + '\n')
pyml.append('# Load protein and set name' + '\n')
pdb_file_name = cdp.structure.structural_data[0].mol[0].file_name
pdb_file = pdb_file_name.split(".pdb")[0]
pyml.append('load ../../../%s'%pdb_file_name + '\n')
pyml.append("prot='prot'" + '\n')
pyml.append('cmd.set_name("%s", prot)'%pdb_file + '\n')
pyml.append('' + '\n')
pyml.append('# Load tensor pdb' + '\n')
pyml.append('load ../tensor.pdb' + '\n')
pyml.append('' + '\n')
pyml.append('#################################' + '\n')
pyml.append('# Scene 1 :  Make default view' + '\n')
pyml.append('#################################' + '\n')
pyml.append('hide everything, prot' + '\n')
pyml.append('show_as cartoon, prot' + '\n')
pyml.append('zoom prot and polymer' + '\n')
pyml.append('' + '\n')
pyml.append('scene F1, store, load of data, view=1' + '\n')
pyml.append('' + '\n')
pyml.append('################################' + '\n')
pyml.append("# Scenes: We will go through the order like this" + '\n')
pyml.append("# 's2', 's2f', 's2s', 'amp_fast', 'amp_slow', 'te', 'tf', 'ts', 'time_fast', 'time_slow', 'rex'" + '\n')
pyml.append('# s2: S2, the model-free generalised order parameter (S2 = S2f.S2s).' + '\n')
pyml.append('# s2f: S2f, the faster motion model-free generalised order parameter.' + '\n')
pyml.append('# s2s: S2s, the slower motion model-free generalised order parameter.' + '\n')
pyml.append('# amp_fast: ' + '\n')
pyml.append('# amp_slow: ' + '\n')
pyml.append('# te: Single motion effective internal correlation time (seconds).' + '\n')
pyml.append('# tf: Faster motion effective internal correlation time (seconds).' + '\n')
pyml.append('# ts: Slower motion effective internal correlation time (seconds).' + '\n')
pyml.append('# time_fast: ' + '\n')
pyml.append('# time_slow:' + '\n')
pyml.append('# rex: Chemical exchange relaxation (sigma_ex = Rex / omega**2). ' + '\n')
pyml.append('' + '\n')
pyml.append("modes = ['s2', 's2f', 's2s', 'amp_fast', 'amp_slow', 'te', 'tf', 'ts', 'time_fast', 'time_slow', 'rex']" + '\n')
pyml.append('fdir = "./"' + '\n')
pyml.append('python' + '\n')
pyml.append('' + '\n')
pyml.append('# File placement' + '\n')
pyml.append('if True:' + '\n')
pyml.append('    for i, mode in enumerate(modes):' + '\n')
pyml.append('        # Make name' + '\n')
pyml.append('        protn = "%s_%s" % (prot, mode)' + '\n')
pyml.append('' + '\n')
pyml.append('        # Loop over file lines' + '\n')
pyml.append('        fname = fdir + "/%s.pml"%mode' + '\n')
pyml.append('        fname_out = fdir + "/0_mod_%s.pml"%mode' + '\n')
pyml.append('        f_out = open(fname_out, "w")' + '\n')
pyml.append('        with open(fname) as f:' + '\n')
pyml.append('            for line in f:' + '\n')
pyml.append('                line_cmd = ""' + '\n')
pyml.append('                # Add to end of line, depending on command' + '\n')
pyml.append('                if line[0] == "\\n":' + '\n')
pyml.append('                    line_add = ""' + '\n')
pyml.append('                elif line[0:4] == "hide":' + '\n')
pyml.append('                    line_add = " everything, %s"%protn' + '\n')
pyml.append('' + '\n')
pyml.append('                # All not changed' + '\n')
pyml.append('                elif line[0:8] == "bg_color":' + '\n')
pyml.append('                    line_add = ""' + '\n')
pyml.append('                elif line[0:9] == "set_color":' + '\n')
pyml.append('                    line_add = ""' + '\n')
pyml.append('                elif line[0:6] == "delete":' + '\n')
pyml.append('                    line_add = ""' + '\n')
pyml.append('' + '\n')
pyml.append('                else:' + '\n')
pyml.append('                    line_add =  " and %s"%protn' + '\n')
pyml.append('                # Modify line' + '\n')
pyml.append('                line_cmd = line.strip() + line_add + "\\n"' + '\n')
pyml.append('' + '\n')
pyml.append('                # Modify atom name to big' + '\n')
pyml.append('                line_cmd = line_cmd.replace("name ca,n,c", "name CA,N,C")' + '\n')
pyml.append('                line_cmd = line_cmd.replace("name ca,n", "name CA,N")' + '\n')
pyml.append('                line_cmd = line_cmd.replace("name ca,c", "name CA,C")' + '\n')
pyml.append('' + '\n')
pyml.append('                # Write the line' + '\n')
pyml.append('                f_out.write(line_cmd)' + '\n')
pyml.append('            f_out.close()' + '\n')
pyml.append('python end ' + '\n')
pyml.append('' + '\n')
pyml.append('# Make pymol objects' + '\n')
pyml.append('python' + '\n')
pyml.append('for i, mode in enumerate(modes):' + '\n')
pyml.append('    protn = "%s_%s" % (prot, mode)' + '\n')
pyml.append('    cmd.copy(protn, prot)' + '\n')
pyml.append('' + '\n')
pyml.append('    cmd.scene("F1")' + '\n')
pyml.append('    cmd.disable(prot)' + '\n')
pyml.append('    cmd.enable(protn)' + '\n')
pyml.append('    cmd.scene("F%i"%(i+2), "store", mode, view=0)' + '\n')
pyml.append('python end' + '\n')
pyml.append('' + '\n')
pyml.append('#################################' + '\n')
pyml.append('# Scenes' + '\n')
pyml.append("# #modes = ['s2', 's2f', 's2s', 'amp_fast', 'amp_slow', 'te', 'tf', 'ts', 'time_fast', 'time_slow', 'rex']" + '\n')
pyml.append('' + '\n')
pyml.append('scene F2' + '\n')
pyml.append('@./0_mod_s2.pml' + '\n')
pyml.append('scene F2, store, s2: the model-free generalised order parameter (S2 = S2f.S2s), view=0' + '\n')
pyml.append('' + '\n')
pyml.append('scene F3' + '\n')
pyml.append('@./0_mod_s2f.pml' + '\n')
pyml.append('scene F3, store, s2f: the faster motion model-free generalised order parameter, view=0' + '\n')
pyml.append('' + '\n')
pyml.append('scene F4' + '\n')
pyml.append('@./0_mod_s2s.pml' + '\n')
pyml.append('scene F4, store, s2s: the slower motion model-free generalised order parameter, view=0' + '\n')
pyml.append('' + '\n')
pyml.append('scene F5' + '\n')
pyml.append('@./0_mod_amp_fast.pml' + '\n')
pyml.append('scene F5, store, amp_fast, view=0' + '\n')
pyml.append('' + '\n')
pyml.append('scene F6' + '\n')
pyml.append('@./0_mod_amp_slow.pml' + '\n')
pyml.append('scene F6, store, amp_slow, view=0' + '\n')
pyml.append('' + '\n')
pyml.append('scene F7' + '\n')
pyml.append('@./0_mod_te.pml' + '\n')
pyml.append('scene F7, store, te: Single motion effective internal correlation time (seconds), view=0' + '\n')
pyml.append('' + '\n')
pyml.append('scene F8' + '\n')
pyml.append('@./0_mod_tf.pml' + '\n')
pyml.append('scene F8, store, tf: Faster motion effective internal correlation time (seconds), view=0' + '\n')
pyml.append('' + '\n')
pyml.append('scene F9' + '\n')
pyml.append('@./0_mod_ts.pml' + '\n')
pyml.append('scene F9, store, ts: Slower motion effective internal correlation time (seconds), view=0' + '\n')
pyml.append('' + '\n')
pyml.append('scene F10' + '\n')
pyml.append('@./0_mod_time_fast.pml' + '\n')
pyml.append('scene F10, store, time_fast, view=0' + '\n')
pyml.append('' + '\n')
pyml.append('scene F11' + '\n')
pyml.append('@./0_mod_time_slow.pml' + '\n')
pyml.append('scene F11, store, time_slow, view=0' + '\n')
pyml.append('' + '\n')
pyml.append('scene F12' + '\n')
pyml.append('@./0_mod_rex.pml' + '\n')
pyml.append('scene F12, store, rex: Chemical exchange relaxation (sigma_ex = Rex / omega**2), view=0' + '\n')
pyml.append('' + '\n')
pyml.append('# Save session' + '\n')
pyml.append('save ./pymol_session.pse' + '\n')

# Define write out
file_name = "0_0_apply_all_pymol_commands.pml"
write_results_dir_pyml = write_results_dir + os.sep + 'final' + os.sep + 'pymol'
file = lib.io.open_write_file(file_name=file_name, dir=write_results_dir_pyml, force=True)
# Write the file.
for line in pyml:
    file.write(line)
file.close()


###########################################################################################
#Get chi2 per iteration

ans = raw_input("Should I the find chi2 value per iteraion?[n]:") or "n"
#ans = "n"
if ans == 'y':
    dir_list = os.listdir(results_dir)

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
        mdir = results_dir + os.sep + model
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
    file = lib.io.open_write_file(file_name=file_name, dir=write_results_dir, force=True)

    # Write the file.
    headings = ["pipe_name", "model", "round_i", "cdp_iter", "chi2", "tm", "k_glob_Num_params", "n_glob_Num_data_sets", "chi2_glob"]
    lib.io.write_data(out=file, headings=headings, data=out_results)
    file.close()

    # Save the state
    #state.save(state='results_collected.bz2', dir=write_results_dir, force=True)

###########################################################################################
#Write python graphing file
pytl = []
pytl.append("import pandas as pd" + '\n') 
pytl.append("import matplotlib.pyplot as plt" + '\n') 
pytl.append("" + '\n') 
pytl.append("col_n = ['pipe_name', 'model', 'round_i', 'cdp_iter', 'chi2', 'tm', 'k', 'n', 'chi2_glob']" + '\n') 
pytl.append("df = pd.read_csv('results_collected.txt', delim_whitespace=True, skiprows=1, names=col_n)" + '\n') 
pytl.append("" + '\n') 
pytl.append("print('# Plotting')" + '\n') 
pytl.append("f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, figsize=(12, 6))" + '\n') 
pytl.append("" + '\n') 
pytl.append("df[df['model'] == 'sphere'].plot(x='round_i', y='chi2', ax=ax1, color='DarkBlue', label='sphere')" + '\n') 
pytl.append("df[df['model'] == 'prolate'].plot(x='round_i', y='chi2', ax=ax1, color='DarkGreen', label='prolate')" + '\n') 
pytl.append("df[df['model'] == 'oblate'].plot(x='round_i', y='chi2', ax=ax1, color='DarkRed', label='oblate')" + '\n') 
pytl.append("df[df['model'] == 'ellipsoid'].plot(x='round_i', y='chi2', ax=ax1, color='DarkOrange', label='ellipsoid')" + '\n') 
pytl.append("ax1.set_title('chi2')" + '\n') 
pytl.append("box = ax1.get_position()" + '\n') 
pytl.append("ax1.set_position([box.x0, box.y0, box.width * 0.8, box.height])" + '\n') 
pytl.append("ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))" + '\n') 
pytl.append("" + '\n') 
pytl.append("df[df['model'] == 'sphere'].plot(x='round_i', y='k', ax=ax2, color='DarkBlue', label='sphere')" + '\n') 
pytl.append("df[df['model'] == 'prolate'].plot(x='round_i', y='k', ax=ax2, color='DarkGreen', label='prolate')" + '\n') 
pytl.append("df[df['model'] == 'oblate'].plot(x='round_i', y='k', ax=ax2, color='DarkRed', label='oblate')" + '\n') 
pytl.append("df[df['model'] == 'ellipsoid'].plot(x='round_i', y='k', ax=ax2, color='DarkOrange', label='ellipsoid')" + '\n') 
pytl.append("ax2.set_title('k: Number of parameters')" + '\n') 
pytl.append("box = ax2.get_position()" + '\n') 
pytl.append("ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])" + '\n') 
pytl.append("ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))" + '\n') 
pytl.append("" + '\n')
pytl.append("df[df['model'] == 'sphere'].plot(x='round_i', y='tm', ax=ax3, color='DarkBlue', label='sphere')" + '\n') 
pytl.append("df[df['model'] == 'prolate'].plot(x='round_i', y='tm', ax=ax3, color='DarkGreen', label='prolate')" + '\n') 
pytl.append("df[df['model'] == 'oblate'].plot(x='round_i', y='tm', ax=ax3, color='DarkRed', label='oblate')" + '\n') 
pytl.append("df[df['model'] == 'ellipsoid'].plot(x='round_i', y='tm', ax=ax3, color='DarkOrange', label='ellipsoid')" + '\n') 
pytl.append("ax3.set_title('tm:')" + '\n') 
pytl.append("box = ax3.get_position()" + '\n') 
pytl.append("ax3.set_position([box.x0, box.y0, box.width * 0.8, box.height])" + '\n') 
pytl.append("ax3.legend(loc='center left', bbox_to_anchor=(1, 0.5))" + '\n') 
pytl.append("" + '\n') 
pytl.append("plt.savefig('results_collected.png')" + '\n')
pytl.append("#plt.show()" + '\n') 

# Define write out
file_name = "results_collected.py"
file = lib.io.open_write_file(file_name=file_name, dir=write_results_dir, force=True)
# Write the file.
for line in pytl:
    file.write(line)
file.close()
