#!/usr/bin/env python

import ROOT
import imp
from array import array
from collections import OrderedDict
import math

xsec_theory={ ### XX->HH in fb
  "BulkGrav": OrderedDict([ ### k/Mpl = 0.5 https://github.com/CrossSectionsLHC/WED/blob/master/KKGraviton_Bulk/AnalysesTables/BulkGraviton_yr4_13TeV_kmpl0p5_hh4b.dat https://github.com/CrossSectionsLHC/WED/blob/master/KKGraviton_Bulk/AnalysesTables/BulkGraviton_yr4_13TeV_kmpl0p5_hh4b_lowmass.dat
    (750 , 2.04e+01), 
    (800 , 1.50e+01), 
    (900 , 8.16e+00), 
    (1000, 4.74e+00), 
    (1100, 3.00e+00), 
    (1200, 1.90e+00), 
    (1300, 1.20e+00), 
    (1400, 7.63e-01), 
    (1500, 4.83e-01), 
    (1600, 3.30e-01), 
    (1700, 2.26e-01), 
    (1800, 1.55e-01), 
    (1900, 1.09e-01), 
    (2000, 7.65e-02), 
    (2100, 5.58e-02), 
    (2200, 4.07e-02), 
    (2300, 2.97e-02), 
    (2400, 2.17e-02), 
    (2500, 1.58e-02), 
    (2600, 1.18e-02), 
    (2700, 8.87e-03), 
    (2800, 6.64e-03), 
    (2900, 4.98e-03), 
    (3000, 3.73e-03), 
    ]), 
  "Radion": OrderedDict([ ### Lambda = 3 TeV https://github.com/CrossSectionsLHC/WED/blob/master/Radion_Bulk/AnalysesTables/BulkRadion_yr4_13TeV_NLO_LR_3TeV_hh4b.dat https://github.com/CrossSectionsLHC/WED/blob/master/Radion_Bulk/AnalysesTables/BulkRadion_yr4_13TeV_NLO_LR_3TeV_hh4b_lowmass.dat
    (750 , 5.27e+01), 
    (800 , 4.37e+01), 
    (900 , 3.00e+01), 
    (1000, 2.11e+01), 
    (1100, 1.54e+01), 
    (1200, 1.12e+01), 
    (1300, 8.20e+00), 
    (1400, 5.99e+00), 
    (1500, 4.37e+00), 
    (1600, 3.33e+00), 
    (1700, 2.53e+00), 
    (1800, 1.92e+00), 
    (1900, 1.49e+00), 
    (2000, 1.15e+00), 
    (2100, 9.04e-01), 
    (2200, 7.11e-01), 
    (2300, 5.59e-01), 
    (2400, 4.40e-01), 
    (2500, 3.46e-01), 
    (2600, 2.75e-01), 
    (2700, 2.20e-01), 
    (2800, 1.75e-01), 
    (2900, 1.39e-01), 
    (3000, 1.11e-01), 
    ]),
  "Radion_L1TeV": OrderedDict([ ### Lambda = 1 TeV https://github.com/CrossSectionsLHC/WED/blob/master/Radion_Bulk/AnalysesTables/BulkRadion_yr4_13TeV_NLO_LR_1TeV_hh4b_lowmass.dat https://github.com/CrossSectionsLHC/WED/blob/master/Radion_Bulk/AnalysesTables/BulkRadion_yr4_13TeV_NLO_LR_1TeV_hh4b.dat
    (750 , 4.74e+02), 
    (800 , 3.93e+02), 
    (900 , 2.70e+02), 
    (1000, 1.90e+02), 
    (1100, 1.38e+02), 
    (1200, 1.01e+02), 
    (1300, 7.38e+01), 
    (1400, 5.39e+01), 
    (1500, 3.93e+01), 
    (1600, 2.99e+01), 
    (1700, 2.28e+01), 
    (1800, 1.73e+01), 
    (1900, 1.34e+01), 
    (2000, 1.03e+01), 
    (2100, 8.13e+00), 
    (2200, 6.40e+00), 
    (2300, 5.03e+00), 
    (2400, 3.96e+00), 
    (2500, 3.11e+00), 
    (2600, 2.48e+00), 
    (2700, 1.98e+00), 
    (2800, 1.57e+00), 
    (2900, 1.26e+00), 
    (3000, 1.00e+00), 
    ]),
  }

BR_HH2b2g = 0.58*0.00227*2

def getIntersection(gr1, gr2): ### Return a TGraph with the points of intersection 
  
  interPoint = ROOT.TGraph()
  i=0

  ### Loop over all points in this TGraph
  for a_i in xrange(0, gr1.GetN()):
    ### Loop over all points in the other TGraph
    for b_i in xrange(0, gr2.GetN()):
      ### Get the current point, and the next point for each of the objects
      x1=ROOT.Double(0)
      x2=ROOT.Double(0)
      y1=ROOT.Double(0)
      y2=ROOT.Double(0)
      ax1=ROOT.Double(0)
      ax2=ROOT.Double(0)
      ay1=ROOT.Double(0)
      ay2=ROOT.Double(0)
      gr1.GetPoint(a_i   , x1 , y1 )
      gr1.GetPoint(a_i+1 , x2 , y2 )
      gr2.GetPoint(b_i   , ax1, ay1)
      gr2.GetPoint(b_i+1 , ax2, ay2)
      ### Calculate the intersection between two straight lines, x axis
      x = (ax1 *(ay2 *(x1-x2)+x2 * y1 - x1 * y2 )+ ax2 * (ay1 * (-x1+x2)- x2 * y1+x1 * y2)) / (-(ay1-ay2) * (x1-x2)+(ax1-ax2)* (y1-y2));
      ### Calculate the intersection between two straight lines, y axis
      y = (ax1 * ay2 * (y1-y2)+ax2 * ay1 * (-y1+y2)+(ay1-ay2) * (x2 * y1-x1 * y2))/(-(ay1-ay2) * (x1-x2)+(ax1-ax2) * (y1-y2));
      ### Find the tightest interval along the x-axis defined by the four points
      xrange_min = max(min(x1, x2), min(ax1, ax2));
      xrange_max = min(max(x1, x2), max(ax1, ax2));

      ### If points from the two lines overlap, they are trivially intersecting
      if (x1 == ax1 and y1 == ay1) or (x2 == ax2 and y2 == ay2):              
        interPoint.SetPoint(i, x1 if (x1 == ax1 and y1 == ay1) else x2, y1 if (x1 == ax1 and y1 == ay1) else y2) 
        i = i+1
      ### If the intersection between the two lines is within the tight range, add it to the list of intersections.
      elif x > xrange_min and x < xrange_max: 
        interPoint.SetPoint(i,x, y);
        i = i+1
  return interPoint;

def getLimit(model,masses,tag,scale=1):

  print tag, ' ', masses 

  #grobslim = ROOT.TGraph(len(masses))
  grexplim = ROOT.TGraph(len(masses))
  grexp1sig = ROOT.TGraphAsymmErrors(len(masses))
  grexp2sig = ROOT.TGraphAsymmErrors(len(masses))

  #grobslim .SetName('grobslim' +'_'+model+'_'+'_'+tag) 
  grexplim .SetName('grexplim' +'_'+model+'_'+'_'+tag) 
  grexp1sig.SetName('grexp1sig'+'_'+model+'_'+'_'+tag) 
  grexp2sig.SetName('grexp2sig'+'_'+model+'_'+'_'+tag) 

  print model
  for mass in masses:
    i = masses.index(mass)
    xsec = 1.
    f = ROOT.TFile.Open("Run2_first_RD_results_3rdJune2020/AsymptoticRootFiles/higgsCombine_13TeV_%s_%s.AsymptoticLimits.mH125.root" % (model, mass), "READ")
    limit = f.Get("limit")
    entries = limit.GetEntriesFast()
    obs = 0
    exp = 0
    exp1sLow  = 0
    exp1sHigh = 0
    exp2sLow  = 0
    exp2sHigh = 0
    for e in limit:
      quant = e.quantileExpected
      lim = e.limit
      if quant == -1: obs = lim 
      elif quant > 0.024 and quant < 0.026: exp2sLow = lim 
      elif quant > 0.15 and quant < 0.17: exp1sLow = lim 
      elif quant == 0.5: exp = lim
      elif quant > 0.83 and quant < 0.85: exp1sHigh = lim
      elif quant > 0.97 and quant < 0.98: exp2sHigh = lim 
    #grobslim .SetPoint(i, mass, scale*xsec*obs)
    grexplim .SetPoint(i, mass, scale*xsec*exp)
    grexp1sig.SetPoint(i, mass, scale*xsec*exp)
    grexp2sig.SetPoint(i, mass, scale*xsec*exp)
    grexp1sig.SetPointError(i, 0, 0, scale*xsec*abs(exp-exp1sLow), scale*xsec*abs(exp1sHigh-exp))
    grexp2sig.SetPointError(i, 0, 0, scale*xsec*abs(exp-exp2sLow), scale*xsec*abs(exp2sHigh-exp))
    print "mass %i & exp %3.1f & obs %3.1f \\\\" % (mass, scale*xsec*exp, scale*xsec*obs)
    grobslim=1.0
  return grexplim, grexp1sig, grexp2sig

def plotLimits(model, masses):
  """
  n = len(xsec_theory[model].keys())
  grtheory = ROOT.TGraph(n)
  grtheory.SetName('grtheory_'+model)

  grtheory1 = ROOT.TGraph(n)
  grtheory1.SetName('grtheory1_'+model)

  Lambda=3
  kMpl=0.5
  Lambda1=1
  kMpl1=1.0
  i = 0
  for key in xsec_theory[model].keys():
    grtheory.SetPoint(i, key, xsec_theory[model][key])
    if model=="Radion": 
      grtheory1.SetPoint(i, key, xsec_theory[model][key]*pow(Lambda/Lambda1,2.))
    elif model=="BulkGrav": 
      grtheory1.SetPoint(i, key, xsec_theory[model][key]*pow(kMpl1/kMpl, 2.))
    i=i+1
  """
  grexplim, grexp1sig, grexp2sig = getLimit(model,masses,"HHbbgg")
  
  grexplim_hllhc, grexp1sig_hllhc, grexp2sig_hllhc = \
      getLimit(model,masses,"HHbbgg")
  """
  intersects=getIntersection(grtheory1, grexplim)
  for i in xrange(0, intersects.GetN()):
    xe = ROOT.Double(0)
    ye = ROOT.Double(0)
    intersects.GetPoint(i, xe,ye)
    print ">>>>>> exp. lim = %f GeV at %f fb" % (xe, ye)

  intersects=getIntersection(grtheory1, grobslim)
  for i in xrange(0, intersects.GetN()):
    xe = ROOT.Double(0)
    ye = ROOT.Double(0)
    intersects.GetPoint(i, xe,ye)
    print ">>>>>> obs. lim = %f GeV at %f fb" % (xe, ye)
  """
  tdrstyle = imp.load_source('tdrstyle', '/eos/user/l/lata/HH4b/upgrades/CMSSW_9_3_2/src/Upgrades/VBFAnalyzer/tdrstyle.py')
  CMS_lumi = imp.load_source('CMS_lumi', '/eos/user/l/lata/HH4b/upgrades/CMSSW_9_3_2/src/Upgrades/VBFAnalyzer/CMS_lumi.py')
  ROOT.gROOT.SetBatch()
  ROOT.gROOT.SetStyle("Plain")
  ROOT.gStyle.SetOptStat()
  ROOT.gStyle.SetOptTitle(0)
  ROOT.gStyle.SetPalette(1)
  ROOT.gStyle.SetNdivisions(405,"x");
  ROOT.gStyle.SetEndErrorSize(0.)
  ROOT.gStyle.SetErrorX(0.001)
  ROOT.gStyle.SetPadTickX(1)
  ROOT.gStyle.SetPadTickY(1)

  canv = ROOT.TCanvas("Limit_"+model,"Limit_"+model,800,600)
  pad=canv.GetPad(0)
  pad.SetBottomMargin(.12)
  pad.SetLeftMargin(.12)
  pad.SetLogy()
  """
  grtheory.GetYaxis().SetLabelSize(0.05)
  grtheory.GetYaxis().SetTitleSize(0.05)
  grtheory.GetYaxis().SetTitleOffset(1.20)
  grtheory.GetXaxis().SetLabelSize(0.05)
  grtheory.GetXaxis().SetTitleSize(0.05)
  grtheory.GetXaxis().SetTitleOffset(1.12)
  grtheory.GetXaxis().SetNdivisions(506)
  grtheory.GetXaxis().SetLabelFont(42)
  grtheory.GetYaxis().SetLabelFont(42)
  grtheory.GetXaxis().SetTitleFont(42)
  grtheory.GetYaxis().SetTitleFont(42)
  grtheory.GetXaxis().SetNdivisions(510,1);
  grtheory.GetXaxis().SetTitle("m_{X} [GeV]")
  grtheory.GetYaxis().SetTitle("#sigma(pp #rightarrow X) #it{B} (X #rightarrow HH #rightarrow b#bar{b}#gamma#gamma) [fb]")

  grtheory .SetLineColor(2)
  grtheory .SetLineWidth(2)
  grtheory .SetLineStyle(1)

  grtheory1.SetLineColor(2)
  grtheory1.SetLineWidth(2)
  grtheory1.SetLineStyle(2)
  """
  grexp2sig.SetFillColor(800)
  grexp2sig.SetLineColor(800)
  grexp1sig.SetFillColor(417)
  grexp1sig.SetLineColor(417)
  grexplim .SetLineWidth(2)
  grexplim .SetLineStyle(7)
 # grobslim .SetLineWidth(2)

  grexplim .SetMarkerStyle(0)
  #grobslim .SetMarkerStyle(20)

  grexplim .SetMarkerStyle(0)
  #grobslim .SetMarkerStyle(20)

 # grtheory .Draw("al")
  grexp2sig.Draw("3")
  grexp1sig.Draw("3")
  grexplim .Draw("l")
  #grobslim .Draw("l")
  #grtheory .Draw("l")
  #grtheory1.Draw("l")

  #grtheory.GetXaxis().SetRangeUser(250,1000)
  """
  grtheory.SetMinimum(0.1)
  grtheory.SetMaximum(20000)
  if model == 'BulkGrav':
    grtheory.SetMinimum(0.1)
    grtheory.SetMaximum(20000)
  elif model == 'Radion':
    grtheory.SetMinimum(0.1)
    grtheory.SetMaximum(20000)
  """
  text = ["CMS"]
  textsize = 0.045; 
  ntxt = 0
  nleglines = 5.

  xstart = 0.35;
  ystart = 0.55; 
  ystartleg = 0.95 

  theoryline = ""
  legend = ROOT.TLegend(xstart, ystart, xstart+0.45, ystartleg)
  legend.SetFillColor(0)
  legend.SetBorderSize(0)
  legend.SetTextSize(textsize)
  legend.SetTextFont(42)
  legend.SetColumnSeparation(0.0)
  legend.SetEntrySeparation(0.1)
  legend.SetMargin(0.2)
  legend.SetHeader("")
  """
  if model == 'BulkGrav':
    theoryline = "Bulk KK graviton (#kappa/#bar{M_{Pl}} = %2.1f)" % kMpl
  if model == 'Radion':
    theoryline = "Radion (#Lambda_{R} = %i TeV)" % Lambda
  legend.AddEntry(grtheory , theoryline,"l") 
  if model == 'BulkGrav':
    theoryline = "Bulk KK graviton (#kappa/#bar{M_{Pl}} = %2.1f)" % kMpl1
  if model == 'Radion':
    theoryline = "Radion (#Lambda_{R} = %i TeV)" % Lambda1
  legend.AddEntry(grtheory1, theoryline,"l") 
  legend.AddEntry(grobslim  , "Observed 95% upper limit","l")
  """
  legend.AddEntry(grexplim  , "Expected 95% upper limit","l")
  legend.AddEntry(grexp1sig , "Expected limit #pm 1 std. deviation","f")
  legend.AddEntry(grexp2sig , "Expected limit #pm 2 std. deviation","f")
  legend.Draw()

  ### Embellishment
  CMS_lumi.lumi_13TeV = ""
  CMS_lumi.writeExtraText = 1
  CMS_lumi.extraText = ""

  iPos = 11 ###HTshape
  if( iPos==0 ): CMS_lumi.relPosX = 0.12
  CMS_lumi.CMS_lumi(pad, 4, iPos)

  latex = ROOT.TLatex()
  latex.SetNDC()
  latex.SetTextAlign(13)
  latex.SetTextSize(0.04)
  latex.SetTextFont(42);
  latex.DrawLatex(0.69, 0.95, "136.8 fb^{-1} (13 TeV)")

  pad.RedrawAxis()

  pad.Update()
  ###

  for end in ["pdf","png", "root", ".C"]:
    canv.SaveAs("%s_Run2_13TeV_UL.%s" % (model, end))

  grexp2sig_hllhc.SetFillColor(800)
  grexp2sig_hllhc.SetLineColor(800)
  grexp1sig_hllhc.SetFillColor(417)
  grexp1sig_hllhc.SetLineColor(417)
  grexplim_hllhc .SetLineColor(ROOT.kBlue+2)
  grexplim_hllhc .SetLineWidth(2)
  grexplim_hllhc .SetLineStyle(1)

  canv_hllhc = ROOT.TCanvas("Limit_HLLHC_"+model,"Limit_HLLHC_"+model,800,600)
  canv_hllhc.cd()
  pad_hllhc=canv_hllhc.GetPad(0)
  pad_hllhc.SetBottomMargin(.12)
  pad_hllhc.SetLeftMargin(.12)
  pad_hllhc.SetLogy()
  pad_hllhc.cd()

  frame_hllhc = pad_hllhc.DrawFrame(250, 0.01, 1000, 20000, 'frame_hllhc')

  frame_hllhc.GetYaxis().SetLabelSize(0.05)
  frame_hllhc.GetYaxis().SetTitleSize(0.05)
  frame_hllhc.GetYaxis().SetTitleOffset(1.20)
  frame_hllhc.GetXaxis().SetLabelSize(0.05)
  frame_hllhc.GetXaxis().SetTitleSize(0.05)
  frame_hllhc.GetXaxis().SetTitleOffset(1.12)
  frame_hllhc.GetXaxis().SetNdivisions(506)
  frame_hllhc.GetXaxis().SetLabelFont(42)
  frame_hllhc.GetYaxis().SetLabelFont(42)
  frame_hllhc.GetXaxis().SetTitleFont(42)
  frame_hllhc.GetYaxis().SetTitleFont(42)
  frame_hllhc.GetXaxis().SetNdivisions(510,1);
  frame_hllhc.GetXaxis().SetTitle("m_{X} [GeV]")
  frame_hllhc.GetYaxis().SetTitle("#sigma(pp #rightarrow X) #it{B} (X #rightarrow HH #rightarrow b#bar{b}#gamma#gamma) [fb]")

  grexp2sig_hllhc.Draw("3")
  grexp1sig_hllhc.Draw("3")
  grexplim_hllhc .Draw("l")
  grexplim.Draw("l")
#  grtheory .Draw("l")
#  grtheory1.Draw("l")

  if model == "BulkGrav":
    gr_vbf = ROOT.TGraph(3)
    gr_vbf.SetPoint(0, 1500, 0.1748)
    gr_vbf.SetPoint(1, 2000, 0.1157)
    gr_vbf.SetPoint(2, 3000, 0.0493)
    gr_vbf.SetName("gr_vbf")
    gr_vbf.SetLineColor(49)
    gr_vbf.SetLineWidth(3)
    gr_vbf.SetFillColor(0)
    gr_vbf.Draw("l")

  xstart = 0.40;
  ystart = 0.55; 
  ystartleg = 0.95 

  textsize = 0.032; 

  legend_hllhc = ROOT.TLegend(xstart+0.05, ystart-0.1, xstart+0.50, ystartleg-0.1)
  legend_hllhc.SetFillColor(0)
  legend_hllhc.SetBorderSize(0)
  legend_hllhc.SetTextSize(textsize)
  legend_hllhc.SetTextFont(42)
  legend_hllhc.SetColumnSeparation(0.0)
  legend_hllhc.SetEntrySeparation(0.1)
  legend_hllhc.SetMargin(0.2)
  legend_hllhc.SetHeader("upper limits pp#rightarrowX#rightarrowHH#rightarrowb#bar{b}#gamma#gamma (Spin-0)")
  """
  if model == 'BulkGrav':
    theoryline = "Bulk KK graviton (#kappa/#bar{M_{Pl}} = %2.1f)" % kMpl
  if model == 'Radion':
    theoryline = "Radion (#Lambda_{R} = %i TeV)" % Lambda
  legend_hllhc.AddEntry(grtheory , theoryline,"l") 
  if model == 'BulkGrav':
    theoryline = "Bulk KK graviton (#kappa/#bar{M_{Pl}} = %2.1f)" % kMpl1
  if model == 'Radion':
    theoryline = "Radion (#Lambda_{R} = %i TeV)" % Lambda1
  legend_hllhc.AddEntry(grtheory1, theoryline,"l") 
  
  legend_hllhc.AddEntry(grexplim       , "2016 median expected","l")
  """
  legend_hllhc.AddEntry(grexplim_hllhc , "median expected","l")
  legend_hllhc.AddEntry(grexp1sig_hllhc, "68% expected","f")
  legend_hllhc.AddEntry(grexp2sig_hllhc, "95% expected","f")
  if model == "BulkGrav":
    legend_hllhc.AddEntry(gr_vbf, "HL-LHC median expected VBF", "l")
  legend_hllhc.Draw()

  ### Embellishment
  CMS_lumi.lumi_13TeV = ""
  CMS_lumi.writeExtraText = 1
  CMS_lumi.extraText = "Work in progress"

  iPos = 11 ###HTshape
  if( iPos==0 ): CMS_lumi.relPosX = 0.12
  CMS_lumi.CMS_lumi(pad_hllhc, 4, iPos)

  latex_hllhc = ROOT.TLatex()
  latex_hllhc.SetNDC()
  latex_hllhc.SetTextAlign(13)
  latex_hllhc.SetTextSize(0.04)
  latex_hllhc.SetTextFont(42);
  latex_hllhc.DrawLatex(0.69, 0.95, "136.8 fb^{-1} (13 TeV)")

  pad_hllhc.RedrawAxis()

  pad_hllhc.Update()
  ###

  for end in ["pdf","png", "root", ".C"]:
    canv_hllhc.SaveAs("Limit_Run2_13TeV_%s.%s" % (model, end))

masses = [260,270,280,300,350,400,450,500,550,600,650,700,800,900,1000]
models = ['Radion', ]
for model in models: 
  plotLimits(model, masses)
