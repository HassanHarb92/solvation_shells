import os
import shutil
import subprocess

def main():
    # Get all .xyz files in the current directory
    xyz_files = [f for f in os.listdir('.') if f.endswith('.xyz')]

    # Path to the Hydration Shell Radius script
    hydration_script = 'Hydration_shell_radius.py'  # Adjust the path if necessary

    # Create the output directory if it doesn't exist
    hydrated_ready_dir = 'hydrated_ready'
    os.makedirs(hydrated_ready_dir, exist_ok=True)

    for xyz_file in xyz_files:
        base_name = os.path.splitext(xyz_file)[0]
        print(f'\nProcessing {xyz_file}...')

        # Step a: Get the number of atoms and create the input file
        try:
            with open(xyz_file, 'r') as f:
                num_atoms_line = f.readline()
                num_atoms = int(num_atoms_line.strip())
            print(f'Number of atoms in {xyz_file}: {num_atoms}')

            # Create filename.inp
            inp_filename = base_name + '.inp'
            with open(inp_filename, 'w') as f:
                f.write('$fix\n')
                f.write(f'  atoms: 1-{num_atoms}\n')
                f.write('$end\n')
            print(f'Created input file: {inp_filename}')
        except Exception as e:
            print(f'Error processing {xyz_file}: {e}')
            continue

        # Step b: Run xtb on the original xyz file
        cmd_xtb1 = f'xtb {xyz_file} --opt loose --gfn2 --alpb water --chrg -2'
        print(f'Running: {cmd_xtb1}')
        subprocess.run(cmd_xtb1, shell=True)

        # Move xtbopt.xyz to filename_xtb.xyz
        if os.path.exists('xtbopt.xyz'):
            xtb_xyz = f'{base_name}_xtb.xyz'
            shutil.move('xtbopt.xyz', xtb_xyz)
            print(f'Renamed xtbopt.xyz to {xtb_xyz}')
        else:
            print(f'xtbopt.xyz not found after running xtb on {xyz_file}')
            continue

        # Step c: Run the hydration script on the optimized xyz file
        cmd_hydr1 = f'python {hydration_script} {xtb_xyz}'
        print(f'Running: {cmd_hydr1}')
        subprocess.run(cmd_hydr1, shell=True)

        # Check for the solvated xyz file
        solvated_xyz1 = xtb_xyz.replace('.xyz', '_solvated.xyz')
        if os.path.exists(solvated_xyz1):
            print(f'Generated solvated file: {solvated_xyz1}')
        else:
            print(f'{solvated_xyz1} not found after hydration script')
            continue

        # Step d: Run xtb on the solvated xyz file with the input file
        cmd_xtb2 = f'xtb {solvated_xyz1} --opt loose --gfn2 --alpb water --chrg -2  --input {inp_filename}'
        print(f'Running: {cmd_xtb2}')
        subprocess.run(cmd_xtb2, shell=True)

        # Move xtbopt.xyz to filename_xtb_solvated_xtb.xyz
        if os.path.exists('xtbopt.xyz'):
            xtb_solvated_xtb_xyz = f'{base_name}_xtb_solvated_xtb.xyz'
            shutil.move('xtbopt.xyz', xtb_solvated_xtb_xyz)
            print(f'Renamed xtbopt.xyz to {xtb_solvated_xtb_xyz}')
        else:
            print(f'xtbopt.xyz not found after running xtb on {solvated_xyz1}')
            continue

        # Step e: Run the hydration script again
        cmd_hydr2 = f'python {hydration_script} {xtb_solvated_xtb_xyz}'
        print(f'Running: {cmd_hydr2}')
        subprocess.run(cmd_hydr2, shell=True)

        # Check for the second solvated xyz file
        solvated_xyz2 = xtb_solvated_xtb_xyz.replace('.xyz', '_solvated.xyz')
        if os.path.exists(solvated_xyz2):
            print(f'Generated second solvated file: {solvated_xyz2}')
        else:
            print(f'{solvated_xyz2} not found after second hydration script')
            continue

        # Step f: Run xtb on the second solvated xyz file with the input file
        cmd_xtb3 = f'xtb {solvated_xyz2} --opt loose --gfn2 --alpb water --chrg -2 --input {inp_filename}'
        print(f'Running: {cmd_xtb3}')
        subprocess.run(cmd_xtb3, shell=True)

        # Move xtbopt.xyz to filename_final.xyz
        if os.path.exists('xtbopt.xyz'):
            final_xyz = f'{base_name}_final.xyz'
            shutil.move('xtbopt.xyz', final_xyz)
            print(f'Renamed xtbopt.xyz to {final_xyz}')
        else:
            print(f'xtbopt.xyz not found after final xtb run')
            continue

        # Step g: Copy the final xyz file to hydrated_ready directory
        dest_path = os.path.join(hydrated_ready_dir, final_xyz)
        shutil.copy(final_xyz, dest_path)
        print(f'Copied {final_xyz} to {hydrated_ready_dir}')

        # Optional: Clean up intermediate files
        # Uncomment the lines below if you want to remove intermediate files
        os.remove(xtb_xyz)
        os.remove(solvated_xyz1)
        os.remove(xtb_solvated_xtb_xyz)
        os.remove(solvated_xyz2)
        os.remove(final_xyz)
        os.remove(inp_filename)

if __name__ == '__main__':
    main()

