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
