import os
import re
import pandas as pd

# Define the directory containing the log files
log_files_directory = "."

# Define a pattern to match the "SCF Done" line
scf_pattern = re.compile(r"SCF Done:\s+E\(UB3LYP\)\s+=\s+(-?\d+\.\d+)")

# Initialize a dictionary to store the results
data = {
    "Metal": [],
    "Basis_Set": [],
    "SCF_2": [],
    "SCF_3": [],
    "Delta_E": [],
    "Voltage": [],
    "Experimental": [],
    "Error": []
}

# Define experimental values
experimental_values = {
    "Ti": -0.368,
    "V": -0.255,
    "Cr": -0.407,
    "Mn": 1.509
}

# Function to parse the last SCF Done value from a log file
def parse_scf_done(file_path):
    scf_values = []
    with open(file_path, 'r') as file:
        for line in file:
            match = scf_pattern.search(line)
            if match:
                scf_values.append(float(match.group(1)))
    return scf_values[-1] if scf_values else None

# Dictionary to store SCF values temporarily
scf_data = {}

# Process each log file
for filename in os.listdir(log_files_directory):
    if filename.endswith(".log"):
        parts = filename.split('_')
        metal = parts[0]
        charge = parts[1]
        basis_set = parts[-1].split('.')[0]
        scf_value = parse_scf_done(os.path.join(log_files_directory, filename))

        key = (metal, basis_set)
        if key not in scf_data:
            scf_data[key] = {"SCF_2": None, "SCF_3": None}
        
        if charge == "2":
            scf_data[key]["SCF_2"] = scf_value
        elif charge == "3":
            scf_data[key]["SCF_3"] = scf_value

# Fill the data dictionary with parsed SCF values
for (metal, basis_set), scf_values in scf_data.items():
    scf_2 = scf_values["SCF_2"]
    scf_3 = scf_values["SCF_3"]

    if scf_2 is not None and scf_3 is not None:
        delta_e = scf_2 - scf_3
        voltage = -((delta_e * 2625.5 * 1000) / (96485 * 1) + 1.24 + 3.25 - 0.2)
        experimental = experimental_values.get(metal, None)
        error = voltage - experimental if experimental is not None else None

        data["Metal"].append(metal)
        data["Basis_Set"].append(basis_set)
        data["SCF_2"].append(scf_2)
        data["SCF_3"].append(scf_3)
        data["Delta_E"].append(delta_e)
        data["Voltage"].append(voltage)
        data["Experimental"].append(experimental)
        data["Error"].append(error)

# Create a DataFrame from the data dictionary
df = pd.DataFrame(data)

# Display the DataFrame
print(df.head())


output_csv_path = "results.csv"
df.to_csv(output_csv_path, index=False)






