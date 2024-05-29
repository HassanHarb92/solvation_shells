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
        if log_file.endswith('.log'):
            xyz_file = log_file.replace('.log', '.xyz')
            convert_log_to_xyz(log_file, xyz_file)

if __name__ == "__main__":
    process_files()

