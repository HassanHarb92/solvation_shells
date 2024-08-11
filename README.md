# Simple workflow for modeling solvations of metal ions in water
1. Hydration_shell.py places a number of water molecules at a user defined radius
2. xtb_thermo.py performs optimization and frequency calculations on .xyz structure using --gfn2 
3. generate_gaussian.py generates a list of single-point calculations using ~30 DFT functionals, accounts for dispersion when possible 
4. In case of non-spherical systems, i.e. mixed anions, we create a convex hull instead of a sphere: Hydration_convex_hull.py 
5. A simpler one is Hydration_and_xtb.py which calculates the center of the molecule, determines a sphere and places waters accordingly.

## Testing on Fe systems
1. Fe + 2 ions: the mechanism might require desolvation of Fe metals. i.e. we need to consider Fe(H2O)n --> Fe + nH2O
2. Expand the approach: Take metal+ligand+waters then add 2 solvation shells, get xTB geometry, then DFT single points 
3. FeCN6 is still challenging, b3lyp/mbs then single point on larger basis is working. Still need to address the issue with H-bonding.. Try other functionals to see if they perform better, also check: https://schlegelgroup.wayne.edu/Pub_folder/258.pdf

## Metals that dont work
1. check the chemistry of the reaction, model possible side reactions
2. Cu is giving good results

