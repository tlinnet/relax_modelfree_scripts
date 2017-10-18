# Python module imports.
import os, sys, stat

# relax module imports.
from pipe_control import pipes, relax_data
import lib.io
import lib.plotting.grace

# Get the directories in the folder
dirs = [f for f in os.listdir(os.getcwd()) if os.path.isdir(f)]
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

# Print data per spectrometer_frq
print("\nType of data per spectrometer_frq:")
print("#####################################")
for spec_frq in d_dic['spec_frq_list']:
    print("\nFor spectrometer_frq[Hz]: %s" % spec_frq)
    #print(d_dic['spec_frq_data'][spec_frq]['ri_types'])
    print("Type and id: %s"% d_dic['spec_frq_data'][spec_frq]['ri_ids_types'] )

# Do the consistency tests per spectrometer_frq:
print("\nNow doing consistency tests per spectrometer_frq:")
print("###################################################")
for spec_frq in d_dic['spec_frq_list']:
    ri_types = d_dic['spec_frq_data'][spec_frq]['ri_types']
    # Test if all types are present
    test = ['R1', 'R2', 'NOE']
    if not all(x in ri_types for x in test):
        print("sf: %s, Missing either type %s in %s"%(spec_frq, test, ri_types))
        continue

    # Copy the current data pipe
    frq_short = "%.0f_Mhz" % (spec_frq/1e6)
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

    # Create grace files.
    write_results_dir_frq = write_results_dir + os.sep + frq_short
    grace.write(y_data_type='j0', file='j0.agr', dir=write_results_dir_frq, force=True)
    grace.write(y_data_type='f_eta', file='f_eta.agr', dir=write_results_dir_frq, force=True)
    grace.write(y_data_type='f_r2', file='f_r2.agr',  dir=write_results_dir_frq, force=True)

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
