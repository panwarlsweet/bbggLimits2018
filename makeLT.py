#!/usr/bin/env python

from ROOT import *
import os,json
gROOT.SetBatch()
from SMHiggsSamples import *
from utils import *

import argparse
parser =  argparse.ArgumentParser(description='Limit Tree maker')
parser.add_argument("indir", help = "Input directory with flat trees.")
parser.add_argument('-x', nargs='+', choices=['res', 'nonres'], required=True, default=None,
                    help = "Choose which samlples to create the trees from.")
parser.add_argument("-v", "--verbosity",  dest="verb", action="store_true", default=False,
                    help="Print out more stuff")
parser.add_argument("-l", "--lumi", dest="lumi", default=35.9,
                    help="Integrated lumi to scale signal")
parser.add_argument('-o', '--outDir', dest="outDir", type=str, default=None,
                    required=True, help="Output directory (will be created).")
parser.add_argument('-c', '--categ', dest="categ", type=int, default=0,
                    choices = [0,1,2,3], help="Which categorization to use. 0 - 2016 tagger; 1 - 2017 ETH tagger, using 2016 style categorization; 2 - 2017 ETH tagger, with optimized categorization; 3 - 2017 tagger with mjj cuts."
)
parser.add_argument('-MX_1', '--MX_cut1', dest="MX_cut1", type=float, default=0.,
                    required=True, help="MX mass window for resonant analysis.")
parser.add_argument('-MX_2', '--MX_cut2', dest="MX_cut2", type=float, default=35000.,
                    required=True, help="MX mass window for resonant analysis.")
parser.add_argument('-sig', '--signal', dest="signal", type=str, default=None,
                    required=True, help="is it Radion or Graviton?")
parser.add_argument('-m', '--mass', dest="mass", type=str, default="260",
                    required=True, help="resonant mass point.")

opt = parser.parse_args()

#mass =  [260, 300, 350, 450, 700]
_ttHTagger=0;

if opt.verb>0:
  print SMHiggsNodes


if __name__ == "__main__":
  print "This is the __main__ part"

  createDir(opt.outDir)
  if 'res' in opt.x:

      print "Doing signal", opt.signal, opt.mass

      fChain = TChain("tagsDumper/trees/bbggtrees")
      fname = opt.indir+"/output_GluGluTo"+str(opt.signal)+"ToHHTo2B2G_M-"+str(opt.mass)+"_narrow_13TeV-madgraph.root"
      print fname
      fChain.Add(fname)
      ttHkiller = fChain.GetListOfBranches().FindObject("ttHScore");
      if ttHkiller: _ttHTagger=1
      rootName = fname[fname.rfind('/')+1:]
      if opt.verb: print rootName

      outFileName = opt.outDir+"/LT_"+rootName

      fChain.Process("bbggLTMaker.C+", "%.10f %s %i %i %i %.01f %.01f %s %s" % ( opt.lumi, outFileName, 0, opt.categ, _ttHTagger, opt.MX_cut1, opt.MX_cut2, opt.signal, opt.mass) )

      print "Done with signal"

      print "Doing Single Higgs samples"
      for n in SMHiggsNodes:
        if opt.verb: print n
        fChain = TChain("tagsDumper/trees/bbggtrees")
        fname = opt.indir+n[0]
        fChain.Add(fname)
        outFileName = opt.outDir+"/LT_"+n[0]

        fChain.Process("bbggLTMaker.C+", "%.10f %s %i %i %i  %.01f %.01f %s %s" % ( opt.lumi, outFileName, 1, opt.categ, _ttHTagger, opt.MX_cut1, opt.MX_cut2, opt.signal, opt.mass) )

      os.system('hadd -f '+opt.outDir+'/LT_output_bbHToGG_M-125_13TeV_amcatnlo.root '+opt.outDir+'/LT_output_bbHToGG_M-125_4FS_yb*.root')

      print "Done with Single Higgs"

      fChain = TChain("tagsDumper/trees/bbggtrees")
      # fname = opt.indir+'/DoubleEG.root'
      fname = opt.indir+'/FakeData/DoubleEG.root'
      fChain.Add(fname)
      outFileName = opt.outDir+"/LT_DoubleEG.root"
    
      fChain.Process("bbggLTMaker.C+", "%f %s %i %i %i %.01f %.01f %s %s" % ( 1, outFileName, 0, opt.categ, _ttHTagger, opt.MX_cut1, opt.MX_cut2, opt.signal, opt.mass) )
    
      print "Done with Data"
   
  print "Done with Main"

