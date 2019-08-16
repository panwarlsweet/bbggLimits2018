#!/bin/bash

LIMFOLDER=$1/Node_SM

INFILE=${LIMFOLDER}/higgsCombineTest.FitDiagnostics.mH120.*.root
DATAFILE=${LIMFOLDER}/ws_hhbbgg.data_bkg.root

NDIMS=2

BKG=${LIMFOLDER}/Background
mkdir ${BKG}

echo $INFILE
echo $BKG

FACT=1.


for icat in {0..11}
do
    python scripts/MakeFullBackgroundFit_Data.py -i ${INFILE} -d ${DATAFILE} -o ${BKG} -c ${icat} --signalFactor ${FACT} ${FACT} --ndims ${NDIMS} --unblind
done

#for ipurity in {0..2}
#do
#    python scripts/CheckExpoCorrelation.py -d ${DATAFILE} -o ${BKG} -p ${ipurity} --mggmax 150
#    python scripts/CheckExpoCorrelation.py -d ${DATAFILE} -o ${BKG} -p ${ipurity} --mggmax 180
#done
