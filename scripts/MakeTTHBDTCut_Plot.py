#!/usr/bin/env python
import sys

#It is called in ttHOptimization.sh script.
#command "pyhton MakeTTHBDTCut_Plot.py arg1" where arg1=no. of ttHcuts used in ttHOptimization.sh
##############################################################################################################

from ROOT import *

gOpt = TGraph()
iCounter = 0

gROOT.SetBatch()
gStyle.SetOptStat(0)

node=["SM","1","2"]
i=0
nmax=sys.argv[1]
print nmax
for x in range(0,int(nmax)):
    
    iCounter = iCounter+1
    cut=0.0+x*0.05
    print cut
    if x > 0 and  x <= 3: continue   
    #if cut < 0:
     #   file = "outDir_m"+str(abs(cut*10))+"/CombinedCard_ARW_/result_1.log"
    #else
    file = "outDir_LIM_node_"+node[i]+"_ttHcut_"+str(iCounter-1)+"/Node_"+node[i]+"/Limit_stat.txt"

    print file

    with open(file) as f:
        for line in f:
            if line.find("50.0%") > -1:
                print line
                lhs, rhs = line.split("<",1)
                print lhs
                limit = float(rhs)
                print "limit = "+str(limit)
                gOpt.SetPoint(iCounter, cut, limit)
                
    
c = TCanvas("c", "c", 800, 600)
plotter = TH1F("ttHcut_vs_Limit",";ttHkiller_cut;limits on 2D fit;", 1, -0.2, 0.5)
plotter.Draw()
plotter.SetMaximum(0.9)
plotter.SetMinimum(0.65)
#c.SetGrid()
gOpt.SetMarkerStyle(33)
gOpt.SetMarkerColor(2)
gOpt.SetMarkerSize(2)
gOpt.Draw("P")

c.SaveAs("ttH_Optimisation.png")
c.SaveAs("ttH_Optimisation.pdf")
c.SaveAs("ttH_Optimisation.root")
