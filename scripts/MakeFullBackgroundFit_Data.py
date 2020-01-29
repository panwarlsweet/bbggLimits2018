from ROOT import *
from HiggsAnalysis.bbggLimits2018.MyCMSStyle import *
import argparse, sys
import numpy as n

def MakeFullBackgroundPdf(bkg_pdf, bkg_norm, hig_pdfs, hig_norms):
  if len(hig_pdfs) == 0: 
    print 'No HIG background found'
    return bkg_pdf
  argPdfs = RooArgList()
  argNorms = RooArgList()
  argPdfs.add(bkg_pdf)
  argNorms.add(bkg_norm)
  if len(hig_pdfs) != len(hig_norms):
    print "list of higgs pdfs has different size wrt normalizations!"
    return None
  for hh in range(0, len(hig_pdfs)):
#    hig_pdfs[hh].Print()
    argPdfs.add(hig_pdfs[hh])
    argNorms.add(hig_norms[hh])

  argNorms.Print()
  argPdfs.Print()

  if argNorms.getSize() != argPdfs.getSize():
    print 'ArgNorms and ArgPdfs have different sizes!'
    return None
  totPdf = RooAddPdf('totBkg', 'Nonresonant + single H background', argPdfs, argNorms)
  return totPdf


def MakeFullModelPdf(sig_pdf, sig_norm, totBkg_pdf, totBkg_norm):

  argPdfs = RooArgList()
  argNorms = RooArgList()
  argPdfs.add(totBkg_pdf)
  argPdfs.add(sig_pdf)
  argNorms.add(totBkg_norm)
  argNorms.add(sig_norm)

  totModPdf = RooAddPdf('totModPdf', 'Signal + Nonresonant background + single H background', argPdfs, argNorms)
  return totModPdf



gSystem.Load("libHiggsAnalysisCombinedLimit.so")
gROOT.SetBatch(kTRUE)

parser =  argparse.ArgumentParser(description='Background fit plot maker')
parser.add_argument('-i', '--inputFile', dest="dname", type=str, default=None, required=True)
parser.add_argument('-d', '--dataFile', dest="dataname", type=str, default=None, required=True)
parser.add_argument('-o', '--outName', dest="outName", type=str, default=None, required=True)
parser.add_argument('-c', '--cat', dest="category", type=int, default=None, required=True)
parser.add_argument('-L', '--lumi', dest='lumi', type=str, default='3000')
parser.add_argument('-Sf', '--signalFactor', dest='fsignal', type=float, default=[10.0,10.0], nargs='+')
parser.add_argument('-u', '--unblind', dest='unblind', default=False, action='store_true')
parser.add_argument('-n', '--ndims', dest='ndims', type=int, default=2)

opt = parser.parse_args()


Higgses = ['ggh', 'vbf', 'tth', 'vh', 'bbh']

dims = ['mgg', 'mjj']

if opt.ndims == 1:
  dims = ['mgg']

bin = [40, 20]
minval = [100, 94]
maxval = [180, 190]

hig_pdfs = []
hig_norms = []
totHiggs = 0

xtitle = ['m_{#gamma#gamma} [GeV]', 'm_{jj} [GeV]']
ytitle = ['Events/(2 GeV)', 'Events/(5 GeV)']
Cats = ["HP, 560 GeV < M_{X}", "HP, 478 < M_{X} < 560 GeV",  "HP, 354 < M_{X} < 478 GeV",  "HP, 250 < M_{X} < 354 GeV", "MP, 560 GeV < M_{X}", "MP, 478 < M_{X} < 560 GeV",  "MP, 354 < M_{X} < 478 GeV",  "MP, 250 < M_{X} < 354 GeV", "LP, 560 GeV < M_{X}", "LP, 478 < M_{X} < 560 GeV",  "LP, 354 < M_{X} < 478 GeV",  "LP, 250 < M_{X} < 354 GeV"]


tfile = TFile(opt.dname, "READ")

print "============================== Datafile name ", opt.dataname
datafile = TFile(opt.dataname, "READ")
w_all = tfile.Get("w")


icat = opt.category


for iobs,obs in enumerate(dims):

  var = w_all.var(obs)
  var.Print()

#  sig_pdf_name = obs+'Sig_cat'+str(icat)+'_CMS_sig_cat'+str(icat)
#  sig_pdf = w_all.pdf(sig_pdf_name)
#  sig_normName = 'n_exp_binch'+str(icat+1)+'_proc_Sig'
#  sig_norm = RooRealVar('sig_norm','signal norm', opt.fsignal[iobs]*w_all.obj(sig_normName).getVal())

#  print sig_pdf_name
#  sig_pdf.Print()
#  print "@@@ sig_norm: %.1f including SF: %.1f" % (sig_norm.getVal(), opt.fsignal[iobs])


 # model = MakeFullModelPdf(sig_pdf, sig_norm, totBkg_pdf, totBkg_norm)
 # totModel_norm =  RooRealVar("totModel_norm", "Total normalisation including signal", totBkg_norm.getVal()+sig_norm.getVal())


  w_data = datafile.Get("w_all")
#  w_data.Print()
  ddata="data_obs_cat"+str(icat)
  data2d = w_data.data(ddata)
#  data2d = tfile.Get("toys/toy_asimov;1")
#  data2d.Print()
  
  print "============================== totData = ",   data2d.sumEntries()


  data = data2d.reduce(RooFit.CutRange('catcut'))

  data.Print()



#  w_all.Print()
  bkg_pdf_name = "CMS_bkg_"+obs+"_cat"+str(icat)+"_bern1"

  bkg_pdf = w_all.pdf(bkg_pdf_name)
  if not bkg_pdf:
     bkg_pdf_name = "CMS_bkg_"+obs+"_cat"+str(icat)+"_bern2"
     bkg_pdf = w_all.pdf(bkg_pdf_name)
     if not bkg_pdf:
       bkg_pdf_name = "CMS_bkg_"+obs+"_cat"+str(icat)+"_bern3"
       bkg_pdf = w_all.pdf(bkg_pdf_name)

  bkg_normName = 'n_exp_final_bincat'+str(icat)+'_proc_Bkg'
  bkg_norm = RooRealVar('bkg_norm', 'nonres bkg norm', w_all.obj(bkg_normName).getVal())

  print bkg_pdf_name 
  bkg_pdf.Print()

  nBkgParams = bkg_pdf.getParameters(data).getSize()
  print "Number of background parameters:", nBkgParams
  bkg_pdf.getParameters(data).Print("v")
  print "Normalisation ", w_all.obj(bkg_normName).getVal() 

  par_name= obs+"_p0amp_cat"+str(icat)+"_CMS_Bkg_cat"+str(icat)
  p0amp =  w_data.function(par_name)

  func_name="bern_1par_cat"+str(icat)
  ext_func_name="ext_bern_1par_cat"+str(icat)

  bkg_pdf_1par = RooBernstein(func_name,"",var,RooArgList(p0amp));
  ext_bkg_pdf_1par  = RooExtendPdf(ext_func_name, "",  bkg_pdf_1par, bkg_norm);

#  print "name of the parameter = ", par_name
#  p0amp.Print("v") 

  for hh in Higgses:
    hig_pdf_name = obs+'Hig_'+hh+'_cat'+str(icat)+'_CMS_hig_'+hh+'_cat'+str(icat)
    
    if opt.ndims == 1:
      hig_pdf_name = 'shapeBkg_' + hh + '_cat'+str(icat)

    hig_pdf = w_all.pdf(hig_pdf_name)
    hig_pdfs.append(hig_pdf)

    hig_normName = 'n_exp_bincat'+str(icat)+'_proc_'+hh
    print hig_normName
    hig_norm = RooRealVar(hh+'_norm', hh+' bkg norm', w_all.obj(hig_normName).getVal() )
    hig_norms.append(hig_norm)
    print hig_pdf_name, " ", hig_norm.getVal()
    totHiggs += w_all.obj(hig_normName).getVal()

  totBkg_pdf = MakeFullBackgroundPdf(bkg_pdf, bkg_norm, hig_pdfs, hig_norms)
  totBkg_norm =  RooRealVar("totBkg_norm", "Normaisation of the total background",totHiggs + bkg_norm.getVal())

  print "============================== totBkgNorm = ",  totBkg_norm.getVal()





  binning = bin[iobs]
  cNiceBlueDark = TColor.GetColor('#2175E0')
  cNiceGreenDark = TColor.GetColor('#008040')
  cNiceRed = TColor.GetColor('#FA4912')

  ymax =  bkg_norm.getVal()/bin[iobs]*5

  print obs, " ymax = ", ymax

#  pdfout = opt.outName+"/Cat"+ str(icat) + "_" + obs+".pdf"
#  pngout = opt.outName+"/Cat"+str(icat) + "_" + obs+".png"
  poiss_pdfout = opt.outName+"/Cat"+str(icat) + "_" + obs+"_data.pdf"
  poiss_pngout = opt.outName+"/Cat"+str(icat) + "_"+obs+"_data.png"



  frame = var.frame(RooFit.Title(" "),RooFit.Bins(binning),RooFit.Range(minval[iobs],maxval[iobs]))
  dataind = 0
  if not opt.unblind:
    dataind = 2
    blindedRegions = {}
    blindedRegions['mgg'] = [100, 120, 130, 180]
    blindedRegions['mjj'] = [70, 100, 140, 190]
#    var.removeRange("unblindReg_1")
#    var.removeRange("unblindReg_2")
    var.setRange("unblindReg_1",blindedRegions[var.GetName()][0],blindedRegions[var.GetName()][1])
    var.setRange("unblindReg_2",blindedRegions[var.GetName()][2],blindedRegions[var.GetName()][3])
    data.plotOn(frame,RooFit.DataError(RooAbsData.SumW2),RooFit.XErrorSize(0), RooFit.CutRange("unblindReg_1"))
    data.plotOn(frame,RooFit.DataError(RooAbsData.SumW2),RooFit.XErrorSize(0), RooFit.CutRange("unblindReg_2"))
    data.plotOn(frame,RooFit.DataError(RooAbsData.SumW2),RooFit.XErrorSize(0), RooFit.Invisible())
    var.removeRange("unblindReg_1")
    var.removeRange("unblindReg_2")
  else:
#    data.plotOn(frame,RooFit.DataError(RooAbsData.Poisson),RooFit.XErrorSize(0))
    data.plotOn(frame,RooFit.DataError(RooAbsData.SumW2),RooFit.XErrorSize(0))
    

#  ext_bkg_pdf_1par.plotOn(frame,RooFit.LineColor(cNiceRed), RooFit.LineStyle(kDashed), RooFit.Precision(1E-5), RooFit.Normalization(bkg_norm.getVal(), RooAbsReal.NumEvent))
  bkg_pdf.plotOn(frame,RooFit.LineColor(cNiceGreenDark), RooFit.LineStyle(kDashed), RooFit.Precision(1E-5), RooFit.Normalization(bkg_norm.getVal(), RooAbsReal.NumEvent))
  totBkg_pdf.plotOn(frame,RooFit.LineColor(cNiceBlueDark),RooFit.Precision(1E-5), RooFit.Normalization(totBkg_norm.getVal(), RooAbsReal.NumEvent))

#  model.plotOn(frame,RooFit.LineColor(cNiceRed), RooFit.Precision(1E-5), RooFit.Normalization(totModel_norm.getVal(),RooAbsReal.NumEvent))

  datahist = frame.getObject(0)
  bkghist = frame.getObject(dataind+1)
  totbkgh = frame.getObject(dataind+2)
#  modelhist = frame.getObject(dataind+3)
  ##sigh = frame.getObject(dataind+4)


  leg = TLegend(0.45, 0.55, 0.89, 0.89)
  leg.SetBorderSize(0)
  leg.SetFillStyle(0)
  leg.SetTextFont(43)
  leg.SetTextSize(28)
#  leg.SetNColumns(3)
  leg.AddEntry(datahist, 'Data', 'pe')
  leg.AddEntry(bkghist, 'Nonresonant backgr.', 'l')
  leg.AddEntry(totbkgh, 'Full backgr.', 'l')
#  leg.AddEntry(modelhist, 'Sig. + Full backgr.', 'l')






  SetGeneralStyle()
  c = TCanvas("c", "c", 800, 600)
  frame.Draw()
  frame.GetXaxis().SetTitle(xtitle[iobs])
  frame.GetYaxis().SetTitle(ytitle[iobs])
  frame.SetMaximum(ymax)
  frame.SetMinimum(0.001)
  leg.Draw('same')
  SetPadStyle(c)
  SetAxisTextSizes(frame)
  DrawCMSLabels(c, opt.lumi)
  DrawCatLabels(c, Cats[icat])
  c.Update()


  if opt.unblind:
    print " ============= Making Data scaling ================== "

    N = datahist.GetN()
    alpha = 1 - 0.6827
    x=n.zeros(1, dtype=float)
    y=n.zeros(1, dtype=float)


    for i in range(0,N):

      datahist.GetPoint(i, x, y)   

      if y == 0 :
        L = 0
      else : 
        L = Math.gamma_quantile(alpha/2,y,1.)

      U =  Math.gamma_quantile_c(alpha/2,y+1,1) 

      yl = y-L
      yh = U-y
   
      datahist.SetPointEYlow(i, yl)
      datahist.SetPointEYhigh(i, yh)

      print "x = ", x," y = ",y, " yl ", yl, " yh ", yh




  c.SaveAs(poiss_pdfout)
  c.SaveAs(poiss_pngout)



