#!/bin/bash
#this script is used for ttH cut optimization in which first it creates datacards and workspaces with a set of ttHTagger cut (one directory/ttHcut) with runLimit.py script
#then use Analyzer.sh to run limits and MakeTTHBDTCut_Plot.py to plot limit vs ttHcut to see with which ttH cut we get best limit (plot only for arg2=13 for now).
#command "sh scripts/tthCutOptimization.sh arg1 arg2" where arg1=no. of ttH cuts with each having difference=bin value in this script, arg2=how you want to run limts 
#(put=13 for all categories together or use {1,...12} for running categorywise)
#
#NOTE:: With this script no need to run Analyzer.sh and MakeTTHBDTCut_Plot.py separately 
###################################################################################################################################################
nodes="
SM
"

num=0
max=$1  ###for running while loop
cut=-0.05
bin=0.05
cat=$2
CAT=13
for arg in $nodes:
do
    node=$arg
    echo running limits for node $node
    while [ $num -lt $max ]
    do 
    cut=`echo $cut + $bin | bc`

    echo ttH_cut $cut

    echo === step : creating workspace and datacards ===
    echo ./runLimit.py -f conf_default_local.json --node=$node -o outDir_LIM_node_${node}_ttHcut_$num --ttHTaggerCut=$cut
    ./runLimit.py -f conf_default_local.json --node=$node -o outDir_LIM_node_${node}_ttHcut_$num --ttHTaggerCut=$cut

    echo === step : running combine for limits ===
    sh scripts/Analyzer.sh outDir_LIM_node_${node}_ttHcut_$num $cat    

    num=$(( $num + 1 ))
    done

    echo done with node $node
done

if [ $cat -eq $CAT ];then
  python scripts/MakeTTHBDTCut_Plot.py $max
fi
  
