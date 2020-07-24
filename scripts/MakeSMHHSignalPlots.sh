#!/bin/bash

DIR=$1
Mass=$2
OUT=${DIR}/Node_${Mass}/SignalShapes

mkdir ${OUT}

for icat in {0..2}
do
    python scripts/MakeSigPlot.py -p ${OUT} -w ${DIR}/Node_${Mass}/ws_hhbbgg.HH.sig.mH125_13TeV.root -c ${icat} -o "mjj,mgg" -l "2016+2017 analysis" -a "#font[61]{pp#rightarrowX#rightarrowHH#rightarrowb#bar{b}#gamma#gamma}" -b 24,160 -d 1

done


