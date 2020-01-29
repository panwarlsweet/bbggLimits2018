from ROOT import *
from HiggsAnalysis.bbggLimits2018.MyCMSStyle import *
import math

#vmu = [1, 1, 1, 10, 10, 10, 10, 20, 20, 20, 20, 20]
vmu = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
#vmu = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

ltruths = ["Ber", "Exp", "Pow"]
dir='2016_2017_withPU_BerFast_2D_COMPROMISE_2/Node_SM/BIAS/'
#dir='2016_2017_withPU_BerFast_2D_FORBIAS_BER3All/Node_SM/BIAS/'
fbase = dir+'mlfit.catICAT.tTRUTH.fFUNC.musigMU0'
lcats = [0,1,2,3,4,5,6,7,8,9,10,11]
#lcats = [2,3,4,5,7,8,11]
#lcats = [0,1,2,3,4,5,6]
#lcats = [2,3]
iFunc=0



out = TFile('bias_out.root', 'RECREATE')
grs = []
c1 = TCanvas("c", "c", 800, 600)
c1.cd()

gStyle.SetOptFit(0111)

for truth in ltruths:
  gr = TGraphErrors()
  gr.SetName('gr_t'+truth+"_fBer")
  gr.SetTitle('Truth is '+truth+" fit by Ber")
#  gr.SetName('gr_t'+truth+"_fExp")
#  gr.SetTitle('Truth is '+truth+" fit by Exp")
  for icat in range(0, 11):
    gr.SetPoint(icat, float(icat), -1000)
    gr.SetPointError(icat, float(0), 1)

  for icat in lcats:
    tf = TFile(fbase.replace('ICAT', str(icat)).replace('TRUTH', truth).replace('MU0', str(vmu[icat])).replace('FUNC', ltruths[iFunc])+'.root')
    tt = tf.Get('tree_fit_sb')
    hname2 = 'hist_t'+truth+"_fBer_cat"+str(icat)+"_pm2"
    hist2 = TH1F(hname2, '', 60, -2, 2)
    tt.Draw('(mu-'+str(vmu[icat])+')/muErr>>'+hname2, 'numbadnll>-1 && fit_status == 0 && abs(mu) < 1000')
    fitres2 = hist2.Fit('gaus', 'S')

    # use directly the functionin ROOT::MATH note that the parameters definition is different is (alpha, n sigma, mu)
#    f1  = TF1("f1","[0]*ROOT::Math::crystalball_function(x, [1], [2], [3], [4])",-2,2);
#    f1.SetParameters(50, 1.5, 2, 1, 0)
#    fitres2 = hist2.Fit(f1, 'S')
#    mean2 = fitres2.GetParams()[1]
#    e_mean2 = fitres2.GetErrors()[1]

    mean2 = fitres2.GetParams()[1]
    e_mean2 = fitres2.GetErrors()[1]
    c1.Update()
    c1.SaveAs(fbase.replace('ICAT', str(icat)).replace('TRUTH', truth).replace('MU0', str(vmu[icat])).replace('FUNC', ltruths[iFunc])+'_2sigma.png')
    c1.SaveAs(fbase.replace('ICAT', str(icat)).replace('TRUTH', truth).replace('MU0', str(vmu[icat])).replace('FUNC', ltruths[iFunc])+'_2sigma.pdf')



#    hname2_do = 'hist_t'+truth+"_fBer_cat"+str(icat)+"_pm2_do"
#    hist2_do = TH1F(hname2_do, '', 60, -2, 2)
#    tt.Draw('(mu-'+str(vmu[icat])+')/muHiErr>>'+hname2_do, 'numbadnll>-1 && (mu-'+str(vmu[icat])+') < 0')
#    hname2_asym = 'hist_t'+truth+"_fBer_cat"+str(icat)+"_pm2_asym"
#    hist2_asym = TH1F(hname2_asym, '', 60, -2, 2)
#    tt.Draw('(mu-'+str(vmu[icat])+')/muLoErr>>'+hname2_asym, 'numbadnll>-1 && (mu-'+str(vmu[icat])+') > 0')
#    hist2_asym.Add(hist2_do)
#    mean2_asym =  hist2_asym.GetMean()
#    e_mean2_asym = hist2_asym.GetRMS()/math.sqrt(hist2_asym.Integral())
#    c1.Update()
#    c1.SaveAs(fbase.replace('ICAT', str(icat)).replace('TRUTH', truth).replace('MU0', str(vmu[icat])).replace('FUNC', ltruths[iFunc])+'_2sigma_asym.png')









    hname1p5 = 'hist_t'+truth+"_fBer_cat"+str(icat)+"_pm1p5"
    hist1p5 = TH1F(hname1p5, '', 60, -1.5, 1.5)
    tt.Draw('(mu-'+str(vmu[icat])+')/muErr>>'+hname1p5, 'numbadnll>-1 && fit_status == 0 && abs(mu) < 1000')
    fitres1p5 = hist1p5.Fit('gaus', 'S')
    mean1p5 = fitres1p5.GetParams()[1]
    e_mean1p5 = fitres1p5.GetErrors()[1]
    c1.SaveAs(fbase.replace('ICAT', str(icat)).replace('TRUTH', truth).replace('MU0', str(vmu[icat])).replace('FUNC', ltruths[iFunc])+'_1p5sigma.png')





    hname5 = 'hist_t'+truth+"_fBer_cat"+str(icat)+"_pm5"
    hist5 = TH1F(hname5, '', 120, -5, 5)
    tt.Draw('(mu-'+str(vmu[icat])+')/muErr>>'+hname5, 'numbadnll>-1 && fit_status == 0 && abs(mu) < 1000')
    fitres5 = hist5.Fit('gaus', 'S')

#    f1  = TF1("f1","[0]*ROOT::Math::crystalball_function(x, [1], [2], [3], [4])",-5,5);
#    f1.SetParameters(50, 1.5, 2, 1, 0)
#    fitres5 = hist2.Fit(f1, 'S')
#    mean5 = fitres2.GetParams()[4]
#    e_mean5 = fitres2.GetErrors()[4]

    mean5 = fitres5.GetParams()[1]
    e_mean5 = fitres5.GetErrors()[1]
    c1.Update()
    c1.SaveAs(fbase.replace('ICAT', str(icat)).replace('TRUTH', truth).replace('MU0', str(vmu[icat])).replace('FUNC', ltruths[iFunc])+'_5sigma.png')

    mymean = mean2
    myerr = e_mean2
    if abs(mean5) < abs(mean2):
      mymean = mean5
      myerr = e_mean5
    if abs(mean1p5) < abs(mymean):
      mymean = mean1p5
      myerr = e_mean1p5
#    if abs(mean2_asym) < abs(mymean):
#      mymean = mean2_asym
#      myerr = e_mean2_asym

    print icat, " for truth function ",truth, mymean, myerr



    gr.SetPoint(icat, float(icat), mymean)
    gr.SetPointError(icat, float(0), myerr)
  grs.append(gr)

out.cd()
c = TCanvas("c", "c", 800, 600)
leg = TLegend(0.55, 0.70, 0.85, 0.89)
leg.SetHeader("Fit by Bernstein polynomial from FTest")
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetTextFont(43)
leg.SetTextSize(20)



for igr,gr in enumerate(grs):
  if igr == 0: 
      gr.Draw("APE")
  else:
      gr.Draw("PE")

  leg.AddEntry(gr, gr.GetTitle(), 'pe')


  gr.GetXaxis().SetRangeUser(-0.5, 11.5)
  gr.GetXaxis().SetTitle("category")
  gr.GetYaxis().SetTitle("relative bias")
  gr.GetYaxis().SetRangeUser(-0.5, 0.5)
  gr.SetLineColor(igr+1)
  gr.SetMarkerColor(igr+1)
  gr.SetMarkerStyle(igr+20)
  gr.SetMarkerSize(2)
  gr.SetTitle("")
  if igr == 0: 
      gr.Draw("APE")


  gr.Write()



out.Close()

leg.Draw()
LUp = TLine(0, 0.2, 11.5, 0.2)
LDo = TLine(0, -0.2, 11.5, -0.2)
LUp.SetLineStyle(5)
LDo.SetLineStyle(5)

LUp1p4 = TLine(0, 0.14, 11.5, 0.14)
LDo1p4 = TLine(0, -0.14, 11.5, -0.14)
LUp1p4.SetLineStyle(7)
LDo1p4.SetLineStyle(7)
LUp1p4.SetLineColor(kBlue)
LDo1p4.SetLineColor(kBlue)

LUp.Draw()
LDo.Draw()
LUp1p4.Draw()
LDo1p4.Draw()

SetPadStyle(c)
DrawCMSLabels(c, '77.4')
#DrawCatLabels(c, '~1-3 #sigma sig. inj. / cat')
#DrawCatLabels(c, 'SM inj.')
DrawCatLabels(c, '1fb inj.')
c.Update()
print 'Saved into '+dir+"BiasStudies.png"
#c.SaveAs(dir+"BiasStudies_SM.png")
c.SaveAs(dir+"BiasStudies_1fb.png")
raw_input("Press Enter to continue...")
