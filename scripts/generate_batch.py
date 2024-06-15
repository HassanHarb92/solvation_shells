import os
import math

# Directory containing .com files
com_files_dir = '.'  # replace with your actual directory
pbs_files_dir = '.'  # replace with your desired directory to save pbs files
os.makedirs(pbs_files_dir, exist_ok=True)

# Get list of .com files
com_files = [f for f in os.listdir(com_files_dir) if f.endswith('.com')]
num_files_per_pbs = 13
num_pbs_files = math.ceil(len(com_files) / num_files_per_pbs)

pbs_template = """#!/bin/sh
#PBS -N g16-batch-{batch_num:04d}
#PBS -l select=1:ncpus=128
#PBS -l walltime=72:00:00
#PBS -q compute
#PBS -e g16-batch-{batch_num:04d}.stderr
#PBS -A AICarbonFree
cd $PBS_O_WORKDIR

module load gaussian/16.C.02
export GAUSS_SCRDIR=/scratch
export GAUSS_WDEF="$(cat $PBS_NODEFILE | paste -d, -s)"
export GAUSS_CDEF=0-127
export GAUSS_MDEF=100GB
export GAUSS_SDEF=ssh
"""

# Create PBS files
for i in range(num_pbs_files):
    batch_num = i + 1
    pbs_filename = os.path.join(pbs_files_dir, f'g16-batch-{batch_num:04d}.pbs')
    with open(pbs_filename, 'w') as pbs_file:
        pbs_file.write(pbs_template.format(batch_num=batch_num))
        
        # Add g16 commands for this PBS file
        for j in range(num_files_per_pbs):
            com_index = i * num_files_per_pbs + j
            if com_index < len(com_files):
                com_file = com_files[com_index]
                log_file = com_file.replace('.com', '.log')
                pbs_file.write(f'g16 {com_file} > {log_file}\n')

print(f"Created {num_pbs_files} PBS files in {pbs_files_dir}")

