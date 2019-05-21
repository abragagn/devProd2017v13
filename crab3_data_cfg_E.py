from WMCore.Configuration import Configuration
config = Configuration()

config.section_('General')

###### set here a name for this task
config.General.requestName = 'Charmonium_Run2017E'
#request name is the name of the folder where crab log is saved

config.General.workArea = 'crab3_projects'
config.General.transferOutputs = True

config.section_('JobType')

###### specify here the .py config file to run
config.JobType.psetName = 'cfg_data_mini.py'

config.JobType.pluginName = 'Analysis'
config.JobType.outputFiles = ['ntu.root']
config.JobType.allowUndistributedCMSSW = True

config.section_('Data')

###### specify here the dataset to process
config.Data.inputDataset = '/Charmonium/Run2017E-31Mar2018-v1/MINIAOD'

###### specify here the JSON file to use
config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions17/13TeV/Final/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'

config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
#NJOBS = 200  # This is not a configuration parameter, but an auxiliary variable that we use in the next line.
#config.Data.totalUnits = config.Data.unitsPerJob * NJOBS

###### set here the path of a storage area you can write to
config.Data.outLFNDirBase = '/store/user/abragagn'
config.Data.publication = False

############## 

#config.Data.ignoreLocality = True

config.section_("Site")

###### set here a storage site you can write to
config.Site.storageSite = 'T2_IT_Legnaro'





