#define hi_cxx
#include "hi.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TLorentzVector.h>
#include <vector>
#include <iostream>

bool TEST_MODE = false;

bool GenMatched(const TLorentzVector& genP, const TLorentzVector& recoP )
{
  double deltaR =genP.DeltaR(recoP);
  double deltaPt=fabs(genP.Pt() - recoP.Pt()) / genP.Pt();
  return (deltaR < 0.2) && (deltaPt < 1.0);
}
bool FailedOfficalGenMatching(hi* POOL)
{
    for ( int iJet = 0; iJet < POOL->nJet; ++iJet )
        if ( POOL->jetGenPartonID->at(iJet) > -99 )
            return false;
    return true;
}
int GenJetMulplicity_MatchToGenPho(hi* POOL, const TLorentzVector& mcPHO, int mcPHOidx)
{
    int matchJetNum = 0;
    int matchJetIdx = -1;
    // reversed looping, at the end it gets largest pt matching
    for ( int iJetPlus1 = POOL->nJet; iJetPlus1 > 0; --iJetPlus1)
    {
        // this looping will be skipped if _failed_offical_gen_matching_ checking failed.
      int iJet = iJetPlus1 - 1;
      if ( POOL->jetGenPartonID->at(iJet) < -90 ) continue;

      TLorentzVector genJet;
      genJet.SetPtEtaPhiE(
              POOL->jetGenJetPt ->at(iJet),
              POOL->jetGenJetEta->at(iJet),
              POOL->jetGenJetPhi->at(iJet),
              POOL->jetGenJetEn ->at(iJet)  );
      if ( genJet.DeltaR(mcPHO) < 0.5  &&
           genJet.DeltaR(mcPHO) < 0.15 )
        continue; // remove gen photon and gen jet overlapping event

      int jetMomID = POOL->jetGenPartonMomID->at(iJet);
      if ( POOL->mcMomPID->at(mcPHOidx) == POOL->jetGenPartonMomID->at(iJet) )
      { matchJetIdx = iJet; ++matchJetNum; }
    }
    return matchJetNum;
    // return matchJetIdx;
}
std::vector<int> GenJetIdxMatchedToGenPho(hi* POOL, const TLorentzVector& mcPHO, int mcPHOidx)
{
    std::vector<int> matchJetIdx;
    // reversed looping, at the end it gets largest pt matching
    for ( int iJet = 0; iJet < POOL->nJet; ++iJet )
    {
      if ( POOL->jetGenPartonID->at(iJet) < -90 ) continue;

      TLorentzVector genJet;
      genJet.SetPtEtaPhiE(
              POOL->jetGenJetPt ->at(iJet),
              POOL->jetGenJetEta->at(iJet),
              POOL->jetGenJetPhi->at(iJet),
              POOL->jetGenJetEn ->at(iJet)  );
      if ( genJet.DeltaR(mcPHO) < 0.5  &&
           genJet.DeltaR(mcPHO) < 0.15 )
        continue; // remove gen photon and gen jet overlapping event

      if ( POOL->mcMomPID->at(mcPHOidx) == POOL->jetGenPartonMomID->at(iJet) )
          matchJetIdx.push_back(iJet);
    }
    return matchJetIdx;
}
int Interpreter_GenJetMatchingMultiplicity(
        bool evtFAILEDofficalGENmatching, const std::vector<int>& idxLIST)
{
    /* -2 : this event failed offical gen jet matching
     *  0 ~ N : gen jet matching multiplicity to gen phton.
     *  */
    if ( evtFAILEDofficalGENmatching ) return -2;
    //if ( idxLIST.size() == 0 ) return -1;
    return idxLIST.size();
}
int Interpreter_GenJetIdx(
        bool evtFAILEDofficalGENmatching, const std::vector<int>& idxLIST)
{
    /* -2 : this event failed offical gen jet matching
     * -1 : all jets failed to match gen photon
     *  0 ~ N : gen jet matching multiplicity to gen phton.
     *  */
    if ( evtFAILEDofficalGENmatching ) return -2;
    if ( idxLIST.size() == 0 ) return -1;
    return idxLIST[0];
}
int IsLeadingJet(hi* POOL, const TLorentzVector& mcPHO, int matchedJETidx)
{
    /*
     * minus : follow meaning of matchedJETidx
     *  0 : is a secondary jet
     *  1 : is a leading jet
     */
    if ( matchedJETidx < 0 ) return matchedJETidx; // no matching. Follow code from matchedJETidx

    for ( int iJet = 0; iJet < matchedJETidx; ++iJet )
    {
      if ( POOL->jetGenPartonID->at(iJet) < -90 ) continue;

      TLorentzVector genJet;
      genJet.SetPtEtaPhiE(
              POOL->jetGenJetPt ->at(iJet),
              POOL->jetGenJetEta->at(iJet),
              POOL->jetGenJetPhi->at(iJet),
              POOL->jetGenJetEn ->at(iJet)  );
      if ( genJet.DeltaR(mcPHO) < 0.5  &&
           genJet.DeltaR(mcPHO) < 0.15 )
        continue; // remove gen photon and gen jet overlapping event
      return 0; // leading jet found, so the matchJETidx means secondary jet
    }
    return 1; // the matchJETidx means leading jet
}

TH1F* CreateStatusPlot(const char* name, int maxVAL )
{ return new TH1F(name, "", maxVAL+2, -2, maxVAL); }
void FillStatus(TH1F* h, int val)
{ h->Fill(val+0.001); }
void hi::Loop( const char* outputFILEname )
{
  if (fChain == 0)
    return;

  TH1F *hDeltaR = new TH1F("truthMatch_deltaR", "", 60, 0., 0.6);
  TH1F *hDeltaPt = new TH1F("truthMatch_deltaPt", "", 50, 0., 2.0);
  TH1F *hCutDeltaR = new TH1F("truthMatch_Cut_deltaR", "", 60, 0., 0.6);
  TH1F *hCutDeltaPt = new TH1F("truthMatch_Cut_deltaPt", "", 50, 0., 2.0);

  TH1F *hJetPhoDeltaR = new TH1F("truthJetPhoMatch_deltaR", "", 60, 0., 0.6);
  TH1F *hJetPhoDeltaPt = new TH1F("truthJetPhoMatch_deltaPt", "", 50, 0., 2.0);
  TH1F *hJetPhoCutDeltaR = new TH1F("truthJetPhoMatch_Cut_deltaR", "", 60, 0., 0.6);
  TH1F *hJetPhoCutDeltaPt = new TH1F("truthJetPhoMatch_Cut_deltaPt", "", 50, 0., 2.0);
  auto hSuperLeadingPt = new TH1F("superLeadingJetPt", "", 100, -100., 1000.);
  auto hSuperLeadingPtDiff = new TH1F("superLeadingJetPtDiff", "", 100, -100., 100.);



  // -2  : Failed offical gen-jet matching
  // -1  : No Jet matched to gen photon.
  // 0~N : jet index of the matching.
  // 9   : total event
  TH1F* hMatchJetIdxWithMomID = CreateStatusPlot("matchJetIdxWithMomID", 6);
  hMatchJetIdxWithMomID->GetXaxis()->SetTitle("max Pt jet index");

  // -2  : Failed offical gen-jet matching
  // 0~N : gen jet matching multiplicity to gen photon
  // 9   : total event
  TH1F* hNumMatchedJet_eachEvent = CreateStatusPlot("numMatchedJet_eachEvent", 10);
  hNumMatchedJet_eachEvent->GetXaxis()->SetTitle("GenJet Matching Multiplicity to GenPho");

  // -1 : Failed offical gen-jet matching
  //  0 : secondary jet
  //  1 : leading jet
  TH1F* hIsLeadingJet = CreateStatusPlot("isLeadingJet", 3);


  const std::vector<float> pt_definitions({190,200,220,250,300,350,400,500,750,1000});
  auto hGenCyield = new TH1F("genCyield", "", pt_definitions.size()-1, &(pt_definitions.front()));
  auto hGenLyield = new TH1F("genLyield", "", pt_definitions.size()-1, &(pt_definitions.front()));
  auto hGenByield = new TH1F("genByield", "", pt_definitions.size()-1, &(pt_definitions.front()));

  TH1F* checkerplot = new TH1F("checkerplot", "PID before leading jet", 125, -100, 25);


  Long64_t nentries = TEST_MODE ? 20 : fChain->GetEntriesFast();

  Long64_t nbytes = 0, nb = 0;
  for (Long64_t jentry = 0; jentry < nentries; jentry++)
  {
    Long64_t ientry = LoadTree(jentry);
    if (ientry < 0) break;
    nb = fChain->GetEntry(jentry);

    if (nPho == 0) continue; // skip if no reco photon in event
    if (nJet == 0) continue; // skip if no reco jet in event

    int mcPhoIdx = -1;
    for (int iMC = 0; iMC < nMC; ++iMC)
    {
      if (mcPt->at(iMC) < 15. ) continue;
      if (mcPID->at(iMC) != 22) continue;
      if (mcStatusFlag->at(iMC) != 3) continue;
      if (mcStatus->at(iMC) != 1) continue;
      mcPhoIdx = iMC;
      break; // find first photon candidate
    }
    if (mcPhoIdx < 0) continue; // skip if no gen photon in event

    TLorentzVector mcPho;
    mcPho.SetPtEtaPhiM(mcPt->at(mcPhoIdx), mcEta->at(mcPhoIdx), mcPhi->at(mcPhoIdx), mcMass->at(mcPhoIdx));
    TLorentzVector recoPho;
    recoPho.SetPtEtaPhiM(phoEt->at(0), phoEta->at(0), phoPhi->at(0), 0.); // choose leading photon


    // fill gen matching variables
    double deltaR =mcPho.DeltaR(recoPho);
    double deltaPt=fabs(mcPho.Pt() - recoPho.Pt()) / mcPho.Pt();

    hDeltaR->Fill(deltaR)  ; if ( deltaPt < 1.0 ) hCutDeltaR->Fill(deltaR);
    hDeltaPt->Fill(deltaPt); if (deltaR < 0.2 )   hCutDeltaPt->Fill(deltaPt);
    // fill gen matching variables end



    if (!GenMatched(mcPho, recoPho) ) continue; // skip if gen photon and leading photon mismatched.
    // fill genjet genpho matching variables
    for ( int iJet = 0; iJet < nJet; ++iJet )
    {
        if ( jetGenJetEn->at(iJet) < 0. ) break;

        TLorentzVector genJet;
        genJet.SetPtEtaPhiE(jetGenJetPt->at(iJet), jetGenJetEta->at(iJet), jetGenJetPhi->at(iJet), jetGenJetEn->at(iJet));

        double deltaR =mcPho.DeltaR(genJet);
        double deltaPt=fabs(mcPho.Pt() - genJet.Pt()) / mcPho.Pt();

        hJetPhoDeltaR->Fill(deltaR)  ; if ( deltaPt < 0.5 ) hJetPhoCutDeltaR->Fill(deltaR);
        hJetPhoDeltaPt->Fill(deltaPt); if (deltaR < 0.15 )  hJetPhoCutDeltaPt->Fill(deltaPt);
    }
    // fill genjet genpho matching variables end

    FillStatus(hNumMatchedJet_eachEvent,9); // as the total entries

    
    bool event_failed_offical_gen_matching =  FailedOfficalGenMatching(this);
    const std::vector<int>& matched_jet_idxs = GenJetIdxMatchedToGenPho(this, mcPho, mcPhoIdx);

    int matchJetNum = Interpreter_GenJetMatchingMultiplicity(
            event_failed_offical_gen_matching, matched_jet_idxs);
    int matchJetIdx = Interpreter_GenJetIdx(
            event_failed_offical_gen_matching, matched_jet_idxs);
    
    // testing for components before matchJetIdx
    if (!event_failed_offical_gen_matching )
        for ( int iJet = 0; iJet < matchJetIdx; ++iJet )
        {
            checkerplot->Fill(jetGenPartonID->at(iJet));
            hSuperLeadingPt    ->Fill(jetGenJetPt->at(iJet));
            hSuperLeadingPtDiff->Fill(jetGenJetPt->at(iJet) - jetGenJetPt->at(matchJetIdx));
        }


    FillStatus(hNumMatchedJet_eachEvent,matchJetNum);
    FillStatus(hMatchJetIdxWithMomID,matchJetIdx);

    int isLeadingJet = IsLeadingJet(this, mcPho, matchJetIdx);
    FillStatus(hIsLeadingJet,isLeadingJet);
    if ( matchJetIdx < 0 ) continue;


    // skip event failed offical jet-parton matching
    if ( abs(jetGenPartonID->at(matchJetIdx)) < 4 || jetGenPartonID->at(matchJetIdx) == 21 )
      hGenLyield->Fill( jetGenPt->at(matchJetIdx) );
    if ( abs(jetGenPartonID->at(matchJetIdx)) == 5 )
      hGenByield->Fill( jetGenPt->at(matchJetIdx) );
    if ( abs(jetGenPartonID->at(matchJetIdx)) == 4 )
      hGenCyield->Fill( jetGenPt->at(matchJetIdx) );
  }


  //auto newfile = new TFile("output.root", "RECREATE");
  auto newfile = new TFile(outputFILEname, "RECREATE");
  newfile->cd();

  auto dir_pho_match = newfile->mkdir("matching_to_gen_reco_photon");
  dir_pho_match->cd();
  hDeltaR->Write();
  hDeltaPt->Write();
  hCutDeltaR->Write();
  hCutDeltaPt->Write();

  auto dir_jet_pho_match = newfile->mkdir("matching_to_gen_jet_gen_photon");
  dir_jet_pho_match->cd();
  hMatchJetIdxWithMomID->Write();
  hNumMatchedJet_eachEvent->Write();
  hIsLeadingJet->Write();
  hSuperLeadingPt    ->Write();
  hSuperLeadingPtDiff->Write();

  hJetPhoDeltaR->Write();
  hJetPhoDeltaPt->Write();
  hJetPhoCutDeltaR->Write();
  hJetPhoCutDeltaPt->Write();


  newfile->cd();
  checkerplot->Write();
  hGenLyield->Write();
  hGenCyield->Write();
  hGenByield->Write();

  newfile->Close();
}

void PrintHelp()
{
  printf("Input argument : \n \
    Arg1: output filename \n \
    Arg2~N: ggNtuples root file \n \
    "
  );
  throw;
}

#include <cstring> // for strtok

std::vector<const char*> splitByComma(const char* input) {
    std::vector<const char*> result;
    char* str = new char[strlen(input) + 1]; // Create a mutable copy of the input string
    strcpy(str, input); // Copy the input string to the mutable string

    char* token = strtok(str, ",");
    while (token != nullptr) {
        result.push_back(token); // Store the token in the vector
        token = strtok(nullptr, ",");
    }

    // No need to delete str because the pointers in result still point to this memory
    return result;
}

int main(int argc, char* argv[])
{
  if ( argc < 3 )
    PrintHelp();
  const char* outputFILEname = argv[1];

  TChain* chain = new TChain("ggNtuplizer/EventTree");
  for ( const char* filename : splitByComma(argv[2]) )
      chain->Add(filename);
  // for (int i=2; i<argc; ++i)
  //   chain->Add(argv[i]);

  hi a(chain);
  a.Loop(outputFILEname);

  return 0;
}
