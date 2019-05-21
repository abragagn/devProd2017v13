import FWCore.ParameterSet.Config as cms

process = cms.PSet()

filename = open('pat_files.list', 'r')
filelist = cms.vstring( filename.readlines() )

process.fwliteInput = cms.PSet(
    fileNames   = filelist,               ## mandatory
    maxEvents   = cms.int32(1000),        ## optional, use maxEvents<=0
                                          ##           to read all events
    outputEvery = cms.uint32(10),         ## optional (usage not clear...)
)
    
process.pdAnalyzer = cms.PSet(

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
    ## (default ptCut=40GeV)
    ptCut = cms.double( 10.0 )

)


