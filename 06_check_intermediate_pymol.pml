# Start settings
reinitialize
bg_color white
set scene_buttons, 1

# Load protein and set name
load energy_1.pdb
prot='prot'
cmd.set_name("energy_1", prot)

# Load tensor pdb
load ./result_06_check_intermediate/final/tensor.pdb

#################################
# Scene 1 :  Make default view
#################################
hide everything, prot
show_as cartoon, prot
zoom prot and polymer

scene F1, store, load of data, view=1

################################
# Scenes: We will go through the order like this
# 's2', 's2f', 's2s', 'amp_fast', 'amp_slow', 'te', 'tf', 'ts', 'time_fast', 'time_slow', 'rex'
# s2: S2, the model-free generalised order parameter (S2 = S2f.S2s).
# s2f: S2f, the faster motion model-free generalised order parameter.
# s2s: S2s, the slower motion model-free generalised order parameter.
# amp_fast: 
# amp_slow: 
# te: Single motion effective internal correlation time (seconds).
# tf: Faster motion effective internal correlation time (seconds).
# ts: Slower motion effective internal correlation time (seconds).
# time_fast: 
# time_slow:
# rex: Chemical exchange relaxation (sigma_ex = Rex / omega**2). 

#modes = ['s2']
#modes = ['s2', 's2f']
modes = ['s2', 's2f', 's2s', 'amp_fast', 'amp_slow', 'te', 'tf', 'ts', 'time_fast', 'time_slow', 'rex']
fdir = "./result_06_check_intermediate/final/pymol"

python
# File placement
if True:
    for i, mode in enumerate(modes):
        # Make name
        protn = '%s_%s' % (prot, mode)

        # Loop over file lines
        fname = fdir + "/%s.pml"%mode
        fname_out = fdir + "/0_mod_%s.pml"%mode
        f_out = open(fname_out, "w")
        with open(fname) as f:
            for line in f:
                line_cmd = ""
                # Add to end of line, depending on command
                if line[0] == "\n":
                    line_add = ""
                elif line[0:4] == "hide":
                    line_add = " %s"%protn

                # All not changed
                elif line[0:8] == "bg_color":
                    line_add = ""
                elif line[0:9] == "set_color":
                    line_add = ""
                elif line[0:6] == "delete":
                    line_add = ""

                else:
                    line_add =  " and %s"%protn
                # Modify line
                line_cmd = line.strip() + line_add + "\n"

                # Write the line
                f_out.write(line_cmd)
            f_out.close()
python end 

# Make pymol objects
python
for i, mode in enumerate(modes):
    protn = '%s_%s' % (prot, mode)
    cmd.copy(protn, prot)
    
    cmd.scene("F1")
    cmd.disable(prot)
    cmd.enable(protn)
    cmd.scene("F%i"%(i+2), "store", mode, view=0)
python end

#################################
# Scenes
# #modes = ['s2', 's2f', 's2s', 'amp_fast', 'amp_slow', 'te', 'tf', 'ts', 'time_fast', 'time_slow', 'rex']

scene F2
@./result_06_check_intermediate/final/pymol/0_mod_s2.pml
scene F2, store, s2: the model-free generalised order parameter (S2 = S2f.S2s), view=0

scene F3
@./result_06_check_intermediate/final/pymol/0_mod_s2f.pml
scene F3, store, s2f: the faster motion model-free generalised order parameter, view=0

scene F4
@./result_06_check_intermediate/final/pymol/0_mod_s2s.pml
scene F4, store, s2s: the slower motion model-free generalised order parameter, view=0

scene F5
@./result_06_check_intermediate/final/pymol/0_mod_amp_fast.pml
scene F5, store, amp_fast, view=0

scene F6
@./result_06_check_intermediate/final/pymol/0_mod_amp_slow.pml
scene F6, store, amp_slow, view=0

scene F7
@./result_06_check_intermediate/final/pymol/0_mod_te.pml
scene F7, store, te: Single motion effective internal correlation time (seconds), view=0

scene F8
@./result_06_check_intermediate/final/pymol/0_mod_tf.pml
scene F8, store, tf: Faster motion effective internal correlation time (seconds), view=0

scene F9
@./result_06_check_intermediate/final/pymol/0_mod_ts.pml
scene F9, store, ts: Slower motion effective internal correlation time (seconds), view=0

scene F10
@./result_06_check_intermediate/final/pymol/0_mod_time_fast.pml
scene F10, store, time_fast, view=0

scene F11
@./result_06_check_intermediate/final/pymol/0_mod_time_slow.pml
scene F11, store, time_slow, view=0

scene F12
@./result_06_check_intermediate/final/pymol/0_mod_rex.pml
scene F12, store, rex: Chemical exchange relaxation (sigma_ex = Rex / omega**2), view=0

