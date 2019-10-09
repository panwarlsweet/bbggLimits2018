#define bbggLTMaker_cxx

#include "bbggLTMaker.h"

const bool DEBUG = 0;


//// upating the categrisation number according to this part of 2017 analysis code https://github.com/michelif/flashgg/blob/hh_tag_94X_20180601/Taggers/python/flashggDoubleHTag_cfi.py#L31-L34
const Float_t boundary_MVA_2017[4]   = {0.29, 0.441, 0.724, 1.0}; // category boundaries for MVA


void bbggLTMaker::Begin(TTree * /*tree*/)
{
  TString option = GetOption();

  cout<<"Options are: \n \t "<<option.Data()<<endl;
  TObjArray *args = (TObjArray*)option.Tokenize(" ");
  _normalization = std::stod((string)((TObjString*)args->At(0))->GetString());
  _outFileName = (string)((TObjString*)args->At(1))->GetString();
  _genDiPhotonFilter = (Bool_t) std::stoi( (string)((TObjString*)args->At(2))->GetString() );
  _whichCategorization = (Int_t) std::stoi( (string)((TObjString*)args->At(3))->GetString() );
  _ttHTagger = (Bool_t) std::stoi( (string)((TObjString*)args->At(4))->GetString() );
  _MX_cut1 = std::stod( (string)((TObjString*)args->At(5))->GetString() );
  _MX_cut2 = std::stod( (string)((TObjString*)args->At(6))->GetString() );
  _signal = (string)((TObjString*)args->At(7))->GetString();
  _mass = (string)((TObjString*)args->At(8))->GetString();
  std::cout<<"Input paremeters:\n"
	   <<"_normalization: "<<_normalization<<"\n"
	   <<"_outFileName: "<< _outFileName<<"\n"
	   <<"_genDiPhotonFilter: "<< _genDiPhotonFilter<<"\n"
           <<"_ttHTagger: "<< _ttHTagger<<"\n"
           <<"_MX_cut1: "<< _MX_cut1 <<"\n"
           <<"_MX_cut2: "<< _MX_cut2 <<"\n"
           <<"_signal: "<< _signal <<"\n"
           <<"_mass: "<< _mass <<"\n"
	   <<std::endl;

  // Could make those come from external options as well:
  _phoVariation = 0;
  _trigVariation = 0;

  _outFile = new TFile(_outFileName, "RECREATE");
  _outTree = new TTree("LT", "A tree for studying new particles");

  _outTree->Branch("run", &o_run, "o_run/i");
  _outTree->Branch("evt", &o_evt, "o_evt/l");

  _outTree->Branch("evWeight", &o_weight, "o_weight/D");
  _outTree->Branch("mgg", &o_mgg, "o_mgg/D");
  _outTree->Branch("mjj", &o_mjj, "o_mjj/D");
  _outTree->Branch("MX",  &o_MX,  "o_MX/D");
  _outTree->Branch("mbbgg", &o_bbggMass, "o_bbggMass/D");
  _outTree->Branch("catID", &o_catID, "o_catID/I");
  _outTree->Branch("ttHTagger", &o_ttHTagger, "ttHTagger/D");


  TString phoSFID_file = TString(std::getenv("CMSSW_BASE")) + TString("/src/HiggsAnalysis/bbggLimits2018/Weights/MVAID/egammaEffi.txt_EGM2D.root");
  if (DEBUG) cout << "phoSFsID file: " << phoSFID_file << endl;
  TString phoSFeveto_file = TString(std::getenv("CMSSW_BASE")) + TString("/src/HiggsAnalysis/bbggLimits2018/Weights/MVAID/ScalingFactors_80X_Summer16.root");
  if (DEBUG) cout << "phoSFsEV file: " << phoSFeveto_file << endl;
  bbggLTMaker::SetupPhotonSF( phoSFID_file, phoSFeveto_file);

  TString trig_file = TString(std::getenv("CMSSW_BASE")) + TString("/src/HiggsAnalysis/bbggLimits2018/Weights/TriggerSF/TriggerSFs.root");
  if (DEBUG) cout << "TriggSF file: " << trig_file << endl;
  bbggLTMaker::SetupTriggerSF(trig_file);

}

void bbggLTMaker::SlaveBegin(TTree * /*tree*/)
{
  TString option = GetOption();
}

Bool_t bbggLTMaker::Process(Long64_t entry)
{
  GetEntry(entry);
  o_run = run;
  o_evt = event;

  o_weight = weight*_normalization;
  //o_weight = 1;
  o_mgg = CMS_hgg_mass;
  o_mjj = Mjj;
  o_bbggMass = diHiggs_mass;

  o_MX = MX;

  o_catID = -1;

  if(_ttHTagger)
    o_ttHTagger = ttHScore;
  else     
    o_ttHTagger = -1;

//// using categrisation 2 for 2017 ///////

  if (_whichCategorization==2 || _whichCategorization==3){
    if (o_MX >= _MX_cut1 && o_MX <= _MX_cut2){
      if (HHbbggMVA > boundary_MVA_2017[0] && HHbbggMVA <= boundary_MVA_2017[1]){
	o_catID = 2;
      }
      else if (HHbbggMVA > boundary_MVA_2017[1] && HHbbggMVA <= boundary_MVA_2017[2]){
	o_catID = 1;
      }
      else if (HHbbggMVA > boundary_MVA_2017[2] && HHbbggMVA <= boundary_MVA_2017[3]){
        o_catID = 0;
      }
      
    }
   
  const Double_t preweight = 1*_normalization;
  if( preweight == 1) o_weight = 1; // When preweight == 1 it's the data, no SF needed.
 
  }
  _outTree->Fill();

  return kTRUE;
}

void bbggLTMaker::SlaveTerminate()
{
}

void bbggLTMaker::Terminate()
{
  _outFile->Write();
  _outFile->Close();
}


void bbggLTMaker::SetupPhotonSF(TString idfile, TString evfile)
{
  photonidFile = new TFile(idfile, "READ");
  photonIDhist = (TH2F*) photonidFile->Get("EGamma_SF2D;1");
  csevFile = new TFile(evfile, "READ");
  csevhist = (TH2F*) csevFile->Get("Scaling_Factors_CSEV_R9 Inclusive");
}


float bbggLTMaker::PhotonSF(bbggLTMaker::LorentzVector pho, int phovar)
{
  float sf_id = -99, sf_ev = -99, sf_id_err = -99, sf_ev_err = -99;
  sf_id_err = photonIDhist->GetBinError( photonIDhist->FindBin(pho.eta(), pho.pt()) );
  sf_id = photonIDhist->GetBinContent( photonIDhist->FindBin(pho.eta(), pho.pt()) ) + phovar*sf_id_err;
  sf_ev_err = csevhist->GetBinContent( csevhist->FindBin(pho.eta(), pho.pt()) );
  if(sf_ev_err==1) sf_ev_err=0;
  sf_ev = csevhist->GetBinContent( csevhist->FindBin(fabs(pho.eta()), pho.pt()) ) + phovar*sf_ev_err;
  float totSF = sf_id*sf_ev;
  if (totSF < 1E-1) return 1;
  else return totSF;
}

void bbggLTMaker::SetupTriggerSF(TString sfFile)
{
  triggerFile = new TFile(sfFile, "READ");
  ltriggerHist = (TH3F*) triggerFile->Get("leadingPhotonTSF");
  striggerHist = (TH3F*) triggerFile->Get("subleadingPhotonTSF");
}

float bbggLTMaker::TriggerSF(LorentzVector lpho, float lr9, LorentzVector spho, float sr9, int var)
{
   int leadingBin = ltriggerHist->FindBin(lr9, fabs(lpho.Eta()), lpho.Pt());
   int subleadingBin = striggerHist->FindBin(sr9, fabs(spho.Eta()), spho.Pt());
   if(DEBUG) cout << "[bbggLTMaker::TriggerSF] leading Bin: " << leadingBin << " subleadingBin " << subleadingBin << std::endl;

   float leadingSF = ltriggerHist->GetBinContent(leadingBin);
   float sleadingSF =striggerHist->GetBinContent(subleadingBin);
   if(DEBUG) cout << "[bbggLTMaker::TriggerSF] leading SF: " << leadingSF << " subleadingSF " << sleadingSF << std::endl;

   float leadingErr = ltriggerHist->GetBinError(leadingBin);
   float subleadingErr = striggerHist->GetBinError(subleadingBin);
   if(DEBUG) cout << "[bbggLTMaker::TriggerSF] leading SFerr: " << leadingErr << " subleadingSFerr " << subleadingErr << std::endl;

   return (leadingSF + var*leadingErr)*(sleadingSF + var*subleadingErr);
}
