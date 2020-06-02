from ROOT import *

def SetAxisTextSizes(obj, yoff=0, ysize=1, xoff=0, xsize=1):
  obj.GetYaxis().SetTitleOffset(1.1+yoff)
  obj.GetYaxis().SetTitleSize(0.0425*ysize)
  obj.GetYaxis().SetLabelSize(0.04*ysize)
  obj.GetXaxis().SetTitleOffset(1.1+xoff)
  obj.GetXaxis().SetTitleSize(0.0425*xsize)
  obj.GetXaxis().SetLabelSize(0.04*xsize)
  try:
    obj.GetZaxis().SetTitleOffset(1.1)
    obj.GetZaxis().SetTitleSize(0.0425)
    obj.GetZaxis().SetLabelSize(0.04)
  except AttributeError:
    a=1

def SetGeneralStyle():
  gStyle.SetFrameLineWidth(2)


def DefineLabels():

  tlatex = TLatex()
  tlatex.SetNDC()
  tlatex.SetTextAngle(0)
  tlatex.SetTextColor(kBlack)
  tlatex.SetTextFont(63)
  tlatex.SetTextAlign(11)
  tlatex.SetTextSize(25)

  tlatex.SetTextFont(53)

  tlatex.SetTextFont(43)
  tlatex.SetTextSize(20)
  tlatex.SetTextAlign(31)

  tlatex.SetTextAlign(11)
  tlatex.SetTextSize(25)
  return tlatex


def SetPadStyle(obj):
  obj.SetTicky()
  obj.SetTickx()

def DrawCMSLabels(obj, lumi, sim = 0):
  pad = obj.cd()
  l = pad.GetLeftMargin()
  t = pad.GetTopMargin()
  r = pad.GetRightMargin()
  b = pad.GetBottomMargin()
  lat = TLatex()
  lat.SetTextSize(0.045)
  lat.SetTextAlign(11)
  lat.SetTextFont(62)
  cmsTag = "CMS"
  lumiTag = lumi+' fb^{-1} (13 TeV)'
  if sim==1:
    cmsTag = "#bf{CMS} #it{Simulation}"
    lumiTag = lumi
  lat.DrawLatexNDC(l+0.01, 1-t+0.02, cmsTag)

  lat.SetTextFont(42)
  lat.SetTextAlign(31)
  lat.DrawLatexNDC(1-r-0.001, 1-t+0.02, lumiTag)


def DrawCatLabels(obj, cat):
  pad = obj.cd()
  lat = TLatex()
  lat.SetNDC()
  lat.SetTextAlign(11)
  lat.SetTextSize(25)

  topy = 0.91
  stepy = 0.08

  labelPrel =   "#it{Work ongoing}"
  label =   "#bf{pp#rightarrowX#rightarrowHH#rightarrow#gamma#gammab#bar{b}}"

  lat.SetTextFont(43)
#  lat.DrawLatex(0.14, topy-stepy*2, label)
#  print labelPrel
#  lat.SetTextFont(43)
  lat.DrawLatex(0.14, topy-stepy*1, labelPrel)
  lat.DrawLatex(0.14, topy-stepy*2, label)
  lat.DrawLatex(0.14, topy-stepy*3, cat)


