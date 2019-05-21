#include <memory>
#include <string>
#include <vector>
#include <sstream>
#include <fstream>
#include <iostream>
#include <iomanip>

#include <TH1F.h>
#include <TH2F.h>
#include <TROOT.h>
#include <TFile.h>
#include <TSystem.h>

#include "DataFormats/FWLite/interface/Event.h"
#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/FWLite/interface/AutoLibraryLoader.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "PhysicsTools/FWLite/interface/TFileService.h"
#include "PhysicsTools/FWLite/interface/CommandLineParser.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/PythonParameterSet/interface/MakeParameterSets.h"
#include "DataFormats/FWLite/interface/InputSource.h"
#include "DataFormats/FWLite/interface/OutputFiles.h"

#include "NtuAnalysis/Write/interface/NtuEDConsumer.h"
#include "PDAnalysis/EDM/interface/PDEDMToNtuple.h"
#include "NtuAnalysis/Write/interface/NtuWriteInterface.h"

using namespace std;

int main( int argc, char* argv[] ) {

  // load framework libraries
  gSystem->Load( "libFWCoreFWLite" );
  AutoLibraryLoader::enable();

  // initialize command line parser
  optutl::CommandLineParser parser ("Analyze Skims");

  // set defaults
  parser.integerValue( "maxEvents"   ) = 10;
  parser.integerValue( "outputEvery" ) = 1;
  parser.stringValue ( "outputFile"  ) = "hist.root";

  parser.addOption( "cfg", optutl::CommandLineParser::kString, "", ".py file" );
  // parse arguments
  parser.parseArguments ( argc, argv );

  vector<string> inputFiles_;
  int maxEvents_ = 0;
//  unsigned int outputEvery_ = 999999;
  string outputFile_;

  const edm::ParameterSet* pps = 0;
  string cfg = parser.stringValue( "cfg" );
  if ( edm::readPSetsFrom( cfg )->existsAs<edm::ParameterSet>( "process" ) ) {
    // get the python configuration
    const edm::ParameterSet& process =
          edm::readPSetsFrom( cfg )
          ->getParameter<edm::ParameterSet>( "process" );
    fwlite::InputSource  inputHandler_( process );
//    fwlite::OutputFiles outputHandler_( process );
    pps = new edm::ParameterSet( process.getParameter<edm::ParameterSet>(
                                 "pdAnalyzer" ) );
    inputFiles_ = inputHandler_.files();
    outputFile_ = pps->getUntrackedParameter<string>( "histName" );
//    outputFile_ = outputHandler_.file();
    maxEvents_ = inputHandler_.maxEvents();
  }
  else {
    maxEvents_ = parser.integerValue( "maxEvents" );
//    outputEvery_ = parser.integerValue( "outputEvery" );
    outputFile_  = parser.stringValue ( "outputFile"  );
    inputFiles_.push_back( "dcap://t2-srm-02.lnl.infn.it/pnfs/lnl.infn.it/data/cms/store/user/slacapra/AZh_Prod6//TTJets_SemiLeptMGDecays_8TeV-madgraph-tauola/patTuple_PF2PAT_1_1_ref.root" );
    pps = new edm::ParameterSet;
  }

//  fwlite::TFileService fs = fwlite::TFileService( outputFile_.c_str() );

  cout << "create writer/analyzer" << endl;
  NtuEDConsumer<edm::EDAnalyzer>* dumPtr = 0;
  NtuWriteInterface<PDEDMToNtuple>* ntu = new NtuWriteInterface<PDEDMToNtuple>( *pps, dumPtr );

  ntu->beginJob();

  unsigned int iFile;
  bool endAna = false;
  for ( iFile = 0; iFile < inputFiles_.size(); ++iFile ) {
    string& fileName = inputFiles_[iFile];
    fileName = fileName.substr( 0, fileName.find( "\n" ) );
  }
  for ( iFile = 0; iFile < inputFiles_.size(); ++iFile ) {
    cout << "---->" << inputFiles_[iFile].c_str() << "<----" << endl;
    // loop the events
    // open input file 
    TFile* inFile = TFile::Open( inputFiles_[iFile].c_str() );
    if ( inFile ) {
      fwlite::Event ev( inFile );
      // loop the events in the input file 
      int ientry = 0;
      int analyzedFile = 0;
      for ( ev.toBegin(); !ev.atEnd(); ++ev ) {
        edm::EventBase const & event = ev;
        ntu->analyzeEDM( event, ientry++, analyzedFile++ );
        if ( ( endAna = ( ( maxEvents_ > 0 ) &&
                          ( ntu->analyzedEvents() >= maxEvents_ ) ) ) ) break;
      } // end event loop  
      inFile->Close();
    }
    // break loop if maximal number of events is reached:
    // this has to be done twice to stop the file loop as well
    if ( endAna ) break;
  }
  ntu->endJob();
  TreeWrapper* ntt = ntu;
  ntt->save( outputFile_.c_str() );

  return 0;
}

