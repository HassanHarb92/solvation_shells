from ase import Atoms, Atom
from ase.io import read, write
import numpy as np

# Load the Fe(CN)6 molecule
molecule = read('Fe_CN6.xyz')

# Move the molecule so that Fe is at the center
center_of_mass = molecule.get_center_of_mass()
molecule.translate(-center_of_mass)

# Locate Fe and nitrogen positions
fe_position = molecule.positions[[atom.index for atom in molecule if atom.symbol == 'Fe'][0]]
nitrogen_indices = [atom.index for atom in molecule if atom.symbol == 'N']
nitrogen_positions = molecule.positions[nitrogen_indices]

# Define bond lengths and angles
NH_bond_length = 1.6  # Å
OH_bond_length = 0.95  # Å
HOH_angle = 104.5  # degrees
tetrahedral_angle = 109.5  # degrees

# Function to add a water molecule with correct geometry
def add_water_to_nitrogen(fe_pos, n_position):
    # Calculate the Fe-N vector and normalize it
    fe_n_vector = n_position - fe_pos
    fe_n_unit_vector = fe_n_vector / np.linalg.norm(fe_n_vector)
    
    # Position the first hydrogen along the Fe-N axis
    hydrogen_pos = n_position + NH_bond_length * fe_n_unit_vector
    
    # Create a perpendicular vector for the oxygen
    # We need a vector perpendicular to the Fe-N-H plane. One way to do this is to take an arbitrary vector that's not parallel to the Fe-N axis and cross it with the Fe-N vector.
    arbitrary_vector = np.array([1, 0, 0])  # Just an arbitrary vector
    if np.allclose(fe_n_unit_vector, arbitrary_vector):  # To avoid using a parallel vector
        arbitrary_vector = np.array([0, 1, 0])
    perpendicular_vector = np.cross(fe_n_unit_vector, arbitrary_vector)
    perpendicular_vector = perpendicular_vector / np.linalg.norm(perpendicular_vector)
    
    # Position the oxygen at the correct angle from the hydrogen
    oxygen_pos = hydrogen_pos + OH_bond_length * (np.cos(np.radians(tetrahedral_angle)) * fe_n_unit_vector + np.sin(np.radians(tetrahedral_angle)) * perpendicular_vector)
    
    # Position the second hydrogen atom
    second_hydrogen_pos = oxygen_pos + OH_bond_length * (np.cos(np.radians(HOH_angle)) * (hydrogen_pos - oxygen_pos) / np.linalg.norm(hydrogen_pos - oxygen_pos) + np.sin(np.radians(HOH_angle)) * perpendicular_vector)
    
    # Add the atoms to the molecule
    molecule.append(Atom('H', hydrogen_pos))
    molecule.append(Atom('O', oxygen_pos))
    molecule.append(Atom('H', second_hydrogen_pos))

# Add waters around all nitrogens
for n_pos in nitrogen_positions:
    add_water_to_nitrogen(fe_position, n_pos)

# Save the new structure to an XYZ file
write('Fe_CN6_with_waters.xyz', molecule)

