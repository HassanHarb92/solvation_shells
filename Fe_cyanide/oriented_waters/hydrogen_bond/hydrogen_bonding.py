from ase import Atoms
from ase.io import read, write
import numpy as np

# Load the Fe(CN)6 molecule
molecule = read('Fe_CN6.xyz')

# Move the molecule so that Fe is at the center
center_of_mass = molecule.get_center_of_mass()
molecule.translate(-center_of_mass)

# Locate nitrogen positions
nitrogen_indices = [atom.index for atom in molecule if atom.symbol == 'N']
nitrogen_positions = molecule.positions[nitrogen_indices]

# Define bond lengths and angles
NH_bond_length = 1.6  # Å
OH_bond_length = 0.95  # Å
HOH_angle = 104.5  # degrees, converted to radians

# Function to add a water molecule
def add_water_to_nitrogen(n_position):
    # Calculate the position of the first hydrogen
    hydrogen_pos = n_position + np.array([0, 0, NH_bond_length])
    
    # Calculate the position of the oxygen
    oxygen_pos = hydrogen_pos + np.array([0, 0, OH_bond_length])
    
    # Calculate the position of the second hydrogen
    angle_rad = np.radians(HOH_angle)
    second_hydrogen_pos = oxygen_pos + np.array([
        OH_bond_length * np.sin(angle_rad),
        0,
        OH_bond_length * np.cos(angle_rad)
    ])
    
    # Add the atoms to the molecule
    molecule.append('H', hydrogen_pos)
    molecule.append('O', oxygen_pos)
    molecule.append('H', second_hydrogen_pos)

# Add waters around all nitrogens
for n_pos in nitrogen_positions:
    add_water_to_nitrogen(n_pos)

# Save the new structure to an XYZ file
write('Fe_CN6_with_waters.xyz', molecule)

