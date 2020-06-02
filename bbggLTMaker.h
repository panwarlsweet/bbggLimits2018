#ifndef bbggLTMaker_h
#define bbggLTMaker_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TSelector.h>
#include "TH2F.h"
#include "TH3F.h"

// Header file for the classes stored in the TTree if any.
#include "vector"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PxPyPzE4D.h"
#include "vector"
#include "map"

class bbggLTMaker : public TSelector {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain


   // Output tree and variables:
   TString _outFileName;
   TFile *_outFile;
   TTree *_outTree;

   Double_t o_weight;
   Double_t o_mgg, o_mjj, o_bbggMass, o_MX, o_ttHTagger;
   Int_t o_catID;
   UInt_t o_run;
   ULong64_t o_evt;

   // Some external variables:
   Double_t _normalization;
   Bool_t _genDiPhotonFilter;
   Bool_t _ttHTagger;
   Int_t _whichCategorization;
   Double_t _MX_cut1;
   Double_t _MX_cut2;
   TString _mass;
   TString _signal;
   //Photon ID SF stuff
   TFile* photonidFile;
   TH2F* photonIDhist;
   TFile* csevFile;
   TH2F* csevhist;

   //Trigger stuff
   TFile* triggerFile;
   TH3F* ltriggerHist;
   TH3F* striggerHist;

   Int_t _phoVariation, _trigVariation;


   
   //Variables from the input tree:
   
   typedef ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double> > LorentzVector;
   Int_t           candidate_id;
   Float_t         weight;
   Int_t           isSignal;
   Double_t        genTotalWeight;
   Float_t         ttHScore;
   Float_t         CMS_hgg_mass;
   Float_t         dZ;
   Float_t         centralObjectWeight;
   Float_t         leadingJet_bDis;
   Float_t         subleadingJet_bDis;
   Float_t         absCosThetaStar_CS;
   Float_t         absCosTheta_bb;
   Float_t         absCosTheta_gg;
   Float_t         diphotonCandidatePtOverdiHiggsM;
   Float_t         dijetCandidatePtOverdiHiggsM;
   Float_t         customLeadingPhotonIDMVA;
   Float_t         customSubLeadingPhotonIDMVA;
   Float_t         leadingPhotonSigOverE;
   Float_t         subleadingPhotonSigOverE;
   Float_t         sigmaMOverM;
   Float_t         sigmaMOverMDecorr;
   Float_t         sigmaMJets;
   Float_t         PhoJetMinDr;
//   Float_t         HHbbggMVA;
   Double_t   	   HHbbggMVA;
  // Double_t        xmltransfMVA;	
   Float_t         MX;
   Float_t         Mjj;
   Float_t         dijet_pt;
   Float_t         dijet_eta;
   Float_t         dijet_phi;
   Float_t         diphoton_pt;
   Float_t         diphoton_eta;
   Float_t         diphoton_phi;
   Float_t         diHiggs_pt;
   Float_t         diHiggs_mass;
   Float_t         diHiggs_eta;
   Float_t         diHiggs_phi;
   Float_t         category;
   Float_t         leadingPhoton_pt;
   Float_t         leadingPhoton_eta;
   Float_t         leadingPhoton_phi;
   Float_t         subleadingPhoton_pt;
   Float_t         subleadingPhoton_eta;
   Float_t         subleadingPhoton_phi;
   Float_t         leadingJet_pt;
   Float_t         leadingJet_eta;
   Float_t         leadingJet_phi;
   Float_t         leadingJet_mass;
   Float_t         leadingJet_bRegNNCorr;
   Float_t         leadingJet_bRegNNResolution;
   Float_t         subleadingJet_pt;
   Float_t         subleadingJet_eta;
   Float_t         subleadingJet_phi;
   Float_t         subleadingJet_mass;
   Float_t         subleadingJet_bRegNNCorr;
   Float_t         subleadingJet_bRegNNResolution;
   Float_t         ttHMVA_MET;
   Float_t         ttHMVA_njets;
   Float_t         ttHMVA_Xtt0;
   Float_t         ttHMVA_Xtt1;
   Float_t         ttHMVA_MjjW0;
   Float_t         ttHMVA_MjjW1;
   Float_t         ttHMVA_Mjjbt0;
   Float_t         ttHMVA_Mjjbt1;
   Float_t         ttHMVA_leadingMuon;
   Float_t         ttHMVA_subleadingMuon;
   Float_t         ttHMVA_nmus;
   Float_t         ttHMVA_leadingElectron;
   Float_t         ttHMVA_subleadingElectron;
   Float_t         ttHMVA_nelecs;
   Float_t         ttHHHbggMVA;
   Float_t         rho;
   ULong64_t       event;
   UInt_t          lumi;
   Int_t           processIndex;
   UInt_t          run;
   Int_t           nvtx;
   Float_t         npu;
   Float_t         puweight;
   
   // List of branches
   //TBranch        *b_genWeights;   //!
   TBranch        *b_genTotalWeight;   //!
   //TBranch        *b_gen_mHH;   //!
   //TBranch        *b_cosTheta;   //!
      
   TBranch          *b_leadingJet_bDis;   //!
   TBranch         *b_subleadingJet_bDis;   //!

   TBranch        *b_dijetCandidate;

   TBranch        *b_isSignal;   //!

   TBranch        *b_HHbbggMVA;   //!
   TBranch        *b_HHTagger_LM;   //!
   TBranch        *b_HHTagger_HM;   //!

   TBranch        *b_MX;   //!
   TBranch        *b_ttHTagger;
   //TBranch        *b_nelecs;   //!
   //TBranch        *b_nelecs_loose;   //!
   //TBranch        *b_rho;   //!
   //TBranch        *b_nvtx;   //!
   TBranch        *b_event;   //!
   TBranch        *b_lumi;   //!
   //TBranch        *b_processIndex;   //!
   TBranch        *b_run;   //!
   TBranch        *b_Mjj;
   TBranch        *b_Mgg;
   TBranch        *b_mbbgg;
   TBranch        *b_evWeight;

   bbggLTMaker(TTree * /*tree*/ =0) : fChain(0) { }
   virtual ~bbggLTMaker() { }
   virtual Int_t   Version() const { return 2; }
   virtual void    Begin(TTree *tree);
   virtual void    SlaveBegin(TTree *tree);
   virtual void    Init(TTree *tree);
   virtual Bool_t  Notify();
   virtual Bool_t  Process(Long64_t entry);
   virtual Int_t   GetEntry(Long64_t entry, Int_t getall = 0) { return fChain ? fChain->GetTree()->GetEntry(entry, getall) : 0; }
   virtual void    SetOption(const char *option) { fOption = option; }
   virtual void    SetObject(TObject *obj) { fObject = obj; }
   virtual void    SetInputList(TList *input) { fInput = input; }
   virtual TList  *GetOutputList() const { return fOutput; }
   virtual void    SlaveTerminate();
   virtual void    Terminate();



   void SetupPhotonSF(TString idfile, TString evfile);
   float PhotonSF(LorentzVector pho, int phovar = 0);
   void SetupTriggerSF(TString trig_file);
   float TriggerSF(LorentzVector lpho, float lr9, LorentzVector spho, float sr9, int var);
   
   ClassDef(bbggLTMaker,0);
};

#endif

#ifdef bbggLTMaker_cxx
void bbggLTMaker::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
   //genWeights = 0;
   //leadingPhoton = 0;
   //subleadingPhoton = 0;
   //dijetCandidate = 0;
   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   //fChain->SetBranchAddress("leadingJet_DeepCSV", &leadingJet_DeepCSV, &b_leadingJet_bDis);
   //fChain->SetBranchAddress("subleadingJet_DeepCSV", &subleadingJet_DeepCSV, &b_subleadingJet_bDis);
   fChain->SetBranchAddress("MX", &MX, &b_MX);
   fChain->SetBranchAddress("event", &event, &b_event);
//   fChain->SetBranchAddress("HHbbggMVA", &HHbbggMVA, &b_HHbbggMVA);
   fChain->SetBranchAddress("xmlMVAtransf", &HHbbggMVA, &b_HHbbggMVA);  
   fChain->SetBranchAddress("run", &run, &b_run);
   fChain->SetBranchAddress("Mjj", &Mjj, &b_Mjj);
   fChain->SetBranchAddress("CMS_hgg_mass", &CMS_hgg_mass, &b_Mgg);
   fChain->SetBranchAddress("diHiggs_mass", &diHiggs_mass, &b_mbbgg);
   fChain->SetBranchAddress("weight", &weight, &b_evWeight);
   fChain->SetBranchAddress("ttHScore", &ttHScore, &b_ttHTagger);
}

Bool_t bbggLTMaker::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

#endif // #ifdef bbggLTMaker_cxx
