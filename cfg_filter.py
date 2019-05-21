import FWCore.ParameterSet.Config as cms

process = cms.Process("pdSelect")

process.load("FWCore.MessageService.MessageLogger_cfi")

# Quiet Mode or event dump
#process.MessageLogger.cerr.threshold = 'ERROR'
process.MessageLogger.cerr.threshold = 'WARNING'
#process.MessageLogger.cerr.FwkReport.reportEvery = 10000

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

filename = open('pat_files.list', 'r')
fileList = cms.untracked.vstring( filename.readlines() )

process.source = cms.Source ("PoolSource", fileNames=fileList)

#process.evNumFilter = cms.EDFilter('EvNumFilter',
#    eventList = cms.string('evList')
#)

process.pdFilter = cms.EDFilter('PDFilter',

    ## mandatory
    ## ntuple file name: empty string to drop ntuple filling
    ntuName = cms.untracked.string('test_ntu.root'),
    ## histogram file name
    histName = cms.untracked.string('test_his.root'),

    ## optional
#    eventList = cms.string('evtlist'),
#    listType = cms.string('skip'),

    verbose = cms.untracked.bool(True),

    labelMuons        = cms.string('calibratedPatMuonsPFlow'),
    labelJets         = cms.string('selectedPatJetsLooseIDUserDataPFlow'),

    ## select events with at least a muon with pT > 10 GeV
    ## (default ptCut=70GeV)
    ptCut = cms.double( 10.0 )

)


process.p = cms.Path(#process.evNumFilter *
                     process.pdFilter)

process.out = cms.OutputModule("PoolOutputModule",
    outputCommands = cms.untracked.vstring('keep *_*_*_HLT',
                                           'keep *_*_*_RECO',
                                           'keep *_*_*_PAT' ,
                                           'drop *_*_*_pdSelect'),
#                                           'drop *_puJetId_*_*',
#  output file name:
    fileName = cms.untracked.string('selPAT.root'),   
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('p')
    )
)
process.e = cms.EndPath(process.out)
