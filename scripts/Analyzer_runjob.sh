#!/bin/bash
#This script run limits using Higgs combime tool. It is called in tthCutOptimization.sh scripts.
#command "sh scripts/Analyzer.sh arg1 arg2" where arg1=directory to run the limits and save the result and arg2=run the limits for each catgegry if arg2={1....12}. 
#use arg2=13 if want to run for categories combinely.
########################################################################################################################################################
source /cvmfs/cms.cern.ch/cmsset_default.sh
echo '=== Preparing datacards in root format ==='
cd /afs/cern.ch/work/l/lata/bbggLimits/CMSSW_8_1_0/src/HiggsAnalysis/bbggLimits2018
eval `scram runtime -sh`
DIR=/afs/cern.ch/work/l/lata/bbggLimits/CMSSW_8_1_0/src/HiggsAnalysis/bbggLimits2018/$1/Node_SM  
echo $DIR
opt=$2   ##put no of categroies for which you want to run limits as 2nd arguement
opt_1=13

if [ $opt -eq $opt_1 ];then

  echo 'running for all categories'

  text2workspace.py $DIR/hhbbgg_13TeV_DataCard.txt $DIR/hhbbgg_13TeV_DataCard.root -m 125

  cd $DIR

  printf '\n=== Start fitting for background plots ==\n\n'

  combine -M FitDiagnostics -t -1 -d hhbbgg_13TeV_DataCard.root -S 0  --saveWorkspace --saveShapes --saveNormalization  --saveToys --savePredictionsPerToy -s -1 --X-rtd TMCSO_AdaptivePseudoAsimov=100

  printf '\n=====\n\n'

  combine -M AsymptoticLimits -d hhbbgg_13TeV_DataCard.root --run blind -m 125 -n SM_13TeV_3ab -S 0 -s -1 --X-rtd TMCSO_AdaptivePseudoAsimov=100&> Limit_stat_ttH0.txt
#  combine -M AsymptoticLimits -d hhbbgg_13TeV_DataCard.root --run blind -m 125 -n SM_13TeV_3ab &> Limit.txt

  echo '== 3.1) Finished stat only limits'

  tail  Limit_stat_ttH0.txt
#  tail  Limit.txt

  cd -

  printf '\n== END ===\n\n'

elif [ $opt -ne $opt_1 ];then

icat=0

  while [ $icat -lt $opt ]
  do

     text2workspace.py $DIR/hhbbgg_13TeV_DataCard_cat${icat}.txt $DIR/hhbbgg_13TeV_DataCard_cat${icat}.root -m 125

     cd $DIR

     printf '\n=== Start fitting for background plots ==\n\n'

     combine -M FitDiagnostics -t -1 -d hhbbgg_13TeV_DataCard_cat${icat}.root -S 0  --saveWorkspace --saveShapes --saveNormalization  --saveToys --savePredictionsPerToy

     printf '\n=====\n\n'

     combine -M AsymptoticLimits -d hhbbgg_13TeV_DataCard_cat${icat}.root --run blind -m 125 -n SM_13TeV_3ab -S 0 &> Limit_stat_cat${icat}.txt

     echo '== 3.1) Finished stat only limits for cat='$icat 

     tail   Limit_stat_cat${icat}.txt

     cd -

     printf '\n== END ===\n\n'
     icat=$(( $icat + 1 ))
  done
fi
