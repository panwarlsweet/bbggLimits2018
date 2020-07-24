#!/bin/bash/

##./makeLT.py inDir/ -x nonres -o outDir -c 2
signal=$1
mass=(260 270 280 300 350 400 450 500 550 600 650 700 800 900 1000)

MX_cut1=(255 265 275 291 337 374 418 464 510 555 615 655 745 835 925)
MX_cut2=(263 275 286 309 360 413 463 514 565 615 680 725 825 925 1025)
##Input directory with samples
indir16="/eos/user/l/lata/Resonant_bbgg/flattening_highmass_"${signal}"2016_fixedbtag/analysistrees_ttHVar/"
indir17="/eos/user/l/lata/Resonant_bbgg/flattening_highmass_"${signal}"2017_fixedbtag/analysistrees_ttHVar/"
indir18="/eos/user/l/lata/Resonant_bbgg/flattening_highmass_"${signal}"2018_fixedbtag/analysistrees_ttHVar/"

##Output directory with Limit Tree (LT) for 1D
#path=.
#LT=LT_1D_Y3_31012020

##Output directory with Limit Tree (LT) for 2D
for imass in {11..14}
do
   path="/eos/user/l/lata/Resonant_bbgg/Run2_LT_trees_PR1186_ttHVar"
   LT=LT_2D_Run2_${signal}_${mass[${imass}]}

   out="$path/$LT"

   mkdir $out

   outdir16="$path/$LT/2016"
   outdir17="$path/$LT/2017"
   outdir18="$path/$LT/2018"

   mkdir $outdir16
   mkdir $outdir17
   mkdir $outdir18

   echo "Start makeLT ..."

   echo ${signal} ${mass[${imass}]} "MX_cut=[" ${MX_cut1[${imass}]}  ${MX_cut2[${imass}]} "]"
##For 2D method
#   echo "./makeLT.py" $indir16 "-x res -l 35.9 -o" $outdir16 "-c 2 -m "${mass[${imass}]} "-MX_1" ${MX_cut1[${imass}]} "-MX_2 "${MX_cut2[${imass}]} "-sig "${signal} "--year 2016"
   ./makeLT.py  $indir16 -x res -o $outdir16 -c 2 -m ${mass[${imass}]} -MX_1 ${MX_cut1[${imass}]} -MX_2 ${MX_cut2[${imass}]} -sig ${signal} --year 2016
   ./makeLT.py  $indir17 -x res -o $outdir17 -c 2 -m ${mass[${imass}]} -MX_1 ${MX_cut1[${imass}]} -MX_2 ${MX_cut2[${imass}]} -sig ${signal} --year 2017
   ./makeLT.py  $indir18 -x res -o $outdir18 -c 2 -m ${mass[${imass}]} -MX_1 ${MX_cut1[${imass}]} -MX_2 ${MX_cut2[${imass}]} -sig ${signal} --year 2018 
   echo "Finish makeLT ..."

   execute_cmd=hadd

   dirout="$path/$LT/merged_"${signal}${mass[${imass}]}
   mkdir $dirout
   dir1="$path/$LT/2016"
   dir2="$path/$LT/2017"
   dir3="$path/$LT/2018"

   file1="LT_DoubleEG.root"
   file2="LT_output_GluGluTo"${signal}"ToHHTo2B2G_M-"${mass[${imass}]}"_narrow_13TeV-madgraph.root"
   file3="LT_output_VBFHToGG_M-125_13TeV_powheg_pythia8.root"
   file4="LT_output_GluGluHToGG_M-125_13TeV_powheg_pythia8.root"
   file5="LT_output_VHToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8.root"
   file6="LT_output_ttHToGG_M125_13TeV_powheg_pythia8.root"
   file7="LT_output_bbHToGG_M-125_13TeV_amcatnlo.root"

   echo "Merging files ..."

   $execute_cmd $dirout/$file1 $dir1/$file1  $dir2/$file1  $dir3/$file1
   $execute_cmd $dirout/$file2 $dir1/$file2  $dir2/$file2  $dir3/$file2
   $execute_cmd $dirout/$file3 $dir1/$file3  $dir2/$file3  $dir3/$file3
   $execute_cmd $dirout/$file4 $dir1/$file4  $dir2/$file4  $dir3/$file4
   $execute_cmd $dirout/$file5 $dir1/$file5  $dir2/$file5  $dir3/$file5
   $execute_cmd $dirout/$file6 $dir1/$file6  $dir2/$file6  $dir3/$file6
   $execute_cmd $dirout/$file7 $dir1/$file7  $dir2/$file7  $dir3/$file7

   echo "Merge of files completed"
done
