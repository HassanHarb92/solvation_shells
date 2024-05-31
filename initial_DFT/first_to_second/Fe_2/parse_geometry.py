import os
import subprocess
import pandas as pd
import numpy as np

def convert_log_to_xyz(log_file, xyz_file):
    try:
        subprocess.run(['obabel', log_file, '-O', xyz_file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error converting {log_file} to {xyz_file}: {e}")

def parse_xyz(xyz_file):
    atoms = []
    coordinates = []
    with open(xyz_file, 'r') as xyz:
        lines = xyz.readlines()
        for line in lines[2:]:
            parts = line.split()
            atoms.append(parts[0])
            coordinates.append([float(x) for x in parts[1:4]])
    return atoms, np.array(coordinates)

def calculate_bond_length(coords1, coords2):
    return np.linalg.norm(coords1 - coords2)

def process_files():
    data = []
    for log_file in os.listdir('.'):
        if log_file.endswith('.xyz'):
            xyz_file = log_file
#            xyz_file = log_file.replace('.log', '.xyz')
#            convert_log_to_xyz(log_file, xyz_file)
            
            atoms, coordinates = parse_xyz(xyz_file)
            fe_coords = coordinates[atoms.index('Fe')]
            o_coords = [coordinates[i] for i in range(len(atoms)) if atoms[i] == 'O']

            bond_lengths = []
            for o in o_coords:
                bond_length = calculate_bond_length(fe_coords, o)
                bond_lengths.append(bond_length)
            
            bond_lengths.sort()  # Sort bond lengths to find the lowest six
            six_lowest_bonds = bond_lengths[:6]

            # Modify the log file name
            modified_name = log_file[5:-4]
            data.append([modified_name] + six_lowest_bonds)

    # Create DataFrame and save to CSV
    df = pd.DataFrame(data, columns=['File Name', 'Fe-O Bond 1', 'Fe-O Bond 2', 'Fe-O Bond 3', 'Fe-O Bond 4', 'Fe-O Bond 5', 'Fe-O Bond 6'])
    df.to_csv('bond_lengths.csv', index=False)
    print("Bond lengths have been saved to bond_lengths.csv")

if __name__ == "__main__":
    process_files()

