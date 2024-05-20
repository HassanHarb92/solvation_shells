# Simple workflow for modeling solvations of metal ions in water
1. Hydration_shell.py places a number of water molecules at a user defined radius
2. xtb_thermo.py performs optimization and frequency calculations on .xyz structure using --gfn2 
3. generate_gaussian.py generates a list of single-point calculations using ~30 DFT functionals, accounts for dispersion when possible 
4. In case of non-spherical systems, i.e. mixed anions, we create a convex hull instead of a sphere: Hydration_convex_hull.py 


## Next
1. Test on different systems: Ti, V, Cr, Mn, and Co
