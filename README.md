# Simple workflow for modeling solvations of metal ions in water
1. Hydration_shell.py places a number of water molecules at a user defined radius
2. xtb_thermo.py performs optimization and frequency calculations on .xyz structure using --gfn2 
3. generate_gaussian.py generates a list of single-point calculations using ~30 DFT functionals, accounts for dispersion when possible 
4. In case of non-spherical systems, i.e. mixed anions, we create a convex hull instead of a sphere: Hydration_convex_hull.py 
5. A simpler one is Hydration_and_xtb.py which calculates the center of the molecule, determines a sphere and places waters accordingly.

## Testing on Fe systems
1. Fe Boron complexes (enumerated with in-house code)
2. Fe + 2 ions 
 
