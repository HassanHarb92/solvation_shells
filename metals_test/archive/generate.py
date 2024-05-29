import os

functionals = {
    "B3LYP": "B3LYP empiricaldispersion=gd3",
    "BLYP": "BLYP empiricaldispersion=gd3",
    "HSE06": "HSEH1PBE",
    "M08-HX": "M08HX",
    "svwn": "svwn",
    "PBE0": "PBE1PBE empiricaldispersion=gd3"
}

metals_info = {
    "Ti": [(2, 3), (3, 2)],
    "V": [(2, 4), (3, 3)],
    "Cr": [(2, 5), (3, 4)],
    "Mn": [(2, 6), (3, 5)]
}

for metal, charges_multiplicities in metals_info.items():
    os.makedirs(metal, exist_ok=True)
    for charge, multiplicity in charges_multiplicities:
        subfolder = f"{metal}_{charge}"
        os.makedirs(os.path.join(metal, subfolder), exist_ok=True)
        for name, functional in functionals.items():
            filename = f"{metal}_{charge}_{name}.com"
            filepath = os.path.join(metal, subfolder, filename)
            chk_filename = f"{metal}_{charge}_{name}.chk"
            chk_solvated_filename = f"{chk_filename}_solvated"

            with open(filepath, 'w') as file:
                # Write the first part of the Gaussian input
                file.write(f"%chk={chk_filename}\n")
                file.write(f"#p {functional} 6-31+G(2df,p) ")
                file.write("opt=(cartesian,calcall,maxcycles=500) freq ")
                file.write("scf=(maxcycles=500,xqc,maxconventional=50)\n\n")
                file.write("Title\n\n")
                file.write(f"{charge} {multiplicity}")
                file.write(f"""
{metal}                -0.79303724    0.81880520   -0.09490545
O                 -1.20497055    2.57394081   -0.35687399
H                 -2.12106289    2.64974306   -0.63312164
O                  0.99012218    1.19063487   -0.05794062
H                  1.42696163    0.59979814    0.55970687
O                 -0.81751878    1.03069089    1.71365016
H                 -1.02107924    0.19060168    2.13132590
O                 -0.38506840   -0.93350649    0.17117694
H                 -1.15681661   -1.47369231   -0.01432729
O                 -2.57340546    0.45177807   -0.12185749
H                 -2.77755719   -0.08744013   -0.88928543
O                 -0.76965907    0.60461185   -1.90110947
H                  0.09872499    0.83457273   -2.23949049
H                 -0.96533555   -0.30999395   -2.11741799
H                  1.12208139    2.09942625    0.22124191
H                 -1.07671055    3.05839622    0.46184092
H                 -2.81407445   -0.02398059    0.67650046
H                  0.04220351    1.33615276    2.01180888
H                 -0.11531529   -1.06445929    1.08312323
""")
                file.write("\n\n\n")  # Three blank lines
                # Write the link1 section
                file.write("--Link1--\n")
                file.write(f"%oldchk={chk_filename}\n")
                file.write(f"%chk={chk_solvated_filename}\n")
                file.write(f"#p {functional} scf=(maxcycles=500,xqc,maxconventional=50) ")
                file.write("scrf=(cpcm,solvent=water) geom=allcheck guess=read chkbasis\n\n")
                file.write("\n\n\n")  # Three blank lines

print(f"Generated Gaussian input files for {len(functionals)} functionals for each metal and charge combination.")

