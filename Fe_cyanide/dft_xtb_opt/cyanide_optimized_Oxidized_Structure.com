%chk=cyanide_optimized_Oxidized_Structure.chk
#p B3LYP empiricaldispersion=gd3 scrf=(cpcm,solvent=water) scf=(maxcycles=500,xqc,maxconventional=1000) 6-31+G(2df,p)

Oxidized_Structure

-3 2
Fe        -0.00005       -0.00018        0.00006
C         -1.42306        1.39194       -0.02169
C         -1.39203       -1.42336       -0.01658
C          0.02706       -0.00348       -1.98599
C          1.42326       -1.39196        0.02171
C          1.39168        1.42333        0.01664
C         -0.02715        0.00310        1.98610
N         -2.25983        2.21101       -0.03460
N         -2.21082       -2.26042       -0.02639
N          0.04301       -0.00538       -3.15811
N          2.26110       -2.20998        0.03416
N          2.21010        2.26076        0.02633
N         -0.04320        0.00504        3.15821


