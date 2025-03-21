%chk=deferipronate_red_lowspin.chk
#p uB3LYP empiricaldispersion=gd3 opt=(cartesian,loose,maxcycles=2000,calcfc) scf=(maxcycles=500,xqc,maxconventional=50) cep-31  

deferipronate red low-spin state

-1 1
 C                 -0.20161246    0.53702860   -0.43795880
 C                  0.98813900    1.15015429   -0.50842824
 C                  2.23412336    0.38914316   -0.20779070
 O                  3.27942128    1.06882343   -0.28801061
 C                  2.11191557   -1.09138572    0.14291094
 C                  0.86107158   -1.63879124    0.20503663
 N                 -0.26611319   -0.90931366   -0.03144831
 C                 -1.56263062   -1.60751568    0.12497401
 O                  1.12506079    2.35761651   -0.82029961
 H                  2.98244440   -1.68627097    0.33135359
 H                  0.76149953   -2.67375107    0.45125471
 H                 -1.84673118   -2.05069906   -0.80617145
 H                 -1.46246434   -2.37557811    0.86861416
 H                 -2.31554669   -0.91325182    0.43383888
 Fe                 2.88469915    2.83837742   -0.55869535
 C                  3.66261637    2.94137120    3.10796168
 C                  3.58246347    3.04909220    1.78730384
 C                  4.83272513    2.97525960    0.95823593
 O                  4.65524426    3.10042664   -0.26387350
 C                  6.14280780    2.75764511    1.67957370
 C                  6.06059404    2.31261644    2.96400870
 N                  4.87274880    2.24757297    3.62686687
 C                  4.81208896    1.42833107    4.84659311
 O                  2.50409578    3.17801980    1.18558008
 H                  7.07985015    2.91044724    1.19447519
 H                  6.95143244    2.00978084    3.46695498
 H                  4.55337948    0.41936946    4.56894294
 H                  5.76602024    1.42930476    5.32557045
 H                  4.07479554    1.81140232    5.51299541
 C                  1.35171850    5.65990902   -2.44124503
 C                  2.09273342    4.67049186   -1.99010145
 C                  2.44022737    3.54423384   -2.89491095
 O                  3.08504142    2.65215156   -2.36245026
 C                  1.96557767    3.59027479   -4.32931000
 C                  0.96465474    4.46647548   -4.59691694
 N                  0.54032185    5.36413666   -3.66305337
 C                 -0.76576954    5.99571089   -3.87282685
 O                  2.49223400    4.59684930   -0.82762679
 H                  2.36805692    2.94177338   -5.07960636
 H                  0.49990135    4.45373401   -5.55815735
 H                 -0.65662043    6.90087921   -4.41743063
 H                 -1.39047530    5.31593875   -4.42325688
 H                 -1.21697070    6.19937148   -2.92142134
 C                  2.52628324    3.52432482    3.99628756
 H                  2.12225551    4.40049147    3.51655698
 H                  1.75040116    2.80507636    4.12586580
 H                  2.92447334    3.79827411    4.95147247
 H                  1.86187438    2.54294305    1.50483831
 C                 -1.44741636    1.38027708   -0.77585933
 H                 -1.76308659    1.92088330    0.09423889
 H                 -1.19732861    2.07560507   -1.55392787
 H                 -2.23744859    0.74352357   -1.10599873
 H                  0.57308454    2.90365216   -0.26572199
 C                  1.38351010    7.00368240   -1.67334019
 H                  0.65583306    7.00220058   -0.89561404
 H                  2.36441824    7.13167917   -1.24389885
 H                  1.18788793    7.80903007   -2.34865340
 H                  1.79238216    4.85361788   -0.20733871



--link1--
%chk=deferipronate_red_lowspin.chk
#p ub3lyp geom=allcheck guess=read chkbasis empiricaldispersion=gd3 scf=(maxcycles=500,xqc,maxconventional=50) scrf=(cpcm,solvent=water)


