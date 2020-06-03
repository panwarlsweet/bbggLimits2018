# How to

* Get latest combine tools ([link](http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/#setting-up-the-environment-and-installation)):
```
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_2_13
cd CMSSW_10_2_13/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v8.0.1
scramv1 b clean; scramv1 b
```
Get this repository code:
```
cd ../
git clone git@github.com:panwarlsweet/bbggLimits2018.git -b ResonantAnalysis
cd bbggLimits2018
scramv1 b
```

## Limit trees

* Run the limit tree maker like so: (-x = res/nonres; -o = output directry; -c = categorisation; -m = resonant mass points; -MX_1 and -MX_2 =  MX mass window cut; -sig Radion or Bulk Graviton; --year =  to pick correct bTag reshape norm. factor and lumi of Run2 year(default is 2016))

```
./makeLT.py /afs/cern.ch/work/l/lata/public/ResHHbbgg/2016/root_files_with_ETH_training_noMjj/  -x res -o LT_OutDir_Radion_300 -c 2 -m 300 -MX_1 288 -MX_2 305 -sig Radion --year 2016
```
* For full run2 limits trees, there is script which will automatically produce all three year LT trees (inculuding bTag norm. factor) and merge them for full Run2 trees for each masss
```
sh run1.sh Radion  # make sure you put correct path of working directly and output location
```
The core code that makes the trees is `bbggLTMaker.C`. It is based on
[TSelector](https://root.cern.ch/developing-tselector) and does not depend on CMSSW, just
the ROOT.  
The goal of this code is to categorize events and make a new tree which *catID* variable,
as well as *mgg* and *mjj*. Different type of categorizations can be done chosen by option `-c Y`:  
```
 Y = 0: 2016 tagger with categorization used in 2016 analysis (4 categories)
 Y = 1: 2017 ETH tagger, using 2016 style categorization (4 categories);
 Y = 2: Run2 Res. tagger, with optimized categorization with MX cut(3 MVA categories);
```


## Fits and limits
* Run the fits and limits on the produced LTs:

```
./runLimit.py -f conf_default.json --mass=300 -o ws_DIR_Name -v 4 -sig Radion
sh scripts/Analyzer.sh mass_point ws_DIR_Name cat_no     #### it runs the limit from 0 to cat_no. for each categroy put 3 for running combinely
# example
sh scripts/Analyzer.sh 300 ws_DIR_Name 3
sh scripts/MakeSMHHFullBkgPlots.sh TEST #### To get background plots in TEST/Node_SM/Background
sh scripts/MakeSMHHSignalPlots.sh TEST #### To get signal plots test/Node_SM/SignalShapes
```  
The process may take a while to complete, especially when running with many categories.  
The config file `conf_default.json` can be edited to provide needed parameters. Some of them are:  
```
 LTDIR: location of the input Limit Trees (expected to be in the local diractory, after running previous step)
 ncat: number of categories. This should much the number of categories produced in limit tries (currently, should be 4 or 12)
 fitStrategy: 2 - for 2D fit of (mgg, mjj); 1 - for 1D fit of mgg, in which case a cut is set to 100<mjj<150 somewhere in runLimit.py script.
```

The results of the limit will be in `LIMS_OutDir/Node_SM/Limit.txt`. In case of problems,
the logfile _mainLog_data-time.log[.bbgg2D]_ can be useful


### Notes on datacards and limits

* Systematic uncertainties are not real (especially the ones for b-tagging and JEC) for
  the case of 2017 categorization (the older numbers are used). Once proper systematics
  are obtained they need to be propagated to template datacards for each category (in
  _templates_ directory).
* The same background fit function is used in all categories (3d order Benrnstein). It may
  be necessary in the future to have different functions in each category. This should be
  modifien from _templates/models_2D_higgs_mjj70_cat*.rs_ files and then taken care in
  _src/bbgg2DFitter.cc_
  
Note that you may see many warnings. They are ignored at the moment, but should be fixed in the future.

* non-integer bin entry:  
```
[#0] WARNING:Plotting -- RooHist::addBin(ch4_plot__mgg) WARNING: non-integer bin entry 14.5154 with Poisson errors, interpolating between Poisson errors of adjacent integer
```  
These are probably due to the fact that the observed data are taken from MC with weights and the events are not integers. 
* parameters at boundary:  
```
[WARNING] Found [CMS_hhbbgg_13TeV_mjj_bkg_slope2_cat0] at boundary.
```

## The ttH cut optimization

* Run the following command to optimize ttH cut for all categories/per catgeory (depends on the arg2 in the command), it will generate a plot for limts vs cut if arg=13 (only when you optimize this for all catgegories)
``` 
sh scripts/tthCutOptimization.sh arg1 arg2   ## arg1=no. of ttH cuts, arg2= cat_no. use accordingly as explained above
```  

## Bias study

* RunBias.sh script is for interactely running. For condor jobs use this script condor_job.sub according to this command 
``` 
condor_submit condor_job.sub DIR=ws_DIR_Name
```  



