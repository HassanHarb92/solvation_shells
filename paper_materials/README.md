# SI for paper

The code and structures used in this study are available at https://github.com/HassanHarb92/solvation_shells/paper_materials. Within this repository, the codes folder contains the following Python scripts:
1.	Hydration_shell_radius.py: This script places spherical layers of water molecules around a given structure at a radius calculated as radius = max_distance+ 1.5. It reads in optimized structure coordinates (.xyz) and generates one or more solvation shells at specified radii.
2.	run_multiple_xtb.py: This script generates water layers around a structure and performs xTB calculations on the water molecules while freezing the coordinates of the main structure. It repeats the process twice to simulate multiple solvation layers.
Additionally, the structures folder in the main repository contains the. xyz structures of all the complexes used in this study.

The repository also includes a web_app folder with stream_app.py, a web application that visualizes the molecules in 3D within a web browser, providing an interactive view of the structures and solvation shells.

All results, energies, and structures related to this study can be found in the repository under solvation_shells/results.

