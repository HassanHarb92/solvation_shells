import os
import re
import pandas as pd

# Define directories
dir_3 = 'inputs_Fe3plus_HS'
dir_2 = 'inputs_Fe2plus_HS'

# Regular expression to find SCF Done values
scf_regex = re.compile(r'SCF Done:\s+E\(.*\)\s+=\s+([-.\d]+)')

# Function to extract the last SCF Done value from a log file
def extract_scf_energy(filepath):
    with open(filepath, 'r') as file:
        content = file.read()
    scf_values = scf_regex.findall(content)
    return float(scf_values[-1]) if scf_values else None

# Prepare a list to store the data
data = []

# Iterate through the files in the Fe3+ directory
for filename in os.listdir(dir_3):
    if filename.endswith('.log'):
        label = filename.split('_')[1].zfill(4)
        scf_3 = extract_scf_energy(os.path.join(dir_3, filename))
        
        # Corresponding file in the Fe2+ directory
        corresponding_file_2 = filename.replace('Fe3plus', 'Fe2plus')
        scf_2 = extract_scf_energy(os.path.join(dir_2, corresponding_file_2))
        
        if scf_3 is not None and scf_2 is not None:
            delta_scf = (scf_2 - scf_3) * 2625.5 * 1000
            e_red = - delta_scf / (96485 * 1) - 1.24 - 3.25 + 0.2
            data.append([label, scf_3, scf_2, delta_scf, e_red])

# Create the dataframe
df = pd.DataFrame(data, columns=['XXXX', 'SCF_3', 'SCF_2', 'Delta_SCF', 'E_red'])


# Save the dataframe to a CSV file
df.to_csv('Fe_Boryls_HS.csv', index=False)

