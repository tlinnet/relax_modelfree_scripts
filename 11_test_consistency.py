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

out_dir = "_consistency"
write_results_dir = results_dir+out_dir
print("write_results dir is: %s"%write_results_dir)

# Load the state with setup.
state.load(state=var+'_ini.bz2', dir=results_dir, force=True)

# Read the pipe info
pipe.display()
pipe_name = pipes.cdp_name()
pipe_bundle = pipes.get_bundle(pipe_name)

# Show the current_data
relax_data_ids = relax_data.get_ids()
d_dic = {}
d_dic['spec_frq_list'] = []
d_dic['spec_frq_data'] = {}
print("relax_data.get_ids() : %s"% relax_data_ids )
for ri_id in relax_data_ids:
    #print("relax_data id: %s, type: %s, spectrometer_frq[Hz]: %s" %(ri_id, cdp.ri_type[ri_id], cdp.spectrometer_frq[ri_id]) )
    # Test if this is the first data
    if cdp.spectrometer_frq[ri_id] not in d_dic['spec_frq_list']:
        # Assign to list
        d_dic['spec_frq_list'].append(cdp.spectrometer_frq[ri_id])
        # Make dic structure
        d_dic['spec_frq_data'][cdp.spectrometer_frq[ri_id]] = {}
        d_dic['spec_frq_data'][cdp.spectrometer_frq[ri_id]]['ri_ids_types'] = []
        d_dic['spec_frq_data'][cdp.spectrometer_frq[ri_id]]['ri_types'] = []
    # Assign data
    d_dic['spec_frq_data'][cdp.spectrometer_frq[ri_id]]['ri_ids_types'].append([cdp.ri_type[ri_id], ri_id])
    d_dic['spec_frq_data'][cdp.spectrometer_frq[ri_id]]['ri_types'].append(cdp.ri_type[ri_id])

# Do the consistency tests per spectrometer_frq:
print("\nNow doing consistency tests per spectrometer_frq:")
print("###################################################")
for spec_frq in d_dic['spec_frq_list']:
    print("\nFor spectrometer_frq[Hz]: %s" % spec_frq)
    #print(d_dic['spec_frq_data'][spec_frq]['ri_types'])
    print("Type and id: %s"% d_dic['spec_frq_data'][spec_frq]['ri_ids_types'] )

    # Extract types
    ri_types = d_dic['spec_frq_data'][spec_frq]['ri_types']
    # Test if all types are present
    test = ['R1', 'R2', 'NOE']
    if not all(x in ri_types for x in test):
        print("sf: %s, Missing either type %s in %s"%(spec_frq, test, ri_types))
        continue

    # Copy the current data pipe
    frq_short = "%.0f_MHz" % (spec_frq/1e6)
    pipe_name_ct = "%s_%s" %("consistency", frq_short)
    pipe.copy(pipe_from=pipe_name, pipe_to=pipe_name_ct, bundle_to=pipe_bundle)
    pipe.switch(pipe_name=pipe_name_ct)
    pipe.change_type(pipe_type='ct')
    print("Current pipe:", pipes.cdp_name())

    # Set the frequency.
    consistency_tests.set_frq(frq=spec_frq)

    # Set the angle between the 15N-1H vector and the principal axis of the 15N chemical shift tensor
    # FIXME: Where does this value come from???
    val_orientation = "15.7"
    print("Enter the angle between the 15N-1H vector and the principal axis of the 15N chemical shift tensor")
    val_orientation = raw_input("orientation=%s:"%val_orientation) or val_orientation
    val_orientation = float(val_orientation)
    value.set(val=val_orientation, param='orientation')

    # Set the approximate correlation time.
    print("Enter the approximate correlation time")
    # FIXME: Where does this value come from???
    val_tc = "13e-9"
    val_tc = raw_input("Default val=%s:"%val_tc) or val_tc
    val_tc = float(val_tc)
    value.set(val=val_tc, param='tc')

    # Consistency tests.
    minimise.calculate()

    # Monte Carlo simulations.
    val_mc= "3"
    print("Enter the number of Monte-Carlo simulations. 500 is standard. 3 for fast run.")
    val_mc = raw_input("MC_NUM=%s:"%val_mc) or val_mc
    val_mc =int(val_mc)

    monte_carlo.setup(number=val_mc)
    monte_carlo.create_data()
    minimise.calculate()
    monte_carlo.error_analysis()

    # Define output dir
    #write_results_dir_frq = write_results_dir + os.sep + frq_short+"_MC_%i"%(val_mc)
    # Post-fix to file names
    #pf = ""

    write_results_dir_frq = write_results_dir + os.sep + "MC_%i"%(val_mc)
    pf = "_"+frq_short

    # Create grace files.
    grace.write(y_data_type='j0', file='j0%s.agr'%pf, dir=write_results_dir_frq, force=True)
    grace.write(y_data_type='f_eta', file='f_eta%s.agr'%pf, dir=write_results_dir_frq, force=True)
    grace.write(y_data_type='f_r2', file='f_r2%s.agr'%pf,  dir=write_results_dir_frq, force=True)

    # Create value files
    value.write(param='j0', file='j0%s.txt'%pf, dir=write_results_dir_frq, force=True)
    value.write(param='f_eta', file='f_eta%s.txt'%pf, dir=write_results_dir_frq, force=True)
    value.write(param='f_r2', file='f_r2%s.txt'%pf,  dir=write_results_dir_frq, force=True)

    # Write a python "grace to PNG/EPS/SVG..." conversion script.
    # Open the file for writing.
    file_name = "grace2images.py"
    write_results_dir_grace = write_results_dir_frq
    file = lib.io.open_write_file(file_name=file_name, dir=write_results_dir_grace, force=True)
    # Write the file.
    lib.plotting.grace.script_grace2images(file=file)
    file.close()
    file_path = lib.io.get_file_path(file_name, write_results_dir_grace)
    os.chmod(file_path, stat.S_IRWXU|stat.S_IRGRP|stat.S_IROTH)

    # Finish.
    results.write(file='results%s'%pf, dir=write_results_dir_frq, force=True)
    state.save('state%s'%pf, dir=write_results_dir_frq, force=True)

pyt_script = r"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from glob import glob
import itertools
import decimal
import numpy as np
from pandas.plotting import scatter_matrix
from seaborn import pairplot, despine

# All files has this column name
col_n = ['mol_name', 'res_num', 'res_name', 'spin_num', 'spin_name', 'value', 'error']
# All files should skip 3
skiprows = 3

# Define the parameters
#parameters = ['j0', 'f_eta', 'f_r2']
#parameters = ['f_eta']
parameters = ['j0']

# Set values for warning
warn_ratio_over = 1.2
warn_ratio_under = 0.8

# Collect data
dfg_frames = []
file_ids = []
for i, par in enumerate(parameters):
    flist = glob("%s_*.txt"%par)

    # Get the files
    df_frames = []
    val_ids = []
    err_ids = []
    for j,f in enumerate(flist):
        # Get the file_ids
        file_id = f.split("%s_"%par)[-1].split(".txt")[0]
        file_ids.append(file_id)

        # Read csv
        df_par = pd.read_csv(f, delim_whitespace=True, skiprows=skiprows, names=col_n)
        # Replace 'None' with NaN 
        df_par = df_par.mask(df_par.astype(object).eq('None'))
        # Then drop 
        df_par = df_par.dropna(axis=0, how='all', subset=['value'])

        # Get scaling
        df_min = df_par['value'].min()
        dc = str(decimal.Decimal(df_min))
        if "E" in dc:
            dc_s = "1e"+dc.split("E")[-1]
        else:
            dc_s = 1

        # Convert to numeric
        df_par = df_par.apply(pd.to_numeric, errors='ignore')
        # Rename
        val_id = '%s_%s'%(par, file_id)
        val_ids.append(val_id)
        err_id = 'err_%s_%s'%(par, file_id)
        err_ids.append(err_id)

        df_par.rename(columns={'value': val_id, 'error': err_id}, inplace=True)

        # Append to frames
        df_frames.append(df_par)

    # Merge data frames
    df = df_frames[0].merge(df_frames[1], left_on=['mol_name', 'res_num', 'res_name', 'spin_num', 'spin_name'], right_on=['mol_name', 'res_num', 'res_name', 'spin_num', 'spin_name'], how='outer')
    if len(flist) > 2:
        for k in range(2, len(flist)):
            df = df.merge(df_frames[k], left_on=['mol_name', 'res_num', 'res_name', 'spin_num', 'spin_name'], right_on=['mol_name', 'res_num', 'res_name', 'spin_num', 'spin_name'], how='outer')
    #print df
    #print df.info()

    # Collect merged dataframe
    dfg_frames.append(df)

    # Scale values
    for val_id, err_id in zip(val_ids, err_ids):
        df[val_id] = df[val_id] * 1./float(dc_s)
        df[err_id] = df[err_id] * 1./float(dc_s)
        print("Scaling parameter: %s with 1/%s"%(par, dc_s))

    # Plot single graphs of combinations of indexes.
    for xi, yi in itertools.combinations(range(len(val_ids)), 2):
        # Get ids
        x_val_id = val_ids[xi]
        y_val_id = val_ids[yi]
        x_err_id = err_ids[xi]
        y_err_id = err_ids[yi]

        # Get val
        x_val_data = df[x_val_id]
        y_val_data = df[y_val_id]
        # Make ratio
        ratio = y_val_data / x_val_data
        # Get err
        x_err_data = df[x_err_id]
        y_err_data = df[y_err_id]

        # Make warning labels
        ## Over True/False
        ratio_over = ratio > warn_ratio_over
        ratio_under = ratio > warn_ratio_under
        ## Under True/False
        ratio_under = ratio < warn_ratio_under
        ratio_under = ratio < warn_ratio_under
        # Get data
        ## Over data
        ratio_over_x = x_val_data[ratio_over].tolist()
        ratio_over_y = y_val_data[ratio_over].tolist()
        ratio_over_resi = df['res_num'][ratio_over].astype(str).tolist()
        ## Under data
        ratio_under_x = x_val_data[ratio_under].tolist()
        ratio_under_y = y_val_data[ratio_under].tolist()
        ratio_under_resi = df['res_num'][ratio_under].astype(str).tolist()

        # Create figure
        f, ax = plt.subplots(1, figsize=(8, 8))
        df.plot(ax=ax, x=x_val_id, y=y_val_id, kind='scatter')
        # Create warning 
        ## Over
        for x, y, s in zip(ratio_over_x, ratio_over_y, ratio_over_resi):
            ax.text(x, y, s)
        ## Under
        for x, y, s in zip(ratio_under_x, ratio_under_y, ratio_under_resi):
            ax.text(x, y, s)

        # Create line by getting window size
        lim = ax.get_xlim()
        x_data_line = np.linspace(lim[0], lim[1], num=50)
        ax.plot(x_data_line, x_data_line, linestyle="-", color="k", label="scale 1/%s"%(dc_s))
        #box = ax.get_position()
        #ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        #ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        ax.legend(loc='upper left')
        # Save figure
        plt.savefig('plot_0_scatter_%s_%s_%s.png'%(par, x_val_id, y_val_id))
        #plt.show()
        plt.close()

        # Create histogram
        # Create figure
        f, ax = plt.subplots(1, figsize=(8, 4))
        ax.hist(ratio, bins=50, normed=True, label="%s %s"%(x_val_id, y_val_id))
        ax.legend(loc='upper right')
        # Save figure
        plt.savefig('plot_0_hist_%s_%s_%s.png'%(par, x_val_id, y_val_id))
        #plt.show()
        plt.close()

        # For the following calculations, see:
        # Linnet, T.E., Teilum, K. "Non-uniform sampling of NMR relaxation data", Journal of Biomolecular NMR, 2016, 
        # DOI: 10.1007/s10858-016-0020-6, http://dx.doi.org/10.1007/s10858-016-0020-6

        # ratio normalization
        v_g = x_val_data / x_val_data
        v_h = y_val_data / x_val_data
        # normalized vector uncertainties
        v_s_g = x_err_data / x_val_data
        v_s_h = y_err_data / x_val_data
        # difference vector
        v_d = v_g - v_h
        # pooled standard deviation. These are equal: std_pool_test = np.sqrt( np.sum( v_s_g**2 + v_s_h**2 )/len(v_s_g) )
        std_pool = np.sqrt( np.mean( np.square(v_s_g) + np.square(v_s_h) ) )
        # mean difference. These are equal: mean_diff_test = np.dot( np.ones(len(v_d)), v_d ) / len(v_d)
        mean_d = np.mean(v_d)
        # standard deviation of differences
        std_d = np.std(v_d, ddof=1)

        # Create figure for scatter
        f, ax = plt.subplots(1, figsize=(8, 8))
        # Plot
        ax.scatter(np.zeros(len(v_h)), v_d, label="%s %s"%(x_val_id, y_val_id))
        ax.scatter(0, mean_d, label="Mean of differences")
        ax.scatter([0, 0], [mean_d+std_d, mean_d-std_d], label="Mean +/- 1*std")
        ax.set_ylabel("Ratio normalized differences")
        ax.legend(loc='upper right')
        # Save figure
        plt.savefig('plot_1_scatter_%s_%s_%s.png'%(par, x_val_id, y_val_id))
        #plt.show()
        plt.close()

        # Create figure for histogram
        f, ax = plt.subplots(1, figsize=(8, 8))
        ax.hist(v_d, bins=50, normed=True, label="%s %s"%(x_val_id, y_val_id))
        # Get lim and set equal
        max_lim = np.max(np.abs( ax.get_xlim() ))
        ax.set_xlim(-1*max_lim, max_lim)

        # Plot normal distribution
        x_norm = np.linspace(-1*max_lim, max_lim, 100)
        # Library
        y_norm = mlab.normpdf(x_norm, mean_d, std_d)
        plt.plot(x_norm, y_norm, label="normpdf")
        # Manually
        #y_norm_1 = np.exp(-np.power(x_norm - mean_d, 2.) / (2 * np.power(std_d, 2.)))
        #plt.plot(x_norm, y_norm_1, label="norm 1")
        #y_norm_2 = y_norm_1 * (1.0/(std_d * np.sqrt(2.0 * np.pi))) 
        #plt.plot(x_norm, y_norm_2, label="norm 2")

        # Create the comparison normal distribution
        y_norm_pool = mlab.normpdf(x_norm, 0.0, std_pool)
        #y_norm_pool = mlab.normpdf(x_norm, mean_d, std_pool)
        plt.plot(x_norm, y_norm_pool, label="normpdf pool")

        # Save figure
        ax.legend(loc='upper right')
        plt.savefig('plot_1_hist_%s_%s_%s.png'%(par, x_val_id, y_val_id))
        #plt.show()
        plt.close()

    # Try matrix plot. Drop everyting, except data points
    df_m = df.drop(['mol_name', 'res_num', 'res_name', 'spin_num', 'spin_name']+err_ids, axis=1)
    #print df_m.info()
    scatter_matrix(df_m, alpha=0.2, figsize=(6, 6), diagonal='kde')
    plt.savefig('plot_0_scattermatrix_%s.png'%(par))
    plt.close()
    #plt.show()

# Merge data frames
for i, par in enumerate(parameters):
    dfi = dfg_frames[i]
    # Rename
    val_ids = []
    err_ids = []
    for j, file_id in enumerate(file_ids):
        # Define previous ids
        val_id_prev = '%s_%s'%(par, file_id)
        err_id_prev = 'err_%s_%s'%(par, file_id)

        # Define new ids
        val_id = 'value_%s'%file_id
        err_id = 'error_%s'%file_id
        val_ids.append(val_id)
        err_ids.append(err_id)

        # Rename
        dfi.rename(columns={val_id_prev: val_id, err_id_prev: err_id}, inplace=True)
        # Add the param to column
        dfi = dfi.assign(param=par)

    # Merge downwards
    if i == 0:
        dfg = dfi
    else:
        # Concatenate data from first run
        dfg = pd.concat([dfg, dfi], ignore_index=True)

# Drop data
dfg = dfg.drop(['mol_name', 'res_num', 'res_name', 'spin_num', 'spin_name']+err_ids, axis=1)
#print dfg.info()

# Make pairplo
g = pairplot(dfg, hue="param", diag_kind='kde')
g.fig.set_size_inches(8, 8)
plt.savefig('plot_0_pairplot.png')
#plt.show()
plt.close()

"""
file_name = "plot_txt_files.py"
file = lib.io.open_write_file(file_name=file_name, dir=write_results_dir_frq, force=True)
# Write the file.
file.write(pyt_script)
#lib.plotting.grace.script_grace2images(file=file)
file.close()


out_string = """############################################################################################################################################

Script for consistency testing.
Severe artifacts can be introduced if model-free analysis is performed from inconsistent multiple magnetic field datasets. 

The use of simple tests as validation tools for the consistency assessment can help avoid such problems in order to extract more 
reliable information from spin relaxation experiments. In particular, these tests are useful for detecting inconsistencies arising from R2 data. 

Since such inconsistencies can yield artifactual Rex parameters within model-free analysis, these tests should be used 
routinely prior to any analysis such as model-free calculations.

This script will allow one to calculate values for the three consistency tests J(0), F_eta and F_R2. 

Once this is done, qualitative analysis can be performed by comparing values obtained at different magnetic fields. 
Correlation plots and histograms are useful tools for such comparison, such as presented in Morin & Gagne (2009a) J. Biomol. NMR, 45: 361-372.

References
==========
The description of the consistency testing approach:
    Morin & Gagne (2009a) Simple tests for the validation of multiple field spin relaxation data. J. Biomol. NMR, 45: 361-372. U{http://dx.doi.org/10.1007/s10858-009-9381-4}
The origins of the equations used in the approach:
    J(0):
        Farrow et al. (1995) Spectral density function mapping using 15N relaxation data exclusively. J. Biomol. NMR, 6: 153-162. U{http://dx.doi.org/10.1007/BF00211779}
    F_eta:
        Fushman et al. (1998) Direct measurement of 15N chemical shift anisotropy in solution. J. Am. Chem. Soc., 120: 10947-10952. U{http://dx.doi.org/10.1021/ja981686m}
    F_R2:
        Fushman et al. (1998) Direct measurement of 15N chemical shift anisotropy in solution. J. Am. Chem. Soc., 120: 10947-10952. U{http://dx.doi.org/10.1021/ja981686m}
A study where consistency tests were used:
    Morin & Gagne (2009) NMR dynamics of PSE-4 beta-lactamase: An interplay of ps-ns order and us-ms motions in the active site. Biophys. J., 96: 4681-4691. U{http://dx.doi.org/10.1016/j.bpj.2009.02.068}


Performing these simple calculations for each residue
=====================================================

* Comparing results obtained at different magnetic fields should, in the case of perfect consistency and 
assuming the absence of conformational exchange, yield equal values independently of the magnetic field

"""

file_name = "README.txt"
file = lib.io.open_write_file(file_name=file_name, dir=write_results_dir, force=True)
# Write the file.
file.write(out_string)
#lib.plotting.grace.script_grace2images(file=file)
file.close()
print(out_string)
