#!/usr/bin/env python

from ROOT import *
import argparse, os
from math import sqrt
from HiggsAnalysis.bbggLimits2018.NiceColors import *
#import HiggsAnalysis.bbggLimits2018.CMS_lumi as CMS_lumi
from HiggsAnalysis.bbggLimits2018.MyCMSStyle import *

gROOT.SetBatch()



myLineHeight = 0.02
myLineWidth = 0.05


outf='BMscanResult.root'
limdir='WS/BMScans'

outfile = TFile(limdir+'/'+outf, 'RECREATE')

quantiles = ['0.025', '0.160', '0.500', '0.840', '0.975']
lims = {}
plots = {}
for qt in quantiles:
  lims[qt] = []
  plots[qt] = TGraphAsymmErrors()
  plots[qt].SetName('plot_'+qt.replace('.', 'p').replace("-", "m"))

scan_kl=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

myKl = []
for kl in scan_kl:
    myKl.append(kl+1)
    with open(limdir+'/Limit_stat_BM'+str(kl)+'.txt', 'r') as fp:
        print kl
        line = fp.readline()
        cnt=-1
        print("Line {}: {}".format(cnt, line.strip()))
        while line.find("-- AsymptoticLimits ( CLs ) --") < -0.5:
          line = fp.readline()
        if line.find("-- AsymptoticLimits ( CLs ) --") > -0.5:
          for qt in quantiles:
            line = fp.readline()        
            print("Line {}: {}".format(qt, line.strip()))
            array = line.split(" ")
            if line.find("%") > -0.5:
              lims[qt].append(float(array[len(array)-1]))
#              lims[qt].append(float(array[len(array)-1]))


h1 = TH1F('h1', '', 14, 0.5, 14.5)
h1.GetXaxis().SetTitle("Shape benchmark hypothesis")
h1.GetYaxis().SetTitle("#sigma(pp#rightarrowHH) #times #it{B}(HH#rightarrow#gamma#gammab#bar{b}) [fb]")
h1.SetMaximum(3)
h1.SetStats(0)

print myKl
print lims
for ikl,kl in enumerate(myKl):
  for qt in quantiles:
    plots[qt].SetPoint(ikl, kl, lims['0.500'][ikl])

    plots['0.160'].SetPointError(ikl, 0,0, lims['0.500'][ikl] - lims['0.160'][ikl], lims['0.840'][ikl] - lims['0.500'][ikl] ) 
    plots['0.025'].SetPointError(ikl, 0,0, lims['0.500'][ikl] - lims['0.025'][ikl], lims['0.975'][ikl] - lims['0.500'][ikl] ) 
#    plots['-1'].SetPointError(ikl, myLineWidth,myLineWidth, myLineHeight, myLineHeight )
    plots['0.500'].SetPointError(ikl, myLineWidth,myLineWidth, myLineHeight, myLineHeight )
    thisbin = h1.FindBin(float(kl - 0.01))
    h1.GetXaxis().SetBinLabel(thisbin, str(kl))

smbin = h1.FindBin(12.99)
topbin = h1.FindBin(13.99)
h1.GetXaxis().SetBinLabel(smbin, 'SM')
h1.GetXaxis().SetBinLabel(topbin, '#kappa_{#lambda}= 0')
SetAxisTextSizes(h1)
h1.GetXaxis().SetLabelSize(0.052)

#s2_col = kYellow
s2_col = kOrange
#s1_col = kGreen
s1_col = TColor.GetColor(NiceGreen2)
#th_col = kRed
th_col = TColor.GetColor(NiceRed)
th2_col = TColor.GetColor(NiceOrange)
ob_col = kBlack
#ob_col = TColor.GetColor(NiceBlueDark)
cen_col = cNiceBlueDark

SetGeneralStyle()
c = TCanvas("c", "c", 800, 600)
#c.SetGrid()
h1.Draw()
#plots['0.025'].SetMaximum(11)
plots['0.025'].Draw("PZ same")
plots['0.025'].SetLineColor(s2_col)
plots['0.025'].SetFillColor(s2_col)
plots['0.025'].SetLineWidth(10)
#plots['0.025'].SetTitle("")
#plots['0.025'].GetXaxis().SetLimits(-1, len(klJHEP))
#plots['0.025'].GetYaxis().SetRangeUser(0, 10)
#plots['0.025'].GetXaxis().SetTitle("Shape Benchmark Points")
#plots['0.025'].GetYaxis().SetTitle("#sigma(pp#rightarrowHH)#times#it{B}(HH#rightarrowb#bar{b}#gamma#gamma) [fb]")
c.Update()
plots['0.160'].Draw("EPZ same")
#plots['0.160'].SetMarkerStyle(21)
plots['0.160'].SetMarkerColor(s1_col)
plots['0.160'].SetLineWidth(10)
plots['0.160'].SetLineColor(s1_col)
plots['0.160'].SetFillColor(s1_col)
c.Update()
SetPadStyle(c)
c.Update()
#SetAxisTextSizes(plots['0.025'])
c.Update()
plots['0.500'].SetLineWidth(2)
plots['0.500'].SetLineColor(cen_col)
plots['0.500'].SetFillStyle(1)
plots['0.500'].SetFillColor(cen_col)
plots['0.500'].SetMarkerColor(cen_col)
plots['0.500'].SetMarkerStyle(24)
plots['0.500'].SetMarkerSize(1.1)
plots['0.500'].Draw("P same")

ltx = TLatex()
ltx.SetNDC()
ltx.SetTextSize(.035)
ltx.DrawLatex(0.14,0.83,'#font[61]{pp#rightarrowHH#rightarrow#gamma#gammab#bar{b}}')


leg = TLegend(0.50, 0.6, 0.80, 0.87)
leg.SetFillColorAlpha(kWhite, 0.8)
leg.SetBorderSize(0)
headerTitle = "95% CL upper limits"
leg.SetHeader(headerTitle)
header = leg.GetListOfPrimitives().First()
leg.SetTextSize(.035)
#leg.AddEntry(plots['-1'], 'Observed', 'p')
leg.AddEntry(plots['0.500'], 'Expected', 'p')
leg.AddEntry(plots['0.160'], 'Expected #pm 1 std. deviation', 'l')
leg.AddEntry(plots['0.025'], 'Expected #pm 2 std. deviation', 'l')
leg.Draw("same")


DrawCMSLabels(c, '136.8')

c.SaveAs(limdir+'/'+outf.replace(".root", "sys.pdf"))
c.SaveAs(limdir+'/'+outf.replace(".root", "sys.png"))
