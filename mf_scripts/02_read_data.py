# Python module imports.
from time import asctime, localtime
import os

# relax module imports.
from auto_analyses.dauvergne_protocol import dAuvergne_protocol

# Set up the data pipe.
#######################

# The following sequence of user function calls can be changed as needed.

# Create the data pipe.
bundle_name = "mf (%s)" % asctime(localtime())
name = "origin"
pipe.create(name, 'mf', bundle=bundle_name)

# Load the PDB file.
structure.read_pdb('energy_1.pdb', set_mol_name='ArcCALD', read_model=1)

# Set up the 15N and 1H spins (both backbone and Trp indole sidechains).
structure.load_spins('@N', ave_pos=True)
structure.load_spins('@NE1', ave_pos=True)
structure.load_spins('@H', ave_pos=True)
structure.load_spins('@HE1', ave_pos=True)

# Assign isotopes
spin.isotope('15N', spin_id='@N*')
spin.isotope('1H', spin_id='@H*')

# Load the relaxation data.
relax_data.read(ri_id='R1_600',  ri_type='R1',  frq=600.17*1e6, file='R1_600MHz_new_model_free.dat',  mol_name_col=1, res_num_col=2, res_name_col=3, spin_num_col=4, spin_name_col=5, data_col=6, error_col=7)
relax_data.read(ri_id='R2_600',  ri_type='R2',  frq=600.17*1e6, file='R2_600MHz_new_model_free.dat',  mol_name_col=1, res_num_col=2, res_name_col=3, spin_num_col=4, spin_name_col=5, data_col=6, error_col=7)
relax_data.read(ri_id='NOE_600',  ri_type='NOE',  frq=600.17*1e6, file='NOE_600MHz_new.dat',  mol_name_col=1, res_num_col=2, res_name_col=3, spin_num_col=4, spin_name_col=5, data_col=6, error_col=7)
relax_data.read(ri_id='R1_750',  ri_type='R1',  frq=750.06*1e6, file='R1_750MHz_model_free.dat',  mol_name_col=1, res_num_col=2, res_name_col=3, spin_num_col=4, spin_name_col=5, data_col=6, error_col=7)
relax_data.read(ri_id='R2_750',  ri_type='R2',  frq=750.06*1e6, file='R2_750MHz_model_free.dat',  mol_name_col=1, res_num_col=2, res_name_col=3, spin_num_col=4, spin_name_col=5, data_col=6, error_col=7)
relax_data.read(ri_id='NOE_750', ri_type='NOE', frq=750.06*1e6, file='NOE_750MHz.dat', mol_name_col=1, res_num_col=2, res_name_col=3, spin_num_col=4, spin_name_col=5, data_col=6, error_col=7)

# Define the magnetic dipole-dipole relaxation interaction.
interatom.define(spin_id1='@N', spin_id2='@H', direct_bond=True)
interatom.define(spin_id1='@NE1', spin_id2='@HE1', direct_bond=True)
interatom.set_dist(spin_id1='@N*', spin_id2='@H*', ave_dist=1.02 * 1e-10)
interatom.unit_vectors()

# Define the chemical shift relaxation interaction.
value.set(-172 * 1e-6, 'csa', spin_id='@N*')
