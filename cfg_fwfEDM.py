import FWCore.ParameterSet.Config as cms

process = cms.Process("pdAnalysis")

process.load("FWCore.MessageService.MessageLogger_cfi")

# Quiet Mode or event dump
#process.MessageLogger.cerr.threshold = 'ERROR'
process.MessageLogger.cerr.threshold = 'WARNING'
#process.MessageLogger.cerr.FwkReport.reportEvery = 10000

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

### define here a list of PAT files containing muons
#filename = open('pat_files.list', 'r')
#fileList = cms.untracked.vstring( filename.readlines() )

#process.source = cms.Source ("PoolSource", fileNames=fileList)
process.source = cms.Source("EmptyIOVSource",
    timetype   = cms.string('runnumber'),
    firstValue = cms.uint64(123456),
    lastValue  = cms.uint64(124456),
    interval   = cms.uint64(1)
)

#process.evNumFilter = cms.EDFilter('EvNumFilter',
#    eventList = cms.string('evList')
#)

process.pdAnalyzer = cms.EDProducer('PDEDMNtuplizer',

    ## mandatory
    ## histogram file name
    histName = cms.untracked.string('test_his.root'),

    ## optional
#    eventList = cms.string('evtlist'),
#    listType = cms.string('skip'),

    verbose = cms.untracked.bool(True),

#    labelMuons        = cms.string('calibratedPatMuonsPFlow'),
#    labelJets         = cms.string('selectedPatJetsLooseIDUserDataPFlow'),
    labelMuons        = cms.string('RANDOM'),

    ## select events with at least a muon with pT > 10 GeV
    ## (default ptCut=40GeV)
    ptCut = cms.double( 10.0 )

)

process.pdFilter = cms.EDFilter('EDMNtupleFilter')
process.p = cms.Path(#process.evNumFilter *
                     process.pdAnalyzer * process.pdFilter)

process.out = cms.OutputModule(
    "PoolOutputModule",
    outputCommands = cms.untracked.vstring(
      "drop *",
      "keep *_pdAnalyzer_*_*"      
    ),
    fileName = cms.untracked.string('test_edm.root'),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('p')
    )
)


process.e = cms.EndPath(process.out)

